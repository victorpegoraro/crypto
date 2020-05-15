#! /usr/bin/env python

# Developer: Victor pegoraro

from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
from requests import Request, Session
from datetime import datetime
import PySimpleGUI as sg
import json, colorama


def tudo(convert):

    #Call api
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    parameters = {
        'start':'1',
        'limit':'3000',
        'convert': convert
    }
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': '9f7d4451-fda2-4a7d-891e-3c66a35e7085',#Insert your api key
    }

    #Create session
    session = Session()
    session.headers.update(headers)

    table = []

    #Get results from api
    try:
        response = session.get(url, params=parameters)
        data  = json.loads(response.text)
        currencys = data['data']

        #Get values
        for currency in currencys:
            rank = currency['cmc_rank']
            name = currency['name']
            symbol = currency['symbol']
            last_updated = currency['last_updated']
            quotes = currency['quote'][convert]
            price = quotes['price'] 

            #Add valoues to table
            table.append(str(rank) + "   " +  name + ' (' + symbol + ')' +
                        '          $ ' + 
                        str(price) + 
                        "          " +
                        str(last_updated))

            table.append("-" * 150)
        
        #Show table
        return table
    
    except:
        return "Moeda não identificada"



def convert(convert,moeda):

    #Call api
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    parameters = {
        'start':'1',
        'limit':'3000',
        'convert': convert
    }
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': '9f7d4451-fda2-4a7d-891e-3c66a35e7085',#Insert your api key
    }

    #Create session
    session = Session()
    session.headers.update(headers)

    #Get response from api
    try:
        response = session.get(url, params=parameters)
        data  = json.loads(response.text)
        currencys = data['data']
        print("API funciona")
        #Find coin to convert
        for currency in currencys:
            name = currency['name']
            if(name == moeda):
                name = currency['name']
                symbol = currency['symbol']
                last_updated = currency['last_updated']
                quotes = currency['quote'][convert]
                price = quotes['price'] 

                resultado = name + ' (' + symbol + ')' + " = " + '$' + str(price) + "  " + str(last_updated)
                return resultado
    except:
        return "Valores não foram identificados"

def main():
    sg.theme('DarkTeal9')	# Add a touch of color

    layout = [  [sg.Text('Conversor de cripto moeda.')],
                [sg.Text('Moeda [BRL,USD]:',size=(15,1)), sg.Input(key='moeda'),sg.Text('',size=(1,1)), sg.Button('Lista',size=(15,2))],
                [sg.Text('Coin [Bitcoin,Nano]:',size=(15,1)), sg.Input(key='crypto')],
                [sg.Text(size=(60,1)),sg.Text("Ultima atualização")],
                [sg.Button('Converter',size=(15,2)), sg.Text('Resultado:'), sg.Text(size=(50,1), key='-OUTPUT-')]]

    window = sg.Window('Crypto', layout)
    while True:  # Event Loop
        event, values = window.read()
        print(event, values)
        if event in  (None, 'Sair'):
            break

        if event == 'Converter':
            # Update the "output" text element to be the value of "input" element
            resultado = convert(values['moeda'].upper(),values['crypto'].capitalize())
            window['-OUTPUT-'].update(resultado)

        if event == 'Lista':
            break
            

    window.close()
    if event == 'Lista':
        moeda = "BRL"
        lista(moeda)

def lista(moeda):

    layout1 = [ [sg.Text('Lista')],
                [sg.Text('Moeda [BRL,USD]:', size=(15,1)), sg.Input(key='cash'), sg.Button('Atualizar')],
                [sg.Text('Coin', size=(20,1)),sg.Text(f'Valor {moeda}', size=(20,1)),sg.Text('Ultima atualização', size=(20,1))],
                [sg.Listbox(values=tudo(moeda), size=(100, 30), key='-LIST-', enable_events=True)],
                [sg.Button('Voltar'),sg.Text('',size=(1,1)), sg.Button('Check'), sg.Text('',size=(1,1)), sg.Button('Sair')]]

    window1 = sg.Window('Crypto', layout1)

    while True:  # Event Loop
        event, values = window1.read()
        if event in (None, 'Sair'):
            break

        if event == "Check":
            try:
                sg.popup(' {}'.format(values['-LIST-'][0]))
            except IndexError:
                sg.popup('$$ Selecione um item na lista $$')

        if event == 'Voltar':
            break

        if event == 'Atualizar':
            break

    window1.close()
    if event == 'Voltar':
        main()

    if event == 'Atualizar':
        lista(values['cash'].upper())

main()

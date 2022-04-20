from dotenv import load_dotenv
import os, json, time, ccxt

load_dotenv()  # Take environment variables from .env

binance = ccxt.binance({
    'apiKey': os.getenv('API_KEY'),
    'secret': os.getenv('API_SECRET'),
})

portfolio = binance.fetch_balance() # This returns a dictionary of the assets in your portfolio
#print(json.dumps(portfolio, indent=4)) 

SOL_USDT = binance.markets['SOL/USDT']  # This returns the binance solana market object
#print(json.dumps(SOL_USDT, indent=4))

try:
    margin = portfolio["USDT"]["free"]
    # This gets the free USDT in your account

    amount = margin / binance.fetchTicker("SOL/USDT")["last"]
    # This computes the amount of SOL you can buy with the free USDT based on the last price

    amount = float(binance.amount_to_precision("SOL/USDT", amount))
    # This converts the calculated amount to appropriate amount of decimals accepted by the exchange

    if amount < SOL_USDT["limits"]["amount"]["min"]:
        print("Cannot place order, Not up to minimum tradeable amount")

    else:
        order = binance.create_order("SOL/USDT", 'market', 'buy', amount)
        if order:
            print(f"Successfully purchased {amount} of SOL")

       
except Exception as E:
    print(f"Error encountered when buying: {str(E)}")
    # Simply checking any errors that might have occurred in the try block
    
time.sleep(10)

try:
    margin = portfolio["SOL"]["free"]
    amount = float(binance.amount_to_precision("SOL/USDT", margin))

    if amount < SOL_USDT["limits"]["amount"]["min"]:
        print("Cannot place order, Not up to minimum tradeable amount")

    else:
        order = binance.create_order("SOL/USDT", 'market', 'sell', amount)
        if order:
            print(f"Successfully sold {amount} of SOL")

except Exception as E:
    print(f"Error encountered when selling: {str(E)}")
    # Simply checking any errors that might have occurred in the try block
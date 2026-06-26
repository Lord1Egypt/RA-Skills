import sys
import argparse
import json

try:
    import yfinance as yf
except ImportError:
    print(json.dumps({"error": "Dependency missing. Please run 'pip install yfinance'"}))
    sys.exit(1)

def get_earnings(ticker):
    try:
        stock = yf.Ticker(ticker)
        earnings = stock.calendar
        if earnings is not None:
            # Handle DataFrame or Dict conversion
            return json.dumps(earnings if isinstance(earnings, dict) else earnings.to_dict(), default=str)
        return json.dumps({"error": f"No earnings data found for {ticker}"})
    except Exception as e:
        return json.dumps({"error": str(e)})

def get_financials(ticker):
    try:
        stock = yf.Ticker(ticker)
        financials = stock.quarterly_financials
        if financials is not None and not financials.empty:
            return financials.iloc[:, 0].to_json()
        return json.dumps({"error": f"No financial data found for {ticker}"})
    except Exception as e:
        return json.dumps({"error": str(e)})

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--tool", required=True)
    parser.add_argument("--ticker", required=True)
    args = parser.parse_args()

    if args.tool == "get_earnings":
        print(get_earnings(args.ticker))
    elif args.tool == "get_financials":
        print(get_financials(args.ticker))

import requests
import json
import sys

def get_klines(symbol, interval, limit=500):
    base_url = "https://api.binance.com/api/v3/klines"
    params = {
        "symbol": symbol.upper(),
        "interval": interval,
        "limit": limit
    }
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()  # Raise an exception for HTTP errors
        klines = response.json()
        
        # Format the klines data for easier use
        formatted_klines = []
        for kline in klines:
            formatted_klines.append({
                "open_time": kline[0],
                "open": float(kline[1]),
                "high": float(kline[2]),
                "low": float(kline[3]),
                "close": float(kline[4]),
                "volume": float(kline[5]),
                "close_time": kline[6],
                "quote_asset_volume": float(kline[7]),
                "number_of_trades": kline[8],
                "taker_buy_base_asset_volume": float(kline[9]),
                "taker_buy_quote_asset_volume": float(kline[10]),
                "ignore": float(kline[11])
            })
        return formatted_klines
    except requests.exceptions.RequestException as e:
        print(json.dumps({"error": str(e)}))
        sys.exit(1)
    except Exception as e:
        print(json.dumps({"error": f"An unexpected error occurred: {e}"}))
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(json.dumps({"error": "Usage: python get_binance_data.py <symbol> <interval> [limit]"}))
        sys.exit(1)
    
    symbol = sys.argv[1]
    interval = sys.argv[2]
    limit = int(sys.argv[3]) if len(sys.argv) > 3 else 500
    
    data = get_klines(symbol, interval, limit)
    print(json.dumps(data))

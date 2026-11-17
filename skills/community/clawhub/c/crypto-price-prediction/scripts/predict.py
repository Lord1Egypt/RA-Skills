#!/usr/bin/env python3
"""Fetch next-hour predicted price for BTC/ETH from external API."""
import sys
import argparse
import urllib.request
import urllib.error
import json
import os
from datetime import datetime, timezone, timedelta

API_BASE = "https://myfastapi.zeabur.app/v1/demo/predictions/next_hour"
COINGECKO_API = "https://api.coingecko.com/api/v3/simple/price"
VALID_COINS = ["BTC", "ETH"]
COINGECKO_IDS = {"BTC": "bitcoin", "ETH": "ethereum"}

# Config file for user timezone
CONFIG_DIR = os.path.expanduser("~/.config/crypto-price-prediction")
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.json")

def get_user_timezone():
    """Get user's timezone from config, or prompt if first run."""
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r') as f:
                config = json.load(f)
                return config.get('timezone', 'GMT')
        except Exception:
            pass
    
    # First run - prompt for timezone
    print("First run detected. Please enter your timezone (e.g., HKT, UTC, America/New_York).")
    print("Press Enter to use GMT (UTC) as default:")
    try:
        tz = input("Timezone: ").strip()
        if not tz:
            tz = "GMT"
    except (EOFError, KeyboardInterrupt):
        tz = "GMT"
    
    # Save config
    os.makedirs(CONFIG_DIR, exist_ok=True)
    with open(CONFIG_FILE, 'w') as f:
        json.dump({"timezone": tz}, f)
    
    return tz

def get_tz_info(tz_name):
    """Get timezone offset and display name."""
    tz_name = tz_name.upper()
    if tz_name in ('HKT', 'HONG_KONG', 'ASIA/HONG_KONG'):
        return timezone(timedelta(hours=8)), 'HKT'
    elif tz_name in ('GMT', 'UTC'):
        return timezone.utc, 'GMT'
    else:
        # Try to parse as offset like "+08:00" or "-05:00"
        try:
            if tz_name.startswith(('+', '-')):
                sign = 1 if tz_name[0] == '+' else -1
                parts = tz_name[1:].split(':')
                hours = int(parts[0])
                minutes = int(parts[1]) if len(parts) > 1 else 0
                return timezone(timedelta(hours=sign*hours, minutes=sign*minutes)), tz_name
        except Exception:
            pass
        # Default to UTC
        return timezone.utc, 'GMT'

def get_hour_start(dt):
    """Get the start of the current hour (minute=0, second=0)."""
    return dt.replace(minute=0, second=0, microsecond=0)

def fetch_prediction(coin: str) -> float:
    url = f"{API_BASE}/{coin.upper()}"
    req = urllib.request.Request(url, headers={"User-Agent": "crypto-price-prediction/1.0.1"})
    with urllib.request.urlopen(req, timeout=10) as resp:
        data = json.loads(resp.read().decode())
        key = f"{coin.upper()} predicted price (next_hour)"
        return data[key]

def fetch_current_price(coin: str) -> float:
    """Fetch current price from CoinGecko."""
    cg_id = COINGECKO_IDS[coin]
    url = f"{COINGECKO_API}?ids={cg_id}&vs_currencies=usd"
    req = urllib.request.Request(url, headers={"User-Agent": "crypto-price-prediction/1.0.1"})
    with urllib.request.urlopen(req, timeout=10) as resp:
        data = json.loads(resp.read().decode())
        return data[cg_id]['usd']

def format_price(price):
    """Format price with 2 decimal places and commas."""
    return f"{price:,.2f}"

def main():
    parser = argparse.ArgumentParser(description="Fetch next-hour predicted price")
    parser.add_argument("--coin", required=True, choices=VALID_COINS, help="Coin: BTC or ETH")
    parser.add_argument("--timezone", help="User timezone (e.g., HKT, UTC, America/New_York)")
    args = parser.parse_args()

    # Get timezone
    if args.timezone:
        tz_name = args.timezone
        # Save to config
        os.makedirs(CONFIG_DIR, exist_ok=True)
        with open(CONFIG_FILE, 'w') as f:
            json.dump({"timezone": tz_name}, f)
    else:
        tz_name = get_user_timezone()
    
    tz, tz_display = get_tz_info(tz_name)
    
    # Get current time in user's timezone
    now = datetime.now(tz)
    hour_start = get_hour_start(now)
    next_hour = hour_start + timedelta(hours=1)
    
    # Fetch prediction
    try:
        predicted_price = fetch_prediction(args.coin)
    except urllib.error.HTTPError as e:
        print(f"API error ({e.code}): {e.read().decode()}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error fetching prediction: {e}", file=sys.stderr)
        sys.exit(1)
    
    # Fetch current price (at hour start)
    current_price = None
    try:
        current_price = fetch_current_price(args.coin)
    except Exception as e:
        print(f"Warning: Could not fetch current price: {e}", file=sys.stderr)
    
    # Determine direction
    predicted_direction = None
    if current_price is not None:
        if current_price < predicted_price:
            predicted_direction = "UP"
        else:
            predicted_direction = "DOWN"
    
    # Build unified JSON output
    output = {
        "timestamp": next_hour.strftime(f"%Y-%m-%d %H:%M {tz_display}"),
        "symbol": f"{args.coin}USDT",
        "horizonHours": 1,
        "currentPrice": round(current_price, 2) if current_price is not None else None,
        "predictedPrice": round(predicted_price, 2),
        "predictedDirection": predicted_direction
    }
    
    # Print JSON (for programmatic use)
    print(json.dumps(output, ensure_ascii=False))
    
    # Also print verbal output if all fields populated
    if current_price is not None and predicted_direction is not None:
        print()
        print(f"Current price of {args.coin} at {hour_start.strftime(f'%Y-%m-%d %H:%M {tz_display}')}: {format_price(current_price)}")
        print(f"Predicted price of {args.coin} at {next_hour.strftime(f'%Y-%m-%d %H:%M {tz_display}')}: {format_price(predicted_price)}")
        print(f"Predicted direction of {args.coin} in the next hour: {predicted_direction}")

if __name__ == "__main__":
    main()
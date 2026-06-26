#!/usr/bin/env python3
"""
BTC Price Monitor for OpenClaw
Fetches Bitcoin price from CoinGecko and sends to Telegram
"""

import os
import requests
import sys
from datetime import datetime

# ==================================================
# CONFIGURATION - REPLACE WITH YOUR VALUES
# ==================================================

TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "YOUR_CHAT_ID_HERE")
PRICE_THRESHOLD = float(os.environ.get("PRICE_THRESHOLD_USD", "50000"))

# ==================================================


def get_btc_price():
    """Fetch current BTC price from CoinGecko (free, no API key)"""
    try:
        url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
        response = requests.get(url, timeout=10)
        data = response.json()
        return data["bitcoin"]["usd"]
    except Exception as e:
        return f"Error fetching price: {e}"


def send_telegram_message(message):
    """Send message to Telegram"""
    if TELEGRAM_BOT_TOKEN == "YOUR_BOT_TOKEN_HERE" or TELEGRAM_CHAT_ID == "YOUR_CHAT_ID_HERE":
        print("ERROR: Please set your TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID")
        return False

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }

    try:
        response = requests.post(url, json=payload, timeout=10)
        return response.status_code == 200
    except Exception as e:
        print(f"Failed to send Telegram message: {e}")
        return False


def format_message(price, threshold=None):
    """Format price message with optional alert"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")

    message = "[BTC] Bitcoin Price Update\n\n"
    message += f"Price: ${price:,.0f}\n"
    message += f"Time: {timestamp}\n"

    if threshold and price < threshold:
        message += f"\nALERT: Price dropped below ${threshold:,.0f}!"

    return message


def main():
    """Main entry point"""
    price = get_btc_price()

    if isinstance(price, str) and "Error" in price:
        send_telegram_message(f"[ERROR] {price}")
        sys.exit(1)

    threshold = PRICE_THRESHOLD if PRICE_THRESHOLD != 50000 else None
    message = format_message(price, threshold)

    success = send_telegram_message(message)

    if success:
        print(f"Sent: BTC price ${price:,.0f}")
    else:
        print("Failed to send message")
        sys.exit(1)


if __name__ == "__main__":
    main()
#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "requests>=2.28.0",
# ]
# ///
"""
Query real-time cryptocurrency prices (Binance API)

Usage:
    uv run cryptoprice.py [symbol]
    
Examples:
    uv run cryptoprice.py BTCUSDT    # Query Bitcoin price
    uv run cryptoprice.py ETHUSDT    # Query Ethereum price
    uv run cryptoprice.py            # Display popular coins
"""

import argparse
import json
import sys
from typing import Optional

try:
    import requests
except ImportError:
    print("Error: requests library required")
    print("Run: pip install requests")
    sys.exit(1)


BINANCE_API_URL = "https://api.binance.com/api/v3/ticker/price"

# List of popular cryptocurrencies
POPULAR_SYMBOLS = [
    "BTCUSDT",   # Bitcoin
    "ETHUSDT",   # Ethereum
    "BNBUSDT",   # Binance Coin
    "SOLUSDT",   # Solana
    "XRPUSDT",   # Ripple
    "DOGEUSDT",  # Dogecoin
    "ADAUSDT",   # Cardano
    "AVAXUSDT",  # Avalanche
    "DOTUSDT",   # Polkadot
    "LINKUSDT",  # Chainlink
]


def fetch_all_prices() -> dict:
    """Fetch prices for all symbols"""
    try:
        response = requests.get(BINANCE_API_URL, timeout=10)
        response.raise_for_status()
        data = response.json()
        return {item["symbol"]: item["price"] for item in data}
    except requests.RequestException as e:
        print(f"Failed to fetch prices: {e}", file=sys.stderr)
        sys.exit(1)


def fetch_single_price(symbol: str) -> Optional[str]:
    """Fetch price for a single symbol"""
    try:
        response = requests.get(f"{BINANCE_API_URL}?symbol={symbol.upper()}", timeout=10)
        response.raise_for_status()
        data = response.json()
        return data.get("price")
    except requests.RequestException as e:
        print(f"Failed to fetch {symbol} price: {e}", file=sys.stderr)
        return None


def format_price(symbol: str, price: str) -> str:
    """Format price for display"""
    price_float = float(price)
    
    # Choose precision based on price magnitude
    if price_float >= 1000:
        return f"${price_float:,.2f}"
    elif price_float >= 1:
        return f"${price_float:,.4f}"
    else:
        return f"${price_float:.8f}"


def get_symbol_name(symbol: str) -> str:
    """Get display name for a symbol"""
    names = {
        "BTCUSDT": "Bitcoin (BTC)",
        "ETHUSDT": "Ethereum (ETH)",
        "BNBUSDT": "Binance Coin (BNB)",
        "SOLUSDT": "Solana (SOL)",
        "XRPUSDT": "Ripple (XRP)",
        "DOGEUSDT": "Dogecoin (DOGE)",
        "ADAUSDT": "Cardano (ADA)",
        "AVAXUSDT": "Avalanche (AVAX)",
        "DOTUSDT": "Polkadot (DOT)",
        "LINKUSDT": "Chainlink (LINK)",
    }
    return names.get(symbol, symbol.replace("USDT", ""))


def main():
    parser = argparse.ArgumentParser(description="Query real-time cryptocurrency prices")
    parser.add_argument("symbol", nargs="?", help="Trading pair, e.g. BTCUSDT (default: show popular coins)")
    parser.add_argument("--json", "-j", action="store_true", help="Output in JSON format")
    parser.add_argument("--list", "-l", action="store_true", help="List all available trading pairs")
    
    args = parser.parse_args()
    
    if args.list:
        prices = fetch_all_prices()
        usdt_pairs = sorted([s for s in prices.keys() if s.endswith("USDT")])
        print("Available USDT trading pairs:")
        for pair in usdt_pairs[:50]:  # Show first 50 only
            print(f"  {pair}: {format_price(pair, prices[pair])}")
        if len(usdt_pairs) > 50:
            print(f"  ... {len(usdt_pairs) - 50} more pairs")
        return
    
    if args.symbol:
        # Query single coin
        symbol = args.symbol.upper()
        # Auto-complete to USDT if not a complete trading pair
        # Logic: if symbol is short (<=5) and doesn't end with quote currency, append USDT
        quote_currencies = ["USDT", "USDC", "FDUSD"]
        is_fiat_pair = any(symbol.endswith(q) for q in quote_currencies)
        is_crypto_pair = symbol.endswith("BTC") or symbol.endswith("ETH") or symbol.endswith("BNB")
        
        # If neither fiat pair nor crypto pair, append USDT
        if not is_fiat_pair and not is_crypto_pair:
            symbol = f"{symbol}USDT"
        # Special case: if input is just "BTC"/"ETH"/"BNB", also append USDT
        elif is_crypto_pair and len(symbol) <= 5:
            symbol = f"{symbol}USDT"
        
        price = fetch_single_price(symbol)
        if price:
            if args.json:
                print(json.dumps({"symbol": symbol, "price": price}, indent=2))
            else:
                print(f"{get_symbol_name(symbol)}: {format_price(symbol, price)}")
        else:
            print(f"Price info not found for {symbol}")
            sys.exit(1)
    else:
        # Display popular coins
        prices = fetch_all_prices()
        
        if args.json:
            result = {}
            for symbol in POPULAR_SYMBOLS:
                if symbol in prices:
                    result[symbol] = prices[symbol]
            print(json.dumps(result, indent=2))
        else:
            print("💰 Popular Cryptocurrency Prices (Binance)")
            print("-" * 40)
            for symbol in POPULAR_SYMBOLS:
                if symbol in prices:
                    name = get_symbol_name(symbol)
                    price = format_price(symbol, prices[symbol])
                    print(f"{name:<20} {price:>15}")
            print("-" * 40)
            print("Tip: Use --json for JSON output, or specify a coin like BTCUSDT")


if __name__ == "__main__":
    main()

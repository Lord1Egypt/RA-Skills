#!/usr/bin/env python3
"""
crypto-price-alerter: Price check script
Fetches current crypto price data from CoinGecko free API.
Usage: uv run python scripts/price_check.py --symbol BTC --currency USD
"""

import argparse
import json
import sys
import requests
from datetime import datetime, timezone

# CoinGecko API endpoints
COINGECKO_SEARCH_URL = "https://api.coingecko.com/api/v3/search"
COINGECKO_PRICE_URL = "https://api.coingecko.com/api/v3/simple/price"
COINGECKO_COINS_URL = "https://api.coingecko.com/api/v3/coins"


def search_coin(symbol: str) -> str | None:
    """Search for a coin by symbol and return its CoinGecko ID."""
    try:
        resp = requests.get(COINGECKO_SEARCH_URL, params={"query": symbol}, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        coins = data.get("coins", [])
        # Match by exact symbol (case-insensitive)
        symbol_lower = symbol.lower()
        for coin in coins:
            if coin.get("symbol", "").lower() == symbol_lower:
                return coin.get("id")
        # Fallback: return first match
        if coins:
            return coins[0].get("id")
        return None
    except Exception as e:
        print(f"Search error: {e}", file=sys.stderr)
        return None


def get_price_data(coin_id: str, currency: str = "usd") -> dict | None:
    """Fetch current price and market data for a coin."""
    try:
        params = {
            "ids": coin_id,
            "vs_currencies": currency,
            "include_24hr_vol": "true",
            "include_24hr_change": "true",
            "include_market_cap": "true",
        }
        resp = requests.get(COINGECKO_PRICE_URL, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        coin_data = data.get(coin_id, {})
        if not coin_data:
            return None

        price = coin_data.get(currency, 0)
        change_24h = coin_data.get(f"{currency}_24h_change", 0)
        volume_24h = coin_data.get(f"{currency}_24h_vol", 0)
        market_cap = coin_data.get(f"{currency}_market_cap", 0)

        return {
            "coin_id": coin_id,
            "currency": currency.upper(),
            "price": price,
            "change_24h_percent": round(change_24h, 2),
            "volume_24h": round(volume_24h, 2),
            "market_cap": round(market_cap, 2),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as e:
        print(f"Price fetch error: {e}", file=sys.stderr)
        return None


def get_historical_prices(coin_id: str, currency: str = "usd", days: int = 7) -> list | None:
    """Fetch historical price data for moving average calculation."""
    try:
        url = f"{COINGECKO_COINS_URL}/{coin_id}/market_chart"
        params = {
            "vs_currency": currency,
            "days": days,
        }
        resp = requests.get(url, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        prices = data.get("prices", [])
        # Return list of [timestamp_ms, price]
        return prices[-30:] if len(prices) > 30 else prices
    except Exception as e:
        print(f"Historical fetch error: {e}", file=sys.stderr)
        return None


def calculate_sma(prices: list, period: int = 7) -> float | None:
    """Calculate Simple Moving Average from price list."""
    if not prices or len(prices) < period:
        return None
    # prices is list of [timestamp_ms, price]
    recent = prices[-period:]
    avg = sum(p[1] for p in recent) / len(recent)
    return round(avg, 2)


def calculate_rsi(prices: list, period: int = 14) -> float | None:
    """Calculate basic RSI from price list."""
    if not prices or len(prices) < period + 1:
        return None
    # prices is list of [timestamp_ms, price]
    gains = []
    losses = []
    for i in range(1, min(len(prices), period + 1)):
        change = prices[i][1] - prices[i - 1][1]
        if change > 0:
            gains.append(change)
        else:
            losses.append(abs(change))

    if not losses:
        return 100.0
    avg_gain = sum(gains) / len(gains) if gains else 0
    avg_loss = sum(losses) / len(losses)
    if avg_loss == 0:
        return 100.0
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return round(rsi, 1)


def estimate_support_resistance(prices: list) -> dict:
    """Estimate simple support/resistance from recent price range."""
    if not prices:
        return {"resistance": None, "support": None}
    recent = prices[-30:] if len(prices) > 30 else prices
    high = max(p[1] for p in recent)
    low = min(p[1] for p in recent)
    return {
        "resistance_30d": round(high, 2),
        "support_30d": round(low, 2),
    }


def generate_alert(price_data: dict, thresholds: dict = None) -> list:
    """Generate alerts based on price data and optional thresholds."""
    alerts = []
    if not price_data:
        return alerts

    price = price_data["price"]
    change = price_data["change_24h_percent"]

    # Trend alerts
    if change > 5:
        alerts.append(f"ALERT: {price_data['coin_id']} up {change}% in 24h!")
    elif change < -5:
        alerts.append(f"ALERT: {price_data['coin_id']} down {abs(change)}% in 24h!")

    # Threshold alerts if provided
    if thresholds:
        upper = thresholds.get("upper")
        lower = thresholds.get("lower")
        if upper and price >= upper:
            alerts.append(f"PRICE ALERT: {price_data['coin_id']} hit ${price} (above upper threshold ${upper})!")
        if lower and price <= lower:
            alerts.append(f"PRICE ALERT: {price_data['coin_id']} hit ${price} (below lower threshold ${lower})!")

    return alerts


def build_report(price_data: dict, sma_7: float = None, sma_21: float = None,
                 rsi: float = None, sr_levels: dict = None, thresholds: dict = None) -> str:
    """Build a formatted summary report."""
    coin = price_data["coin_id"].upper()
    currency = price_data["currency"]
    price = price_data["price"]
    change = price_data["change_24h_percent"]
    volume = price_data["volume_24h"]
    market_cap = price_data["market_cap"]
    ts = price_data["timestamp"]

    # Trend indicator
    # Trend indicator
    trend = "^" if change >= 0 else "v"
    trend_text = "BULLISH" if change >= 0 else "BEARISH"

    # Simple signals
    signals = []
    if sma_7 and price > sma_7:
        signals.append("above SMA7")
    elif sma_7 and price < sma_7:
        signals.append("below SMA7")

    if rsi:
        if rsi > 70:
            signals.append("RSI overbought")
        elif rsi < 30:
            signals.append("RSI oversold")

    signal_text = ", ".join(signals) if signals else "neutral"

    # Volume context
    vol_billion = volume / 1e9 if volume else 0

    report = f"""
========================================
         CRYPTO PRICE REPORT: {coin}
========================================
  Price ({currency}):     ${price:,.4f}
  24h Change:          {trend} {change:+.2f}%
  24h Volume:          ${vol_billion:,.2f}B
  Market Cap:         ${market_cap:,.2f}
----------------------------------------
  TECHNICAL INDICATORS
  SMA(7):              {sma_7 or 'N/A'}
  SMA(21):             {sma_21 or 'N/A'}
  RSI(14):             {rsi or 'N/A'}
  Signal:              {signal_text}
----------------------------------------
  KEY LEVELS (30d)
  Resistance:         ${(sr_levels or {}).get('resistance_30d') or 'N/A'}
  Support:            ${(sr_levels or {}).get('support_30d') or 'N/A'}
========================================
Updated: {ts} UTC
"""""
    return report.strip()


def main():
    parser = argparse.ArgumentParser(description="Crypto price check via CoinGecko")
    parser.add_argument("--symbol", required=True, help="Crypto symbol (e.g. BTC, ETH)")
    parser.add_argument("--currency", default="USD", help="Fiat currency (default: USD)")
    parser.add_argument("--upper", type=float, help="Upper price threshold for alert")
    parser.add_argument("--lower", type=float, help="Lower price threshold for alert")
    parser.add_argument("--days", type=int, default=30, help="Historical days for SMA (default: 30)")
    parser.add_argument("--output", choices=["text", "json"], default="text", help="Output format")
    args = parser.parse_args()

    # Find coin ID
    coin_id = search_coin(args.symbol)
    if not coin_id:
        print(f"ERROR: Could not find coin with symbol '{args.symbol}'", file=sys.stderr)
        sys.exit(1)

    # Get current price
    price_data = get_price_data(coin_id, args.currency.lower())
    if not price_data:
        print(f"ERROR: Could not fetch price for '{args.symbol}'", file=sys.stderr)
        sys.exit(1)

    # Get historical data for indicators
    historical = get_historical_prices(coin_id, args.currency.lower(), args.days)

    sma_7 = calculate_sma(historical, 7) if historical else None
    sma_21 = calculate_sma(historical, 21) if historical else None
    rsi = calculate_rsi(historical, 14) if historical else None
    sr = estimate_support_resistance(historical) if historical else None

    # Alerts
    thresholds = {}
    if args.upper:
        thresholds["upper"] = args.upper
    if args.lower:
        thresholds["lower"] = args.lower

    alerts = generate_alert(price_data, thresholds if thresholds else None)

    if args.output == "json":
        result = {
            "price_data": price_data,
            "indicators": {
                "sma_7": sma_7,
                "sma_21": sma_21,
                "rsi_14": rsi,
            },
            "key_levels": sr,
            "alerts": alerts,
        }
        print(json.dumps(result, indent=2))
    else:
        report = build_report(price_data, sma_7, sma_21, rsi, sr, thresholds if thresholds else None)
        print(report)
        if alerts:
            print("\n--- ALERTS ---")
            for alert in alerts:
                print(f"  {alert}")


if __name__ == "__main__":
    main()

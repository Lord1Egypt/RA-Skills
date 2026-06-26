#!/usr/bin/env python3
"""
Currency Converter Pro
Author: Lin Hui
Real-time exchange rates with multi-currency support.
Uses open.er-api.com (free, no API key required).
"""

import sys
import json
import subprocess
import urllib.request
import urllib.error

API_BASE = "https://open.er-api.com/v6"


def fetch_rates(base="USD"):
    """Fetch latest exchange rates from open.er-api.com"""
    url = f"{API_BASE}/latest/{base}"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode())
        if data.get("result") == "success":
            return data
        else:
            return {"error": "API error: " + str(data)}
    except urllib.error.URLError as e:
        return {"error": "Network error: " + str(e)}
    except Exception as e:
        return {"error": str(e)}


def fetch_historical(base, date_str):
    """Fetch historical exchange rates (date format: YYYY-MM-DD)"""
    url = f"{API_BASE}/historical/{date_str}?base={base}"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            return json.loads(resp.read().decode())
    except Exception as e:
        return {"error": str(e)}


def cmd_convert(args):
    """Convert amount from one currency to another"""
    # args: [amount, from_currency, to_currency]
    if len(args) < 3:
        print(json.dumps({"error": "Usage: convert <amount> <from_currency> <to_currency>"}))
        return
    try:
        amount = float(args[0])
        from_curr = args[1].upper()
        to_curr = args[2].upper()
    except ValueError:
        print(json.dumps({"error": "Invalid amount"}))
        return

    data = fetch_rates(from_curr)
    if "error" in data:
        print(json.dumps(data))
        return

    rates = data.get("rates", {})
    if to_curr not in rates:
        print(json.dumps({"error": f"Currency {to_curr} not found in rates"}))
        return

    rate = rates[to_curr]
    converted = amount * rate
    print(json.dumps({
        "from": from_curr,
        "to": to_curr,
        "amount": amount,
        "rate": round(rate, 6),
        "result": round(converted, 2),
        "timestamp": data.get("time_last_update_utc", ""),
        "provider": "open.er-api.com"
    }, ensure_ascii=False, indent=2))


def cmd_rates(args):
    """Show all rates for a base currency"""
    base = args[0].upper() if args else "USD"
    data = fetch_rates(base)
    if "error" in data:
        print(json.dumps(data))
        return

    rates = data.get("rates", {})
    sorted_rates = dict(sorted(rates.items()))

    # Format nicely
    print(json.dumps({
        "base": base,
        "timestamp": data.get("time_last_update_utc", ""),
        "rates": sorted_rates
    }, ensure_ascii=False, indent=2))


def cmd_top(args):
    """Show top currencies by conversion value"""
    if len(args) < 2:
        print(json.dumps({"error": "Usage: top <amount> <from_currency>"}))
        return
    try:
        amount = float(args[0])
        from_curr = args[1].upper()
    except ValueError:
        print(json.dumps({"error": "Invalid amount"}))
        return

    data = fetch_rates(from_curr)
    if "error" in data:
        print(json.dumps(data))
        return

    rates = data.get("rates", {})
    # Common currencies to show
    common = ["CNY", "HKD", "TWD", "JPY", "KRW", "EUR", "GBP", "SGD", "AUD", "CAD",
              "CHF", "JPY", "INR", "THB", "MYR", "PHP", "VND", "IDR", "AED", "SAR",
              "USD"]
    converted = []
    for curr in common:
        if curr in rates:
            converted.append((curr, round(amount * rates[curr], 2)))

    print(json.dumps({
        "from": from_curr,
        "amount": amount,
        "conversions": [{"currency": c, "amount": a} for c, a in converted]
    }, ensure_ascii=False, indent=2))


def cmd_historical(args):
    """Show historical rate between two currencies on a specific date"""
    if len(args) < 3:
        print(json.dumps({"error": "Usage: historical <amount> <from_currency> <to_currency> <date(YYYY-MM-DD)>"}))
        return
    try:
        amount = float(args[0])
        from_curr = args[1].upper()
        to_curr = args[2].upper()
        date_str = args[3] if len(args) > 3 else "2024-01-01"
    except ValueError:
        print(json.dumps({"error": "Invalid amount"}))
        return

    data = fetch_historical(from_curr, date_str)
    if "error" in data:
        print(json.dumps(data))
        return

    rates = data.get("rates", {})
    if to_curr not in rates:
        print(json.dumps({"error": f"Currency {to_curr} not found"}))
        return

    rate = rates[to_curr]
    converted = amount * rate
    print(json.dumps({
        "from": from_curr,
        "to": to_curr,
        "amount": amount,
        "date": date_str,
        "rate": round(rate, 6),
        "result": round(converted, 2),
        "timestamp": data.get("time_last_update_utc", "")
    }, ensure_ascii=False, indent=2))


def main():
    if len(sys.argv) < 2:
        print("Usage: currency.py <command> [args...]")
        print("Commands: convert, rates, top, historical")
        sys.exit(1)

    cmd = sys.argv[1]
    args = sys.argv[2:]

    if cmd == "convert":
        cmd_convert(args)
    elif cmd == "rates":
        cmd_rates(args)
    elif cmd == "top":
        cmd_top(args)
    elif cmd == "historical":
        cmd_historical(args)
    else:
        print(f"Unknown command: {cmd}")


if __name__ == "__main__":
    main()

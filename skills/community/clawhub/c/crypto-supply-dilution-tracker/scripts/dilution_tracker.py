#!/usr/bin/env python3
"""
Crypto Supply Dilution Tracker

Pulls circulating supply, total supply, and max supply for one or more
coins from the free CoinGecko API (no API key required) and computes a
dilution risk score based on how much future supply remains to enter
circulation relative to today's circulating supply.

This is a supply-side proxy for future sell pressure, NOT a full unlock
calendar. It cannot see vesting cliffs or team lockup schedules (those
require project-specific data that isn't published in a standard API).
What it CAN tell you, honestly:
  - How much of a token's eventual supply is already circulating
  - The ratio of "supply still to be released" vs "supply already out"
  - A simple flag for coins where a large multiple of current supply
    still has to be minted/unlocked (mining rewards, treasury, vesting)

Usage:
    python3 dilution_tracker.py bitcoin ethereum solana dogecoin
    python3 dilution_tracker.py --ids bitcoin,ethereum --json
    python3 dilution_tracker.py --top 25          # scan top 25 by market cap
"""

import argparse
import json
import sys
import urllib.request
import urllib.error

COINGECKO_MARKETS = "https://api.coingecko.com/api/v3/coins/markets"


def fetch_markets(ids=None, top=None):
    params = {
        "vs_currency": "usd",
        "sparkline": "false",
        "price_change_percentage": "24h",
    }
    if ids:
        params["ids"] = ",".join(ids)
        params["per_page"] = str(len(ids))
        params["page"] = "1"
    else:
        params["order"] = "market_cap_desc"
        params["per_page"] = str(top or 25)
        params["page"] = "1"

    query = "&".join(f"{k}={v}" for k, v in params.items())
    url = f"{COINGECKO_MARKETS}?{query}"
    req = urllib.request.Request(url, headers={"User-Agent": "dilution-tracker/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        print(f"HTTP error {e.code} calling CoinGecko: {e.reason}", file=sys.stderr)
        sys.exit(1)
    except urllib.error.URLError as e:
        print(f"Network error calling CoinGecko: {e.reason}", file=sys.stderr)
        sys.exit(1)


def dilution_score(circulating, total, max_supply):
    """
    Returns (score, label, remaining_pct).

    score = (eventual_supply - circulating) / circulating
      0.0   -> fully diluted already, no more supply coming
      0.25  -> 25% more supply than what's circulating still has to appear
      1.0+  -> more than 100% additional supply still to come (high risk)

    eventual_supply prefers max_supply; falls back to total_supply
    (some coins, e.g. ETH, have no max_supply and are not "capped" at all,
    which we flag separately as UNCAPPED).
    """
    if not circulating or circulating <= 0:
        return None, "UNKNOWN", None

    eventual = max_supply or total_supply_fallback(total)
    if eventual is None:
        return None, "UNCAPPED", None

    if eventual <= circulating:
        return 0.0, "FULLY DILUTED", 0.0

    remaining = eventual - circulating
    score = remaining / circulating
    remaining_pct = remaining / eventual * 100

    if score >= 1.0:
        label = "HIGH DILUTION RISK"
    elif score >= 0.25:
        label = "MODERATE DILUTION"
    elif score > 0:
        label = "LOW DILUTION"
    else:
        label = "FULLY DILUTED"

    return score, label, remaining_pct


def total_supply_fallback(total_supply):
    return total_supply if total_supply else None


def analyze(coin):
    circ = coin.get("circulating_supply")
    total = coin.get("total_supply")
    max_sup = coin.get("max_supply")
    score, label, remaining_pct = dilution_score(circ, total, max_sup)
    return {
        "id": coin.get("id"),
        "symbol": (coin.get("symbol") or "").upper(),
        "name": coin.get("name"),
        "price_usd": coin.get("current_price"),
        "market_cap_usd": coin.get("market_cap"),
        "fully_diluted_valuation_usd": coin.get("fully_diluted_valuation"),
        "circulating_supply": circ,
        "total_supply": total,
        "max_supply": max_sup,
        "dilution_score": round(score, 3) if score is not None else None,
        "remaining_supply_pct": round(remaining_pct, 1) if remaining_pct is not None else None,
        "risk_label": label,
    }


def main():
    ap = argparse.ArgumentParser(description="Crypto supply dilution tracker (CoinGecko-backed)")
    ap.add_argument("ids", nargs="*", help="CoinGecko coin ids, e.g. bitcoin ethereum solana")
    ap.add_argument("--ids", dest="ids_csv", help="Comma-separated coin ids (alternative to positional args)")
    ap.add_argument("--top", type=int, help="Scan top N coins by market cap instead of specific ids")
    ap.add_argument("--json", action="store_true", help="Output raw JSON instead of a table")
    args = ap.parse_args()

    ids = []
    if args.ids_csv:
        ids.extend([i.strip() for i in args.ids_csv.split(",") if i.strip()])
    ids.extend(args.ids)

    if not ids and not args.top:
        ap.print_help()
        sys.exit(1)

    raw = fetch_markets(ids=ids if ids else None, top=args.top)
    results = [analyze(c) for c in raw]
    results.sort(key=lambda r: (r["dilution_score"] is None, -(r["dilution_score"] or 0)))

    if args.json:
        print(json.dumps(results, indent=2))
        return

    header = f"{'SYM':<8}{'PRICE':>12}{'CIRC SUPPLY':>18}{'REF SUPPLY':>18}{'REMAIN %':>10}  {'RISK'}"
    print(header)
    print("-" * len(header))
    for r in results:
        circ = f"{r['circulating_supply']:,.0f}" if r["circulating_supply"] else "-"
        ref_supply = r["max_supply"] or r["total_supply"]
        ref_label = "max" if r["max_supply"] else ("total" if r["total_supply"] else None)
        maxs = f"{ref_supply:,.0f} ({ref_label})" if ref_supply else "no cap data"
        remain = f"{r['remaining_supply_pct']:.1f}%" if r["remaining_supply_pct"] is not None else "-"
        price = f"${r['price_usd']:,.4f}" if r["price_usd"] else "-"
        print(f"{r['symbol']:<8}{price:>12}{circ:>18}{maxs:>18}{remain:>10}  {r['risk_label']}")


if __name__ == "__main__":
    main()

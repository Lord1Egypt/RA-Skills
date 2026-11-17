#!/usr/bin/env python3
"""
Cross-Exchange Crypto Arbitrage Scanner
----------------------------------------
Pulls live public spot tickers (no API key required) from Coinbase, Kraken,
Bitstamp, Gemini, and OKX, and reports the best bid/ask spread across
exchanges for each requested symbol. Useful for spotting cross-exchange
price arbitrage opportunities (buy low on exchange A, sell high on
exchange B) before fees/withdrawal time eat the edge.

Usage:
    python3 arb_scanner.py BTC ETH SOL
    python3 arb_scanner.py --min-spread-bps 15 BTC ETH
    python3 arb_scanner.py --json BTC

Notes:
    - This only compares displayed bid/ask, not tradable depth. Always
      sanity-check size/depth and withdrawal/network fees before acting.
    - Binance is intentionally excluded: its public REST API blocks
      requests from many cloud/server IP ranges with a 451-style error.
    - Exchanges that don't list a symbol are skipped silently.
"""
import argparse
import json
import sys
import urllib.request
import urllib.error

TIMEOUT = 10
HEADERS = {"User-Agent": "cross-exchange-arb-scanner/1.0"}


def _get_json(url: str):
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
        return json.loads(resp.read().decode())


def fetch_coinbase(symbol: str):
    try:
        d = _get_json(f"https://api.exchange.coinbase.com/products/{symbol}-USD/ticker")
        return {"bid": float(d["bid"]), "ask": float(d["ask"])}
    except Exception:
        return None


def fetch_kraken(symbol: str):
    pair_map = {"BTC": "XBTUSD", "DOGE": "XDGUSD"}
    pair = pair_map.get(symbol, f"{symbol}USD")
    try:
        d = _get_json(f"https://api.kraken.com/0/public/Ticker?pair={pair}")
        if d.get("error"):
            return None
        result = next(iter(d["result"].values()))
        return {"bid": float(result["b"][0]), "ask": float(result["a"][0])}
    except Exception:
        return None


def fetch_bitstamp(symbol: str):
    try:
        d = _get_json(f"https://www.bitstamp.net/api/v2/ticker/{symbol.lower()}usd/")
        return {"bid": float(d["bid"]), "ask": float(d["ask"])}
    except Exception:
        return None


def fetch_gemini(symbol: str):
    try:
        d = _get_json(f"https://api.gemini.com/v1/pubticker/{symbol.lower()}usd")
        return {"bid": float(d["bid"]), "ask": float(d["ask"])}
    except Exception:
        return None


def fetch_okx(symbol: str):
    try:
        d = _get_json(f"https://www.okx.com/api/v5/market/ticker?instId={symbol}-USDT")
        if d.get("code") != "0" or not d.get("data"):
            return None
        row = d["data"][0]
        return {"bid": float(row["bidPx"]), "ask": float(row["askPx"])}
    except Exception:
        return None


EXCHANGES = {
    "coinbase": fetch_coinbase,
    "kraken": fetch_kraken,
    "bitstamp": fetch_bitstamp,
    "gemini": fetch_gemini,
    "okx": fetch_okx,
}


def scan_symbol(symbol: str):
    quotes = {}
    for name, fn in EXCHANGES.items():
        q = fn(symbol)
        if q:
            quotes[name] = q

    if len(quotes) < 2:
        return {"symbol": symbol, "quotes": quotes, "opportunity": None}

    best_bid_ex = max(quotes, key=lambda e: quotes[e]["bid"])
    best_ask_ex = min(quotes, key=lambda e: quotes[e]["ask"])
    best_bid = quotes[best_bid_ex]["bid"]
    best_ask = quotes[best_ask_ex]["ask"]

    opportunity = None
    if best_bid_ex != best_ask_ex and best_bid > best_ask:
        spread = best_bid - best_ask
        spread_bps = (spread / best_ask) * 10000
        opportunity = {
            "buy_on": best_ask_ex,
            "buy_price": best_ask,
            "sell_on": best_bid_ex,
            "sell_price": best_bid,
            "spread_usd": round(spread, 4),
            "spread_bps": round(spread_bps, 2),
        }

    return {"symbol": symbol, "quotes": quotes, "opportunity": opportunity}


def main():
    parser = argparse.ArgumentParser(description="Scan public exchange tickers for cross-exchange arb spreads.")
    parser.add_argument("symbols", nargs="+", help="Base symbols, e.g. BTC ETH SOL")
    parser.add_argument("--min-spread-bps", type=float, default=0.0, help="Only report opportunities at/above this bps threshold")
    parser.add_argument("--json", action="store_true", help="Output raw JSON instead of a formatted report")
    args = parser.parse_args()

    results = [scan_symbol(s.upper()) for s in args.symbols]

    if args.json:
        print(json.dumps(results, indent=2))
        return

    found_any = False
    for r in results:
        print(f"\n=== {r['symbol']} ===")
        if not r["quotes"]:
            print("  No exchange data available (symbol may not be listed).")
            continue
        for ex, q in sorted(r["quotes"].items()):
            print(f"  {ex:10s}  bid={q['bid']:<14.4f} ask={q['ask']:<14.4f}")
        opp = r["opportunity"]
        if opp and opp["spread_bps"] >= args.min_spread_bps:
            found_any = True
            print(f"  >> ARB: buy {r['symbol']} on {opp['buy_on']} @ {opp['buy_price']:.4f}, "
                  f"sell on {opp['sell_on']} @ {opp['sell_price']:.4f} "
                  f"= {opp['spread_bps']:.1f} bps gross (before fees/withdrawal)")
        elif opp:
            print(f"  (opportunity of {opp['spread_bps']:.1f} bps below --min-spread-bps threshold)")
        else:
            print("  No crossed market detected (bid <= ask across exchanges, as expected).")

    if not found_any:
        print("\nNo opportunities met the spread threshold this run.")


if __name__ == "__main__":
    sys.exit(main())

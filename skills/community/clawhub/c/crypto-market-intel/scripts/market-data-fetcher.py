#!/usr/bin/env python3
"""
Market Data Fetcher — pulls live prices, metrics, and macro data from free APIs.
Zero API keys required. Outputs JSON files for agent analysis.

Usage:
  python3 market-data-fetcher.py [crypto|stocks|all] [--output DIR]

Examples:
  python3 market-data-fetcher.py crypto --output ~/market-data
  python3 market-data-fetcher.py all --output /tmp/market
"""
import json
import urllib.request
import urllib.error
import sys
import os
import argparse
from datetime import datetime, timezone


def fetch_json(url, timeout=15):
    """Fetch JSON from URL with error handling."""
    try:
        req = urllib.request.Request(url, headers={
            "User-Agent": "Mozilla/5.0",
            "Accept": "application/json"
        })
        resp = urllib.request.urlopen(req, timeout=timeout)
        return json.loads(resp.read())
    except Exception as e:
        print(f"  ⚠️ Failed: {url[:60]}... — {e}", flush=True)
        return None


def fetch_crypto(output_dir):
    """Fetch crypto market data from free APIs."""
    print("📊 Fetching crypto data...", flush=True)
    data = {"fetched_at": datetime.now(timezone.utc).isoformat(), "source": "coingecko+alternative.me"}

    # ── Top coins from CoinGecko (free, no key) ─────────────
    coins = fetch_json(
        "https://api.coingecko.com/api/v3/coins/markets?"
        "vs_currency=usd&order=market_cap_desc&per_page=30&page=1"
        "&sparkline=false&price_change_percentage=1h,24h,7d"
    )
    if coins:
        data["top_coins"] = [{
            "symbol": c["symbol"].upper(),
            "name": c["name"],
            "price": c["current_price"],
            "market_cap": c["market_cap"],
            "volume_24h": c["total_volume"],
            "change_24h_pct": c.get("price_change_percentage_24h"),
            "change_7d_pct": c.get("price_change_percentage_7d_in_currency"),
            "change_1h_pct": c.get("price_change_percentage_1h_in_currency"),
            "ath": c.get("ath"),
            "ath_change_pct": c.get("ath_change_percentage"),
            "rank": c.get("market_cap_rank"),
        } for c in coins]
        print(f"  ✅ {len(coins)} coins fetched", flush=True)

    # ── Global market data ───────────────────────────────────
    global_data = fetch_json("https://api.coingecko.com/api/v3/global")
    if global_data and "data" in global_data:
        g = global_data["data"]
        data["global"] = {
            "total_market_cap_usd": g.get("total_market_cap", {}).get("usd"),
            "total_volume_24h_usd": g.get("total_volume", {}).get("usd"),
            "btc_dominance": g.get("market_cap_percentage", {}).get("btc"),
            "eth_dominance": g.get("market_cap_percentage", {}).get("eth"),
            "active_cryptocurrencies": g.get("active_cryptocurrencies"),
            "market_cap_change_24h_pct": g.get("market_cap_change_percentage_24h_usd"),
        }
        print(f"  ✅ Global: ${data['global']['total_market_cap_usd']/1e12:.2f}T mcap, BTC dom {data['global']['btc_dominance']:.1f}%", flush=True)

    # ── Fear & Greed Index ───────────────────────────────────
    fng = fetch_json("https://api.alternative.me/fng/?limit=7")
    if fng and "data" in fng:
        data["fear_greed"] = [{
            "value": int(d["value"]),
            "label": d["value_classification"],
            "date": d["timestamp"],
        } for d in fng["data"]]
        current = data["fear_greed"][0]
        print(f"  ✅ Fear & Greed: {current['value']} ({current['label']})", flush=True)

    # ── Trending coins ───────────────────────────────────────
    trending = fetch_json("https://api.coingecko.com/api/v3/search/trending")
    if trending and "coins" in trending:
        data["trending"] = [{
            "name": c["item"]["name"],
            "symbol": c["item"]["symbol"],
            "rank": c["item"]["market_cap_rank"],
            "score": c["item"].get("score"),
        } for c in trending["coins"][:10]]
        print(f"  ✅ {len(data['trending'])} trending coins", flush=True)

    # ── DeFi TVL from DeFi Llama ─────────────────────────────
    defi = fetch_json("https://api.llama.fi/v2/historicalChainTvl")
    if defi and len(defi) > 0:
        latest = defi[-1] if defi else None
        prev_day = defi[-2] if len(defi) > 1 else None
        if latest:
            data["defi_tvl"] = {
                "total_tvl": latest.get("tvl"),
                "date": latest.get("date"),
                "change_1d": ((latest["tvl"] - prev_day["tvl"]) / prev_day["tvl"] * 100) if prev_day else None,
            }
            print(f"  ✅ DeFi TVL: ${latest['tvl']/1e9:.1f}B", flush=True)

    # ── Write output ─────────────────────────────────────────
    out_path = os.path.join(output_dir, "crypto-latest.json")
    with open(out_path, "w") as f:
        json.dump(data, f, indent=2)
    print(f"  📁 Saved to {out_path}", flush=True)
    return data


def fetch_stocks(output_dir):
    """Fetch stock/macro data from Yahoo Finance."""
    print("📈 Fetching stock/macro data...", flush=True)
    data = {"fetched_at": datetime.now(timezone.utc).isoformat()}

    # ── Major indices and AI stocks via Yahoo Finance ───────
    tickers = {
        "indices": ["^GSPC", "^IXIC", "^DJI", "^VIX"],
        "ai_chips": ["NVDA", "AMD", "AVGO", "MRVL", "TSM", "ASML", "ARM"],
        "ai_cloud": ["MSFT", "AMZN", "GOOG", "META", "ORCL"],
        "ai_energy": ["VST", "CEG", "OKLO", "SMR", "TLN"],
        "ai_infra": ["VRT", "ANET", "CRDO"],
    }

    data["stocks"] = {}
    for category, symbols in tickers.items():
        data["stocks"][category] = []
        for sym in symbols:
            clean_sym = sym.replace("^", "%5E")
            q = fetch_json(f"https://query1.finance.yahoo.com/v8/finance/chart/{clean_sym}?interval=1d&range=5d")
            if q and "chart" in q and "result" in q["chart"] and q["chart"]["result"]:
                result = q["chart"]["result"][0]
                meta = result.get("meta", {})
                data["stocks"][category].append({
                    "symbol": sym,
                    "price": meta.get("regularMarketPrice"),
                    "prev_close": meta.get("previousClose"),
                    "change_pct": round((meta.get("regularMarketPrice", 0) - meta.get("previousClose", 1)) / meta.get("previousClose", 1) * 100, 2) if meta.get("previousClose") else None,
                    "currency": meta.get("currency"),
                })
                print(f"  ✅ {sym}: ${meta.get('regularMarketPrice', '?')}", flush=True)
            else:
                data["stocks"][category].append({"symbol": sym, "error": "fetch failed"})

    # ── DXY (Dollar Index) ───────────────────────────────────
    dxy = fetch_json("https://query1.finance.yahoo.com/v8/finance/chart/DX-Y.NYB?interval=1d&range=5d")
    if dxy and "chart" in dxy and dxy["chart"].get("result"):
        meta = dxy["chart"]["result"][0].get("meta", {})
        data["dxy"] = {
            "price": meta.get("regularMarketPrice"),
            "prev_close": meta.get("previousClose"),
        }
        print(f"  ✅ DXY: {meta.get('regularMarketPrice', '?')}", flush=True)

    # ── 10Y Treasury ─────────────────────────────────────────
    tnx = fetch_json("https://query1.finance.yahoo.com/v8/finance/chart/%5ETNX?interval=1d&range=5d")
    if tnx and "chart" in tnx and tnx["chart"].get("result"):
        meta = tnx["chart"]["result"][0].get("meta", {})
        data["treasury_10y"] = {
            "yield": meta.get("regularMarketPrice"),
            "prev_close": meta.get("previousClose"),
        }
        print(f"  ✅ 10Y: {meta.get('regularMarketPrice', '?')}%", flush=True)

    # ── Write output ─────────────────────────────────────────
    out_path = os.path.join(output_dir, "stocks-latest.json")
    with open(out_path, "w") as f:
        json.dump(data, f, indent=2)
    print(f"  📁 Saved to {out_path}", flush=True)
    return data


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fetch market data from free APIs")
    parser.add_argument("mode", choices=["crypto", "stocks", "all"], default="all", nargs="?",
                        help="Data to fetch: crypto, stocks, or all (default: all)")
    parser.add_argument("--output", "-o", default="./market-data",
                        help="Output directory for JSON files (default: ./market-data)")
    args = parser.parse_args()

    # Create output directory
    os.makedirs(args.output, exist_ok=True)

    # Fetch requested data
    if args.mode in ("crypto", "all"):
        fetch_crypto(args.output)
    if args.mode in ("stocks", "all"):
        fetch_stocks(args.output)

    print(f"\n✅ Market data fetch complete. Files in {args.output}/", flush=True)

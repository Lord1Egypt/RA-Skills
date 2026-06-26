#!/usr/bin/env python3
"""Viral trend detection - hot ticker scanner."""

import argparse, json, sys

def ensure_yfinance():
    try:
        import yfinance; return yfinance
    except ImportError:
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "yfinance", "-q"])
        import yfinance; return yfinance


# Curated watchlists for scanning
STOCK_TICKERS = ["AAPL", "MSFT", "GOOGL", "AMZN", "NVDA", "TSLA", "META", "AMD", "NFLX", "CRM",
    "COIN", "PLTR", "SOFI", "RIVN", "LCID", "NIO", "BABA", "JD", "PDD", "MARA"]
CRYPTO_TICKERS = ["BTC-USD", "ETH-USD", "SOL-USD", "XRP-USD", "DOGE-USD", "ADA-USD",
    "AVAX-USD", "DOT-USD", "LINK-USD", "MATIC-USD", "SHIB-USD", "PEPE24478-USD"]


def scan(market="all", top_n=10):
    yf = ensure_yfinance()
    tickers = []
    if market in ("all", "stock"): tickers += STOCK_TICKERS
    if market in ("all", "crypto"): tickers += CRYPTO_TICKERS

    results = []
    for sym in tickers:
        try:
            t = yf.Ticker(sym)
            info = t.info or {}
            price = info.get("currentPrice") or info.get("regularMarketPrice")
            prev = info.get("previousClose")
            vol = info.get("volume") or 0
            avg_vol = info.get("averageVolume") or 1

            if not price or not prev:
                continue

            change_pct = (price - prev) / prev * 100
            vol_surge = vol / avg_vol if avg_vol else 1

            # Hot score: combine price move + volume surge
            hot_score = abs(change_pct) * 0.6 + min(vol_surge * 2, 10) * 0.4

            results.append({
                "ticker": sym,
                "name": info.get("shortName", sym),
                "price": round(price, 2),
                "change_pct": round(change_pct, 2),
                "volume": vol,
                "vol_surge": round(vol_surge, 2),
                "hot_score": round(hot_score, 2),
            })
        except:
            continue

    results.sort(key=lambda x: x["hot_score"], reverse=True)
    return results[:top_n]


def format_output(data):
    lines = ["🔥 Hot Scanner — 热门标的排行", ""]
    for i, d in enumerate(data):
        arrow = "🟢" if d["change_pct"] >= 0 else "🔴"
        surge = "🔥" if d["vol_surge"] > 2 else ""
        lines.append(f"{i+1}. {arrow} {d['name']} ({d['ticker']})")
        lines.append(f"   价格: {d['price']} | 涨跌: {d['change_pct']}% | 量比: {d['vol_surge']}x {surge}")
        lines.append(f"   热度分: {d['hot_score']}")
        lines.append("")
    return "\n".join(lines)


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--market", choices=["all", "stock", "crypto"], default="all")
    p.add_argument("--top", type=int, default=10)
    p.add_argument("--json", action="store_true")
    a = p.parse_args()
    data = scan(a.market, a.top)
    print(json.dumps(data, indent=2) if a.json else format_output(data))

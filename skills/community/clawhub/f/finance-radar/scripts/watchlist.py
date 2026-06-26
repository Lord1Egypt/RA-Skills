#!/usr/bin/env python3
"""Watchlist with price alerts."""

import argparse, json, os, sys

WATCHLIST_FILE = os.path.expanduser("~/.openclaw/workspace/finance-radar/data/watchlist.json")

def ensure_yfinance():
    try:
        import yfinance; return yfinance
    except ImportError:
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "yfinance", "-q"])
        import yfinance; return yfinance


def load():
    os.makedirs(os.path.dirname(WATCHLIST_FILE), exist_ok=True)
    if os.path.exists(WATCHLIST_FILE):
        return json.load(open(WATCHLIST_FILE))
    return {"items": []}


def save(data):
    os.makedirs(os.path.dirname(WATCHLIST_FILE), exist_ok=True)
    json.dump(data, open(WATCHLIST_FILE, "w"), indent=2)


def add(ticker, above=None, below=None):
    wl = load()
    entry = {"ticker": ticker, "above": above, "below": below}
    # Remove existing
    wl["items"] = [i for i in wl["items"] if i["ticker"] != ticker]
    wl["items"].append(entry)
    save(wl)
    return entry


def remove(ticker):
    wl = load()
    wl["items"] = [i for i in wl["items"] if i["ticker"] != ticker]
    save(wl)


def check():
    yf = ensure_yfinance()
    wl = load()
    alerts = []
    for item in wl["items"]:
        try:
            t = yf.Ticker(item["ticker"])
            info = t.info or {}
            price = info.get("currentPrice") or info.get("regularMarketPrice") or 0
        except:
            price = 0

        triggered = []
        if item.get("above") and price >= item["above"]:
            triggered.append(f"突破上限 {item['above']}")
        if item.get("below") and price <= item["below"]:
            triggered.append(f"跌破下限 {item['below']}")

        alerts.append({
            "ticker": item["ticker"],
            "price": round(price, 2),
            "above": item.get("above"),
            "below": item.get("below"),
            "triggered": triggered,
        })
    return alerts


def show():
    wl = load()
    return wl["items"]


def format_output(alerts):
    lines = ["👁️ 观察名单", ""]
    for a in alerts:
        icon = "🚨" if a["triggered"] else "👀"
        lines.append(f"{icon} {a['ticker']}: 现价 {a['price']}")
        if a["above"]: lines.append(f"   上限: {a['above']}")
        if a["below"]: lines.append(f"   下限: {a['below']}")
        for t in a["triggered"]:
            lines.append(f"   ⚠️ 警报: {t}")
        lines.append("")
    if not alerts:
        lines.append("  (空列表)")
    return "\n".join(lines)


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--action", choices=["add", "remove", "check", "show"], default="check")
    p.add_argument("--ticker", default=None)
    p.add_argument("--above", type=float, default=None)
    p.add_argument("--below", type=float, default=None)
    p.add_argument("--json", action="store_true")
    a = p.parse_args()

    if a.action == "add":
        r = add(a.ticker.upper(), a.above, a.below)
        print(f"✅ 已添加 {r['ticker']} 上限:{r['above']} 下限:{r['below']}")
    elif a.action == "remove":
        remove(a.ticker.upper())
        print(f"✅ 已移除 {a.ticker.upper()}")
    elif a.action == "show":
        data = show()
        print(json.dumps(data, indent=2))
    else:
        data = check()
        print(json.dumps(data, indent=2) if a.json else format_output(data))

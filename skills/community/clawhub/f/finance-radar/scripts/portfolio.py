#!/usr/bin/env python3
"""Portfolio tracking & P/L management."""

import argparse, json, os, sys

PORTFOLIO_FILE = os.path.expanduser("~/.openclaw/workspace/finance-radar/data/portfolio.json")

def ensure_yfinance():
    try:
        import yfinance; return yfinance
    except ImportError:
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "yfinance", "-q"])
        import yfinance; return yfinance


def load():
    os.makedirs(os.path.dirname(PORTFOLIO_FILE), exist_ok=True)
    if os.path.exists(PORTFOLIO_FILE):
        return json.load(open(PORTFOLIO_FILE))
    return {"holdings": []}


def save(data):
    os.makedirs(os.path.dirname(PORTFOLIO_FILE), exist_ok=True)
    json.dump(data, open(PORTFOLIO_FILE, "w"), indent=2)


def add(ticker, shares, cost):
    pf = load()
    for h in pf["holdings"]:
        if h["ticker"] == ticker:
            total_cost = h["shares"] * h["avg_cost"] + shares * cost
            h["shares"] += shares
            h["avg_cost"] = round(total_cost / h["shares"], 4)
            save(pf)
            return h
    entry = {"ticker": ticker, "shares": shares, "avg_cost": cost}
    pf["holdings"].append(entry)
    save(pf)
    return entry


def remove(ticker):
    pf = load()
    pf["holdings"] = [h for h in pf["holdings"] if h["ticker"] != ticker]
    save(pf)


def show():
    yf = ensure_yfinance()
    pf = load()
    if not pf["holdings"]:
        return {"holdings": [], "total_value": 0, "total_cost": 0, "total_pnl": 0}

    results = []
    total_val = total_cost = 0
    for h in pf["holdings"]:
        try:
            t = yf.Ticker(h["ticker"])
            info = t.info or {}
            price = info.get("currentPrice") or info.get("regularMarketPrice") or 0
        except:
            price = 0
        val = price * h["shares"]
        cost = h["avg_cost"] * h["shares"]
        pnl = val - cost
        pnl_pct = (pnl / cost * 100) if cost else 0
        total_val += val
        total_cost += cost
        results.append({
            "ticker": h["ticker"], "shares": h["shares"], "avg_cost": h["avg_cost"],
            "price": round(price, 2), "value": round(val, 2),
            "pnl": round(pnl, 2), "pnl_pct": round(pnl_pct, 2),
        })

    return {
        "holdings": results,
        "total_value": round(total_val, 2),
        "total_cost": round(total_cost, 2),
        "total_pnl": round(total_val - total_cost, 2),
        "total_pnl_pct": round((total_val - total_cost) / total_cost * 100, 2) if total_cost else 0,
    }


def format_output(data):
    lines = ["📁 投资组合", ""]
    for h in data["holdings"]:
        arrow = "🟢" if h["pnl"] >= 0 else "🔴"
        lines.append(f"{arrow} {h['ticker']}: {h['shares']}股 @ {h['avg_cost']}")
        lines.append(f"   现价: {h['price']} | 市值: {h['value']} | 盈亏: {h['pnl']} ({h['pnl_pct']}%)")
    lines.append(f"\n💰 总市值: {data['total_value']} | 总成本: {data['total_cost']}")
    lines.append(f"📊 总盈亏: {data['total_pnl']} ({data['total_pnl_pct']}%)")
    if not data["holdings"]:
        lines.append("  (空仓)")
    return "\n".join(lines)


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--action", choices=["show", "add", "remove"], default="show")
    p.add_argument("--ticker", default=None)
    p.add_argument("--shares", type=float, default=0)
    p.add_argument("--cost", type=float, default=0)
    p.add_argument("--json", action="store_true")
    a = p.parse_args()

    if a.action == "add":
        if not a.ticker: print("Error: --ticker required"); sys.exit(1)
        r = add(a.ticker.upper(), a.shares, a.cost)
        print(f"✅ 已添加 {r['ticker']}: {r['shares']}股 @ {r['avg_cost']}")
    elif a.action == "remove":
        remove(a.ticker.upper())
        print(f"✅ 已移除 {a.ticker.upper()}")
    else:
        data = show()
        print(json.dumps(data, indent=2) if a.json else format_output(data))

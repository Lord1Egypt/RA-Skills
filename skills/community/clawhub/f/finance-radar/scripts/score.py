#!/usr/bin/env python3
"""8-dimension stock scoring model."""

import argparse, json, sys

def ensure_yfinance():
    try:
        import yfinance; return yfinance
    except ImportError:
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "yfinance", "-q"])
        import yfinance; return yfinance


def score_stock(ticker):
    yf = ensure_yfinance()
    t = yf.Ticker(ticker)
    info = t.info or {}
    hist = t.history(period="6mo")
    scores = {}

    # 1. Valuation (PE, PB, PS)
    pe = info.get("trailingPE")
    scores["valuation"] = 8 if pe and pe < 15 else 6 if pe and pe < 25 else 4 if pe and pe < 40 else 2 if pe else 5

    # 2. Growth (revenue/earnings growth)
    eg = info.get("earningsGrowth") or 0
    rg = info.get("revenueGrowth") or 0
    scores["growth"] = min(10, max(1, int((eg + rg) * 10 + 5)))

    # 3. Profitability (margins)
    pm = info.get("profitMargins") or 0
    scores["profitability"] = min(10, max(1, int(pm * 30 + 3)))

    # 4. Momentum (price trend)
    if len(hist) > 20:
        ret_1m = (hist["Close"].iloc[-1] / hist["Close"].iloc[-22] - 1) * 100 if len(hist) > 22 else 0
        scores["momentum"] = 8 if ret_1m > 10 else 6 if ret_1m > 0 else 4 if ret_1m > -10 else 2
    else:
        scores["momentum"] = 5

    # 5. Stability (beta, volatility)
    beta = info.get("beta") or 1
    scores["stability"] = 8 if beta < 0.8 else 6 if beta < 1.2 else 4 if beta < 1.8 else 2

    # 6. Dividend
    dy = info.get("dividendYield") or 0
    scores["dividend"] = min(10, max(1, int(dy * 200 + 1)))

    # 7. Analyst sentiment
    rec = info.get("recommendationMean") or 3
    scores["analyst"] = min(10, max(1, int(11 - rec * 2)))

    # 8. Volume health
    vol = info.get("volume") or 0
    avg_vol = info.get("averageVolume") or 1
    vol_ratio = vol / avg_vol if avg_vol else 1
    scores["volume_health"] = 8 if 0.8 < vol_ratio < 1.5 else 6 if vol_ratio < 2 else 4

    total = sum(scores.values())
    max_total = 80
    grade = "A+" if total >= 65 else "A" if total >= 55 else "B+" if total >= 48 else "B" if total >= 40 else "C+" if total >= 32 else "C"

    return {
        "ticker": ticker,
        "name": info.get("shortName", ticker),
        "scores": scores,
        "total": total,
        "max": max_total,
        "pct": round(total / max_total * 100, 1),
        "grade": grade,
    }


def format_output(data):
    dims = {
        "valuation": "💰 估值", "growth": "📈 成长", "profitability": "💵 盈利",
        "momentum": "🚀 动量", "stability": "🛡️ 稳定", "dividend": "💎 股息",
        "analyst": "👨‍💼 分析师", "volume_health": "📦 量能",
    }
    lines = [f"🎯 {data['name']} ({data['ticker']}) — 综合评分"]
    lines.append(f"")
    lines.append(f"总分: {data['total']}/{data['max']} ({data['pct']}%) 评级: {data['grade']}")
    lines.append(f"")
    for k, v in data["scores"].items():
        bar = "█" * v + "░" * (10 - v)
        lines.append(f"{dims.get(k, k):8s} [{bar}] {v}/10")
    return "\n".join(lines)


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--ticker", required=True)
    p.add_argument("--json", action="store_true")
    a = p.parse_args()
    data = score_stock(a.ticker.upper())
    print(json.dumps(data, indent=2) if a.json else format_output(data))

#!/usr/bin/env python3
"""Dividend analysis."""

import argparse, json, sys

def ensure_yfinance():
    try:
        import yfinance; return yfinance
    except ImportError:
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "yfinance", "-q"])
        import yfinance; return yfinance


def analyze_dividend(ticker):
    yf = ensure_yfinance()
    t = yf.Ticker(ticker)
    info = t.info or {}
    divs = t.dividends

    result = {
        "ticker": ticker,
        "name": info.get("shortName", ticker),
        "price": info.get("currentPrice") or info.get("regularMarketPrice"),
        "dividend_rate": info.get("dividendRate"),
        "dividend_yield": info.get("dividendYield"),
        "payout_ratio": info.get("payoutRatio"),
        "ex_date": info.get("exDividendDate"),
        "5y_avg_yield": info.get("fiveYearAvgDividendYield"),
    }

    # Recent dividend history
    if divs is not None and len(divs) > 0:
        recent = divs.tail(8)
        result["history"] = [{"date": str(d.date()), "amount": round(v, 4)} for d, v in recent.items()]
        result["annual_total"] = round(divs.tail(4).sum(), 4)
        # Growth: compare last year vs previous year
        if len(divs) >= 8:
            last_4 = divs.tail(4).sum()
            prev_4 = divs.iloc[-8:-4].sum()
            if prev_4 > 0:
                result["div_growth"] = round((last_4 / prev_4 - 1) * 100, 2)
    else:
        result["history"] = []
        result["annual_total"] = 0

    return result


def format_output(data):
    lines = [f"💎 {data['name']} ({data['ticker']}) — 股息分析", ""]
    if data.get("price"): lines.append(f"💰 股价: {data['price']}")
    if data.get("dividend_rate"): lines.append(f"📊 年度股息: ${data['dividend_rate']}")
    if data.get("dividend_yield"): lines.append(f"📈 股息率: {data['dividend_yield']*100:.2f}%")
    if data.get("5y_avg_yield"): lines.append(f"📉 5年均息率: {data['5y_avg_yield']:.2f}%")
    if data.get("payout_ratio"): lines.append(f"💵 派息率: {data['payout_ratio']*100:.1f}%")
    if data.get("div_growth") is not None: lines.append(f"📈 股息增长: {data['div_growth']}%")
    if data.get("annual_total"): lines.append(f"💰 近4季合计: ${data['annual_total']}")
    if data["history"]:
        lines.append(f"\n📅 近期派息:")
        for h in data["history"]:
            lines.append(f"  {h['date']}: ${h['amount']}")
    else:
        lines.append("\n⚠️ 无股息记录")
    return "\n".join(lines)


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--ticker", required=True)
    p.add_argument("--json", action="store_true")
    a = p.parse_args()
    data = analyze_dividend(a.ticker.upper())
    print(json.dumps(data, indent=2, default=str) if a.json else format_output(data))

#!/usr/bin/env python3
"""
每日美股分析数据获取脚本
只处理用户当前持仓：BMI 和 PDD
数据源：Yahoo Finance (yfinance)
"""

import sys
import json
import time
from datetime import datetime

# 设置编码，支持 Windows 终端
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

try:
    import yfinance as yf
except ImportError:
    print("Installing yfinance...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "yfinance", "-q"])
    import yfinance as yf

# 用户持仓：只有 BMI 和 PDD
HOLDINGS = {
    "BMI": {"name": "Badger Meter", "cost": 123.0, "shares": None},
    "PDD": {"name": "PDD Holdings", "cost": 110.0, "shares": None},
}

# 大盘指数
INDICES = {
    "QQQ": {"name": "Nasdaq QQQ", "ETF": "QQQ"},
    "DIA": {"name": "Dow Jones DIA", "ETF": "DIA"},
    "SPY": {"name": "S&P 500 SPY", "ETF": "SPY"},
}


def get_quote(ticker, retries=3):
    """获取单个标的行情，带重试机制"""
    for attempt in range(retries):
        try:
            info = yf.Ticker(ticker).info
            return {
                "regularMarketPrice": info.get("regularMarketPrice"),
                "regularMarketChange": info.get("regularMarketChange"),
                "regularMarketChangePercent": info.get("regularMarketChangePercent"),
                "fiftyTwoWeekHigh": info.get("fiftyTwoWeekHigh"),
                "fiftyTwoWeekLow": info.get("fiftyTwoWeekLow"),
                "marketCap": info.get("marketCap"),
                "trailingPE": info.get("trailingPE"),
                "beta": info.get("beta"),
            }
        except Exception as e:
            if attempt < retries - 1:
                time.sleep(2)
                continue
            return {"error": str(e)}


def get_recommendations(ticker):
    """获取分析师建议"""
    try:
        info = yf.Ticker(ticker).info
        recommendations = info.get("recommendationTrend", {})
        if recommendations and "trend" in recommendations:
            trend = recommendations["trend"][0]
            return {
                "buy": trend.get("buy", 0),
                "hold": trend.get("hold", 0),
                "sell": trend.get("sell", 0),
                "strongBuy": trend.get("strongBuy", 0),
                "strongSell": trend.get("strongSell", 0),
            }
        return {
            "buy": info.get("recommendationKey", "N/A"),
            "recommendation": info.get("numberOfAnalystOpinions", "N/A"),
        }
    except Exception as e:
        return {"error": str(e)}


def format_market_cap(cap):
    """格式化市值"""
    if not cap:
        return "N/A"
    if cap >= 1e12:
        return f"${cap/1e12:.2f}T"
    elif cap >= 1e9:
        return f"${cap/1e9:.2f}B"
    elif cap >= 1e6:
        return f"${cap/1e6:.2f}M"
    else:
        return f"${cap:.0f}"


def main():
    print("=" * 60)
    print("  Daily US Stock Report")
    print(f"  {datetime.now().strftime('%Y-%m-%d %H:%M')} (Weekend - data from last Friday)")
    print("=" * 60)
    print()

    # 1. 大盘概况
    print("=== Market Overview ===")
    print()
    for ticker, data in INDICES.items():
        q = get_quote(data["ETF"])
        if "error" in q:
            print(f"  {data['name']}: FAILED - {q['error']}")
        else:
            price = q.get("regularMarketPrice", "N/A")
            change = q.get("regularMarketChange", 0)
            change_pct = q.get("regularMarketChangePercent", 0)
            if price and change_pct is not None:
                direction = "+" if change > 0 else ""
                print(f"  {data['name']}: ${price:.2f}  {direction}{change:.2f} ({change_pct:+.2f}%)")
        print()

    # 2. 持仓分析
    print("=== Holdings Analysis ===")
    print()
    for ticker, data in HOLDINGS.items():
        q = get_quote(ticker)
        rec = get_recommendations(ticker)

        if "error" in q:
            print(f"  {ticker} ({data['name']}): FAILED - {q['error']}")
            continue

        price = q.get("regularMarketPrice", 0) or 0
        change = q.get("regularMarketChange", 0) or 0
        change_pct = q.get("regularMarketChangePercent", 0) or 0
        high_52 = q.get("fiftyTwoWeekHigh", 0) or 0
        low_52 = q.get("fiftyTwoWeekLow", 0) or 0
        cap = q.get("marketCap", 0)
        pe = q.get("trailingPE", 0)
        beta = q.get("beta", 0)

        cost = data["cost"]
        pnl = price - cost
        pnl_pct = (pnl / cost * 100) if cost else 0

        print(f"  {ticker} ({data['name']})")
        print(f"     Price: ${price:.2f} | Cost: ${cost:.2f}")
        pnl_str = f"+${pnl:.2f}" if pnl >= 0 else f"-${abs(pnl):.2f}"
        print(f"     P&L: {pnl_str} ({pnl_pct:+.2f}%)")
        print(f"     52W Range: ${high_52:.2f} / ${low_52:.2f}")
        if cap:
            print(f"     Market Cap: {format_market_cap(cap)}")
        if pe:
            print(f"     PE: {pe:.2f}")
        if beta:
            print(f"     Beta: {beta:.2f}")
        if "buy" in rec and "error" not in rec:
            if isinstance(rec.get("buy"), int):
                print(f"     Analysts: Buy={rec['buy']} Hold={rec.get('hold', 0)} Sell={rec.get('sell', 0)}")
            else:
                print(f"     Recommendation: {rec.get('buy', 'N/A')}")
        print()

    # 3. 综合操作建议
    print("=== Actionable Suggestions ===")
    print()
    print("  Note: User's current holdings are BMI and PDD only.")
    print("  (CTNT, SQQQ, KC have been fully stopped out / sold)")
    print()
    print("  Suggestions:")
    for ticker, data in HOLDINGS.items():
        q = get_quote(ticker)
        price = q.get("regularMarketPrice", 0) or 0
        low_52 = q.get("fiftyTwoWeekLow", 0) or 0

        if price and low_52:
            if price <= low_52 * 1.05:
                print(f"    [WATCH] {ticker}: Near 52W low ${low_52:.2f} - watch support")
            else:
                print(f"    [OK] {ticker}: Above 52W low, watch cost ${data['cost']:.2f}")

    print()
    print("=" * 60)
    print("  DISCLAIMER: For reference only, not investment advice.")
    print("=" * 60)


if __name__ == "__main__":
    main()
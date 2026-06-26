#!/usr/bin/env python3
"""Stock/crypto analysis via Yahoo Finance (yfinance)."""

import argparse, json, sys

def ensure_yfinance():
    try:
        import yfinance
        return yfinance
    except ImportError:
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "yfinance", "-q"])
        import yfinance
        return yfinance


def analyze(ticker):
    yf = ensure_yfinance()
    t = yf.Ticker(ticker)
    info = t.info or {}
    hist = t.history(period="1mo")

    price = info.get("currentPrice") or info.get("regularMarketPrice") or (hist["Close"].iloc[-1] if len(hist) > 0 else None)
    prev = info.get("previousClose") or (hist["Close"].iloc[-2] if len(hist) > 1 else None)
    change = ((price - prev) / prev * 100) if price and prev else None

    result = {
        "ticker": ticker,
        "name": info.get("shortName", ticker),
        "type": info.get("quoteType", "N/A"),
        "price": round(price, 2) if price else None,
        "change_pct": round(change, 2) if change else None,
        "currency": info.get("currency", "USD"),
        "market_cap": info.get("marketCap"),
        "pe_ratio": info.get("trailingPE"),
        "forward_pe": info.get("forwardPE"),
        "eps": info.get("trailingEps"),
        "52w_high": info.get("fiftyTwoWeekHigh"),
        "52w_low": info.get("fiftyTwoWeekLow"),
        "50d_avg": info.get("fiftyDayAverage"),
        "200d_avg": info.get("twoHundredDayAverage"),
        "volume": info.get("volume"),
        "avg_volume": info.get("averageVolume"),
        "beta": info.get("beta"),
        "dividend_yield": info.get("dividendYield"),
        "sector": info.get("sector", "N/A"),
        "industry": info.get("industry", "N/A"),
    }

    # 1-month price trend
    if len(hist) > 0:
        result["1mo_high"] = round(hist["High"].max(), 2)
        result["1mo_low"] = round(hist["Low"].min(), 2)
        result["1mo_return"] = round((hist["Close"].iloc[-1] / hist["Close"].iloc[0] - 1) * 100, 2)

    return result


def format_output(data):
    lines = [f"📊 {data['name']} ({data['ticker']})"]
    lines.append(f"类型: {data['type']} | 货币: {data['currency']}")
    lines.append(f"")
    if data["price"]:
        arrow = "🟢" if (data.get("change_pct") or 0) >= 0 else "🔴"
        lines.append(f"💰 价格: {data['price']} {arrow} {data.get('change_pct', 'N/A')}%")
    if data.get("market_cap"):
        mc = data["market_cap"]
        if mc >= 1e12: mc_str = f"{mc/1e12:.2f}T"
        elif mc >= 1e9: mc_str = f"{mc/1e9:.2f}B"
        elif mc >= 1e6: mc_str = f"{mc/1e6:.2f}M"
        else: mc_str = str(mc)
        lines.append(f"📈 市值: {mc_str}")
    if data.get("pe_ratio"): lines.append(f"📊 P/E: {data['pe_ratio']:.1f} | Forward P/E: {data.get('forward_pe', 'N/A')}")
    if data.get("eps"): lines.append(f"💵 EPS: {data['eps']}")
    if data.get("52w_high"): lines.append(f"📏 52周: {data['52w_low']} ~ {data['52w_high']}")
    if data.get("50d_avg"): lines.append(f"📉 均线: 50D={data['50d_avg']:.2f} | 200D={data.get('200d_avg', 'N/A')}")
    if data.get("volume"): lines.append(f"📦 成交量: {data['volume']:,} | 均量: {data.get('avg_volume', 'N/A'):,}")
    if data.get("beta"): lines.append(f"⚡ Beta: {data['beta']:.2f}")
    if data.get("dividend_yield"): lines.append(f"💎 股息率: {data['dividend_yield']*100:.2f}%")
    if data.get("sector") != "N/A": lines.append(f"🏢 行业: {data['sector']} / {data['industry']}")
    if data.get("1mo_return") is not None: lines.append(f"📅 1月回报: {data['1mo_return']}%")
    return "\n".join(lines)


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--ticker", required=True, help="Ticker symbol (e.g. AAPL, BTC-USD)")
    p.add_argument("--json", action="store_true", help="Output raw JSON")
    a = p.parse_args()
    data = analyze(a.ticker.upper())
    if a.json:
        print(json.dumps(data, indent=2, ensure_ascii=False))
    else:
        print(format_output(data))

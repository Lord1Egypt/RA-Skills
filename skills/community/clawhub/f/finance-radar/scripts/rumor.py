#!/usr/bin/env python3
"""Rumor & early signal detection."""

import argparse, json, sys

def ensure_yfinance():
    try:
        import yfinance; return yfinance
    except ImportError:
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "yfinance", "-q"])
        import yfinance; return yfinance


def detect_signals(ticker):
    yf = ensure_yfinance()
    t = yf.Ticker(ticker)
    info = t.info or {}
    hist = t.history(period="3mo")
    signals = []

    if len(hist) < 5:
        return {"ticker": ticker, "signals": [], "alert_level": "low"}

    # 1. Unusual volume spike (last 5 days vs avg)
    recent_vol = hist["Volume"].tail(5).mean()
    avg_vol = hist["Volume"].mean()
    if avg_vol > 0 and recent_vol / avg_vol > 2:
        signals.append({"type": "volume_spike", "severity": "high",
            "detail": f"近5日均量是历史均量的 {recent_vol/avg_vol:.1f}x"})

    # 2. Price breakout (new highs/lows)
    last_price = hist["Close"].iloc[-1]
    high_3m = hist["High"].max()
    low_3m = hist["Low"].min()
    if last_price >= high_3m * 0.98:
        signals.append({"type": "breakout_high", "severity": "medium",
            "detail": f"接近3月新高 {high_3m:.2f}"})
    if last_price <= low_3m * 1.02:
        signals.append({"type": "breakout_low", "severity": "high",
            "detail": f"接近3月新低 {low_3m:.2f}"})

    # 3. Sudden price move (>5% in a day)
    daily_returns = hist["Close"].pct_change().tail(5)
    for date, ret in daily_returns.items():
        if abs(ret) > 0.05:
            direction = "暴涨" if ret > 0 else "暴跌"
            signals.append({"type": "sudden_move", "severity": "high",
                "detail": f"{date.strftime('%m-%d')} {direction} {ret*100:.1f}%"})

    # 4. Options/insider activity hints (via info fields)
    short_ratio = info.get("shortRatio")
    if short_ratio and short_ratio > 5:
        signals.append({"type": "high_short", "severity": "medium",
            "detail": f"做空比率偏高: {short_ratio:.1f}"})

    # 5. Earnings approaching
    try:
        import datetime
        earnings_dates = t.earnings_dates
        if earnings_dates is not None and len(earnings_dates) > 0:
            next_earn = earnings_dates.index[0]
            if hasattr(next_earn, 'date'):
                days_to = (next_earn.date() - datetime.date.today()).days
                if 0 < days_to <= 14:
                    signals.append({"type": "earnings_soon", "severity": "medium",
                        "detail": f"财报将在 {days_to} 天后发布"})
    except Exception:
        pass  # lxml may not be available

    # 6. Analyst upgrade/downgrade hints
    rec = info.get("recommendationMean")
    rec_key = info.get("recommendationKey", "")
    if rec and rec <= 1.5:
        signals.append({"type": "strong_buy", "severity": "low",
            "detail": f"分析师共识: {rec_key} ({rec:.1f})"})

    alert = "high" if any(s["severity"] == "high" for s in signals) else \
            "medium" if signals else "low"

    return {
        "ticker": ticker,
        "name": info.get("shortName", ticker),
        "price": round(last_price, 2),
        "signals": signals,
        "signal_count": len(signals),
        "alert_level": alert,
    }


def format_output(data):
    icons = {"high": "🔴", "medium": "🟡", "low": "🟢"}
    lines = [f"🕵️ {data['name']} ({data['ticker']}) — 信号检测"]
    lines.append(f"价格: {data['price']} | 警报级别: {icons[data['alert_level']]} {data['alert_level']}")
    lines.append(f"发现 {data['signal_count']} 个信号:")
    lines.append("")
    for s in data["signals"]:
        lines.append(f"  {icons[s['severity']]} [{s['type']}] {s['detail']}")
    if not data["signals"]:
        lines.append("  ✅ 暂无异常信号")
    return "\n".join(lines)


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--ticker", required=True)
    p.add_argument("--json", action="store_true")
    a = p.parse_args()
    data = detect_signals(a.ticker.upper())
    print(json.dumps(data, indent=2, default=str) if a.json else format_output(data))

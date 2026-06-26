#!/usr/bin/env python3
import argparse
import csv
import json
import math
from dataclasses import dataclass
from typing import List, Optional


def _f(v: str) -> float:
    return float(v.strip())


def read_ohlcv(path: str):
    rows = []
    with open(path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            norm = {k.strip().lower(): (v.strip() if isinstance(v, str) else v) for k, v in r.items()}
            rows.append(
                {
                    "date": norm.get("date") or norm.get("datetime") or norm.get("time") or "",
                    "open": _f(norm["open"]),
                    "high": _f(norm["high"]),
                    "low": _f(norm["low"]),
                    "close": _f(norm["close"]),
                    "volume": _f(norm.get("volume", "0") or "0"),
                }
            )
    if len(rows) < 60:
        raise ValueError("Need at least 60 rows for stable indicators.")
    return rows


def sma(vals: List[float], n: int) -> List[Optional[float]]:
    out: List[Optional[float]] = [None] * len(vals)
    s = 0.0
    for i, v in enumerate(vals):
        s += v
        if i >= n:
            s -= vals[i - n]
        if i >= n - 1:
            out[i] = s / n
    return out


def ema(vals: List[float], n: int) -> List[Optional[float]]:
    out: List[Optional[float]] = [None] * len(vals)
    k = 2.0 / (n + 1)
    e = None
    for i, v in enumerate(vals):
        if e is None:
            e = v
        else:
            e = v * k + e * (1 - k)
        if i >= n - 1:
            out[i] = e
    return out


def rsi(closes: List[float], n: int = 14) -> List[Optional[float]]:
    out: List[Optional[float]] = [None] * len(closes)
    gains = [0.0]
    losses = [0.0]
    for i in range(1, len(closes)):
        ch = closes[i] - closes[i - 1]
        gains.append(max(ch, 0.0))
        losses.append(max(-ch, 0.0))

    avg_gain = sum(gains[1 : n + 1]) / n
    avg_loss = sum(losses[1 : n + 1]) / n
    for i in range(n, len(closes)):
        if i > n:
            avg_gain = (avg_gain * (n - 1) + gains[i]) / n
            avg_loss = (avg_loss * (n - 1) + losses[i]) / n
        if avg_loss == 0:
            out[i] = 100.0
        else:
            rs = avg_gain / avg_loss
            out[i] = 100 - (100 / (1 + rs))
    return out


def atr(highs: List[float], lows: List[float], closes: List[float], n: int = 14) -> List[Optional[float]]:
    tr = [0.0]
    for i in range(1, len(closes)):
        tr.append(max(highs[i] - lows[i], abs(highs[i] - closes[i - 1]), abs(lows[i] - closes[i - 1])))
    out = [None] * len(closes)
    a = sum(tr[1 : n + 1]) / n
    for i in range(n, len(closes)):
        if i > n:
            a = (a * (n - 1) + tr[i]) / n
        out[i] = a
    return out


@dataclass
class SignalResult:
    signal: str
    confidence: float
    entry: Optional[float]
    stop: Optional[float]
    target: Optional[float]
    size: Optional[float]
    reason: str


def generate(rows, strategy: str, account_size: float, risk_per_trade: float) -> SignalResult:
    closes = [r["close"] for r in rows]
    highs = [r["high"] for r in rows]
    lows = [r["low"] for r in rows]

    sma20 = sma(closes, 20)
    sma50 = sma(closes, 50)
    ema12 = ema(closes, 12)
    ema26 = ema(closes, 26)
    macd_line = [None if ema12[i] is None or ema26[i] is None else ema12[i] - ema26[i] for i in range(len(closes))]
    macd_sig = ema([x if x is not None else 0.0 for x in macd_line], 9)
    rsi14 = rsi(closes, 14)
    atr14 = atr(highs, lows, closes, 14)

    i = len(rows) - 1
    px = closes[i]
    if any(x is None for x in (sma20[i], sma50[i], macd_line[i], macd_sig[i], rsi14[i], atr14[i])):
        return SignalResult("flat", 0.0, None, None, None, None, "Indicators not warmed up")

    s20 = float(sma20[i])
    s50 = float(sma50[i])
    m = float(macd_line[i])
    ms = float(macd_sig[i])
    r = float(rsi14[i])
    a = float(atr14[i])

    signal = "flat"
    conf = 0.0
    reason = "No edge"

    if strategy == "trend":
        if px > s20 > s50 and m > ms and 45 <= r <= 68:
            signal = "long"
            conf = 0.72
            reason = "Uptrend alignment: price>SMA20>SMA50, MACD bullish, RSI healthy"
        elif px < s20 < s50 and m < ms and 32 <= r <= 55:
            signal = "short"
            conf = 0.72
            reason = "Downtrend alignment: price<SMA20<SMA50, MACD bearish, RSI weak"
    elif strategy == "mean-reversion":
        if px < s20 and r < 30:
            signal = "long"
            conf = 0.62
            reason = "Oversold pullback below SMA20 with RSI<30"
        elif px > s20 and r > 70:
            signal = "short"
            conf = 0.62
            reason = "Overbought extension above SMA20 with RSI>70"
    elif strategy == "breakout":
        lookback = 20
        hh = max(highs[-lookback:])
        ll = min(lows[-lookback:])
        if px >= hh and m > ms:
            signal = "long"
            conf = 0.68
            reason = "20-bar high breakout with MACD confirmation"
        elif px <= ll and m < ms:
            signal = "short"
            conf = 0.68
            reason = "20-bar low breakdown with MACD confirmation"
    else:
        raise ValueError("Unknown strategy")

    if signal == "flat":
        return SignalResult(signal, conf, None, None, None, None, reason)

    stop = px - 1.5 * a if signal == "long" else px + 1.5 * a
    target = px + 3.0 * a if signal == "long" else px - 3.0 * a

    risk_budget = account_size * risk_per_trade
    per_unit_risk = abs(px - stop)
    size = 0.0 if per_unit_risk <= 0 else risk_budget / per_unit_risk
    size = math.floor(size * 1000) / 1000.0

    return SignalResult(signal, conf, px, stop, target, size, reason)


def main():
    ap = argparse.ArgumentParser(description="Generate TA signal from OHLCV CSV")
    ap.add_argument("--csv", required=True, help="Path to OHLCV csv")
    ap.add_argument("--symbol", default="UNKNOWN")
    ap.add_argument("--strategy", choices=["trend", "mean-reversion", "breakout"], default="trend")
    ap.add_argument("--account-size", type=float, default=100000.0)
    ap.add_argument("--risk-per-trade", type=float, default=0.01)
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    rows = read_ohlcv(args.csv)
    res = generate(rows, args.strategy, args.account_size, args.risk_per_trade)
    out = {
        "symbol": args.symbol,
        "strategy": args.strategy,
        "bars": len(rows),
        "as_of": rows[-1]["date"],
        "signal": res.signal,
        "confidence": round(res.confidence, 3),
        "entry": res.entry,
        "stop": res.stop,
        "target": res.target,
        "size": res.size,
        "reason": res.reason,
    }

    if args.json:
        print(json.dumps(out, ensure_ascii=True, indent=2))
    else:
        for k, v in out.items():
            print(f"{k}: {v}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
import argparse
import csv
import json
import math
import sys
import time
import urllib.parse
import urllib.request
from datetime import datetime, timezone


INTERVALS = {
    "1m", "3m", "5m", "15m", "30m",
    "1h", "2h", "4h", "6h", "8h", "12h",
    "1d", "3d", "1w", "1M",
}


def fetch_binance_klines(symbol, interval, limit, market, base_url):
    if interval not in INTERVALS:
        raise ValueError(f"Unsupported interval: {interval}")
    path = "/api/v3/klines" if market == "spot" else "/fapi/v1/klines"
    query = urllib.parse.urlencode({
        "symbol": symbol.upper(),
        "interval": interval,
        "limit": limit,
    })
    url = base_url.rstrip("/") + path + "?" + query
    req = urllib.request.Request(url, headers={"User-Agent": "crypto-one-way-market/1.0"})
    with urllib.request.urlopen(req, timeout=20) as resp:
        raw = json.loads(resp.read().decode("utf-8"))
    candles = []
    for row in raw:
        candles.append({
            "open_time": int(row[0]),
            "open": float(row[1]),
            "high": float(row[2]),
            "low": float(row[3]),
            "close": float(row[4]),
            "volume": float(row[5]),
            "close_time": int(row[6]),
        })
    return candles, url


def ema(values, period):
    if not values:
        return []
    alpha = 2 / (period + 1)
    out = [values[0]]
    for value in values[1:]:
        out.append(alpha * value + (1 - alpha) * out[-1])
    return out


def rma(values, period):
    if not values:
        return []
    out = []
    avg = None
    for i, value in enumerate(values):
        if i < period:
            out.append(None)
            if avg is None:
                avg = 0.0
            avg += value
            if i == period - 1:
                avg /= period
                out[-1] = avg
        else:
            avg = (avg * (period - 1) + value) / period
            out.append(avg)
    return out


def compute_adx(candles, period=14):
    trs, plus_dm, minus_dm = [], [], []
    for i in range(1, len(candles)):
        cur, prev = candles[i], candles[i - 1]
        up_move = cur["high"] - prev["high"]
        down_move = prev["low"] - cur["low"]
        plus_dm.append(up_move if up_move > down_move and up_move > 0 else 0.0)
        minus_dm.append(down_move if down_move > up_move and down_move > 0 else 0.0)
        tr = max(
            cur["high"] - cur["low"],
            abs(cur["high"] - prev["close"]),
            abs(cur["low"] - prev["close"]),
        )
        trs.append(tr)

    atr = rma(trs, period)
    p_dm = rma(plus_dm, period)
    m_dm = rma(minus_dm, period)
    dx = []
    for a, p, m in zip(atr, p_dm, m_dm):
        if a is None or not a:
            dx.append(None)
            continue
        pdi = 100 * p / a
        mdi = 100 * m / a
        denom = pdi + mdi
        dx.append(0.0 if denom == 0 else 100 * abs(pdi - mdi) / denom)

    valid_dx = [x for x in dx if x is not None]
    adx_values = rma(valid_dx, period)
    latest_adx = next((x for x in reversed(adx_values) if x is not None), None)
    latest_atr = next((x for x in reversed(atr) if x is not None), None)
    return latest_adx, latest_atr


def max_countertrend_pullback(candles, direction):
    closes = [c["close"] for c in candles]
    first, last = closes[0], closes[-1]
    net = abs(last - first)
    if net == 0:
        return 1.0
    worst = 0.0
    if direction > 0:
        peak = closes[0]
        for close in closes:
            peak = max(peak, close)
            worst = max(worst, peak - close)
    else:
        trough = closes[0]
        for close in closes:
            trough = min(trough, close)
            worst = max(worst, close - trough)
    return worst / net


def classify(candles):
    if len(candles) < 60:
        raise ValueError("Need at least 60 candles for a stable classification")

    closes = [c["close"] for c in candles]
    first, last = closes[0], closes[-1]
    net_move = last - first
    direction = 1 if net_move > 0 else -1 if net_move < 0 else 0
    directional_return = last / first - 1
    path = sum(abs(closes[i] - closes[i - 1]) for i in range(1, len(closes)))
    efficiency = 0.0 if path == 0 else abs(net_move) / path
    adx, atr = compute_adx(candles)
    atr_move = 0.0 if not atr else abs(net_move) / atr
    pullback = max_countertrend_pullback(candles, direction) if direction else 1.0
    ema20, ema50 = ema(closes, 20), ema(closes, 50)
    ema20_slope = ema20[-1] - ema20[max(0, len(ema20) - 10)]
    ema50_slope = ema50[-1] - ema50[max(0, len(ema50) - 20)]
    ma_agrees = (
        direction > 0 and ema20_slope > 0 and ema50_slope > 0 and last > ema20[-1] > ema50[-1]
    ) or (
        direction < 0 and ema20_slope < 0 and ema50_slope < 0 and last < ema20[-1] < ema50[-1]
    )

    score = 0
    score += 1 if abs(directional_return) >= 0.015 else 0
    score += 2 if efficiency >= 0.60 else 1 if efficiency >= 0.45 else 0
    score += 2 if adx is not None and adx >= 35 else 1 if adx is not None and adx >= 25 else 0
    score += 1 if atr_move >= 3.0 else 0
    score += 1 if pullback <= 0.35 else 0
    score += 1 if ma_agrees else 0

    if direction and score >= 6:
        classification = "bullish_one_way" if direction > 0 else "bearish_one_way"
    elif direction and score >= 4:
        classification = "weak_trend"
    else:
        classification = "range_or_chop"

    confidence = min(0.95, max(0.15, score / 8))
    return {
        "classification": classification,
        "confidence": round(confidence, 3),
        "direction": "up" if direction > 0 else "down" if direction < 0 else "flat",
        "first_close": first,
        "last_close": last,
        "directional_return_pct": round(directional_return * 100, 4),
        "trend_efficiency": round(efficiency, 4),
        "adx": None if adx is None else round(adx, 2),
        "atr": None if atr is None else round(atr, 8),
        "atr_normalized_move": round(atr_move, 3),
        "max_countertrend_pullback": round(pullback, 4),
        "ema20_slope": round(ema20_slope, 8),
        "ema50_slope": round(ema50_slope, 8),
        "ma_agrees": ma_agrees,
        "score": score,
    }


def iso_ms(ms):
    return datetime.fromtimestamp(ms / 1000, tz=timezone.utc).isoformat()


def write_csv(path, candles):
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(candles[0].keys()))
        writer.writeheader()
        writer.writerows(candles)


def main():
    parser = argparse.ArgumentParser(description="Fetch crypto candles and classify one-way market structure.")
    parser.add_argument("--symbol", default="BTCUSDT")
    parser.add_argument("--interval", default="15m")
    parser.add_argument("--limit", type=int, default=200)
    parser.add_argument("--market", choices=["spot", "futures"], default="spot")
    parser.add_argument("--base-url", default="https://api.binance.com")
    parser.add_argument("--output", help="Optional CSV output path for candles")
    parser.add_argument("--json", action="store_true", help="Emit JSON only")
    args = parser.parse_args()

    if args.limit < 60 or args.limit > 1000:
        raise SystemExit("--limit must be between 60 and 1000")

    candles, source_url = fetch_binance_klines(args.symbol, args.interval, args.limit, args.market, args.base_url)
    result = classify(candles)
    payload = {
        "symbol": args.symbol.upper(),
        "interval": args.interval,
        "market": args.market,
        "source_url": source_url,
        "candles": len(candles),
        "start_utc": iso_ms(candles[0]["open_time"]),
        "end_utc": iso_ms(candles[-1]["close_time"]),
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "analysis": result,
    }

    if args.output:
        write_csv(args.output, candles)
        payload["csv_output"] = args.output

    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        a = payload["analysis"]
        print(f"{payload['symbol']} {payload['interval']} {payload['market']} candles={payload['candles']}")
        print(f"span_utc: {payload['start_utc']} -> {payload['end_utc']}")
        print(f"classification: {a['classification']} confidence={a['confidence']}")
        print(
            "metrics: "
            f"return={a['directional_return_pct']}% "
            f"efficiency={a['trend_efficiency']} "
            f"adx={a['adx']} "
            f"atr_move={a['atr_normalized_move']} "
            f"pullback={a['max_countertrend_pullback']} "
            f"ma_agrees={a['ma_agrees']} "
            f"score={a['score']}/8"
        )


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        sys.exit(1)

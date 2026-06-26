#!/usr/bin/env python3
"""
Fetch Binance public REST ticker + klines; compute SMA / RSI / MACD / Bollinger / ATR (stdlib only).
Output JSON on stdout for use with OpenClaw `exec`.

Usage:
  python3 crypto_market_snapshot.py BTCUSDT 1d 200

Env (optional):
  CRYPTO_HTTP_PROXY / HTTP_PROXY / HTTPS_PROXY — passed to urllib opener if set.
"""
from __future__ import annotations

import json
import math
import os
import sys
import urllib.request


def _sma(closes: list[float], period: int) -> list[float | None]:
    out: list[float | None] = []
    for i in range(len(closes)):
        if i + 1 < period:
            out.append(None)
        else:
            out.append(sum(closes[i + 1 - period : i + 1]) / period)
    return out


def _ema(series: list[float], period: int) -> list[float | None]:
    k = 2.0 / (period + 1)
    out: list[float | None] = []
    prev: float | None = None
    for i, x in enumerate(series):
        if i + 1 < period:
            out.append(None)
            continue
        if prev is None:
            seed = sum(series[i + 1 - period : i + 1]) / period
            prev = seed
            out.append(prev)
        else:
            prev = x * k + prev * (1 - k)
            out.append(prev)
    return out


def _rsi(closes: list[float], period: int = 14) -> list[float | None]:
    out: list[float | None] = [None] * len(closes)
    gains: list[float] = []
    losses: list[float] = []
    for i in range(1, len(closes)):
        ch = closes[i] - closes[i - 1]
        gains.append(max(ch, 0.0))
        losses.append(max(-ch, 0.0))
    for i in range(period, len(closes)):
        ag = sum(gains[i - period : i]) / period
        al = sum(losses[i - period : i]) / period
        if al == 0:
            out[i] = 100.0 if ag > 0 else 50.0
        else:
            rs = ag / al
            out[i] = 100.0 - (100.0 / (1.0 + rs))
    return out


def _stddev(window: list[float]) -> float:
    m = sum(window) / len(window)
    v = sum((x - m) ** 2 for x in window) / len(window)
    return math.sqrt(v)


def _true_range(high: float, low: float, prev_close: float) -> float:
    return max(high - low, abs(high - prev_close), abs(low - prev_close))


def fetch_json(url: str) -> dict | list:
    req = urllib.request.Request(url, method="GET")
    req.add_header("User-Agent", "openclaw-skill-crypto-market/1.0")
    proxy = (
        os.environ.get("CRYPTO_HTTP_PROXY")
        or os.environ.get("HTTPS_PROXY")
        or os.environ.get("HTTP_PROXY")
        or ""
    ).strip()
    if proxy:
        opener = urllib.request.build_opener(urllib.request.ProxyHandler({"http": proxy, "https": proxy}))
        with opener.open(req, timeout=60) as resp:
            return json.loads(resp.read().decode("utf-8"))
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.loads(resp.read().decode("utf-8"))


def main() -> int:
    if len(sys.argv) < 2:
        print(json.dumps({"ok": False, "detail": "usage: crypto_market_snapshot.py BTCUSDT [interval] [limit]"}))
        return 2
    symbol = sys.argv[1].upper().replace("/", "")
    interval = (sys.argv[2] if len(sys.argv) > 2 else "1d").lower()
    limit = int(sys.argv[3]) if len(sys.argv) > 3 else 200

    base = "https://api.binance.com"
    try:
        ticker = fetch_json(f"{base}/api/v3/ticker/24hr?symbol={symbol}")
        klines = fetch_json(
            f"{base}/api/v3/klines?symbol={symbol}&interval={interval}&limit={limit}"
        )
    except Exception as e:
        print(json.dumps({"ok": False, "detail": str(e), "exchange": "binance", "symbol": symbol}))
        return 1

    # kline: [ open time, open, high, low, close, volume, ... ]
    ts = [int(k[0]) for k in klines]
    opens = [float(k[1]) for k in klines]
    highs = [float(k[2]) for k in klines]
    lows = [float(k[3]) for k in klines]
    closes = [float(k[4]) for k in klines]
    vols = [float(k[5]) for k in klines]

    sma20 = _sma(closes, 20)
    rsi14 = _rsi(closes, 14)
    ema12 = _ema(closes, 12)
    ema26 = _ema(closes, 26)
    macd_line: list[float | None] = []
    for i in range(len(closes)):
        a, b = ema12[i], ema26[i]
        macd_line.append((a - b) if a is not None and b is not None else None)
    # 9-period EMA of MACD line (only on defined macd points; align back to index)
    macd_vals: list[float] = []
    macd_idx: list[int] = []
    for i, m in enumerate(macd_line):
        if m is not None:
            macd_vals.append(m)
            macd_idx.append(i)
    sig_vals = _ema(macd_vals, 9) if len(macd_vals) >= 9 else [None] * len(macd_vals)
    signal: list[float | None] = [None] * len(closes)
    for j, i in enumerate(macd_idx):
        if sig_vals[j] is not None:
            signal[i] = sig_vals[j]
    hist = [
        (m - s) if m is not None and s is not None else None
        for m, s in zip(macd_line, signal, strict=False)
    ]

    bb_mid = _sma(closes, 20)
    bb_up: list[float | None] = []
    bb_lo: list[float | None] = []
    for i in range(len(closes)):
        if i + 1 < 20 or bb_mid[i] is None:
            bb_up.append(None)
            bb_lo.append(None)
        else:
            sd = _stddev(closes[i + 1 - 20 : i + 1])
            bb_up.append(bb_mid[i] + 2 * sd)
            bb_lo.append(bb_mid[i] - 2 * sd)

    atr14: list[float | None] = [None] * len(closes)
    trs: list[float] = []
    for i in range(len(closes)):
        prev_c = closes[i - 1] if i > 0 else closes[0]
        trs.append(_true_range(highs[i], lows[i], prev_c))
    for i in range(13, len(closes)):
        atr14[i] = sum(trs[i + 1 - 14 : i + 1]) / 14

    last = len(closes) - 1
    payload = {
        "ok": True,
        "exchange": "binance",
        "symbol": symbol,
        "interval": interval,
        "ticker_24h": ticker,
        "ohlcv_meta": {
            "count": len(closes),
            "columns": ["timestamp_ms", "open", "high", "low", "close", "volume"],
            "last_row": [ts[last], opens[last], highs[last], lows[last], closes[last], vols[last]],
        },
        "indicators": {
            "sma_20": {"latest": sma20[last], "period": 20},
            "rsi_14": {"latest": rsi14[last], "period": 14},
            "macd_12_26_9": {
                "latest": {
                    "macd": macd_line[last],
                    "signal": signal[last],
                    "hist": hist[last],
                }
            },
            "bollinger_20_2": {
                "latest": {
                    "mid": bb_mid[last],
                    "upper": bb_up[last],
                    "lower": bb_lo[last],
                }
            },
            "atr_14": {"latest": atr14[last], "period": 14},
        },
        "note": "Public Binance REST only; not investment advice.",
    }
    print(json.dumps(payload, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

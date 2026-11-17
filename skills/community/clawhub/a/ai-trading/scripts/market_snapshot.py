#!/usr/bin/env python3
"""market_snapshot.py - US equity/ETF snapshot with technicals.

Sources: a market data provider (when an API key is present) or a local CSV
with columns date,open,high,low,close,volume. Stdlib only.

Usage:
    python3 market_snapshot.py --symbol AAPL
    python3 market_snapshot.py --symbol AAPL --provider finnhub --out snap.json
    python3 market_snapshot.py --symbol AAPL --bars /path/to/aapl.csv
    python3 market_snapshot.py --symbol SPY --bars spy.csv --sma 20 50 200 --rsi 14

Everything printed carries a source and an ET timestamp. Nothing is estimated:
if a value is unavailable it is reported as unavailable.
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone

try:  # Python 3.9+
    from zoneinfo import ZoneInfo

    ET = ZoneInfo("America/New_York")
except Exception:  # pragma: no cover - fallback when tzdata is missing
    ET = timezone.utc


def et_now() -> datetime:
    return datetime.now(ET)


def http_json(url: str, headers: dict, timeout: int = 20) -> dict:
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8"))


# --------------------------------------------------------------------------- #
# indicators
# --------------------------------------------------------------------------- #
def sma(values: list, period: int) -> float | None:
    if len(values) < period or period <= 0:
        return None
    return round(sum(values[-period:]) / period, 4)


def ema_series(values: list, period: int) -> list:
    if len(values) < period or period <= 0:
        return []
    k = 2.0 / (period + 1.0)
    seed = sum(values[:period]) / period
    out = [seed]
    for price in values[period:]:
        out.append(price * k + out[-1] * (1 - k))
    return out


def rsi(values: list, period: int = 14) -> float | None:
    if len(values) < period + 1:
        return None
    gains, losses = [], []
    for prev, cur in zip(values[:-1], values[1:]):
        change = cur - prev
        gains.append(max(change, 0.0))
        losses.append(max(-change, 0.0))
    avg_gain = sum(gains[:period]) / period
    avg_loss = sum(losses[:period]) / period
    for g, l in zip(gains[period:], losses[period:]):
        avg_gain = (avg_gain * (period - 1) + g) / period
        avg_loss = (avg_loss * (period - 1) + l) / period
    if avg_loss == 0:
        return 100.0
    rs = avg_gain / avg_loss
    return round(100 - (100 / (1 + rs)), 2)


def true_range(bars: list) -> list:
    trs = []
    for idx in range(1, len(bars)):
        high = bars[idx]["high"]
        low = bars[idx]["low"]
        prev_close = bars[idx - 1]["close"]
        trs.append(max(high - low, abs(high - prev_close), abs(low - prev_close)))
    return trs


def atr(bars: list, period: int = 14) -> float | None:
    trs = true_range(bars)
    if len(trs) < period:
        return None
    return round(sum(trs[-period:]) / period, 4)


def annualized_vol(closes: list, periods: int = 252) -> float | None:
    if len(closes) < 30:
        return None
    rets = [(b / a - 1) for a, b in zip(closes[:-1], closes[1:]) if a]
    if len(rets) < 20:
        return None
    mean = sum(rets) / len(rets)
    var = sum((r - mean) ** 2 for r in rets) / (len(rets) - 1)
    return round((var ** 0.5) * (periods ** 0.5) * 100, 2)


def max_drawdown(closes: list) -> float | None:
    if len(closes) < 5:
        return None
    peak, worst = closes[0], 0.0
    for price in closes:
        peak = max(peak, price)
        dd = (price / peak - 1) * 100
        worst = min(worst, dd)
    return round(worst, 2)


# --------------------------------------------------------------------------- #
# data loading
# --------------------------------------------------------------------------- #
def load_csv(path: str) -> list:
    bars = []
    with open(path, "r", encoding="utf-8-sig", newline="") as fh:
        reader = csv.DictReader(fh)
        if not reader.fieldnames:
            raise SystemExit("CSV has no header row.")
        lowered = {name.strip().lower(): name for name in reader.fieldnames}
        required = ("date", "open", "high", "low", "close", "volume")
        missing = [c for c in required if c not in lowered]
        if missing:
            raise SystemExit(f"CSV header must contain {required}. Missing: {missing}")
        for row in reader:
            try:
                bars.append(
                    {
                        "date": str(row[lowered["date"]]).strip(),
                        "open": float(row[lowered["open"]]),
                        "high": float(row[lowered["high"]]),
                        "low": float(row[lowered["low"]]),
                        "close": float(row[lowered["close"]]),
                        "volume": float(row[lowered["volume"]] or 0),
                    }
                )
            except (TypeError, ValueError):
                continue
    bars.sort(key=lambda b: b["date"])
    return bars


def fetch_finnhub(symbol: str, key: str, range_days: int = 365) -> tuple:
    quote = http_json(
        f"https://finnhub.io/api/v1/quote?symbol={urllib.parse.quote(symbol)}&token={key}"
    )
    end = et_now()
    start = end.timestamp() - range_days * 86400
    url = (
        "https://finnhub.io/api/v1/stock/candle?symbol="
        f"{urllib.parse.quote(symbol)}&resolution=D&from={int(start)}&to={int(end.timestamp())}&token={key}"
    )
    raw = http_json(url)
    bars = []
    for row in raw.get("c", []):
        if len(row) < 5:
            continue
        ts, o, h, l, c = row[0], row[1], row[2], row[3], row[4]
        v = row[5] if len(row) > 5 else 0
        bars.append(
            {
                "date": datetime.fromtimestamp(ts, ET).strftime("%Y-%m-%d"),
                "open": o,
                "high": h,
                "low": l,
                "close": c,
                "volume": v,
            }
        )
    bars.sort(key=lambda b: b["date"])
    return quote, bars


def fetch_twelvedata(symbol: str, key: str) -> tuple:
    quote = http_json(
        f"https://api.twelvedata.com/quote?symbol={urllib.parse.quote(symbol)}&apikey={key}"
    )
    series = http_json(
        f"https://api.twelvedata.com/time_series?symbol={urllib.parse.quote(symbol)}"
        f"&interval=1day&outputsize=400&apikey={key}"
    )
    bars = []
    for row in series.get("values", []):
        try:
            bars.append(
                {
                    "date": row["datetime"][:10],
                    "open": float(row["open"]),
                    "high": float(row["high"]),
                    "low": float(row["low"]),
                    "close": float(row["close"]),
                    "volume": float(row.get("volume") or 0),
                }
            )
        except (KeyError, TypeError, ValueError):
            continue
    bars.sort(key=lambda b: b["date"])
    return quote, bars


PROVIDERS = {
    "finnhub": ("FINNHUB_API_KEY", fetch_finnhub),
    "twelvedata": ("TWELVE_DATA_API_KEY", fetch_twelvedata),
}


# --------------------------------------------------------------------------- #
# snapshot
# --------------------------------------------------------------------------- #
def build_snapshot(symbol: str, bars: list, quote: dict, source: str) -> dict:
    closes = [b["close"] for b in bars]
    highs = [b["high"] for b in bars]
    lows = [b["low"] for b in bars]
    vols = [b["volume"] for b in bars]
    snap = {
        "symbol": symbol.upper(),
        "generated_at_et": et_now().isoformat(timespec="seconds"),
        "source": source,
        "bars_used": len(bars),
        "last_bar_date": bars[-1]["date"] if bars else None,
        "last_close": closes[-1] if closes else None,
        "quote": quote or {},
        "technicals": {},
        "availability": {},
    }
    if closes:
        snap["technicals"]["sma_20"] = sma(closes, 20)
        snap["technicals"]["sma_50"] = sma(closes, 50)
        snap["technicals"]["sma_200"] = sma(closes, 200)
        snap["technicals"]["rsi_14"] = rsi(closes, 14)
        snap["technicals"]["atr_14"] = atr(bars, 14)
        snap["technicals"]["high_52w"] = round(max(highs), 4) if highs else None
        snap["technicals"]["low_52w"] = round(min(lows), 4) if lows else None
        snap["technicals"]["avg_volume_20"] = int(sum(vols[-20:]) / min(20, len(vols))) if vols else None
        snap["technicals"]["annualized_vol_pct"] = annualized_vol(closes)
        snap["technicals"]["max_drawdown_pct"] = max_drawdown(closes)
        snap["technicals"]["pct_from_52w_high"] = (
            round((closes[-1] / max(highs) - 1) * 100, 2) if highs and max(highs) else None
        )
        ema20 = ema_series(closes, 20)
        snap["technicals"]["ema_20"] = round(ema20[-1], 4) if ema20 else None
    for name in ("sma_200", "atr_14", "annualized_vol_pct", "high_52w"):
        snap["availability"][name] = "ok" if snap["technicals"].get(name) is not None else "unavailable"
    return snap


def render(snap: dict) -> str:
    t = snap["technicals"]
    lines = [
        f"Symbol        : {snap['symbol']}",
        f"Generated (ET): {snap['generated_at_et']}",
        f"Source        : {snap['source']}",
        f"Bars used     : {snap['bars_used']} (last bar {snap['last_bar_date']})",
        "",
        f"Last close    : {snap['last_close']}",
        f"SMA 20/50/200 : {t.get('sma_20')} / {t.get('sma_50')} / {t.get('sma_200')}",
        f"EMA 20        : {t.get('ema_20')}",
        f"RSI 14        : {t.get('rsi_14')}",
        f"ATR 14        : {t.get('atr_14')}",
        f"52w high/low  : {t.get('high_52w')} / {t.get('low_52w')}",
        f"% from 52w hi : {t.get('pct_from_52w_high')}%",
        f"Avg vol (20)  : {t.get('avg_volume_20')}",
        f"Ann. vol      : {t.get('annualized_vol_pct')}%",
        f"Max drawdown  : {t.get('max_drawdown_pct')}%",
        "",
        "Values marked unavailable need more history or a data source. Do not estimate them.",
    ]
    quote = snap.get("quote") or {}
    if quote:
        lines.insert(6, f"Live quote     : {json.dumps(quote)[:220]}")
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser(description="US market snapshot with technicals.")
    ap.add_argument("--symbol", required=True, help="US ticker, e.g. AAPL, SPY, BRK.B")
    ap.add_argument("--provider", default="auto", choices=["auto", "finnhub", "twelvedata", "csv"])
    ap.add_argument("--bars", help="Local CSV: date,open,high,low,close,volume")
    ap.add_argument("--out", help="Write JSON snapshot to this path")
    ap.add_argument("--json", action="store_true", help="Print JSON instead of text")
    args = ap.parse_args()

    quote, bars, source = {}, [], "unavailable"

    if args.bars:
        bars = load_csv(args.bars)
        source = f"csv:{os.path.basename(args.bars)}"
    else:
        provider = args.provider
        if provider == "auto":
            for name, (env_name, _fn) in PROVIDERS.items():
                if os.environ.get(env_name):
                    provider = name
                    break
            else:
                provider = "csv"
        if provider in PROVIDERS:
            env_name, fn = PROVIDERS[provider]
            key = os.environ.get(env_name)
            if not key:
                print(f"error: {env_name} is not set. Use --bars <file.csv> instead.", file=sys.stderr)
                return 2
            try:
                quote, bars = fn(args.symbol, key)
                source = f"{provider} api"
            except urllib.error.HTTPError as exc:
                print(f"error: {provider} returned HTTP {exc.code}.", file=sys.stderr)
                return 3
            except Exception as exc:  # network, json, timeout
                print(f"error: {provider} request failed: {exc}", file=sys.stderr)
                return 3
        else:
            print("error: no provider key available and no --bars file given.", file=sys.stderr)
            return 2

    if not bars:
        print("error: no price history available for this symbol.", file=sys.stderr)
        return 4

    snap = build_snapshot(args.symbol, bars, quote, source)
    if args.out:
        with open(args.out, "w", encoding="utf-8") as fh:
            json.dump(snap, fh, indent=2)
        print(f"written: {args.out}")
    print(json.dumps(snap, indent=2) if args.json else render(snap))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

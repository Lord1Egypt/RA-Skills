#!/usr/bin/env python3
"""Fetch Binance USD-M perpetual public data and compute strategy helpers."""

from __future__ import annotations

import argparse
import json
import math
import statistics
import sys
import time
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from typing import Dict, Iterable, List, Optional, Sequence, Tuple

BASE_URL = "https://fapi.binance.com"
USER_AGENT = "binance-futures-strategy-analysis/1.0"


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M")


def round_value(value: Optional[float], digits: int = 6) -> Optional[float]:
    if value is None:
        return None
    return round(float(value), digits)


def http_get_json(path: str, params: Dict[str, object]) -> object:
    query = urllib.parse.urlencode(params)
    url = f"{BASE_URL}{path}?{query}" if query else f"{BASE_URL}{path}"
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=20) as resp:
        return json.loads(resp.read().decode("utf-8"))


def normalize_symbol(raw: str) -> Dict[str, str]:
    token = raw.strip().upper().replace("-", "").replace("_", "").replace("/", "")
    if not token:
        raise ValueError("symbol is empty")
    if token.endswith("USDT"):
        base = token[:-4]
        binance_symbol = token
    else:
        base = token
        binance_symbol = f"{token}USDT"
    return {
        "input": raw,
        "base": base,
        "inst_id": f"{base}-USDT",
        "binance_symbol": binance_symbol,
    }


def ema(values: Sequence[float], period: int) -> List[Optional[float]]:
    if period <= 0:
        raise ValueError("period must be positive")
    out: List[Optional[float]] = [None] * len(values)
    if len(values) < period:
        return out
    seed = sum(values[:period]) / period
    multiplier = 2.0 / (period + 1.0)
    out[period - 1] = seed
    prev = seed
    for idx in range(period, len(values)):
        prev = (values[idx] - prev) * multiplier + prev
        out[idx] = prev
    return out


def rsi(values: Sequence[float], period: int) -> List[Optional[float]]:
    out: List[Optional[float]] = [None] * len(values)
    if len(values) <= period:
        return out
    gains = []
    losses = []
    for idx in range(1, period + 1):
        delta = values[idx] - values[idx - 1]
        gains.append(max(delta, 0.0))
        losses.append(max(-delta, 0.0))
    avg_gain = sum(gains) / period
    avg_loss = sum(losses) / period
    if avg_loss == 0:
        out[period] = 100.0
    else:
        rs = avg_gain / avg_loss
        out[period] = 100.0 - (100.0 / (1.0 + rs))
    for idx in range(period + 1, len(values)):
        delta = values[idx] - values[idx - 1]
        gain = max(delta, 0.0)
        loss = max(-delta, 0.0)
        avg_gain = ((avg_gain * (period - 1)) + gain) / period
        avg_loss = ((avg_loss * (period - 1)) + loss) / period
        if avg_loss == 0:
            out[idx] = 100.0
        else:
            rs = avg_gain / avg_loss
            out[idx] = 100.0 - (100.0 / (1.0 + rs))
    return out


def atr(highs: Sequence[float], lows: Sequence[float], closes: Sequence[float], period: int) -> List[Optional[float]]:
    out: List[Optional[float]] = [None] * len(closes)
    if len(closes) <= period:
        return out
    true_ranges: List[float] = [0.0]
    for idx in range(1, len(closes)):
        tr = max(
            highs[idx] - lows[idx],
            abs(highs[idx] - closes[idx - 1]),
            abs(lows[idx] - closes[idx - 1]),
        )
        true_ranges.append(tr)
    seed = sum(true_ranges[1:period + 1]) / period
    out[period] = seed
    prev = seed
    for idx in range(period + 1, len(closes)):
        prev = ((prev * (period - 1)) + true_ranges[idx]) / period
        out[idx] = prev
    return out


def adx(highs: Sequence[float], lows: Sequence[float], closes: Sequence[float], period: int) -> List[Optional[float]]:
    size = len(closes)
    out: List[Optional[float]] = [None] * size
    if size <= period * 2:
        return out

    trs = [0.0] * size
    plus_dm = [0.0] * size
    minus_dm = [0.0] * size
    for idx in range(1, size):
        up = highs[idx] - highs[idx - 1]
        down = lows[idx - 1] - lows[idx]
        trs[idx] = max(
            highs[idx] - lows[idx],
            abs(highs[idx] - closes[idx - 1]),
            abs(lows[idx] - closes[idx - 1]),
        )
        plus_dm[idx] = up if up > down and up > 0 else 0.0
        minus_dm[idx] = down if down > up and down > 0 else 0.0

    tr14 = sum(trs[1:period + 1])
    plus14 = sum(plus_dm[1:period + 1])
    minus14 = sum(minus_dm[1:period + 1])

    dx_values: List[Optional[float]] = [None] * size
    for idx in range(period, size):
        if idx > period:
            tr14 = tr14 - (tr14 / period) + trs[idx]
            plus14 = plus14 - (plus14 / period) + plus_dm[idx]
            minus14 = minus14 - (minus14 / period) + minus_dm[idx]
        if tr14 == 0:
            continue
        plus_di = 100.0 * (plus14 / tr14)
        minus_di = 100.0 * (minus14 / tr14)
        denom = plus_di + minus_di
        if denom == 0:
            dx_values[idx] = 0.0
        else:
            dx_values[idx] = 100.0 * abs(plus_di - minus_di) / denom

    initial = [value for value in dx_values[period:period * 2] if value is not None]
    if len(initial) < period:
        return out
    adx_value = sum(initial) / period
    out[period * 2 - 1] = adx_value
    for idx in range(period * 2, size):
        if dx_values[idx] is None:
            continue
        adx_value = ((adx_value * (period - 1)) + dx_values[idx]) / period
        out[idx] = adx_value
    return out


def macd_histogram(values: Sequence[float], fast: int = 12, slow: int = 26, signal: int = 9) -> List[Optional[float]]:
    fast_ema = ema(values, fast)
    slow_ema = ema(values, slow)
    macd_line: List[Optional[float]] = [None] * len(values)
    for idx in range(len(values)):
        if fast_ema[idx] is None or slow_ema[idx] is None:
            continue
        macd_line[idx] = fast_ema[idx] - slow_ema[idx]

    compact = [value for value in macd_line if value is not None]
    signal_line_compact = ema(compact, signal)
    signal_line: List[Optional[float]] = [None] * len(values)
    compact_idx = 0
    for idx, value in enumerate(macd_line):
        if value is None:
            continue
        signal_line[idx] = signal_line_compact[compact_idx]
        compact_idx += 1

    histogram: List[Optional[float]] = [None] * len(values)
    for idx in range(len(values)):
        if macd_line[idx] is None or signal_line[idx] is None:
            continue
        histogram[idx] = macd_line[idx] - signal_line[idx]
    return histogram


def take_last(values: Sequence[Optional[float]], limit: int, digits: int = 6) -> List[Optional[float]]:
    tail = list(values[-limit:])
    return [round_value(value, digits) if value is not None else None for value in tail]


def average(values: Sequence[float]) -> float:
    return sum(values) / len(values) if values else 0.0


def stddev(values: Sequence[float]) -> float:
    if len(values) < 2:
        return 0.0
    return statistics.pstdev(values)


def detect_swings(candles: Sequence[Dict[str, float]], window: int = 2) -> Dict[str, List[Dict[str, float]]]:
    highs: List[Dict[str, float]] = []
    lows: List[Dict[str, float]] = []
    if len(candles) < window * 2 + 1:
        return {"highs": highs, "lows": lows}

    for idx in range(window, len(candles) - window):
        segment = candles[idx - window:idx + window + 1]
        center = candles[idx]
        if all(center["high"] > item["high"] for item in segment if item is not center):
            highs.append({"ts": center["ts"], "price": round_value(center["high"], 4)})
        if all(center["low"] < item["low"] for item in segment if item is not center):
            lows.append({"ts": center["ts"], "price": round_value(center["low"], 4)})
    return {"highs": highs[-8:], "lows": lows[-8:]}


def structure_label(swings: Dict[str, List[Dict[str, float]]]) -> str:
    highs = swings["highs"]
    lows = swings["lows"]
    if len(highs) < 2 or len(lows) < 2:
        return "UNKNOWN"
    last_high = highs[-1]["price"]
    prev_high = highs[-2]["price"]
    last_low = lows[-1]["price"]
    prev_low = lows[-2]["price"]
    if last_high > prev_high and last_low > prev_low:
        return "HH-HL"
    if last_high < prev_high and last_low < prev_low:
        return "LH-LL"
    return "RANGE"


def recent_reversal_candles(candles: Sequence[Dict[str, float]], lookback: int = 20) -> List[Dict[str, object]]:
    recent = list(candles[-lookback:])
    if not recent:
        return []
    avg_volume = average([item["volume"] for item in recent])
    out: List[Dict[str, object]] = []

    for idx, candle in enumerate(recent):
        body = abs(candle["close"] - candle["open"])
        full = max(candle["high"] - candle["low"], 1e-9)
        upper = candle["high"] - max(candle["open"], candle["close"])
        lower = min(candle["open"], candle["close"]) - candle["low"]
        volume_ratio = candle["volume"] / avg_volume if avg_volume else 0.0
        labels: List[str] = []

        if candle["close"] > candle["open"] and body / full >= 0.6 and volume_ratio >= 1.5:
            labels.append("bullish_long")
        if candle["close"] < candle["open"] and body / full >= 0.6 and volume_ratio >= 1.5:
            labels.append("bearish_long")
        if lower > body * 2 and upper <= body and volume_ratio >= 1.2:
            labels.append("hammer")
        if upper > body * 2 and lower <= body and volume_ratio >= 1.2:
            labels.append("shooting_star")

        if idx > 0:
            prev = recent[idx - 1]
            prev_high_body = max(prev["open"], prev["close"])
            prev_low_body = min(prev["open"], prev["close"])
            cur_high_body = max(candle["open"], candle["close"])
            cur_low_body = min(candle["open"], candle["close"])
            if prev["close"] < prev["open"] and candle["close"] > candle["open"]:
                if cur_high_body >= prev_high_body and cur_low_body <= prev_low_body:
                    labels.append("bullish_engulfing")
            if prev["close"] > prev["open"] and candle["close"] < candle["open"]:
                if cur_high_body >= prev_high_body and cur_low_body <= prev_low_body:
                    labels.append("bearish_engulfing")

        if labels:
            out.append(
                {
                    "ts": candle["ts"],
                    "labels": labels,
                    "volume_ratio": round_value(volume_ratio, 4),
                }
            )
    return out[-8:]


def volume_anomalies(candles: Sequence[Dict[str, float]], lookback: int = 30) -> List[Dict[str, object]]:
    recent = list(candles[-lookback:])
    volumes = [item["volume"] for item in recent]
    if not volumes:
        return []
    avg_volume = average(volumes)
    deviation = stddev(volumes)
    out = []
    for candle in recent:
        threshold = max(avg_volume * 1.8, avg_volume + deviation * 2.0)
        if candle["volume"] >= threshold:
            direction = "up" if candle["close"] >= candle["open"] else "down"
            out.append(
                {
                    "ts": candle["ts"],
                    "direction": direction,
                    "volume": round_value(candle["volume"], 4),
                    "volume_ratio": round_value(candle["volume"] / avg_volume if avg_volume else 0.0, 4),
                }
            )
    return out[-8:]


def volume_profile(candles: Sequence[Dict[str, float]], bins: int = 24) -> Dict[str, object]:
    if not candles:
        return {}
    low_price = min(item["low"] for item in candles)
    high_price = max(item["high"] for item in candles)
    if math.isclose(low_price, high_price):
        return {
            "range_low": round_value(low_price, 4),
            "range_high": round_value(high_price, 4),
            "poc": round_value(low_price, 4),
            "val": round_value(low_price, 4),
            "vah": round_value(high_price, 4),
            "top_nodes": [{"price": round_value(low_price, 4), "share": 1.0}],
        }

    bin_size = (high_price - low_price) / bins
    hist = [0.0] * bins
    total = 0.0
    for candle in candles:
        price = (candle["high"] + candle["low"] + candle["close"]) / 3.0
        idx = min(int((price - low_price) / bin_size), bins - 1)
        weight = candle["quote_volume"]
        hist[idx] += weight
        total += weight

    poc_idx = max(range(bins), key=lambda idx: hist[idx])
    selected = {poc_idx}
    coverage = hist[poc_idx]
    left = poc_idx - 1
    right = poc_idx + 1
    target = total * 0.7 if total else 0.0
    while coverage < target and (left >= 0 or right < bins):
        left_val = hist[left] if left >= 0 else -1.0
        right_val = hist[right] if right < bins else -1.0
        if left_val >= right_val:
            if left >= 0:
                selected.add(left)
                coverage += hist[left]
                left -= 1
            elif right < bins:
                selected.add(right)
                coverage += hist[right]
                right += 1
        else:
            if right < bins:
                selected.add(right)
                coverage += hist[right]
                right += 1
            elif left >= 0:
                selected.add(left)
                coverage += hist[left]
                left -= 1

    def bin_price(idx: int) -> float:
        return low_price + bin_size * (idx + 0.5)

    top_nodes = sorted(range(bins), key=lambda idx: hist[idx], reverse=True)[:5]
    top = [
        {
            "price": round_value(bin_price(idx), 4),
            "share": round_value(hist[idx] / total if total else 0.0, 4),
        }
        for idx in top_nodes
        if hist[idx] > 0
    ]

    return {
        "range_low": round_value(low_price, 4),
        "range_high": round_value(high_price, 4),
        "poc": round_value(bin_price(poc_idx), 4),
        "val": round_value(bin_price(min(selected)), 4),
        "vah": round_value(bin_price(max(selected)), 4),
        "top_nodes": top,
    }


def consecutive_confirmation(candles: Sequence[Dict[str, float]], level: Optional[float], direction: str) -> int:
    if level is None:
        return 0
    count = 0
    for candle in reversed(candles):
        close = candle["close"]
        if direction == "above" and close > level:
            count += 1
        elif direction == "below" and close < level:
            count += 1
        else:
            break
    return count


def recent_levels(swings: Dict[str, List[Dict[str, float]]]) -> Dict[str, Optional[float]]:
    highs = swings["highs"]
    lows = swings["lows"]
    return {
        "swing_high": highs[-1]["price"] if highs else None,
        "prev_swing_high": highs[-2]["price"] if len(highs) >= 2 else None,
        "swing_low": lows[-1]["price"] if lows else None,
        "prev_swing_low": lows[-2]["price"] if len(lows) >= 2 else None,
    }


def trend_hint(close_price: float, ema21_value: Optional[float], ema50_value: Optional[float], macd_value: Optional[float], rsi_value: Optional[float], adx_value: Optional[float], structure: str) -> str:
    bull_score = 0
    bear_score = 0

    if ema21_value is not None and ema50_value is not None:
        if close_price > ema21_value > ema50_value:
            bull_score += 2
        if close_price < ema21_value < ema50_value:
            bear_score += 2

    if macd_value is not None:
        if macd_value > 0:
            bull_score += 1
        if macd_value < 0:
            bear_score += 1

    if rsi_value is not None:
        if rsi_value >= 55:
            bull_score += 1
        if rsi_value <= 45:
            bear_score += 1

    if adx_value is not None:
        if adx_value >= 22:
            if structure == "HH-HL":
                bull_score += 1
            if structure == "LH-LL":
                bear_score += 1

    if structure == "HH-HL":
        bull_score += 1
    elif structure == "LH-LL":
        bear_score += 1

    if bull_score >= 5 and bull_score > bear_score + 1:
        return "STRONG_UP"
    if bear_score >= 5 and bear_score > bull_score + 1:
        return "STRONG_DOWN"
    if bull_score >= bear_score:
        return "MODERATE_UP"
    return "MODERATE_DOWN"


def nearest_target(levels: Iterable[Optional[float]], price: float, direction: str) -> Optional[float]:
    cleaned = sorted({float(level) for level in levels if level is not None})
    if direction == "up":
        for level in cleaned:
            if level > price:
                return level
    else:
        for level in reversed(cleaned):
            if level < price:
                return level
    return None


def risk_reward(close_price: float, stop: Optional[float], target: Optional[float], side: str) -> Optional[float]:
    if stop is None or target is None:
        return None
    if side == "long":
        risk = close_price - stop
        reward = target - close_price
    else:
        risk = stop - close_price
        reward = close_price - target
    if risk <= 0 or reward <= 0:
        return None
    return reward / risk


def format_candles(candles: Sequence[Dict[str, float]], limit: int) -> Dict[str, List[object]]:
    trimmed = list(candles[-limit:])
    return {
        "ts": [item["ts"] for item in trimmed],
        "open": [round_value(item["open"], 4) for item in trimmed],
        "high": [round_value(item["high"], 4) for item in trimmed],
        "low": [round_value(item["low"], 4) for item in trimmed],
        "close": [round_value(item["close"], 4) for item in trimmed],
        "volume": [round_value(item["volume"], 4) for item in trimmed],
    }


def estimate_market_slippage(levels: Sequence[Sequence[str]], notional: float, side: str) -> Dict[str, Optional[float]]:
    if not levels:
        return {"notional": notional, "filled_qty": None, "vwap": None, "slippage_bps": None}
    best_price = float(levels[0][0])
    target_qty = notional / best_price
    filled_qty = 0.0
    total_cost = 0.0
    for price_str, qty_str in levels:
        price = float(price_str)
        qty = float(qty_str)
        take = min(target_qty - filled_qty, qty)
        if take <= 0:
            break
        filled_qty += take
        total_cost += take * price
        if filled_qty >= target_qty:
            break
    if filled_qty <= 0:
        return {"notional": notional, "filled_qty": None, "vwap": None, "slippage_bps": None}
    vwap = total_cost / filled_qty
    if side == "buy":
        slippage = ((vwap - best_price) / best_price) * 10000.0
    else:
        slippage = ((best_price - vwap) / best_price) * 10000.0
    return {
        "notional": notional,
        "filled_qty": round_value(filled_qty, 6),
        "vwap": round_value(vwap, 6),
        "slippage_bps": round_value(slippage, 4),
    }


def parse_kline_rows(rows: Sequence[Sequence[object]]) -> List[Dict[str, float]]:
    candles = []
    for row in rows:
        open_time = int(row[0])
        close_time = int(row[6])
        candles.append(
            {
                "open_time": open_time,
                "close_time": close_time,
                "ts": datetime.fromtimestamp(open_time / 1000.0, tz=timezone.utc).strftime("%Y-%m-%d %H:%M"),
                "open": float(row[1]),
                "high": float(row[2]),
                "low": float(row[3]),
                "close": float(row[4]),
                "volume": float(row[5]),
                "quote_volume": float(row[7]),
                "trades": int(row[8]),
            }
        )
    return candles


def split_current_candle(candles: Sequence[Dict[str, float]]) -> Tuple[List[Dict[str, float]], Optional[Dict[str, float]]]:
    if not candles:
        return [], None
    now_ms = int(time.time() * 1000)
    last = candles[-1]
    if last["close_time"] > now_ms:
        return list(candles[:-1]), dict(last)
    return list(candles), None


def build_timeframe_snapshot(name: str, rows: Sequence[Sequence[object]], series_limit: int) -> Dict[str, object]:
    candles = parse_kline_rows(rows)
    closed, current = split_current_candle(candles)
    working = closed if closed else candles
    opens = [item["open"] for item in working]
    highs = [item["high"] for item in working]
    lows = [item["low"] for item in working]
    closes = [item["close"] for item in working]
    if not closes:
        raise ValueError(f"no candles for {name}")

    ema9_values = ema(closes, 9)
    ema21_values = ema(closes, 21)
    ema50_values = ema(closes, 50)
    rsi14_values = rsi(closes, 14)
    rsi7_values = rsi(closes, 7)
    atr14_values = atr(highs, lows, closes, 14)
    adx14_values = adx(highs, lows, closes, 14)
    macd_hist_values = macd_histogram(closes)

    swings = detect_swings(working)
    structure = structure_label(swings)
    levels = recent_levels(swings)
    vp = volume_profile(working[-min(len(working), 120):])

    last_close = closes[-1]
    last_atr = atr14_values[-1]
    last_ema21 = ema21_values[-1]
    last_ema50 = ema50_values[-1]
    last_macd = macd_hist_values[-1]
    last_rsi = rsi14_values[-1]
    last_adx = adx14_values[-1]
    hint = trend_hint(last_close, last_ema21, last_ema50, last_macd, last_rsi, last_adx, structure)

    resistance_candidates = [
        levels["swing_high"],
        levels["prev_swing_high"],
        vp.get("vah"),
        vp.get("poc"),
    ] + [node["price"] for node in vp.get("top_nodes", [])]
    support_candidates = [
        levels["swing_low"],
        levels["prev_swing_low"],
        vp.get("val"),
        vp.get("poc"),
    ] + [node["price"] for node in vp.get("top_nodes", [])]

    long_stop = None
    short_stop = None
    if last_atr is not None:
        long_stop = min(
            value for value in [levels["swing_low"], last_close - (1.5 * last_atr)] if value is not None
        )
        short_stop = max(
            value for value in [levels["swing_high"], last_close + (1.5 * last_atr)] if value is not None
        )

    long_target = nearest_target(resistance_candidates, last_close, "up")
    short_target = nearest_target(support_candidates, last_close, "down")
    rr_long = risk_reward(last_close, long_stop, long_target, "long")
    rr_short = risk_reward(last_close, short_stop, short_target, "short")

    breakout_above = consecutive_confirmation(working[-5:], levels["swing_high"], "above")
    breakout_below = consecutive_confirmation(working[-5:], levels["swing_low"], "below")
    pullback_hold_long = bool(
        levels["swing_high"] is not None
        and len(working) >= 2
        and working[-1]["low"] >= levels["swing_high"] * 0.995
        and last_ema21 is not None
        and working[-1]["close"] >= last_ema21
    )
    pullback_hold_short = bool(
        levels["swing_low"] is not None
        and len(working) >= 2
        and working[-1]["high"] <= levels["swing_low"] * 1.005
        and last_ema21 is not None
        and working[-1]["close"] <= last_ema21
    )

    return {
        "interval": name,
        "closed_bars": len(working),
        "current_candle": None
        if current is None
        else {
            "ts": current["ts"],
            "open": round_value(current["open"], 4),
            "high": round_value(current["high"], 4),
            "low": round_value(current["low"], 4),
            "close": round_value(current["close"], 4),
            "volume": round_value(current["volume"], 4),
        },
        "closed_series": format_candles(working, series_limit),
        "indicators": {
            "ema9": take_last(ema9_values, min(series_limit, len(ema9_values)), 4),
            "ema21": take_last(ema21_values, min(series_limit, len(ema21_values)), 4),
            "ema50": take_last(ema50_values, min(series_limit, len(ema50_values)), 4),
            "rsi14": take_last(rsi14_values, min(series_limit, len(rsi14_values)), 4),
            "rsi7": take_last(rsi7_values, min(series_limit, len(rsi7_values)), 4),
            "atr14": take_last(atr14_values, min(series_limit, len(atr14_values)), 4),
            "adx14": take_last(adx14_values, min(series_limit, len(adx14_values)), 4),
            "macd_histogram": take_last(macd_hist_values, min(series_limit, len(macd_hist_values)), 6),
            "latest": {
                "close": round_value(last_close, 4),
                "ema9": round_value(ema9_values[-1], 4),
                "ema21": round_value(last_ema21, 4),
                "ema50": round_value(last_ema50, 4),
                "rsi14": round_value(last_rsi, 4),
                "rsi7": round_value(rsi7_values[-1], 4),
                "atr14": round_value(last_atr, 4),
                "adx14": round_value(last_adx, 4),
                "macd_histogram": round_value(last_macd, 6),
            },
        },
        "structure": {
            "label": structure,
            "trend_hint": hint,
            "swings": swings,
            "recent_levels": {key: round_value(value, 4) if value is not None else None for key, value in levels.items()},
            "breakout_confirmation": {
                "bars_above_last_swing_high": breakout_above,
                "bars_below_last_swing_low": breakout_below,
                "pullback_hold_long": pullback_hold_long,
                "pullback_hold_short": pullback_hold_short,
            },
        },
        "reversal_candles": recent_reversal_candles(working),
        "volume_anomalies": volume_anomalies(working),
        "volume_profile": vp,
        "trade_levels": {
            "long_stop": round_value(long_stop, 4) if long_stop is not None else None,
            "long_target": round_value(long_target, 4) if long_target is not None else None,
            "long_rr": round_value(rr_long, 4) if rr_long is not None else None,
            "short_stop": round_value(short_stop, 4) if short_stop is not None else None,
            "short_target": round_value(short_target, 4) if short_target is not None else None,
            "short_rr": round_value(rr_short, 4) if rr_short is not None else None,
        },
    }


def fetch_symbol_snapshot(symbol: str, series_limit: int) -> Dict[str, object]:
    symbol_info = normalize_symbol(symbol)
    market_symbol = symbol_info["binance_symbol"]
    ticker = http_get_json("/fapi/v1/ticker/price", {"symbol": market_symbol})
    premium = http_get_json("/fapi/v1/premiumIndex", {"symbol": market_symbol})
    open_interest = http_get_json("/fapi/v1/openInterest", {"symbol": market_symbol})
    depth = http_get_json("/fapi/v1/depth", {"symbol": market_symbol, "limit": 50})

    klines_5m = http_get_json("/fapi/v1/klines", {"symbol": market_symbol, "interval": "5m", "limit": 160})
    klines_15m = http_get_json("/fapi/v1/klines", {"symbol": market_symbol, "interval": "15m", "limit": 220})
    klines_2h = http_get_json("/fapi/v1/klines", {"symbol": market_symbol, "interval": "2h", "limit": 120})

    bids = depth.get("bids", [])
    asks = depth.get("asks", [])
    best_bid = float(bids[0][0]) if bids else None
    best_ask = float(asks[0][0]) if asks else None
    mid = None
    spread_bps = None
    if best_bid is not None and best_ask is not None:
        mid = (best_bid + best_ask) / 2.0
        spread_bps = ((best_ask - best_bid) / mid) * 10000.0 if mid else None

    return {
        "symbol_code": symbol_info["base"],
        "inst_id": symbol_info["inst_id"],
        "binance_symbol": market_symbol,
        "price": {
            "last_price": round_value(float(ticker["price"]), 6),
            "mark_price": round_value(float(premium["markPrice"]), 6),
            "index_price": round_value(float(premium["indexPrice"]), 6),
        },
        "funding": {
            "last_funding_rate": round_value(float(premium["lastFundingRate"]), 8),
            "next_funding_time_ms": int(premium["nextFundingTime"]),
            "next_funding_time_iso": datetime.fromtimestamp(int(premium["nextFundingTime"]) / 1000.0, tz=timezone.utc).strftime("%Y-%m-%d %H:%M"),
        },
        "open_interest": {
            "open_interest": round_value(float(open_interest["openInterest"]), 6),
            "timestamp_ms": int(open_interest["time"]),
            "timestamp_iso": datetime.fromtimestamp(int(open_interest["time"]) / 1000.0, tz=timezone.utc).strftime("%Y-%m-%d %H:%M"),
        },
        "depth": {
            "best_bid": round_value(best_bid, 6) if best_bid is not None else None,
            "best_ask": round_value(best_ask, 6) if best_ask is not None else None,
            "mid_price": round_value(mid, 6) if mid is not None else None,
            "spread_bps": round_value(spread_bps, 4) if spread_bps is not None else None,
            "buy_slippage": [
                estimate_market_slippage(asks, 1000.0, "buy"),
                estimate_market_slippage(asks, 5000.0, "buy"),
            ],
            "sell_slippage": [
                estimate_market_slippage(bids, 1000.0, "sell"),
                estimate_market_slippage(bids, 5000.0, "sell"),
            ],
        },
        "timeframes": {
            "5m": build_timeframe_snapshot("5m", klines_5m, min(series_limit, 48)),
            "15m": build_timeframe_snapshot("15m", klines_15m, min(series_limit, 72)),
            "2h": build_timeframe_snapshot("2h", klines_2h, min(series_limit, 40)),
        },
    }


def parse_args(argv: Sequence[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Fetch Binance futures public data and compute strategy helpers.")
    parser.add_argument("symbols", nargs="+", help="Base symbols or Binance USDT perpetual symbols, for example BTC ETH BTCUSDT")
    parser.add_argument("--series-limit", type=int, default=48, help="Maximum number of closed bars to keep in each output series")
    parser.add_argument("--indent", type=int, default=2, help="JSON indentation")
    return parser.parse_args(argv)


def main(argv: Sequence[str]) -> int:
    args = parse_args(argv)
    try:
        payload = {
            "generated_at": utc_now_iso(),
            "source": "binance-usdt-perpetual-public",
            "symbols": [fetch_symbol_snapshot(symbol, max(12, args.series_limit)) for symbol in args.symbols],
        }
    except Exception as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False, indent=2), file=sys.stderr)
        return 1

    print(json.dumps(payload, ensure_ascii=False, indent=args.indent))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))

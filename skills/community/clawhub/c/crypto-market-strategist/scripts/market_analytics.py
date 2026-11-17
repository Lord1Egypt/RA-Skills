"""Deterministic volatility and price-structure analytics for BTC and ETH."""
from __future__ import annotations

import math
from statistics import mean, pstdev


def _annualize(variance: float, periods: float = 365.0) -> float:
    return math.sqrt(max(variance, 0) * periods) * 100


def _sample_variance(values: list[float]) -> float | None:
    if len(values) < 2:
        return None
    average = mean(values)
    return sum((value - average) ** 2 for value in values) / (len(values) - 1)


def _realized_estimators(rows: list[dict], window: int) -> dict | None:
    sample = rows[-window:]
    if len(sample) < max(3, window // 2):
        return None
    close_returns = [math.log(sample[index]["close"] / sample[index - 1]["close"]) for index in range(1, len(sample))]
    close_variance = _sample_variance(close_returns)
    if close_variance is None:
        return None
    parkinson = mean(math.log(row["high"] / row["low"]) ** 2 for row in sample) / (4 * math.log(2))
    garman_klass = mean(
        .5 * math.log(row["high"] / row["low"]) ** 2
        - (2 * math.log(2) - 1) * math.log(row["close"] / row["open"]) ** 2
        for row in sample
    )
    overnight = [math.log(sample[index]["open"] / sample[index - 1]["close"]) for index in range(1, len(sample))]
    open_close = [math.log(row["close"] / row["open"]) for row in sample[1:]]
    rogers_satchell = [
        math.log(row["high"] / row["open"]) * math.log(row["high"] / row["close"])
        + math.log(row["low"] / row["open"]) * math.log(row["low"] / row["close"])
        for row in sample[1:]
    ]
    overnight_variance = _sample_variance(overnight) or 0
    open_close_variance = _sample_variance(open_close) or 0
    n = len(sample) - 1
    k = .34 / (1.34 + (n + 1) / max(n - 1, 1))
    yang_zhang = overnight_variance + k * open_close_variance + (1 - k) * mean(rogers_satchell)
    return {
        "window_days": window,
        "observations": len(sample),
        "close_to_close_pct": round(_annualize(close_variance), 3),
        "parkinson_pct": round(_annualize(parkinson), 3),
        "garman_klass_pct": round(_annualize(garman_klass), 3),
        "yang_zhang_pct": round(_annualize(yang_zhang), 3),
    }


def realized_volatility_dossier(daily_rows: list[dict]) -> dict:
    """Return several horizon-aligned OHLC realized-volatility estimators."""
    windows = [row for days in (7, 14, 30, 60, 90) if (row := _realized_estimators(daily_rows, days))]
    rolling = []
    for end in range(30, len(daily_rows) + 1):
        estimate = _realized_estimators(daily_rows[:end], 30)
        if estimate:
            rolling.append(estimate["yang_zhang_pct"])
    current = rolling[-1] if rolling else None
    percentile = None
    if current is not None and rolling:
        percentile = 100 * sum(value <= current for value in rolling) / len(rolling)
    return {
        "status": "ok" if windows else "insufficient_history",
        "estimators": windows,
        "current_30d_yang_zhang_percentile": round(percentile, 2) if percentile is not None else None,
        "volatility_of_volatility_30d_pct": round(pstdev(rolling[-60:]), 3) if len(rolling) >= 2 else None,
        "method": "Annualized daily OHLC estimators; percentile uses available rolling 30-day Yang-Zhang history.",
    }


def _true_ranges(rows: list[dict]) -> list[float]:
    result = []
    for index, row in enumerate(rows):
        previous = rows[index - 1]["close"] if index else row["open"]
        result.append(max(row["high"] - row["low"], abs(row["high"] - previous), abs(row["low"] - previous)))
    return result


def _pivot_levels(rows: list[dict], radius: int = 2) -> list[dict]:
    pivots = []
    for index in range(radius, len(rows) - radius):
        nearby = rows[index - radius:index + radius + 1]
        if rows[index]["low"] == min(row["low"] for row in nearby):
            pivots.append({"price": rows[index]["low"], "kind": "support", "index": index, "volume": rows[index]["volume"]})
        if rows[index]["high"] == max(row["high"] for row in nearby):
            pivots.append({"price": rows[index]["high"], "kind": "resistance", "index": index, "volume": rows[index]["volume"]})
    return pivots


def _cluster_pivots(pivots: list[dict], current: float, tolerance: float) -> list[dict]:
    clusters: list[list[dict]] = []
    for pivot in sorted(pivots, key=lambda row: row["price"]):
        if not clusters or abs(pivot["price"] / mean(row["price"] for row in clusters[-1]) - 1) > tolerance:
            clusters.append([pivot])
        else:
            clusters[-1].append(pivot)
    result = []
    max_volume = max((pivot["volume"] for pivot in pivots), default=1) or 1
    for cluster in clusters:
        price = sum(row["price"] * (1 + row["volume"] / max_volume) for row in cluster) / sum(1 + row["volume"] / max_volume for row in cluster)
        touches = len(cluster)
        recency = max(row["index"] for row in cluster) / max(1, max(row["index"] for row in pivots))
        result.append({
            "price": round(price, 2),
            "side": "support" if price < current else "resistance",
            "distance_pct": round((price / current - 1) * 100, 3),
            "touches": touches,
            "strength_score": round(min(100, 25 + touches * 12 + recency * 20), 1),
        })
    return result


def price_level_dossier(daily_rows: list[dict], four_hour_rows: list[dict]) -> dict:
    """Identify range boundaries and clustered multi-touch support/resistance."""
    if len(daily_rows) < 21 or len(four_hour_rows) < 30:
        return {"status": "insufficient_history", "levels": []}
    current = four_hour_rows[-1]["close"]
    daily_atr = mean(_true_ranges(daily_rows)[-14:])
    four_hour_atr = mean(_true_ranges(four_hour_rows)[-14:])
    pivots = _pivot_levels(daily_rows[-120:], 2) + _pivot_levels(four_hour_rows[-180:], 3)
    tolerance = max(.004, min(.02, .5 * daily_atr / current))
    levels = _cluster_pivots(pivots, current, tolerance)
    support = sorted((row for row in levels if row["price"] < current), key=lambda row: (-row["price"], -row["strength_score"]))[:4]
    resistance = sorted((row for row in levels if row["price"] > current), key=lambda row: (row["price"], -row["strength_score"]))[:4]
    prior_daily = daily_rows[-21:-1]
    prior_four_hour = four_hour_rows[-121:-1]
    upper = max(row["high"] for row in prior_daily)
    lower = min(row["low"] for row in prior_daily)
    latest_volume = four_hour_rows[-1]["volume"]
    average_volume = mean(row["volume"] for row in four_hour_rows[-21:-1])
    if current > upper:
        state = "upside_breakout_confirming" if latest_volume >= average_volume else "upside_break_without_volume_confirmation"
    elif current < lower:
        state = "downside_breakout_confirming" if latest_volume >= average_volume else "downside_break_without_volume_confirmation"
    else:
        state = "inside_range"
    return {
        "status": "ok",
        "current_price": current,
        "atr_14d": round(daily_atr, 2),
        "atr_14d_pct": round(daily_atr / current * 100, 3),
        "atr_14x4h": round(four_hour_atr, 2),
        "range_20d": {"low": round(lower, 2), "high": round(upper, 2), "position_pct": round((current - lower) / max(upper - lower, 1e-12) * 100, 2)},
        "donchian_20d": {"lower": round(lower, 2), "upper": round(upper, 2)},
        "range_20x4h": {"low": round(min(row["low"] for row in prior_four_hour[-20:]), 2), "high": round(max(row["high"] for row in prior_four_hour[-20:]), 2)},
        "breakout_state": state,
        "volume_confirmation_ratio": round(latest_volume / average_volume, 3) if average_volume else None,
        "nearest_support": support,
        "nearest_resistance": resistance,
        "method": "ATR-scaled clustering of confirmed daily and four-hour swing pivots plus prior-period Donchian ranges.",
    }

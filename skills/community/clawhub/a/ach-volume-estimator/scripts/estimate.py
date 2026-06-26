#!/usr/bin/env python3
"""
ACH Volume Forecaster v3.1

Sophisticated forecasting with:
- Seasonal decomposition (monthly indices from historical data)
- Linear trend extraction (growth trajectory)
- Weighted recency bias (recent months matter more)
- Confidence intervals (80% band)
- Business day normalization using Fed holiday calendar
- Current month run-rate blending with seasonal/trend forecast
- Payroll spillover detection and BD1 adjustment

The more historical data in MONTHLY_ACTUALS, the better the forecasts.
Add new months as they close.

Usage:
    estimate.py --transactions N --bds-elapsed N [--month YYYY-MM] [--json]
    estimate.py --per-bd N [--month YYYY-MM] [--json]
    estimate.py --forecast-only [--month YYYY-MM] [--json]   # no live data, pure model
"""

import argparse
import json
import math
import sys
from datetime import date, timedelta
from collections import defaultdict

# ---------------------------------------------------------------------------
# US Federal Reserve bank holidays (observed dates 2023-2027)
# Source: https://www.federalreserve.gov/aboutthefed/k8.htm
# ---------------------------------------------------------------------------
FED_HOLIDAYS = {
    # 2023
    date(2023, 1, 2),   # New Year's (observed)
    date(2023, 1, 16),  # MLK Jr Day
    date(2023, 2, 20),  # Presidents' Day
    date(2023, 5, 29),  # Memorial Day
    date(2023, 6, 19),  # Juneteenth
    date(2023, 7, 4),   # Independence Day
    date(2023, 9, 4),   # Labor Day
    date(2023, 10, 9),  # Columbus Day
    date(2023, 11, 10), # Veterans Day (observed)
    date(2023, 11, 23), # Thanksgiving
    date(2023, 12, 25), # Christmas

    # 2024
    date(2024, 1, 1),   # New Year's Day
    date(2024, 1, 15),  # MLK Jr Day
    date(2024, 2, 19),  # Presidents' Day
    date(2024, 5, 27),  # Memorial Day
    date(2024, 6, 19),  # Juneteenth
    date(2024, 7, 4),   # Independence Day
    date(2024, 9, 2),   # Labor Day
    date(2024, 10, 14), # Columbus Day
    date(2024, 11, 11), # Veterans Day
    date(2024, 11, 28), # Thanksgiving
    date(2024, 12, 25), # Christmas

    # 2025
    date(2025, 1, 1),   # New Year's Day
    date(2025, 1, 20),  # MLK Jr Day
    date(2025, 2, 17),  # Presidents' Day
    date(2025, 5, 26),  # Memorial Day
    date(2025, 6, 19),  # Juneteenth
    date(2025, 7, 4),   # Independence Day
    date(2025, 9, 1),   # Labor Day
    date(2025, 10, 13), # Columbus Day
    date(2025, 11, 11), # Veterans Day
    date(2025, 11, 27), # Thanksgiving
    date(2025, 12, 25), # Christmas

    # 2026
    date(2026, 1, 1),   # New Year's Day
    date(2026, 1, 19),  # MLK Jr Day
    date(2026, 2, 16),  # Presidents' Day
    date(2026, 5, 25),  # Memorial Day
    date(2026, 6, 19),  # Juneteenth
    date(2026, 7, 3),   # Independence Day (observed)
    date(2026, 9, 7),   # Labor Day
    date(2026, 10, 12), # Columbus Day
    date(2026, 11, 11), # Veterans Day
    date(2026, 11, 26), # Thanksgiving
    date(2026, 12, 25), # Christmas

    # 2027
    date(2027, 1, 1),   # New Year's Day
    date(2027, 1, 18),  # MLK Jr Day
    date(2027, 2, 15),  # Presidents' Day
    date(2027, 5, 31),  # Memorial Day
    date(2027, 6, 18),  # Juneteenth (observed)
    date(2027, 7, 5),   # Independence Day (observed)
    date(2027, 9, 6),   # Labor Day
    date(2027, 10, 11), # Columbus Day
    date(2027, 11, 11), # Veterans Day
    date(2027, 11, 25), # Thanksgiving
    date(2027, 12, 24), # Christmas (observed)
}

# ---------------------------------------------------------------------------
# Historical monthly actuals (transactions)
# Source: ACH KPI emails. Add new months as they close.
# The more data here, the better the seasonal model.
# ---------------------------------------------------------------------------
MONTHLY_ACTUALS = {
    # 2025 actuals (Jan-Feb estimated; Mar-Dec confirmed from Tableau ACH KPIs charts)
    "2025-01": 5_633_673,    # confirmed from Tableau MoM/YoY 2026-03-19
    "2025-02": 5_220_612,    # confirmed from Tableau MoM/YoY 2026-03-19
    "2025-03": 5_700_654,    # confirmed from Tableau 2026-03-04
    "2025-04": 5_820_172,    # confirmed from Tableau 2026-03-04
    "2025-05": 5_779_929,    # confirmed from Tableau 2026-03-04
    "2025-06": 5_638_789,    # confirmed from Tableau 2026-03-04
    "2025-07": 5_482_190,    # confirmed from Tableau 2026-03-04
    "2025-08": 5_352_917,    # confirmed from Tableau 2026-03-04
    "2025-09": 5_858_619,    # confirmed from Tableau 2026-03-04
    "2025-10": 5_958_010,    # confirmed from Tableau 2026-03-04
    "2025-11": 5_283_677,    # confirmed from Tableau 2026-03-04
    "2025-12": 6_406_067,    # confirmed from Tableau 2026-03-04
    # 2026 actuals
    "2026-01": 6_121_127,    # confirmed from Tableau 2026-03-04
    "2026-02": 5_681_773,    # confirmed from Tableau 2026-03-04 (month closed)
}


# ---------------------------------------------------------------------------
# Calendar utilities
# ---------------------------------------------------------------------------

def business_days_in_month(year: int, month: int) -> int:
    """Count business days (weekdays minus Fed holidays) in a month."""
    first = date(year, month, 1)
    if month == 12:
        last = date(year + 1, 1, 1) - timedelta(days=1)
    else:
        last = date(year, month + 1, 1) - timedelta(days=1)
    count = 0
    d = first
    while d <= last:
        if d.weekday() < 5 and d not in FED_HOLIDAYS:
            count += 1
        d += timedelta(days=1)
    return count


def months_in_quarter(year: int, month: int):
    q_start = ((month - 1) // 3) * 3 + 1
    return [(year, q_start + i) for i in range(3)]


def months_in_year(year: int):
    return [(year, m) for m in range(1, 13)]


def detect_spillover(year: int, month: int) -> dict:
    """
    Check if payroll transactions from the prior month likely spilled into
    this month's first business day.

    Spillover occurs when the last 1-2 calendar days of the prior month were
    non-business days (weekends or Fed holidays), causing payroll that would
    have processed on those days to roll to this month's BD1.

    Returns dict with:
      detected (bool): True if spillover risk exists
      reason (str): Human-readable explanation
      non_business_days (int): Count of trailing non-BDs in prior month
    """
    # Prior month
    if month == 1:
        prior_year, prior_month = year - 1, 12
    else:
        prior_year, prior_month = year, month - 1

    # Last calendar day of prior month
    if prior_month == 12:
        last_day = date(prior_year + 1, 1, 1) - timedelta(days=1)
    else:
        last_day = date(prior_year, prior_month + 1, 1) - timedelta(days=1)

    # Count trailing non-business days (check last 2 calendar days)
    day_names = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    trailing = []
    for offset in range(2):
        d = last_day - timedelta(days=offset)
        if d.weekday() >= 5 or d in FED_HOLIDAYS:
            trailing.append(f"{d} ({day_names[d.weekday()]})")
        else:
            break  # stop at first business day going backward

    if trailing:
        reason = (
            f"Prior month ({prior_year}-{prior_month:02d}) ended on non-business "
            f"day(s): {', '.join(trailing)}. Payroll likely spilled into BD1."
        )
        return {"detected": True, "reason": reason, "non_business_days": len(trailing)}

    return {
        "detected": False,
        "reason": f"No spillover: {prior_year}-{prior_month:02d} ended on a business day.",
        "non_business_days": 0,
    }


# ---------------------------------------------------------------------------
# Forecasting engine
# ---------------------------------------------------------------------------

def get_sorted_actuals():
    """Return actuals sorted chronologically as list of (key, year, month, value)."""
    items = []
    for key, val in MONTHLY_ACTUALS.items():
        y, m = int(key[:4]), int(key[5:7])
        items.append((key, y, m, val))
    items.sort(key=lambda x: (x[1], x[2]))
    return items


def compute_per_bd_series():
    """Normalize actuals to per-BD rates for apples-to-apples comparison."""
    series = {}
    for key, val in MONTHLY_ACTUALS.items():
        y, m = int(key[:4]), int(key[5:7])
        bds = business_days_in_month(y, m)
        series[key] = val / bds if bds > 0 else 0
    return series


def compute_seasonal_indices():
    """
    Calculate monthly seasonal indices from per-BD normalized data.
    Index > 1.0 means that month runs hotter than average.
    Uses ratio-to-moving-average when enough data, otherwise ratio-to-mean.
    """
    per_bd = compute_per_bd_series()
    if len(per_bd) < 6:
        return {m: 1.0 for m in range(1, 13)}

    # Group by calendar month
    by_month = defaultdict(list)
    for key, rate in per_bd.items():
        m = int(key[5:7])
        by_month[m].append(rate)

    # Overall mean per-BD rate
    all_rates = list(per_bd.values())
    overall_mean = sum(all_rates) / len(all_rates)

    if overall_mean == 0:
        return {m: 1.0 for m in range(1, 13)}

    # Seasonal index = avg per-BD for that month / overall avg per-BD
    indices = {}
    for m in range(1, 13):
        if by_month[m]:
            # Weight recent years more heavily (exponential decay)
            vals = by_month[m]
            if len(vals) == 1:
                month_avg = vals[0]
            else:
                # Most recent observation gets weight 1.0, prior gets 0.6, etc.
                weights = [0.6 ** i for i in range(len(vals) - 1, -1, -1)]
                month_avg = sum(v * w for v, w in zip(vals, weights)) / sum(weights)
            indices[m] = month_avg / overall_mean
        else:
            indices[m] = 1.0

    # Normalize indices so they average to 1.0
    avg_idx = sum(indices.values()) / 12
    if avg_idx > 0:
        indices = {m: v / avg_idx for m, v in indices.items()}

    return indices


def compute_trend():
    """
    Extract linear trend from per-BD series using weighted least squares.
    Recent months weighted more heavily.
    Returns (slope_per_month, intercept) in per-BD rate space.
    """
    per_bd = compute_per_bd_series()
    items = get_sorted_actuals()

    if len(items) < 3:
        return 0.0, sum(per_bd.values()) / max(len(per_bd), 1)

    # Assign sequential index (0, 1, 2, ...)
    n = len(items)
    xs = list(range(n))
    ys = [per_bd[item[0]] for item in items]

    # Exponential weights: most recent = 1.0, decaying backward
    decay = 0.85
    weights = [decay ** (n - 1 - i) for i in range(n)]

    # Weighted linear regression
    sw = sum(weights)
    sx = sum(w * x for w, x in zip(weights, xs))
    sy = sum(w * y for w, y in zip(weights, ys))
    sxx = sum(w * x * x for w, x in zip(weights, xs))
    sxy = sum(w * x * y for w, x, y in zip(weights, xs, ys))

    denom = sw * sxx - sx * sx
    if abs(denom) < 1e-10:
        return 0.0, sy / sw

    slope = (sw * sxy - sx * sy) / denom
    intercept = (sy - slope * sx) / sw

    return slope, intercept


def compute_forecast_error():
    """
    Calculate historical forecast error (MAPE) for confidence intervals.
    Uses leave-one-out on the last 6 months.
    """
    items = get_sorted_actuals()
    if len(items) < 8:
        return 0.05  # default 5% error if not enough data

    per_bd = compute_per_bd_series()
    errors = []

    # Test on last 6 months
    for i in range(max(len(items) - 6, 3), len(items)):
        # Build model from data before month i
        subset_keys = [items[j][0] for j in range(i)]
        subset_vals = [per_bd[k] for k in subset_keys]
        if len(subset_vals) < 3:
            continue

        # Simple trend extrapolation
        n = len(subset_vals)
        weights = [0.85 ** (n - 1 - j) for j in range(n)]
        sw = sum(weights)
        xs = list(range(n))
        sx = sum(w * x for w, x in zip(weights, xs))
        sy = sum(w * y for w, y in zip(weights, subset_vals))
        sxx = sum(w * x * x for w, x in zip(weights, xs))
        sxy = sum(w * x * y for w, x, y in zip(weights, xs, subset_vals))
        denom = sw * sxx - sx * sx
        if abs(denom) < 1e-10:
            predicted = sy / sw
        else:
            sl = (sw * sxy - sx * sy) / denom
            intc = (sy - sl * sx) / sw
            predicted = intc + sl * n  # extrapolate one step

        actual = per_bd[items[i][0]]
        if actual > 0:
            errors.append(abs(predicted - actual) / actual)

    if not errors:
        return 0.05
    return sum(errors) / len(errors)


def forecast_month_model(year: int, month: int) -> dict:
    """
    Forecast a future month using trend + seasonality.
    Returns per-BD rate forecast and confidence band.
    """
    items = get_sorted_actuals()
    if not items:
        return {"per_bd": 0, "confidence_low": 0, "confidence_high": 0, "method": "no_data"}

    seasonal = compute_seasonal_indices()
    slope, intercept = compute_trend()
    mape = compute_forecast_error()

    # How many months ahead from the last actual?
    last_y, last_m = items[-1][1], items[-1][2]
    last_idx = len(items) - 1
    months_ahead = (year - last_y) * 12 + (month - last_m)
    forecast_idx = last_idx + months_ahead

    # Base forecast: trend line
    trend_per_bd = intercept + slope * forecast_idx

    # Apply seasonal index
    seasonal_per_bd = trend_per_bd * seasonal.get(month, 1.0)

    # Confidence widens with distance
    distance_factor = 1.0 + 0.15 * max(0, months_ahead - 1)
    error_margin = mape * distance_factor * 1.28  # 80% CI ~ 1.28 * std

    bds = business_days_in_month(year, month)
    est = round(seasonal_per_bd * bds)
    low = round(seasonal_per_bd * (1 - error_margin) * bds)
    high = round(seasonal_per_bd * (1 + error_margin) * bds)

    return {
        "per_bd": round(seasonal_per_bd),
        "estimated_total": est,
        "confidence_low": low,
        "confidence_high": high,
        "seasonal_index": round(seasonal.get(month, 1.0), 3),
        "trend_per_bd": round(trend_per_bd),
        "method": "trend_seasonal",
    }


# ---------------------------------------------------------------------------
# Month estimation (combines live data with model)
# ---------------------------------------------------------------------------

def estimate_month(year: int, month: int, current_per_bd: float = None,
                   current_txns: int = None, current_bds_elapsed: int = None) -> dict:
    """Estimate a single month's volume."""
    key = f"{year}-{month:02d}"
    total_bds = business_days_in_month(year, month)

    # If we have actuals, use them
    if key in MONTHLY_ACTUALS:
        actual = MONTHLY_ACTUALS[key]
        return {
            "month": key,
            "total_business_days": total_bds,
            "estimated_total": actual,
            "estimated_total_M": round(actual / 1_000_000, 2),
            "method": "actual",
            "per_bd": round(actual / total_bds) if total_bds > 0 else 0,
        }

    # Current month with live data: blend run-rate with model
    today = date.today()
    if year == today.year and month == today.month and current_per_bd:
        model = forecast_month_model(year, month)

        # Blending: as more BDs elapse, trust run-rate more, model less
        # At 0 BDs elapsed, 100% model. At all BDs elapsed, 100% run-rate.
        if current_bds_elapsed and total_bds > 0:
            run_rate_weight = current_bds_elapsed / total_bds
        else:
            run_rate_weight = 0.5

        model_weight = 1.0 - run_rate_weight

        blended_per_bd = (current_per_bd * run_rate_weight +
                          model.get("per_bd", current_per_bd) * model_weight)

        est = round(blended_per_bd * total_bds)

        # Run-rate only estimate for comparison
        run_rate_est = round(current_per_bd * total_bds)

        return {
            "month": key,
            "total_business_days": total_bds,
            "bds_elapsed": current_bds_elapsed,
            "bds_remaining": total_bds - (current_bds_elapsed or 0),
            "transactions_so_far": current_txns,
            "estimated_total": est,
            "estimated_total_M": round(est / 1_000_000, 2),
            "run_rate_estimate_M": round(run_rate_est / 1_000_000, 2),
            "model_estimate_M": round(model.get("estimated_total", 0) / 1_000_000, 2),
            "blend_weights": {
                "run_rate": round(run_rate_weight, 2),
                "model": round(model_weight, 2),
            },
            "per_bd": round(blended_per_bd),
            "run_rate_per_bd": round(current_per_bd),
            "seasonal_index": model.get("seasonal_index"),
            "confidence_low_M": round(model.get("confidence_low", 0) / 1_000_000, 2),
            "confidence_high_M": round(model.get("confidence_high", 0) / 1_000_000, 2),
            "method": f"blended_{int(run_rate_weight*100)}pct_runrate",
        }

    # Future month: pure model forecast
    model = forecast_month_model(year, month)
    return {
        "month": key,
        "total_business_days": total_bds,
        "estimated_total": model["estimated_total"],
        "estimated_total_M": round(model["estimated_total"] / 1_000_000, 2),
        "per_bd": model["per_bd"],
        "seasonal_index": model.get("seasonal_index"),
        "confidence_low_M": round(model.get("confidence_low", 0) / 1_000_000, 2),
        "confidence_high_M": round(model.get("confidence_high", 0) / 1_000_000, 2),
        "method": model["method"],
    }


# ---------------------------------------------------------------------------
# Full forecast
# ---------------------------------------------------------------------------

def forecast(transactions: int = None, bds_elapsed: int = None,
             per_bd: float = None, month_str: str = None,
             forecast_only: bool = False) -> dict:
    """Full forecast: current month, quarter, year, with model diagnostics."""
    today = date.today()
    if month_str:
        parts = month_str.split("-")
        year, month = int(parts[0]), int(parts[1])
    else:
        year, month = today.year, today.month

    # Detect payroll spillover from prior month
    spillover = {"detected": False, "reason": "", "non_business_days": 0}
    if transactions is not None and bds_elapsed is not None:
        spillover = detect_spillover(year, month)

    # Calculate per-BD rate with optional spillover adjustment
    txn_per_bd = None
    effective_bds = bds_elapsed
    if per_bd is not None:
        txn_per_bd = per_bd
    elif transactions is not None and bds_elapsed is not None and bds_elapsed > 0:
        if spillover["detected"] and bds_elapsed < 5:
            # BD1 is inflated by prior-month spillover. Adjust by treating it as
            # ~1.5 effective BDs. The extra weight fades as more BDs elapse.
            # At bds_elapsed=1: +0.50, 2: +0.35, 3: +0.20, 4: +0.05, 5+: 0
            extra = max(0.0, 0.5 - (bds_elapsed - 1) * 0.15)
            effective_bds = bds_elapsed + extra
        txn_per_bd = transactions / effective_bds

    if not forecast_only and txn_per_bd is None:
        return {"error": "Provide --transactions + --bds-elapsed, or --per-bd, or --forecast-only"}

    # Current month
    current_month = estimate_month(year, month, txn_per_bd, transactions, bds_elapsed)

    # Annotate current_month with spillover info
    if spillover["detected"] and bds_elapsed is not None:
        current_month["spillover_detected"] = True
        current_month["spillover_note"] = spillover["reason"]
        if effective_bds != bds_elapsed:
            current_month["spillover_effective_bds"] = round(effective_bds, 2)
    else:
        current_month["spillover_detected"] = False

    # Quarter
    q_months = months_in_quarter(year, month)
    q_estimates = []
    q_total = 0
    q_low = 0
    q_high = 0
    for y, m in q_months:
        est = estimate_month(y, m, txn_per_bd, transactions, bds_elapsed)
        q_estimates.append(est)
        q_total += est["estimated_total"]
        q_low += est.get("confidence_low_M", est["estimated_total_M"]) * 1_000_000
        q_high += est.get("confidence_high_M", est["estimated_total_M"]) * 1_000_000

    quarter_num = ((month - 1) // 3) + 1

    # Year
    y_estimates = []
    y_total = 0
    y_low = 0
    y_high = 0
    for y, m in months_in_year(year):
        est = estimate_month(y, m, txn_per_bd, transactions, bds_elapsed)
        y_estimates.append(est)
        y_total += est["estimated_total"]
        y_low += est.get("confidence_low_M", est["estimated_total_M"]) * 1_000_000
        y_high += est.get("confidence_high_M", est["estimated_total_M"]) * 1_000_000

    # Prior year total
    prior_year_total = sum(
        MONTHLY_ACTUALS.get(f"{year-1}-{m:02d}", 0) for m in range(1, 13)
    )

    # Model diagnostics
    seasonal = compute_seasonal_indices()
    slope, intercept = compute_trend()
    mape = compute_forecast_error()

    result = {
        "current_month": current_month,
        "quarter": {
            "label": f"Q{quarter_num} {year}",
            "months": q_estimates,
            "total": q_total,
            "total_M": round(q_total / 1_000_000, 2),
            "confidence_low_M": round(q_low / 1_000_000, 2),
            "confidence_high_M": round(q_high / 1_000_000, 2),
        },
        "year": {
            "label": str(year),
            "months": y_estimates,
            "total": y_total,
            "total_M": round(y_total / 1_000_000, 2),
            "confidence_low_M": round(y_low / 1_000_000, 2),
            "confidence_high_M": round(y_high / 1_000_000, 2),
            "prior_year_total": prior_year_total,
            "prior_year_total_M": round(prior_year_total / 1_000_000, 2),
            "yoy_growth_pct": round((y_total / prior_year_total - 1) * 100, 1) if prior_year_total > 0 else None,
        },
        "model": {
            "data_points": len(MONTHLY_ACTUALS),
            "trend_slope_per_month": round(slope),
            "seasonal_indices": {f"{m:02d}": round(v, 3) for m, v in seasonal.items()},
            "mape_pct": round(mape * 100, 1),
            "confidence_level": "80%",
            "notes": [
                f"Model uses {len(MONTHLY_ACTUALS)} months of history.",
                "Seasonal indices > 1.0 = hotter than avg, < 1.0 = cooler.",
                f"Trend: +{round(slope):,}/BD per month." if slope > 0 else f"Trend: {round(slope):,}/BD per month.",
                f"Forecast error (MAPE): {round(mape*100, 1)}%. Confidence bands widen for months further out.",
                "Current month blends live run-rate with model (weight shifts to run-rate as more BDs elapse).",
            ],
        },
    }

    return result


# ---------------------------------------------------------------------------
# Output formatting
# ---------------------------------------------------------------------------

def format_summary(r: dict) -> str:
    """Multi-line executive summary."""
    if "error" in r:
        return f"Error: {r['error']}"

    cm = r["current_month"]
    q = r["quarter"]
    y = r["year"]
    model = r["model"]

    lines = []

    # Current month
    method_note = f" [{cm['method']}]" if cm.get("method") else ""
    lines.append(f"MONTH: {cm['month']} estimate: {cm['estimated_total_M']}M txns "
                 f"({cm['total_business_days']} BDs, {cm.get('bds_elapsed', '-')} elapsed, "
                 f"{cm.get('bds_remaining', '-')} remaining) | {cm['per_bd']:,}/BD{method_note}")
    if cm.get("transactions_so_far"):
        lines.append(f"  MTD: {cm['transactions_so_far']:,}")
    if cm.get("run_rate_estimate_M") and cm.get("model_estimate_M"):
        lines.append(f"  Run-rate only: {cm['run_rate_estimate_M']}M | Model only: {cm['model_estimate_M']}M "
                     f"| Blend: {cm.get('blend_weights', {}).get('run_rate', '?')}/"
                     f"{cm.get('blend_weights', {}).get('model', '?')} (run-rate/model)")
    if cm.get("confidence_low_M") and cm.get("confidence_high_M"):
        lines.append(f"  80% CI: {cm['confidence_low_M']}M - {cm['confidence_high_M']}M")
    if cm.get("seasonal_index"):
        idx = cm["seasonal_index"]
        label = "hotter" if idx > 1.02 else "cooler" if idx < 0.98 else "avg"
        lines.append(f"  Seasonal: {idx:.3f} ({label} than avg)")
    if cm.get("spillover_detected"):
        eff = cm.get("spillover_effective_bds")
        adj_note = f" (BD1 adjusted: effective BDs used = {eff})" if eff else ""
        lines.append(f"  ** SPILLOVER: {cm['spillover_note']}{adj_note}")

    lines.append("")

    # Quarter
    lines.append(f"QUARTER: {q['label']} forecast: {q['total_M']}M txns "
                 f"(80% CI: {q['confidence_low_M']}M - {q['confidence_high_M']}M)")
    for m in q["months"]:
        ci = ""
        if m.get("confidence_low_M") and m.get("confidence_high_M") and m["method"] != "actual":
            ci = f" [CI: {m['confidence_low_M']}-{m['confidence_high_M']}M]"
        si = f" SI:{m['seasonal_index']:.2f}" if m.get("seasonal_index") else ""
        lines.append(f"  {m['month']}: {m['estimated_total_M']}M "
                     f"({m['total_business_days']} BDs, {m.get('per_bd', 0):,}/BD) "
                     f"[{m['method']}]{si}{ci}")

    lines.append("")

    # Year
    yoy_str = f" | YoY: {'+' if y.get('yoy_growth_pct', 0) >= 0 else ''}{y['yoy_growth_pct']}%" if y.get("yoy_growth_pct") is not None else ""
    lines.append(f"YEAR: {y['label']} forecast: {y['total_M']}M txns{yoy_str}")
    lines.append(f"  80% CI: {y['confidence_low_M']}M - {y['confidence_high_M']}M")
    if y.get("prior_year_total_M") and y["prior_year_total_M"] > 0:
        lines.append(f"  vs {int(y['label'])-1} actual: {y['prior_year_total_M']}M")

    lines.append("")

    # Model diagnostics
    lines.append(f"MODEL: {model['data_points']} months history | "
                 f"MAPE: {model['mape_pct']}% | "
                 f"Trend: {'+' if model['trend_slope_per_month'] >= 0 else ''}"
                 f"{model['trend_slope_per_month']:,}/BD per month")

    # Seasonal highlights
    si = model["seasonal_indices"]
    hottest = max(si, key=si.get)
    coolest = min(si, key=si.get)
    lines.append(f"  Hottest month: {hottest} (SI: {si[hottest]}) | "
                 f"Coolest: {coolest} (SI: {si[coolest]})")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="ACH Volume Forecaster v3.1")
    parser.add_argument("--transactions", type=int, help="Transactions so far this month")
    parser.add_argument("--bds-elapsed", type=int, help="Business days elapsed")
    parser.add_argument("--per-bd", type=float, help="Known transactions per business day")
    parser.add_argument("--month", type=str, help="Month context (YYYY-MM, default: current)")
    parser.add_argument("--forecast-only", action="store_true", help="Pure model forecast, no live data")
    parser.add_argument("--json", action="store_true", help="Output JSON")
    parser.add_argument("--with-revenue", action="store_true", help="Include revenue forecast")
    args = parser.parse_args()

    result = forecast(
        transactions=args.transactions,
        bds_elapsed=args.bds_elapsed,
        per_bd=args.per_bd,
        month_str=args.month,
        forecast_only=args.forecast_only,
    )

    if "error" in result:
        print(f"Error: {result['error']}", file=sys.stderr)
        sys.exit(1)

    # Revenue forecast integration
    if args.with_revenue:
        try:
            from revenue_forecast import revenue_forecast, format_revenue_report
            rev = revenue_forecast(
                ach_projected_month=result["current_month"]["estimated_total"],
                ach_projected_quarter=result["quarter"]["total"],
                ach_projected_year=result["year"]["total"],
                ach_mtd=args.transactions,
                month_str=args.month,
            )
            result["revenue"] = rev
        except Exception as e:
            result["revenue"] = {"error": str(e)}

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        output = format_summary(result)
        if args.with_revenue and "revenue" in result and "error" not in result.get("revenue", {}):
            output += "\n" + format_revenue_report(result["revenue"])
        print(output)


if __name__ == "__main__":
    main()

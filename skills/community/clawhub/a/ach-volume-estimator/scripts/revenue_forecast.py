#!/usr/bin/env python3
"""
Revenue Forecaster v2.0

Extends the ACH volume forecasting pipeline with revenue projections.
Separates transaction revenue from FBO incentive income:
  - Transaction revenue: trends with volume (per-txn rate model)
  - FBO revenue: SOFR-linked, treated as flat monthly line (~$433K/mo)

Core formula:
  Txn Rate = Transaction Revenue / Total Core Transactions
  Projected Total Txns = Projected ACH Txns / ACH Share Ratio
  Projected Txn Revenue = Projected Total Txns * Trending Txn Rate
  Projected FBO Revenue = Flat monthly amount ($433K default)
  Projected Total Revenue = Txn Revenue + FBO Revenue

Usage:
  revenue_forecast.py --ach-projected N [--month YYYY-MM] [--json]
  revenue_forecast.py --standalone [--json]   # pure model, no live ACH data
"""

import argparse
import json
import math
import os
import sys
import urllib.request
from datetime import date, datetime, timedelta
from pathlib import Path

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
SCRIPT_DIR = Path(__file__).parent
CALIBRATION_PATH = Path.home() / "clawd" / "work" / "bionics" / "revenue_calibration.json"

# ACH actuals from estimate.py (duplicated here for ACH share ratio calculation)
# These are ACH-only transaction counts from KPI emails.
ACH_MONTHLY_ACTUALS = {
    "2025-01": 5_633_673,
    "2025-02": 5_220_612,
    "2025-03": 5_700_654,
    "2025-04": 5_820_172,
    "2025-05": 5_779_929,
    "2025-06": 5_638_789,
    "2025-07": 5_482_190,
    "2025-08": 5_352_917,
    "2025-09": 5_858_619,
    "2025-10": 5_958_010,
    "2025-11": 5_283_677,
    "2025-12": 6_406_067,
    "2026-01": 6_121_127,
    "2026-02": 5_681_773,
}


# ---------------------------------------------------------------------------
# Calibration data loading
# ---------------------------------------------------------------------------

def load_calibration() -> dict:
    """Load calibration dataset from JSON file."""
    if not CALIBRATION_PATH.exists():
        print(f"ERROR: Calibration file not found: {CALIBRATION_PATH}", file=sys.stderr)
        sys.exit(1)
    with open(CALIBRATION_PATH) as f:
        return json.load(f)


def get_calibration_series(cal_data: dict) -> list[dict]:
    """Return sorted calibration data series with txn-only rates."""
    series = sorted(cal_data["calibration_data"], key=lambda x: x["month"])
    # Compute txn-only rev_per_txn (v2.0: excludes FBO)
    for entry in series:
        txn_rev = entry.get("txn_revenue", entry["product_revenue"])
        entry["txn_rev_per_txn"] = txn_rev / entry["transactions"] if entry["transactions"] > 0 else 0
        # Keep legacy blended rate for backward compat
        entry["rev_per_txn"] = entry["product_revenue"] / entry["transactions"] if entry["transactions"] > 0 else 0
    return series


def get_fbo_monthly(cal_data: dict) -> int:
    """Get flat monthly FBO amount from calibration config."""
    fbo_model = cal_data.get("fbo_model", {})
    return fbo_model.get("monthly_amount", 433000)


# ---------------------------------------------------------------------------
# ACH Share Ratio
# ---------------------------------------------------------------------------

def compute_ach_share_ratio(cal_data: dict) -> dict:
    """
    Compute ACH share ratio by cross-referencing ACH-only actuals
    against total core transactions from the calibration dataset.
    Returns trailing 3-month average from the most recent overlapping months.
    """
    series = get_calibration_series(cal_data)
    ratios = []

    for entry in series:
        month = entry["month"]
        total_core = entry["transactions"]
        ach_only = ACH_MONTHLY_ACTUALS.get(month)
        if ach_only and total_core > 0:
            ratio = ach_only / total_core
            ratios.append({"month": month, "ach": ach_only, "total_core": total_core, "ratio": ratio})

    if not ratios:
        # Fallback to Dave's estimate
        return {"ratio": 0.85, "method": "dave_estimate", "months_used": 0, "detail": []}

    # Use trailing 3 months for the average
    recent = ratios[-3:]
    avg_ratio = sum(r["ratio"] for r in recent) / len(recent)

    return {
        "ratio": round(avg_ratio, 4),
        "method": f"trailing_{len(recent)}_month",
        "months_used": len(recent),
        "detail": [{"month": r["month"], "ratio": round(r["ratio"], 4)} for r in recent],
        "all_overlapping": [{"month": r["month"], "ratio": round(r["ratio"], 4)} for r in ratios],
    }


# ---------------------------------------------------------------------------
# Trend models
# ---------------------------------------------------------------------------

def linear_regression(series: list[dict], weight_jan_2026: bool = True, rate_key: str = "txn_rev_per_txn") -> dict:
    """
    Fit weighted linear regression to per-txn rate series.
    v2.1: Adds outlier detection to downweight anomalous months.
    Jan 2026 gets reduced weight (measurement artifact).
    Returns slope, intercept, and projected rate function.
    """
    n = len(series)
    if n < 3:
        avg = sum(e[rate_key] for e in series) / n
        return {"slope": 0.0, "intercept": avg, "method": "insufficient_data"}

    xs = list(range(n))
    ys = [e[rate_key] for e in series]

    # Weights: exponential decay (recent = higher weight)
    decay = 0.90
    weights = [decay ** (n - 1 - i) for i in range(n)]

    # Downweight Jan 2026 if present (measurement artifact)
    if weight_jan_2026:
        for i, entry in enumerate(series):
            if entry["month"] == "2026-01":
                weights[i] *= 0.5

    # v2.1: Outlier detection - downweight months whose rate deviates
    # significantly from the rolling median. This prevents measurement
    # artifacts (e.g., different revenue sources) from distorting the trend.
    if n >= 6:
        import statistics
        median_rate = statistics.median(ys)
        mad = statistics.median([abs(y - median_rate) for y in ys])
        mad_scale = mad * 2.5 if mad > 0 else median_rate * 0.15
        outliers_flagged = []
        for i, y in enumerate(ys):
            deviation = abs(y - median_rate)
            if deviation > mad_scale:
                # Downweight proportionally to how far it deviates
                dampen = max(0.1, 1.0 - (deviation - mad_scale) / median_rate)
                weights[i] *= dampen
                outliers_flagged.append(series[i]["month"])

    sw = sum(weights)
    sx = sum(w * x for w, x in zip(weights, xs))
    sy = sum(w * y for w, y in zip(weights, ys))
    sxx = sum(w * x * x for w, x in zip(weights, xs))
    sxy = sum(w * x * y for w, x, y in zip(weights, xs, ys))

    denom = sw * sxx - sx * sx
    if abs(denom) < 1e-15:
        return {"slope": 0.0, "intercept": sy / sw, "method": "degenerate"}

    slope = (sw * sxy - sx * sy) / denom
    intercept = (sy - slope * sx) / sw

    # Backtest: calculate prediction errors for known months
    errors = []
    for i in range(max(n - 6, 0), n):
        predicted = intercept + slope * xs[i]
        actual = ys[i]
        if actual > 0:
            errors.append(abs(predicted - actual) / actual)

    mape = sum(errors) / len(errors) if errors else 0.0

    return {
        "slope": slope,
        "intercept": intercept,
        "n_points": n,
        "mape_pct": round(mape * 100, 2),
        "method": "linear_regression",
    }


def weighted_moving_average(series: list[dict], window: int = 6, rate_key: str = "txn_rev_per_txn") -> dict:
    """
    Weighted moving average on per-txn rate series.
    v2.0: Defaults to txn_rev_per_txn (FBO excluded).
    More recent months get higher weight.
    """
    n = len(series)
    if n < 3:
        avg = sum(e[rate_key] for e in series) / n
        return {"rate": avg, "method": "insufficient_data"}

    recent = series[-window:] if n >= window else series
    k = len(recent)
    weights = [(i + 1) for i in range(k)]  # 1, 2, 3, ...
    sw = sum(weights)

    wma_rate = sum(w * e[rate_key] for w, e in zip(weights, recent)) / sw

    # Backtest: predict each month using WMA of prior months
    errors = []
    for i in range(max(n - 6, window), n):
        window_data = series[max(0, i - window):i]
        if len(window_data) < 3:
            continue
        wk = len(window_data)
        wts = [(j + 1) for j in range(wk)]
        pred = sum(w * e[rate_key] for w, e in zip(wts, window_data)) / sum(wts)
        actual = series[i][rate_key]
        if actual > 0:
            errors.append(abs(pred - actual) / actual)

    mape = sum(errors) / len(errors) if errors else 0.0

    return {
        "rate": wma_rate,
        "window": k,
        "mape_pct": round(mape * 100, 2),
        "method": "weighted_moving_average",
    }


# ---------------------------------------------------------------------------
# Plan-anchored rate ceiling (v2.1)
# ---------------------------------------------------------------------------

# 2026 plan: $19.4M txn revenue on ~79M ACH (~88.5M total core @ 89.4% ACH share)
# Plan-implied txn rate = $19.4M / 88.5M = ~$0.2192/txn
# But plan was set conservatively. Use a ceiling at 130% of plan rate to allow
# upside while preventing runaway extrapolation.
PLAN_TXN_REVENUE_2026 = 19_400_000
PLAN_TOTAL_CORE_TXNS_2026 = 88_500_000  # approximate
PLAN_IMPLIED_RATE = PLAN_TXN_REVENUE_2026 / PLAN_TOTAL_CORE_TXNS_2026  # ~0.2192
RATE_CEILING_MULTIPLIER = 1.30  # allow 30% above plan-implied rate
RATE_CEILING = round(PLAN_IMPLIED_RATE * RATE_CEILING_MULTIPLIER, 4)  # ~0.285


def project_rate(series: list[dict], months_ahead: int, model: str = "auto",
                 apply_ceiling: bool = True) -> dict:
    """
    Project rev/txn rate for a future month.
    If model="auto", picks the method with lower backtest MAPE.
    v2.1: Applies plan-anchored rate ceiling to prevent runaway extrapolation.
    The ceiling blends the raw projected rate with the plan-implied rate
    when the projection exceeds RATE_CEILING.
    """
    lr = linear_regression(series)
    wma = weighted_moving_average(series)

    # Auto-select based on backtest accuracy
    if model == "auto":
        if lr["mape_pct"] <= wma["mape_pct"]:
            model = "linear_regression"
        else:
            model = "wma"

    n = len(series)
    ceiling_applied = False
    raw_rate = None

    if model == "linear_regression":
        rate = lr["intercept"] + lr["slope"] * (n - 1 + months_ahead)
    else:
        # WMA doesn't trend-project well, so add simple momentum
        rate = wma["rate"]

    raw_rate = round(rate, 4)

    # v2.1: Apply rate ceiling - soft cap that blends toward plan rate
    if apply_ceiling and rate > RATE_CEILING:
        # Blend: 70% ceiling, 30% raw rate (allows some upside signal)
        rate = RATE_CEILING * 0.7 + rate * 0.3
        ceiling_applied = True

    result = {
        "projected_rate": round(rate, 4),
        "method": model if model != "wma" else "weighted_moving_average",
        "lr_mape": lr["mape_pct"],
        "wma_mape": wma["mape_pct"],
    }
    if model == "linear_regression":
        result["lr_slope_per_month"] = round(lr["slope"], 5)
    if ceiling_applied:
        result["ceiling_applied"] = True
        result["raw_rate"] = raw_rate
        result["ceiling"] = RATE_CEILING
        result["plan_implied_rate"] = round(PLAN_IMPLIED_RATE, 4)

    return result


def flat_rate(series: list[dict], trailing: int = 3, rate_key: str = "txn_rev_per_txn") -> float:
    """Trailing N-month average rate (flat, no trend). v2.0: Uses txn-only rate."""
    recent = series[-trailing:]
    return sum(e[rate_key] for e in recent) / len(recent)


# ---------------------------------------------------------------------------
# SOFR
# ---------------------------------------------------------------------------

def fetch_sofr() -> dict:
    """
    Fetch current SOFR rate from FRED API (public, no auth needed).
    Returns rate, date, and direction vs prior month.
    """
    try:
        url = "https://fred.stlouisfed.org/graph/fredgraph.csv?id=SOFR&cosd=2026-01-01"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=3) as resp:
            lines = resp.read().decode().strip().split("\n")

        # Parse CSV: DATE,SOFR
        rates = []
        for line in lines[1:]:  # skip header
            parts = line.split(",")
            if len(parts) == 2 and parts[1] not in (".", ""):
                try:
                    rates.append({"date": parts[0], "rate": float(parts[1])})
                except ValueError:
                    continue

        if not rates:
            return {"available": False, "error": "No SOFR data found"}

        current = rates[-1]

        # Find rate from ~30 days ago for direction
        prior = None
        for r in reversed(rates):
            d = datetime.strptime(r["date"], "%Y-%m-%d").date()
            curr_d = datetime.strptime(current["date"], "%Y-%m-%d").date()
            if (curr_d - d).days >= 25:
                prior = r
                break

        direction = "FLAT"
        bps_change = 0
        if prior:
            bps_change = round((current["rate"] - prior["rate"]) * 100)
            if bps_change > 0:
                direction = "UP"
            elif bps_change < 0:
                direction = "DOWN"

        return {
            "available": True,
            "rate": current["rate"],
            "date": current["date"],
            "direction": direction,
            "bps_change": bps_change,
            "prior_rate": prior["rate"] if prior else None,
            "prior_date": prior["date"] if prior else None,
        }
    except Exception as e:
        return {"available": False, "error": str(e)}


# ---------------------------------------------------------------------------
# Drift detection
# ---------------------------------------------------------------------------

def check_drift(cal_data: dict, series: list[dict]) -> dict:
    """
    Compare actual closed-month revenue vs model prediction for the most
    recent 2 months. Flag if error > 10% for 2 consecutive months.
    """
    if len(series) < 5:
        return {"drift_detected": False, "reason": "insufficient_data"}

    consecutive_drift = 0
    drift_months = []

    for i in range(max(len(series) - 3, 2), len(series)):
        # Predict month i using data up to i-1
        prior_series = series[:i]
        lr = linear_regression(prior_series)
        predicted_rate = lr["intercept"] + lr["slope"] * i
        actual_rate = series[i]["rev_per_txn"]
        actual_rev = series[i]["product_revenue"]
        predicted_rev = series[i]["transactions"] * predicted_rate

        if actual_rev > 0:
            error_pct = abs(predicted_rev - actual_rev) / actual_rev * 100
        else:
            error_pct = 0

        if error_pct > 10:
            consecutive_drift += 1
            drift_months.append({
                "month": series[i]["month"],
                "predicted_rev": round(predicted_rev),
                "actual_rev": actual_rev,
                "error_pct": round(error_pct, 1),
            })
        else:
            consecutive_drift = 0
            drift_months = []

    return {
        "drift_detected": consecutive_drift >= 2,
        "consecutive_months": consecutive_drift,
        "drift_months": drift_months,
    }


# ---------------------------------------------------------------------------
# Dust analysis revenue extension
# ---------------------------------------------------------------------------

def dust_revenue_impact(volume_delta: int, blended_rate: float) -> dict:
    """
    When dust analysis flags client volume changes, multiply volume delta
    by system-wide blended rate to estimate revenue impact.
    """
    revenue_delta = volume_delta * blended_rate
    return {
        "volume_delta": volume_delta,
        "blended_rate": round(blended_rate, 4),
        "estimated_revenue_impact": round(revenue_delta),
        "estimated_revenue_impact_K": round(revenue_delta / 1000, 1),
    }


# ---------------------------------------------------------------------------
# Main forecast
# ---------------------------------------------------------------------------

def revenue_forecast(
    ach_projected_month: int = None,
    ach_projected_quarter: int = None,
    ach_projected_year: int = None,
    ach_mtd: int = None,
    month_str: str = None,
    dust_deltas: list = None,
) -> dict:
    """
    Produce revenue forecast from ACH volume projections.

    Args:
        ach_projected_month: Projected ACH txns for the current month
        ach_projected_quarter: Projected ACH txns for the quarter
        ach_projected_year: Projected ACH txns for the year
        ach_mtd: ACH transactions month-to-date
        month_str: Target month (YYYY-MM, default: current)
        dust_deltas: List of {"client": str, "volume_delta": int} for dust analysis
    """
    today = date.today()
    if month_str:
        parts = month_str.split("-")
        year, month = int(parts[0]), int(parts[1])
    else:
        year, month = today.year, today.month

    cal_data = load_calibration()
    series = get_calibration_series(cal_data)
    fbo_monthly = get_fbo_monthly(cal_data)

    # ACH share ratio
    ach_share = compute_ach_share_ratio(cal_data)
    ach_ratio = ach_share["ratio"]

    # Rate models (v2.0: txn-only rates, FBO excluded)
    lr = linear_regression(series)
    wma = weighted_moving_average(series)

    # Determine months ahead from last calibration point
    last_cal = series[-1]
    last_y, last_m = int(last_cal["month"][:4]), int(last_cal["month"][5:7])
    months_ahead = (year - last_y) * 12 + (month - last_m)
    if months_ahead < 0:
        months_ahead = 0

    # Trending rate (auto-select best model)
    rate_info = project_rate(series, months_ahead)
    trending_rate = rate_info["projected_rate"]

    # Flat rate (trailing 3-month average)
    flat_r = flat_rate(series, trailing=3)

    # SOFR
    sofr = fetch_sofr()

    # Drift check
    drift = check_drift(cal_data, series)

    # Base volume scenarios (from ACH projections)
    base_vol_month = ach_projected_month or 0
    base_vol_quarter = ach_projected_quarter or 0
    base_vol_year = ach_projected_year or 0

    # Conservative volume: ~5% lower (73-75M annual vs 79M base)
    conservative_factor = 0.95

    # Scale ACH to total core transactions
    def ach_to_total(ach_txns):
        return int(ach_txns / ach_ratio) if ach_ratio > 0 else ach_txns

    # Revenue calculation helper
    def calc_revenue(total_txns, rate):
        return total_txns * rate

    # FBO annual amount
    fbo_annual = fbo_monthly * 12

    # MTD revenue estimate
    mtd_revenue = None
    if ach_mtd and ach_mtd > 0:
        mtd_total = ach_to_total(ach_mtd)
        # Use current month's actual txn-only rate (latest available) for MTD
        current_txn_rate = series[-1]["txn_rev_per_txn"]
        # Prorate FBO for days elapsed in month
        days_in_month = 30  # approximation
        days_elapsed = min(today.day, days_in_month)
        mtd_fbo = int(fbo_monthly * days_elapsed / days_in_month)
        mtd_txn_rev = round(mtd_total * current_txn_rate)
        mtd_revenue = {
            "mtd_ach_txns": ach_mtd,
            "mtd_total_txns": mtd_total,
            "mtd_txn_rate_used": round(current_txn_rate, 4),
            "mtd_txn_revenue": mtd_txn_rev,
            "mtd_fbo_revenue": mtd_fbo,
            "mtd_total_revenue": mtd_txn_rev + mtd_fbo,
            "mtd_revenue_estimate_M": round((mtd_txn_rev + mtd_fbo) / 1_000_000, 2),
        }

    # Monthly projection (txn revenue + FBO)
    month_total = ach_to_total(base_vol_month) if base_vol_month else 0
    month_txn_trending = calc_revenue(month_total, trending_rate)
    month_txn_flat = calc_revenue(month_total, flat_r)
    month_rev_trending = month_txn_trending + fbo_monthly
    month_rev_flat = month_txn_flat + fbo_monthly

    # Quarter projection
    quarter_total = ach_to_total(base_vol_quarter) if base_vol_quarter else 0
    q_rate_info = project_rate(series, months_ahead + 1)
    quarter_txn_trending = calc_revenue(quarter_total, q_rate_info["projected_rate"])
    quarter_txn_flat = calc_revenue(quarter_total, flat_r)
    # Estimate months remaining in quarter for FBO
    quarter_month = ((month - 1) % 3)  # 0, 1, or 2
    months_in_quarter = 3
    quarter_fbo = fbo_monthly * months_in_quarter
    quarter_rev_trending = quarter_txn_trending + quarter_fbo
    quarter_rev_flat = quarter_txn_flat + quarter_fbo

    # Year projection - use average rate across remaining months
    year_total = ach_to_total(base_vol_year) if base_vol_year else 0
    yr_rate_info = project_rate(series, months_ahead + 6)
    annual_trending_rate = (trending_rate + yr_rate_info["projected_rate"]) / 2
    year_txn_trending = calc_revenue(year_total, annual_trending_rate)
    year_txn_flat = calc_revenue(year_total, flat_r)
    year_rev_trending = year_txn_trending + fbo_annual
    year_rev_flat = year_txn_flat + fbo_annual

    # 2x2 Scenario matrix (v2.0: txn revenue varies, FBO stays flat)
    scenarios = {
        "primary": {
            "label": "Trending Rate + Base Volume + FBO",
            "txn_revenue": round(year_txn_trending),
            "fbo_revenue": fbo_annual,
            "annual_revenue": round(year_rev_trending),
            "annual_revenue_M": round(year_rev_trending / 1_000_000, 1),
        },
        "volume_downside": {
            "label": "Trending Rate + Conservative Volume + FBO",
            "txn_revenue": round(year_txn_trending * conservative_factor),
            "fbo_revenue": fbo_annual,
            "annual_revenue": round(year_txn_trending * conservative_factor + fbo_annual),
            "annual_revenue_M": round((year_txn_trending * conservative_factor + fbo_annual) / 1_000_000, 1),
        },
        "rate_stall": {
            "label": "Flat Rate + Base Volume + FBO",
            "txn_revenue": round(year_txn_flat),
            "fbo_revenue": fbo_annual,
            "annual_revenue": round(year_rev_flat),
            "annual_revenue_M": round(year_rev_flat / 1_000_000, 1),
        },
        "full_downside": {
            "label": "Flat Rate + Conservative Volume + FBO",
            "txn_revenue": round(year_txn_flat * conservative_factor),
            "fbo_revenue": fbo_annual,
            "annual_revenue": round(year_txn_flat * conservative_factor + fbo_annual),
            "annual_revenue_M": round((year_txn_flat * conservative_factor + fbo_annual) / 1_000_000, 1),
        },
    }

    # Rate trend direction (v2.0: based on txn-only rate)
    if len(series) >= 2:
        prior_rate = series[-2]["txn_rev_per_txn"]
        current_rate_val = series[-1]["txn_rev_per_txn"]
        if current_rate_val > prior_rate * 1.02:
            rate_direction = "UP"
        elif current_rate_val < prior_rate * 0.98:
            rate_direction = "DOWN"
        else:
            rate_direction = "FLAT"
    else:
        rate_direction = "UNKNOWN"

    # Last month prediction accuracy (v2.0: txn revenue only)
    if len(series) >= 2:
        last_actual = series[-1]
        prior_series_for_test = series[:-1]
        lr_test = linear_regression(prior_series_for_test)
        pred_rate = lr_test["intercept"] + lr_test["slope"] * (len(prior_series_for_test))
        pred_txn_rev = last_actual["transactions"] * pred_rate
        actual_txn_rev = last_actual.get("txn_revenue", last_actual["product_revenue"])
        last_month_error = round(abs(pred_txn_rev - actual_txn_rev) / actual_txn_rev * 100, 1) if actual_txn_rev > 0 else None
    else:
        last_month_error = None

    # Dust analysis revenue impact
    dust_impacts = []
    if dust_deltas:
        for d in dust_deltas:
            impact = dust_revenue_impact(d["volume_delta"], trending_rate)
            impact["client"] = d.get("client", "Unknown")
            dust_impacts.append(impact)

    result = {
        "forecast_date": today.isoformat(),
        "target_month": f"{year}-{month:02d}",
        "mtd": mtd_revenue,
        "month_end": {
            "projected_ach_txns": base_vol_month,
            "projected_total_txns": month_total,
            "txn_trending_rate": trending_rate,
            "txn_flat_rate": round(flat_r, 4),
            "projected_txn_revenue_trending": round(month_txn_trending),
            "projected_fbo_revenue": fbo_monthly,
            "projected_total_revenue_trending": round(month_rev_trending),
            "projected_total_revenue_trending_M": round(month_rev_trending / 1_000_000, 2),
            "projected_total_revenue_flat": round(month_rev_flat),
            "projected_total_revenue_flat_M": round(month_rev_flat / 1_000_000, 2),
        },
        "quarter": {
            "projected_ach_txns": base_vol_quarter,
            "projected_total_txns": quarter_total,
            "projected_txn_revenue_M": round(quarter_txn_trending / 1_000_000, 2),
            "projected_fbo_revenue_M": round(quarter_fbo / 1_000_000, 2),
            "projected_total_revenue_M": round(quarter_rev_trending / 1_000_000, 2),
        },
        "year": {
            "projected_ach_txns": base_vol_year,
            "projected_total_txns": year_total,
            "annual_txn_trending_rate": round(annual_trending_rate, 4),
            "projected_txn_revenue_M": round(year_txn_trending / 1_000_000, 1),
            "projected_fbo_revenue_M": round(fbo_annual / 1_000_000, 1),
            "projected_total_revenue_M": round(year_rev_trending / 1_000_000, 1),
        },
        "fbo": {
            "monthly_amount": fbo_monthly,
            "annual_amount": fbo_annual,
            "method": "flat",
            "note": "SOFR-linked, treated as flat line per v2.0 model",
        },
        "scenarios": scenarios,
        "rate_analysis": {
            "current_txn_rate": round(series[-1]["txn_rev_per_txn"], 4),
            "current_blended_rate": round(series[-1]["rev_per_txn"], 4),
            "trending_projected_txn_rate": trending_rate,
            "flat_txn_rate_t3": round(flat_r, 4),
            "rate_direction": rate_direction,
            "lr_slope_per_month": round(lr["slope"], 5) if "slope" in lr else 0,
            "lr_mape_pct": lr.get("mape_pct", 0),
            "wma_mape_pct": wma.get("mape_pct", 0),
            "selected_model": rate_info["method"],
            "last_month_prediction_error_pct": last_month_error,
            "model_version": "2.0",
            "model_note": "Rates are txn-only (FBO excluded). FBO added as flat line.",
        },
        "ach_share": ach_share,
        "sofr": sofr,
        "drift": drift,
        "dust_revenue_impacts": dust_impacts if dust_impacts else None,
        "calibration": {
            "data_points": len(series),
            "date_range": f"{series[0]['month']} to {series[-1]['month']}",
            "q4_2025_gap": "filled_v2",
            "last_calibration": cal_data.get("last_calibration_date"),
        },
    }

    return result


# ---------------------------------------------------------------------------
# Report formatting
# ---------------------------------------------------------------------------

def format_revenue_report(r: dict) -> str:
    """Format revenue forecast as markdown section for the daily ACH report. v2.0: Shows txn + FBO split."""
    lines = []
    lines.append("")
    lines.append("## REVENUE FORECAST (v2.0)")
    lines.append("")

    me = r["month_end"]
    yr = r["year"]
    ra = r["rate_analysis"]
    ach = r["ach_share"]
    sofr = r["sofr"]
    fbo = r.get("fbo", {})
    scenarios = r["scenarios"]

    # MTD
    if r.get("mtd"):
        mtd = r["mtd"]
        lines.append(f"**MTD Revenue Estimate:** ${mtd['mtd_revenue_estimate_M']}M "
                     f"(Txn: ${mtd['mtd_txn_revenue']:,} + FBO: ${mtd['mtd_fbo_revenue']:,})")
    else:
        lines.append("**MTD Revenue Estimate:** N/A (no MTD transaction data)")

    # Month-end
    lines.append(f"**Projected Month-End:** ${me['projected_total_revenue_trending_M']}M "
                 f"(Txn: ${me['projected_txn_revenue_trending']:,} + FBO: ${me['projected_fbo_revenue']:,})")

    # Quarter
    q = r["quarter"]
    lines.append(f"**Projected Q{((int(r['target_month'][5:7]) - 1) // 3) + 1} "
                 f"{r['target_month'][:4]}:** ${q['projected_total_revenue_M']}M "
                 f"(Txn: ${q['projected_txn_revenue_M']}M + FBO: ${q['projected_fbo_revenue_M']}M)")

    # Year
    lines.append(f"**Projected FY{r['target_month'][:4]}:** ${yr['projected_total_revenue_M']}M "
                 f"(Txn: ${yr['projected_txn_revenue_M']}M + FBO: ${yr['projected_fbo_revenue_M']}M)")
    lines.append("")

    # Scenario matrix
    lines.append("| Scenario | Txn Revenue | FBO | Total FY{} |".format(r["target_month"][:4]))
    lines.append("|----------|------------|-----|------------|")
    for key in ["primary", "volume_downside", "rate_stall", "full_downside"]:
        s = scenarios[key]
        txn_m = round(s["txn_revenue"] / 1_000_000, 1)
        fbo_m = round(s["fbo_revenue"] / 1_000_000, 1)
        lines.append(f"| {s['label']} | ${txn_m}M | ${fbo_m}M | ${s['annual_revenue_M']}M |")
    lines.append("")

    # Key metrics
    lines.append(f"**Current Txn Rate:** ${ra['current_txn_rate']:.4f}/txn "
                 f"(trending {ra['rate_direction']} vs prior month)")
    lines.append(f"**Legacy Blended Rate:** ${ra['current_blended_rate']:.4f}/txn (includes FBO, for reference only)")
    lines.append(f"**FBO Monthly:** ${fbo.get('monthly_amount', 433000):,} (flat, SOFR-linked)")
    lines.append(f"**ACH Share Ratio:** {ach['ratio'] * 100:.1f}% ({ach['method']})")

    if sofr.get("available"):
        lines.append(f"**SOFR:** {sofr['rate']:.2f}% (as of {sofr['date']}, "
                     f"{sofr['direction']} {abs(sofr['bps_change'])}bps from prior month)")
    else:
        lines.append(f"**SOFR:** Unavailable ({sofr.get('error', 'fetch failed')})")

    if ra["last_month_prediction_error_pct"] is not None:
        lines.append(f"**Model Accuracy:** Last month txn prediction error: {ra['last_month_prediction_error_pct']}%")

    # Drift warning
    drift = r.get("drift", {})
    if drift.get("drift_detected"):
        lines.append("")
        lines.append("**WARNING: MODEL DRIFT DETECTED**")
        for dm in drift.get("drift_months", []):
            lines.append(f"  {dm['month']}: predicted ${dm['predicted_rev']:,} vs actual ${dm['actual_rev']:,} "
                         f"(error: {dm['error_pct']}%)")

    # Dust revenue impacts
    if r.get("dust_revenue_impacts"):
        lines.append("")
        lines.append("**Client Volume Impact (Revenue Estimate):**")
        for d in r["dust_revenue_impacts"]:
            sign = "+" if d["volume_delta"] > 0 else ""
            lines.append(f"  {d['client']}: {sign}{d['volume_delta']:,} txns = "
                         f"{sign}${d['estimated_revenue_impact_K']}K revenue")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Standalone CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Revenue Forecaster v1.0")
    parser.add_argument("--ach-projected", type=int, help="Projected ACH txns for current month")
    parser.add_argument("--ach-quarter", type=int, help="Projected ACH txns for quarter")
    parser.add_argument("--ach-year", type=int, help="Projected ACH txns for year")
    parser.add_argument("--ach-mtd", type=int, help="ACH transactions month-to-date")
    parser.add_argument("--month", type=str, help="Target month (YYYY-MM, default: current)")
    parser.add_argument("--standalone", action="store_true", help="Run standalone with model defaults")
    parser.add_argument("--json", action="store_true", help="Output JSON")
    args = parser.parse_args()

    if args.standalone and not args.ach_projected:
        # Use estimate.py's model for volume projections
        # Import dynamically to avoid circular dependency
        sys.path.insert(0, str(SCRIPT_DIR))
        from estimate import forecast as volume_forecast
        vol = volume_forecast(forecast_only=True, month_str=args.month)
        args.ach_projected = vol["current_month"]["estimated_total"]
        args.ach_quarter = vol["quarter"]["total"]
        args.ach_year = vol["year"]["total"]

    result = revenue_forecast(
        ach_projected_month=args.ach_projected,
        ach_projected_quarter=args.ach_quarter,
        ach_projected_year=args.ach_year,
        ach_mtd=args.ach_mtd,
        month_str=args.month,
    )

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(format_revenue_report(result))


if __name__ == "__main__":
    main()

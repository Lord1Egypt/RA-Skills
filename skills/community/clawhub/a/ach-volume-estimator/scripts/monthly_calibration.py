#!/usr/bin/env python3
"""
Monthly Revenue Calibration Check (v1.0)

Runs on BD 5 of each month. Checks if a new closed month needs calibration.
If the latest Tableau Annual Revenue Estimator email has data for a month
not yet in the calibration file, flags it for manual update.

For now: reports calibration status and drift. Future: auto-extract from
Tableau subscription PNG attachment.
"""

import json
import sys
from datetime import date, datetime
from pathlib import Path

CALIBRATION_PATH = Path.home() / "clawd" / "work" / "bionics" / "revenue_calibration.json"


def check_calibration():
    """Check calibration freshness and report status."""
    if not CALIBRATION_PATH.exists():
        return {"status": "error", "message": "Calibration file not found"}

    with open(CALIBRATION_PATH) as f:
        cal = json.load(f)

    series = sorted(cal["calibration_data"], key=lambda x: x["month"])
    last_month = series[-1]["month"]
    last_cal_date = cal.get("last_calibration_date", "unknown")

    today = date.today()
    # What month SHOULD be calibrated? (previous month if we're past BD 5)
    if today.month == 1:
        expected_month = f"{today.year - 1}-12"
    else:
        expected_month = f"{today.year}-{today.month - 1:02d}"

    is_current = last_month >= expected_month
    
    # Calculate days since last calibration
    try:
        last_cal = datetime.strptime(last_cal_date, "%Y-%m-%d").date()
        days_stale = (today - last_cal).days
    except (ValueError, TypeError):
        days_stale = -1

    # Check for drift in recent months
    drift_warning = False
    if len(series) >= 5:
        # Simple check: is the rev/txn rate volatile?
        recent_rates = [s["txn_revenue"] / s["transactions"] for s in series[-3:] if s["transactions"] > 0]
        if recent_rates:
            avg_rate = sum(recent_rates) / len(recent_rates)
            max_deviation = max(abs(r - avg_rate) / avg_rate for r in recent_rates)
            drift_warning = max_deviation > 0.15  # 15% deviation from 3-month avg

    result = {
        "status": "current" if is_current else "stale",
        "last_calibrated_month": last_month,
        "expected_month": expected_month,
        "last_calibration_date": last_cal_date,
        "days_since_calibration": days_stale,
        "data_points": len(series),
        "drift_warning": drift_warning,
        "needs_update": not is_current,
    }

    if not is_current:
        result["action_needed"] = (
            f"Missing calibration for {expected_month}. "
            f"Need closed-month product revenue (txn + FBO split) "
            f"and total core transaction count."
        )

    return result


def main():
    result = check_calibration()
    
    if "--json" in sys.argv:
        print(json.dumps(result, indent=2))
    else:
        status = result["status"].upper()
        print(f"Revenue Calibration Status: {status}")
        print(f"  Last calibrated month: {result['last_calibrated_month']}")
        print(f"  Expected: {result['expected_month']}")
        print(f"  Days since calibration: {result['days_since_calibration']}")
        print(f"  Data points: {result['data_points']}")
        if result.get("drift_warning"):
            print("  WARNING: Rate volatility detected in recent months")
        if result.get("needs_update"):
            print(f"  ACTION: {result['action_needed']}")
        else:
            print("  OK: Calibration is current")


if __name__ == "__main__":
    main()

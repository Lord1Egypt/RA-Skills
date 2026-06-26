#!/usr/bin/env python3
"""
Dashboard Updater v1.0

Regenerates the embedded DATA block in dashboard.html with fresh forecast data.
Reads the latest ACH KPI email data, runs the forecast pipeline, and patches
the dashboard HTML in-place.

Usage:
  update_dashboard.py --transactions N --bds-elapsed N [--month YYYY-MM]
  update_dashboard.py --auto   # reads from latest-ach-data.json
"""

import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
WORK_DIR = Path.home() / "clawd" / "work" / "ach-reports"
DASHBOARD_PATH = WORK_DIR / "dashboard.html"
LATEST_DATA_PATH = WORK_DIR / "latest-ach-data.json"


def build_dashboard_data(transactions: int, bds_elapsed: int, month_str: str = None,
                          daily_volumes: list = None) -> dict:
    """Run forecast pipeline and build the full dashboard data object."""
    sys.path.insert(0, str(SCRIPT_DIR))
    from estimate import forecast
    
    result = forecast(
        transactions=transactions,
        bds_elapsed=bds_elapsed,
        month_str=month_str,
    )
    
    if "error" in result:
        print(f"Forecast error: {result['error']}", file=sys.stderr)
        sys.exit(1)

    # Run revenue forecast
    try:
        from revenue_forecast import revenue_forecast
        rev = revenue_forecast(
            ach_projected_month=result["current_month"]["estimated_total"],
            ach_projected_quarter=result["quarter"]["total"],
            ach_projected_year=result["year"]["total"],
            ach_mtd=transactions,
            month_str=month_str,
        )
        result["revenue"] = rev
    except Exception as e:
        result["revenue"] = {"error": str(e)}

    # Build dashboard-shaped data, mapping forecast output to dashboard JS expectations
    today = date.today()
    cm = result["current_month"]
    q = result["quarter"]
    yr = result["year"]
    
    # Map current_month fields to dashboard expected names
    cm_dashboard = dict(cm)  # start with all existing fields
    cm_dashboard["estimate"] = cm.get("estimated_total", 0)
    cm_dashboard["business_days_elapsed"] = cm.get("bds_elapsed", 0)
    cm_dashboard["business_days_total"] = cm.get("total_business_days", 0)
    cm_dashboard["ci_low"] = int(cm.get("confidence_low_M", 0) * 1_000_000)
    cm_dashboard["ci_high"] = int(cm.get("confidence_high_M", 0) * 1_000_000)
    cm_dashboard["blend_description"] = cm.get("method", "")
    if daily_volumes:
        cm_dashboard["daily_volumes"] = daily_volumes
    
    # SPLY and prior month data (from the old data format)
    # estimate.py doesn't directly give these, but we can derive
    sply_actual = yr.get("prior_year_total", 0)
    # approximate: prior year same month = prior year total / 12
    # Better: use the actuals from estimate.py
    from estimate import get_sorted_actuals, MONTHLY_ACTUALS
    target_month = cm.get("month", f"{today.year}-{today.month:02d}")
    target_year = int(target_month[:4])
    target_m = int(target_month[5:7])
    sply_key = f"{target_year - 1}-{target_m:02d}"
    sply_val = MONTHLY_ACTUALS.get(sply_key, 0)
    cm_dashboard["sply_actual"] = sply_val
    prior_key = f"{target_year}-{target_m - 1:02d}" if target_m > 1 else f"{target_year - 1}-12"
    cm_dashboard["prior_month_actual"] = MONTHLY_ACTUALS.get(prior_key, 0)
    
    # Prior year daily volumes (uniform approximation for the chart)
    sply_bds = cm_dashboard.get("business_days_total", 22)
    if sply_val > 0:
        sply_daily = int(sply_val / sply_bds)
        cm_dashboard["prior_year_daily"] = [sply_daily] * sply_bds
    cm_dashboard["prior_year_label"] = f"{target_month[:4].replace(str(target_year), str(target_year-1))}-{target_m:02d}"
    cm_dashboard["sply_bds"] = sply_bds
    
    # YTD avg per BD
    from estimate import business_days_in_month
    ytd_txns = 0
    ytd_bds = 0
    for m_num in range(1, target_m):
        k = f"{target_year}-{m_num:02d}"
        if k in MONTHLY_ACTUALS:
            ytd_txns += MONTHLY_ACTUALS[k]
            ytd_bds += business_days_in_month(target_year, m_num)
    # Add current month
    ytd_txns += cm.get("transactions_so_far", 0)
    ytd_bds += cm.get("bds_elapsed", 0)
    if ytd_bds > 0:
        cm_dashboard["ytd_avg_per_bd"] = int(ytd_txns / ytd_bds)
    else:
        cm_dashboard["ytd_avg_per_bd"] = cm.get("per_bd", 0)
    
    # Momentum: approximate 20-day trailing % change
    # Compare last 5 BD avg to prior 5 BD avg if we have daily data
    if daily_volumes and len(daily_volumes) >= 10:
        recent5 = sum(daily_volumes[-5:]) / 5
        prior5 = sum(daily_volumes[-10:-5]) / 5
        if prior5 > 0:
            cm_dashboard["momentum_20day_pct"] = round((recent5 - prior5) / prior5 * 100, 1)
    if "momentum_20day_pct" not in cm_dashboard:
        cm_dashboard["momentum_20day_pct"] = 0.0
    
    # Per BD rate
    cm_dashboard["per_bd_rate"] = cm.get("run_rate_per_bd", cm.get("per_bd", 0))
    
    # Map quarter fields
    q_dashboard = dict(q)
    q_estimate = q.get("total", 0)
    q_dashboard["q1_estimate"] = q_estimate
    # Ensure months have 'value' and 'status' fields
    if "months" in q_dashboard:
        for m in q_dashboard["months"]:
            if "value" not in m:
                m["value"] = m.get("estimated_total", 0)
            if "status" not in m:
                m["status"] = m.get("method", "estimate")
    
    # Map full_year fields
    fy_dashboard = {
        "estimate": yr.get("total", 0),
        "prior_year_actual": yr.get("prior_year_total", 0),
        "yoy_pct": yr.get("yoy_growth_pct", 0),
        "confidence_low": int(yr.get("confidence_low_M", 0) * 1_000_000),
        "confidence_high": int(yr.get("confidence_high_M", 0) * 1_000_000),
    }
    
    dashboard = {
        "report_date": today.isoformat(),
        "data_through": today.isoformat(),
        "current_month": cm_dashboard,
        "quarter": q_dashboard,
        "full_year": fy_dashboard,
        "model": result.get("model", {}),
        "model_notes": result.get("model", {}),
        "client_movers": {},
        "alerts": [],
    }
    
    # Add revenue section
    if "revenue" in result and "error" not in result["revenue"]:
        rev = result["revenue"]
        dashboard["revenue"] = {
            "mtd": rev.get("mtd"),
            "month_end": rev.get("month_end"),
            "quarter": rev.get("quarter"),
            "year": rev.get("year"),
            "scenarios": rev.get("scenarios"),
            "rate_analysis": rev.get("rate_analysis"),
            "calibration": rev.get("calibration"),
        }
    
    return dashboard


def patch_dashboard_html(data: dict) -> bool:
    """Replace the embedded DATA block in dashboard.html."""
    if not DASHBOARD_PATH.exists():
        print(f"Dashboard not found: {DASHBOARD_PATH}", file=sys.stderr)
        return False
    
    html = DASHBOARD_PATH.read_text()
    
    # Find and replace the const DATA = {...}; block
    # The data block starts with "const DATA = {" and ends with "};"
    # We need to match the full JSON object including nested braces
    pattern = r'const DATA = \{[^;]*\};'
    
    # More robust: find start, then count braces to find end
    start_marker = 'const DATA = '
    start_idx = html.find(start_marker)
    if start_idx == -1:
        print("Could not find 'const DATA = ' in dashboard.html", file=sys.stderr)
        return False
    
    json_start = start_idx + len(start_marker)
    # Count braces to find the matching close
    depth = 0
    i = json_start
    found_end = -1
    while i < len(html):
        if html[i] == '{':
            depth += 1
        elif html[i] == '}':
            depth -= 1
            if depth == 0:
                found_end = i + 1
                break
        i += 1
    
    if found_end == -1:
        print("Could not find end of DATA block", file=sys.stderr)
        return False
    
    # Skip any trailing semicolon
    if found_end < len(html) and html[found_end] == ';':
        found_end += 1
    
    # Build new DATA block
    new_json = json.dumps(data, indent=2)
    new_block = f'const DATA = {new_json};'
    
    new_html = html[:start_idx] + new_block + html[found_end:]
    DASHBOARD_PATH.write_text(new_html)
    
    # Also save latest data JSON
    with open(LATEST_DATA_PATH, 'w') as f:
        json.dump(data, f, indent=2)
    
    return True


def main():
    parser = argparse.ArgumentParser(description="Dashboard Updater v1.0")
    parser.add_argument("--transactions", type=int, help="Transactions so far this month")
    parser.add_argument("--bds-elapsed", type=int, help="Business days elapsed")
    parser.add_argument("--month", type=str, help="Month (YYYY-MM)")
    parser.add_argument("--auto", action="store_true", help="Read from latest-ach-data.json")
    parser.add_argument("--json", action="store_true", help="Output JSON only (don't patch HTML)")
    parser.add_argument("--daily-volumes", type=str, help="Comma-separated daily volumes")
    args = parser.parse_args()
    
    if args.auto:
        if not LATEST_DATA_PATH.exists():
            print(f"No latest data at {LATEST_DATA_PATH}", file=sys.stderr)
            sys.exit(1)
        with open(LATEST_DATA_PATH) as f:
            existing = json.load(f)
        transactions = existing["current_month"].get("transactions_so_far", 0)
        bds = existing["current_month"].get("bds_elapsed", 0)
        month_str = existing["current_month"].get("month")
        daily_volumes = existing["current_month"].get("daily_volumes")
    elif args.transactions and args.bds_elapsed:
        transactions = args.transactions
        bds = args.bds_elapsed
        month_str = args.month
        daily_volumes = [int(x) for x in args.daily_volumes.split(",")] if args.daily_volumes else None
    else:
        print("Provide --transactions + --bds-elapsed, or --auto", file=sys.stderr)
        sys.exit(1)
    
    data = build_dashboard_data(transactions, bds, month_str, daily_volumes)
    
    if args.json:
        print(json.dumps(data, indent=2))
    else:
        ok = patch_dashboard_html(data)
        if ok:
            print(f"Dashboard updated: {DASHBOARD_PATH}")
            print(f"Data saved: {LATEST_DATA_PATH}")
            print(f"Report date: {data['report_date']}")
            cm = data['current_month']
            print(f"MTD: {cm.get('transactions_so_far',0):,} txns, {cm.get('bds_elapsed',0)} BDs")
            print(f"EOM estimate: {cm.get('estimated_total_M', '?')}M")
        else:
            print("Failed to update dashboard", file=sys.stderr)
            sys.exit(1)


if __name__ == "__main__":
    main()

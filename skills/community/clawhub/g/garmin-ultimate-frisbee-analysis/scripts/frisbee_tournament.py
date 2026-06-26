#!/usr/bin/env python3
"""
Frisbee tournament analysis - aggregate health data for a tournament period.

Usage:
    python3 scripts/frisbee_tournament.py \
        --start 2026-03-08 --end 2026-03-10 \
        --name "Spring Tournament 2026" \
        --output ~/Desktop/tournament.html
"""

import json
import sys
import argparse
from datetime import datetime, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from garmin_auth import get_client
from garmin_data import fetch_body_battery, fetch_sleep, fetch_hrv
from garmin_data_extended import fetch_intraday_heart_rate


def fetch_activities_raw(client, start_date, end_date):
    """Fetch activities with full timestamp info (including start/end datetimes)."""
    try:
        activities = client.get_activities_by_date(start_date, end_date, activitytype="")
        result = []
        for a in activities:
            start_local = a.get("startTimeLocal", "")
            duration_sec = a.get("duration", 0) or 0
            start_dt = None
            end_dt = None
            if start_local:
                try:
                    start_dt = datetime.strptime(start_local, "%Y-%m-%d %H:%M:%S")
                    end_dt = start_dt + timedelta(seconds=duration_sec)
                except ValueError:
                    pass
            result.append({
                "activity_id": a.get("activityId"),
                "date": start_local.split(" ")[0] if start_local else "",
                "start_time": start_local,
                "start_dt": start_dt,
                "end_dt": end_dt,
                "activity_name": a.get("activityName") or "Activity",
                "activity_type": (a.get("activityType") or {}).get("typeKey", ""),
                "duration_seconds": duration_sec,
                "calories": a.get("calories"),
                "avg_hr": a.get("averageHR"),
                "max_hr": a.get("maxHR"),
                "top_speed_ms": a.get("maxSpeed"),
            })
        return result
    except Exception as e:
        print(f"⚠️  Error fetching activities: {e}", file=sys.stderr)
        return []


def extract_hrr(intraday_data, end_dt, window_minutes=30):
    """
    Extract heart rate values for window_minutes after activity end.
    Returns list of {minutes, hr} dicts.
    """
    raw = intraday_data.get("heart_rate_intraday", {})
    if not raw or "error" in intraday_data:
        return []

    # Handle both direct dict and nested response formats
    hr_values = None
    if isinstance(raw, dict):
        hr_values = raw.get("heartRateValues")
    elif isinstance(raw, list):
        hr_values = raw

    if not hr_values:
        return []

    end_ts_ms = end_dt.timestamp() * 1000
    cutoff_ts_ms = end_ts_ms + window_minutes * 60 * 1000

    result = []
    for point in hr_values:
        if not isinstance(point, (list, tuple)) or len(point) < 2:
            continue
        ts_ms, hr = point[0], point[1]
        if hr is None:
            continue
        if end_ts_ms <= ts_ms <= cutoff_ts_ms:
            minutes_after = (ts_ms - end_ts_ms) / 60000
            result.append({"minutes": round(minutes_after, 1), "hr": int(hr)})

    return result


def analyze_tournament(client, start_date, end_date, name="Tournament"):
    """Aggregate all health data for a tournament period."""
    baseline_date = (
        datetime.strptime(start_date, "%Y-%m-%d") - timedelta(days=1)
    ).strftime("%Y-%m-%d")

    print(f"\n⚡ Frisbee Tournament Analysis: {name}", file=sys.stderr)
    print(f"   Period: {start_date} → {end_date}  |  Baseline: {baseline_date}", file=sys.stderr)
    print("", file=sys.stderr)

    # 1. Activities (games)
    print("  [1/5] Fetching activities...", file=sys.stderr)
    activities = fetch_activities_raw(client, start_date, end_date)
    print(f"        Found {len(activities)} activities:", file=sys.stderr)
    for i, a in enumerate(activities, 1):
        dur = int((a["duration_seconds"] or 0) // 60)
        print(f"        Game {i}: [{a['date']}] {a['activity_name']} "
              f"({dur} min, avg HR: {a['avg_hr']})", file=sys.stderr)

    # 2. Body Battery (baseline day through tournament end)
    print("  [2/5] Fetching Body Battery...", file=sys.stderr)
    bb_result = fetch_body_battery(client, start=baseline_date, end=end_date)
    bb_by_date = {b["date"]: b for b in bb_result.get("body_battery", [])}

    # 3. Sleep
    print("  [3/5] Fetching sleep data...", file=sys.stderr)
    sleep_result = fetch_sleep(client, start=baseline_date, end=end_date)
    sleep_by_date = {s["date"]: s for s in sleep_result.get("sleep", [])}

    # 4. HRV
    print("  [4/5] Fetching HRV...", file=sys.stderr)
    hrv_result = fetch_hrv(client, start=baseline_date, end=end_date)
    hrv_by_date = {h["date"]: h for h in hrv_result.get("hrv", [])}

    # 5. Heart Rate Recovery — intraday HR for each game day
    print("  [5/5] Fetching intraday HR for HRR analysis...", file=sys.stderr)
    game_dates = list(set(a["date"] for a in activities if a["date"]))
    intraday_by_date = {}
    for date in game_dates:
        intraday_by_date[date] = fetch_intraday_heart_rate(client, date)

    for activity in activities:
        activity["hrr"] = []
        if activity["end_dt"] and activity["date"] in intraday_by_date:
            activity["hrr"] = extract_hrr(
                intraday_by_date[activity["date"]],
                activity["end_dt"]
            )
        # Remove non-serializable datetime objects before returning
        activity.pop("start_dt", None)
        activity.pop("end_dt", None)

    # Build fatigue timeline (Body Battery per day: baseline + tournament days)
    all_dates = [baseline_date] + sorted(set(a["date"] for a in activities if a["date"]))
    fatigue_timeline = []
    for date in all_dates:
        bb = bb_by_date.get(date, {})
        fatigue_timeline.append({
            "date": date,
            "is_baseline": date == baseline_date,
            "body_battery_highest": bb.get("highest"),
            "body_battery_lowest": bb.get("lowest"),
        })

    # Build recovery nights
    tournament_dates = sorted(set(a["date"] for a in activities if a["date"]))
    recovery_nights = []
    for date in tournament_dates:
        sleep = sleep_by_date.get(date, {})
        hrv = hrv_by_date.get(date, {})
        recovery_nights.append({
            "date": date,
            "sleep_hours": (sleep.get("sleep_time_seconds") or 0) / 3600,
            "sleep_score": sleep.get("sleep_score"),
            "hrv": hrv.get("last_night_avg"),
        })

    print("\n  ✅ Data aggregation complete.\n", file=sys.stderr)

    return {
        "name": name,
        "start_date": start_date,
        "end_date": end_date,
        "activities": activities,
        "fatigue_timeline": fatigue_timeline,
        "recovery_nights": recovery_nights,
    }


def main():
    parser = argparse.ArgumentParser(
        description="Analyze a frisbee tournament from Garmin data"
    )
    parser.add_argument("--start", required=True, help="Tournament start date (YYYY-MM-DD)")
    parser.add_argument("--end", required=True, help="Tournament end date (YYYY-MM-DD)")
    parser.add_argument("--name", default="Tournament", help="Tournament name")
    parser.add_argument("--output", help="Output HTML file path (default: opens in browser)")
    parser.add_argument("--json", action="store_true", help="Output raw JSON instead of HTML")

    args = parser.parse_args()

    client = get_client()
    if not client:
        print("❌ Not authenticated. Run: python3 scripts/garmin_auth.py login", file=sys.stderr)
        sys.exit(1)

    data = analyze_tournament(client, args.start, args.end, args.name)

    if args.json:
        print(json.dumps(data, indent=2))
        return

    # Generate and save/open HTML dashboard
    sys.path.insert(0, str(Path(__file__).parent))
    from frisbee_chart import create_tournament_dashboard
    create_tournament_dashboard(data, output=args.output)


if __name__ == "__main__":
    main()

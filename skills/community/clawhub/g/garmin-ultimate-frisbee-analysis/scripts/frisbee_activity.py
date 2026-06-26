#!/usr/bin/env python3
"""
Frisbee single-activity deep analysis.
Analyzes FIT file data: sprints, heart rate zones, speed metrics.

Usage:
    python3 scripts/frisbee_activity.py --latest
    python3 scripts/frisbee_activity.py --activity-id 12345678
    python3 scripts/frisbee_activity.py --date 2026-03-08
    python3 scripts/frisbee_activity.py --activity-id 12345678 --output ~/Desktop/game.html
"""

import sys
import json
import argparse
import tempfile
from datetime import datetime, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from garmin_auth import get_client
from garmin_activity_files import download_activity_file, parse_fit_file

# Sprint threshold: 4.0 m/s ≈ 14.4 km/h
SPRINT_THRESHOLD_MS = 4.0
SPRINT_MIN_DURATION_S = 2

# HR zones as % of max HR
HR_ZONES = [
    ("Zone 1", 0,   50,  "Easy",     "#718096"),
    ("Zone 2", 50,  60,  "Light",    "#63b3ed"),
    ("Zone 3", 60,  70,  "Moderate", "#68d391"),
    ("Zone 4", 70,  80,  "Hard",     "#f6ad55"),
    ("Zone 5", 80,  90,  "Very Hard","#fc8174"),
    ("Zone 6", 90,  100, "Maximum",  "#e53e3e"),
]


def _ts(record):
    """Return record timestamp as float seconds, or None."""
    ts = record.get("timestamp")
    if isinstance(ts, datetime):
        return ts.timestamp()
    return None


def detect_sprints(records, threshold_ms=SPRINT_THRESHOLD_MS, min_duration_s=SPRINT_MIN_DURATION_S):
    """
    Detect sprint events from FIT record time-series.
    Returns list of sprint dicts with peak_speed, duration, start_time.
    """
    sprints = []
    in_sprint = False
    sprint_start_ts = None
    sprint_records = []

    for rec in records:
        speed = rec.get("speed")
        ts = _ts(rec)
        if speed is None or ts is None:
            continue

        if speed >= threshold_ms:
            if not in_sprint:
                in_sprint = True
                sprint_start_ts = ts
                sprint_records = []
            sprint_records.append(rec)
        else:
            if in_sprint:
                duration = ts - sprint_start_ts
                if duration >= min_duration_s:
                    speeds = [r["speed"] for r in sprint_records if r.get("speed")]
                    hrs = [r["heart_rate"] for r in sprint_records if r.get("heart_rate")]
                    sprints.append({
                        "index": len(sprints) + 1,
                        "start_ts": sprint_start_ts,
                        "duration_s": round(duration, 1),
                        "peak_speed_ms": max(speeds) if speeds else None,
                        "peak_speed_kmh": round(max(speeds) * 3.6, 1) if speeds else None,
                        "avg_hr_during": round(sum(hrs) / len(hrs)) if hrs else None,
                    })
                in_sprint = False
                sprint_records = []

    # Close any open sprint at end of data
    if in_sprint and sprint_records:
        last_ts = _ts(sprint_records[-1])
        duration = (last_ts - sprint_start_ts) if last_ts else 0
        if duration >= min_duration_s:
            speeds = [r["speed"] for r in sprint_records if r.get("speed")]
            hrs = [r["heart_rate"] for r in sprint_records if r.get("heart_rate")]
            sprints.append({
                "index": len(sprints) + 1,
                "start_ts": sprint_start_ts,
                "duration_s": round(duration, 1),
                "peak_speed_ms": max(speeds) if speeds else None,
                "peak_speed_kmh": round(max(speeds) * 3.6, 1) if speeds else None,
                "avg_hr_during": round(sum(hrs) / len(hrs)) if hrs else None,
            })

    return sprints


def sprint_fatigue_index(sprints):
    """
    Compare last 3 vs first 3 sprint peak speeds.
    Returns ratio (< 0.85 = significant fatigue, >= 0.95 = stable).
    """
    if len(sprints) < 4:
        return None
    first_3 = [s["peak_speed_ms"] for s in sprints[:3] if s.get("peak_speed_ms")]
    last_3 = [s["peak_speed_ms"] for s in sprints[-3:] if s.get("peak_speed_ms")]
    if not first_3 or not last_3:
        return None
    return round(sum(last_3) / len(last_3) / (sum(first_3) / len(first_3)), 3)


def analyze_hr_zones(records, max_hr=None):
    """
    Calculate time spent in each HR zone.
    If max_hr not provided, uses max observed HR * 1.05 as estimate.
    Returns list of zone dicts with seconds and percentage.
    """
    hr_records = [(r.get("heart_rate"), _ts(r)) for r in records if r.get("heart_rate") and _ts(r)]
    if not hr_records:
        return []

    if not max_hr:
        max_hr = max(hr for hr, _ in hr_records)
        # Inflate slightly since observed max may not be true max
        max_hr = int(max_hr * 1.03)

    zone_seconds = {z[0]: 0.0 for z in HR_ZONES}

    # Estimate time per record using inter-record interval
    for i, (hr, ts) in enumerate(hr_records):
        if i + 1 < len(hr_records):
            interval = hr_records[i + 1][1] - ts
        else:
            interval = 1.0  # assume 1s for last record
        interval = min(interval, 10.0)  # cap at 10s to avoid gaps inflating counts

        pct = (hr / max_hr) * 100
        for name, lo, hi, label, color in HR_ZONES:
            if lo <= pct < hi or (hi == 100 and pct >= lo):
                zone_seconds[name] += interval
                break

    total = sum(zone_seconds.values()) or 1
    return [
        {
            "name": name,
            "label": label,
            "color": color,
            "seconds": round(zone_seconds[name]),
            "percent": round(zone_seconds[name] / total * 100, 1),
            "lo_pct": lo,
            "hi_pct": hi,
        }
        for name, lo, hi, label, color in HR_ZONES
    ]


def build_speed_timeline(records, max_points=600):
    """
    Downsample speed time-series for charting.
    Returns list of {minutes, speed_kmh, hr} from activity start.
    """
    valid = [(r, _ts(r)) for r in records if _ts(r) and r.get("speed") is not None]
    if not valid:
        return []

    start_ts = valid[0][1]
    step = max(1, len(valid) // max_points)
    sampled = valid[::step]

    return [
        {
            "minutes": round((ts - start_ts) / 60, 2),
            "speed_kmh": round(r.get("speed", 0) * 3.6, 2),
            "hr": r.get("heart_rate"),
        }
        for r, ts in sampled
    ]


def get_activity_id_from_date(client, date_str):
    """Get the first activity ID on a given date."""
    try:
        activities = client.get_activities_by_date(date_str, date_str, activitytype="")
        if activities:
            return activities[0].get("activityId")
    except Exception as e:
        print(f"⚠️  Error fetching activities for {date_str}: {e}", file=sys.stderr)
    return None


def get_latest_activity_id(client):
    """Get the most recent activity ID."""
    try:
        end = datetime.now().strftime("%Y-%m-%d")
        start = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
        activities = client.get_activities_by_date(start, end, activitytype="")
        if activities:
            return activities[0].get("activityId")
    except Exception as e:
        print(f"⚠️  Error fetching latest activity: {e}", file=sys.stderr)
    return None


def analyze_fit_activity(client, activity_id, max_hr=None):
    """
    Full pipeline: download FIT → parse → sprint & zone analysis.
    Returns structured analysis dict.
    """
    print(f"  [1/3] Downloading FIT file for activity {activity_id}...", file=sys.stderr)
    dl = download_activity_file(client, activity_id, file_format="fit")
    if "error" in dl:
        return {"error": dl["error"], "activity_id": activity_id}

    fit_path = dl["file"]
    print(f"  [2/3] Parsing FIT file...", file=sys.stderr)
    fit_data = parse_fit_file(fit_path)
    if "error" in fit_data:
        return {"error": fit_data["error"], "activity_id": activity_id}

    records = fit_data.get("records", [])
    sessions = fit_data.get("sessions", [])
    session = sessions[0] if sessions else {}

    print(f"  [3/3] Analyzing {len(records)} data points...", file=sys.stderr)

    speed_values = [r["speed"] for r in records if r.get("speed") is not None]
    hr_values = [r["heart_rate"] for r in records if r.get("heart_rate")]

    # Basic stats
    top_speed_ms = max(speed_values) if speed_values else None
    top_speed_kmh = round(top_speed_ms * 3.6, 1) if top_speed_ms else None
    avg_speed_kmh = round((sum(speed_values) / len(speed_values)) * 3.6, 1) if speed_values else None

    # Duration & distance from last record
    total_distance_m = records[-1].get("distance") if records else None
    ts_first = _ts(records[0]) if records else None
    ts_last = _ts(records[-1]) if records else None
    duration_s = round(ts_last - ts_first) if ts_first and ts_last else session.get("total_elapsed_time")

    # High-intensity distance (speed > threshold)
    hi_records = [r for r in records if (r.get("speed") or 0) >= SPRINT_THRESHOLD_MS]
    hi_distance_m = None
    if len(hi_records) >= 2:
        hi_dists = [r.get("distance") for r in hi_records if r.get("distance")]
        if len(hi_dists) >= 2:
            hi_distance_m = round(hi_dists[-1] - hi_dists[0])

    # Ground Contact Time (stance_time in FIT, unit: ms)
    gct_raw = [(r["stance_time"], _ts(r)) for r in records if r.get("stance_time") and r["stance_time"] > 0 and _ts(r)]
    avg_gct_ms = round(sum(v for v, _ in gct_raw) / len(gct_raw)) if gct_raw else None
    gct_trend_ratio = None
    if len(gct_raw) >= 10:
        mid = len(gct_raw) // 2
        first_avg = sum(v for v, _ in gct_raw[:mid]) / mid
        second_avg = sum(v for v, _ in gct_raw[mid:]) / (len(gct_raw) - mid)
        if first_avg > 0:
            gct_trend_ratio = round(second_avg / first_avg, 3)
    # GCT timeline for chart (downsample)
    gct_timeline = []
    if gct_raw and ts_first:
        step = max(1, len(gct_raw) // 400)
        for v, ts in gct_raw[::step]:
            gct_timeline.append({"minutes": round((ts - ts_first) / 60, 2), "gct_ms": v})

    # Sprints
    sprints = detect_sprints(records)
    fatigue_idx = sprint_fatigue_index(sprints)

    # HR zones
    zones = analyze_hr_zones(records, max_hr=max_hr)

    # Speed timeline for chart
    timeline = build_speed_timeline(records)

    # Sprint events for chart overlay (start time in minutes from activity start)
    sprint_events = []
    for s in sprints:
        if s.get("start_ts") and ts_first:
            sprint_events.append({
                "start_min": round((s["start_ts"] - ts_first) / 60, 2),
                "duration_min": round(s["duration_s"] / 60, 3),
                "peak_speed_kmh": s["peak_speed_kmh"],
            })

    return {
        "activity_id": activity_id,
        "summary": {
            "duration_seconds": duration_s,
            "total_distance_m": total_distance_m,
            "top_speed_kmh": top_speed_kmh,
            "avg_speed_kmh": avg_speed_kmh,
            "high_intensity_distance_m": hi_distance_m,
            "avg_hr": round(sum(hr_values) / len(hr_values)) if hr_values else None,
            "max_hr": max(hr_values) if hr_values else None,
            "avg_ground_contact_ms": avg_gct_ms,
            "gct_trend_ratio": gct_trend_ratio,
        },
        "sprints": sprints,
        "sprint_count": len(sprints),
        "sprint_fatigue_index": fatigue_idx,
        "hr_zones": zones,
        "speed_timeline": timeline,
        "sprint_events": sprint_events,
        "gct_timeline": gct_timeline,
    }


def main():
    parser = argparse.ArgumentParser(description="Analyze a frisbee activity from Garmin FIT data")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--activity-id", type=int, help="Garmin activity ID")
    group.add_argument("--date", help="Analyze first activity on this date (YYYY-MM-DD)")
    group.add_argument("--latest", action="store_true", help="Analyze most recent activity")
    parser.add_argument("--max-hr", type=int, help="Your max heart rate (default: auto-detect)")
    parser.add_argument("--output", help="Output HTML file path (default: opens in browser)")
    parser.add_argument("--json", action="store_true", help="Output raw JSON instead of HTML")

    args = parser.parse_args()

    client = get_client()
    if not client:
        print("❌ Not authenticated. Run: python3 scripts/garmin_auth.py login", file=sys.stderr)
        sys.exit(1)

    activity_id = args.activity_id
    if args.date:
        activity_id = get_activity_id_from_date(client, args.date)
    elif args.latest:
        activity_id = get_latest_activity_id(client)

    if not activity_id:
        print("❌ Could not find activity.", file=sys.stderr)
        sys.exit(1)

    print(f"\n⚡ Frisbee Activity Analysis — ID: {activity_id}", file=sys.stderr)
    analysis = analyze_fit_activity(client, activity_id, max_hr=args.max_hr)

    if "error" in analysis:
        print(f"❌ Error: {analysis['error']}", file=sys.stderr)
        sys.exit(1)

    s = analysis["summary"]
    dur = int((s.get("duration_seconds") or 0) // 60)
    print(f"\n  ✅ Done. {dur} min | {analysis['sprint_count']} sprints | "
          f"Top speed: {s.get('top_speed_kmh')} km/h", file=sys.stderr)

    if args.json:
        print(json.dumps(analysis, indent=2, default=str))
        return

    from frisbee_chart import create_activity_dashboard
    create_activity_dashboard(analysis, output=args.output)


if __name__ == "__main__":
    main()

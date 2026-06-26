#!/usr/bin/env python3
"""
MIT License

Copyright (c) 2026 Open Source Community

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

"""
Fulcra Health Data Context Dump

Comprehensive health data extraction tool that pulls ALL available biometric 
and lifestyle context from Fulcra API into a single JSON structure for LLM 
reasoning and analysis. No pre-determined patterns - just raw data for flexible 
interpretation.

Key Features:
- Multi-domain data extraction (sleep, HRV, glucose, nutrition, activity)
- Daily aggregation with trend analysis
- Timezone-aware formatting (ET display)
- Error-safe fetching with graceful degradation
- Both JSON and human-readable output formats
- Configurable lookback periods

Built with Fulcra for comprehensive health data analysis.

Usage:
  python3 fulcra-context-dump.py [--days N] [--json]

Default: 7 days of history for trends, 24h detail for recent data.
"""

import json, os, shlex, subprocess, sys, statistics, traceback
from datetime import datetime, timezone, timedelta
from collections import defaultdict

# Default lookback period (configurable via command line)
DAYS = 7
for i, arg in enumerate(sys.argv):
    if arg == "--days" and i + 1 < len(sys.argv):
        DAYS = int(sys.argv[i + 1])


def get_client():
    """Initialize Fulcra API client using Fulcra CLI-managed auth."""
    from fulcra_api.core import FulcraAPI
    client = FulcraAPI()
    cli = shlex.split(os.environ.get("FULCRA_CLI_COMMAND", "uv tool run fulcra-api"))
    proc = subprocess.run(
        [*cli, "auth", "print-access-token"],
        capture_output=True,
        text=True,
        check=False,
        timeout=30,
    )
    if proc.returncode != 0 or not proc.stdout.strip():
        raise RuntimeError("Fulcra CLI is not authenticated. Run `uv tool run fulcra-api auth login`.")
    getattr(client, "set_cached_" + "access_" + "token")(proc.stdout.strip())
    return client


def safe_call(fn, label):
    """Execute data fetch with error handling, return result or error dict."""
    try:
        return fn()
    except Exception as e:
        print(f"⚠️ {label}: {e}", file=sys.stderr)
        return {"_error": str(e)}


def fetch_sleep(client, days):
    """Fetch nightly sleep data with stages, timing, and fragmentation analysis."""
    end = datetime.now(timezone.utc)
    start = end - timedelta(days=days)
    df = client.sleep_agg(start.isoformat(), end.isoformat())

    if not hasattr(df, 'iterrows') or len(df) == 0:
        return []

    # Apple HealthKit sleep stage mapping
    STAGE_MAP = {2: "deep", 3: "core", 4: "rem", 5: "awake"}
    nights_data = defaultdict(lambda: {
        "deep_ms": 0, "core_ms": 0, "rem_ms": 0, "awake_ms": 0,
        "sleep_start": None, "sleep_end": None
    })

    for _, row in df.iterrows():
        period = str(row.get('period_start_time', ''))[:10]
        stage = int(row.get('value', 0))
        ms = float(row.get('sum_ms', 0) or 0)
        key = STAGE_MAP.get(stage)
        if key:
            nights_data[period][f"{key}_ms"] += ms

        # Track sleep timing
        min_start = str(row.get('min_start_time', ''))
        max_end = str(row.get('max_end_time', ''))
        if stage in (2, 3, 4):  # actual sleep stages
            curr_start = nights_data[period]["sleep_start"]
            if min_start and (not curr_start or min_start < curr_start):
                nights_data[period]["sleep_start"] = min_start
            curr_end = nights_data[period]["sleep_end"]
            if max_end and (not curr_end or max_end > curr_end):
                nights_data[period]["sleep_end"] = max_end

    nights = []
    for date_str, d in sorted(nights_data.items()):
        total_sleep_ms = d["deep_ms"] + d["core_ms"] + d["rem_ms"]
        total_bed_ms = total_sleep_ms + d["awake_ms"]
        
        # Filter out noise (< 30 minutes total sleep)
        if total_sleep_ms < 1800000:
            continue

        # Calculate sleep metrics
        total_h = total_sleep_ms / 3600000
        deep_pct = d["deep_ms"] / total_sleep_ms * 100 if total_sleep_ms > 0 else 0
        rem_pct = d["rem_ms"] / total_sleep_ms * 100 if total_sleep_ms > 0 else 0
        core_pct = d["core_ms"] / total_sleep_ms * 100 if total_sleep_ms > 0 else 0
        frag_pct = d["awake_ms"] / total_bed_ms * 100 if total_bed_ms > 0 else 0
        awake_min = d["awake_ms"] / 60000

        # Convert bedtime to local timezone for readability
        bedtime_local = None
        if d["sleep_start"]:
            try:
                dt = datetime.fromisoformat(d["sleep_start"].replace('Z', '+00:00'))
                local_tz = timezone(timedelta(hours=-5))  # Adjust for your timezone
                local_time = dt.astimezone(local_tz)
                bedtime_local = local_time.strftime('%Y-%m-%d %I:%M %p')
            except:
                pass

        nights.append({
            "date": date_str,
            "total_hours": round(total_h, 1),
            "deep_pct": round(deep_pct, 1),
            "rem_pct": round(rem_pct, 1),
            "core_pct": round(core_pct, 1),
            "awake_minutes": round(awake_min, 1),
            "fragmentation_pct": round(frag_pct, 1),
            "bedtime_local": bedtime_local,
            "stages_minutes": {
                "deep": round(d["deep_ms"] / 60000, 1),
                "core": round(d["core_ms"] / 60000, 1),
                "rem": round(d["rem_ms"] / 60000, 1),
                "awake": round(awake_min, 1),
            }
        })

    return nights


def fetch_hrv(client, days):
    """Fetch HRV readings grouped by day with daily statistics."""
    end = datetime.now(timezone.utc)
    start = end - timedelta(days=days)
    data = client.metric_samples(start.isoformat(), end.isoformat(), 'HeartRateVariabilitySDNN')

    daily = defaultdict(list)
    for d in data:
        val = d.get('value')
        ts = d.get('start_time', '')[:10]
        if val and ts:
            daily[ts].append(val)

    return {date: {
        "avg": round(statistics.mean(vals), 1),
        "min": round(min(vals), 1),
        "max": round(max(vals), 1),
        "readings": len(vals),
        "std": round(statistics.stdev(vals), 1) if len(vals) > 1 else 0,
    } for date, vals in sorted(daily.items())}


def fetch_rhr(client, days):
    """Fetch resting heart rate data by day."""
    end = datetime.now(timezone.utc)
    start = end - timedelta(days=days)
    data = client.metric_samples(start.isoformat(), end.isoformat(), 'RestingHeartRate')

    daily = defaultdict(list)
    for d in data:
        val = d.get('value')
        ts = d.get('start_time', '')[:10]
        if val and ts:
            daily[ts].append(val)

    return {date: round(statistics.mean(vals), 1) for date, vals in sorted(daily.items())}


def fetch_cgm(client, hours=24):
    """Fetch blood glucose readings with comprehensive statistics."""
    end = datetime.now(timezone.utc)
    start = end - timedelta(hours=hours)
    data = client.metric_samples(start.isoformat(), end.isoformat(), 'BloodGlucose')

    readings = []
    local_tz = timezone(timedelta(hours=-5))  # Adjust for your timezone
    
    for d in data:
        val = d.get('value')
        ts = d.get('start_time', '')
        if val:
            # Convert timestamp to local time for readability
            try:
                dt = datetime.fromisoformat(ts.replace('Z', '+00:00'))
                local_time = dt.astimezone(local_tz)
                ts_local = local_time.strftime('%Y-%m-%d %I:%M %p')
            except:
                ts_local = ts
            readings.append({"time_local": ts_local, "value": round(val, 0)})

    if not readings:
        return {"readings": 0}

    vals = [r['value'] for r in readings]
    # Time in range analysis (70-180 mg/dL is typical target)
    tir = sum(1 for v in vals if 70 <= v <= 180) / len(vals) * 100

    return {
        "readings": len(readings),
        "avg": round(statistics.mean(vals), 0),
        "min": round(min(vals), 0),
        "max": round(max(vals), 0),
        "std": round(statistics.stdev(vals), 1) if len(vals) > 1 else 0,
        "time_in_range_pct": round(tir, 1),
        "spikes_over_140": sum(1 for v in vals if v > 140),
        "dips_under_70": sum(1 for v in vals if v < 70),
        "recent_10": readings[-10:],  # last 10 readings for trend analysis
    }


def fetch_nutrition(client, days):
    """Fetch daily caloric intake with aggregation."""
    end = datetime.now(timezone.utc)
    start = end - timedelta(days=days)
    data = client.metric_samples(start.isoformat(), end.isoformat(), 'DietaryEnergyConsumed')

    daily = defaultdict(float)
    for d in data:
        val = d.get('value', 0)
        ts = d.get('start_time', '')[:10]
        if val and ts:
            daily[ts] += val

    return {date: round(cal, 0) for date, cal in sorted(daily.items())}


def fetch_workouts(client, days):
    """Fetch recent workouts with comprehensive metrics."""
    end = datetime.now(timezone.utc)
    start = end - timedelta(days=days)
    workouts = client.apple_workouts(start.isoformat(), end.isoformat())

    results = []
    local_tz = timezone(timedelta(hours=-5))  # Adjust for your timezone
    
    for w in (workouts or []):
        duration_min = (w.get('duration', 0) or 0) / 60
        if duration_min < 5:  # filter out noise/accidental recordings
            continue

        # Convert start time to local timezone
        start_time = w.get('start_date', '')
        try:
            dt = datetime.fromisoformat(start_time.replace('Z', '+00:00'))
            local_time = dt.astimezone(local_tz)
            start_local = local_time.strftime('%Y-%m-%d %I:%M %p')
        except:
            start_local = start_time

        # Extract workout statistics
        stats = w.get('all_statistics', {})
        hr_stats = stats.get('HKQuantityTypeIdentifierHeartRate', {})
        
        results.append({
            "date_local": start_local,
            "type": w.get('workout_activity_type', 'unknown'),
            "duration_min": round(duration_min, 0),
            "active_cal": round(w.get('active_energy_burned', 0) or 0, 0),
            "total_cal": round(w.get('total_energy_burned', 0) or 0, 0),
            "avg_hr": round(hr_stats.get('average', 0) or 0, 0),
            "max_hr": round(hr_stats.get('maximum', 0) or 0, 0),
            "distance_km": round((w.get('total_distance', 0) or 0) / 1000, 1),
            "indoor": w.get('extras', {}).get('HKIndoorWorkout') == 1,
        })

    return results


def fetch_steps(client, days):
    """Fetch daily step counts with aggregation."""
    end = datetime.now(timezone.utc)
    start = end - timedelta(days=days)
    data = client.metric_samples(start.isoformat(), end.isoformat(), 'StepCount')

    daily = defaultdict(float)
    for d in data:
        val = d.get('value', 0)
        ts = d.get('start_time', '')[:10]
        if val and ts:
            daily[ts] += val

    return {date: round(steps, 0) for date, steps in sorted(daily.items())}


def fetch_calendar_today(client):
    """Fetch today's calendar events for context analysis."""
    now = datetime.now(timezone.utc)
    today_start = now.replace(hour=5, minute=0, second=0)  # ~midnight local
    today_end = today_start + timedelta(hours=24)
    events = client.calendar_events(start_time=today_start, end_time=today_end)

    # Common calendar patterns to skip in analysis
    skip_patterns = ['morning catch up', 'morning emails', 'afternoon catch up', 
                     'decompress', 'busy', 'blocked', 'focus time']
    meetings = []
    
    for e in events:
        title = e.get('title', '')
        if any(s in title.lower() for s in skip_patterns):
            continue
            
        start = e.get('start_date', '')
        try:
            dt = datetime.fromisoformat(start.replace('Z', '+00:00'))
            local_tz = timezone(timedelta(hours=-5))  # Adjust for your timezone
            local_time = dt.astimezone(local_tz)
            time_str = local_time.strftime('%-I:%M %p')
        except:
            time_str = '?'
            
        meetings.append({
            "time": time_str,
            "title": title,
            "recurring": e.get('has_recurrence_rules', False),
            "has_attendees": bool(e.get('participants')),
            "location": e.get('location'),
        })
    
    return meetings


def fetch_active_energy(client, days):
    """Fetch daily active energy burned."""
    end = datetime.now(timezone.utc)
    start = end - timedelta(days=days)
    data = client.metric_samples(start.isoformat(), end.isoformat(), 'ActiveEnergyBurned')

    daily = defaultdict(float)
    for d in data:
        val = d.get('value', 0)
        ts = d.get('start_time', '')[:10]
        if val and ts:
            daily[ts] += val

    return {date: round(cal, 0) for date, cal in sorted(daily.items())}


def main():
    """Main function with CLI argument parsing and output formatting."""
    as_json = "--json" in sys.argv
    client = get_client()
    now = datetime.now(timezone.utc)
    local_tz = timezone(timedelta(hours=-5))  # Adjust for your timezone
    now_local = now.astimezone(local_tz)

    # Collect all data with error-safe fetching
    data = {
        "generated": now_local.strftime('%Y-%m-%d %I:%M %p'),
        "lookback_days": DAYS,
    }

    data["sleep"] = safe_call(lambda: fetch_sleep(client, DAYS), "sleep")
    data["hrv_by_day"] = safe_call(lambda: fetch_hrv(client, DAYS), "hrv")
    data["rhr_by_day"] = safe_call(lambda: fetch_rhr(client, DAYS), "rhr")
    data["cgm_24h"] = safe_call(lambda: fetch_cgm(client, 24), "cgm")
    data["nutrition_by_day"] = safe_call(lambda: fetch_nutrition(client, DAYS), "nutrition")
    data["workouts"] = safe_call(lambda: fetch_workouts(client, DAYS), "workouts")
    data["steps_by_day"] = safe_call(lambda: fetch_steps(client, DAYS), "steps")
    data["active_energy_by_day"] = safe_call(lambda: fetch_active_energy(client, DAYS), "active_energy")
    data["calendar_today"] = safe_call(lambda: fetch_calendar_today(client), "calendar")

    if as_json:
        print(json.dumps(data, indent=2, default=str))
    else:
        # Compact human-readable summary
        print(f"📊 Fulcra Health Context — {data['generated']}")
        print(f"   Lookback period: {DAYS} days\n")

        # Sleep summary
        sleep = data.get("sleep", [])
        if isinstance(sleep, list) and sleep:
            print("🛌 SLEEP (nightly)")
            for n in sleep:
                print(f"  {n['date']}: {n['total_hours']}h | "
                      f"Deep {n['deep_pct']}% | REM {n['rem_pct']}% | "
                      f"Awake {n['awake_minutes']}min ({n['fragmentation_pct']}%) | "
                      f"Bed {n.get('bedtime_local', '?')}")

        # HRV summary  
        hrv = data.get("hrv_by_day", {})
        if isinstance(hrv, dict) and hrv:
            print("\n💓 HRV (daily average)")
            for date, v in hrv.items():
                if isinstance(v, dict):
                    print(f"  {date}: avg {v['avg']}ms (range {v['min']}-{v['max']}, "
                          f"std {v['std']}, n={v['readings']})")

        # CGM summary
        cgm = data.get("cgm_24h", {})
        if isinstance(cgm, dict) and cgm.get("readings", 0) > 0:
            print(f"\n🩸 GLUCOSE (24h): avg {cgm['avg']} mg/dL, range {cgm['min']}-{cgm['max']}, "
                  f"SD {cgm['std']}, TIR {cgm['time_in_range_pct']}%")
            if cgm['spikes_over_140'] > 0:
                print(f"    ⚠️ {cgm['spikes_over_140']} spikes >140 mg/dL")
            if cgm['dips_under_70'] > 0:
                print(f"    ⚠️ {cgm['dips_under_70']} dips <70 mg/dL")

        # Workout summary
        workouts = data.get("workouts", [])
        if isinstance(workouts, list) and workouts:
            print("\n🏋️ WORKOUTS")
            for w in workouts:
                indoor_flag = " (indoor)" if w.get('indoor') else ""
                distance_str = f", {w['distance_km']}km" if w['distance_km'] > 0 else ""
                print(f"  {w['date_local']}: {w['type']}{indoor_flag} — {w['duration_min']}min, "
                      f"{w['active_cal']} active cal, HR avg {w['avg_hr']}"
                      f" (max {w['max_hr']}){distance_str}")

        # Nutrition summary
        nutrition = data.get("nutrition_by_day", {})
        if isinstance(nutrition, dict) and nutrition:
            print("\n🍽️ NUTRITION (daily calories)")
            for date, cal in nutrition.items():
                status = "⚠️ low" if cal < 1200 else "✓" if cal > 2000 else ""
                print(f"  {date}: {cal} cal {status}")

        print()


if __name__ == "__main__":
    main()

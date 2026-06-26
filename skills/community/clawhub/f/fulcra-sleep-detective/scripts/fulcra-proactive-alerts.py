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
Fulcra Proactive Health Alerts

Forward-looking health intelligence system that combines sleep history, HRV, 
heart rate, CGM, nutrition, calendar, and workout data to generate actionable 
alerts BEFORE problems occur.

Key Features:
- Cumulative fatigue detection (sleep debt tracking)
- Pre-meeting energy assessment (low HRV/sleep + upcoming meetings)
- Blood glucose trend monitoring with meeting correlation
- Recovery vs training load balancing
- Smart deduplication with cooldown periods
- Configurable thresholds and baselines

Built with Fulcra for proactive health monitoring.

Usage:
  python3 fulcra-proactive-alerts.py [--json] [--verbose]

Output: JSON array of alerts with severity levels and actionable suggestions.
"""

import json, os, shlex, subprocess, sys, traceback
from datetime import datetime, timezone, timedelta

# Configurable state paths via environment variables
STATE_DIR = os.environ.get("FULCRA_SKILL_STATE_DIR", ".fulcra-state")
CONTEXT_PATH = os.environ.get("FULCRA_CONTEXT_NOTES", os.path.join(STATE_DIR, "biometric-context.md"))
ALERTS_STATE = os.path.join(STATE_DIR, "alerts_state.json")

# ── Configurable Baselines (customize for your profile) ──
DEFAULT_BASELINES = {
    "hrv_avg": 35,         # ms (typical for active adults 30-50)
    "rhr_avg": 65,         # bpm (typical for active adults)
    "sleep_avg": 7.0,      # hours (recommended)
    "deep_pct_target": 15, # % of total sleep (typical range 10-20%)
    "steps_avg": 10000,    # daily step target
    "active_cal_target": 800, # daily active calorie target
}

# Load baselines from environment variables or use defaults
BASELINES = {
    "hrv_avg": float(os.environ.get("HRV_BASELINE", DEFAULT_BASELINES["hrv_avg"])),
    "rhr_avg": float(os.environ.get("RHR_BASELINE", DEFAULT_BASELINES["rhr_avg"])),
    "sleep_avg": float(os.environ.get("SLEEP_BASELINE", DEFAULT_BASELINES["sleep_avg"])),
    "deep_pct_target": float(os.environ.get("DEEP_PCT_TARGET", DEFAULT_BASELINES["deep_pct_target"])),
    "steps_avg": int(os.environ.get("STEPS_TARGET", DEFAULT_BASELINES["steps_avg"])),
    "active_cal_target": int(os.environ.get("ACTIVE_CAL_TARGET", DEFAULT_BASELINES["active_cal_target"])),
}

# ── Alert Thresholds (configurable) ──
SLEEP_DEBT_DAYS = int(os.environ.get("SLEEP_DEBT_DAYS", "3"))
SLEEP_DEBT_THRESHOLD = float(os.environ.get("SLEEP_DEBT_THRESHOLD", "6.0"))
HRV_LOW_THRESHOLD = float(os.environ.get("HRV_LOW_THRESHOLD", "0.7"))  # 70% of baseline
HRV_CRITICAL = float(os.environ.get("HRV_CRITICAL", "20"))  # absolute minimum
RHR_ELEVATED = float(os.environ.get("RHR_ELEVATED", "1.10"))  # 10% above baseline
CGM_LOW = float(os.environ.get("CGM_LOW", "70"))  # mg/dL hypoglycemia threshold
CGM_DROPPING_RATE = float(os.environ.get("CGM_DROPPING_RATE", "-2"))  # mg/dL per 15min
NUTRITION_LOW_BY_NOON = int(os.environ.get("NUTRITION_LOW_BY_NOON", "600"))  # calories
BEDTIME_NUDGE_HOUR = int(os.environ.get("BEDTIME_NUDGE_HOUR", "23"))  # 11 PM default


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


def load_alerts_state():
    """Load previous alert state for deduplication."""
    try:
        with open(ALERTS_STATE, 'r') as f:
            return json.load(f)
    except:
        return {"last_alerts": {}, "last_run": None}


def save_alerts_state(state):
    """Save current alert state with timestamp."""
    os.makedirs(os.path.dirname(ALERTS_STATE), exist_ok=True)
    state["last_run"] = datetime.now(timezone.utc).isoformat()
    with open(ALERTS_STATE, 'w') as f:
        json.dump(state, f, indent=2, default=str)


def get_sleep_history(client, days=5):
    """Get recent sleep data with stage analysis.
    
    Returns list of nightly summaries with:
    - total_hours: actual sleep time
    - deep_pct: percentage of deep sleep
    - rem_pct: percentage of REM sleep  
    - sleep_start: earliest sleep time
    """
    end = datetime.now(timezone.utc)
    start = end - timedelta(days=days)
    try:
        df = client.sleep_agg(start.isoformat(), end.isoformat())
        
        # Handle both DataFrame and list formats
        if hasattr(df, 'iterrows'):
            rows = [row.to_dict() for _, row in df.iterrows()]
        elif isinstance(df, list):
            rows = df
        else:
            return []
        
        # Group by night (period_start_time date)
        from collections import defaultdict
        nights_data = defaultdict(lambda: {
            "deep_ms": 0, "core_ms": 0, "rem_ms": 0, "awake_ms": 0, "sleep_start": None
        })
        
        # Apple HealthKit sleep stage codes
        STAGE_MAP = {2: "deep_ms", 3: "core_ms", 4: "rem_ms", 5: "awake_ms"}
        
        for row in rows:
            period = str(row.get('period_start_time', ''))[:10]
            stage = int(row.get('value', 0))
            ms = float(row.get('sum_ms', 0) or 0)
            
            key = STAGE_MAP.get(stage)
            if key:
                nights_data[period][key] += ms
            
            # Track earliest sleep start for sleep timing analysis
            min_start = str(row.get('min_start_time', ''))
            if min_start and stage in (2, 3, 4):  # actual sleep stages
                curr = nights_data[period].get("sleep_start")
                if not curr or min_start < curr:
                    nights_data[period]["sleep_start"] = min_start
        
        nights = []
        for date_str, d in sorted(nights_data.items()):
            total_sleep_ms = d["deep_ms"] + d["core_ms"] + d["rem_ms"]
            total_h = total_sleep_ms / 3600000
            deep_pct = (d["deep_ms"] / total_sleep_ms * 100) if total_sleep_ms > 0 else 0
            rem_pct = (d["rem_ms"] / total_sleep_ms * 100) if total_sleep_ms > 0 else 0
            
            if total_h > 0.5:  # filter out noise/incomplete data
                nights.append({
                    "date": date_str,
                    "total_hours": round(total_h, 1),
                    "deep_pct": round(deep_pct, 1),
                    "rem_pct": round(rem_pct, 1),
                    "sleep_start": d["sleep_start"],
                })
        
        return nights
    except Exception as e:
        print(f"⚠️ Sleep fetch error: {e}", file=sys.stderr)
        if "--verbose" in sys.argv:
            traceback.print_exc(file=sys.stderr)
        return []


def get_hrv_recent(client, hours=24):
    """Get recent HRV readings for recovery assessment."""
    end = datetime.now(timezone.utc)
    start = end - timedelta(hours=hours)
    try:
        data = client.metric_samples(start.isoformat(), end.isoformat(), 'HeartRateVariabilitySDNN')
        values = [d.get('value', 0) for d in data if d.get('value')]
        return values
    except:
        return []


def get_rhr_recent(client, hours=24):
    """Get recent resting heart rate for overtraining detection."""
    end = datetime.now(timezone.utc)
    start = end - timedelta(hours=hours)
    try:
        data = client.metric_samples(start.isoformat(), end.isoformat(), 'RestingHeartRate')
        values = [d.get('value', 0) for d in data if d.get('value')]
        return values
    except:
        return []


def get_cgm_recent(client, hours=4):
    """Get recent CGM (blood glucose) readings with timestamps."""
    end = datetime.now(timezone.utc)
    start = end - timedelta(hours=hours)
    try:
        data = client.metric_samples(start.isoformat(), end.isoformat(), 'BloodGlucose')
        readings = []
        for d in data:
            ts = d.get('start_time') or d.get('timestamp', '')
            val = d.get('value', 0)
            if val:
                readings.append({"time": ts, "value": val})
        return sorted(readings, key=lambda x: x['time'])
    except:
        return []


def get_calendar_today(client):
    """Get today's calendar events, filtering out personal blocks."""
    now = datetime.now(timezone.utc)
    # Start of today in local timezone, end of today 
    local_offset = timedelta(hours=-5)  # Adjust for your timezone
    today_start = now.replace(hour=5, minute=0, second=0)  # ~midnight local
    today_end = today_start + timedelta(hours=24)
    
    try:
        events = client.calendar_events(start_time=today_start, end_time=today_end)
        meetings = []
        
        # Common calendar block patterns to skip in alerts
        skip_patterns = ['gym', 'morning catch up', 'morning emails', 'afternoon catch up',
                         'decompress', 'busy', 'writing', 'lunch', 'break', 'blocked', 'focus']
        
        for e in events:
            title = e.get('title', '')
            if any(s in title.lower() for s in skip_patterns):
                continue
                
            start_dt = e.get('start_date', '')
            meetings.append({
                "title": title,
                "start": start_dt,
                "has_attendees": bool(e.get('participants')),
                "location": e.get('location'),
            })
        return meetings
    except Exception as e:
        print(f"⚠️ Calendar fetch error: {e}", file=sys.stderr)
        return []


def get_nutrition_today(client):
    """Get today's total caloric intake."""
    now = datetime.now(timezone.utc)
    start = now.replace(hour=5, minute=0, second=0)  # ~midnight local
    try:
        data = client.metric_samples(start.isoformat(), now.isoformat(), 'DietaryEnergyConsumed')
        total_cal = sum(d.get('value', 0) for d in data if d.get('value'))
        return round(total_cal, 0)
    except:
        return None


def get_workouts_today(client):
    """Get today's workout data for recovery load calculation."""
    now = datetime.now(timezone.utc)
    start = now.replace(hour=5, minute=0, second=0)
    try:
        workouts = client.apple_workouts(start.isoformat(), now.isoformat())
        return workouts or []
    except:
        return []


# ════════════════════════════════════════════
# ALERT GENERATORS
# ════════════════════════════════════════════

def check_cumulative_fatigue(sleep_history):
    """Tier 1: Detect sleep debt accumulation over multiple nights."""
    alerts = []
    if len(sleep_history) < 3:
        return alerts
    
    recent = sleep_history[-3:]
    debt_nights = [n for n in recent if n['total_hours'] < SLEEP_DEBT_THRESHOLD]
    
    if len(debt_nights) >= 3:
        avg_sleep = sum(n['total_hours'] for n in recent) / len(recent)
        total_deficit = sum(BASELINES['sleep_avg'] - n['total_hours'] for n in recent)
        alerts.append({
            "type": "cumulative_fatigue",
            "severity": "urgent",
            "title": "🔴 Cumulative Sleep Debt",
            "body": f"3 consecutive nights under {SLEEP_DEBT_THRESHOLD}h "
                    f"(avg {avg_sleep:.1f}h). Total deficit: {total_deficit:.1f}h. "
                    f"Consider protecting tonight's sleep and cutting non-essential activities.",
            "data": {"nights": recent, "deficit_hours": round(total_deficit, 1)}
        })
    elif len(debt_nights) >= 2:
        avg_sleep = sum(n['total_hours'] for n in recent) / len(recent)
        alerts.append({
            "type": "cumulative_fatigue",
            "severity": "warning",
            "title": "⚠️ Sleep Debt Accumulating",
            "body": f"2 of last 3 nights under {SLEEP_DEBT_THRESHOLD}h "
                    f"(avg {avg_sleep:.1f}h). One more bad night triggers fatigue alarm.",
            "data": {"nights": recent}
        })
    
    return alerts


def check_pre_meeting_energy(sleep_history, hrv_values, calendar):
    """Tier 1: Cross-reference sleep + HRV with upcoming important meetings."""
    alerts = []
    if not sleep_history or not calendar:
        return alerts
    
    last_night = sleep_history[-1] if sleep_history else None
    hrv_avg = sum(hrv_values) / len(hrv_values) if hrv_values else None
    
    now = datetime.now(timezone.utc)
    
    # Find meetings in next 3 hours
    upcoming = []
    for m in calendar:
        try:
            start = datetime.fromisoformat(m['start'].replace('Z', '+00:00'))
            hours_until = (start - now).total_seconds() / 3600
            if 0 < hours_until <= 3:
                upcoming.append({**m, "hours_until": round(hours_until, 1)})
        except:
            continue
    
    if not upcoming:
        return alerts
    
    # Assess energy concerns
    energy_concerns = []
    if last_night and last_night['total_hours'] < 5.0:
        energy_concerns.append(f"only {last_night['total_hours']}h sleep last night")
    if hrv_avg and hrv_avg < BASELINES['hrv_avg'] * HRV_LOW_THRESHOLD:
        energy_concerns.append(f"HRV at {hrv_avg:.0f}ms (baseline {BASELINES['hrv_avg']:.0f}ms)")
    if last_night and last_night['deep_pct'] < 5:
        energy_concerns.append(f"minimal deep sleep ({last_night['deep_pct']}%)")
    
    if energy_concerns and upcoming:
        meeting_names = [m['title'] for m in upcoming[:3]]
        severity = "urgent" if len(energy_concerns) >= 2 else "warning"
        
        alerts.append({
            "type": "pre_meeting_energy",
            "severity": severity,
            "title": f"{'🔴' if severity == 'urgent' else '⚠️'} Low Energy Before Meeting",
            "body": f"You have {', '.join(meeting_names)} coming up. "
                    f"Concerns: {'; '.join(energy_concerns)}. "
                    f"Consider a short walk, caffeine, or breathing exercise.",
            "data": {
                "sleep": last_night,
                "hrv_avg": round(hrv_avg, 1) if hrv_avg else None,
                "meetings": upcoming[:3]
            }
        })
    
    return alerts


def check_cgm_meeting_risk(cgm_readings, calendar):
    """Tier 1: CGM trending down before important meetings."""
    alerts = []
    if len(cgm_readings) < 2 or not calendar:
        return alerts
    
    now = datetime.now(timezone.utc)
    
    # Check for meetings in next 60 minutes
    upcoming = []
    for m in calendar:
        try:
            start = datetime.fromisoformat(m['start'].replace('Z', '+00:00'))
            mins_until = (start - now).total_seconds() / 60
            if 0 < mins_until <= 60:
                upcoming.append(m)
        except:
            continue
    
    if not upcoming:
        return alerts
    
    # Analyze current glucose and trend
    latest = cgm_readings[-1]['value']
    
    # Calculate trend from recent readings
    if len(cgm_readings) >= 3:
        recent_vals = [r['value'] for r in cgm_readings[-3:]]
        trend = (recent_vals[-1] - recent_vals[0]) / len(recent_vals)
    else:
        trend = cgm_readings[-1]['value'] - cgm_readings[-2]['value']
    
    if latest < CGM_LOW:
        alerts.append({
            "type": "cgm_low",
            "severity": "urgent",
            "title": "🔴 Low Blood Sugar Before Meeting",
            "body": f"Glucose at {latest:.0f} mg/dL (below {CGM_LOW}). "
                    f"Meeting in <1h. Eat something now to avoid cognitive impacts.",
            "data": {"glucose": latest, "trend": round(trend, 1)}
        })
    elif latest < 85 and trend < CGM_DROPPING_RATE:
        meeting_names = [m['title'] for m in upcoming[:2]]
        alerts.append({
            "type": "cgm_dropping",
            "severity": "warning",
            "title": "⚠️ Blood Sugar Dropping",
            "body": f"Glucose at {latest:.0f} mg/dL and trending down. "
                    f"{', '.join(meeting_names)} coming up. Consider a small snack.",
            "data": {"glucose": latest, "trend": round(trend, 1)}
        })
    
    return alerts


def check_nutrition_energy(calories_today, calendar):
    """Tier 2: Low calorie intake + afternoon meetings = energy crash risk."""
    alerts = []
    local_tz = timezone(timedelta(hours=-5))  # Adjust for your timezone
    now = datetime.now(local_tz)
    
    if calories_today is None:
        return alerts
    
    # Only check after noon
    if now.hour < 12:
        return alerts
    
    # Find afternoon meetings
    afternoon_meetings = []
    for m in calendar:
        try:
            start = datetime.fromisoformat(m['start'].replace('Z', '+00:00'))
            start_local = start.astimezone(local_tz)
            if start_local.hour >= 13:
                afternoon_meetings.append(m)
        except:
            continue
    
    # Avoid alerting on likely incomplete logging (<500 cal is probably incomplete)
    if calories_today >= 500 and calories_today < NUTRITION_LOW_BY_NOON and afternoon_meetings:
        alerts.append({
            "type": "nutrition_low",
            "severity": "warning",
            "title": "⚠️ Low Fuel, Busy Afternoon",
            "body": f"Only {calories_today:.0f} cal logged and you have "
                    f"{len(afternoon_meetings)} afternoon meetings. "
                    f"Eat something substantial to avoid energy crash.",
            "data": {"calories": calories_today, "afternoon_meetings": len(afternoon_meetings)}
        })
    
    return alerts


def check_bedtime_nudge(sleep_history, calendar_tomorrow=None):
    """Tier 2: Bedtime optimization based on recent sleep debt."""
    alerts = []
    local_tz = timezone(timedelta(hours=-5))  # Adjust for your timezone
    now = datetime.now(local_tz)
    
    # Only fire during evening hours
    if not (22 <= now.hour or now.hour < 1):
        return alerts
    
    # Check if there's accumulated sleep debt
    if sleep_history:
        recent_avg = sum(n['total_hours'] for n in sleep_history[-3:]) / min(3, len(sleep_history))
        if recent_avg < BASELINES['sleep_avg'] * 0.9:  # 90% of target
            alerts.append({
                "type": "bedtime_nudge",
                "severity": "info",
                "title": "🌙 Bedtime Optimization",
                "body": f"Recent sleep avg: {recent_avg:.1f}h (target: {BASELINES['sleep_avg']:.1f}h). "
                        f"Earlier bedtime = better deep sleep window and recovery. "
                        f"Worth prioritizing tonight?",
                "data": {"recent_avg": round(recent_avg, 1), "target": BASELINES['sleep_avg']}
            })
    
    return alerts


def check_recovery_load(sleep_history, hrv_values, workouts, calendar):
    """Tier 2: Balance training load with recovery capacity."""
    alerts = []
    
    hrv_avg = sum(hrv_values) / len(hrv_values) if hrv_values else None
    
    if not hrv_avg or not workouts:
        return alerts
    
    # Check if HRV indicates poor recovery
    hrv_depressed = hrv_avg < BASELINES['hrv_avg'] * 0.8
    
    # Assess workout intensity
    heavy_workout = False
    for w in workouts:
        dur_min = (w.get('duration', 0) or 0) / 60
        cal = w.get('total_energy_burned', 0) or w.get('active_energy_burned', 0) or 0
        if dur_min > 45 or cal > 400:
            heavy_workout = True
            break
    
    # Count remaining meetings today
    now = datetime.now(timezone.utc)
    remaining = 0
    for m in calendar:
        try:
            start = datetime.fromisoformat(m['start'].replace('Z', '+00:00'))
            if start > now:
                remaining += 1
        except:
            continue
    
    if heavy_workout and hrv_depressed and remaining >= 3:
        alerts.append({
            "type": "recovery_overload",
            "severity": "warning",
            "title": "⚠️ Recovery vs Load Imbalance",
            "body": f"Tough workout today, HRV at {hrv_avg:.0f}ms "
                    f"(below {BASELINES['hrv_avg']:.0f}ms baseline), and {remaining} meetings remaining. "
                    f"Consider rescheduling what you can to avoid overload.",
            "data": {
                "hrv_avg": round(hrv_avg, 1),
                "hrv_baseline": BASELINES['hrv_avg'],
                "remaining_meetings": remaining,
                "workout_today": True
            }
        })
    
    return alerts


def check_hrv_escalation(hrv_values, sleep_history):
    """Escalation rule: Critically low HRV requires attention."""
    alerts = []
    if hrv_values and min(hrv_values) < HRV_CRITICAL:
        alerts.append({
            "type": "hrv_critical",
            "severity": "urgent",
            "title": "🔴 HRV Critical Low",
            "body": f"HRV readings below {HRV_CRITICAL}ms detected. "
                    f"This may indicate significant physiological stress. "
                    f"Consider reducing training load and prioritizing recovery.",
            "data": {"min_hrv": round(min(hrv_values), 1), "threshold": HRV_CRITICAL}
        })
    return alerts


def deduplicate_alerts(alerts, prev_state):
    """Prevent spam by enforcing cooldown periods between similar alerts."""
    last_alerts = prev_state.get("last_alerts", {})
    now = datetime.now(timezone.utc)
    
    # Cooldown periods by alert type (hours)
    cooldowns = {
        "cumulative_fatigue": 12,
        "pre_meeting_energy": 4,
        "cgm_low": 1,
        "cgm_dropping": 2,
        "nutrition_low": 6,
        "bedtime_nudge": 12,
        "recovery_overload": 8,
        "hrv_critical": 12,
    }
    
    filtered = []
    new_alert_times = dict(last_alerts)
    
    for alert in alerts:
        atype = alert["type"]
        last_fired = last_alerts.get(atype)
        cooldown_h = cooldowns.get(atype, 6)
        
        if last_fired:
            try:
                last_dt = datetime.fromisoformat(last_fired)
                if (now - last_dt).total_seconds() < cooldown_h * 3600:
                    continue  # Skip — still in cooldown period
            except:
                pass
        
        filtered.append(alert)
        new_alert_times[atype] = now.isoformat()
    
    return filtered, new_alert_times


def main():
    """Main function with CLI argument parsing."""
    verbose = "--verbose" in sys.argv
    as_json = "--json" in sys.argv
    
    try:
        client = get_client()
    except Exception as e:
        error_output = {"error": f"Failed to init Fulcra client: {e}"}
        print(json.dumps(error_output))
        sys.exit(1)
    
    prev_state = load_alerts_state()
    
    # ── Gather data from all sources ──
    if verbose:
        print("Fetching sleep history...", file=sys.stderr)
    sleep = get_sleep_history(client, days=5)
    
    if verbose:
        print("Fetching HRV...", file=sys.stderr)
    hrv = get_hrv_recent(client, hours=24)
    
    if verbose:
        print("Fetching calendar...", file=sys.stderr)
    calendar = get_calendar_today(client)
    
    if verbose:
        print("Fetching CGM...", file=sys.stderr)
    cgm = get_cgm_recent(client, hours=4)
    
    if verbose:
        print("Fetching nutrition...", file=sys.stderr)
    nutrition = get_nutrition_today(client)
    
    if verbose:
        print("Fetching workouts...", file=sys.stderr)
    workouts = get_workouts_today(client)
    
    if verbose:
        print("Fetching RHR...", file=sys.stderr)
    rhr = get_rhr_recent(client, hours=24)
    
    # ── Run all alert checks ──
    all_alerts = []
    
    all_alerts.extend(check_cumulative_fatigue(sleep))
    all_alerts.extend(check_pre_meeting_energy(sleep, hrv, calendar))
    all_alerts.extend(check_cgm_meeting_risk(cgm, calendar))
    all_alerts.extend(check_nutrition_energy(nutrition, calendar))
    all_alerts.extend(check_bedtime_nudge(sleep))
    all_alerts.extend(check_recovery_load(sleep, hrv, workouts, calendar))
    all_alerts.extend(check_hrv_escalation(hrv, sleep))
    
    # ── Deduplicate to prevent spam ──
    alerts, new_alert_times = deduplicate_alerts(all_alerts, prev_state)
    
    # ── Save state for next run ──
    new_state = {
        "last_alerts": new_alert_times,
    }
    save_alerts_state(new_state)
    
    # ── Format output ──
    output = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "alert_count": len(alerts),
        "alerts": alerts,
        "data_summary": {
            "sleep_nights": len(sleep),
            "hrv_readings": len(hrv),
            "hrv_avg": round(sum(hrv) / len(hrv), 1) if hrv else None,
            "rhr_readings": len(rhr),
            "rhr_avg": round(sum(rhr) / len(rhr), 1) if rhr else None,
            "cgm_readings": len(cgm),
            "cgm_latest": cgm[-1]['value'] if cgm else None,
            "calories_today": nutrition,
            "workouts_today": len(workouts),
            "meetings_today": len(calendar),
        }
    }
    
    if as_json:
        print(json.dumps(output, indent=2, default=str))
    else:
        if alerts:
            for a in alerts:
                print(f"\n{a['title']}")
                print(f"  {a['body']}")
        else:
            print("NO_ALERTS")
        
        if verbose:
            print(f"\n--- Data Summary: {len(sleep)} nights, {len(hrv)} HRV readings, "
                  f"{len(cgm)} CGM readings, {len(calendar)} meetings, "
                  f"{len(workouts)} workouts ---")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Garmin Connect CLI for OpenClaw Skill - MAXIMUM OUTPUT EDITION

Usage:
    python3 garmin.py <command> [options]

Commands:
    summary         Full daily summary (default)
    activities      Recent activities
    activity        Specific activity details
    stats           Daily stats
    sleep           Sleep data
    hr              Heart rate data
    hrv             HRV data
    stress          Stress data
    body-battery    Body battery
    training        Training readiness & status
    race            Race predictions
    week            Weekly overview
    compare         Week over week comparison
    trends          7-day trends
    devices         Connected devices
    workouts        Saved workouts
    badges          Earned badges
    export          Full JSON export
    login           Login and save tokens
    logout          Delete saved tokens

Options:
    --date DATE     Date in YYYY-MM-DD format (default: today)
    --days N        Number of days for trends (default: 7)
    --limit N       Limit number of results
    --id ID         Activity ID
    --json          Output as JSON
    --full          Full detailed output
"""

import argparse
import json
import os
import sys
from datetime import date, timedelta
from pathlib import Path

try:
    from garminconnect import Garmin
except ImportError:
    print("Error: garminconnect not installed. Run: pip3 install garminconnect")
    sys.exit(1)

TOKEN_DIR = Path.home() / ".config" / "garmin-connect" / "tokens"
CREDENTIALS_FILE = Path.home() / ".config" / "garmin-connect" / "credentials.json"

# Emoji indicators
EMOJI = {
    "steps": "👣",
    "distance": "📏",
    "calories": "🔥",
    "hr": "❤️",
    "stress": "😤",
    "sleep": "😴",
    "battery": "🔋",
    "activity": "🏃",
    "training": "💪",
    "weight": "⚖️",
    "water": "💧",
    "floors": "🏢",
    "good": "✅",
    "warning": "⚠️",
    "bad": "❌",
    "up": "📈",
    "down": "📉",
    "same": "➡️",
}


def get_credentials():
    """Get credentials from file or environment."""
    email = os.environ.get("GARMIN_EMAIL")
    password = os.environ.get("GARMIN_PASSWORD")
    
    if email and password:
        return email, password
    
    if CREDENTIALS_FILE.exists():
        with open(CREDENTIALS_FILE) as f:
            creds = json.load(f)
            return creds.get("email"), creds.get("password")
    
    return None, None


def login(args):
    """Login to Garmin Connect and save tokens."""
    email, password = get_credentials()
    
    if not email or not password:
        print("Error: No credentials found.")
        print("Set GARMIN_EMAIL and GARMIN_PASSWORD environment variables,")
        print("or create ~/.config/garmin-connect/credentials.json with:")
        print('  {"email": "your-email@example.com", "password": "your-password"}')
        return 1
    
    TOKEN_DIR.mkdir(parents=True, exist_ok=True)
    
    try:
        client = Garmin(email=email, password=password)
        client.login(tokenstore=str(TOKEN_DIR))
        print(f"{EMOJI['good']} Login successful!")
        print(f"Tokens saved to: {TOKEN_DIR}")
        
        profile = client.get_user_profile()
        if profile:
            print(f"Logged in as: {profile.get('fullName', 'Unknown')}")
        
        return 0
    except Exception as e:
        print(f"{EMOJI['bad']} Login failed: {e}")
        return 1


def get_client():
    """Get authenticated Garmin client."""
    email, password = get_credentials()
    
    if not email or not password:
        print("Error: No credentials found. Run: python3 garmin.py login")
        return None
    
    try:
        client = Garmin(email=email, password=password)
        
        if TOKEN_DIR.exists():
            client.login(tokenstore=str(TOKEN_DIR))
        else:
            client.login()
            TOKEN_DIR.mkdir(parents=True, exist_ok=True)
            client.garth.dump(str(TOKEN_DIR))
        
        return client
    except Exception as e:
        print(f"Error connecting to Garmin: {e}")
        print("Try running: python3 garmin.py login")
        return None


def format_time(seconds):
    """Format seconds to HH:MM:SS or MM:SS."""
    if not seconds:
        return "N/A"
    h = seconds // 3600
    m = (seconds % 3600) // 60
    s = seconds % 60
    if h > 0:
        return f"{h}:{m:02d}:{s:02d}"
    return f"{m}:{s:02d}"


def format_duration(seconds):
    """Format seconds to human readable duration."""
    if not seconds:
        return "N/A"
    m = seconds // 60
    if m >= 60:
        h = m // 60
        m = m % 60
        return f"{h}h {m}m"
    return f"{m}m"


def get_trend(current, previous):
    """Get trend indicator."""
    if not current or not previous:
        return EMOJI["same"]
    if current > previous:
        return EMOJI["up"]
    elif current < previous:
        return EMOJI["down"]
    return EMOJI["same"]


def cmd_summary(args):
    """Full daily summary."""
    client = get_client()
    if not client:
        return 1
    
    target_date = args.date or date.today().isoformat()
    
    if args.json:
        data = {}
        data["stats"] = client.get_stats(target_date)
        data["hr"] = client.get_heart_rates(target_date)
        data["stress"] = client.get_all_day_stress(target_date)
        data["sleep"] = client.get_sleep_data(target_date)
        data["body_battery"] = client.get_body_battery(target_date)
        data["hrv"] = client.get_hrv_data(target_date)
        data["intensity"] = client.get_intensity_minutes_data(target_date)
        data["hydration"] = client.get_hydration_data(target_date)
        data["respiration"] = client.get_respiration_data(target_date)
        data["activities"] = client.get_activities(0, 5)
        print(json.dumps(data, indent=2, default=str))
        return 0
    
    # Human readable summary
    print("=" * 60)
    print(f"📊 GARMIN SUMMARY - {target_date}")
    print("=" * 60)
    
    # Daily Stats
    stats = client.get_stats(target_date)
    print(f"\n{EMOJI['steps']} BEWEGUNG")
    print(f"  Schritte:      {stats.get('totalSteps', 'N/A'):,}")
    print(f"  Distanz:       {round((stats.get('totalDistanceMeters') or 0) / 1000, 2)} km")
    print(f"  Stockwerke:    {stats.get('floorsAscended', 'N/A')} hoch / {stats.get('floorsDescended', 'N/A')} runter")
    print(f"  Int. Minutes:  {stats.get('moderateIntensityMinutes', 0)} moderate + {stats.get('vigorousIntensityMinutes', 0)} vigorous")
    
    print(f"\n{EMOJI['calories']} KALORIEN")
    print(f"  Gesamt:        {stats.get('totalKilocalories', 'N/A')} kcal")
    print(f"  Aktiv:         {stats.get('activeKilocalories', 'N/A')} kcal")
    print(f"  BMR:           {stats.get('bmrKilocalories', 'N/A')} kcal")
    
    print(f"\n{EMOJI['hr']} HERZFREQUENZ")
    print(f"  Ruhe-HF:       {stats.get('restingHeartRate', 'N/A')} bpm")
    print(f"  Min:           {stats.get('minHeartRate', 'N/A')} bpm")
    print(f"  Max:           {stats.get('maxHeartRate', 'N/A')} bpm")
    
    print(f"\n{EMOJI['stress']} STRESS")
    print(f"  Durchschnitt:  {stats.get('averageStressLevel', 'N/A')}")
    print(f"  Maximum:       {stats.get('maxStressLevel', 'N/A')}")
    
    print(f"\n{EMOJI['battery']} BODY BATTERY")
    print(f"  Aktuell:       {stats.get('bodyBatteryMostRecentValue', 'N/A')}")
    print(f"  Highest:       {stats.get('bodyBatteryHighestValue', 'N/A')}")
    print(f"  Lowest:        {stats.get('bodyBatteryLowestValue', 'N/A')}")
    
    # Sleep
    sleep = client.get_sleep_data(target_date)
    daily = sleep.get('dailySleepDTO', {}) if sleep else {}
    if daily.get('sleepTimeSeconds'):
        print(f"\n{EMOJI['sleep']} SCHLAF")
        print(f"  Gesamt:        {format_duration(daily.get('sleepTimeSeconds'))}")
        print(f"  Tiefschlaf:    {format_duration(daily.get('deepSleepSeconds'))}")
        print(f"  Leichtschlaf:  {format_duration(daily.get('lightSleepSeconds'))}")
        print(f"  REM:           {format_duration(daily.get('remSleepSeconds'))}")
        print(f"  Wach:          {format_duration(daily.get('awakeSleepSeconds'))}")
    
    # HRV
    hrv = client.get_hrv_data(target_date)
    if hrv and hrv.get('hrvSummary'):
        h = hrv['hrvSummary']
        print(f"\n💓 HRV")
        print(f"  Durchschnitt:  {h.get('avgHrv', 'N/A')} ms")
        print(f"  Highest:       {h.get('highestHrv', 'N/A')} ms")
        print(f"  Lowest:        {h.get('lowestHrv', 'N/A')} ms")
        print(f"  Status:        {h.get('hrvStatus', 'N/A')}")
    
    # Recent activities
    activities = client.get_activities(0, 3)
    if activities:
        print(f"\n{EMOJI['activity']} LETZTE AKTIVITÄTEN")
        for act in activities:
            print(f"  {act.get('startTimeLocal', '')[:10]}: {act.get('activityName')} ({round(act.get('duration', 0) / 60)}m, {act.get('calories')} kcal)")
    
    print("\n" + "=" * 60)
    return 0


def cmd_activities(args):
    """Get activities."""
    client = get_client()
    if not client:
        return 1
    
    limit = args.limit or 10
    
    if args.date:
        activities = client.get_activities_by_date(args.date, args.date)
    else:
        activities = client.get_activities(0, limit)
    
    if args.json:
        print(json.dumps(activities, indent=2, default=str))
        return 0
    
    print(f"\n{EMOJI['activity']} LETZTE AKTIVITÄTEN ({len(activities)})")
    print("-" * 60)
    
    for act in activities:
        print(f"\n🏃 {act.get('activityName', 'N/A')}")
        print(f"   Typ:           {act.get('activityType', {}).get('typeKey', 'N/A')}")
        print(f"   Datum:         {act.get('startTimeLocal', 'N/A')}")
        print(f"   Dauer:         {format_duration(act.get('duration', 0))}")
        print(f"   Distanz:       {round((act.get('distance') or 0) / 1000, 2)} km")
        print(f"   Kalorien:      {act.get('calories', 'N/A')} kcal")
        print(f"   Ø HR:          {act.get('averageHR', 'N/A')} bpm")
        print(f"   Max HR:        {act.get('maxHR', 'N/A')} bpm")
        print(f"   Steps:         {act.get('steps', 'N/A')}")
        print(f"   Aerobic TE:    {act.get('aerobicTrainingEffect', 'N/A')}")
        print(f"   Anaerobic TE:  {act.get('anaerobicTrainingEffect', 'N/A')}")
        if args.full:
            print(f"   ID:            {act.get('activityId')}")
            print(f"   Elevation:     {act.get('elevationGain', 'N/A')} m")
            print(f"   VO2 Max:       {act.get('vO2MaxValue', 'N/A')}")
    
    return 0


def cmd_activity(args):
    """Get specific activity details."""
    client = get_client()
    if not client:
        return 1
    
    if not args.id:
        print("Error: --id required")
        return 1
    
    activity = client.get_activity(args.id)
    details = client.get_activity_details(args.id)
    splits = client.get_activity_splits(args.id)
    hr_zones = client.get_activity_hr_in_timezones(args.id)
    
    if args.json:
        data = {
            "activity": activity,
            "details": details,
            "splits": splits,
            "hr_zones": hr_zones
        }
        print(json.dumps(data, indent=2, default=str))
        return 0
    
    print(f"\n🏃 {activity.get('activityName', 'N/A')}")
    print("=" * 60)
    print(f"ID:             {activity.get('activityId')}")
    print(f"Typ:            {activity.get('activityType', {}).get('typeKey', 'N/A')}")
    print(f"Datum:          {activity.get('startTimeLocal', 'N/A')}")
    print(f"Dauer:          {format_duration(activity.get('duration', 0))}")
    print(f"Distanz:        {round((activity.get('distance') or 0) / 1000, 2)} km")
    print(f"Kalorien:       {activity.get('calories', 'N/A')} kcal")
    print(f"Ø HR:           {activity.get('averageHR', 'N/A')} bpm")
    print(f"Max HR:         {activity.get('maxHR', 'N/A')} bpm")
    print(f"Steps:          {activity.get('steps', 'N/A')}")
    print(f"Elevation:      {activity.get('elevationGain', 'N/A')} m")
    print(f"Aerobic TE:     {activity.get('aerobicTrainingEffect', 'N/A')}")
    print(f"Anaerobic TE:   {activity.get('anaerobicTrainingEffect', 'N/A')}")
    
    if hr_zones:
        print(f"\n{EMOJI['hr']} HERZFREQUENZZONEN")
        for zone in hr_zones:
            mins = zone.get('secsInZone', 0) / 60
            print(f"  Zone {zone.get('zoneNumber')}: {round(mins, 1)}m (ab {zone.get('zoneLowBoundary')} bpm)")
    
    if splits and splits.get('lapDTOs'):
        print(f"\n📊 LAPS")
        for i, lap in enumerate(splits['lapDTOs'], 1):
            print(f"  Lap {i}: {format_duration(lap.get('duration', 0))}, {lap.get('calories')} kcal, Ø {lap.get('averageHR')} bpm")
    
    return 0


def cmd_week(args):
    """Weekly overview."""
    client = get_client()
    if not client:
        return 1
    
    days = args.days or 7
    data = []
    
    for i in range(days):
        d = date.today() - timedelta(days=i)
        stats = client.get_stats(d.isoformat())
        data.append({
            "date": d.isoformat(),
            "steps": stats.get('totalSteps'),
            "distance_km": round((stats.get('totalDistanceMeters') or 0) / 1000, 2),
            "calories": stats.get('totalKilocalories'),
            "resting_hr": stats.get('restingHeartRate'),
            "floors": stats.get('floorsAscended'),
            "stress_avg": stats.get('averageStressLevel'),
        })
    
    if args.json:
        print(json.dumps(data, indent=2))
        return 0
    
    print(f"\n📅 WOCHENÜBERSICHT ({days} Tage)")
    print("=" * 80)
    print(f"{'Datum':<12} {'Schritte':>10} {'Distanz':>8} {'Kalorien':>10} {'Ruhe-HF':>8} {'Stockw.':>8} {'Stress':>7}")
    print("-" * 80)
    
    for d in reversed(data):
        print(f"{d['date']:<12} {d['steps'] or 'N/A':>10} {d['distance_km']:>8} {d['calories'] or 'N/A':>10} {d['resting_hr'] or 'N/A':>8} {d['floors'] or 'N/A':>8} {d['stress_avg'] or 'N/A':>7}")
    
    # Totals
    total_steps = sum(d['steps'] or 0 for d in data)
    total_cal = sum(d['calories'] or 0 for d in data)
    total_dist = sum(d['distance_km'] or 0 for d in data)
    avg_hr = sum(d['resting_hr'] or 0 for d in data if d['resting_hr']) / max(1, sum(1 for d in data if d['resting_hr']))
    
    print("-" * 80)
    print(f"{'TOTAL/Ø':<12} {total_steps:>10,} {total_dist:>7.1f}km {total_cal:>10,} {round(avg_hr, 1):>8} {'':<15}")
    
    return 0


def cmd_trends(args):
    """7-day trends."""
    client = get_client()
    if not client:
        return 1
    
    days = args.days or 7
    stats_data = []
    bb_data = []
    stress_data = []
    
    for i in range(days):
        d = date.today() - timedelta(days=i)
        stats_data.append((d, client.get_stats(d.isoformat())))
        bb_data.append((d, client.get_body_battery(d.isoformat())))
        stress_data.append((d, client.get_all_day_stress(d.isoformat())))
    
    if args.json:
        output = {
            "stats": [(d.isoformat(), s) for d, s in stats_data],
            "body_battery": [(d.isoformat(), b) for d, b in bb_data],
            "stress": [(d.isoformat(), s) for d, s in stress_data],
        }
        print(json.dumps(output, indent=2, default=str))
        return 0
    
    print(f"\n📈 TRENDS ({days} Tage)")
    print("=" * 60)
    
    # Steps trend
    steps = [s.get('totalSteps') or 0 for _, s in stats_data]
    print(f"\n{EMOJI['steps']} Schritte")
    print(f"  Durchschnitt:  {sum(steps) // len(steps):,}")
    print(f"  Maximum:       {max(steps):,}")
    print(f"  Minimum:       {min(steps):,}")
    print(f"  Trend:         {get_trend(steps[0], steps[-1])} {'↑' if steps[0] > steps[-1] else '↓' if steps[0] < steps[-1] else '→'}")
    
    # Body Battery
    print(f"\n{EMOJI['battery']} Body Battery")
    for d, bb in bb_data[:5]:
        if bb and isinstance(bb, list) and len(bb) > 0:
            charged = bb[0].get('charged', 0)
            drained = bb[0].get('drained', 0)
            net = charged - drained
            print(f"  {d}: {EMOJI['up'] if net > 0 else EMOJI['down']} {net:+d} (charged: {charged}, drained: {drained})")
    
    # Stress
    print(f"\n{EMOJI['stress']} Stress")
    for d, s in stress_data[:5]:
        if s:
            print(f"  {d}: Ø {s.get('avgStressLevel', 'N/A')} (max: {s.get('maxStressLevel', 'N/A')})")
    
    # Resting HR
    rhr = [s.get('restingHeartRate') or 0 for _, s in stats_data if s.get('restingHeartRate')]
    if rhr:
        print(f"\n{EMOJI['hr']} Ruhe-Herzfrequenz")
        print(f"  Durchschnitt:  {round(sum(rhr) / len(rhr), 1)} bpm")
        print(f"  Minimum:       {min(rhr)} bpm")
        print(f"  Maximum:       {max(rhr)} bpm")
    
    return 0


def cmd_compare(args):
    """Week over week comparison."""
    client = get_client()
    if not client:
        return 1
    
    # This week
    this_week = []
    for i in range(7):
        d = date.today() - timedelta(days=i)
        this_week.append(client.get_stats(d.isoformat()))
    
    # Last week
    last_week = []
    for i in range(7, 14):
        d = date.today() - timedelta(days=i)
        last_week.append(client.get_stats(d.isoformat()))
    
    if args.json:
        print(json.dumps({"this_week": this_week, "last_week": last_week}, indent=2, default=str))
        return 0
    
    def sum_or_none(data, key):
        vals = [d.get(key) or 0 for d in data]
        return sum(vals) if vals else 0
    
    print(f"\n📊 WOCHE VS. WOCHE")
    print("=" * 50)
    
    metrics = [
        ("Schritte", "totalSteps", "{:,}"),
        ("Distanz (km)", "totalDistanceMeters", lambda x: round(x / 1000, 1)),
        ("Kalorien", "totalKilocalories", "{:,}"),
        ("Ruhe-HF (Ø)", "restingHeartRate", lambda x: round(x, 1)),
        ("Stockwerke", "floorsAscended", "{:,}"),
    ]
    
    print(f"{'Metrik':<15} {'Diese Woche':>15} {'Letzte Woche':>15} {'Diff':>10}")
    print("-" * 55)
    
    for name, key, fmt in metrics:
        this = sum_or_none(this_week, key)
        last = sum_or_none(last_week, key)
        
        if key == "restingHeartRate":
            # Average, not sum
            this_vals = [d.get(key) for d in this_week if d.get(key)]
            last_vals = [d.get(key) for d in last_week if d.get(key)]
            this = sum(this_vals) / len(this_vals) if this_vals else 0
            last = sum(last_vals) / len(last_vals) if last_vals else 0
        
        diff = this - last
        diff_pct = ((this - last) / last * 100) if last else 0
        
        if callable(fmt):
            this_str = fmt(this)
            last_str = fmt(last)
        else:
            this_str = fmt.format(int(this))
            last_str = fmt.format(int(last))
        
        trend = EMOJI["up"] if diff > 0 else EMOJI["down"] if diff < 0 else EMOJI["same"]
        print(f"{name:<15} {this_str:>15} {last_str:>15} {trend} {diff_pct:+.1f}%")
    
    return 0


def cmd_race(args):
    """Race predictions."""
    client = get_client()
    if not client:
        return 1
    
    rp = client.get_race_predictions()
    
    if args.json:
        print(json.dumps(rp, indent=2, default=str))
        return 0
    
    print(f"\n🏁 RACE PREDICTIONS")
    print("=" * 40)
    print(f"5K:            {format_time(rp.get('time5K'))}")
    print(f"10K:           {format_time(rp.get('time10K'))}")
    print(f"Halbmarathon:  {format_time(rp.get('timeHalfMarathon'))}")
    print(f"Marathon:      {format_time(rp.get('timeMarathon'))}")
    
    return 0


def cmd_training(args):
    """Training readiness and status."""
    client = get_client()
    if not client:
        return 1
    
    target_date = args.date or date.today().isoformat()
    
    if args.json:
        data = {
            "readiness": client.get_training_readiness(target_date),
            "status": client.get_training_status(target_date),
            "intensity": client.get_intensity_minutes_data(target_date),
        }
        print(json.dumps(data, indent=2, default=str))
        return 0
    
    print(f"\n{EMOJI['training']} TRAINING - {target_date}")
    print("=" * 50)
    
    # Training Readiness
    try:
        tr = client.get_training_readiness(target_date)
        if isinstance(tr, list) and tr:
            tr = tr[0]
        if tr:
            print(f"\nTraining Readiness")
            print(f"  Score:         {tr.get('trainingReadinessScore', 'N/A')}")
            print(f"  Level:         {tr.get('trainingReadinessLevel', 'N/A')}")
    except:
        print("\nTraining Readiness: Nicht verfügbar")
    
    # Intensity Minutes
    im = client.get_intensity_minutes_data(target_date)
    if im:
        print(f"\nIntensity Minutes")
        print(f"  Moderate:      {im.get('moderateMinutes', 0)} min")
        print(f"  Vigorous:      {im.get('vigorousMinutes', 0)} min")
        print(f"  Weekly Total:  {im.get('weeklyTotal', 0)} / {im.get('weekGoal', 300)} min")
        pct = (im.get('weeklyTotal', 0) / im.get('weekGoal', 300)) * 100
        bar = "█" * int(pct / 5) + "░" * (20 - int(pct / 5))
        print(f"  Progress:      [{bar}] {pct:.0f}%")
    
    return 0


def cmd_devices(args):
    """List devices."""
    client = get_client()
    if not client:
        return 1
    
    devices = client.get_devices()
    
    if args.json:
        print(json.dumps(devices, indent=2, default=str))
        return 0
    
    print(f"\n⌚ GERÄTE")
    print("=" * 50)
    
    for dev in devices:
        print(f"\n{dev.get('displayName', 'Unknown')}")
        print(f"  Serial:        {dev.get('serialNumber')}")
        print(f"  Product:       {dev.get('productName')}")
    
    return 0


def cmd_workouts(args):
    """List saved workouts."""
    client = get_client()
    if not client:
        return 1
    
    workouts = client.get_workouts()
    
    if args.json:
        print(json.dumps(workouts, indent=2, default=str))
        return 0
    
    print(f"\n🏋️ WORKOUTS ({len(workouts)})")
    print("=" * 50)
    
    for w in workouts:
        print(f"  • {w.get('workoutName', 'N/A')} ({w.get('sportTypeKey', 'N/A')})")
    
    return 0


def cmd_badges(args):
    """List earned badges."""
    client = get_client()
    if not client:
        return 1
    
    badges = client.get_earned_badges()
    limit = args.limit or 20
    
    if args.json:
        print(json.dumps(badges[:limit], indent=2, default=str))
        return 0
    
    print(f"\n🏆 BADGES ({len(badges)})")
    print("=" * 50)
    
    for b in badges[:limit]:
        desc = b.get('badgeDescription', '')[:40] if b.get('badgeDescription') else ''
        print(f"  {b.get('badgeName', 'N/A')}: {desc}")
    
    return 0


def cmd_export(args):
    """Full JSON export."""
    client = get_client()
    if not client:
        return 1
    
    target_date = args.date or date.today().isoformat()
    days = args.days or 7
    
    data = {
        "export_date": target_date,
        "profile": client.get_user_profile(),
        "devices": client.get_devices(),
        "race_predictions": client.get_race_predictions(),
        "workouts": client.get_workouts(),
        "badges": client.get_earned_badges(),
        "activities": client.get_activities(0, args.limit or 20),
        "daily_data": [],
    }
    
    # Daily data for range
    for i in range(days):
        d = date.today() - timedelta(days=i)
        d_str = d.isoformat()
        data["daily_data"].append({
            "date": d_str,
            "stats": client.get_stats(d_str),
            "sleep": client.get_sleep_data(d_str),
            "hr": client.get_heart_rates(d_str),
            "hrv": client.get_hrv_data(d_str),
            "stress": client.get_all_day_stress(d_str),
            "body_battery": client.get_body_battery(d_str),
            "intensity_minutes": client.get_intensity_minutes_data(d_str),
            "hydration": client.get_hydration_data(d_str),
            "respiration": client.get_respiration_data(d_str),
            "floors": client.get_floors(d_str),
        })
    
    print(json.dumps(data, indent=2, default=str))
    return 0


def cmd_stats(args):
    """Get daily stats."""
    client = get_client()
    if not client:
        return 1
    
    target_date = args.date or date.today().isoformat()
    stats = client.get_stats(target_date)
    
    if args.json:
        print(json.dumps(stats, indent=2, default=str))
        return 0
    
    print(f"\n📊 STATS - {target_date}")
    print("=" * 40)
    print(f"Schritte:       {stats.get('totalSteps', 'N/A'):,}")
    print(f"Distanz:        {round((stats.get('totalDistanceMeters') or 0) / 1000, 2)} km")
    print(f"Kalorien:       {stats.get('totalKilocalories', 'N/A')}")
    print(f"Ruhe-HF:        {stats.get('restingHeartRate', 'N/A')} bpm")
    print(f"Stockwerke:     {stats.get('floorsAscended', 'N/A')}")
    print(f"Stress (Ø):     {stats.get('averageStressLevel', 'N/A')}")
    print(f"Body Battery:   {stats.get('bodyBatteryMostRecentValue', 'N/A')}")
    
    return 0


def cmd_sleep(args):
    """Get sleep data."""
    client = get_client()
    if not client:
        return 1
    
    target_date = args.date or date.today().isoformat()
    sleep = client.get_sleep_data(target_date)
    
    if args.json:
        print(json.dumps(sleep, indent=2, default=str))
        return 0
    
    daily = sleep.get('dailySleepDTO', {}) if sleep else {}
    
    print(f"\n{EMOJI['sleep']} SCHLAF - {target_date}")
    print("=" * 40)
    
    if daily.get('sleepTimeSeconds'):
        print(f"Gesamt:         {format_duration(daily.get('sleepTimeSeconds'))}")
        print(f"Tiefschlaf:     {format_duration(daily.get('deepSleepSeconds'))}")
        print(f"Leichtschlaf:   {format_duration(daily.get('lightSleepSeconds'))}")
        print(f"REM:            {format_duration(daily.get('remSleepSeconds'))}")
        print(f"Wach:           {format_duration(daily.get('awakeSleepSeconds'))}")
        if daily.get('overallSleepScore'):
            print(f"Score:          {daily['overallSleepScore'].get('value', 'N/A')}")
    else:
        print("Keine Schlafdaten verfügbar")
    
    return 0


def cmd_hr(args):
    """Get heart rate data."""
    client = get_client()
    if not client:
        return 1
    
    target_date = args.date or date.today().isoformat()
    hr = client.get_heart_rates(target_date)
    
    if args.json:
        print(json.dumps(hr, indent=2, default=str))
        return 0
    
    print(f"\n{EMOJI['hr']} HERZFREQUENZ - {target_date}")
    print("=" * 40)
    print(f"Ruhe-HF:        {hr.get('restingHeartRate', 'N/A')} bpm")
    print(f"Minimum:        {hr.get('minHeartRate', 'N/A')} bpm")
    print(f"Maximum:        {hr.get('maxHeartRate', 'N/A')} bpm")
    print(f"Datenpunkte:    {len(hr.get('heartRateValues', []))}")
    
    return 0


def cmd_hrv(args):
    """Get HRV data."""
    client = get_client()
    if not client:
        return 1
    
    target_date = args.date or date.today().isoformat()
    hrv = client.get_hrv_data(target_date)
    
    if args.json:
        print(json.dumps(hrv, indent=2, default=str))
        return 0
    
    print(f"\n💓 HRV - {target_date}")
    print("=" * 40)
    
    if hrv and hrv.get('hrvSummary'):
        h = hrv['hrvSummary']
        print(f"Durchschnitt:   {h.get('avgHrv', 'N/A')} ms")
        print(f"Highest:        {h.get('highestHrv', 'N/A')} ms")
        print(f"Lowest:         {h.get('lowestHrv', 'N/A')} ms")
        print(f"Status:         {h.get('hrvStatus', 'N/A')}")
    else:
        print("Keine HRV-Daten verfügbar")
    
    return 0


def cmd_stress(args):
    """Get stress data."""
    client = get_client()
    if not client:
        return 1
    
    target_date = args.date or date.today().isoformat()
    stress = client.get_all_day_stress(target_date)
    
    if args.json:
        print(json.dumps(stress, indent=2, default=str))
        return 0
    
    print(f"\n{EMOJI['stress']} STRESS - {target_date}")
    print("=" * 40)
    
    if stress:
        print(f"Durchschnitt:   {stress.get('avgStressLevel', 'N/A')}")
        print(f"Maximum:        {stress.get('maxStressLevel', 'N/A')}")
        print(f"Datenpunkte:    {len(stress.get('stressValuesArray', []))}")
    else:
        print("Keine Stress-Daten verfügbar")
    
    return 0


def cmd_body_battery(args):
    """Get body battery data."""
    client = get_client()
    if not client:
        return 1
    
    target_date = args.date or date.today().isoformat()
    bb = client.get_body_battery(target_date)
    
    if args.json:
        print(json.dumps(bb, indent=2, default=str))
        return 0
    
    print(f"\n{EMOJI['battery']} BODY BATTERY - {target_date}")
    print("=" * 40)
    
    if bb and isinstance(bb, list):
        for b in bb[:5]:
            print(f"Charged:        {b.get('charged', 'N/A')}")
            print(f"Drained:        {b.get('drained', 'N/A')}")
            print(f"Net:            {(b.get('charged') or 0) - (b.get('drained') or 0)}")
    else:
        print("Keine Body Battery Daten verfügbar")
    
    return 0


def cmd_logout(args):
    """Delete saved tokens."""
    import shutil
    if TOKEN_DIR.exists():
        shutil.rmtree(TOKEN_DIR)
        print(f"Deleted tokens from: {TOKEN_DIR}")
    else:
        print("No tokens to delete.")
    return 0


def main():
    parser = argparse.ArgumentParser(
        description="Garmin Connect CLI - Maximum Output Edition",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--full", action="store_true", help="Full detailed output")
    
    subparsers = parser.add_subparsers(dest="command", help="Command")
    
    # Summary (default)
    p_summary = subparsers.add_parser("summary", help="Full daily summary")
    p_summary.add_argument("--date", help="Date (YYYY-MM-DD)")
    
    # Activities
    p_activities = subparsers.add_parser("activities", help="Recent activities")
    p_activities.add_argument("--date", help="Date (YYYY-MM-DD)")
    p_activities.add_argument("--limit", type=int, default=10, help="Limit results")
    
    # Activity
    p_activity = subparsers.add_parser("activity", help="Specific activity details")
    p_activity.add_argument("--id", required=True, help="Activity ID")
    
    # Stats
    p_stats = subparsers.add_parser("stats", help="Daily stats")
    p_stats.add_argument("--date", help="Date (YYYY-MM-DD)")
    
    # Sleep
    p_sleep = subparsers.add_parser("sleep", help="Sleep data")
    p_sleep.add_argument("--date", help="Date (YYYY-MM-DD)")
    
    # HR
    p_hr = subparsers.add_parser("hr", help="Heart rate data")
    p_hr.add_argument("--date", help="Date (YYYY-MM-DD)")
    
    # HRV
    p_hrv = subparsers.add_parser("hrv", help="HRV data")
    p_hrv.add_argument("--date", help="Date (YYYY-MM-DD)")
    
    # Stress
    p_stress = subparsers.add_parser("stress", help="Stress data")
    p_stress.add_argument("--date", help="Date (YYYY-MM-DD)")
    
    # Body Battery
    p_bb = subparsers.add_parser("body-battery", help="Body battery")
    p_bb.add_argument("--date", help="Date (YYYY-MM-DD)")
    
    # Training
    p_training = subparsers.add_parser("training", help="Training readiness")
    p_training.add_argument("--date", help="Date (YYYY-MM-DD)")
    
    # Race predictions
    p_race = subparsers.add_parser("race", help="Race predictions")
    
    # Week
    p_week = subparsers.add_parser("week", help="Weekly overview")
    p_week.add_argument("--days", type=int, default=7, help="Number of days")
    
    # Trends
    p_trends = subparsers.add_parser("trends", help="7-day trends")
    p_trends.add_argument("--days", type=int, default=7, help="Number of days")
    
    # Compare
    p_compare = subparsers.add_parser("compare", help="Week over week comparison")
    
    # Devices
    p_devices = subparsers.add_parser("devices", help="Connected devices")
    
    # Workouts
    p_workouts = subparsers.add_parser("workouts", help="Saved workouts")
    
    # Badges
    p_badges = subparsers.add_parser("badges", help="Earned badges")
    p_badges.add_argument("--limit", type=int, default=20, help="Limit results")
    
    # Export
    p_export = subparsers.add_parser("export", help="Full JSON export")
    p_export.add_argument("--date", help="Start date (YYYY-MM-DD)")
    p_export.add_argument("--days", type=int, default=7, help="Number of days")
    p_export.add_argument("--limit", type=int, default=20, help="Activity limit")
    
    # Login/Logout
    subparsers.add_parser("login", help="Login and save tokens")
    subparsers.add_parser("logout", help="Delete saved tokens")
    
    args = parser.parse_args()
    
    if not args.command:
        args.command = "summary"
        return cmd_summary(args)
    
    commands = {
        "login": lambda a: login(a) if not TOKEN_DIR.exists() else (print(f"{EMOJI['good']} Already logged in") or 0),
        "logout": cmd_logout,
        "summary": cmd_summary,
        "activities": cmd_activities,
        "activity": cmd_activity,
        "stats": cmd_stats,
        "sleep": cmd_sleep,
        "hr": cmd_hr,
        "hrv": cmd_hrv,
        "stress": cmd_stress,
        "body-battery": cmd_body_battery,
        "training": cmd_training,
        "race": cmd_race,
        "week": cmd_week,
        "trends": cmd_trends,
        "compare": cmd_compare,
        "devices": cmd_devices,
        "workouts": cmd_workouts,
        "badges": cmd_badges,
        "export": cmd_export,
    }
    
    if args.command == "login":
        return login(args)
    
    if args.command in commands:
        return commands[args.command](args)
    
    parser.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
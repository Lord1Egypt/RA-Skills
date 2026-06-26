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
Fulcra Daily Health Insights

Comprehensive cross-domain health analysis using Fulcra API. Pulls sleep, HRV,
heart rate, nutrition, calendar, and workout data to generate actionable health
insights with correlation analysis across multiple biometric domains.

Key Features:
- Multi-domain correlation (sleep ↔ HRV ↔ training load ↔ stress)
- Change detection (only report new/significant changes)
- Actionable suggestions based on data patterns
- Phantom workout detection (left-running Apple Watch workouts)
- Nutrition analysis with logging completeness detection
- Meeting load vs recovery correlation

Built with Fulcra for automated health monitoring.
"""

import json, os, shlex, subprocess, sys
from datetime import datetime, timezone, timedelta
from collections import defaultdict

# Configurable state path via environment variables
STATE_DIR = os.environ.get("FULCRA_SKILL_STATE_DIR", ".fulcra-state")
STATE_PATH = os.path.join(STATE_DIR, "last_report_state.json")

def load_last_state():
    """Load the last reported state for change detection."""
    try:
        with open(STATE_PATH, 'r') as f:
            return json.load(f)
    except:
        return {}

def save_state(state):
    """Persist current state for next run's change detection."""
    os.makedirs(os.path.dirname(STATE_PATH), exist_ok=True)
    with open(STATE_PATH, 'w') as f:
        json.dump(state, f, indent=2, default=str)

def diff_insights(current_output, last_state):
    """Compare current data to last report. Return only what's new/changed."""
    changes = []
    
    last_sleep = last_state.get('last_sleep', {})
    last_workouts = set(last_state.get('workout_ids', []))
    last_hrv = last_state.get('last_hrv_avg')
    last_rhr = last_state.get('last_rhr_avg')
    last_nutrition_date = last_state.get('last_nutrition_date')
    last_nutrition_cal = last_state.get('last_nutrition_cal', 0)
    
    # New sleep data?
    sleep = current_output.get('sleep', [])
    if sleep:
        latest = sleep[-1]
        if latest['date'] != last_sleep.get('date') or abs(latest['total_hours'] - last_sleep.get('total_hours', 0)) > 0.3:
            changes.append(('sleep', f"🛌 Sleep update: {latest['total_hours']}h (REM {latest['rem_pct']}%, Deep {latest['deep_pct']}%)"))
    
    # New workouts?
    workouts = current_output.get('workouts', [])
    for w in workouts:
        wid = w.get('start_time', '')
        if wid and wid not in last_workouts:
            phantom = " ⚠️ PHANTOM — likely left running" if w['is_phantom'] else ""
            dist = f", {w['distance_mi']}mi" if w.get('distance_mi', 0) > 0 else ""
            changes.append(('workout', f"🏋️ New workout: {w['activity']} — {w['duration_min']:.0f}min, avgHR {w['hr_avg']}, {w['active_cal']}cal{dist}{phantom}"))
    
    # HRV shift? (percentage-based: 10% of last value, minimum 3ms)
    hrv_daily = current_output.get('hrv_daily', {})
    if hrv_daily:
        latest_hrv = hrv_daily[max(hrv_daily.keys())]['avg']
        if last_hrv is not None:
            hrv_threshold = max(3, last_hrv * 0.10)
            if abs(latest_hrv - last_hrv) >= hrv_threshold:
                direction = "⬆️" if latest_hrv > last_hrv else "⬇️"
                pct = abs(latest_hrv - last_hrv) / last_hrv * 100
                changes.append(('hrv', f"❤️ HRV shifted {direction} {last_hrv}→{latest_hrv}ms ({pct:.0f}%)"))
        else:
            changes.append(('hrv', f"❤️ HRV: {latest_hrv}ms"))
    
    # RHR shift? (percentage-based: 3% of last value, minimum 2bpm)
    rhr_daily = current_output.get('rhr_daily', {})
    if rhr_daily:
        latest_rhr = rhr_daily[max(rhr_daily.keys())]['avg']
        if last_rhr is not None:
            rhr_threshold = max(2, last_rhr * 0.03)
            if abs(latest_rhr - last_rhr) >= rhr_threshold:
                direction = "⬆️" if latest_rhr > last_rhr else "⬇️"
                changes.append(('rhr', f"💓 RHR shifted {direction} {last_rhr}→{latest_rhr}bpm"))
    
    # Nutrition updated? (catches late-day logging)
    nutrition = current_output.get('nutrition', {})
    cal_data = nutrition.get('Calories', {})
    if cal_data:
        latest_nutr_date = max(cal_data.keys())
        latest_cal = cal_data[latest_nutr_date]['avg']
        if latest_nutr_date != last_nutrition_date or (latest_cal > 500 and last_nutrition_cal < 500):
            protein_data = nutrition.get('Protein', {})
            protein = protein_data.get(latest_nutr_date, {}).get('avg', 0)
            changes.append(('nutrition', f"🍽️ Nutrition ({latest_nutr_date}): {latest_cal:.0f} cal, {protein:.0f}g protein"))
    
    # Build new state snapshot for next comparison
    hrv_all = [v['avg'] for v in hrv_daily.values()] if hrv_daily else []
    rhr_all = [v['avg'] for v in rhr_daily.values()] if rhr_daily else []
    sleep_all = [s['total_hours'] for s in sleep] if sleep else []
    
    new_state = {
        'timestamp': datetime.now(timezone.utc).isoformat(),
        'last_sleep': sleep[-1] if sleep else {},
        'workout_ids': [w.get('start_time', '') for w in workouts],
        'last_hrv_avg': hrv_daily[max(hrv_daily.keys())]['avg'] if hrv_daily else None,
        'baselines': {
            'hrv_7d_avg': round(sum(hrv_all) / len(hrv_all), 1) if hrv_all else None,
            'rhr_7d_avg': round(sum(rhr_all) / len(rhr_all), 1) if rhr_all else None,
            'sleep_7d_avg': round(sum(sleep_all) / len(sleep_all), 1) if sleep_all else None,
        },
        'last_rhr_avg': rhr_daily[max(rhr_daily.keys())]['avg'] if rhr_daily else None,
        'last_nutrition_date': max(cal_data.keys()) if cal_data else None,
        'last_nutrition_cal': cal_data[max(cal_data.keys())]['avg'] if cal_data else 0,
        'last_insights': [c[1] for c in changes],
    }
    
    return changes, new_state

def get_api():
    """Initialize Fulcra API client using Fulcra CLI-managed auth."""
    from fulcra_api.core import FulcraAPI
    api = FulcraAPI()
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
    setattr(api, "fulcra_cached_" + "access_" + "token", proc.stdout.strip())
    setattr(
        api,
        "fulcra_cached_" + "access_" + "token_expiration",
        datetime.now(timezone.utc) + timedelta(hours=1),
    )
    return api

def safe_samples(api, start, end, metric):
    """Fetch metric_samples with error handling, return list of dicts."""
    try:
        data = api.metric_samples(start, end, metric)
        return data if isinstance(data, list) else []
    except:
        return []

def safe_df_to_records(df_or_list):
    """Convert pandas DataFrame or list to list of dicts safely."""
    if df_or_list is None:
        return []
    if hasattr(df_or_list, 'to_dict'):
        return df_or_list.to_dict('records')
    if isinstance(df_or_list, list):
        return df_or_list
    return []

def get_workouts(api, start, end):
    """Fetch Apple Watch workouts with phantom detection and parsed statistics."""
    try:
        raw = api.apple_workouts(start, end)
        records = safe_df_to_records(raw)
    except:
        return []
    
    workouts = []
    for w in records:
        stats = w.get('all_statistics', {})
        hr_stats = stats.get('HKQuantityTypeIdentifierHeartRate', {})
        active_cal = stats.get('HKQuantityTypeIdentifierActiveEnergyBurned', {})
        distance = stats.get('HKQuantityTypeIdentifierDistanceWalkingRunning', {})
        
        duration_sec = w.get('duration', 0)
        activity = w.get('workout_activity_type', 'unknown')
        start_date = str(w.get('start_date', ''))
        date = start_date[:10]
        
        # Detect phantom workouts (indoor + abnormally long duration)
        extras = w.get('extras', {})
        is_indoor = extras.get('HKIndoorWorkout') == 1
        is_phantom = is_indoor and duration_sec > 7200  # >2h indoor = suspicious
        
        workouts.append({
            'date': date,
            'activity': activity,
            'duration_min': round(duration_sec / 60, 1),
            'hr_avg': round(hr_stats.get('average', 0), 1),
            'hr_max': hr_stats.get('maximum', 0),
            'hr_min': hr_stats.get('minimum', 0),
            'active_cal': round(active_cal.get('sum', 0)),
            'distance_mi': round(distance.get('sum', 0), 2) if distance else 0,
            'is_indoor': is_indoor,
            'is_phantom': is_phantom,
            'start_time': start_date,
        })
    return workouts

def parse_sleep(api, start, end):
    """Parse sleep_agg data into per-night summaries with stage analysis."""
    raw = api.sleep_agg(start, end)
    records = safe_df_to_records(raw)
    
    # Apple HealthKit sleep stage codes: 2=Deep, 3=Core(Light), 4=REM, 5=Awake
    stage_names = {1: 'InBed', 2: 'Deep', 3: 'Core', 4: 'REM', 5: 'Awake'}
    by_date = defaultdict(dict)
    
    for r in records:
        ts = r.get('period_start_time', '')
        date = str(ts)[:10]
        stage = stage_names.get(r.get('value'), 'unknown')
        hours = r.get('sum_ms', 0) / 3600000
        by_date[date][stage] = hours
    
    nights = []
    for date in sorted(by_date):
        d = by_date[date]
        total = sum(v for k, v in d.items() if k not in ('Awake', 'InBed', 'unknown'))
        nights.append({
            'date': date,
            'total_hours': round(total, 1),
            'rem_hours': round(d.get('REM', 0), 1),
            'deep_hours': round(d.get('Deep', 0), 1),
            'core_hours': round(d.get('Core', 0), 1),
            'awake_hours': round(d.get('Awake', 0), 1),
            'rem_pct': round(d.get('REM', 0) / total * 100 if total else 0),
            'deep_pct': round(d.get('Deep', 0) / total * 100 if total else 0),
        })
    return nights

def parse_metric_daily(samples):
    """Aggregate metric samples into daily avg/min/max statistics."""
    by_date = defaultdict(list)
    for s in samples:
        ts = s.get('start_date') or s.get('start_time') or ''
        date = str(ts)[:10]
        val = s.get('value')
        if val is not None:
            by_date[date].append(float(val))
    
    result = {}
    for date, vals in sorted(by_date.items()):
        result[date] = {
            'avg': round(sum(vals) / len(vals), 1),
            'min': round(min(vals), 1),
            'max': round(max(vals), 1),
            'count': len(vals),
        }
    return result

def get_calendar_context(api, start, end):
    """Get meeting count and types per day, filtering out calendar blocks."""
    events = api.calendar_events(start, end)
    events = events if isinstance(events, list) else []
    
    by_date = defaultdict(list)
    for e in events:
        title = e.get('title', '')
        start_date = str(e.get('start_date', ''))[:10]
        has_attendees = bool(e.get('participants'))
        
        # Skip common calendar management blocks
        if title.lower() in ('busy', 'admin time', 'blocked') or 'decompress' in title.lower():
            continue
            
        by_date[start_date].append({
            'title': title,
            'has_attendees': has_attendees,
        })
    
    result = {}
    for date, meetings in by_date.items():
        external = [m for m in meetings if m['has_attendees']]
        result[date] = {
            'total_events': len(meetings),
            'external_meetings': len(external),
        }
    return result

def get_nutrition(api, start, end):
    """Get nutrition data across key macronutrients and micronutrients."""
    metrics = ['CaloriesConsumed', 'DietaryProteinConsumed', 'TotalFatConsumed', 
               'DietaryCarbohydratesConsumed', 'DietaryFiberConsumed', 'DietarySugarConsumed']
    nutrition = {}
    for m in metrics:
        samples = safe_samples(api, start, end, m)
        daily = parse_metric_daily(samples)
        short_name = m.replace('Dietary', '').replace('Consumed', '').replace('Total', '')
        nutrition[short_name] = daily
    return nutrition

def generate_insights(sleep, hr_daily, hrv_daily, rhr_daily, steps_daily, 
                      nutrition, calendar, today_str, yesterday_str,
                      workouts=None):
    """Cross-correlate all data and generate actionable health insights."""
    insights = []
    suggestions = []
    
    # --- SLEEP ANALYSIS ---
    today_sleep = next((s for s in sleep if s['date'] == today_str), None)
    yesterday_sleep = next((s for s in sleep if s['date'] == yesterday_str), None)
    
    if today_sleep:
        total = today_sleep['total_hours']
        rem = today_sleep['rem_hours']
        deep = today_sleep['deep_hours']
        rem_pct = today_sleep['rem_pct']
        deep_pct = today_sleep['deep_pct']
        
        if total < 5:
            insights.append(f"⚠️ Short sleep: {total}h. Cognitive performance drops ~25% under 5h.")
            suggestions.append("Consider a 20-min nap before 2 PM if schedule allows. Avoid complex decisions after 3 PM.")
        
        if rem_pct >= 20:
            insights.append(f"✅ REM excellent: {rem}h ({rem_pct}%). Good for emotional processing and memory consolidation.")
        elif rem_pct < 15:
            insights.append(f"⚠️ REM low: {rem}h ({rem_pct}%). Target is 20-25%. Affects emotional regulation and learning.")
            suggestions.append("REM occurs more in later sleep cycles. Going to bed earlier won't help — sleeping longer will. Alcohol and THC suppress REM.")
        
        if deep_pct < 10:
            insights.append(f"⚠️ Deep sleep very low: {deep}h ({deep_pct}%). Physical recovery compromised.")
            suggestions.append("Deep sleep is front-loaded in the night. Cool room (65-68°F) and magnesium before bed can help.")
        elif deep_pct >= 20:
            insights.append(f"✅ Deep sleep strong: {deep}h ({deep_pct}%). Good physical recovery.")
        
        # Sleep trend analysis
        if yesterday_sleep and today_sleep:
            delta = total - yesterday_sleep['total_hours']
            if abs(delta) > 1.5:
                direction = "up" if delta > 0 else "down"
                insights.append(f"📊 Sleep {direction} {abs(delta):.1f}h from yesterday ({yesterday_sleep['total_hours']}h → {total}h)")
    
    # --- HRV + MEETING LOAD CORRELATION ---
    today_hrv = hrv_daily.get(today_str, {})
    today_cal = calendar.get(today_str, {})
    
    if today_hrv:
        hrv_avg = today_hrv['avg']
        if hrv_avg < 25:
            insights.append(f"🔴 HRV very low: {hrv_avg}ms. High stress / poor recovery. Consider lighter day if possible.")
            suggestions.append("Prioritize parasympathetic activation: box breathing (4-4-4-4) between meetings, skip intense training today.")
        elif hrv_avg < 35:
            insights.append(f"🟡 HRV moderate: {hrv_avg}ms. Manageable but not fully recovered.")
    
    if today_cal.get('external_meetings', 0) >= 3:
        meeting_count = today_cal['external_meetings']
        insights.append(f"📅 Heavy meeting day: {meeting_count} external meetings.")
        if today_hrv and today_hrv.get('avg', 50) < 30:
            suggestions.append(f"Low HRV + {meeting_count} meetings = high cognitive drain. Block 15 min between calls for recovery. Front-load important decisions.")
        if today_sleep and today_sleep['total_hours'] < 5.5:
            suggestions.append(f"Short sleep ({today_sleep['total_hours']}h) + heavy meetings. Protein-rich lunch critical — aim for 40g+ to avoid afternoon crash.")
    
    # --- NUTRITION ANALYSIS ---
    yesterday_nutrition = {}
    for metric, daily in nutrition.items():
        if yesterday_str in daily:
            yesterday_nutrition[metric] = daily[yesterday_str]['avg']
    
    calories = yesterday_nutrition.get('Calories', 0)
    protein = yesterday_nutrition.get('Protein', 0)
    
    # Detect likely incomplete logging vs actual low intake
    likely_incomplete = calories > 0 and calories < 500
    
    if likely_incomplete:
        insights.append(f"📝 Yesterday's nutrition looks incomplete ({calories:.0f} cal / {protein:.0f}g protein) — likely logged late or partially.")
    else:
        if protein > 0:
            protein_target = 150  # Configurable target
            if protein < protein_target * 0.85:  # 85% of target
                insights.append(f"⚠️ Yesterday's protein: {protein:.0f}g (target: ~{protein_target}g)")
                suggestions.append(f"You're {protein_target - protein:.0f}g short on protein. Add a protein shake or extra serving today.")
            else:
                insights.append(f"✅ Protein on track: {protein:.0f}g yesterday")
        
        if calories > 0:
            if calories > 3000:
                insights.append(f"📊 High calorie day yesterday: {calories:.0f} cal. Check if data entry error.")
            elif calories < 1200:
                insights.append(f"⚠️ Very low calories yesterday: {calories:.0f} cal. Under-fueling affects recovery and HRV.")
                suggestions.append("Chronic under-eating can impact HRV and sleep quality. Focus on nutrient-dense foods if appetite is suppressed.")
    
    # --- WORKOUT ANALYSIS ---
    if workouts:
        today_workouts = [w for w in workouts if w['date'] == today_str]
        yesterday_workouts = [w for w in workouts if w['date'] == yesterday_str]
        
        for w in today_workouts + yesterday_workouts:
            day_label = "Today" if w['date'] == today_str else "Yesterday"
            
            if w['is_phantom']:
                insights.append(f"⚠️ {day_label}: {w['activity']} workout ran {w['duration_min']:.0f} min — likely left running. {w['active_cal']} phantom active calories.")
                end_suggestion = f"End the {w['activity']} workout on your Apple Watch to fix calorie data."
                if end_suggestion not in suggestions:
                    suggestions.append(end_suggestion)
            else:
                hr_zone = ""
                if w['hr_max'] >= 140:
                    hr_zone = f" (peak HR {w['hr_max']} — solid zone 4+ effort)"
                elif w['hr_max'] >= 120:
                    hr_zone = f" (peak HR {w['hr_max']} — moderate effort)"
                
                dist = f", {w['distance_mi']} mi" if w['distance_mi'] > 0 else ""
                insights.append(f"🏋️ {day_label}: {w['activity']} — {w['duration_min']:.0f} min, avg HR {w['hr_avg']}, {w['active_cal']} cal{dist}{hr_zone}")
        
        # Training load analysis: total active calories from real workouts
        recent_workouts = [w for w in workouts if not w['is_phantom']]
        if recent_workouts:
            total_active = sum(w['active_cal'] for w in recent_workouts)
            workout_days = len(set(w['date'] for w in recent_workouts))
            if total_active > 1500 and today_hrv and today_hrv.get('avg', 50) < 30:
                suggestions.append(f"High training load ({total_active} active cal across {workout_days} days) + low HRV = recovery deficit. Consider a lighter day.")
    
    # --- RESTING HEART RATE TRENDS ---
    if rhr_daily:
        rhr_vals = [v['avg'] for v in rhr_daily.values()]
        if len(rhr_vals) >= 3:
            recent = sum(rhr_vals[-3:]) / 3
            older = sum(rhr_vals[:3]) / min(3, len(rhr_vals))
            if recent < older - 2:
                insights.append(f"✅ RHR trending down ({older:.0f} → {recent:.0f} bpm). Cardiovascular adaptation improving.")
            elif recent > older + 3:
                insights.append(f"⚠️ RHR trending up ({older:.0f} → {recent:.0f} bpm). Could indicate overtraining, illness, or stress accumulation.")
                suggestions.append("Rising RHR + low HRV = recovery deficit. Consider a deload day or swap training for walking/yoga.")
    
    # --- ACTIVITY SUMMARY ---
    today_steps = steps_daily.get(today_str, {})
    if today_steps and today_steps.get('avg', 0) > 0:
        insights.append(f"🚶 Steps so far today: ~{int(today_steps['max'])} (from {today_steps['count']} readings)")
    
    # --- DEFAULT SUGGESTIONS ---
    if not suggestions:
        suggestions.append("No red flags today. Maintain current protocol.")
    
    return insights, suggestions

def main():
    """Main function with CLI argument parsing and output formatting."""
    import argparse
    parser = argparse.ArgumentParser(description="Fulcra daily health insights generator")
    parser.add_argument("--days", type=int, default=7, help="Days of history to pull")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--diff", action="store_true", help="Only show changes since last run")
    parser.add_argument("--full", action="store_true", help="Force full report (ignore diff state)")
    args = parser.parse_args()
    
    api = get_api()
    now = datetime.now(timezone.utc)
    start = (now - timedelta(days=args.days)).isoformat()
    end = now.isoformat()
    
    # Today/yesterday in Eastern Time (adjust timezone as needed)
    et_now = now - timedelta(hours=5)
    today_str = et_now.strftime('%Y-%m-%d')
    yesterday_str = (et_now - timedelta(days=1)).strftime('%Y-%m-%d')
    
    # Fetch all data sources
    sleep = parse_sleep(api, start, end)
    
    hr_samples = safe_samples(api, start, end, 'HeartRate')
    hr_daily = parse_metric_daily(hr_samples)
    
    hrv_samples = safe_samples(api, start, end, 'HeartRateVariabilitySDNN')
    hrv_daily = parse_metric_daily(hrv_samples)
    
    rhr_samples = safe_samples(api, start, end, 'RestingHeartRate')
    rhr_daily = parse_metric_daily(rhr_samples)
    
    step_samples = safe_samples(api, start, end, 'StepCount')
    steps_daily = parse_metric_daily(step_samples)
    
    nutrition = get_nutrition(api, start, end)
    calendar = get_calendar_context(api, start, end)
    workouts = get_workouts(api, start, end)
    
    # Generate cross-domain insights
    insights, suggestions = generate_insights(
        sleep, hr_daily, hrv_daily, rhr_daily, steps_daily,
        nutrition, calendar, today_str, yesterday_str,
        workouts=workouts
    )
    
    output = {
        'generated_at': now.isoformat(),
        'today': today_str,
        'sleep': sleep,
        'hrv_daily': hrv_daily,
        'rhr_daily': rhr_daily,
        'hr_daily': hr_daily,
        'steps_daily': steps_daily,
        'nutrition': nutrition,
        'calendar': calendar,
        'workouts': workouts,
        'insights': insights,
        'suggestions': suggestions,
    }
    
    # Diff mode: compare to last run, only output changes
    if args.diff and not args.full:
        last_state = load_last_state()
        changes, new_state = diff_insights(output, last_state)
        save_state(new_state)
        
        if args.json:
            print(json.dumps({'changes': [c[1] for c in changes], 'has_changes': bool(changes)}, indent=2))
        elif changes:
            print(f"📊 Health Update — {today_str}")
            for _, msg in changes:
                print(f"  {msg}")
            # Include relevant suggestions for changed categories
            change_cats = set(c[0] for c in changes)
            relevant_suggestions = []
            if 'sleep' in change_cats:
                relevant_suggestions.extend([s for s in suggestions if any(k in s.lower() for k in ['sleep', 'deep', 'rem', 'nap', 'magnesium'])])
            if 'workout' in change_cats:
                relevant_suggestions.extend([s for s in suggestions if any(k in s.lower() for k in ['workout', 'training', 'deload'])])
            if 'nutrition' in change_cats:
                relevant_suggestions.extend([s for s in suggestions if any(k in s.lower() for k in ['protein', 'calor', 'eating', 'nutrient'])])
            if 'hrv' in change_cats:
                relevant_suggestions.extend([s for s in suggestions if any(k in s.lower() for k in ['hrv', 'recovery', 'breathing'])])
            
            # Deduplicate and display relevant suggestions
            seen = set()
            for s in relevant_suggestions:
                if s not in seen:
                    seen.add(s)
                    print(f"  → {s}")
        else:
            print("NO_CHANGES")
        return
    
    # Full mode (also saves state for future diffs)
    changes, new_state = diff_insights(output, {})
    save_state(new_state)
    
    if args.json:
        print(json.dumps(output, indent=2, default=str))
    else:
        print(f"📊 Health Insights for {today_str}")
        print(f"{'='*50}")
        print()
        
        if insights:
            print("📋 FINDINGS:")
            for i in insights:
                print(f"  {i}")
        print()
        
        if suggestions:
            print("💡 SUGGESTIONS:")
            for s in suggestions:
                print(f"  → {s}")
        print()
        
        # Workout summary
        if workouts:
            print("🏋️ WORKOUTS (last 7d):")
            for w in workouts:
                phantom = " ⚠️ PHANTOM" if w['is_phantom'] else ""
                dist = f", {w['distance_mi']}mi" if w['distance_mi'] > 0 else ""
                print(f"  {w['date']} {w['activity']}: {w['duration_min']:.0f}min, avgHR {w['hr_avg']}, {w['active_cal']}cal{dist}{phantom}")
            print()
        
        # Raw data summary
        if sleep:
            last = sleep[-1]
            print(f"🛌 Last night: {last['total_hours']}h (REM {last['rem_hours']}h/{last['rem_pct']}%, Deep {last['deep_hours']}h/{last['deep_pct']}%)")
        if hrv_daily:
            latest_date = max(hrv_daily.keys())
            print(f"❤️ HRV ({latest_date}): {hrv_daily[latest_date]['avg']}ms")
        if rhr_daily:
            latest_date = max(rhr_daily.keys())
            print(f"💓 RHR ({latest_date}): {rhr_daily[latest_date]['avg']}bpm")

if __name__ == "__main__":
    main()

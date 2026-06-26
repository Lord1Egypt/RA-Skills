#!/usr/bin/env python3
"""
Fetch Concept2 Logbook workouts via API with pulse zone analysis and trends.
Usage: python fetch_workouts.py --token <API_TOKEN> [options]
"""

import argparse
import json
import sys
import math
from datetime import datetime, timedelta
from collections import defaultdict

try:
    import urllib.request
    import urllib.error
    HAS_URLLIB = True
except ImportError:
    HAS_URLLIB = False

try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False

API_BASE = "https://log.concept2.com/api"

# Heart rate zones (percentage of max HR)
HR_ZONES = {
    1: {"name": "Restitusjon", "min": 0, "max": 60, "color": "🟢"},
    2: {"name": "Aerob kapasitet", "min": 60, "max": 70, "color": "🔵"},
    3: {"name": "Aerob effekt", "min": 70, "max": 80, "color": "🟡"},
    4: {"name": "Anaerob terskel", "min": 80, "max": 90, "color": "🟠"},
    5: {"name": "Maks kapasitet", "min": 90, "max": 100, "color": "🔴"},
}

def estimate_max_hr(age, gender=None):
    """Estimate max heart rate based on age."""
    # Tanaka formula (more accurate than 220-age)
    return int(208 - 0.7 * age)

def get_hr_zone(heart_rate, max_hr):
    """Get heart rate zone for a given heart rate."""
    if not heart_rate or not max_hr:
        return None
    pct = (heart_rate / max_hr) * 100
    for zone_num, zone in HR_ZONES.items():
        if zone["min"] <= pct < zone["max"]:
            return zone_num
    return 5 if pct >= 90 else 1

def api_request(endpoint, token, params=None):
    """Make authenticated API request."""
    url = f"{API_BASE}{endpoint}"
    if params:
        query = "&".join(f"{k}={v}" for k, v in params.items())
        url = f"{url}?{query}"
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.c2logbook.v1+json",
        "Content-Type": "application/json"
    }
    
    if HAS_REQUESTS:
        try:
            resp = requests.get(url, headers=headers, timeout=30)
            if resp.status_code == 200:
                return resp.json()
            return {"error": resp.text, "status_code": resp.status_code}
        except Exception as e:
            return {"error": str(e), "status_code": 0}
    
    elif HAS_URLLIB:
        req = urllib.request.Request(url)
        for k, v in headers.items():
            req.add_header(k, v)
        
        try:
            with urllib.request.urlopen(req, timeout=30) as response:
                return json.loads(response.read().decode('utf-8'))
        except urllib.error.HTTPError as e:
            error_body = e.read().decode('utf-8')
            try:
                return {"error": json.loads(error_body), "status_code": e.code}
            except:
                return {"error": error_body, "status_code": e.code}
        except Exception as e:
            return {"error": str(e), "status_code": 0}
    else:
        return {"error": "No HTTP library available", "status_code": 0}

def get_user_info(token):
    """Get authenticated user info."""
    return api_request("/users/me", token)

def get_workouts(token, from_date=None, to_date=None, workout_type="rower", per_page=250):
    """Get workouts for authenticated user."""
    params = {"type": workout_type, "per_page": per_page}
    if from_date:
        params["from"] = from_date
    if to_date:
        params["to"] = to_date
    return api_request("/users/me/results", token, params)

def format_time(tenths):
    """Convert tenths of seconds to MM:SS.d format."""
    if not tenths:
        return "N/A"
    total_seconds = tenths / 10
    minutes = int(total_seconds // 60)
    seconds = total_seconds % 60
    if minutes >= 60:
        hours = minutes // 60
        minutes = minutes % 60
        return f"{hours}:{minutes:02d}:{seconds:04.1f}"
    return f"{minutes}:{seconds:04.1f}"

def format_pace(tenths_per_500m):
    """Convert pace (tenths of sec per 500m) to M:SS.d format."""
    if not tenths_per_500m or tenths_per_500m == 0:
        return "N/A"
    total_seconds = tenths_per_500m / 10
    minutes = int(total_seconds // 60)
    seconds = total_seconds % 60
    return f"{minutes}:{seconds:04.1f}"

def calculate_pace(distance_m, time_tenths):
    """Calculate pace per 500m."""
    if distance_m == 0 or time_tenths == 0:
        return 0
    return int((time_tenths / distance_m) * 500)

def parse_date(date_str):
    """Parse date string to datetime."""
    if not date_str:
        return None
    try:
        return datetime.strptime(date_str[:10], "%Y-%m-%d")
    except:
        return None

def analyze_hr_zones(workouts, max_hr):
    """Analyze time spent in each HR zone."""
    zone_time = defaultdict(int)  # in tenths of seconds
    zone_counts = defaultdict(int)
    
    for w in workouts:
        hr_data = w.get("heart_rate", {})
        avg_hr = hr_data.get("average") if hr_data else None
        if avg_hr:
            zone = get_hr_zone(avg_hr, max_hr)
            if zone:
                zone_time[zone] += w.get("time", 0)
                zone_counts[zone] += 1
    
    return zone_time, zone_counts

def calculate_trends(workouts, weeks=4):
    """Calculate trends over weeks."""
    if not workouts:
        return {}
    
    # Sort by date
    sorted_workouts = sorted(workouts, key=lambda x: x.get("date", ""))
    
    # Group by week
    weekly_data = defaultdict(lambda: {"distance": 0, "time": 0, "count": 0, "workouts": []})
    
    for w in sorted_workouts:
        date = parse_date(w.get("date"))
        if date:
            week_key = date.strftime("%Y-W%U")
            weekly_data[week_key]["distance"] += w.get("distance", 0)
            weekly_data[week_key]["time"] += w.get("time", 0)
            weekly_data[week_key]["count"] += 1
            pace = calculate_pace(w.get("distance", 0), w.get("time", 0))
            if pace > 0:
                weekly_data[week_key]["workouts"].append(pace)
    
    # Calculate weekly averages
    trends = {}
    for week, data in sorted(weekly_data.items())[-weeks:]:
        avg_pace = sum(data["workouts"]) / len(data["workouts"]) if data["workouts"] else 0
        trends[week] = {
            "distance_km": data["distance"] / 1000,
            "time_hours": data["time"] / 36000,  # tenths to hours
            "workouts": data["count"],
            "avg_pace": avg_pace,
            "avg_pace_formatted": format_pace(int(avg_pace))
        }
    
    return trends

def calculate_improvement(trends):
    """Calculate improvement from first to last period."""
    if len(trends) < 2:
        return None
    
    weeks = list(trends.values())
    first = weeks[0]
    last = weeks[-1]
    
    # Lower pace is better
    pace_change = last["avg_pace"] - first["avg_pace"]
    pace_pct = (pace_change / first["avg_pace"]) * 100 if first["avg_pace"] else 0
    
    distance_change = last["distance_km"] - first["distance_km"]
    distance_pct = (distance_change / first["distance_km"]) * 100 if first["distance_km"] else 0
    
    return {
        "pace_change_tenths": pace_change,
        "pace_change_pct": pace_pct,
        "pace_improved": pace_change < 0,  # negative is good (faster)
        "distance_change_km": distance_change,
        "distance_change_pct": distance_pct,
        "weeks": len(weeks)
    }

def analyze_workout_quality(workout, max_hr):
    """Analyze quality metrics for a single workout."""
    analysis = {}
    
    # HR zone check
    hr_data = workout.get("heart_rate", {})
    avg_hr = hr_data.get("average") if hr_data else None
    max_hr_workout = hr_data.get("max") if hr_data else None
    
    if avg_hr and max_hr:
        zone = get_hr_zone(avg_hr, max_hr)
        analysis["hr_zone"] = zone
        analysis["hr_zone_name"] = HR_ZONES.get(zone, {}).get("name", "Ukjent")
        analysis["hr_zone_emoji"] = HR_ZONES.get(zone, {}).get("color", "⚪")
    
    # Pace consistency (if splits available)
    workout_data = workout.get("workout", {})
    splits = workout_data.get("splits", [])
    if splits and len(splits) > 1:
        paces = []
        for split in splits:
            split_pace = calculate_pace(split.get("distance", 0), split.get("time", 0))
            if split_pace > 0:
                paces.append(split_pace)
        
        if paces:
            avg_pace = sum(paces) / len(paces)
            variance = sum((p - avg_pace) ** 2 for p in paces) / len(paces)
            std_dev = math.sqrt(variance)
            
            analysis["pace_consistency"] = std_dev / avg_pace if avg_pace else 0
            analysis["consistency_rating"] = "🟢 Jevn" if analysis["pace_consistency"] < 0.05 else "🟡 OK" if analysis["pace_consistency"] < 0.1 else "🔴 Ujevn"
    
    # Stroke efficiency
    stroke_rate = workout.get("stroke_rate", 0)
    drag_factor = workout.get("drag_factor", 0)
    
    if stroke_rate:
        if 18 <= stroke_rate <= 22:
            analysis["spm_rating"] = "🟢 Effektiv"
        elif 24 <= stroke_rate <= 28:
            analysis["spm_rating"] = "🟡 Tempo"
        elif stroke_rate > 30:
            analysis["spm_rating"] = "🟠 Høyt SPM"
        else:
            analysis["spm_rating"] = "🔵 Rask recovery"
    
    return analysis

def print_summary(workouts, user_data, max_hr):
    """Print detailed summary with pulse zones and trends."""
    print("=" * 70)
    print(f"📊 TRENINGSSAMMENDRAG - {user_data.get('first_name', 'Bruker')}")
    print("=" * 70)
    
    # Basic stats
    total_distance = sum(w.get("distance", 0) for w in workouts)
    total_time = sum(w.get("time", 0) for w in workouts)
    total_calories = sum(w.get("calories_total", 0) or 0 for w in workouts)
    workout_count = len(workouts)
    
    # Averages
    valid_paces = []
    valid_hrs = []
    for w in workouts:
        pace = calculate_pace(w.get("distance", 0), w.get("time", 0))
        if pace > 0:
            valid_paces.append(pace)
        hr_data = w.get("heart_rate", {})
        avg_hr = hr_data.get("average") if hr_data else None
        if avg_hr:
            valid_hrs.append(avg_hr)
    
    avg_pace = sum(valid_paces) / len(valid_paces) if valid_paces else 0
    avg_hr = sum(valid_hrs) / len(valid_hrs) if valid_hrs else 0
    
    print(f"\n📈 SAMMENDRAG")
    print(f"   Økter:        {workout_count}")
    print(f"   Distanse:     {total_distance/1000:.1f} km")
    print(f"   Tid:          {total_time/36000:.1f} timer")
    print(f"   Kalorier:     {total_calories:,} kcal")
    print(f"   Gj.sn. pace:  {format_pace(int(avg_pace))}/500m" if avg_pace else "")
    print(f"   Gj.sn. puls:  {avg_hr:.0f} bpm" if avg_hr else "")
    
    # HR Zone Analysis
    if max_hr:
        print(f"\n💓 PULSSONEANALYSE (Maks HR: {max_hr} bpm)")
        zone_time, zone_counts = analyze_hr_zones(workouts, max_hr)
        
        total_zone_time = sum(zone_time.values())
        if total_zone_time > 0:
            for zone_num in sorted(HR_ZONES.keys()):
                zone = HR_ZONES[zone_num]
                pct = (zone_time[zone_num] / total_zone_time) * 100 if total_zone_time else 0
                time_mins = zone_time[zone_num] / 600  # tenths to minutes
                bar = "█" * int(pct / 5)
                print(f"   {zone['color']} Sone {zone_num}: {zone['name']:<20} {pct:>5.1f}% {bar} ({time_mins:.0f} min)")
        
        # Recommendation
        zone_4_time = zone_time.get(4, 0)
        zone_5_time = zone_time.get(5, 0)
        high_intensity = (zone_4_time + zone_5_time) / total_zone_time * 100 if total_zone_time else 0
        
        print(f"\n   📋 Vurdering:")
        if high_intensity > 20:
            print(f"      ⚠️  Høy intensitet ({high_intensity:.1f}% i sone 4-5)")
            print(f"      Tips: Vurder mer sone 1-2 for bedre restitusjon")
        elif high_intensity < 5:
            print(f"      ℹ️  Lav intensitet ({high_intensity:.1f}% i sone 4-5)")
            print(f"      Tips: Legg inn mer sone 3-4 for å bygge kapasitet")
        else:
            print(f"      ✅ Balansert fordeling ({high_intensity:.1f}% høy intensitet)")
    
    # Trends
    trends = calculate_trends(workouts)
    if trends:
        print(f"\n📉 UKENTLIG TREND")
        print(f"   {'Uke':<10} {'Økter':>6} {'Distanse':>10} {'Tid':>8} {'Pace':>10}")
        print(f"   {'-'*50}")
        
        for week, data in trends.items():
            print(f"   {week:<10} {data['workouts']:>6} {data['distance_km']:>9.1f}km {data['time_hours']:>7.1f}t {data['avg_pace_formatted']:>10}")
        
        # Improvement analysis
        improvement = calculate_improvement(trends)
        if improvement:
            print(f"\n   📊 Utvikling over {improvement['weeks']} uker:")
            
            pace_icon = "🟢 Raskere" if improvement['pace_improved'] else "🔴 Saktre"
            pace_change = abs(improvement['pace_change_pct'])
            print(f"      Pace: {pace_icon} ({pace_change:.1f}%)")
            
            dist_icon = "🟢 Mer" if improvement['distance_change_km'] > 0 else "🔴 Mindre"
            print(f"      Distanse: {dist_icon} ({improvement['distance_change_km']:+.1f} km)")
    
    # Recent workouts analysis
    print(f"\n🎯 SISTE ØKTER")
    print(f"   {'Dato':<12} {'Type':<20} {'Dist':>8} {'Tid':>10} {'Pace':>8} {'HR':>5} {'Sone':<12}")
    print(f"   {'-'*80}")
    
    for w in sorted(workouts, key=lambda x: x.get("date", ""), reverse=True)[:5]:
        date = w.get("date", "")[:10]
        wtype = w.get("workout_type", "ukjent")[:20]
        dist = w.get("distance", 0)
        time = w.get("time", 0)
        pace = calculate_pace(dist, time)
        
        hr_data = w.get("heart_rate", {})
        hr = hr_data.get("average") if hr_data else None
        hr_str = f"{hr:.0f}" if hr else "-"
        
        zone_str = ""
        if hr and max_hr:
            zone = get_hr_zone(hr, max_hr)
            zone_info = HR_ZONES.get(zone, {})
            zone_str = f"{zone_info.get('color', '')} Sone {zone}"
        
        print(f"   {date:<12} {wtype:<20} {dist/1000:>7.2f}km {format_time(time):>10} {format_pace(pace):>8} {hr_str:>5} {zone_str:<12}")
        
        # Detailed analysis for last workout
        if w == workouts[0]:
            analysis = analyze_workout_quality(w, max_hr)
            if analysis:
                details = []
                if "consistency_rating" in analysis:
                    details.append(f"Jevnhet: {analysis['consistency_rating']}")
                if "spm_rating" in analysis:
                    details.append(f"Teknikk: {analysis['spm_rating']}")
                if details:
                    print(f"      └─ {' | '.join(details)}")

def main():
    parser = argparse.ArgumentParser(
        description="Fetch Concept2 workouts with pulse zone analysis and trends",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Eksempler:
  %(prog)s --token <TOKEN> --from-date 2026-02-01
  %(prog)s --token <TOKEN> --format summary --max-hr 165
  %(prog)s --token <TOKEN> --type skierg --trends 8
        """
    )
    parser.add_argument("--token", required=True, help="API access token")
    parser.add_argument("--from-date", help="Start date (YYYY-MM-DD)")
    parser.add_argument("--to-date", help="End date (YYYY-MM-DD)")
    parser.add_argument("--type", default="rower", help="Workout type (rower, skierg, bike, etc.)")
    parser.add_argument("--limit", type=int, default=250, help="Max results (default: 250)")
    parser.add_argument("--format", choices=["json", "table", "summary"], default="summary", help="Output format")
    parser.add_argument("--max-hr", type=int, help="Maximum heart rate (for zone calculation)")
    parser.add_argument("--age", type=int, help="Age (to estimate max HR if not provided)")
    parser.add_argument("--trends", type=int, default=4, help="Number of weeks for trend analysis")
    
    args = parser.parse_args()
    
    # Get user info
    user = get_user_info(args.token)
    if "error" in user:
        print(f"❌ API-feil: {user.get('error', 'Ukjent feil')}", file=sys.stderr)
        sys.exit(1)
    
    user_data = user.get("data", {})
    
    # Estimate max HR if needed
    max_hr = args.max_hr
    if not max_hr and args.age:
        max_hr = estimate_max_hr(args.age, user_data.get("gender"))
    elif not max_hr and user_data.get("dob"):
        try:
            dob = datetime.strptime(user_data["dob"], "%Y-%m-%d")
            age = datetime.now().year - dob.year
            max_hr = estimate_max_hr(age, user_data.get("gender"))
        except:
            pass
    
    # Get workouts
    workouts = get_workouts(args.token, args.from_date, args.to_date, args.type, args.limit)
    if "error" in workouts:
        print(f"❌ Feil ved henting av økter: {workouts.get('error', 'Ukjent feil')}", file=sys.stderr)
        sys.exit(1)
    
    data = workouts.get("data", [])
    meta = workouts.get("meta", {})
    pagination = meta.get("pagination", {})
    
    if args.format == "json":
        print(json.dumps(workouts, indent=2))
    elif args.format == "table":
        print(f"User: {user_data.get('first_name')} {user_data.get('last_name')}")
        print(f"Found {pagination.get('total', len(data))} workouts")
        print(f"{'Date':<12} {'Dist':>8} {'Time':>10} {'Pace':>8} {'SPM':>4} {'HR':>4} {'Type':<20}")
        print("-" * 75)
        for w in data:
            date = w.get("date", "")[:10]
            dist = w.get("distance", 0)
            time = w.get("time", 0)
            pace = calculate_pace(dist, time)
            spm = w.get("stroke_rate", 0) or "-"
            hr_data = w.get("heart_rate", {})
            hr = hr_data.get("average") if hr_data else "-"
            wtype = w.get("workout_type", "unknown")[:20]
            print(f"{date:<12} {dist/1000:>7.2f}km {format_time(time):>10} {format_pace(pace):>8} {spm:>4} {hr if isinstance(hr, str) else f'{hr:.0f}' if hr else '-':>4} {wtype:<20}")
    else:  # summary
        if not data:
            print("Ingen økter funnet for valgt periode.")
            sys.exit(0)
        
        print_summary(data, user_data, max_hr)
        
        # Training recommendations
        print(f"\n💡 ANBEFALINGER")
        print(f"   Basert på dine siste {len(data)} økter:")
        
        # Check consistency
        recent_dates = [parse_date(w.get("date")) for w in data]
        recent_dates = [d for d in recent_dates if d]
        if recent_dates:
            date_diffs = [(recent_dates[i] - recent_dates[i+1]).days for i in range(len(recent_dates)-1)]
            avg_gap = sum(date_diffs) / len(date_diffs) if date_diffs else 0
            
            if avg_gap > 5:
                print(f"      • Du trener i snitt hver {avg_gap:.0f}. dag — vurder å øke til 3-4x/uke")
            elif avg_gap < 2:
                print(f"      • Høy frekvens! Sørg for nok restitusjon mellom økter")
            else:
                print(f"      ✅ God treningsfrekvens ({avg_gap:.1f} dager mellom økter)")
        
        # Check for long workouts
        long_workouts = [w for w in data if w.get("time", 0) > 18000]  # >30 min
        if len(long_workouts) < len(data) * 0.3:
            print(f"      • Få lange økter — legg inn en 30-45 min økt i uken")
        
        # Check for intervals
        interval_types = ["FixedTimeInterval", "FixedDistanceInterval", "VariableInterval"]
        has_intervals = any(w.get("workout_type") in interval_types for w in data)
        if not has_intervals:
            print(f"      • Ingen intervalløkter registrert — vurder å legge inn for å bygge kapasitet")
        
        print(f"\n   God trening! 💪")

if __name__ == "__main__":
    main()

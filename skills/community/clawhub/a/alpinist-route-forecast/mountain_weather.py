#!/usr/bin/env python3
"""
Mountain Route Weather - Get hourly weather forecast along a GPX route.

Parses a GPX file, samples key waypoints, estimates timing based on pace,
and queries Open-Meteo for hourly conditions at each point.

Usage:
    python3 mountain_weather.py --gpx route.gpx --date 2026-07-28
    python3 mountain_weather.py --gpx route.gpx --date 2026-07-28 --pace slow
    python3 mountain_weather.py --gpx route.gpx --date 2026-07-28 --start-hour 3 --json

Pace profiles (vertical gain rate):
    elite:    1,475 ft/hr up, 2,300 ft/hr down
    moderate: 1,000 ft/hr up, 1,640 ft/hr down (default)
    amateur:  650 ft/hr up, 1,310 ft/hr down
"""

import argparse
import json
import math
import sys
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
from urllib.request import urlopen, Request
from urllib.error import URLError
from urllib.parse import urlencode

PACE_PROFILES = {
    "elite": {"up_mhr": 450, "down_mhr": 700, "flat_kmh": 5.5},
    "moderate": {"up_mhr": 300, "down_mhr": 500, "flat_kmh": 4.0},
    "amateur": {"up_mhr": 200, "down_mhr": 400, "flat_kmh": 3.0},
}

OPEN_METEO_URL = "https://api.open-meteo.com/v1/forecast"


def parse_gpx(gpx_path, ascent_only=True):
    """Parse GPX file and return list of trackpoints with lat, lng, ele, name.
    
    If ascent_only=True, detects the summit (highest elevation point) and
    returns only the ascent portion. Handles out-and-back routes from Garmin etc.
    """
    tree = ET.parse(gpx_path)
    root = tree.getroot()
    
    # Handle namespace
    ns = {"gpx": "http://www.topografix.com/GPX/1/1"}
    
    points = []
    for trkpt in root.findall(".//gpx:trkpt", ns):
        lat = float(trkpt.get("lat"))
        lng = float(trkpt.get("lon"))
        ele_el = trkpt.find("gpx:ele", ns)
        ele = float(ele_el.text) if ele_el is not None else None
        name_el = trkpt.find("gpx:name", ns)
        name = name_el.text if name_el is not None else None
        points.append({"lat": lat, "lng": lng, "ele": ele, "name": name})
    
    if ascent_only and points:
        # Find summit (highest elevation point)
        summit_idx = max(range(len(points)), key=lambda i: points[i]["ele"] or 0)
        points = points[:summit_idx + 1]
        # Label the summit
        if not points[-1].get("name"):
            points[-1]["name"] = "Summit"
    
    return points


def haversine_km(lat1, lng1, lat2, lng2):
    """Great-circle distance between two points in km."""
    dlat = math.radians(lat2 - lat1)
    dlng = math.radians(lng2 - lng1)
    a = (math.sin(dlat/2)**2 +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
         math.sin(dlng/2)**2)
    return 6371.0 * 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))


# Terrain classification based on slope angle
TERRAIN_TYPES = {
    "trail": {"max_slope_deg": 30, "pace_mult": 1.0, "label": "Trail/approach"},
    "steep": {"max_slope_deg": 45, "pace_mult": 0.75, "label": "Steep snow/scree/glacier"},
    "technical": {"max_slope_deg": 90, "pace_mult": 0.45, "label": "Technical/scramble"},
}

import os as _os
_SCRIPT_DIR = _os.path.dirname(_os.path.abspath(__file__))

def _resolve_data_path(filename):
    """Resolve data file: check next to script, then scripts/data/."""
    p = _os.path.join(_SCRIPT_DIR, filename)
    if _os.path.exists(p):
        return p
    p2 = _os.path.join(_SCRIPT_DIR, "data", filename)
    if _os.path.exists(p2):
        return p2
    return p  # default: next to script

PACE_PROFILE_FILE = _resolve_data_path("alpinist_profile.json")
PEAK_ROUTES_FILE = _resolve_data_path("peak_routes.json")


def load_peak_routes():
    """Load the peak routes database."""
    try:
        with open(PEAK_ROUTES_FILE) as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def route_to_points(route_data):
    """Convert a peak route database entry into a list of trackpoints."""
    points = []
    trailhead = route_data["trailhead"]
    summit = route_data["summit"]
    segments = route_data["segments"]
    
    # Generate intermediate points from segments
    total_miles = sum(s["miles"] for s in segments)
    lat_range = summit["lat"] - trailhead["lat"]
    lng_range = summit["lng"] - trailhead["lng"]
    
    cumulative_miles = 0
    for i, seg in enumerate(segments):
        # Start of segment
        frac_start = cumulative_miles / total_miles if total_miles else 0
        lat = trailhead["lat"] + lat_range * frac_start
        lng = trailhead["lng"] + lng_range * frac_start
        ele_ft = seg["ele_ft"][0]
        
        point = {
            "lat": lat,
            "lng": lng,
            "ele": ele_ft / 3.281,  # convert to meters for internal use
            "name": seg["name"],
            "terrain_override": seg["terrain"],
        }
        if "crux" in seg:
            point["crux"] = seg["crux"]
        points.append(point)
        
        cumulative_miles += seg["miles"]
    
    # Add summit
    points.append({
        "lat": summit["lat"],
        "lng": summit["lng"],
        "ele": summit["ele_ft"] / 3.281,
        "name": "Summit",
        "terrain_override": segments[-1]["terrain"],
    })
    
    return points


def classify_terrain(slope_deg):
    """Classify terrain type based on slope angle."""
    if slope_deg < 30:
        return "trail"
    elif slope_deg < 45:
        return "steep"
    else:
        return "technical"


def segment_slope_deg(dist_km, ele_change_m):
    """Calculate slope angle in degrees from horizontal distance and elevation change."""
    if dist_km <= 0:
        return 0
    dist_m = dist_km * 1000
    return math.degrees(math.atan2(abs(ele_change_m), dist_m))


def load_alpinist_profile(profile_path=None):
    """Load saved alpinist pace profile from past trips."""
    path = profile_path or PACE_PROFILE_FILE
    try:
        with open(path) as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return None


def save_alpinist_profile(profile_data, profile_path=None):
    """Save alpinist pace profile."""
    import os
    path = profile_path or PACE_PROFILE_FILE
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        json.dump(profile_data, f, indent=2)


def calibrate_pace(gpx_path, actual_start, actual_summit, pace="moderate"):
    """Back-calculate actual pace from reported start/summit times.
    
    Args:
        gpx_path: GPX file used
        actual_start: HH:MM format
        actual_summit: HH:MM format
        pace: base pace profile used
    
    Returns updated alpinist profile dict.
    """
    points = parse_gpx(gpx_path)
    if not points:
        return None
    
    # Calculate actual ascent hours
    start_h, start_m = map(int, actual_start.split(":"))
    summit_h, summit_m = map(int, actual_summit.split(":"))
    actual_hrs = (summit_h - start_h) + (summit_m - start_m) / 60.0
    if actual_hrs <= 0:
        actual_hrs += 24  # overnight
    
    # Compute predicted ascent hours with terrain
    timed_points = compute_route_timing_terrain(points, pace)
    predicted_hrs = timed_points[-1]["cumulative_hr"]
    
    # Overall pace multiplier
    pace_factor = predicted_hrs / actual_hrs if actual_hrs > 0 else 1.0
    
    # Compute terrain breakdown
    terrain_hrs = {"trail": 0, "steep": 0, "technical": 0}
    for pt in timed_points[1:]:
        terrain_hrs[pt.get("terrain", "trail")] += pt.get("time_hr", 0)
    
    # Load existing profile
    profile = load_alpinist_profile() or {
        "trips": [],
        "avg_pace_factor": 1.0,
        "terrain_factors": {"trail": 1.0, "steep": 0.7, "technical": 0.4},
    }
    
    # Add this trip
    trip = {
        "gpx": gpx_path,
        "date": datetime.now().strftime("%Y-%m-%d"),
        "actual_start": actual_start,
        "actual_summit": actual_summit,
        "actual_hrs": round(actual_hrs, 2),
        "predicted_hrs": round(predicted_hrs, 2),
        "pace_factor": round(pace_factor, 3),
        "base_pace": pace,
        "terrain_breakdown_hr": {k: round(v, 2) for k, v in terrain_hrs.items()},
    }
    profile["trips"].append(trip)
    
    # Recalculate average pace factor from all trips
    factors = [t["pace_factor"] for t in profile["trips"]]
    profile["avg_pace_factor"] = round(sum(factors) / len(factors), 3)
    profile["total_trips"] = len(profile["trips"])
    
    save_alpinist_profile(profile)
    return profile


def compute_route_timing_terrain(points, pace, start_hour=3, alpinist_profile=None):
    """Compute route timing with terrain-based pace adjustments."""
    timed_points = []
    cumulative_hr = 0.0
    
    # Load alpinist profile for custom factors
    custom_factor = 1.0
    if alpinist_profile:
        custom_factor = alpinist_profile.get("avg_pace_factor", 1.0)
    
    for i, pt in enumerate(points):
        if i == 0:
            pt["time_hr"] = 0.0
            pt["cumulative_hr"] = 0.0
            pt["terrain"] = "trail"
            timed_points.append(pt)
            continue
        
        prev = points[i-1]
        dist = haversine_km(prev["lat"], prev["lng"], pt["lat"], pt["lng"])
        ele_gain = max(0, (pt["ele"] or 0) - (prev["ele"] or 0))
        ele_loss = max(0, (prev["ele"] or 0) - (pt["ele"] or 0))
        
        # Classify terrain (use override if available from route database)
        if pt.get("terrain_override"):
            terrain = pt["terrain_override"]
        else:
            slope = segment_slope_deg(dist, ele_gain + ele_loss)
            terrain = classify_terrain(slope)
        terrain_mult = TERRAIN_TYPES[terrain]["pace_mult"]
        
        # Check for crux with fixed time override
        crux = pt.get("crux")
        if crux and "fixed_time_min" in crux:
            fixed_times = crux["fixed_time_min"]
            seg_time = fixed_times.get(pace, fixed_times.get("moderate", 60)) / 60.0
            # Apply alpinist calibration
            seg_time = seg_time / custom_factor
            pt["is_crux"] = True
            pt["crux_info"] = crux
        else:
            # Base time
            seg_time = estimate_segment_time_hr(dist, ele_gain, ele_loss, pace)
            # Apply terrain slowdown (divide by multiplier since mult < 1 means slower)
            seg_time = seg_time / terrain_mult
            # Apply alpinist calibration (higher factor = faster climber)
            seg_time = seg_time / custom_factor
        
        cumulative_hr += seg_time
        
        pt["time_hr"] = seg_time
        pt["cumulative_hr"] = cumulative_hr
        pt["terrain"] = terrain
        timed_points.append(pt)
    
    return timed_points


def estimate_segment_time_hr(dist_km, ele_gain_m, ele_loss_m, pace):
    """Estimate time for a segment considering distance and elevation change."""
    p = PACE_PROFILES[pace]
    
    # Time from elevation gain
    time_up = ele_gain_m / p["up_mhr"] if ele_gain_m > 0 else 0
    # Time from elevation loss
    time_down = ele_loss_m / p["down_mhr"] if ele_loss_m > 0 else 0
    # Time from horizontal distance (only the flat component)
    time_flat = dist_km / p["flat_kmh"]
    
    # Use the larger of vertical time or flat time (they overlap)
    return max(time_up + time_down, time_flat)


def compute_route_timing(points, pace, start_hour=3):
    """Compute estimated arrival time at each point."""
    timed_points = []
    cumulative_hr = 0.0
    
    for i, pt in enumerate(points):
        if i == 0:
            pt["time_hr"] = 0.0
            pt["cumulative_hr"] = 0.0
            timed_points.append(pt)
            continue
        
        prev = points[i-1]
        dist = haversine_km(prev["lat"], prev["lng"], pt["lat"], pt["lng"])
        ele_gain = max(0, (pt["ele"] or 0) - (prev["ele"] or 0))
        ele_loss = max(0, (prev["ele"] or 0) - (pt["ele"] or 0))
        
        seg_time = estimate_segment_time_hr(dist, ele_gain, ele_loss, pace)
        cumulative_hr += seg_time
        
        pt["time_hr"] = seg_time
        pt["cumulative_hr"] = cumulative_hr
        timed_points.append(pt)
    
    return timed_points


def sample_key_points(points, max_points=8):
    """Sample key waypoints: named points + evenly spaced by time."""
    if len(points) <= max_points:
        return points
    
    # Always include first, last, and named points
    key = [points[0], points[-1]]
    named = [p for p in points[1:-1] if p.get("name")]
    key.extend(named)
    
    # Fill remaining slots evenly by cumulative time
    remaining = max_points - len(key)
    if remaining > 0 and len(points) > 2:
        total_time = points[-1]["cumulative_hr"]
        interval = total_time / (remaining + 1)
        for i in range(1, remaining + 1):
            target_time = interval * i
            closest = min(points, key=lambda p: abs(p["cumulative_hr"] - target_time))
            if closest not in key:
                key.append(closest)
    
    # Sort by cumulative time
    key.sort(key=lambda p: p["cumulative_hr"])
    return key


def fetch_weather(lat, lng, ele, date, timezone="America/Los_Angeles"):
    """Fetch hourly weather from Open-Meteo for a specific point and date."""
    params = {
        "latitude": lat,
        "longitude": lng,
        "elevation": ele,
        "hourly": "temperature_2m,wind_speed_10m,wind_gusts_10m,precipitation,snowfall,cloud_cover,freezing_level_height,visibility",
        "temperature_unit": "fahrenheit",
        "wind_speed_unit": "mph",
        "precipitation_unit": "inch",
        "timezone": timezone,
        "start_date": date,
        "end_date": date,
    }
    url = f"{OPEN_METEO_URL}?{urlencode(params)}"
    
    try:
        req = Request(url, headers={"User-Agent": "OpenClaw-MountainWeather/1.0"})
        with urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read())
    except (URLError, json.JSONDecodeError) as e:
        return None, str(e)
    
    return data.get("hourly"), None


def get_weather_at_hour(hourly_data, hour):
    """Extract weather at a specific hour from hourly data."""
    if not hourly_data or hour < 0 or hour >= len(hourly_data.get("temperature_2m", [])):
        return None
    
    return {
        "temp_f": hourly_data["temperature_2m"][hour],
        "wind_mph": hourly_data["wind_speed_10m"][hour],
        "wind_gust_mph": hourly_data["wind_gusts_10m"][hour],
        "precip_in": hourly_data["precipitation"][hour],
        "snowfall_cm": hourly_data["snowfall"][hour],
        "cloud_pct": hourly_data["cloud_cover"][hour],
        "freezing_level_ft": round(hourly_data["freezing_level_height"][hour] * 3.281) if hourly_data["freezing_level_height"][hour] else None,
        "visibility_m": hourly_data.get("visibility", [None]*24)[hour],
    }


def find_best_start(points, hourly_data_summit, pace, date):
    """Find the best start hour to minimize summit wind/cloud."""
    summit = points[-1]
    summit_time_hr = summit["cumulative_hr"]
    
    best_start = None
    best_score = float("inf")
    
    # Try start hours from 1 AM to 6 AM
    for start in range(1, 7):
        summit_hour = int(start + summit_time_hr)
        if summit_hour >= 24:
            continue
        
        w = get_weather_at_hour(hourly_data_summit, summit_hour)
        if not w:
            continue
        
        # Score: lower is better (wind + cloud penalty)
        score = w["wind_mph"] * 2 + w["wind_gust_mph"] + w["cloud_pct"] * 0.3
        # Penalize precip heavily
        if w["precip_in"] and w["precip_in"] > 0:
            score += 1000
        
        if score < best_score:
            best_score = score
            best_start = start
    
    return best_start


def main():
    parser = argparse.ArgumentParser(description="Mountain route weather forecast")
    parser.add_argument("--gpx", default=None, help="GPX file path")
    parser.add_argument("--route", default=None, help="Named route from database (e.g. 'rainier-dc', 'forbidden-wr')")
    parser.add_argument("--list-routes", action="store_true", help="List all available routes in database")
    parser.add_argument("--trailhead-ft", type=int, default=None, help="Trailhead elevation in ft (simple mode)")
    parser.add_argument("--summit-ft", type=int, default=None, help="Summit elevation in ft (simple mode)")
    parser.add_argument("--distance-mi", type=float, default=None, help="One-way distance in miles (simple mode)")
    parser.add_argument("--summit-lat", type=float, default=None, help="Summit latitude (simple mode)")
    parser.add_argument("--summit-lng", type=float, default=None, help="Summit longitude (simple mode)")
    parser.add_argument("--date", default=None, help="Forecast date (YYYY-MM-DD)")
    parser.add_argument("--pace", default="moderate", choices=["elite", "moderate", "amateur"],
                        help="Climbing pace (default: moderate)")
    parser.add_argument("--start-hour", type=int, default=None,
                        help="Start hour (0-23). If omitted, auto-picks best window.")
    parser.add_argument("--timezone", default="America/Los_Angeles",
                        help="Timezone (default: America/Los_Angeles)")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--peak", default=None,
                        help="Peak name for mountain-forecast.com verification (e.g. 'forbidden peak')")
    parser.add_argument("--actual-start", default=None,
                        help="Post-trip: actual start time HH:MM (for pace calibration)")
    parser.add_argument("--actual-summit", default=None,
                        help="Post-trip: actual summit time HH:MM (for pace calibration)")
    args = parser.parse_args()
    
    # Handle calibration mode
    if args.actual_start and args.actual_summit:
        profile = calibrate_pace(args.gpx, args.actual_start, args.actual_summit, args.pace)
        if profile:
            print(f"\n✅ Pace calibrated from trip data!")
            print(f"   Actual ascent: {profile['trips'][-1]['actual_hrs']:.1f} hrs")
            print(f"   Predicted was: {profile['trips'][-1]['predicted_hrs']:.1f} hrs")
            print(f"   Your pace factor: {profile['trips'][-1]['pace_factor']:.2f}x (>1 = faster than profile)")
            print(f"   Average across {profile['total_trips']} trip(s): {profile['avg_pace_factor']:.2f}x")
            print(f"   Saved to: {PACE_PROFILE_FILE}")
        else:
            print("Error: Could not calibrate pace", file=sys.stderr)
        sys.exit(0)
    
    # Handle --list-routes
    if args.list_routes:
        routes = load_peak_routes()
        if not routes:
            print("No routes database found.", file=sys.stderr)
            sys.exit(1)
        print(f"\n📋 Available routes ({len(routes)}):")
        print(f"{'Route ID':<22} {'Name':<45} {'Gain':<10} {'Miles'}")
        print("-" * 90)
        for rid, r in sorted(routes.items()):
            print(f"{rid:<22} {r['name']:<45} {r['gain_ft']:,} ft   {r['distance_mi']}")
        sys.exit(0)
    
    # Require a date for forecast
    if not args.date:
        print("Error: --date is required for forecast", file=sys.stderr)
        sys.exit(1)
    
    # Check forecast range
    target_date = datetime.strptime(args.date, "%Y-%m-%d").date()
    today = datetime.now().date()
    days_ahead = (target_date - today).days
    if days_ahead < 0:
        print("Error: Date is in the past", file=sys.stderr)
        sys.exit(1)
    elif days_ahead > 16:
        print(f"Error: Date is {days_ahead} days out. Maximum forecast range is 16 days.", file=sys.stderr)
        print("  Days 1-7:  High confidence (Open-Meteo + NOAA + Mountain-Forecast)", file=sys.stderr)
        print("  Days 8-16: Low confidence (Open-Meteo only, no verification)", file=sys.stderr)
        sys.exit(1)
    
    # Set confidence level
    if days_ahead <= 3:
        confidence = "HIGH"
        confidence_note = "3-day forecast — very reliable"
    elif days_ahead <= 7:
        confidence = "MODERATE"
        confidence_note = f"{days_ahead}-day forecast — all 3 sources available"
    else:
        confidence = "LOW"
        confidence_note = f"{days_ahead}-day forecast — Open-Meteo only, expect significant changes"
    
    # Determine points from one of three sources
    route_name = None
    if args.route:
        routes = load_peak_routes()
        if args.route not in routes:
            print(f"Error: Route '{args.route}' not found. Use --list-routes to see options.", file=sys.stderr)
            sys.exit(1)
        route_data = routes[args.route]
        route_name = route_data["name"]
        # Auto-set peak for mountain-forecast verification
        if not args.peak and route_data.get("peak"):
            args.peak = route_data["peak"]
        # Handle multi-day: forecast summit day from high camp
        num_days = route_data.get("days", 1)
        camps = route_data.get("camps", [])
        summit_camp_name = route_data.get("summit_day_start_camp")
        if num_days > 1 and camps and summit_camp_name:
            camp = next((c for c in camps if c["name"] == summit_camp_name), camps[-1])
            from datetime import date as date_cls
            base_date = datetime.strptime(args.date, "%Y-%m-%d").date()
            summit_date = base_date + timedelta(days=num_days - 1)
            # Build points from camp to summit only
            full_points = route_to_points(route_data)
            camp_ele_m = camp["ele_ft"] / 3.281
            camp_idx = min(range(len(full_points)), key=lambda i: abs(full_points[i]["ele"] - camp_ele_m))
            points = full_points[camp_idx:]
            if camp.get("lat") and camp.get("lng"):
                points[0]["lat"] = camp["lat"]
                points[0]["lng"] = camp["lng"]
            points[0]["name"] = summit_camp_name
            # Use summit date for weather
            args.date = summit_date.strftime("%Y-%m-%d")
            # Print multi-day itinerary
            print(f"\n\U0001f4c5 Multi-day route ({num_days} days):")
            for c in camps:
                day_date = (base_date + timedelta(days=c.get('day', 1) - 1)).strftime('%a %b %d')
                print(f"   Day {c.get('day', 1)} ({day_date}): Hike to {c['name']} ({c['ele_ft']:,} ft)")
            print(f"   Summit day ({summit_date.strftime('%a %b %d')}): {summit_camp_name} \u2192 Summit")
            if route_data.get("notes"):
                print(f"   Note: {route_data['notes']}")
            print()
        else:
            points = route_to_points(route_data)
    elif args.gpx:
        points = parse_gpx(args.gpx)
        route_name = args.gpx
    elif args.trailhead_ft and args.summit_ft and args.distance_mi:
        # Simple point-to-point mode
        lat = args.summit_lat or 47.5  # default PNW latitude
        lng = args.summit_lng or -121.5
        gain_ft = args.summit_ft - args.trailhead_ft
        # Create simple linear profile with 4 points
        points = []
        for i, frac in enumerate([0.0, 0.33, 0.66, 1.0]):
            ele_ft = args.trailhead_ft + gain_ft * frac
            name = ["Trailhead", None, None, "Summit"][i]
            points.append({
                "lat": lat,
                "lng": lng,
                "ele": ele_ft / 3.281,
                "name": name,
            })
        route_name = f"{args.trailhead_ft:,} ft → {args.summit_ft:,} ft ({args.distance_mi} mi)"
    else:
        print("Error: Provide --gpx, --route, or --trailhead-ft/--summit-ft/--distance-mi", file=sys.stderr)
        sys.exit(1)
    
    # Parse GPX
    if not points:
        print("Error: No trackpoints found", file=sys.stderr)
        sys.exit(1)
    
    # Load alpinist profile if available
    alpinist_profile = load_alpinist_profile()
    
    # Compute timing with terrain classification
    timed_points = compute_route_timing_terrain(points, args.pace, alpinist_profile=alpinist_profile)
    
    # Sample key waypoints
    key_points = sample_key_points(timed_points, max_points=8)
    
    # Fetch weather for summit to determine best start
    summit = timed_points[-1]
    summit_weather, err = fetch_weather(summit["lat"], summit["lng"], summit["ele"], args.date, args.timezone)
    if err:
        print(f"Error fetching weather: {err}", file=sys.stderr)
        sys.exit(1)
    
    # Determine start hour
    if args.start_hour is not None:
        start_hour = args.start_hour
    else:
        start_hour = find_best_start(timed_points, summit_weather, args.pace, args.date)
        if start_hour is None:
            start_hour = 3  # Default alpine start
    
    # Fetch weather for each key point and compute conditions at arrival time
    results = []
    for pt in key_points:
        arrival_hour = int(start_hour + pt["cumulative_hr"])
        if arrival_hour >= 24:
            arrival_hour = 23
        
        hourly, err = fetch_weather(pt["lat"], pt["lng"], pt["ele"], args.date, args.timezone)
        if err:
            results.append({"point": pt, "error": err})
            continue
        
        weather = get_weather_at_hour(hourly, arrival_hour)
        
        result_entry = {
            "name": pt.get("name") or f"{round(pt['ele'] * 3.281):,} ft",
            "elevation_m": round(pt["ele"]),
            "elevation_ft": round(pt["ele"] * 3.281),
            "arrival_hour": arrival_hour,
            "arrival_time": f"{arrival_hour:02d}:00",
            "cumulative_hr": round(pt["cumulative_hr"], 1),
            "weather": weather,
        }
        if pt.get("is_crux"):
            result_entry["is_crux"] = True
            result_entry["crux_info"] = pt["crux_info"]
        results.append(result_entry)
    
    # Compute descent timing
    total_up_hr = timed_points[-1]["cumulative_hr"]
    # Descent is roughly 60% of ascent time
    descent_hr = total_up_hr * 0.6
    back_at_camp_hour = int(start_hour + total_up_hr + descent_hr)
    
    # Compute descent waypoints (reverse of ascent, with descent timing)
    descent_results = []
    summit_hour = int(start_hour + total_up_hr)
    # Sample a few descent points (summit, midpoint, camp/trailhead)
    descent_points = [key_points[-1]]  # summit
    if len(key_points) > 2:
        descent_points.append(key_points[len(key_points) // 2])  # midpoint
    descent_points.append(key_points[0])  # camp/trailhead
    
    descent_elapsed = 0.0
    for i, pt in enumerate(descent_points):
        if i == 0:
            hour = summit_hour  # just summited
        elif i == len(descent_points) - 1:
            hour = back_at_camp_hour  # back at start
        else:
            hour = int(summit_hour + descent_hr * 0.5)  # midpoint
        
        if hour >= 24:
            hour = 23
        
        hourly, err = fetch_weather(pt["lat"], pt["lng"], pt["ele"], args.date, args.timezone)
        if err:
            continue
        weather = get_weather_at_hour(hourly, hour)
        descent_results.append({
            "name": pt.get("name") or f"{round(pt['ele'] * 3.281):,} ft",
            "elevation_ft": round(pt["ele"] * 3.281),
            "hour": hour,
            "time": f"{hour:02d}:00",
            "weather": weather,
        })
    
    output = {
        "route": route_name,
        "date": args.date,
        "pace": args.pace,
        "days_ahead": days_ahead,
        "confidence": confidence,
        "confidence_note": confidence_note,
        "recommended_start": f"{start_hour:02d}:00",
        "estimated_summit_time": f"{int(start_hour + total_up_hr):02d}:00",
        "estimated_return": f"{min(back_at_camp_hour, 23):02d}:00",
        "total_ascent_hr": round(total_up_hr, 1),
        "waypoints": results,
        "descent": descent_results,
    }
    
    # Mountain-forecast.com verification
    mf_data = None
    if args.peak:
        mf_data = fetch_mountain_forecast(args.peak)
        if mf_data and "error" not in mf_data:
            output["mountain_forecast_verification"] = mf_data
    
    # NOAA verification (use summit coords)
    noaa_data = None
    summit_pt = timed_points[-1]
    summit_hour = int(start_hour + total_up_hr)
    target_hours = list(range(start_hour, min(summit_hour + 2, 24)))
    noaa_data = fetch_noaa_forecast(summit_pt["lat"], summit_pt["lng"], args.date, target_hours)
    if noaa_data and "error" not in noaa_data:
        output["noaa_verification"] = noaa_data
    
    if args.json:
        print(json.dumps(output, indent=2))
    else:
        print(f"\n🏔️  Route: {route_name}")
        print(f"📅  Date: {args.date} | Pace: {args.pace}")
        confidence_emoji = {"🟢": "HIGH", "🟡": "MODERATE", "🟠": "LOW"}
        c_emoji = next(k for k, v in confidence_emoji.items() if v == confidence)
        print(f"{c_emoji}  Confidence: {confidence} — {confidence_note}")
        print(f"⏰  Recommended start: {output['recommended_start']}")
        print(f"🔝  Summit by: {output['estimated_summit_time']}")
        print(f"🏕️  Back at camp: {output['estimated_return']}")
        print(f"\n{'Time':<8} {'Location':<25} {'Elev':<12} {'Temp':<8} {'Wind':<14} {'Cloud':<8} {'Precip'}")
        print("-" * 95)
        
        for r in results:
            w = r.get("weather")
            if not w:
                print(f"{r['arrival_time']:<8} {r['name']:<25} {r['elevation_ft']} ft     [no data]")
                continue
            wind_str = f"{w['wind_mph']:.0f} ({w['wind_gust_mph']:.0f}g) mph"
            precip_str = f"{w['precip_in']:.2f}\"" if w['precip_in'] else "None"
            print(f"{r['arrival_time']:<8} {r['name']:<25} {r['elevation_ft']:<7} ft  {w['temp_f']:<6.0f}°F {wind_str:<14} {w['cloud_pct']:<6}%  {precip_str}")
        
        # Crux segment details
        crux_segments = [r for r in results if r.get("is_crux")]
        if crux_segments:
            print(f"\n⚠️  Technical crux segments:")
            for cs in crux_segments:
                ci = cs["crux_info"]
                fixed = ci["fixed_time_min"]
                print(f"   🧗 {cs['name']}")
                print(f"      {ci['description']}")
                print(f"      Time: {fixed.get('elite','-')}min (elite) / {fixed.get('moderate','-')}min (moderate) / {fixed.get('amateur','-')}min (amateur)")
                if ci.get('queue_risk_min'):
                    print(f"      ⏳ Queue risk: +{ci['queue_risk_min']}min on weekends")
                if ci.get('bail_rate'):
                    print(f"      🔄 Bail rate: {int(ci['bail_rate']*100)}% of parties turn back here")
                if ci.get('notes'):
                    print(f"      💡 {ci['notes']}")

        # Warnings
        summit_w = results[-1].get("weather") if results else None
        if summit_w:
            print(f"\n📊 Summit conditions at {results[-1]['arrival_time']}:")
            print(f"   Freezing level: {summit_w['freezing_level_ft']} ft")
            if summit_w["wind_gust_mph"] > 30:
                print(f"   ⚠️  HIGH WIND WARNING: Gusts to {summit_w['wind_gust_mph']:.0f} mph on summit")
            if summit_w["precip_in"] and summit_w["precip_in"] > 0:
                print(f"   ⚠️  PRECIPITATION expected at summit")
            if summit_w["cloud_pct"] > 80:
                print(f"   ⚠️  LOW VISIBILITY likely (cloud cover {summit_w['cloud_pct']}%)")
        
        # Descent forecast
        if descent_results:
            print(f"\n⬇️  Descent forecast:")
            for d in descent_results:
                w = d.get("weather")
                if not w:
                    continue
                wind_str = f"{w['wind_mph']:.0f} ({w['wind_gust_mph']:.0f}g) mph"
                precip_str = f"{w['precip_in']:.2f}\"" if w['precip_in'] else "None"
                print(f"   {d['time']:<8} {d['name']:<25} {d['elevation_ft']:<7} ft  {w['temp_f']:<6.0f}°F {wind_str:<14} {precip_str}")
            # Descent warnings
            for d in descent_results:
                w = d.get("weather")
                if not w:
                    continue
                if w.get("precip_in") and w["precip_in"] > 0.1:
                    print(f"   ⚠️  PRECIPITATION on descent at {d['time']} ({d['name']})")
                if w.get("wind_gust_mph", 0) > 40:
                    print(f"   ⚠️  HIGH WINDS on descent at {d['time']}: gusts {w['wind_gust_mph']:.0f} mph")
                if w.get("cloud_pct", 0) > 80:
                    print(f"   ⚠️  LOW VISIBILITY on descent at {d['time']} ({d['name']})")
        
        # Mountain-forecast.com verification
        if mf_data and "error" not in mf_data:
            print(f"\n🌐 Mountain-Forecast.com verification ({mf_data['peak']} @ {mf_data['elevation_ft']}ft):")
            print(f"   {mf_data.get('summary', 'N/A')[:150]}")
            if mf_data.get('wind_kmh'):
                winds_mph = [(int(w*0.621), d) for w, d in mf_data['wind_kmh'][:6]]
                wind_str = ', '.join(f"{s}mph {d}" for s, d in winds_mph)
                print(f"   Winds: {wind_str}")
            if mf_data.get('temp_min_c') and mf_data.get('temp_max_c'):
                print(f"   Temps: {mf_data['temp_min_c'][0]}–{mf_data['temp_max_c'][0]}°C ({int(mf_data['temp_min_c'][0]*1.8+32)}–{int(mf_data['temp_max_c'][0]*1.8+32)}°F)")
            print(f"   Source: {mf_data['url']}")
        elif mf_data and "error" in mf_data:
            print(f"\n🌐 Mountain-Forecast.com: {mf_data['error']}")
        
        # NOAA verification
        if noaa_data and "error" not in noaa_data:
            print(f"\n🇸🇺 NOAA/NWS verification (summit grid):")
            for h in noaa_data["hours"]:
                print(f"   {h['time']}  {h['temp_f']}°F  Wind {h['wind_mph']}mph {h['wind_dir']}  {h['condition']}")
        elif noaa_data and "error" in noaa_data:
            print(f"\n🇸🇺 NOAA/NWS: {noaa_data['error']}")


# --- NOAA NWS secondary verification ---

def fetch_noaa_forecast(lat, lng, date_str, target_hours=None):
    """Fetch hourly forecast from NOAA NWS for a specific location and date.
    
    Args:
        lat, lng: Coordinates (US only)
        date_str: YYYY-MM-DD
        target_hours: list of hours (0-23) to extract, or None for all
    
    Returns dict with hourly conditions, or None if unavailable.
    """
    import re
    
    headers = {"User-Agent": "(mountain-weather-skill)", "Accept": "application/json"}
    
    # Step 1: Get grid point
    try:
        url = f"https://api.weather.gov/points/{lat},{lng}"
        req = Request(url, headers=headers)
        resp = urlopen(req, timeout=10)
        data = json.loads(resp.read())
        hourly_url = data["properties"]["forecastHourly"]
    except Exception as e:
        return {"error": f"NOAA points lookup failed: {e}"}
    
    # Step 2: Get hourly forecast
    try:
        req = Request(hourly_url, headers=headers)
        resp = urlopen(req, timeout=10)
        data = json.loads(resp.read())
        periods = data["properties"]["periods"]
    except Exception as e:
        return {"error": f"NOAA hourly fetch failed: {e}"}
    
    # Step 3: Filter to target date and hours
    results = []
    for p in periods:
        start = p["startTime"][:10]  # YYYY-MM-DD
        if start != date_str:
            continue
        hour = int(p["startTime"][11:13])
        if target_hours and hour not in target_hours:
            continue
        wind_speed = 0
        wind_match = re.match(r'(\d+)', p.get("windSpeed", "0"))
        if wind_match:
            wind_speed = int(wind_match.group(1))
        results.append({
            "hour": hour,
            "time": f"{hour:02d}:00",
            "temp_f": p["temperature"],
            "temp_c": round((p["temperature"] - 32) * 5 / 9, 1),
            "wind_mph": wind_speed,
            "wind_dir": p.get("windDirection", ""),
            "condition": p.get("shortForecast", ""),
            "detail": p.get("detailedForecast", ""),
        })
    
    if not results:
        return {"error": f"No NOAA data for {date_str} (forecast may not extend that far)"}
    
    return {
        "source": "NOAA/NWS",
        "grid_url": hourly_url,
        "location": f"{lat},{lng}",
        "date": date_str,
        "hours": results,
    }


# --- Mountain-Forecast.com secondary verification ---

MOUNTAIN_FORECAST_PEAKS = {
    # PNW
    "rainier": ("Mount-Rainier", 4392),
    "mount rainier": ("Mount-Rainier", 4392),
    "baker": ("Mount-Baker", 3286),
    "mount baker": ("Mount-Baker", 3286),
    "shuksan": ("Mount-Shuksan", 2782),
    "mount shuksan": ("Mount-Shuksan", 2782),
    "forbidden": ("Forbidden-Peak", 2687),
    "forbidden peak": ("Forbidden-Peak", 2687),
    "glacier peak": ("Glacier-Peak", 3213),
    "olympus": ("Mount-Olympus-Washington", 2432),
    "mount olympus": ("Mount-Olympus-Washington", 2432),
    "stuart": ("Mount-Stuart", 2870),
    "mount stuart": ("Mount-Stuart", 2870),
    "adams": ("Mount-Adams-Washington", 3743),
    "mount adams": ("Mount-Adams-Washington", 3743),
    "hood": ("Mount-Hood", 3429),
    "mount hood": ("Mount-Hood", 3429),
    "st helens": ("Mount-Saint-Helens", 2549),
    "mount st helens": ("Mount-Saint-Helens", 2549),
    # Add more as needed
}


def fetch_mountain_forecast(peak_name):
    """Fetch summit forecast from mountain-forecast.com as secondary verification.
    
    Args:
        peak_name: Common peak name (e.g. 'rainier', 'forbidden peak')
    
    Returns dict with days/time slots and conditions, or None if unavailable.
    """
    import re
    
    key = peak_name.lower().strip()
    if key not in MOUNTAIN_FORECAST_PEAKS:
        return {"error": f"Peak '{peak_name}' not in database. Available: {', '.join(sorted(set(v[0] for v in MOUNTAIN_FORECAST_PEAKS.values())))}"}  
    
    slug, elevation = MOUNTAIN_FORECAST_PEAKS[key]
    url = f"https://www.mountain-forecast.com/peaks/{slug}/forecasts/{elevation}"
    
    try:
        req = Request(url, headers={"User-Agent": "Mozilla/5.0"})
        resp = urlopen(req, timeout=15)
        html = resp.read().decode("utf-8", errors="replace")
    except Exception as e:
        return {"error": f"Failed to fetch: {e}"}
    
    rows = re.findall(r'<tr class="forecast-table__row" data-row="(.*?)">(.*?)</tr>', html, re.DOTALL)
    if not rows:
        return {"error": "Could not parse forecast table"}
    
    data = {}
    for name, content in rows:
        text = re.sub(r'<[^>]+>', ' ', content)
        text = ' '.join(text.split())
        data[name] = text
    
    # Parse into structured format
    result = {
        "source": "mountain-forecast.com",
        "url": url,
        "peak": slug,
        "elevation_m": elevation,
        "elevation_ft": int(elevation * 3.281),
    }
    
    # Extract days and time slots
    if "days" in data:
        parts = data["days"].replace("Change units", "").strip().split()
        result["days"] = parts
    
    if "time" in data:
        result["time_slots"] = data["time"].split()
    
    if "phrases" in data:
        result["conditions"] = data["phrases"].split("  ") if "  " in data["phrases"] else data["phrases"].split()
    
    # Wind (km/h values)
    if "wind" in data:
        wind_vals = re.findall(r'(\d+)\s+([NSEW]+)', data["wind"])
        result["wind_kmh"] = [(int(s), d) for s, d in wind_vals]
    
    # Temperatures
    if "temperature-max" in data:
        temps = re.findall(r'(-?\d+)', data["temperature-max"].replace("max", "").replace("C", "").replace("&deg;", ""))
        result["temp_max_c"] = [int(t) for t in temps]
    if "temperature-min" in data:
        temps = re.findall(r'(-?\d+)', data["temperature-min"].replace("min", "").replace("C", "").replace("&deg;", ""))
        result["temp_min_c"] = [int(t) for t in temps]
    
    # Snow/rain
    if "snow" in data:
        snow_vals = re.findall(r'(\d+\.?\d*)', data["snow"].replace("cm", "").replace("&nbsp;", ""))
        if snow_vals:
            result["snow_cm"] = [float(v) for v in snow_vals]
    
    if "rain" in data:
        rain_vals = re.findall(r'(\d+\.?\d*)', data["rain"].replace("mm", "").replace("&nbsp;", ""))
        if rain_vals:
            result["rain_mm"] = [float(v) for v in rain_vals]
    
    # Summary
    if "summary" in data:
        result["summary"] = data["summary"]
    
    return result


if __name__ == "__main__":
    # Add --mf-verify flag
    if "--mf-verify" in sys.argv:
        peak = sys.argv[sys.argv.index("--mf-verify") + 1] if sys.argv.index("--mf-verify") + 1 < len(sys.argv) else None
        if not peak:
            print("Usage: --mf-verify <peak_name>", file=sys.stderr)
            sys.exit(1)
        result = fetch_mountain_forecast(peak)
        print(json.dumps(result, indent=2))
    else:
        main()

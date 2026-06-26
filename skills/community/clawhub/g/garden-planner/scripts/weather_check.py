#!/usr/bin/env python3
"""
weather_check.py - Fetch local weather and frost warnings via Open-Meteo.
Usage: weather_check.py --lat 37.54 --lon -77.44
       weather_check.py --zip 23220   (requires geocoding via Open-Meteo)
       weather_check.py --lat 37.54 --lon -77.44 --json
"""

import argparse
import json
import os
import sys
import urllib.request
import urllib.parse
import urllib.error
from datetime import datetime, date, timedelta

FORECAST_URL = "https://api.open-meteo.com/v1/forecast"
GEOCODE_URL = "https://geocoding-api.open-meteo.com/v1/search"

FROST_THRESHOLD_C = 0.0       # 32°F
FROST_WARNING_C = 2.0         # warn if within 2°C of freezing
FREEZE_HARD_C = -4.0          # hard freeze warning


def fetch_json(url, params):
    """Fetch JSON from a URL with query params. Returns dict or raises."""
    query = urllib.parse.urlencode(params)
    full_url = f"{url}?{query}"
    try:
        with urllib.request.urlopen(full_url, timeout=10) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.URLError as e:
        raise ConnectionError(f"Network error: {e.reason}") from e
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON response: {e}") from e


def zip_to_latlon(zip_code):
    """Use Open-Meteo geocoding to resolve a US ZIP code."""
    try:
        data = fetch_json(GEOCODE_URL, {"name": zip_code, "count": 1, "language": "en", "format": "json"})
        results = data.get("results", [])
        if not results:
            raise ValueError(f"No geocoding results for ZIP '{zip_code}'")
        r = results[0]
        return r["latitude"], r["longitude"], r.get("name", zip_code)
    except ConnectionError:
        raise
    except Exception as e:
        raise ValueError(f"Geocoding failed for '{zip_code}': {e}") from e


def fetch_forecast(lat, lon):
    """Fetch 7-day forecast from Open-Meteo."""
    params = {
        "latitude": lat,
        "longitude": lon,
        "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum,weathercode",
        "hourly": "temperature_2m",
        "temperature_unit": "fahrenheit",
        "precipitation_unit": "inch",
        "timezone": "auto",
        "forecast_days": 7,
    }
    return fetch_json(FORECAST_URL, params)


def celsius_from_f(f):
    return (f - 32) * 5 / 9


def analyze_frost(daily):
    """Return list of frost warning dicts."""
    warnings = []
    dates = daily.get("time", [])
    mins_f = daily.get("temperature_2m_min", [])

    for i, (d, min_f) in enumerate(zip(dates, mins_f)):
        if min_f is None:
            continue
        min_c = celsius_from_f(min_f)
        if min_c <= FREEZE_HARD_C:
            warnings.append({"date": d, "min_f": min_f, "min_c": round(min_c, 1),
                              "level": "HARD FREEZE", "emoji": "🧊"})
        elif min_c <= FROST_THRESHOLD_C:
            warnings.append({"date": d, "min_f": min_f, "min_c": round(min_c, 1),
                              "level": "FROST", "emoji": "❄️"})
        elif min_c <= FROST_WARNING_C:
            warnings.append({"date": d, "min_f": min_f, "min_c": round(min_c, 1),
                              "level": "FROST WARNING", "emoji": "⚠️"})
    return warnings


WEATHER_CODES = {
    0: "Clear sky",
    1: "Mainly clear", 2: "Partly cloudy", 3: "Overcast",
    45: "Fog", 48: "Depositing rime fog",
    51: "Light drizzle", 53: "Moderate drizzle", 55: "Dense drizzle",
    61: "Slight rain", 63: "Moderate rain", 65: "Heavy rain",
    71: "Slight snow", 73: "Moderate snow", 75: "Heavy snow",
    77: "Snow grains",
    80: "Slight showers", 81: "Moderate showers", 82: "Violent showers",
    85: "Slight snow showers", 86: "Heavy snow showers",
    95: "Thunderstorm", 96: "Thunderstorm w/ slight hail", 99: "Thunderstorm w/ heavy hail",
}


def build_summary(data, lat, lon, location_name=None):
    daily = data.get("daily", {})
    dates = daily.get("time", [])
    max_f = daily.get("temperature_2m_max", [])
    min_f = daily.get("temperature_2m_min", [])
    precip = daily.get("precipitation_sum", [])
    codes = daily.get("weathercode", [])
    timezone = data.get("timezone", "Unknown")

    frost_warnings = analyze_frost(daily)

    days = []
    for i in range(len(dates)):
        day = {
            "date": dates[i] if i < len(dates) else None,
            "max_f": max_f[i] if i < len(max_f) else None,
            "min_f": min_f[i] if i < len(min_f) else None,
            "precip_in": precip[i] if i < len(precip) else None,
            "condition": WEATHER_CODES.get(codes[i] if i < len(codes) else None, "Unknown"),
        }
        days.append(day)

    return {
        "lat": lat,
        "lon": lon,
        "location": location_name or f"{lat}, {lon}",
        "timezone": timezone,
        "generated": date.today().isoformat(),
        "forecast": days,
        "frost_warnings": frost_warnings,
        "has_frost_risk": len(frost_warnings) > 0,
    }


def print_human(summary):
    print(f"\n{'='*58}")
    print(f"🌤  Weather Forecast — {summary['location']}")
    print(f"    Timezone: {summary['timezone']} | Generated: {summary['generated']}")
    print(f"{'='*58}")

    # Frost alert banner
    if summary["has_frost_risk"]:
        print(f"\n  {'!'*52}")
        for w in summary["frost_warnings"]:
            print(f"  {w['emoji']}  {w['level']}: {w['date']} — Low: {w['min_f']:.0f}°F ({w['min_c']}°C)")
        print(f"  {'!'*52}")
        print(f"  ⚡ Protect frost-sensitive plants! Cover or bring indoors.")
    else:
        print(f"\n  ✅  No frost risk in the 7-day forecast.")

    print(f"\n  {'─'*54}")
    print(f"  {'Date':<12} {'High':>6} {'Low':>6} {'Rain':>6}  Conditions")
    print(f"  {'─'*54}")

    for d in summary["forecast"]:
        date_str = d["date"] or "?"
        high = f"{d['max_f']:.0f}°F" if d["max_f"] is not None else "  N/A"
        low  = f"{d['min_f']:.0f}°F" if d["min_f"] is not None else "  N/A"
        rain = f"{d['precip_in']:.2f}\"" if d["precip_in"] is not None else "   N/A"
        cond = d["condition"]

        # Flag frost days
        frost_flag = ""
        for w in summary["frost_warnings"]:
            if w["date"] == date_str:
                frost_flag = f"  {w['emoji']}"
        print(f"  {date_str:<12} {high:>6} {low:>6} {rain:>6}  {cond}{frost_flag}")

    print(f"\n{'='*58}\n")


def main():
    parser = argparse.ArgumentParser(description="Fetch 7-day weather forecast with frost warnings.")
    coord_group = parser.add_mutually_exclusive_group()
    coord_group.add_argument("--zip", help="US ZIP code (uses geocoding)")
    coord_group.add_argument("--lat", type=float, help="Latitude")
    parser.add_argument("--lon", type=float, help="Longitude (required with --lat)")
    parser.add_argument("--json", action="store_true", dest="json_output",
                        help="Output raw JSON instead of human-readable")
    parser.add_argument("--data-dir", default=os.path.expanduser("~/.openclaw/workspace/garden"),
                        help="Garden data dir (for reading config lat/lon)")
    args = parser.parse_args()

    lat = lon = None
    location_name = None

    # Resolve coordinates
    if args.zip:
        try:
            lat, lon, location_name = zip_to_latlon(args.zip)
            print(f"Resolved ZIP {args.zip} → {location_name} ({lat}, {lon})", file=sys.stderr)
        except (ConnectionError, ValueError) as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)
    elif args.lat is not None:
        if args.lon is None:
            print("Error: --lon is required when using --lat", file=sys.stderr)
            sys.exit(1)
        lat, lon = args.lat, args.lon
    else:
        # Try to read from garden config
        garden_file = os.path.join(os.path.expanduser(args.data_dir), "garden.json")
        if os.path.exists(garden_file):
            with open(garden_file) as f:
                garden = json.load(f)
            config = garden.get("config", {})
            lat = config.get("lat")
            lon = config.get("lon")
            location_name = config.get("location_name")
            if lat and lon:
                print(f"Using coordinates from garden config: {lat}, {lon}", file=sys.stderr)
            else:
                print("Error: No coordinates found. Use --lat/--lon or --zip, or set lat/lon in garden.json config.",
                      file=sys.stderr)
                sys.exit(1)
        else:
            print("Error: Provide --lat/--lon, --zip, or configure lat/lon in garden.json", file=sys.stderr)
            parser.print_help()
            sys.exit(1)

    # Fetch forecast
    try:
        data = fetch_forecast(lat, lon)
    except ConnectionError as e:
        print(f"Error: Could not reach Open-Meteo API. {e}", file=sys.stderr)
        print("Check your internet connection and try again.", file=sys.stderr)
        sys.exit(1)
    except ValueError as e:
        print(f"Error parsing forecast data: {e}", file=sys.stderr)
        sys.exit(1)

    summary = build_summary(data, lat, lon, location_name)

    if args.json_output:
        print(json.dumps(summary, indent=2))
    else:
        print_human(summary)


if __name__ == "__main__":
    main()

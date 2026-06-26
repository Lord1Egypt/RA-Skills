#!/usr/bin/env python3
"""
natal_chart.py — Calculate natal chart from birth data.

Usage:
  python3 natal_chart.py --date "1993-05-13" --time "01:20" --tz "Australia/Brisbane" --lat -27.2308 --lon 153.0972
  python3 natal_chart.py --config natal.json

Outputs JSON with planetary positions, house cusps, and metadata.
Requires: pyswisseph (pip install pyswisseph)
"""

import argparse
import json
import sys
import math
from datetime import datetime

try:
    import swisseph as swe
except ImportError:
    print(json.dumps({"error": "pyswisseph not installed. Run: pip install pyswisseph"}))
    sys.exit(1)

SIGNS = [
    "Aries", "Taurus", "Gemini", "Cancer",
    "Leo", "Virgo", "Libra", "Scorpio",
    "Sagittarius", "Capricorn", "Aquarius", "Pisces",
]

PLANETS = {
    "Sun": swe.SUN, "Moon": swe.MOON, "Mercury": swe.MERCURY,
    "Venus": swe.VENUS, "Mars": swe.MARS, "Jupiter": swe.JUPITER,
    "Saturn": swe.SATURN, "Uranus": swe.URANUS, "Neptune": swe.NEPTUNE,
    "Pluto": swe.PLUTO, "North Node": swe.TRUE_NODE,
}


def calc_planet(jd, planet_id):
    try:
        result, ret_flag = swe.calc_ut(jd, planet_id, swe.FLG_SWIEPH)
        if ret_flag < 0:
            raise RuntimeError("Swiss Eph error")
        return result[0]
    except Exception:
        result, _ = swe.calc_ut(jd, planet_id, swe.FLG_MOSEPH)
        return result[0]


def sign_of(deg):
    return SIGNS[int(deg / 30) % 12]


def birth_to_jd_utc(date_str, time_str, tz_str):
    """Convert local birth date/time to Julian Day in UTC."""
    try:
        from zoneinfo import ZoneInfo
    except ImportError:
        from backports.zoneinfo import ZoneInfo

    local_dt = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
    tz = ZoneInfo(tz_str)
    local_dt = local_dt.replace(tzinfo=tz)
    utc_dt = local_dt.astimezone(ZoneInfo("UTC"))
    hour_frac = utc_dt.hour + utc_dt.minute / 60.0 + utc_dt.second / 3600.0
    return swe.julday(utc_dt.year, utc_dt.month, utc_dt.day, hour_frac)


def calculate_natal(date_str, time_str, tz_str, lat, lon):
    jd = birth_to_jd_utc(date_str, time_str, tz_str)

    # Planetary positions
    positions = {}
    for name, pid in PLANETS.items():
        deg = calc_planet(jd, pid)
        positions[name] = round(deg, 2)

    # South Node = opposite North Node
    positions["South Node"] = round((positions["North Node"] + 180) % 360, 2)

    # House cusps (Placidus)
    cusps, ascmc = swe.houses(jd, lat, lon, b'P')
    house_cusps = [round(c, 2) for c in cusps]
    positions["Ascendant"] = round(ascmc[0], 2)
    positions["Midheaven"] = round(ascmc[1], 2)

    # Build output
    chart = {
        "birth_data": {
            "date": date_str,
            "time": time_str,
            "timezone": tz_str,
            "latitude": lat,
            "longitude": lon,
        },
        "positions": positions,
        "house_cusps": house_cusps,
        "signs": {name: sign_of(deg) for name, deg in positions.items()},
    }
    return chart


def main():
    parser = argparse.ArgumentParser(description="Calculate natal chart")
    parser.add_argument("--config", help="Path to JSON config with birth data")
    parser.add_argument("--date", help="Birth date YYYY-MM-DD")
    parser.add_argument("--time", help="Birth time HH:MM (24h)")
    parser.add_argument("--tz", help="Timezone (e.g. Australia/Brisbane)")
    parser.add_argument("--lat", type=float, help="Birth latitude")
    parser.add_argument("--lon", type=float, help="Birth longitude")
    parser.add_argument("--save", help="Save chart to this file path")
    args = parser.parse_args()

    if args.config:
        with open(args.config) as f:
            cfg = json.load(f)
        date_str = cfg["date"]
        time_str = cfg["time"]
        tz_str = cfg["timezone"]
        lat = cfg["latitude"]
        lon = cfg["longitude"]
    elif args.date and args.time and args.tz and args.lat is not None and args.lon is not None:
        date_str = args.date
        time_str = args.time
        tz_str = args.tz
        lat = args.lat
        lon = args.lon
    else:
        parser.error("Provide either --config or all of --date --time --tz --lat --lon")
        return

    chart = calculate_natal(date_str, time_str, tz_str, lat, lon)

    if args.save:
        with open(args.save, "w") as f:
            json.dump(chart, f, indent=2)
        print("Natal chart saved to %s" % args.save)
    else:
        print(json.dumps(chart, indent=2))


if __name__ == "__main__":
    main()

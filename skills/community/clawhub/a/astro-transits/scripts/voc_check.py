#!/usr/bin/env python3
"""
voc_check.py - Check if Moon is currently void-of-course.

Void-of-course: Moon has made its last major aspect to any planet before
changing signs. Major aspects: conjunction (0), sextile (60), square (90),
trine (120), opposition (180). Orb <= 1.0 degree for "applying" detection.

Output JSON:
  {"voc": true, "start_time_utc": "...", "end_time_utc": "...", "duration_hours": X.X, "end_sign": "Aries"}
  {"voc": false}
"""

import json
import sys
from datetime import datetime, timezone, timedelta

try:
    import swisseph as swe
except ImportError:
    print(json.dumps({"error": "pyswisseph not installed"}))
    sys.exit(1)

PLANETS = [swe.SUN, swe.MERCURY, swe.VENUS, swe.MARS, swe.JUPITER,
           swe.SATURN, swe.URANUS, swe.NEPTUNE, swe.PLUTO]
PLANET_NAMES = {swe.SUN: "Sun", swe.MERCURY: "Mercury", swe.VENUS: "Venus",
                swe.MARS: "Mars", swe.JUPITER: "Jupiter", swe.SATURN: "Saturn",
                swe.URANUS: "Uranus", swe.NEPTUNE: "Neptune", swe.PLUTO: "Pluto"}
ASPECTS = [0, 60, 90, 120, 180]
VOC_ORB = 1.0
SIGNS = ["Aries","Taurus","Gemini","Cancer","Leo","Virgo",
         "Libra","Scorpio","Sagittarius","Capricorn","Aquarius","Pisces"]

def get_pos(jd, planet):
    flags = swe.FLG_SWIEPH | swe.FLG_SPEED
    try:
        result, _ = swe.calc_ut(jd, planet, flags)
    except Exception:
        result, _ = swe.calc_ut(jd, planet, swe.FLG_MOSEPH | swe.FLG_SPEED)
    return result[0], result[3]  # longitude, speed

def angle_diff(a, b):
    diff = abs(a - b) % 360
    if diff > 180:
        diff = 360 - diff
    return diff

def nearest_aspect(moon_lon, planet_lon):
    diffs = [(abs(angle_diff(moon_lon, planet_lon) - asp), asp)
             for asp in ASPECTS]
    return min(diffs, key=lambda x: x[0])

def sign_of(lon):
    return int(lon / 30)

def sign_ingress_time(jd_start, current_sign_idx):
    """Find JD when Moon enters the next sign via bisection."""
    target_sign = (current_sign_idx + 1) % 12
    jd_end = jd_start + 3.5
    lo, hi = jd_start, jd_end
    for _ in range(50):
        mid = (lo + hi) / 2
        lon, _ = get_pos(mid, swe.MOON)
        if sign_of(lon) == target_sign:
            hi = mid
        else:
            lo = mid
        if hi - lo < 1/86400:
            break
    return hi

def has_applying_aspect_before_ingress(jd_now, jd_ingress):
    """Check if Moon makes any applying major aspect to any planet before ingress."""
    step = 15 / (24 * 60)  # 15 minutes in JD
    jd = jd_now
    while jd < jd_ingress:
        jd = min(jd + step, jd_ingress)
        moon_lon, _ = get_pos(jd, swe.MOON)
        for planet in PLANETS:
            planet_lon, _ = get_pos(jd, planet)
            diff, asp = nearest_aspect(moon_lon, planet_lon)
            if diff <= VOC_ORB:
                return True, jd, planet, asp
    return False, None, None, None

def main():
    now_utc = datetime.now(timezone.utc)
    jd_now = swe.julday(now_utc.year, now_utc.month, now_utc.day,
                        now_utc.hour + now_utc.minute/60.0 + now_utc.second/3600.0)

    moon_lon, moon_speed = get_pos(jd_now, swe.MOON)
    current_sign_idx = sign_of(moon_lon)

    jd_ingress = sign_ingress_time(jd_now, current_sign_idx)
    next_sign = SIGNS[(current_sign_idx + 1) % 12]

    has_aspect, aspect_jd, aspect_planet, aspect_type = has_applying_aspect_before_ingress(jd_now, jd_ingress)

    if has_aspect:
        print(json.dumps({"voc": False}))
        return

    # Moon is void-of-course
    J2000 = 2451545.0
    ingress_dt = datetime(2000, 1, 1, 12, 0, 0, tzinfo=timezone.utc) + timedelta(days=jd_ingress - J2000)
    duration_hours = (jd_ingress - jd_now) * 24

    result = {
        "voc": True,
        "start_time_utc": now_utc.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "end_time_utc": ingress_dt.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "duration_hours": round(duration_hours, 1),
        "end_sign": next_sign,
        "moon_sign": SIGNS[current_sign_idx]
    }
    print(json.dumps(result))

if __name__ == "__main__":
    main()

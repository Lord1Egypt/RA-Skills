#!/usr/bin/env python3
"""
transits.py — Daily astrological transit calculator.

Usage:
  python3 transits.py --chart natal.json
  python3 transits.py --chart natal.json --date 2026-03-15
  python3 transits.py --chart natal.json --week

First generate a natal chart:
  python3 natal_chart.py --date "1993-05-13" --time "01:20" --tz "Australia/Brisbane" --lat -27.2308 --lon 153.0972 --save natal.json

Requires: pyswisseph (pip install pyswisseph)
"""

import argparse
import json
import sys
import math
from datetime import datetime, timedelta, timezone

try:
    import swisseph as swe
except ImportError:
    print("ERROR: pyswisseph not installed. Run: pip install pyswisseph")
    sys.exit(1)

SIGNS = [
    "Aries", "Taurus", "Gemini", "Cancer",
    "Leo", "Virgo", "Libra", "Scorpio",
    "Sagittarius", "Capricorn", "Aquarius", "Pisces",
]

TRANSIT_PLANETS = {
    "Sun": swe.SUN, "Moon": swe.MOON, "Mercury": swe.MERCURY,
    "Venus": swe.VENUS, "Mars": swe.MARS, "Jupiter": swe.JUPITER,
    "Saturn": swe.SATURN, "Uranus": swe.URANUS, "Neptune": swe.NEPTUNE,
    "Pluto": swe.PLUTO, "True Node": swe.TRUE_NODE,
}

PERSONAL_PLANETS = {"Sun", "Moon", "Mercury", "Venus", "Mars"}
ANGLE_POINTS = {"Ascendant", "Midheaven"}

ASPECTS = [
    (0, "conjunct", 8, 6, 10),
    (60, "sextile", 4, 4, 4),
    (90, "square", 7, 5, 7),
    (120, "trine", 7, 5, 7),
    (180, "opposite", 8, 6, 8),
]

ASPECT_MEANINGS = {
    ("Sun", "conjunct"): "vital identity, bold self-expression",
    ("Sun", "sextile"): "ease in showing up, creative flow",
    ("Sun", "square"): "identity tension, growth through friction",
    ("Sun", "trine"): "natural vitality, confidence flows",
    ("Sun", "opposite"): "awareness through contrast, visibility",
    ("Moon", "conjunct"): "emotional depth, instinct sharpened",
    ("Moon", "sextile"): "emotional ease, intuition opens",
    ("Moon", "square"): "emotional friction, feelings surface",
    ("Moon", "trine"): "inner peace, emotional support",
    ("Moon", "opposite"): "feeling vs reality, mirror moment",
    ("Mercury", "conjunct"): "sharp mind, key communications",
    ("Mercury", "sextile"): "clear thinking, good for dialogue",
    ("Mercury", "square"): "mental friction, rethink approach",
    ("Mercury", "trine"): "ideas flow, writing and speaking strong",
    ("Mercury", "opposite"): "listen as much as speak",
    ("Venus", "conjunct"): "beauty, connection, value aligned",
    ("Venus", "sextile"): "charm flows, good for relationships",
    ("Venus", "square"): "values tested, desire vs reality",
    ("Venus", "trine"): "harmony, creative magnetism",
    ("Venus", "opposite"): "relationship mirror, what you attract",
    ("Mars", "conjunct"): "energy surges, decisive action",
    ("Mars", "sextile"): "focused drive, productive momentum",
    ("Mars", "square"): "friction activates will, channel it",
    ("Mars", "trine"): "energy flows smoothly, act now",
    ("Mars", "opposite"): "others push back, assert clearly",
    ("Jupiter", "conjunct"): "expansion, luck, big picture opens",
    ("Jupiter", "sextile"): "opportunity knocks, take it",
    ("Jupiter", "square"): "overreach risk, but growth possible",
    ("Jupiter", "trine"): "growth comes easily, trust it",
    ("Jupiter", "opposite"): "excess vs balance, calibrate",
    ("Saturn", "conjunct"): "structure tested, commitment required",
    ("Saturn", "sextile"): "steady progress through discipline",
    ("Saturn", "square"): "hard work phase, results are real",
    ("Saturn", "trine"): "solid foundations, effort recognised",
    ("Saturn", "opposite"): "accountability moment, face reality",
    ("Uranus", "conjunct"): "sudden change, awakening arrives",
    ("Uranus", "sextile"): "innovation flows, fresh perspective",
    ("Uranus", "square"): "disruption demands flexibility",
    ("Uranus", "trine"): "inspired change, freedom opens",
    ("Uranus", "opposite"): "unexpected shifts, adapt or resist",
    ("Neptune", "conjunct"): "dissolution, dreams surface",
    ("Neptune", "sextile"): "intuition heightened, art inspired",
    ("Neptune", "square"): "confusion risk, ground yourself",
    ("Neptune", "trine"): "spiritual flow, imagination expands",
    ("Neptune", "opposite"): "illusion vs truth, clarity needed",
    ("Pluto", "conjunct"): "deep transformation, no going back",
    ("Pluto", "sextile"): "power used constructively",
    ("Pluto", "square"): "power struggle, ego death possible",
    ("Pluto", "trine"): "deep change, empowerment flows",
    ("Pluto", "opposite"): "power dynamics surface, own it",
    ("True Node", "conjunct"): "destiny activated, soul path opens",
    ("True Node", "sextile"): "karmic opportunity, say yes",
    ("True Node", "square"): "tension with direction, clarify",
    ("True Node", "trine"): "aligned with purpose, flow",
    ("True Node", "opposite"): "past vs future, choose forward",
}

PHASE_NAMES = [
    (0, "New Moon"), (45, "Waxing Crescent"), (90, "First Quarter"),
    (135, "Waxing Gibbous"), (180, "Full Moon"), (225, "Waning Gibbous"),
    (270, "Last Quarter"), (315, "Waning Crescent"), (360, "New Moon"),
]


def sign_of(deg):
    return SIGNS[int(deg / 30) % 12]

def deg_in_sign(deg):
    return deg % 30

def calc_planet(jd, planet_id):
    try:
        result, ret_flag = swe.calc_ut(jd, planet_id, swe.FLG_SWIEPH)
        if ret_flag < 0:
            raise RuntimeError("Swiss Eph error")
        return result[0]
    except Exception:
        result, _ = swe.calc_ut(jd, planet_id, swe.FLG_MOSEPH)
        return result[0]

def angular_diff(a, b):
    diff = abs(a - b) % 360
    return diff if diff <= 180 else 360 - diff

def house_of(lon, house_cusps):
    for i in range(12):
        c_start = house_cusps[i]
        c_end = house_cusps[(i + 1) % 12]
        if c_end < c_start:
            if lon >= c_start or lon < c_end:
                return i + 1
        else:
            if c_start <= lon < c_end:
                return i + 1
    return 1

def moon_phase(jd):
    sun_lon = calc_planet(jd, swe.SUN)
    moon_lon = calc_planet(jd, swe.MOON)
    angle = (moon_lon - sun_lon) % 360
    pct = round((1 - math.cos(math.radians(angle))) / 2 * 100, 1)
    for i, (thresh, name) in enumerate(PHASE_NAMES[:-1]):
        if angle < PHASE_NAMES[i + 1][0]:
            return pct, name
    return pct, "New Moon"

def significance(transit_planet, natal_point, orb, aspect_name):
    score = (10 - orb) * 10
    if transit_planet not in PERSONAL_PLANETS:
        score += 25
    if natal_point in ANGLE_POINTS:
        score += 40
    if natal_point in PERSONAL_PLANETS:
        score += 20
    if aspect_name in ("conjunct", "opposite"):
        score += 10
    return score

def check_stations(jd):
    stations = []
    for name, pid in TRANSIT_PLANETS.items():
        if name in ("Sun", "Moon", "True Node"):
            continue
        try:
            lon_before = calc_planet(jd - 1, pid)
            lon_after = calc_planet(jd + 1, pid)
            daily_motion = (lon_after - lon_before) / 2
            if abs(daily_motion) < 0.05:
                direction = "direct" if daily_motion > 0 else "retrograde"
                stations.append("%s stationing %s" % (name, direction))
        except Exception:
            pass
    return stations

def check_ingresses(jd):
    ingresses = []
    for name, pid in TRANSIT_PLANETS.items():
        try:
            lon_y = calc_planet(jd - 1, pid)
            lon_t = calc_planet(jd, pid)
            if int(lon_y / 30) != int(lon_t / 30):
                ingresses.append("%s enters %s" % (name, SIGNS[int(lon_t / 30) % 12]))
        except Exception:
            pass
    return ingresses

def theme_for(transit_planet, natal_point, aspect_name):
    p = transit_planet
    if p == "Pluto":
        return "transformation" if natal_point in ANGLE_POINTS else "depth"
    if p == "Jupiter":
        return "breakthrough" if natal_point in ANGLE_POINTS else "expansion"
    if p == "Saturn":
        return "tension" if aspect_name in ("square", "opposite") else "structure"
    if p == "Uranus":
        return "disruption" if aspect_name in ("square", "opposite") else "clarity"
    if p == "Neptune":
        return "vision" if aspect_name in ("conjunct", "trine", "sextile") else "release"
    if p == "Mars":
        return "friction" if aspect_name in ("square", "opposite") else "momentum"
    if p == "Mercury":
        return "clarity"
    if p == "Venus":
        return "connection"
    if p in ("Sun", "Moon"):
        return "vitality" if p == "Sun" else "release"
    return "momentum"


def run_daily(chart, target_date=None):
    natal = chart["positions"]
    cusps = chart["house_cusps"]

    if target_date:
        date = datetime.strptime(target_date, "%Y-%m-%d").date()
    else:
        date = datetime.now(timezone.utc).date()

    # Noon UTC
    jd = swe.julday(date.year, date.month, date.day, 12.0)

    transiting = {}
    for name, pid in TRANSIT_PLANETS.items():
        transiting[name] = calc_planet(jd, pid)

    moon_lon = transiting["Moon"]
    pct_illum, phase_name = moon_phase(jd)

    found = []
    for t_name, t_lon in transiting.items():
        for n_name, n_lon in natal.items():
            diff = angular_diff(t_lon, n_lon)
            for asp_angle, asp_name, orb_p, orb_o, orb_a in ASPECTS:
                asp_diff = abs(diff - asp_angle)
                if n_name in ANGLE_POINTS:
                    limit = orb_a
                elif t_name in PERSONAL_PLANETS or n_name in PERSONAL_PLANETS:
                    limit = orb_p
                else:
                    limit = orb_o
                if asp_diff <= limit:
                    orb = round(asp_diff, 1)
                    score = significance(t_name, n_name, orb, asp_name)
                    meaning = ASPECT_MEANINGS.get((t_name, asp_name), "notable activation")
                    found.append({
                        "transit": t_name, "aspect": asp_name,
                        "natal": n_name, "orb": orb,
                        "house": house_of(n_lon, cusps),
                        "score": score, "meaning": meaning,
                    })

    found.sort(key=lambda x: -x["score"])
    stations = check_stations(jd)
    ingresses = check_ingresses(jd)

    weekday = date.strftime("%A")
    date_str = date.strftime("%-d %B %Y")

    print("TRANSIT CONTEXT — %s %s" % (weekday, date_str))
    print("Moon: %s %.1f° — %s (%.1f%% illuminated)" % (
        sign_of(moon_lon), deg_in_sign(moon_lon), phase_name, pct_illum))
    print()
    print("Transits active today (ranked by significance):")

    for a in found[:8]:
        print("%s %s natal %s (orb %.1f°) [house %d] — %s" % (
            a["transit"], a["aspect"], a["natal"], a["orb"], a["house"], a["meaning"]))

    if not found:
        print("No major transits active today.")

    notable = "; ".join(stations + ingresses) or "None today"
    print()
    print("Notable: %s" % notable)


def run_weekly(chart, target_date=None):
    natal = chart["positions"]
    cusps = chart["house_cusps"]

    if target_date:
        today = datetime.strptime(target_date, "%Y-%m-%d").date()
    else:
        today = datetime.now(timezone.utc).date()

    # Next Monday
    days_until_monday = (7 - today.weekday()) % 7
    if days_until_monday == 0:
        days_until_monday = 7
    monday = today + timedelta(days=days_until_monday)
    week_dates = [monday + timedelta(days=i) for i in range(7)]

    transit_best = {}

    for date in week_dates:
        jd = swe.julday(date.year, date.month, date.day, 12.0)
        transiting = {}
        for pname, pid in TRANSIT_PLANETS.items():
            try:
                transiting[pname] = calc_planet(jd, pid)
            except Exception:
                pass

        for t_name, t_lon in transiting.items():
            for n_name, n_lon in natal.items():
                diff = angular_diff(t_lon, n_lon)
                for asp_angle, asp_name, orb_p, orb_o, orb_a in ASPECTS:
                    asp_diff = abs(diff - asp_angle)
                    if n_name in ANGLE_POINTS:
                        limit = orb_a
                    elif t_name in PERSONAL_PLANETS or n_name in PERSONAL_PLANETS:
                        limit = orb_p
                    else:
                        limit = orb_o
                    if asp_diff <= limit:
                        orb = round(asp_diff, 2)
                        key = (t_name, asp_name, n_name)
                        score = significance(t_name, n_name, orb, asp_name)
                        if key not in transit_best or orb < transit_best[key]["orb"]:
                            transit_best[key] = {
                                "orb": orb, "date": date, "score": score,
                                "transit": t_name, "aspect": asp_name, "natal": n_name,
                            }

    all_transits = list(transit_best.values())
    all_transits.sort(key=lambda x: -x["score"])

    sunday = week_dates[-1]
    print("WEEK AHEAD — %s to %s" % (monday.strftime("%-d %b"), sunday.strftime("%-d %b %Y")))

    for i, t in enumerate(all_transits[:3], 1):
        day = t["date"].strftime("%A")
        ds = t["date"].strftime("%-d %b")
        th = theme_for(t["transit"], t["natal"], t["aspect"])
        print("%d. %s %s natal %s — exact %s, %s — theme: %s" % (
            i, t["transit"], t["aspect"], t["natal"], day, ds, th))


def main():
    parser = argparse.ArgumentParser(description="Astrological transit calculator")
    parser.add_argument("--chart", required=True, help="Path to natal chart JSON (from natal_chart.py)")
    parser.add_argument("--date", help="Target date YYYY-MM-DD (default: today)")
    parser.add_argument("--week", action="store_true", help="Show weekly forecast instead of daily")
    args = parser.parse_args()

    with open(args.chart) as f:
        chart = json.load(f)

    if args.week:
        run_weekly(chart, args.date)
    else:
        run_daily(chart, args.date)


if __name__ == "__main__":
    main()

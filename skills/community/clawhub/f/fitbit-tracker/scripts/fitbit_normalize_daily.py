#!/usr/bin/env python3
"""Normalize Fitbit daily raw bundle into Wellness-like fields.

Usage:
  python3 scripts/fitbit_normalize_daily.py raw.json --out fitbit_day.json
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from typing import Any, Dict, Optional


def safe_get(d: Any, *keys):
    cur = d
    for k in keys:
        if not isinstance(cur, dict):
            return None
        cur = cur.get(k)
    return cur


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("raw")
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    raw = json.load(open(args.raw, "r", encoding="utf-8"))
    date = raw.get("requested_date")
    tz = raw.get("requested_tz")

    ep = raw.get("endpoints") or {}
    act = (ep.get("activity") or {}).get("data")
    slp = (ep.get("sleep") or {}).get("data")

    steps = safe_get(act, "summary", "steps")
    dist = None
    # Fitbit distance is in summary.distances list; pick "total" or first.
    distances = safe_get(act, "summary", "distances")
    if isinstance(distances, list) and distances:
        for x in distances:
            if isinstance(x, dict) and x.get("activity") == "total":
                dist = x.get("distance")
                break
        if dist is None and isinstance(distances[0], dict):
            dist = distances[0].get("distance")

    # Get full activity summary
    calories_out = safe_get(act, "summary", "caloriesOut")
    calories_bmr = safe_get(act, "summary", "caloriesBMR")
    activity_calories = safe_get(act, "summary", "activityCalories")
    sedentary_min = safe_get(act, "summary", "sedentaryMinutes")
    lightly_active = safe_get(act, "summary", "lightlyActiveMinutes")
    fairly_active = safe_get(act, "summary", "fairlyActiveMinutes")
    very_active = safe_get(act, "summary", "veryActiveMinutes")
    resting_hr = safe_get(act, "summary", "restingHeartRate")

    # Heart rate zones
    hr_zones = []
    for zone in safe_get(act, "summary", "heartRateZones") or []:
        if isinstance(zone, dict):
            hr_zones.append({
                "name": zone.get("name"),
                "minutes": zone.get("minutes"),
                "calories": zone.get("caloriesOut"),
                "min_hr": zone.get("min"),
                "max_hr": zone.get("max")
            })

    # Sleep data
    sleeps = safe_get(slp, "sleep")
    sleep_minutes = None
    sleep_score = None
    sleep_efficiency = None
    sleep_deep = None
    sleep_light = None
    sleep_rem = None
    sleep_wake = None
    time_in_bed = None
    nap_minutes = None

    if isinstance(sleeps, list) and sleeps:
        # Separate main sleep from naps (Fitbit returns nap before main sleep)
        main_records = [s for s in sleeps if s.get("isMainSleep")]
        nap_records = [s for s in sleeps if not s.get("isMainSleep")]

        # Main sleep
        s0 = main_records[0] if main_records else (sleeps[0] if isinstance(sleeps[0], dict) else None)
        if isinstance(s0, dict):
            sleep_minutes = s0.get("minutesAsleep")
            sleep_efficiency = s0.get("efficiency")
            time_in_bed = s0.get("timeInBed")
            # Sleep stages from summary
            stages = s0.get("levels", {}).get("summary", {}) if isinstance(s0.get("levels"), dict) else {}
            if isinstance(stages, dict):
                sleep_deep = stages.get("deep", {}).get("minutes") if isinstance(stages.get("deep"), dict) else None
                sleep_light = stages.get("light", {}).get("minutes") if isinstance(stages.get("light"), dict) else None
                sleep_rem = stages.get("rem", {}).get("minutes") if isinstance(stages.get("rem"), dict) else None
                sleep_wake = stages.get("wake", {}).get("minutes") if isinstance(stages.get("wake"), dict) else None
            # score may be in s0['sleepScore']['overallScore'] depending on API.
            ss = s0.get("sleepScore")
            if isinstance(ss, dict):
                sleep_score = ss.get("overallScore") or ss.get("score")

        # Nap (take first nap if multiple)
        if nap_records and isinstance(nap_records[0], dict):
            nap_minutes = nap_records[0].get("minutesAsleep") or nap_records[0].get("timeInBed")

    out: Dict[str, Any] = {
        "date": date,
        "timezone": tz,
        "generated_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "sleep": {
            "duration_minutes": sleep_minutes,
            "efficiency": sleep_efficiency,
            "time_in_bed_minutes": time_in_bed,
            "sleep_score": sleep_score,
            "deep_minutes": sleep_deep,
            "light_minutes": sleep_light,
            "rem_minutes": sleep_rem,
            "wake_minutes": sleep_wake,
            "nap_minutes": nap_minutes,
            "source": "fitbit",
        },
        "activity": {
            "steps": steps,
            "distance_km": dist,
            "calories_out": calories_out,
            "calories_bmr": calories_bmr,
            "activity_calories": activity_calories,
            "sedentary_minutes": sedentary_min,
            "lightly_active_minutes": lightly_active,
            "fairly_active_minutes": fairly_active,
            "very_active_minutes": very_active,
            "resting_heart_rate": resting_hr,
            "heart_rate_zones": hr_zones,
            "source": "fitbit",
        },
        "sources_present": ["fitbit"],
        "source": {"raw_files": [args.raw]},
    }

    json.dump(out, open(args.out, "w", encoding="utf-8"), indent=2, sort_keys=True)
    open(args.out, "a", encoding="utf-8").write("\n")


if __name__ == "__main__":
    main()

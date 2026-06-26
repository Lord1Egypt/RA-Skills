#!/usr/bin/env python3
"""fitbuddy - 初始化用户档案"""

import argparse
import json
import os
import sys
from datetime import datetime

DATA_DIR = os.path.join("fitbuddy-data")
PROFILE_PATH = os.path.join(DATA_DIR, "profile.json")

# Activity multipliers
ACTIVITY = {
    "sedentary": 1.200,
    "light": 1.375,
    "moderate": 1.550,
    "heavy": 1.725,
}

# Macro ratios per goal (g per kg bodyweight)
MACRO_PROFILES = {
    "cut":      {"protein": 2.0, "fat": 0.8},
    "bulk":     {"protein": 2.2, "fat": 1.0},
    "maintain": {"protein": 1.8, "fat": 1.0},
}

CALORIE_ADJUST = {"cut": -500, "bulk": 300, "maintain": 0}


def calc_bmr(gender, weight_kg, height_cm, age):
    bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age
    return bmr + 5 if gender == "male" else bmr - 161


def calc_tdee(bmr, activity_level):
    return bmr * ACTIVITY.get(activity_level, 1.2)


def calc_macros(goal, weight_kg, daily_cal):
    p = MACRO_PROFILES.get(goal, MACRO_PROFILES["maintain"])
    protein_g = round(weight_kg * p["protein"])
    fat_g = round(weight_kg * p["fat"])
    fat_cal = fat_g * 9
    protein_cal = protein_g * 4
    carbs_cal = daily_cal - protein_cal - fat_cal
    carbs_g = max(0, round(carbs_cal / 4))
    return {"protein_g": protein_g, "carbs_g": carbs_g, "fat_g": fat_g}


def init_profile(data_str):
    data = json.loads(data_str)

    gender = data["gender"]
    weight = float(data["weight_kg"])
    height = float(data["height_cm"])
    age = int(data["age"])
    goal = data.get("goal", "maintain")
    activity = data.get("activity_level", "sedentary")

    bmr = round(calc_bmr(gender, weight, height, age))
    tdee = round(calc_tdee(bmr, activity))
    daily_cal = round(tdee + CALORIE_ADJUST.get(goal, 0))
    macros = calc_macros(goal, weight, daily_cal)

    now = datetime.now().isoformat()

    profile = {
        "name": data.get("name", ""),
        "gender": gender,
        "age": age,
        "height_cm": height,
        "weight_kg": weight,
        "goal": goal,
        "target_weight_kg": data.get("target_weight_kg"),
        "target_date": data.get("target_date"),
        "activity_level": activity,
        "bmr": bmr,
        "tdee": tdee,
        "daily_calorie_target": daily_cal,
        "macros": macros,
        "reminders": data.get("reminders", {
            "weight": {"enabled": False, "time": "07:30", "channel": ""},
            "meals": {
                "breakfast": {"enabled": False, "time": "08:00"},
                "lunch": {"enabled": False, "time": "12:00"},
                "dinner": {"enabled": False, "time": "18:30"},
            },
            "water": {"enabled": False, "interval_hours": 2, "start_time": "08:00", "end_time": "22:00"},
        }),
        "channel": data.get("channel", {"type": "", "config": {}}),
        "created_at": now,
        "updated_at": now,
    }

    os.makedirs(DATA_DIR, exist_ok=True)
    with open(PROFILE_PATH, "w", encoding="utf-8") as f:
        json.dump(profile, f, ensure_ascii=False, indent=2)

    print(json.dumps(profile, ensure_ascii=False))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="fitbuddy init profile")
    parser.add_argument("--data", required=True, help="Profile data as JSON string")
    args = parser.parse_args()
    init_profile(args.data)

#!/usr/bin/env python3
"""fitbuddy - 计算工具 (BMR/TDEE/热量/营养素)"""

import argparse
import json
import sys

ACTIVITY = {
    "sedentary": 1.200,
    "light": 1.375,
    "moderate": 1.550,
    "heavy": 1.725,
}

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
    carbs_cal = daily_cal - protein_g * 4 - fat_g * 9
    carbs_g = max(0, round(carbs_cal / 4))
    return {"protein_g": protein_g, "carbs_g": carbs_g, "fat_g": fat_g}


# ── 碳循环 / 热量循环 ─────────────────────────────────────

CARB_CYCLING = {
    "high_carb":  {"carbs_g_per_kg": 3.5, "protein_g_per_kg": 2.0, "fat_g_per_kg": 0.7, "calorie_ratio": 1.0},
    "mid_carb":   {"carbs_g_per_kg": 2.0, "protein_g_per_kg": 2.0, "fat_g_per_kg": 0.9, "calorie_ratio": 0.92},
    "low_carb":   {"carbs_g_per_kg": 1.2, "protein_g_per_kg": 2.3, "fat_g_per_kg": 1.1, "calorie_ratio": 0.82},
}

CALORIE_CYCLING = {
    "training": {"calorie_ratio": 1.0},   # TDEE
    "rest":     {"calorie_ratio": 0.78},   # TDEE - ~500
}


def calc_daily_targets(profile, date_str=None):
    """根据 profile 和日期计算当日目标（支持碳循环/热量循环）。"""
    from datetime import datetime
    weight = profile["weight_kg"]
    bmr = profile.get("bmr", calc_bmr(profile["gender"], weight, profile["height_cm"], profile["age"]))
    tdee = profile.get("tdee", calc_tdee(bmr, profile.get("activity_level", "light")))
    goal = profile.get("goal", "maintain")
    base_cal = tdee + CALORIE_ADJUST.get(goal, 0)

    strategy = profile.get("diet_strategy", {}).get("type")
    if date_str is None:
        date_str = datetime.now().strftime("%Y-%m-%d")

    if strategy == "carb_cycling":
        dow = datetime.strptime(date_str, "%Y-%m-%d").strftime("%a").lower()[:3]
        day_map = {"mon": "mon", "tue": "tue", "wed": "wed", "thu": "thu",
                   "fri": "fri", "sat": "sat", "sun": "sun"}
        weekly = profile["diet_strategy"].get("weekly_plan", {})
        day_type = weekly.get(dow, "mid_carb")
        cfg = CARB_CYCLING.get(day_type, CARB_CYCLING["mid_carb"])
        protein_g = round(weight * cfg["protein_g_per_kg"])
        carbs_g = round(weight * cfg["carbs_g_per_kg"])
        fat_g = round(weight * cfg["fat_g_per_kg"])
        cal = round(base_cal * cfg["calorie_ratio"])
        return {
            "date": date_str,
            "day_of_week": dow,
            "day_type": day_type,
            "strategy": "carb_cycling",
            "daily_calorie_target": cal,
            "macros": {"protein_g": protein_g, "carbs_g": carbs_g, "fat_g": fat_g},
        }
    elif strategy == "calorie_cycling":
        # 简化版：按训练日/休息日区分
        dow = datetime.strptime(date_str, "%Y-%m-%d").strftime("%a").lower()[:3]
        weekly = profile["diet_strategy"].get("weekly_plan", {})
        day_type = weekly.get(dow, "rest")
        cfg = CALORIE_CYCLING.get(day_type, CALORIE_CYCLING["rest"])
        cal = round(base_cal * cfg["calorie_ratio"])
        macros = calc_macros(goal, weight, cal)
        return {
            "date": date_str,
            "day_of_week": dow,
            "day_type": day_type,
            "strategy": "calorie_cycling",
            "daily_calorie_target": cal,
            "macros": macros,
        }
    else:
        # 默认固定热量
        macros = calc_macros(goal, weight, base_cal)
        return {
            "date": date_str,
            "strategy": "fixed",
            "daily_calorie_target": round(base_cal),
            "macros": macros,
        }


def cmd_daily(args):
    """calc daily --profile <path> [--date YYYY-MM-DD]"""
    with open(args.profile, "r", encoding="utf-8") as f:
        profile = json.load(f)
    print(json.dumps(calc_daily_targets(profile, args.date), ensure_ascii=False))


def cmd_bmr(args):
    bmr = calc_bmr(args.gender, args.weight, args.height, args.age)
    print(json.dumps({"bmr": round(bmr)}, ensure_ascii=False))


def cmd_tdee(args):
    bmr = calc_bmr(args.gender, args.weight, args.height, args.age)
    tdee = calc_tdee(bmr, args.activity)
    print(json.dumps({"bmr": round(bmr), "tdee": round(tdee)}, ensure_ascii=False))


def cmd_calories(args):
    cal = args.protein * 4 + args.carbs * 4 + args.fat * 9
    print(json.dumps({
        "protein_g": args.protein, "carbs_g": args.carbs, "fat_g": args.fat,
        "calories": round(cal),
    }, ensure_ascii=False))


def cmd_macros(args):
    bmr = calc_bmr(args.gender, args.weight, args.height, args.age)
    tdee = calc_tdee(bmr, args.activity)
    daily_cal = tdee + CALORIE_ADJUST.get(args.goal, 0)
    macros = calc_macros(args.goal, args.weight, daily_cal)
    print(json.dumps({
        "bmr": round(bmr), "tdee": round(tdee),
        "daily_calorie_target": round(daily_cal),
        "macros": macros,
    }, ensure_ascii=False))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="fitbuddy calc")
    sub = parser.add_subparsers(dest="command")

    p_bmr = sub.add_parser("bmr")
    p_bmr.add_argument("--gender", required=True, choices=["male", "female"])
    p_bmr.add_argument("--weight", type=float, required=True)
    p_bmr.add_argument("--height", type=float, required=True)
    p_bmr.add_argument("--age", type=int, required=True)

    p_tdee = sub.add_parser("tdee")
    p_tdee.add_argument("--gender", required=True, choices=["male", "female"])
    p_tdee.add_argument("--weight", type=float, required=True)
    p_tdee.add_argument("--height", type=float, required=True)
    p_tdee.add_argument("--age", type=int, required=True)
    p_tdee.add_argument("--activity", required=True, choices=list(ACTIVITY.keys()))

    p_cal = sub.add_parser("calories")
    p_cal.add_argument("--protein", type=float, required=True)
    p_cal.add_argument("--carbs", type=float, required=True)
    p_cal.add_argument("--fat", type=float, required=True)

    p_mac = sub.add_parser("macros")
    p_mac.add_argument("--gender", required=True, choices=["male", "female"])
    p_mac.add_argument("--weight", type=float, required=True)
    p_mac.add_argument("--height", type=float, required=True)
    p_mac.add_argument("--age", type=int, required=True)
    p_mac.add_argument("--activity", required=True, choices=list(ACTIVITY.keys()))
    p_mac.add_argument("--goal", required=True, choices=["cut", "bulk", "maintain"])

    p_daily = sub.add_parser("daily")
    p_daily.add_argument("--profile", required=True, help="Path to profile.json")
    p_daily.add_argument("--date", default=None, help="Date YYYY-MM-DD")

    args = parser.parse_args()
    if args.command == "bmr":
        cmd_bmr(args)
    elif args.command == "tdee":
        cmd_tdee(args)
    elif args.command == "calories":
        cmd_calories(args)
    elif args.command == "macros":
        cmd_macros(args)
    elif args.command == "daily":
        cmd_daily(args)
    else:
        parser.print_help()

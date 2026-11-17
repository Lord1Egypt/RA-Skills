#!/usr/bin/env python3
"""Compute BMI, BMR (Mifflin-St Jeor), TDEE, calorie target, and macros.

Used by the fitness-assistant skill. Standard library only.
"""

import argparse
import json
import sys

ACTIVITY = {
    "sedentary": 1.2,
    "light": 1.375,
    "moderate": 1.55,
    "active": 1.725,
    "very": 1.9,
}

GOAL_ALIASES = {
    "lose": "lose",
    "loss": "lose",
    "cut": "lose",
    "maintain": "maintain",
    "maintenance": "maintain",
    "gain": "gain",
    "bulk": "gain",
}

FLOOR_KCAL = {"male": 1500, "female": 1200, "other": 1500}
MAX_LOSS_DEFICIT = 750
DEFAULT_PROTEIN_PER_KG = 1.8
PROTEIN_RANGE = (1.2, 2.5)
MIN_FAT_G_PER_KG = 0.6
FAT_PCT = (0.20, 0.35)


def normalize_goal(goal):
    key = goal.strip().lower()
    if key not in GOAL_ALIASES:
        sys.exit(f"Unknown goal '{goal}'. Choose from: lose, maintain, gain")
    return GOAL_ALIASES[key]


def compute(age, sex, height_cm, weight_kg, activity, goal, protein_per_kg):
    bmi = weight_kg / (height_cm / 100) ** 2

    if sex == "male":
        bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age + 5
    elif sex == "female":
        bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age - 161
    else:
        bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age - 78

    tdee = bmr * ACTIVITY[activity]

    if goal == "lose":
        target = tdee - 400
        if tdee - target > MAX_LOSS_DEFICIT:
            target = tdee - MAX_LOSS_DEFICIT
        floor = FLOOR_KCAL[sex]
        if target < floor:
            target = floor
    elif goal == "gain":
        target = tdee + 250
    else:
        target = tdee

    protein_g = weight_kg * protein_per_kg
    protein_kcal = protein_g * 4
    fat_kcal = max(target * FAT_PCT[0], MIN_FAT_G_PER_KG * weight_kg * 9)
    fat_kcal = min(fat_kcal, target * FAT_PCT[1])
    fat_g = fat_kcal / 9
    carbs_kcal = max(0.0, target - protein_kcal - fat_kcal)
    carbs_g = carbs_kcal / 4

    result = {
        "age": age,
        "sex": sex,
        "height_cm": height_cm,
        "weight_kg": weight_kg,
        "activity": activity,
        "goal": goal,
        "bmi": round(bmi, 1),
        "bmr_kcal": round(bmr),
        "tdee_kcal": round(tdee),
        "target_kcal": round(target),
        "protein_g": round(protein_g),
        "fat_g": round(fat_g),
        "carbs_g": round(carbs_g),
        "water_ml": round(weight_kg * 32),
        "notes": [],
    }

    if goal == "lose" and target == FLOOR_KCAL[sex]:
        result["notes"].append(
            f"Calorie target hit the safety floor of {FLOOR_KCAL[sex]} kcal/day."
        )
    if age < 18 or age > 65:
        result["notes"].append(
            "Age outside 18-65: plan conservatively and recommend professional guidance."
        )
    if bmi < 18.5:
        result["notes"].append(
            "BMI is low: consider a maintain/gain goal and professional review."
        )
    elif bmi > 30:
        result["notes"].append(
            "BMI is high: a slow, supervised approach is safer; consider professional review."
        )
    return result


def parse_args(argv):
    p = argparse.ArgumentParser(
        description="Compute BMI/BMR/TDEE/calorie/macro targets for fitness-assistant."
    )
    p.add_argument("--age", type=int, required=True, help="Age in years (10-100)")
    p.add_argument("--sex", choices=["male", "female", "other"], required=True)
    p.add_argument("--height", type=float, required=True, help="Height in current unit")
    p.add_argument("--weight", type=float, required=True, help="Weight in current unit")
    p.add_argument(
        "--unit",
        choices=["metric", "imperial"],
        default="metric",
        help="metric = cm/kg, imperial = in/lb (default: metric)",
    )
    p.add_argument(
        "--activity",
        choices=sorted(ACTIVITY),
        required=True,
        help="sedentary | light | moderate | active | very",
    )
    p.add_argument("--goal", required=True, help="lose | maintain | gain")
    p.add_argument(
        "--protein-per-kg",
        type=float,
        default=DEFAULT_PROTEIN_PER_KG,
        help=f"Protein g per kg body weight (default {DEFAULT_PROTEIN_PER_KG})",
    )
    p.add_argument("--json", action="store_true", help="Emit JSON only")
    args = p.parse_args(argv)

    if not 10 <= args.age <= 100:
        sys.exit("--age must be between 10 and 100")
    if args.unit == "imperial":
        height_cm = args.height * 2.54
        weight_kg = args.weight / 2.20462
    else:
        height_cm = args.height
        weight_kg = args.weight
    if not 100 <= height_cm <= 250:
        sys.exit("Height out of plausible range (100-250 cm)")
    if not 25 <= weight_kg <= 300:
        sys.exit("Weight out of plausible range (25-300 kg)")
    if not PROTEIN_RANGE[0] <= args.protein_per_kg <= PROTEIN_RANGE[1]:
        sys.exit(f"--protein-per-kg should be within {PROTEIN_RANGE}")
    return args, height_cm, weight_kg


def main(argv=None):
    args, height_cm, weight_kg = parse_args(argv or sys.argv[1:])
    goal = normalize_goal(args.goal)
    result = compute(
        args.age,
        args.sex,
        height_cm,
        weight_kg,
        args.activity,
        goal,
        args.protein_per_kg,
    )

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    lines = [
        f"BMI: {result['bmi']}",
        f"BMR: {result['bmr_kcal']} kcal",
        f"TDEE: {result['tdee_kcal']} kcal",
        f"Daily calorie target ({goal}): {result['target_kcal']} kcal",
        f"Macros: {result['protein_g']} g protein / {result['fat_g']} g fat / {result['carbs_g']} g carbs",
        f"Water target: ~{result['water_ml'] / 1000:.1f} L/day",
    ]
    if result["notes"]:
        lines.append("Notes: " + " ".join(result["notes"]))
    print("\n".join(lines))


if __name__ == "__main__":
    main()

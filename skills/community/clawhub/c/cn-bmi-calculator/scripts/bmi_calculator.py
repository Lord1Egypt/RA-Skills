#!/usr/bin/env python3
"""BMI Calculator - Calculate Body Mass Index with health assessment."""

import argparse
import json
import re
import sys

CATEGORIES = [
    (0, 18.5, "Underweight", "体重过轻"),
    (18.5, 25.0, "Normal", "体重正常"),
    (25.0, 30.0, "Overweight", "超重"),
    (30.0, 40.0, "Obese", "肥胖"),
    (40.0, 100.0, "Severely Obese", "重度肥胖"),
]

def parse_height(height_str):
    if "ft" in height_str.lower():
        match = re.match(r"(\d+(?:\.\d+)?)ft\s*(\d+(?:\.\d+)?)?in?", height_str.lower())
        if match:
            feet = float(match.group(1))
            inches = float(match.group(2) or 0)
            return (feet * 12 + inches) * 2.54
    return float(height_str)

def parse_weight(weight_str):
    if "lbs" in weight_str.lower():
        return float(re.sub(r"[^0-9.]", "", weight_str)) * 0.453592
    return float(weight_str)

def calculate_bmi(height_cm, weight_kg):
    height_m = height_cm / 100
    return round(weight_kg / (height_m ** 2), 1)

def get_category(bmi):
    for low, high, en, cn in CATEGORIES:
        if low <= bmi < high:
            return {"english": en, "chinese": cn}
    return {"english": "Unknown", "chinese": "未知"}

def healthy_range(height_cm):
    height_m = height_cm / 100
    low = round(18.5 * height_m ** 2, 1)
    high = round(24.9 * height_m ** 2, 1)
    return low, high

def main():
    parser = argparse.ArgumentParser(description="BMI Calculator")
    parser.add_argument("--height", required=True, help="Height (cm or ft-in)")
    parser.add_argument("--weight", required=True, help="Weight (kg or lbs)")
    args = parser.parse_args()

    try:
        height_cm = parse_height(args.height)
        weight_kg = parse_weight(args.weight)
        bmi = calculate_bmi(height_cm, weight_kg)
        category = get_category(bmi)
        low, high = healthy_range(height_cm)
        
        result = {
            "bmi": bmi,
            "category": category,
            "height_cm": round(height_cm, 1),
            "weight_kg": round(weight_kg, 1),
            "healthy_weight_range_kg": {"low": low, "high": high},
        }
        print(json.dumps(result, ensure_ascii=False, indent=2))
    except Exception as e:
        print(json.dumps({"error": str(e)}, ensure_ascii=False))
        sys.exit(1)

if __name__ == "__main__":
    main()

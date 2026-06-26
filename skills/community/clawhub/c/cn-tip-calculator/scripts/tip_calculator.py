#!/usr/bin/env python3
"""Tip Calculator - Calculate tips and split bills."""

import argparse
import json
import sys

COMMON_TIPS = [15, 18, 20, 25]

def calculate_tip(bill, tip_percent, split=1):
    tip_amount = round(bill * tip_percent / 100, 2)
    total = round(bill + tip_amount, 2)
    per_person = round(total / split, 2) if split > 1 else total
    tip_per_person = round(tip_amount / split, 2) if split > 1 else tip_amount
    
    return {
        "bill": bill,
        "tip_percent": tip_percent,
        "tip_amount": tip_amount,
        "total": total,
        "split": split,
        "per_person": per_person if split > 1 else None,
        "tip_per_person": tip_per_person if split > 1 else None,
        "common_tips": {p: round(bill * p / 100, 2) for p in COMMON_TIPS},
    }

def main():
    parser = argparse.ArgumentParser(description="Tip Calculator")
    parser.add_argument("--bill", type=float, required=True, help="Bill amount")
    parser.add_argument("--tip", type=float, default=18, help="Tip percentage (default: 18)")
    parser.add_argument("--split", type=int, default=1, help="Number of people to split")
    args = parser.parse_args()

    if args.bill <= 0:
        print(json.dumps({"error": "Bill must be positive"}))
        sys.exit(1)
    if args.tip < 0:
        print(json.dumps({"error": "Tip percentage cannot be negative"}))
        sys.exit(1)
    if args.split < 1:
        print(json.dumps({"error": "Split must be at least 1"}))
        sys.exit(1)

    result = calculate_tip(args.bill, args.tip, args.split)
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()

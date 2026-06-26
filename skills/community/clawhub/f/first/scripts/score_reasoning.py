#!/usr/bin/env python3
import argparse
import json
import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)

from lib.storage import load_cases, save_cases, append_promoted_pattern
from lib.reasoning import compute_score, infer_pattern_candidate, promotion_status

def main():
    parser = argparse.ArgumentParser(description="Score a saved reasoning case")
    parser.add_argument("--id", required=True, help="Case ID")
    args = parser.parse_args()

    data = load_cases()
    case = data["cases"].get(args.id)
    if not case:
        print(f"Case not found: {args.id}")
        sys.exit(1)

    case["score"] = compute_score(case)
    case["reusable_pattern_candidate"] = infer_pattern_candidate(case)
    case["promotion_status"] = promotion_status(case)
    data["cases"][args.id] = case
    save_cases(data)

    if case["promotion_status"] == "promoted":
        append_promoted_pattern(case)

    print("✓ Case scored:", args.id)
    print(json.dumps({
        "score": case["score"],
        "reusable_pattern_candidate": case["reusable_pattern_candidate"],
        "promotion_status": case["promotion_status"]
    }, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()

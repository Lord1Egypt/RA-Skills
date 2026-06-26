#!/usr/bin/env python3
"""
Decision Dynamo — Weighted Decision Matrix Calculator
Scores 2-4 options across 5 configurable criteria and prints a ranked result.
"""

import json
import sys


POSITIVE_CRITERIA = ["skill_leverage", "goal_alignment"]
NEGATIVE_CRITERIA = ["mental_drag", "financial_cost", "time_effort"]
ALL_CRITERIA = POSITIVE_CRITERIA + NEGATIVE_CRITERIA

CRITERIA_LABELS = {
    "skill_leverage":  "Skill / Leverage Gain",
    "goal_alignment":  "Long-term Goal Alignment",
    "mental_drag":     "Mental / Emotional Drag",
    "financial_cost":  "Financial / Resource Cost",
    "time_effort":     "Time and Effort",
}


def score_option(scores: dict, weights: dict) -> float:
    total = 0.0
    for c in POSITIVE_CRITERIA:
        total += scores[c] * weights[c]
    for c in NEGATIVE_CRITERIA:
        total += (11 - scores[c]) * weights[c]
    return round(total, 2)


def run(data: dict) -> None:
    weights = data["weights"]
    options = data["options"]

    results = []
    for opt in options:
        s = score_option(opt["scores"], weights)
        results.append({"name": opt["name"], "score": s})

    results.sort(key=lambda x: x["score"], reverse=True)

    print("\n=== Decision Dynamo Results ===\n")
    for rank, r in enumerate(results, 1):
        marker = " ✅ WINNER" if rank == 1 else ""
        print(f"  {rank}. {r['name']:<30} Score: {r['score']}{marker}")

    print("\n--- Criteria Weights ---")
    for c, w in weights.items():
        kind = "(positive)" if c in POSITIVE_CRITERIA else "(negative/inverted)"
        print(f"  {CRITERIA_LABELS[c]:<35} Weight: {w}  {kind}")

    print()


def interactive() -> None:
    print("\n=== Decision Dynamo — Interactive Mode ===\n")

    print("Step 1: Name your options (2-4, blank to stop):")
    option_names = []
    while len(option_names) < 4:
        name = input(f"  Option {len(option_names)+1}: ").strip()
        if not name and len(option_names) >= 2:
            break
        if name:
            option_names.append(name)

    print("\nStep 2: Set weights for each criterion (1-10):")
    weights = {}
    for c in ALL_CRITERIA:
        while True:
            try:
                w = int(input(f"  {CRITERIA_LABELS[c]}: "))
                if 1 <= w <= 10:
                    weights[c] = w
                    break
            except ValueError:
                pass
            print("  Please enter a number between 1 and 10.")

    options = []
    for name in option_names:
        print(f"\nStep 3: Score '{name}' for each criterion (1-10):")
        scores = {}
        for c in ALL_CRITERIA:
            while True:
                try:
                    s = int(input(f"  {CRITERIA_LABELS[c]}: "))
                    if 1 <= s <= 10:
                        scores[c] = s
                        break
                except ValueError:
                    pass
                print("  Please enter a number between 1 and 10.")
        options.append({"name": name, "scores": scores})

    run({"weights": weights, "options": options})


def main():
    if len(sys.argv) == 1:
        interactive()
    elif len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            data = json.load(f)
        run(data)
    else:
        print("Usage: decision_matrix.py [input.json]")
        print("       decision_matrix.py          (interactive mode)")
        sys.exit(1)


if __name__ == "__main__":
    main()

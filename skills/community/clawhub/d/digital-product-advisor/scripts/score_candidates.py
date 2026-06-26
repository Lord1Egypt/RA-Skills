#!/usr/bin/env python3
"""Score product candidates with weighted 0-10 dimensions.

Input JSON shape:
{
  "weights": {"anc": 0.25, "mic": 0.22},
  "candidates": [
    {"model": "...", "scores": {"anc": 8, "mic": 7}}
  ]
}

Unknown score fields are ignored and the denominator is renormalized.
"""

import argparse
import json
from pathlib import Path


def weighted_score(candidate, weights):
    scores = candidate.get("scores", {})
    total = 0.0
    denom = 0.0
    missing = []
    for key, weight in weights.items():
        value = scores.get(key)
        if value is None:
            missing.append(key)
            continue
        total += float(value) * float(weight)
        denom += float(weight)
    if denom == 0:
        return None, missing
    return round(total / denom, 2), missing


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="Path to candidate JSON")
    args = parser.parse_args()

    data = json.loads(Path(args.input).read_text(encoding="utf-8"))
    weights = data.get("weights", {})
    candidates = data.get("candidates", [])

    ranked = []
    for candidate in candidates:
        score, missing = weighted_score(candidate, weights)
        item = dict(candidate)
        item["weighted_score"] = score
        item["missing_score_fields"] = missing
        ranked.append(item)

    ranked.sort(key=lambda item: (-1 if item["weighted_score"] is None else -item["weighted_score"], item.get("price", 0)))
    print(json.dumps({"ranked_candidates": ranked}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

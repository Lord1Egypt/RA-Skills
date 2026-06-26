#!/usr/bin/env python3
"""Edu Homework Grader · end-to-end pipeline."""
from __future__ import annotations
import argparse, json, sys
from pathlib import Path
from grade_objective import grade_objective
from grade_subjective import grade_subjective


def run(homework: dict, key: dict, rubric: dict | None = None) -> dict:
    results = []
    total_earned = 0
    total_max = 0
    for item in homework["items"]:
        ans_key = key.get(item["id"], {})
        if item["type"] in ("MC", "FIB", "TF"):
            res = grade_objective(item, ans_key)
        else:
            res = grade_subjective(item, ans_key, rubric)
        total_earned += res["earned"]
        total_max += res["max"]
        results.append(res)
    return {
        "student": homework.get("student", "anonymous"),
        "score": total_earned,
        "max_score": total_max,
        "percentage": round(total_earned / total_max * 100, 2) if total_max else 0.0,
        "items": results,
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True)
    ap.add_argument("--answer-key", required=True)
    ap.add_argument("--rubric", default=None)
    ap.add_argument("--output", default="-")
    args = ap.parse_args()
    hw = json.loads(Path(args.input).read_text(encoding="utf-8"))
    key = json.loads(Path(args.answer_key).read_text(encoding="utf-8"))
    rub = json.loads(Path(args.rubric).read_text(encoding="utf-8")) if args.rubric else None
    result = run(hw, key, rub)
    text = json.dumps(result, ensure_ascii=False, indent=2)
    if args.output == "-":
        print(text)
    else:
        Path(args.output).write_text(text, encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())

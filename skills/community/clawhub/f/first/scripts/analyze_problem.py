#!/usr/bin/env python3
import argparse
import json
import os
import sys
from datetime import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)

from lib.storage import load_cases, save_cases, generate_case_id, ensure_storage, append_case_index, append_promoted_pattern
from lib.reasoning import (
    clean_title,
    infer_goal,
    infer_assumptions,
    infer_truths,
    infer_components,
    infer_constraints,
    detect_anti_patterns,
    select_heuristics,
    infer_rebuilt_solution,
    infer_next_actions,
    infer_pattern_candidate,
    promotion_status,
    compute_score
)

def now_iso():
    return datetime.utcnow().isoformat()

def main():
    parser = argparse.ArgumentParser(description="Analyze a problem using first principles")
    parser.add_argument("--text", required=True, help="Problem statement")
    parser.add_argument("--title", help="Optional title")
    args = parser.parse_args()

    ensure_storage()
    data = load_cases()
    case_id = generate_case_id()
    title = args.title.strip() if args.title else clean_title(args.text)

    case = {
        "id": case_id,
        "title": title,
        "problem": args.text.strip(),
        "goal": infer_goal(args.text),
        "assumptions": infer_assumptions(args.text),
        "truths": infer_truths(args.text),
        "components": infer_components(args.text),
        "constraints": infer_constraints(args.text),
        "anti_patterns": detect_anti_patterns(args.text),
        "heuristics_used": select_heuristics(args.text),
        "reusable_pattern_candidate": "",
        "promotion_status": "none",
        "rebuilt_solution": infer_rebuilt_solution(args.text),
        "next_actions": infer_next_actions(args.text),
        "score": {},
        "created_at": now_iso(),
        "updated_at": now_iso()
    }

    case["score"] = compute_score(case)
    case["reusable_pattern_candidate"] = infer_pattern_candidate(case)
    case["promotion_status"] = promotion_status(case)

    data["cases"][case_id] = case
    save_cases(data)
    append_case_index(case)

    if case["promotion_status"] == "promoted":
        append_promoted_pattern(case)

    print(f"✓ Case created: {case_id}")
    print(json.dumps(case, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()

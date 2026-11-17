#!/usr/bin/env python3
"""Create a module-scoped analysis worksheet without inventing unsupported findings."""

import argparse
import json
from pathlib import Path


MODULE_QUESTIONS = {
    "snapshot": ["What positioning and target audience are directly supported?", "What changed recently?"],
    "product": ["Which decision-relevant capabilities are present, partial, not found publicly, or not applicable?", "What adoption blockers are supported?"],
    "pricing": ["Are currency, period, unit, commitment, and workload comparable?", "Which values remain unknown?"],
    "reviews": ["Which themes recur and with what sample size?", "What source or segment bias applies?"],
    "hiring": ["Which role concentrations are factual?", "Which investment signals are inference only?"],
    "landscape": ["Which players are direct, adjacent, substitutes, or build alternatives?", "What whitespace is a hypothesis?"],
    "battlecard": ["What strengths and objections have evidence?", "Which claims must sales avoid?"],
}


def build_worksheet(evidence: list[dict]) -> dict:
    groups = {}
    for item in evidence:
        key = f'{item["module"]}:{item["entity"]}'
        groups.setdefault(key, {"module": item["module"], "entity": item["entity"], "evidence_ids": [], "questions": MODULE_QUESTIONS.get(item["module"], [])})
        groups[key]["evidence_ids"].append(item["evidence_id"])
    return {"status": "analysis_required", "groups": list(groups.values()), "findings": []}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("evidence", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    evidence = json.loads(args.evidence.read_text(encoding="utf-8"))
    worksheet = build_worksheet(evidence)
    payload = json.dumps(worksheet, ensure_ascii=False, indent=2) + "\n"
    output = args.output or args.evidence.with_name("analysis-workbook.json")
    output.write_text(payload, encoding="utf-8")
    print(payload, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

from __future__ import annotations

import argparse
import json
from pathlib import Path

WEIGHTS = {
    "originality": 20,
    "reader_value": 20,
    "evidence_readiness": 15,
    "timeliness": 15,
    "position_fit": 15,
    "portfolio_contribution": 10,
    "execution_feasibility": 5,
}


def weighted(raw: int, maximum: int) -> float:
    return round(max(0, min(5, raw)) / 5 * maximum, 2)


def score_topic(topic: dict) -> dict:
    raw = topic.get("raw_scores", {})
    base = round(sum(weighted(int(raw.get(key, 0)), max_value) for key, max_value in WEIGHTS.items()), 2)
    deductions = topic.get("deductions", [])
    deduction_total = round(sum(float(item.get("points", 0)) for item in deductions), 2)
    net = round(max(0, base - deduction_total), 2)
    gates = topic.get("gates", {})
    blocking = any(str(value).startswith(("BLOCK", "NEEDS_INPUT")) for value in gates.values())
    if blocking:
        priority = "P3"
        action = "ABANDON"
    elif net >= 82 and raw.get("evidence_readiness", 0) >= 4 and raw.get("originality", 0) >= 4:
        priority = "P0"
        action = "WRITE_NOW"
    elif net >= 70:
        priority = "P1"
        action = "BACKUP"
    elif net >= 50:
        priority = "P2"
        action = "WATCH"
    else:
        priority = "P3"
        action = "ABANDON"
    return {**topic, "base_score": base, "deduction_total": deduction_total, "net_score": net, "priority": priority, "action": action}


def main() -> int:
    parser = argparse.ArgumentParser(description="Calculate topic portfolio scores")
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    data = json.loads(Path(args.input).read_text(encoding="utf-8"))
    topics = data.get("topics", data if isinstance(data, list) else [])
    result = {"topics": [score_topic(topic) for topic in topics]}
    Path(args.output).write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"topics": len(result["topics"])}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

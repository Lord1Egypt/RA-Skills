#!/usr/bin/env python3
import argparse
import json
from pathlib import Path


PRIORITY = {"low": 0, "medium": 1, "high": 2}
SCOPE = {"single-task": 0, "project": 1, "workspace": 2, "cross-session": 3}
WORTH = {"low": 0, "medium": 1, "high": 2}


def load_jsonl(path: Path):
    items = []
    if not path.exists():
        return items
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line:
            items.append(json.loads(line))
    return items


def score_priority(item: dict) -> int:
    base = 0
    base += PRIORITY.get(item.get("reuse_value", "low"), 0) * 3
    base += PRIORITY.get(item.get("confidence", "low"), 0) * 2
    base += SCOPE.get(item.get("impact_scope", "single-task"), 0)
    base += WORTH.get(item.get("promotion_worthiness", "low"), 0) * 2
    if item.get("type") in {"correction", "regression", "decision"}:
        base += 2
    return base


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("input", help="Scored JSONL")
    ap.add_argument("-o", "--output", help="Output JSON")
    args = ap.parse_args()

    items = load_jsonl(Path(args.input))
    backlog = []
    for item in items:
        backlog.append({
            "id": item.get("id"),
            "summary": item.get("summary", ""),
            "type": item.get("type", "discovery"),
            "reuse_value": item.get("reuse_value", "low"),
            "confidence": item.get("confidence", "low"),
            "impact_scope": item.get("impact_scope", "single-task"),
            "promotion_worthiness": item.get("promotion_worthiness", "low"),
            "targets": item.get("promotion_target_candidates", []),
            "priority_score": score_priority(item),
        })

    backlog.sort(key=lambda x: (-x["priority_score"], x["summary"].lower()))
    result = {
        "count": len(backlog),
        "items": backlog,
    }
    text = json.dumps(result, ensure_ascii=False, indent=2)
    if args.output:
        Path(args.output).write_text(text + "\n", encoding="utf-8")
    else:
        print(text)


if __name__ == "__main__":
    main()

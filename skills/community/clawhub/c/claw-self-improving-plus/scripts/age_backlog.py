#!/usr/bin/env python3
import argparse
import json
from datetime import datetime, timezone
from pathlib import Path


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def days_old(ts: str | None) -> int | None:
    if not ts:
        return None
    try:
        dt = datetime.fromisoformat(ts.replace("Z", "+00:00"))
    except ValueError:
        return None
    now = datetime.now(timezone.utc)
    return max(0, (now - dt).days)


def stale_label(days: int | None) -> str:
    if days is None:
        return "unknown"
    if days >= 30:
        return "stale"
    if days >= 7:
        return "aging"
    return "fresh"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("backlog", help="Backlog JSON from build_backlog.py")
    ap.add_argument("scored", help="Scored or consolidated JSONL with timestamps")
    ap.add_argument("-o", "--output", help="Output JSON")
    args = ap.parse_args()

    backlog = load_json(Path(args.backlog))
    ts_by_id = {}
    for line in Path(args.scored).read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        item = json.loads(line)
        ts_by_id[item.get("id")] = item.get("timestamp")

    updated = []
    for item in backlog.get("items", []):
        ts = ts_by_id.get(item.get("id"))
        age = days_old(ts)
        row = dict(item)
        row["timestamp"] = ts
        row["age_days"] = age
        row["stale_status"] = stale_label(age)
        if row["stale_status"] == "stale":
            row["priority_score"] = max(0, row.get("priority_score", 0) - 2)
        updated.append(row)

    updated.sort(key=lambda x: (-x.get("priority_score", 0), x.get("age_days") if x.get("age_days") is not None else 10**9))
    result = {"count": len(updated), "items": updated}
    text = json.dumps(result, ensure_ascii=False, indent=2)
    if args.output:
        Path(args.output).write_text(text + "\n", encoding="utf-8")
    else:
        print(text)


if __name__ == "__main__":
    main()

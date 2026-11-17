from __future__ import annotations

import argparse
import json
from pathlib import Path

ALLOWED_ACTIONS = {"WRITE_NOW", "BACKUP", "MERGE", "WATCH", "SHORT_NOTE", "COVERED_TRACK", "ABANDON"}
ALLOWED_PRIORITIES = {"P0", "P1", "P2", "P3"}


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate an approved topic change set")
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--enforce", action="store_true")
    args = parser.parse_args()
    data = json.loads(Path(args.input).read_text(encoding="utf-8"))
    changes = data.get("changes", [])
    issues: list[str] = []
    ids: set[str] = set()
    for index, change in enumerate(changes, 1):
        page_id = change.get("page_id") or change.get("topic_id")
        if not page_id:
            issues.append(f"change {index}: missing page_id/topic_id")
        elif page_id in ids:
            issues.append(f"change {index}: duplicate page_id/topic_id")
        else:
            ids.add(page_id)
        if change.get("action") not in ALLOWED_ACTIONS:
            issues.append(f"change {index}: invalid action")
        if change.get("priority") not in ALLOWED_PRIORITIES:
            issues.append(f"change {index}: invalid priority")
        if not change.get("reason"):
            issues.append(f"change {index}: missing reason")
    primary = [item for item in changes if item.get("action") == "WRITE_NOW"]
    backups = [item for item in changes if item.get("action") == "BACKUP"]
    if len(primary) != 1:
        issues.append(f"portfolio must contain exactly 1 primary, got {len(primary)}")
    if len(backups) != 2:
        issues.append(f"portfolio must contain exactly 2 backups, got {len(backups)}")
    result = {"status": "pass" if not issues else "fail", "changes": len(changes), "issues": issues}
    Path(args.output).write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False))
    if args.enforce and issues:
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

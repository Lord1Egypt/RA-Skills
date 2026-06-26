#!/usr/bin/env python3
"""Create a machine-readable browser evidence session manifest."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path


def dedupe(values: list[str]) -> list[str]:
    seen: set[str] = set()
    out: list[str] = []
    for value in values:
        normalized = value.strip()
        if not normalized or normalized in seen:
            continue
        seen.add(normalized)
        out.append(normalized)
    return out


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", required=True, help="Output JSON file.")
    parser.add_argument("--session-id", required=True, help="Stable identifier for this browser run.")
    parser.add_argument("--app", required=True, help="Public app or product name.")
    parser.add_argument("--goal", required=True, help="What the browser run is trying to verify or reproduce.")
    parser.add_argument("--base-url", default="", help="Optional base URL under test.")
    parser.add_argument("--run-context", default="manual", help="manual, openclaw, playwright, or similar.")
    parser.add_argument("--environment", default="prod", help="prod, staging, local, or similar.")
    parser.add_argument("--surface", action="append", default=[], help="Repeatable app surface such as login or checkout.")
    parser.add_argument("--tag", action="append", default=[], help="Repeatable tag for grouping sessions.")
    args = parser.parse_args()

    out_path = Path(args.out).expanduser().resolve()
    out_path.parent.mkdir(parents=True, exist_ok=True)

    payload = {
        "schema_version": "1.0",
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "session": {
            "session_id": args.session_id.strip(),
            "app": args.app.strip(),
            "goal": args.goal.strip(),
            "base_url": args.base_url.strip(),
            "run_context": args.run_context.strip() or "manual",
            "environment": args.environment.strip() or "prod",
            "surfaces": dedupe(args.surface),
            "tags": dedupe(args.tag),
        },
        "steps": [],
        "summary": {
            "status": "in_progress",
            "passed_steps": 0,
            "failed_steps": 0,
            "blocked_steps": 0,
            "issue_keys": [],
        },
    }

    out_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(out_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

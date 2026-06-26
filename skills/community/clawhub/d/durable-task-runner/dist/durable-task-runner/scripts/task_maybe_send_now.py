#!/usr/bin/env python3
"""
Conditionally emit an immediate status update after meaningful task state changes.

This exists so task_ctl.py can trigger visible breadcrumbs without creating
recursive send loops.
"""

from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
STATE_DIR = ROOT / "state" / "tasks"
CONFIG_PATH = ROOT / "config" / "defaults.json"
SCRIPT_DIR = ROOT / "scripts"


def load_json(path: Path, default: Any = None) -> Any:
    if not path.exists():
        return default
    return json.loads(path.read_text())


def has_delivery_binding(task: dict[str, Any]) -> bool:
    for item in task.get("artifacts", []):
        if isinstance(item, dict) and item.get("kind") == "delivery_binding":
            return True
    return False


def immediate_allowed(defaults: dict[str, Any], event_type: str) -> bool:
    reporting = defaults.get("reporting", {})
    mapping = {
        "milestone": reporting.get("immediate_updates_on_milestone", False),
        "phase": reporting.get("immediate_updates_on_phase_change", False),
        "blocker": reporting.get("immediate_updates_on_blocker", False),
        "retry": reporting.get("immediate_updates_on_retry", False),
        "resume": reporting.get("immediate_updates_on_resume", False),
        "completion": reporting.get("immediate_updates_on_completion", False),
        "control": True,
    }
    return bool(mapping.get(event_type, False))


def extract_json_object(raw: str) -> dict[str, Any]:
    raw = raw.strip()
    starts = [i for i, ch in enumerate(raw) if ch == "{"]
    best: dict[str, Any] | None = None
    for start in starts:
        depth = 0
        in_string = False
        escape = False
        for idx in range(start, len(raw)):
            ch = raw[idx]
            if in_string:
                if escape:
                    escape = False
                elif ch == "\\":
                    escape = True
                elif ch == '"':
                    in_string = False
                continue
            if ch == '"':
                in_string = True
                continue
            if ch == "{":
                depth += 1
            elif ch == "}":
                depth -= 1
                if depth == 0:
                    candidate = raw[start:idx + 1]
                    try:
                        value = json.loads(candidate)
                    except json.JSONDecodeError:
                        break
                    if isinstance(value, dict):
                        best = value
                    break
    if best is not None:
        return best
    raise SystemExit(f"could not parse JSON payload from output: {raw}")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("task_id")
    ap.add_argument("event_type")
    ap.add_argument("--force", action="store_true")
    args = ap.parse_args()

    task = load_json(STATE_DIR / f"{args.task_id}.json", None)
    if not task:
        raise SystemExit(f"task not found: {args.task_id}")
    defaults = load_json(CONFIG_PATH, {})

    if not has_delivery_binding(task):
        print(json.dumps({"sent": False, "reason": "no_delivery_binding"}, indent=2))
        return 0
    if not args.force and not immediate_allowed(defaults, args.event_type):
        print(json.dumps({"sent": False, "reason": f"disabled_for_{args.event_type}"}, indent=2))
        return 0

    out = subprocess.check_output([
        "python3", str(SCRIPT_DIR / "task_send_status.py"), args.task_id,
        "--kind", "immediate",
        "--reason", args.event_type,
    ], text=True)
    payload = extract_json_object(out)
    print(json.dumps({"sent": True, "reason": args.event_type, "delivery": payload}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

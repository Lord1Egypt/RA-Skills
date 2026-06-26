#!/usr/bin/env python3
"""
Build the canonical status snapshot for durable-task-runner.

Purpose:
- provide a single source of truth for ticker/render/send/batch layers
- keep progress math deterministic and centralized
- expose one structured payload that every higher layer can consume
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
STATE_DIR = ROOT / "state" / "tasks"
CONFIG_PATH = ROOT / "config" / "defaults.json"


def load_json(path: Path, default: Any = None) -> Any:
    if not path.exists():
        return default
    return json.loads(path.read_text())


def load_task(task_id: str) -> dict[str, Any]:
    path = STATE_DIR / f"{task_id}.json"
    if not path.exists():
        raise SystemExit(f"task not found: {task_id}")
    return json.loads(path.read_text())


def progress_bar(percent: int, width: int = 10) -> str:
    percent = max(0, min(100, percent))
    filled = round((percent / 100) * width)
    return "[" + ("#" * filled) + ("." * (width - filled)) + "]"


def milestone_counts(task: dict[str, Any]) -> tuple[int, int]:
    milestones = task.get("milestones", [])
    done = sum(1 for m in milestones if m.get("status") == "done")
    return done, len(milestones)


def current_milestone_record(task: dict[str, Any]) -> dict[str, Any] | None:
    for milestone in task.get("milestones", []):
        if milestone.get("status") == "running":
            return milestone
    return None


def overall_percent(task: dict[str, Any]) -> int:
    milestones = task.get("milestones", [])
    if not milestones:
        return 0
    vals = [int(m.get("percent", 0)) for m in milestones]
    return round(sum(vals) / len(vals))


def current_task_percent(task: dict[str, Any]) -> int:
    milestone = current_milestone_record(task)
    if milestone is not None:
        return int(milestone.get("percent", 0))
    milestones = task.get("milestones", [])
    if milestones and all(m.get("status") == "done" for m in milestones):
        return 100
    done, total = milestone_counts(task)
    if total:
        return round((done / total) * 100)
    return 0


def current_milestone_title(task: dict[str, Any]) -> str:
    milestone = current_milestone_record(task)
    if milestone is not None:
        return milestone.get("title", "running")
    return "none"


def build_snapshot(task_id: str) -> dict[str, Any]:
    task = load_task(task_id)
    defaults = load_json(CONFIG_PATH, {})
    current_pct = current_task_percent(task)
    overall_pct = overall_percent(task)
    done, total = milestone_counts(task)
    interval = int(task.get("status_update_interval_seconds") or defaults.get("reporting", {}).get("status_update_interval_seconds", 300))
    return {
        "task_id": task_id,
        "title": task.get("title", task_id),
        "desired_state": task.get("desired_state", "running"),
        "phase": task.get("phase", "?"),
        "health": task.get("health", "?"),
        "next_step": task.get("next_step", "n/a"),
        "status_update_interval_seconds": interval,
        "last_status_update_at": task.get("last_status_update_at"),
        "current": {
            "percent": current_pct,
            "bar": progress_bar(current_pct),
            "milestone": current_milestone_title(task),
        },
        "overall": {
            "percent": overall_pct,
            "bar": progress_bar(overall_pct),
            "milestones_done": done,
            "milestones_total": total,
        },
    }


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("task_id")
    args = p.parse_args()
    print(json.dumps(build_snapshot(args.task_id), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

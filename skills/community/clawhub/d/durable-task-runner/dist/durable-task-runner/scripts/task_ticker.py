#!/usr/bin/env python3
"""
Compact timed status renderer for durable-task-runner.

Goal:
- minimal tokens
- maximum signal
- suitable for recurring status delivery regardless of milestone
- show both current-task progress and overall-project progress
- remain fully programmatic and independent of human commentary
"""

from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT_DIR = ROOT / "scripts"


def load_snapshot(task_id: str) -> dict:
    out = subprocess.check_output(["python3", str(SCRIPT_DIR / "task_status_snapshot.py"), task_id], text=True)
    return json.loads(out)


def render(snapshot: dict) -> str:
    current = snapshot["current"]
    overall = snapshot["overall"]
    return (
        f"task {current['bar']} {current['percent']:>3}% | "
        f"proj {overall['bar']} {overall['percent']:>3}% | "
        f"ms {overall['milestones_done']}/{overall['milestones_total']} | "
        f"{snapshot['phase']} | {snapshot['health']} | {current['milestone']} | next: {snapshot['next_step']}"
    )


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("task_id")
    args = p.parse_args()
    print(render(load_snapshot(args.task_id)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

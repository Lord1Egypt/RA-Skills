#!/usr/bin/env python3
"""
Build a minimal subagent worker brief for durable-task-runner.

Purpose:
- keep spawn glue thin and explicit
- reuse the controller-managed line metadata
- avoid hiding orchestration behind a giant wrapper too early

Current scope:
- render the exact worker prompt/body for a given task line
- optional shell-friendly JSON output for future automation glue
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
STATE_DIR = ROOT / "state" / "tasks"


def load_task(task_id: str) -> dict[str, Any]:
    path = STATE_DIR / f"{task_id}.json"
    if not path.exists():
        raise SystemExit(f"task not found: {task_id}")
    return json.loads(path.read_text())


def get_line(task: dict[str, Any], line_name: str) -> dict[str, Any]:
    for item in task.get("artifacts", []):
        if isinstance(item, dict) and item.get("kind") == "subagent_lines":
            line = item.get("lines", {}).get(line_name)
            if line:
                return line
    raise SystemExit(f"line not found: {line_name}")


def render_prompt(task: dict[str, Any], line_name: str, line: dict[str, Any]) -> str:
    return f"""You are a worker for durable-task-runner.

Return using exactly these headers first:
tag: autopilot | done | idle | blocked | handoff | need_user
task_id: {task['task_id']}
line: {line_name}
node: {line.get('node', 'n/a')}
goal_status: partial | complete | waiting | blocked
next_role: main | verify | research | worker | user | none

Worker goal:
{line.get('goal', '')}

Task title:
{task.get('title', task['task_id'])}

Task phase:
{task.get('phase', '')}

Line summary:
{line.get('summary', '') or 'n/a'}

Current next step from controller:
{task.get('next_step', '') or 'n/a'}

Keep the body short and include:
1. Goal
2. Completed
3. Changed artifacts/files
4. Current status
5. Next step
6. Risk
""".rstrip()


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("task_id")
    p.add_argument("line")
    p.add_argument("--json", action="store_true")
    args = p.parse_args()

    task = load_task(args.task_id)
    line = get_line(task, args.line)
    prompt = render_prompt(task, args.line, line)
    if args.json:
        print(json.dumps({
            "task_id": args.task_id,
            "line": args.line,
            "prompt": prompt,
            "owner": line.get("owner", "worker"),
            "node": line.get("node", "n/a"),
        }, indent=2))
    else:
        print(prompt)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

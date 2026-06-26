#!/usr/bin/env python3
"""
Prepare a minimal subagent-run payload for durable-task-runner.

Purpose:
- keep orchestration glue explicit and inspectable
- avoid hand-assembling worker prompts each time
- let the controller manage the durable line state first, then emit a ready-to-use
  spawn payload for OpenClaw `sessions_spawn`

Current scope:
- optionally assign/update the line in task state
- render the worker prompt from controller-managed metadata
- print a JSON payload that can be used with `sessions_spawn`

This script does not call OpenClaw tools directly; it only prepares the payload.
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
STATE_DIR = ROOT / "state" / "tasks"
ALLOWED_OWNERS = {"worker", "research", "verify", "main"}


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def task_path(task_id: str) -> Path:
    return STATE_DIR / f"{task_id}.json"


def events_path(task_id: str) -> Path:
    return STATE_DIR / f"{task_id}.events.jsonl"


def progress_path(task_id: str) -> Path:
    return STATE_DIR / f"{task_id}.progress.log"


def load_task(task_id: str) -> dict[str, Any]:
    path = task_path(task_id)
    if not path.exists():
        raise SystemExit(f"task not found: {task_id}")
    return json.loads(path.read_text())


def write_task(task: dict[str, Any]) -> None:
    task_path(task["task_id"]).write_text(json.dumps(task, indent=2) + "\n")


def append_event(task_id: str, event: dict[str, Any]) -> None:
    p = events_path(task_id)
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("a", encoding="utf-8") as f:
        f.write(json.dumps(event) + "\n")


def append_progress(task_id: str, line: str) -> None:
    p = progress_path(task_id)
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("a", encoding="utf-8") as f:
        f.write(f"[{now_iso()}] {line}\n")


def ensure_orchestration_artifact(task: dict[str, Any]) -> dict[str, Any]:
    artifacts = task.setdefault("artifacts", [])
    for item in artifacts:
        if isinstance(item, dict) and item.get("kind") == "subagent_lines":
            item.setdefault("lines", {})
            return item
    artifact = {"kind": "subagent_lines", "lines": {}}
    artifacts.append(artifact)
    return artifact


def ensure_line(task: dict[str, Any], line_name: str, goal: str, owner: str, node: str, summary: str) -> dict[str, Any]:
    if owner not in ALLOWED_OWNERS:
        raise SystemExit(f"unsupported owner: {owner}")
    artifact = ensure_orchestration_artifact(task)
    lines = artifact["lines"]
    ts = now_iso()
    line = lines.get(line_name, {})
    line.update({
        "line": line_name,
        "goal": goal,
        "owner": owner,
        "node": node,
        "status": "assigned",
        "goal_status": "partial",
        "next_role": owner,
        "assigned_at": line.get("assigned_at", ts),
        "updated_at": ts,
        "summary": summary,
        "artifacts": line.get("artifacts", []),
        "controller_decision": "dispatch",
        "controller_note": "spawn payload prepared",
    })
    lines[line_name] = line
    task["updated_at"] = ts
    write_task(task)
    append_event(task["task_id"], {
        "ts": ts,
        "type": "subtask_assigned",
        "task_id": task["task_id"],
        "phase": task.get("phase", ""),
        "status": "ok",
        "details": {
            "line": line_name,
            "owner": owner,
            "node": node,
            "goal": goal,
            "summary": summary,
            "source": "task_subagent_run.py",
        },
    })
    append_progress(task["task_id"], f"prepared spawn payload for line {line_name} ({owner} @ {node})")
    return line


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


def build_spawn_payload(task: dict[str, Any], line_name: str, prompt: str, timeout_seconds: int) -> dict[str, Any]:
    return {
        "runtime": "subagent",
        "agentId": "main",
        "mode": "run",
        "cleanup": "delete",
        "timeoutSeconds": timeout_seconds,
        "runTimeoutSeconds": timeout_seconds,
        "task": prompt,
        "metadata": {
            "task_id": task["task_id"],
            "line": line_name,
        },
    }


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("task_id")
    p.add_argument("line")
    p.add_argument("goal")
    p.add_argument("--owner", default="worker")
    p.add_argument("--node", default="start")
    p.add_argument("--summary", default="")
    p.add_argument("--timeout-seconds", type=int, default=120)
    args = p.parse_args()

    task = load_task(args.task_id)
    line = ensure_line(task, args.line, args.goal, args.owner, args.node, args.summary)
    prompt = render_prompt(task, args.line, line)
    payload = build_spawn_payload(task, args.line, prompt, args.timeout_seconds)
    print(json.dumps(payload, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

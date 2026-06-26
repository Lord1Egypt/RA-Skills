\
#!/usr/bin/env python3
"""
Rate-limited ClawHub publisher.

Features:
- Reads queue JSON: {"items":[{"path":"/abs/skill","command":"clawhub publish \"{path}\""}]}
- Enforces max 5 attempts in any rolling 3600 seconds
- Supports --dry-run and --execute
- Stores state in adjacent .publisher-state.json by default
- Logs each attempt
"""

from __future__ import annotations

import argparse
import json
import os
import shlex
import subprocess
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List

MAX_PER_HOUR = 5
WINDOW_SECONDS = 3600
DEFAULT_COMMAND = 'clawhub publish "{path}"'


@dataclass
class QueueItem:
    path: str
    command: str


def load_json(path: Path) -> Dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise SystemExit(f"Queue/state file not found: {path}")
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid JSON in {path}: {exc}")


def save_json(path: Path, data: Dict[str, Any]) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def normalize_items(queue_data: Dict[str, Any]) -> List[QueueItem]:
    items = queue_data.get("items")
    if not isinstance(items, list):
        raise SystemExit('Queue JSON must contain an "items" array.')
    normalized: List[QueueItem] = []
    for index, item in enumerate(items):
        if not isinstance(item, dict):
            raise SystemExit(f"Queue item #{index} must be an object.")
        path = item.get("path")
        if not isinstance(path, str) or not path.strip():
            raise SystemExit(f'Queue item #{index} missing non-empty "path".')
        command = item.get("command", DEFAULT_COMMAND)
        if not isinstance(command, str) or "{path}" not in command:
            raise SystemExit(f'Queue item #{index} has invalid "command"; it must be a string containing "{{path}}".')
        normalized.append(QueueItem(path=path, command=command))
    return normalized


def ensure_skill_dir(path_str: str) -> Path:
    path = Path(path_str).expanduser().resolve()
    if not path.exists():
        raise SystemExit(f"Skill path does not exist: {path}")
    if not path.is_dir():
        raise SystemExit(f"Skill path is not a directory: {path}")
    if not (path / "SKILL.md").exists():
        raise SystemExit(f"Skill directory does not contain SKILL.md: {path}")
    return path


def prune_attempts(attempts: List[Dict[str, Any]], now: float) -> List[Dict[str, Any]]:
    cutoff = now - WINDOW_SECONDS
    return [a for a in attempts if float(a.get("ts", 0)) >= cutoff]


def next_pending_index(state: Dict[str, Any], items: List[QueueItem]) -> int | None:
    statuses = state.setdefault("statuses", {})
    for i, item in enumerate(items):
        key = str(i)
        st = statuses.get(key, {}).get("status", "pending")
        if st not in {"published", "skipped"}:
            return i
    return None


def run_publish(item: QueueItem, execute: bool) -> subprocess.CompletedProcess[str] | None:
    skill_path = ensure_skill_dir(item.path)
    command_str = item.command.format(path=str(skill_path))
    print(f"[info] command: {command_str}")
    if not execute:
        return None
    return subprocess.run(
        command_str,
        shell=True,
        text=True,
        capture_output=True,
        check=False,
        cwd=str(skill_path.parent),
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Rate-limited ClawHub skill publisher.")
    parser.add_argument("--queue", required=True, help="Path to queue JSON")
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--dry-run", action="store_true", help="Validate and print the next command without executing")
    mode.add_argument("--execute", action="store_true", help="Execute the next publish command")
    parser.add_argument("--state", help="Path to state JSON (default: alongside queue as .publisher-state.json)")
    args = parser.parse_args()

    queue_path = Path(args.queue).expanduser().resolve()
    state_path = Path(args.state).expanduser().resolve() if args.state else queue_path.with_name(".publisher-state.json")

    queue_data = load_json(queue_path)
    items = normalize_items(queue_data)

    state: Dict[str, Any] = {"attempts": [], "statuses": {}}
    if state_path.exists():
        state = load_json(state_path)
        if not isinstance(state, dict):
            raise SystemExit(f"State file must be a JSON object: {state_path}")
        state.setdefault("attempts", [])
        state.setdefault("statuses", {})

    now = time.time()
    state["attempts"] = prune_attempts(state.get("attempts", []), now)
    remaining = MAX_PER_HOUR - len(state["attempts"])
    print(f"[info] rolling-window attempts in last hour: {len(state['attempts'])}/{MAX_PER_HOUR}")

    if remaining <= 0:
        earliest = min(float(a.get("ts", now)) for a in state["attempts"])
        wait_seconds = int((earliest + WINDOW_SECONDS) - now)
        print(f"[warn] hourly cap reached; next slot in about {max(wait_seconds, 0)} seconds")
        save_json(state_path, state)
        return 0

    idx = next_pending_index(state, items)
    if idx is None:
        print("[info] queue complete; nothing pending")
        save_json(state_path, state)
        return 0

    item = items[idx]
    try:
        skill_path = ensure_skill_dir(item.path)
    except SystemExit as exc:
        state["statuses"][str(idx)] = {"status": "failed", "reason": str(exc), "updatedAt": int(now)}
        save_json(state_path, state)
        print(f"[error] {exc}")
        return 2

    print(f"[info] next skill: {skill_path}")
    result = run_publish(item, execute=args.execute)

    if args.dry_run:
        state["statuses"].setdefault(str(idx), {"status": "pending"})
        save_json(state_path, state)
        print("[info] dry-run complete")
        return 0

    attempt_record = {"ts": now, "index": idx, "path": str(skill_path)}
    state["attempts"].append(attempt_record)

    if result is None:
        state["statuses"][str(idx)] = {"status": "failed", "reason": "internal execute error", "updatedAt": int(now)}
        save_json(state_path, state)
        return 3

    stdout = result.stdout.strip()
    stderr = result.stderr.strip()

    if stdout:
        print("[stdout]")
        print(stdout)
    if stderr:
        print("[stderr]", file=sys.stderr)
        print(stderr, file=sys.stderr)

    if result.returncode == 0:
        state["statuses"][str(idx)] = {"status": "published", "updatedAt": int(now)}
        save_json(state_path, state)
        print("[info] publish succeeded")
        return 0

    state["statuses"][str(idx)] = {
        "status": "failed",
        "code": result.returncode,
        "updatedAt": int(now),
        "stderr": stderr[-2000:],
        "stdout": stdout[-2000:],
    }
    save_json(state_path, state)
    print(f"[error] publish failed with exit code {result.returncode}")
    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())

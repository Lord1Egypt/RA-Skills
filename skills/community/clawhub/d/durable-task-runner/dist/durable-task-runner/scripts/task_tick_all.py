#!/usr/bin/env python3
"""
Run recurring maintenance across all eligible durable tasks.

Purpose:
- provide the missing operational runner for recurring status delivery
- drive lightweight continuation checks for running tasks
- scan all task snapshots
- skip tasks that are not active or do not have delivery bindings when reporting
- only send when the task is actually due
- treat per-task delivery/parser failures as task-local errors instead of aborting the full sweep
- do not emit misleading recurring bars for tasks that were just reclassified as stale/paused
"""

from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
STATE_DIR = ROOT / "state" / "tasks"
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


def iter_tasks() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for path in sorted(STATE_DIR.glob("*.json")):
        data = load_json(path, None)
        if isinstance(data, dict) and data.get("task_id"):
            rows.append(data)
    return rows


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
    raise ValueError(f"could not parse JSON payload from output: {raw}")


def run_json(*args: str) -> dict[str, Any]:
    proc = subprocess.run(list(args), text=True, capture_output=True, check=True)
    combined = "\n".join(part for part in [proc.stdout.strip(), proc.stderr.strip()] if part).strip()
    return extract_json_object(combined)


def main() -> int:
    scanned = 0
    eligible = 0
    sent = 0
    errors = 0
    continued = 0
    results = []

    for task in iter_tasks():
        scanned += 1
        task_id = task["task_id"]
        if task.get("desired_state") != "running":
            results.append({"task_id": task_id, "status": "skipped", "reason": "not_running"})
            continue

        try:
            cont = run_json("python3", str(SCRIPT_DIR / "task_auto_continue.py"), task_id)
            continued += 1
        except subprocess.CalledProcessError as exc:
            errors += 1
            results.append({
                "task_id": task_id,
                "status": "error",
                "reason": "auto_continue_failed",
                "command": exc.cmd,
                "returncode": exc.returncode,
                "stdout": (exc.stdout or "").strip(),
                "stderr": (exc.stderr or "").strip(),
            })
            continue
        except Exception as exc:
            errors += 1
            results.append({
                "task_id": task_id,
                "status": "error",
                "reason": "auto_continue_exception",
                "message": str(exc),
            })
            continue

        result = {"task_id": task_id, "continuation": cont}
        cont_status = cont.get("status")
        if cont_status in {"paused", "standby", "skipped"}:
            result.update({"status": "skipped", "reason": cont.get("reason", cont_status)})
            results.append(result)
            continue

        refreshed = load_json(STATE_DIR / f"{task_id}.json", task)
        if refreshed.get("desired_state") != "running":
            result.update({"status": "skipped", "reason": "no_longer_running"})
            results.append(result)
            continue

        if not has_delivery_binding(refreshed):
            result.update({"status": "skipped", "reason": "no_delivery_binding"})
            results.append(result)
            continue

        eligible += 1
        try:
            due = run_json("python3", str(SCRIPT_DIR / "task_should_report.py"), task_id)
            if not due.get("due"):
                result.update({"status": "skipped", "reason": due.get("reason", "not_due")})
                results.append(result)
                continue
            delivery = run_json("python3", str(SCRIPT_DIR / "task_send_status.py"), task_id)
            sent += 1
            result.update({
                "status": "sent",
                "reason": due.get("reason", "due"),
                "line": delivery.get("line", ""),
                "method": (delivery.get("delivery") or {}).get("method", "unknown"),
            })
            results.append(result)
        except subprocess.CalledProcessError as exc:
            errors += 1
            result.update({
                "status": "error",
                "reason": "command_failed",
                "command": exc.cmd,
                "returncode": exc.returncode,
                "stdout": (exc.stdout or "").strip(),
                "stderr": (exc.stderr or "").strip(),
            })
            results.append(result)
        except Exception as exc:
            errors += 1
            result.update({
                "status": "error",
                "reason": type(exc).__name__,
                "message": str(exc),
            })
            results.append(result)

    print(json.dumps({
        "scanned": scanned,
        "eligible": eligible,
        "continued": continued,
        "sent": sent,
        "errors": errors,
        "results": results,
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

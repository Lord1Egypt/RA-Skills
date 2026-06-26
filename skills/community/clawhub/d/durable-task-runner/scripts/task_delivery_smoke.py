#!/usr/bin/env python3
"""
Targeted smoke coverage for delivery behavior.

Covers:
- stdout delivery mode
- noop delivery mode
- immediate-send helper on a bound task
- no-delivery-binding skip behavior
- due-scan skip behavior without recursion or crashes
"""

from __future__ import annotations

import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT_DIR = ROOT / "scripts"


def now_tag() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")


def run(*args: str, input_text: str | None = None) -> str:
    proc = subprocess.run(list(args), text=True, input=input_text, capture_output=True, check=True)
    return proc.stdout


def extract_json_object(raw: str) -> dict:
    raw = raw.strip()
    starts = [i for i, ch in enumerate(raw) if ch == "{"]
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
                        return value
                    break
    raise SystemExit(f"could not parse JSON object from output: {raw}")


def create_task(task_id: str, method: str | None) -> None:
    artifacts = [] if method is None else [{"kind": "delivery_binding", "method": method}]
    run(
        "python3", str(SCRIPT_DIR / "task_ctl.py"), "create", task_id,
        "--title", f"Delivery smoke {task_id}",
        "--goal", "Exercise delivery behavior safely",
        "--done-criteria", '["delivery path exercised"]',
        "--constraints", '["local-only", "non-destructive"]',
        "--desired-state", "running",
        "--execution-priority", "tokens",
        "--phase", "delivery-smoke",
        "--health", "healthy",
        "--next-step", "exercise delivery path",
        "--milestones", '[{"id":"d1","title":"Exercise delivery","status":"running","percent":50}]',
        "--artifacts", json.dumps(artifacts),
    )


def main() -> int:
    stdout_id = f"delivery-stdout-{now_tag()}"
    noop_id = f"delivery-noop-{now_tag()}"
    unbound_id = f"delivery-unbound-{now_tag()}"

    create_task(stdout_id, "stdout")
    create_task(noop_id, "noop")
    create_task(unbound_id, None)

    stdout_send = extract_json_object(run("python3", str(SCRIPT_DIR / "task_send_status.py"), stdout_id, "--kind", "immediate", "--reason", "phase"))
    if stdout_send["delivery"]["method"] != "stdout":
        raise SystemExit(f"stdout method mismatch: {stdout_send}")
    if "update:phase | task [" not in stdout_send["line"]:
        raise SystemExit(f"stdout line missing expected prefix: {stdout_send}")

    noop_send = json.loads(run("python3", str(SCRIPT_DIR / "task_send_status.py"), noop_id))
    if noop_send["delivery"]["method"] != "noop":
        raise SystemExit(f"noop method mismatch: {noop_send}")
    if noop_send["delivery"].get("reason") != "noop_mode":
        raise SystemExit(f"noop reason mismatch: {noop_send}")

    immediate = json.loads(run("python3", str(SCRIPT_DIR / "task_maybe_send_now.py"), stdout_id, "phase"))
    if not immediate.get("sent"):
        raise SystemExit(f"immediate send did not fire: {immediate}")

    unbound = json.loads(run("python3", str(SCRIPT_DIR / "task_maybe_send_now.py"), unbound_id, "phase"))
    if unbound.get("sent"):
        raise SystemExit(f"unbound task should not send: {unbound}")
    if unbound.get("reason") != "no_delivery_binding":
        raise SystemExit(f"unexpected unbound reason: {unbound}")

    tick = json.loads(run("python3", str(SCRIPT_DIR / "task_tick_all.py")))
    seen = {item["task_id"]: item for item in tick["results"]}
    if stdout_id not in seen or noop_id not in seen or unbound_id not in seen:
        raise SystemExit(f"tick results missing smoke tasks: {tick}")

    print(json.dumps({
        "ok": True,
        "stdout_task": stdout_id,
        "noop_task": noop_id,
        "unbound_task": unbound_id,
        "stdout_send": stdout_send["delivery"],
        "noop_send": noop_send["delivery"],
        "unbound": unbound,
        "tick_subset": {
            stdout_id: seen[stdout_id],
            noop_id: seen[noop_id],
            unbound_id: seen[unbound_id],
        },
    }, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())

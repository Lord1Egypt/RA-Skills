#!/usr/bin/env python3
"""High-level: submit a Browse Anything task, wait for it, return the result.

This is the recommended entry point for almost all use cases. Use the
lower-level scripts only if you need fine-grained control (manual
polling, mid-task input, screenshots while running, etc.).

Usage:
    python3 browse.py "Find the cheapest direct flight from Paris to Tokyo next month and return the airline + price."
    python3 browse.py --model gpt-5.2 --max-steps 60 --proxy us "Prompt..."
    python3 browse.py --json "Prompt..."           # emit final task JSON
    python3 browse.py --timeout 1200 "Prompt..."   # wait up to 20 min
    cat prompt.txt | python3 browse.py -           # read prompt from stdin

Exits 0 on success, 1 on task failure, 2 on auth/usage error,
3 on network error, 4 on timeout, 5 if the task is waiting for
human input (use submit_input.py to provide it).
"""
from __future__ import annotations

import argparse
import sys
import time

from _client import ApiError, print_json, request


TERMINAL_STATUSES = {"completed", "failed", "cancelled"}


def main() -> int:
    p = argparse.ArgumentParser(description="Run a Browse Anything task end-to-end.")
    p.add_argument("prompt", help="Natural language task. Use '-' to read from stdin.")
    p.add_argument("--model", help="LLM model override (e.g. gpt-5.2, kimi-k2.6).")
    p.add_argument("--max-steps", type=int, help="Max agent steps (default 80).")
    p.add_argument("--proxy", dest="proxy_location", help="Proxy region, e.g. us, eu.")
    p.add_argument("--metadata", help="Optional JSON metadata to attach to the task.")
    p.add_argument("--timeout", type=int, default=900,
                   help="Seconds to wait for completion (default 900).")
    p.add_argument("--poll-interval", type=int, default=4,
                   help="Seconds between status polls (default 4).")
    p.add_argument("--json", action="store_true",
                   help="Print the final task JSON instead of a friendly summary.")
    args = p.parse_args()

    prompt = sys.stdin.read().strip() if args.prompt == "-" else args.prompt
    if not prompt:
        sys.stderr.write("ERROR: empty prompt.\n")
        return 2

    body: dict = {"prompt": prompt}
    if args.model:
        body["model"] = args.model
    if args.max_steps:
        body["max_steps"] = args.max_steps
    if args.proxy_location:
        body["proxy_location"] = args.proxy_location
    if args.metadata:
        import json as _json
        try:
            body["metadata"] = _json.loads(args.metadata)
        except _json.JSONDecodeError as e:
            sys.stderr.write(f"ERROR: --metadata must be valid JSON: {e}\n")
            return 2

    try:
        created = request("POST", "/api/v1/tasks", body=body)
    except ApiError as e:
        sys.stderr.write(f"Failed to create task: {e}\n")
        return 2 if e.status in (401, 402, 403) else 1

    task_id = created["task"]["id"]
    sys.stderr.write(f"Task {task_id} queued. Polling...\n")

    deadline = time.time() + args.timeout
    last_status = None
    while True:
        if time.time() > deadline:
            sys.stderr.write(
                f"Timed out after {args.timeout}s. Task still {last_status}.\n"
                f"Check later: python3 get_task.py {task_id}\n"
            )
            return 4

        try:
            payload = request("GET", f"/api/v1/tasks/{task_id}")
        except ApiError as e:
            sys.stderr.write(f"Status poll failed: {e}\n")
            return 1

        task = payload["task"]
        status = task.get("status")
        if status != last_status:
            sys.stderr.write(f"  status: {status}\n")
            last_status = status

        if status == "requires_input":
            sys.stderr.write(
                "Task is waiting for human input. Question:\n"
                f"  {task.get('human_input_request')}\n\n"
                "Provide an answer with:\n"
                f"  python3 submit_input.py {task_id} \"<your answer>\"\n"
            )
            if args.json:
                print_json(task)
            return 5

        if status in TERMINAL_STATUSES:
            if args.json:
                print_json(task)
                return 0 if status == "completed" else 1

            if status == "completed":
                result = task.get("result") or {}
                sys.stdout.write(
                    (result.get("description") or "(no description)").rstrip() + "\n"
                )
                if result.get("url"):
                    sys.stdout.write(f"\nFinal URL:   {result['url']}\n")
                if result.get("title"):
                    sys.stdout.write(f"Final title: {result['title']}\n")
                sys.stderr.write(
                    f"\nDone in {task.get('execution_time_ms', 0)} ms / "
                    f"{task.get('step_count', 0)} steps.\n"
                    f"Task id: {task_id}\n"
                )
                return 0

            sys.stderr.write(
                f"Task {status}: {task.get('error_message') or '(no message)'}\n"
            )
            return 1

        time.sleep(args.poll_interval)


if __name__ == "__main__":
    sys.exit(main())

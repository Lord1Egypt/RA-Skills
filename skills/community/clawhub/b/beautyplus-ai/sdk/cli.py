#!/usr/bin/env python3
"""BeautyPlus AI SDK CLI - simplified command line interface"""

import argparse
import json
import os
import sys
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent
if str(PROJECT_DIR) not in sys.path:
    sys.path.insert(0, str(PROJECT_DIR))

# Keep CLI behavior aligned with scripts/beautyplus_ai.py:
# auto-load BP_AK / BP_SK from scripts/.env if env vars are not set.
def _load_env_file() -> None:
    # scripts/.env lives next to scripts/ directory in the repo root.
    candidates = [
        PROJECT_DIR / "scripts" / ".env",
        Path.cwd() / ".env",
    ]
    for env_path in candidates:
        if not env_path.exists():
            continue
        try:
            with open(env_path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith("#") or "=" not in line:
                        continue
                    key, value = line.split("=", 1)
                    key = key.strip()
                    value = value.strip().strip("\"'")
                    # Do not override explicitly exported env vars.
                    if key and key not in os.environ:
                        os.environ[key] = value
        except OSError:
            pass
        break


_load_env_file()

from sdk import SkillClient
from sdk.core.config import INVOKE
from sdk.core.client import ConsumeDeniedError


def _print(data: dict) -> None:
    print(json.dumps(data, indent=2, ensure_ascii=False))


def _task_succeeded(result: dict) -> bool:
    """Check if task succeeded."""
    if not isinstance(result, dict):
        return False
    if result.get("skill_status") == "failed" or result.get("error"):
        return False
    if result.get("skill_status") == "completed":
        return True
    if result.get("output_urls"):
        return True
    data = result.get("data")
    if isinstance(data, dict) and data.get("status") in (10, 2, 20):
        return True
    return False


def _handle(func):
    """Unified error-handling wrapper."""
    try:
        return func()
    except ConsumeDeniedError as e:
        _print({"error": "quota_error", "code": e.code, "message": e.msg})
        return 1
    except Exception as e:
        _print({"error": str(e)})
        return 1


def run_task(ak: str, sk: str, task: str, source: str, params: str = None) -> int:
    """Run a task end-to-end: upload → consume → submit → poll."""
    def _do():
        client = SkillClient(ak=ak, sk=sk)
        p = json.loads(params) if params else {}
        result = client.run_task(task_name=task, image_path=source or "", params=p)
        _print(result)
        return 0 if _task_succeeded(result) else 1
    return _handle(_do)


def query_task(ak: str, sk: str, task_id: str) -> int:
    """Query the status of a submitted task."""
    def _do():
        client = SkillClient(ak=ak, sk=sk)
        result = client.poll_task_status(task_id)
        _print(result)
        return 0 if _task_succeeded(result) else 1
    return _handle(_do)


def list_tasks(ak: str, sk: str) -> int:
    """List all available tasks."""
    def _do():
        client = SkillClient(ak=ak, sk=sk)
        cfg = client.fetch_config()
        invoke_map = {}
        if isinstance(cfg, dict):
            algo = cfg.get("algorithm")
            if isinstance(algo, dict):
                raw_invoke = algo.get("invoke")
                if isinstance(raw_invoke, dict):
                    invoke_map = raw_invoke
        # Backward compatibility: fall back to local INVOKE table if server payload has no invoke map.
        if not invoke_map:
            invoke_map = INVOKE
        tasks = [{"name": n, **c} for n, c in invoke_map.items()]
        _print({"tasks": tasks, "count": len(tasks)})
        return 0
    return _handle(_do)


def main() -> int:
    parser = argparse.ArgumentParser(description="BeautyPlus AI SDK CLI")
    parser.add_argument("--ak", default=os.environ.get("BP_AK"), help="Access Key")
    parser.add_argument("--sk", default=os.environ.get("BP_SK"), help="Secret Key")
    sub = parser.add_subparsers(dest="cmd", required=True)

    # run-task: upload + consume + submit + poll (all-in-one)
    p = sub.add_parser("run-task", help="Run AI task (upload+consume+submit+poll)")
    p.add_argument("--task", required=True, help="Task name")
    p.add_argument("--input", default="", help="Input file or URL")
    p.add_argument("--params", help="Params (JSON)")

    # query-task: query task status
    p = sub.add_parser("query-task", help="Query task status")
    p.add_argument("--task-id", required=True, help="Task ID")

    # list-tasks: list available tasks
    sub.add_parser("list-tasks", help="List available tasks")

    args = parser.parse_args()

    if not args.ak or not args.sk:
        parser.error(
            "--ak and --sk required (or BP_AK/BP_SK env vars; "
            "and/or scripts/.env in repo root)"
        )

    # route to the corresponding handler
    if args.cmd == "run-task":
        return run_task(args.ak, args.sk, args.task, args.input, args.params)
    elif args.cmd == "query-task":
        return query_task(args.ak, args.sk, args.task_id)
    elif args.cmd == "list-tasks":
        return list_tasks(args.ak, args.sk)

    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""Poll an AIDSO digital-human video generation task."""

from __future__ import annotations

import argparse
import sys
import time
import urllib.parse
from typing import Any, Dict

from _aidso import AidsoError, api_base_url, ensure_api_key, json_request, print_json


def parse_result(data: Dict[str, Any]) -> Dict[str, Any]:
    if data.get("code") != 200:
        raise AidsoError(f"Result request failed: {data}")
    result = data.get("data")
    if not isinstance(result, dict):
        raise AidsoError(f"Result response did not include a data object: {data}")
    status = result.get("status")
    payload = {
        "status": status,
        "msg": result.get("msg", data.get("msg")),
        "video_url": result.get("video_url"),
        "preview_url": result.get("preview_url"),
    }
    return payload


def main() -> int:
    parser = argparse.ArgumentParser(description="Poll an AIDSO digital-human video task result.")
    parser.add_argument("--task-id", required=True, help="Task id returned by submit_video.py.")
    parser.add_argument(
        "--env",
        choices=["prod"],
        default="prod",
        help="AIDSO API environment. Only production is supported.",
    )
    parser.add_argument("--once", action="store_true", help="Query once and return immediately.")
    parser.add_argument("--wait-seconds", type=int, default=600, help="Maximum polling wait time.")
    parser.add_argument("--interval-seconds", type=int, default=10, help="Polling interval.")
    args = parser.parse_args()

    try:
        api_key = ensure_api_key()
        deadline = time.time() + args.wait_seconds
        query = urllib.parse.urlencode({"taskId": args.task_id})
        url = f"{api_base_url(args.env)}/openapi/skills/get_digital_human_video_result?{query}"

        while True:
            response = json_request("GET", url, api_key=api_key, timeout=60)
            payload = parse_result(response.data)
            status = payload.get("status")
            if status in {"failed", "fail", "error"}:
                print_json(payload)
                return 3
            if args.once or status == "success":
                print_json(payload)
                return 0
            if time.time() >= deadline:
                print_json(
                    {
                        "status": status or "timeout",
                        "msg": "Polling timed out. Keep the taskId and retry later.",
                        "taskId": args.task_id,
                    }
                )
                return 4
            time.sleep(args.interval_seconds)
    except AidsoError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())

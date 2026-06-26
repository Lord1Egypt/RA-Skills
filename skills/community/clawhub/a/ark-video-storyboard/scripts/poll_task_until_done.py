#!/usr/bin/env python3
"""Poll an Ark video generation task until it finishes, then print video_url."""

from __future__ import annotations

import json
import sys
import time

from get_task_result import get_task, extract_video_url
from submit_segment import load_api_key

TERMINAL_SUCCESS = {"succeeded"}
TERMINAL_FAIL = {"failed", "canceled", "cancelled"}


def poll(task_id: str, interval_seconds: int = 10, timeout_seconds: int = 900) -> dict:
    api_key = load_api_key()
    deadline = time.time() + timeout_seconds
    last = None
    while time.time() < deadline:
        last = get_task(task_id, api_key)
        status = (last.get("status") or "").lower()
        if status in TERMINAL_SUCCESS:
            return {
                "ok": True,
                "id": last.get("id"),
                "status": last.get("status"),
                "video_url": extract_video_url(last),
                "raw": last,
            }
        if status in TERMINAL_FAIL:
            return {
                "ok": False,
                "id": last.get("id"),
                "status": last.get("status"),
                "video_url": extract_video_url(last),
                "raw": last,
            }
        time.sleep(interval_seconds)
    return {
        "ok": False,
        "id": (last or {}).get("id"),
        "status": (last or {}).get("status"),
        "video_url": extract_video_url(last or {}),
        "error": f"timeout after {timeout_seconds}s",
        "raw": last,
    }


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: poll_task_until_done.py <task_id> [interval_seconds] [timeout_seconds]", file=sys.stderr)
        sys.exit(1)
    task_id = sys.argv[1]
    interval_seconds = int(sys.argv[2]) if len(sys.argv) >= 3 else 10
    timeout_seconds = int(sys.argv[3]) if len(sys.argv) >= 4 else 900
    print(json.dumps(poll(task_id, interval_seconds, timeout_seconds), ensure_ascii=False, indent=2))

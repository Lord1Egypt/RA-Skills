#!/usr/bin/env python3
"""Fetch Ark video generation task status and return the video URL when ready."""

from __future__ import annotations

import json
import subprocess
import sys

from submit_segment import load_api_key

API_BASE = "https://ark.cn-beijing.volces.com/api/v3/contents/generations/tasks"


def get_task(task_id: str, api_key: str | None = None) -> dict:
    headers = ["-H", "Content-Type: application/json"]
    if api_key:
        headers += ["-H", f"Authorization: Bearer {api_key}"]
    cmd = ["curl", "-sS", f"{API_BASE}/{task_id}", *headers]
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, check=False)
        if p.returncode != 0:
            return {"ok": False, "error": p.stderr.strip() or "curl failed"}
        return json.loads(p.stdout)
    except Exception as e:
        return {"ok": False, "error": str(e)}


def extract_video_url(resp: dict) -> str | None:
    content = resp.get("content") or {}
    return content.get("video_url")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: get_task_result.py <task_id>", file=sys.stderr)
        sys.exit(1)
    task_id = sys.argv[1]
    api_key = load_api_key()
    result = get_task(task_id, api_key)
    print(json.dumps({
        "id": result.get("id"),
        "status": result.get("status"),
        "video_url": extract_video_url(result),
        "raw": result,
    }, ensure_ascii=False, indent=2))

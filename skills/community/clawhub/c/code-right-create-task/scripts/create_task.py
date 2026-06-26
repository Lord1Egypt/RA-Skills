#!/usr/bin/env python3
"""Create a Code-Right material generation task via API.

Usage:
    python create_task.py --system-name "项目名称" --notify-email "user@example.com"
    python create_task.py --system-name "项目名称" --notify-email "user@example.com" --access-token "xxx"
"""
from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.request

DEFAULT_API_BASE = "https://softcraft.cloud"


def main() -> int:
    parser = argparse.ArgumentParser(description="Create Code-Right task via API.")
    parser.add_argument("--system-name", required=True, help="软件系统名称（必填）")
    parser.add_argument("--notify-email", required=True, help="接收邮箱（必填）")
    parser.add_argument("--access-token", help="会话 token（可选）")
    args = parser.parse_args()

    api_base = DEFAULT_API_BASE.rstrip("/")
    url = f"{api_base}/api/tasks/"

    payload = {"systemName": args.system_name, "notifyEmail": args.notify_email}
    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")

    headers = {"Content-Type": "application/json"}
    if args.access_token:
        headers["access_token"] = args.access_token

    req = urllib.request.Request(url=url, data=data, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            body = resp.read().decode("utf-8", errors="replace")
            print(body)
            return 0
    except urllib.error.HTTPError as e:
        err = e.read().decode("utf-8", errors="replace") if hasattr(e, "read") else str(e)
        print(f"HTTP {e.code}: {err}", file=sys.stderr)
        return 1
    except Exception as e:
        print(str(e), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

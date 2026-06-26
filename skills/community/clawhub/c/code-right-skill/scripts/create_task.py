#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.request

DEFAULT_API_BASE = "https://softcraft.cloud"



def main() -> int:
    parser = argparse.ArgumentParser(description="Create Code-Right task via API.")
    parser.add_argument("--system-name")
    parser.add_argument("--notify-email")
    parser.add_argument("--access-token")
    args = parser.parse_args()

    if not args.system_name:
        print("SYSTEM_NAME is required.", file=sys.stderr)
        return 2
    if not args.notify_email:
        print("NOTIFY_EMAIL is required.", file=sys.stderr)
        return 2

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


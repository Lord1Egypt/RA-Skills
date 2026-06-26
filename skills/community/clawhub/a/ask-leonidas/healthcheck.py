#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.request

DEFAULT_TIMEOUT = 20


def main() -> int:
    api_base = os.environ.get("ASK_LEONIDAS_API_BASE", "").rstrip("/")
    api_key = os.environ.get("ASK_LEONIDAS_API_KEY", "")
    timeout = int(os.environ.get("ASK_LEONIDAS_TIMEOUT_SECONDS", str(DEFAULT_TIMEOUT)))

    if not api_base:
        print(json.dumps({"error": "ASK_LEONIDAS_API_BASE is not set."}, ensure_ascii=False))
        return 1
    if not api_key:
        print(json.dumps({"error": "ASK_LEONIDAS_API_KEY is not set."}, ensure_ascii=False))
        return 1

    req = urllib.request.Request(
        api_base + "/api/v1/openclaw/health",
        headers={"Authorization": f"Bearer {api_key}", "X-Client": "openclaw"},
        method="GET",
    )

    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read().decode("utf-8")
            print(raw if raw.strip() else json.dumps({"status": "empty"}))
            return 0
    except urllib.error.HTTPError as exc:
        raw = exc.read().decode("utf-8", errors="replace")
        print(json.dumps({
            "error": "HTTPError",
            "status_code": exc.code,
            "body": raw,
        }, ensure_ascii=False))
        return 1
    except Exception as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

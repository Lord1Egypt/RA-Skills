#!/usr/bin/env python3
"""Brikko PII Mask — anonymize PII in text via api.brikko.ru.

Reads text from stdin, calls /v1/anonymize, prints JSON to stdout:

    {"masked_text": "...", "mapping_id": "...", "count": N, "audit": [...]}

Exit codes:
    0 — success
    1 — API/network error
    2 — config error (missing BRIKKO_API_KEY, text too large, etc.)
"""

from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.request

DEFAULT_API_URL = "https://api.brikko.ru"
MAX_TEXT_BYTES = 1_000_000  # match /v1/anonymize server-side limit
TIMEOUT_SECONDS = 30


def fail_config(msg: str) -> "None":
    print(json.dumps({"error": msg, "code": "config"}), file=sys.stderr)
    sys.exit(2)


def fail_api(msg: str) -> "None":
    print(json.dumps({"error": msg, "code": "api"}), file=sys.stderr)
    sys.exit(1)


def main() -> int:
    api_key = os.environ.get("BRIKKO_API_KEY", "").strip()
    if not api_key:
        fail_config(
            "BRIKKO_API_KEY env var is not set. "
            "Get one at https://brikko.ru → /app → «Создать API-ключ», "
            "then `export BRIKKO_API_KEY=sk-brk-...`"
        )

    api_url = os.environ.get("BRIKKO_API_URL", DEFAULT_API_URL).rstrip("/")

    text = sys.stdin.read()
    if not text:
        fail_config("stdin is empty — pipe text to mask.py")

    if len(text.encode("utf-8")) > MAX_TEXT_BYTES:
        fail_config(
            f"Text exceeds {MAX_TEXT_BYTES} bytes. Split into chunks "
            "(e.g. by paragraph) and call mask.py per chunk."
        )

    payload = json.dumps({"text": text}).encode("utf-8")
    req = urllib.request.Request(
        f"{api_url}/v1/anonymize",
        data=payload,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "User-Agent": "brikko-pii-skill/0.1.0",
        },
        method="POST",
    )

    last_err = None
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=TIMEOUT_SECONDS) as resp:
                body = resp.read().decode("utf-8")
                result = json.loads(body)
                # Pass-through to stdout — caller (agent) parses this JSON.
                print(json.dumps(result, ensure_ascii=False))
                return 0
        except urllib.error.HTTPError as e:
            try:
                err_body = json.loads(e.read().decode("utf-8"))
                err_msg = err_body.get("detail") or err_body.get(
                    "error", {}
                ).get("message") or str(err_body)
            except Exception:
                err_msg = f"HTTP {e.code}"
            if e.code in (401, 403):
                fail_api(
                    f"Authentication failed ({e.code}): {err_msg}. "
                    "Check BRIKKO_API_KEY validity at brikko.ru → /app → /keys."
                )
            if e.code in (400, 422):
                fail_config(f"Invalid request: {err_msg}")
            # 5xx / 429 — retry
            last_err = f"HTTP {e.code}: {err_msg}"
        except urllib.error.URLError as e:
            last_err = f"Network error: {e.reason}"
        except (TimeoutError, json.JSONDecodeError) as e:
            last_err = str(e)

    fail_api(
        f"Failed after 3 attempts. Last error: {last_err}. "
        f"Check api.brikko.ru reachability or set BRIKKO_API_URL to your "
        f"local Brikko Studio (e.g. http://localhost:3737)."
    )
    return 1  # unreachable, fail_api exits


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""Brikko PII Restore — restore placeholders to original PII via api.brikko.ru.

Reads text from stdin, calls /v1/restore with --mapping-id flag, prints
the restored text to stdout (no JSON wrapper — easier for agents to pipe).

Exit codes:
    0 — success
    1 — API/network error (or mapping_id expired — text returned with
        placeholders intact + warning to stderr)
    2 — config error
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request

DEFAULT_API_URL = "https://api.brikko.ru"
TIMEOUT_SECONDS = 30


def fail_config(msg: str) -> "None":
    print(json.dumps({"error": msg, "code": "config"}), file=sys.stderr)
    sys.exit(2)


def fail_api(msg: str) -> "None":
    print(json.dumps({"error": msg, "code": "api"}), file=sys.stderr)
    sys.exit(1)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Restore PII placeholders using a Brikko mapping_id"
    )
    parser.add_argument(
        "--mapping-id",
        required=True,
        help="mapping_id from a previous mask.py call",
    )
    args = parser.parse_args()

    api_key = os.environ.get("BRIKKO_API_KEY", "").strip()
    if not api_key:
        fail_config("BRIKKO_API_KEY env var is not set.")

    api_url = os.environ.get("BRIKKO_API_URL", DEFAULT_API_URL).rstrip("/")

    text = sys.stdin.read()
    if not text:
        fail_config("stdin is empty — pipe LLM response to restore.py")

    payload = json.dumps(
        {"text": text, "mapping_id": args.mapping_id}
    ).encode("utf-8")
    req = urllib.request.Request(
        f"{api_url}/v1/restore",
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
                # Plain text to stdout — easier для downstream агента который
                # просто берёт результат и отдаёт юзеру.
                print(result["restored_text"], end="")
                return 0
        except urllib.error.HTTPError as e:
            try:
                err_body = json.loads(e.read().decode("utf-8"))
                err_msg = err_body.get("detail") or err_body.get(
                    "error", {}
                ).get("message") or str(err_body)
            except Exception:
                err_msg = f"HTTP {e.code}"
            if e.code == 404:
                # mapping_id expired or unknown. Graceful degradation:
                # return the text as-is (placeholders still visible),
                # warn agent so it can choose to re-run mask.py.
                print(
                    f"WARNING: mapping_id '{args.mapping_id}' not found / expired. "
                    "Returning text with placeholders intact.",
                    file=sys.stderr,
                )
                print(text, end="")
                return 0
            if e.code in (401, 403):
                fail_api(f"Authentication failed ({e.code}): {err_msg}")
            if e.code in (400, 422):
                fail_config(f"Invalid request: {err_msg}")
            last_err = f"HTTP {e.code}: {err_msg}"
        except urllib.error.URLError as e:
            last_err = f"Network error: {e.reason}"
        except (TimeoutError, json.JSONDecodeError, KeyError) as e:
            last_err = str(e)

    fail_api(f"Failed after 3 attempts. Last error: {last_err}.")
    return 1  # unreachable


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""Submit an AIDSO benchmark-video text extraction task."""

from __future__ import annotations

import argparse
import sys
from typing import Any, Dict

from _aidso import AidsoError, api_base_url, ensure_api_key, json_request, print_json


def main() -> int:
    parser = argparse.ArgumentParser(description="Submit an AIDSO text extraction task for a benchmark video URL.")
    parser.add_argument("--url", required=True, help="Benchmark video URL to extract copy from.")
    parser.add_argument(
        "--env",
        choices=["prod"],
        default="prod",
        help="AIDSO API environment. Only production is supported.",
    )
    args = parser.parse_args()

    try:
        api_key = ensure_api_key()
        payload: Dict[str, Any] = {"url": args.url}
        url = f"{api_base_url(args.env)}/openapi/skills/submit_text_extract_task"
        response = json_request("POST", url, api_key=api_key, payload=payload, timeout=120)
        if response.data.get("code") != 200:
            raise AidsoError(f"Text extraction submission failed: {response.data}")
        task_id = response.data.get("data")
        if not isinstance(task_id, str) or not task_id:
            raise AidsoError(f"Submission succeeded but taskId was missing: {response.data}")
        print_json({"taskId": task_id, "msg": response.data.get("msg", "success")})
        return 0
    except AidsoError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())

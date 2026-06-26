#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.request
from typing import Any, Dict, Tuple


def make_headers() -> Dict[str, str]:
    headers = {"Content-Type": "application/json"}
    token = os.environ.get("EZER_BEARER_TOKEN", "").strip()
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers


def request_json(method: str, url: str, payload: Dict[str, Any] | None = None) -> Tuple[int, Dict[str, Any]]:
    data = None
    if payload is not None:
        data = json.dumps(payload, ensure_ascii=False).encode("utf-8")

    req = urllib.request.Request(url=url, method=method, data=data, headers=make_headers())
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            status = resp.status
            body = resp.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as exc:
        status = exc.code
        body = exc.read().decode("utf-8", errors="replace")
    except urllib.error.URLError as exc:
        raise RuntimeError(f"request failed: {exc}") from exc

    try:
        payload_obj = json.loads(body) if body else {}
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"invalid JSON response from {url}: {body[:500]}") from exc
    return status, payload_obj


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Invoke Ezer API task and wait for result")
    parser.add_argument("--code", required=True)
    parser.add_argument("--period", required=True, choices=["FY", "Q1", "Q2", "Q3", "H1"])
    parser.add_argument("--year", required=True, type=int)
    parser.add_argument("--lang", required=True)
    parser.add_argument("--timeout-sec", type=int, default=600)
    parser.add_argument("--poll-interval-sec", type=float, default=2.0)
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    base_url = os.environ.get("EZER_API_BASE_URL", "").strip().rstrip("/")
    if not base_url:
        print("Missing required env: EZER_API_BASE_URL", file=sys.stderr)
        return 2

    create_payload = {
        "code": args.code,
        "period": args.period,
        "year": args.year,
        "lang": args.lang,
    }

    create_url = f"{base_url}/api/tasks"
    status, created = request_json("POST", create_url, create_payload)
    if status != 202:
        print(json.dumps({"error": "create_task_failed", "status": status, "response": created}, ensure_ascii=False), file=sys.stderr)
        return 1

    task_id = created.get("task_id")
    if not task_id:
        print(json.dumps({"error": "missing_task_id", "response": created}, ensure_ascii=False), file=sys.stderr)
        return 1

    result_url = f"{base_url}/api/tasks/{task_id}/result"
    deadline = time.time() + args.timeout_sec

    while True:
        status, result = request_json("GET", result_url)
        if status == 200:
            print(json.dumps(result, ensure_ascii=False, indent=2))
            return 0
        if status >= 500:
            print(json.dumps({"error": "task_failed", "task_id": task_id, "status": status, "response": result}, ensure_ascii=False), file=sys.stderr)
            return 1
        if status not in {202}:
            print(json.dumps({"error": "unexpected_status", "task_id": task_id, "status": status, "response": result}, ensure_ascii=False), file=sys.stderr)
            return 1
        if time.time() > deadline:
            print(json.dumps({"error": "timeout", "task_id": task_id, "status": status, "last_response": result}, ensure_ascii=False), file=sys.stderr)
            return 1
        time.sleep(args.poll_interval_sec)


if __name__ == "__main__":
    raise SystemExit(main())

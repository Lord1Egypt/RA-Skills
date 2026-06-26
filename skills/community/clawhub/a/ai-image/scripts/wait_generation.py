#!/usr/bin/env python3
"""Poll a skills.video generation task until it reaches terminal status."""

from __future__ import annotations

import argparse
import json
import os
import time
from typing import Any
from urllib import error, request

TRANSIENT_HTTP_STATUSES = {429, 500, 502, 503, 504}
SUCCESS_STATUSES = {"COMPLETED", "SUCCEEDED"}
TERMINAL_STATUSES = SUCCESS_STATUSES | {"FAILED", "CANCELED", "CANCELLED"}


def parse_json_or_text(raw: str) -> Any:
    text = raw.strip()
    if not text:
        return None
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return text


def emit(payload: dict[str, Any]) -> None:
    print(json.dumps(payload, ensure_ascii=False))


def extract_message(payload: Any) -> str:
    if payload is None:
        return ""
    if isinstance(payload, str):
        return payload
    if isinstance(payload, dict):
        message = payload.get("message")
        if isinstance(message, str):
            return message
        error_obj = payload.get("error")
        if isinstance(error_obj, dict):
            nested = error_obj.get("message")
            if isinstance(nested, str):
                return nested
    return json.dumps(payload, ensure_ascii=False)


def find_status(payload: Any) -> tuple[str | None, str | None]:
    preferred_keys = (
        "status",
        "state",
        "queue_state",
        "queueState",
        "prediction_status",
        "predictionStatus",
    )

    def walk(node: Any) -> tuple[str | None, str | None]:
        if isinstance(node, dict):
            for key in preferred_keys:
                value = node.get(key)
                if isinstance(value, str) and value.strip():
                    return value.strip(), key
            for value in node.values():
                found = walk(value)
                if found[0]:
                    return found
        elif isinstance(node, list):
            for item in node:
                found = walk(item)
                if found[0]:
                    return found
        return None, None

    return walk(payload)


def fetch_generation(
    base_url: str,
    generation_id: str,
    api_key: str,
    request_timeout: float,
) -> tuple[int, Any]:
    url = f"{base_url.rstrip('/')}/generation/{generation_id}"
    req = request.Request(
        url,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Accept": "application/json",
        },
        method="GET",
    )

    try:
        with request.urlopen(req, timeout=request_timeout) as resp:
            raw = resp.read().decode("utf-8", errors="replace")
            return resp.getcode(), parse_json_or_text(raw)
    except error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        return exc.code, parse_json_or_text(body)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--generation-id", required=True, help="Generation id to poll")
    parser.add_argument("--base-url", default="https://open.skills.video/api/v1")
    parser.add_argument("--interval", type=float, default=3.0, help="Poll interval in seconds")
    parser.add_argument("--timeout", type=float, default=600.0, help="Total wait timeout in seconds")
    parser.add_argument(
        "--request-timeout",
        type=float,
        default=20.0,
        help="HTTP request timeout per poll in seconds",
    )
    args = parser.parse_args()

    api_key = os.environ.get("SKILLS_VIDEO_API_KEY", "").strip()
    if not api_key:
        emit(
            {
                "event": "error",
                "error": "missing_api_key",
                "message": "Set SKILLS_VIDEO_API_KEY before polling generation status.",
            }
        )
        return 1

    if args.interval <= 0:
        emit({"event": "error", "error": "invalid_interval", "message": "--interval must be > 0"})
        return 1
    if args.timeout <= 0:
        emit({"event": "error", "error": "invalid_timeout", "message": "--timeout must be > 0"})
        return 1

    start = time.monotonic()
    attempt = 0
    last_status: str | None = None

    while True:
        elapsed = time.monotonic() - start
        if elapsed > args.timeout:
            emit(
                {
                    "event": "timeout",
                    "generation_id": args.generation_id,
                    "elapsed_seconds": round(elapsed, 2),
                    "last_status": last_status,
                }
            )
            return 11

        attempt += 1
        http_status, payload = fetch_generation(
            base_url=args.base_url,
            generation_id=args.generation_id,
            api_key=api_key,
            request_timeout=args.request_timeout,
        )

        if http_status >= 400:
            message = extract_message(payload)
            transient = http_status in TRANSIENT_HTTP_STATUSES
            emit(
                {
                    "event": "poll_error",
                    "generation_id": args.generation_id,
                    "attempt": attempt,
                    "http_status": http_status,
                    "transient": transient,
                    "message": message,
                }
            )
            if transient:
                time.sleep(args.interval)
                continue
            return 12

        status_value, status_key = find_status(payload)
        normalized = status_value.upper() if status_value else None
        terminal = normalized in TERMINAL_STATUSES if normalized else False

        emit(
            {
                "event": "poll",
                "generation_id": args.generation_id,
                "attempt": attempt,
                "http_status": http_status,
                "status": status_value,
                "status_key": status_key,
                "terminal": terminal,
            }
        )

        if status_value:
            last_status = status_value

        if terminal:
            ok = normalized in SUCCESS_STATUSES
            emit(
                {
                    "event": "terminal",
                    "ok": ok,
                    "generation_id": args.generation_id,
                    "status": status_value,
                    "response": payload,
                }
            )
            return 0 if ok else 10

        time.sleep(args.interval)


if __name__ == "__main__":
    raise SystemExit(main())

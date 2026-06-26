#!/usr/bin/env python3
"""Create generation via SSE, then fallback to polling until terminal status."""

from __future__ import annotations

import argparse
import json
import os
import socket
import subprocess
import sys
from pathlib import Path
from typing import Any
from urllib import error, request

SUCCESS_STATUSES = {"COMPLETED", "SUCCEEDED"}
TERMINAL_STATUSES = SUCCESS_STATUSES | {"FAILED", "CANCELED", "CANCELLED"}
TERMINAL_EVENT_NAMES = {
    "completed",
    "complete",
    "succeeded",
    "success",
    "failed",
    "failure",
    "canceled",
    "cancelled",
    "done",
    "finished",
    "terminal",
}


def emit(payload: dict[str, Any]) -> None:
    print(json.dumps(payload, ensure_ascii=False))


def parse_json_or_text(raw: str) -> Any:
    text = raw.strip()
    if not text:
        return None
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return text


def load_payload(args: argparse.Namespace) -> dict[str, Any]:
    if args.payload_file:
        raw = Path(args.payload_file).read_text(encoding="utf-8")
        payload = parse_json_or_text(raw)
    elif args.payload is not None:
        payload = parse_json_or_text(args.payload)
    else:
        payload = {}

    if payload is None:
        return {}
    if not isinstance(payload, dict):
        raise SystemExit("Payload must be a JSON object.")
    return payload


def endpoint_url(base_url: str, endpoint: str) -> str:
    if endpoint.startswith("http://") or endpoint.startswith("https://"):
        return endpoint
    if not endpoint.startswith("/"):
        endpoint = "/" + endpoint
    return f"{base_url.rstrip('/')}{endpoint}"


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


def find_generation_id(payload: Any) -> tuple[str | None, str | None]:
    preferred_keys = (
        "generation_id",
        "generationId",
        "prediction_id",
        "predictionId",
        "task_id",
        "taskId",
        "id",
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


def is_terminal_event_name(event_name: str | None) -> bool:
    if not event_name:
        return False
    return event_name.strip().lower() in TERMINAL_EVENT_NAMES


def run_sse(
    url: str,
    api_key: str,
    payload: dict[str, Any],
    request_timeout: float,
) -> tuple[int, str | None, Any]:
    req = request.Request(
        url,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Accept": "text/event-stream",
            "Content-Type": "application/json",
        },
        data=json.dumps(payload).encode("utf-8"),
        method="POST",
    )

    generation_id: str | None = None
    terminal_payload: Any = None

    event_name = "message"
    data_lines: list[str] = []

    def flush_event() -> tuple[bool, int]:
        nonlocal event_name, data_lines, generation_id, terminal_payload

        if not data_lines:
            event_name = "message"
            return False, 0

        text = "\n".join(data_lines)
        parsed = parse_json_or_text(text)
        status_value, status_key = find_status(parsed)
        status_normalized = status_value.upper() if status_value else None
        event_terminal = (status_normalized in TERMINAL_STATUSES) or is_terminal_event_name(event_name)

        current_id, _ = find_generation_id(parsed)
        if current_id and not generation_id:
            generation_id = current_id

        emit(
            {
                "event": "sse_event",
                "sse_event_name": event_name,
                "generation_id": generation_id,
                "status": status_value,
                "status_key": status_key,
                "terminal": event_terminal,
                "payload": parsed,
            }
        )

        data_lines = []
        event_name = "message"

        if event_terminal:
            terminal_payload = parsed
            if status_normalized in SUCCESS_STATUSES:
                return True, 0
            if status_normalized in TERMINAL_STATUSES:
                return True, 10
            return True, 0

        return False, 0

    try:
        with request.urlopen(req, timeout=request_timeout) as resp:
            emit({"event": "sse_open", "http_status": resp.getcode(), "url": url})
            for raw_line in resp:
                line = raw_line.decode("utf-8", errors="replace").rstrip("\r\n")
                if not line:
                    done, rc = flush_event()
                    if done:
                        return rc, generation_id, terminal_payload
                    continue
                if line.startswith(":"):
                    continue
                if line.startswith("event:"):
                    event_name = line.split(":", 1)[1].strip() or "message"
                elif line.startswith("data:"):
                    data_lines.append(line.split(":", 1)[1].lstrip())

            done, rc = flush_event()
            if done:
                return rc, generation_id, terminal_payload

            emit(
                {
                    "event": "sse_stream_ended",
                    "generation_id": generation_id,
                    "message": "SSE stream ended before terminal status.",
                }
            )
            return 100, generation_id, None

    except error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        parsed = parse_json_or_text(body)
        emit(
            {
                "event": "sse_http_error",
                "http_status": exc.code,
                "message": extract_message(parsed),
                "payload": parsed,
            }
        )
        return 101, generation_id, parsed
    except (socket.timeout, TimeoutError) as exc:
        emit({"event": "sse_timeout", "message": str(exc), "generation_id": generation_id})
        return 102, generation_id, None
    except error.URLError as exc:
        emit({"event": "sse_connect_error", "message": str(exc), "generation_id": generation_id})
        return 103, generation_id, None


def run_poll_fallback(
    generation_id: str,
    base_url: str,
    timeout: float,
    interval: float,
    request_timeout: float,
) -> int:
    wait_script = Path(__file__).with_name("wait_generation.py")
    if not wait_script.exists():
        emit(
            {
                "event": "error",
                "error": "wait_script_not_found",
                "message": f"Missing fallback script: {wait_script}",
            }
        )
        return 2

    cmd = [
        sys.executable,
        str(wait_script),
        "--generation-id",
        generation_id,
        "--base-url",
        base_url,
        "--timeout",
        str(timeout),
        "--interval",
        str(interval),
        "--request-timeout",
        str(request_timeout),
    ]

    emit(
        {
            "event": "fallback_polling_start",
            "generation_id": generation_id,
            "command": " ".join(cmd),
        }
    )

    result = subprocess.run(cmd, check=False)
    emit(
        {
            "event": "fallback_polling_end",
            "generation_id": generation_id,
            "exit_code": result.returncode,
        }
    )
    return result.returncode


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--sse-endpoint", required=True, help="SSE create endpoint path or full URL")
    parser.add_argument("--base-url", default="https://open.skills.video/api/v1")
    parser.add_argument("--payload", help="JSON object payload string")
    parser.add_argument("--payload-file", help="Path to JSON payload file")
    parser.add_argument("--sse-request-timeout", type=float, default=120.0)
    parser.add_argument("--poll-timeout", type=float, default=900.0)
    parser.add_argument("--poll-interval", type=float, default=3.0)
    parser.add_argument("--poll-request-timeout", type=float, default=20.0)
    args = parser.parse_args()

    api_key = os.environ.get("SKILLS_VIDEO_API_KEY", "").strip()
    if not api_key:
        emit(
            {
                "event": "error",
                "error": "missing_api_key",
                "message": "Set SKILLS_VIDEO_API_KEY before calling skills.video APIs.",
            }
        )
        return 1

    if args.payload is not None and args.payload_file:
        emit(
            {
                "event": "error",
                "error": "invalid_arguments",
                "message": "Use either --payload or --payload-file, not both.",
            }
        )
        return 1

    payload = load_payload(args)
    url = endpoint_url(args.base_url, args.sse_endpoint)

    emit({"event": "start", "url": url, "mode": "sse_then_poll_fallback"})

    sse_rc, generation_id, terminal_payload = run_sse(
        url=url,
        api_key=api_key,
        payload=payload,
        request_timeout=args.sse_request_timeout,
    )

    if sse_rc in (0, 10):
        emit(
            {
                "event": "terminal",
                "source": "sse",
                "ok": sse_rc == 0,
                "generation_id": generation_id,
                "response": terminal_payload,
            }
        )
        return sse_rc

    if not generation_id:
        emit(
            {
                "event": "error",
                "error": "missing_generation_id",
                "message": "SSE did not return generation id; cannot start poll fallback.",
                "sse_exit_code": sse_rc,
            }
        )
        return 3

    return run_poll_fallback(
        generation_id=generation_id,
        base_url=args.base_url,
        timeout=args.poll_timeout,
        interval=args.poll_interval,
        request_timeout=args.poll_request_timeout,
    )


if __name__ == "__main__":
    raise SystemExit(main())

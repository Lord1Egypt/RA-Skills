#!/usr/bin/env python3
"""Classify skills.video runtime API errors and provide actionable guidance."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

INSUFFICIENT_CREDITS_KEYWORDS = (
    "insufficient credit",
    "not enough credit",
    "insufficient balance",
    "credit balance",
    "top up",
    "recharge",
)


def load_body(body: str | None, body_file: str | None) -> Any:
    if body_file:
        raw = Path(body_file).read_text(encoding="utf-8")
    elif body is not None:
        raw = body
    else:
        return None

    raw = raw.strip()
    if not raw:
        return None

    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return raw


def extract_message(payload: Any) -> str:
    if payload is None:
        return ""
    if isinstance(payload, str):
        return payload
    if isinstance(payload, dict):
        message = payload.get("message")
        if isinstance(message, str):
            return message
        error = payload.get("error")
        if isinstance(error, dict):
            nested = error.get("message")
            if isinstance(nested, str):
                return nested
    return json.dumps(payload, ensure_ascii=False)


def classify(status: int, message: str) -> str:
    lowered = message.lower()

    if status == 402 or any(keyword in lowered for keyword in INSUFFICIENT_CREDITS_KEYWORDS):
        return "insufficient_credits"
    if status == 401 or "unauthorized" in lowered:
        return "auth"
    if status == 422 or "validation" in lowered:
        return "validation"
    if status == 404:
        return "not_found"
    if status == 429 or status >= 500:
        return "transient"
    return "unknown"


def exit_code_for(category: str) -> int:
    table = {
        "insufficient_credits": 20,
        "auth": 21,
        "validation": 22,
        "not_found": 23,
        "transient": 24,
        "unknown": 25,
    }
    return table.get(category, 25)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--status", type=int, required=True, help="HTTP status code")
    parser.add_argument("--body", help="Raw response body JSON/text")
    parser.add_argument("--body-file", help="Path to file containing raw response body")
    parser.add_argument("--base-url", default="https://open.skills.video/api/v1")
    parser.add_argument("--credits-endpoint", default="/credits")
    args = parser.parse_args()

    payload = load_body(args.body, args.body_file)
    message = extract_message(payload)
    category = classify(args.status, message)

    guidance: list[str] = []
    should_retry = False

    if category == "insufficient_credits":
        guidance = [
            "Credits are insufficient for this request.",
            "Open https://skills.video/dashboard and go to Billing/Credits to recharge.",
            "After recharge, retry the same request.",
        ]
    elif category == "auth":
        guidance = [
            "Authentication failed.",
            "Verify SKILLS_VIDEO_API_KEY and retry.",
        ]
    elif category == "validation":
        guidance = [
            "Request payload validation failed.",
            "Fix request parameters based on OpenAPI schema and retry.",
        ]
    elif category == "not_found":
        guidance = [
            "Resource or endpoint was not found.",
            "Recheck endpoint path/model id and generation id.",
        ]
    elif category == "transient":
        guidance = [
            "Transient server or rate-limit error.",
            "Retry with bounded exponential backoff.",
        ]
        should_retry = True
    else:
        guidance = [
            "Unhandled runtime error.",
            "Inspect response payload and apply a safe fallback path.",
        ]

    credits_url = f"{args.base_url.rstrip('/')}{args.credits_endpoint}"

    output = {
        "category": category,
        "status": args.status,
        "message": message,
        "should_retry": should_retry,
        "guidance": guidance,
        "credits_check_command": (
            f"curl -X GET \"{credits_url}\" "
            "-H \"Authorization: Bearer $SKILLS_VIDEO_API_KEY\""
        ),
        "recharge": {
            "dashboard_url": "https://skills.video/dashboard",
            "pricing_url": "https://skills.video/pricing",
        },
    }

    print(json.dumps(output, ensure_ascii=False, indent=2))
    return exit_code_for(category)


if __name__ == "__main__":
    raise SystemExit(main())

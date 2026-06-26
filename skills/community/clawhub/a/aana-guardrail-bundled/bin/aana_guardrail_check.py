#!/usr/bin/env python
"""Bundled OpenClaw helper for calling a reviewed localhost AANA bridge.

This helper is intentionally small:
- no third-party dependencies,
- no dynamic imports,
- no shell execution,
- localhost-only HTTP,
- one JSON payload file in, one JSON result out.
"""

from __future__ import annotations

import argparse
import json
import pathlib
import sys
import urllib.error
import urllib.parse
import urllib.request


DEFAULT_URL = "http://localhost:8765/agent-check"
ALLOWED_HOSTS = {"localhost"}
SECRET_KEY_TERMS = {
    "api_key",
    "apikey",
    "authorization",
    "bearer",
    "card_number",
    "password",
    "secret",
    "token",
}


def load_payload(path: pathlib.Path) -> dict:
    with path.open(encoding="utf-8") as handle:
        payload = json.load(handle)
    if not isinstance(payload, dict):
        raise ValueError("Review payload must be a JSON object.")
    return payload


def validate_url(url: str) -> str:
    parsed = urllib.parse.urlparse(url)
    if parsed.scheme not in {"http", "https"}:
        raise ValueError("AANA bridge URL must use http or https.")
    if parsed.hostname not in ALLOWED_HOSTS:
        raise ValueError("AANA bridge URL must target localhost.")
    return url


def find_secret_like_keys(value, prefix="$") -> list[str]:
    found = []
    if isinstance(value, dict):
        for key, item in value.items():
            key_text = str(key).lower()
            path = f"{prefix}.{key}"
            if any(term in key_text for term in SECRET_KEY_TERMS):
                found.append(path)
            found.extend(find_secret_like_keys(item, path))
    elif isinstance(value, list):
        for index, item in enumerate(value):
            found.extend(find_secret_like_keys(item, f"{prefix}[{index}]"))
    return found


def to_agent_event(payload: dict) -> dict:
    adapter_id = payload.get("adapter_id")
    request_summary = payload.get("request_summary")
    candidate_summary = payload.get("candidate_summary")
    if not isinstance(adapter_id, str) or not adapter_id.strip():
        raise ValueError("Payload must include a non-empty adapter_id.")
    if not isinstance(request_summary, str) or not request_summary.strip():
        raise ValueError("Payload must include a non-empty request_summary.")
    if not isinstance(candidate_summary, str) or not candidate_summary.strip():
        raise ValueError("Payload must include a non-empty candidate_summary.")

    evidence_summary = payload.get("evidence_summary", [])
    if isinstance(evidence_summary, str):
        evidence_summary = [evidence_summary]
    if not isinstance(evidence_summary, list) or not all(isinstance(item, str) for item in evidence_summary):
        raise ValueError("evidence_summary must be a string or array of strings.")

    allowed_actions = payload.get("allowed_actions") or ["accept", "revise", "ask", "defer", "refuse"]
    if not isinstance(allowed_actions, list) or not all(isinstance(item, str) for item in allowed_actions):
        raise ValueError("allowed_actions must be an array of strings.")

    metadata = payload.get("metadata", {})
    if metadata is not None and not isinstance(metadata, dict):
        raise ValueError("metadata must be an object when provided.")

    return {
        "event_version": "0.1",
        "event_id": payload.get("event_id", "openclaw-redacted-review"),
        "agent": payload.get("agent", "openclaw"),
        "adapter_id": adapter_id,
        "user_request": request_summary,
        "candidate_action": candidate_summary,
        "available_evidence": evidence_summary,
        "allowed_actions": allowed_actions,
        "metadata": {
            **(metadata or {}),
            "redacted_review_payload": True,
            "helper": "aana_guardrail_check.py",
        },
    }


def post_json(url: str, payload: dict, timeout: float) -> dict:
    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    request = urllib.request.Request(
        validate_url(url),
        data=data,
        headers={"Content-Type": "application/json", "Accept": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            body = response.read().decode("utf-8")
    except urllib.error.URLError as exc:
        raise RuntimeError(f"AANA bridge request failed: {exc}") from exc
    result = json.loads(body)
    if not isinstance(result, dict):
        raise ValueError("AANA bridge returned non-object JSON.")
    return result


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Call a reviewed localhost AANA bridge with a redacted review payload.")
    parser.add_argument("--payload", required=True, help="Path to redacted review payload JSON.")
    parser.add_argument("--url", default=DEFAULT_URL, help="Local AANA bridge URL. Defaults to http://localhost:8765/agent-check.")
    parser.add_argument("--timeout", type=float, default=10.0, help="HTTP timeout in seconds.")
    return parser


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    try:
        payload = load_payload(pathlib.Path(args.payload))
        secret_keys = find_secret_like_keys(payload)
        if secret_keys:
            raise ValueError("Payload contains secret-like keys: " + ", ".join(secret_keys))
        result = post_json(args.url, to_agent_event(payload), args.timeout)
    except (OSError, ValueError, RuntimeError, json.JSONDecodeError) as exc:
        print(json.dumps({"error": str(exc)}, indent=2), file=sys.stderr)
        return 2

    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if result.get("recommended_action") == "accept" else 1


if __name__ == "__main__":
    raise SystemExit(main())

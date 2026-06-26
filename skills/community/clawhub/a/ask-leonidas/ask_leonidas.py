#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from typing import Any, Dict, Optional

DEFAULT_TIMEOUT = 45
DEFAULT_SOURCE = "openclaw-skill"
DEFAULT_SKILL_VERSION = "2.0.0"


def get_env(name: str, default: Optional[str] = None) -> Optional[str]:
    value = os.environ.get(name)
    if value is None or value == "":
        return default
    return value


def build_payload(args: argparse.Namespace) -> Dict[str, Any]:
    max_prompt_length = max(500, min(args.max_prompt_length, 12000))
    return {
        "pain_point": args.pain_point,
        "role": args.role,
        "industry": args.industry,
        "desired_outcome": args.desired_outcome,
        "mode": args.mode,
        "return_candidates": args.return_candidates,
        "return_debug": args.return_debug,
        "locale": args.locale,
        "llm_preference": args.provider,
        "max_prompt_length": max_prompt_length,
        "user_tier": args.user_tier,
        "source": get_env("ASK_LEONIDAS_DEFAULT_SOURCE", DEFAULT_SOURCE),
        "skill_version": get_env("ASK_LEONIDAS_DEFAULT_SKILL_VERSION", DEFAULT_SKILL_VERSION),
    }


def request_json(url: str, payload: Dict[str, Any], api_key: str, timeout_seconds: int) -> Dict[str, Any]:
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
            "X-Client": "openclaw",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=timeout_seconds) as resp:
        return json.loads(resp.read().decode("utf-8"))


def normalize_response(data: Dict[str, Any]) -> Dict[str, Any]:
    inference = data.get("inference", {})
    generation = data.get("generation", {})
    return {
        "request_id": data.get("request_id"),
        "status": data.get("status", "unknown"),
        "detected_role": inference.get("detected_role"),
        "detected_industry": inference.get("detected_industry"),
        "detected_desired_outcome": inference.get("detected_desired_outcome"),
        "confidence": inference.get("confidence"),
        "quality_score": generation.get("quality_score"),
        "prompt_type": generation.get("prompt_type"),
        "provider_route": generation.get("provider_route"),
        "prompt_text": data.get("copy_text"),
    }


def open_browser_fallback(api_base: str) -> None:
    import webbrowser
    url = api_base.rstrip("/") + "/openclaw"
    print(json.dumps({"error": "API unavailable", "fallback": url}, ensure_ascii=False))
    webbrowser.open(url)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate a LEONIDAS prompt via the Ask Leonidas API."
    )
    parser.add_argument("--pain-point", required=True, help="The professional pain point to solve")
    parser.add_argument("--role", default=None, help="Your professional role (inferred if omitted)")
    parser.add_argument("--industry", default=None, help="Your industry (inferred if omitted)")
    parser.add_argument("--desired-outcome", default=None, help="Desired outcome (inferred if omitted)")
    parser.add_argument("--mode", default="full", choices=["full", "infer_only"], help="Generation mode")
    parser.add_argument("--return-candidates", action="store_true", help="Return multiple prompt candidates")
    parser.add_argument("--return-debug", action="store_true", help="Include debug info in response")
    parser.add_argument("--locale", default="en", help="Language locale for the prompt")
    parser.add_argument("--provider", default=None, help="Preferred LLM provider")
    parser.add_argument("--max-prompt-length", type=int, default=3000, help="Max prompt length in chars")
    parser.add_argument("--user-tier", default="free", choices=["free", "pro"], help="User tier")
    args = parser.parse_args()

    api_base = get_env("ASK_LEONIDAS_API_BASE", "").rstrip("/")
    api_key = get_env("ASK_LEONIDAS_API_KEY", "")
    timeout = int(get_env("ASK_LEONIDAS_TIMEOUT_SECONDS", str(DEFAULT_TIMEOUT)))

    if not api_base:
        print(json.dumps({"error": "ASK_LEONIDAS_API_BASE is not set."}, ensure_ascii=False))
        return 1
    if not api_key:
        print(json.dumps({"error": "ASK_LEONIDAS_API_KEY is not set."}, ensure_ascii=False))
        return 1

    url = api_base + "/api/v1/openclaw/generate"
    payload = build_payload(args)

    try:
        raw = request_json(url, payload, api_key, timeout)
        result = normalize_response(raw)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except urllib.error.HTTPError as exc:
        raw = exc.read().decode("utf-8", errors="replace")
        try:
            err_data = json.loads(raw)
        except Exception:
            err_data = {"message": raw}
        print(json.dumps({
            "error": "HTTPError",
            "status_code": exc.code,
            "body": err_data,
        }, ensure_ascii=False))
        return 1
    except Exception as exc:
        open_browser_fallback(api_base)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

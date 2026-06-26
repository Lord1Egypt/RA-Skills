#!/usr/bin/env python3
"""
Herdsman Anthropic Messages compatible script.

Note: The current Anthropic compatible endpoint for Herdsman is /v1/anthropic/messages.
"""

import argparse
import json
import sys

from herdsman_client import HerdsmanAPIError, HerdsmanClient


def build_messages(message: str) -> list:
    return [{"role": "user", "content": message}]


def main() -> None:
    parser = argparse.ArgumentParser(description="Herdsman Anthropic Messages")
    parser.add_argument("message", help="User message")
    parser.add_argument("--model", required=True, help="Model ID")
    parser.add_argument("--system", help="System prompt")
    parser.add_argument("--max-tokens", type=int, default=2048, help="Max output tokens")
    parser.add_argument("--temperature", type=float, help="Temperature")
    parser.add_argument("--base-url", default="http://127.0.0.1:8080", help="Herdsman API base URL")
    parser.add_argument("--api-key", default="", help="Optional API Key")
    parser.add_argument("--json", action="store_true", help="Output full JSON")
    args = parser.parse_args()

    client = HerdsmanClient(base_url=args.base_url, api_key=args.api_key, timeout=300)
    payload = {
        "model": args.model,
        "messages": build_messages(args.message),
        "max_tokens": args.max_tokens,
        "temperature": args.temperature,
    }
    if args.system:
        payload["system"] = args.system

    try:
        result = client.anthropic_messages(**payload)
    except HerdsmanAPIError as exc:
        print(json.dumps(exc.to_dict(), indent=2, ensure_ascii=False), file=sys.stderr)
        sys.exit(1)

    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return

    chunks = []
    for item in result.get("content", []):
        if item.get("type") == "text":
            chunks.append(item.get("text", ""))
    print("".join(chunks))


if __name__ == "__main__":
    main()

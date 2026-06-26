#!/usr/bin/env python3
"""
Herdsman OpenAI Chat Completions script.

Supports standard OpenAI parameters and Herdsman extension fields:
  --reasoning-effort  (low / medium / high)
  --thinking-enabled  (enable thinking mode)
  --thinking-tokens   (thinking token budget)
"""

import argparse
import json
import sys

from herdsman_client import HerdsmanAPIError, HerdsmanClient


def load_messages(args: argparse.Namespace) -> list:
    if args.messages_json:
        with open(args.messages_json, "r", encoding="utf-8") as handle:
            payload = json.load(handle)
        if not isinstance(payload, list):
            raise ValueError("--messages-json must be a JSON file containing a messages array")
        return payload

    messages = []
    if args.system:
        messages.append({"role": "system", "content": args.system})
    if not args.message:
        raise ValueError("no message provided, and no --messages-json specified")
    messages.append({"role": "user", "content": args.message})
    return messages


def print_usage(result: dict) -> None:
    usage = result.get("usage")
    if not usage:
        return
    print(
        f"\nToken usage: prompt={usage.get('prompt_tokens', 0)}, "
        f"completion={usage.get('completion_tokens', 0)}, "
        f"total={usage.get('total_tokens', 0)}"
    )


def run_stream(client: HerdsmanClient, payload: dict) -> None:
    for chunk in client.stream_sse_json("/v1/chat/completions", payload=payload, timeout=300):
        delta = chunk.get("choices", [{}])[0].get("delta", {})
        content = delta.get("content", "")
        if content:
            print(content, end="", flush=True)
    print()


def main() -> None:
    parser = argparse.ArgumentParser(description="Herdsman Chat Completion")
    parser.add_argument("message", nargs="?", help="User message")
    parser.add_argument("--messages-json", help="Full messages JSON file path")
    parser.add_argument("--model", required=True, help="Model ID")
    parser.add_argument("--system", help="System prompt")
    parser.add_argument("--max-tokens", type=int, help="Max tokens")
    parser.add_argument("--temperature", type=float, default=0.7, help="Temperature")
    parser.add_argument("--top-p", type=float, help="top_p")
    # Herdsman / OpenAI extended reasoning parameters
    parser.add_argument(
        "--reasoning-effort",
        choices=["low", "medium", "high"],
        help="OpenAI Chat Completions compatible reasoning level (llama.cpp -> template params)",
    )
    parser.add_argument(
        "--thinking-enabled",
        action="store_true",
        help="Enable thinking mode for supported models (llama.cpp -> enable_thinking)",
    )
    parser.add_argument(
        "--thinking-tokens",
        type=int,
        help="Thinking token budget (llama.cpp -> reasoning_budget)",
    )
    parser.add_argument("--base-url", default="http://127.0.0.1:8080", help="Herdsman API base URL")
    parser.add_argument("--api-key", default="", help="Optional API Key")
    parser.add_argument("--stream", action="store_true", help="Streaming output")
    parser.add_argument("--json", action="store_true", help="Output full JSON")
    args = parser.parse_args()

    try:
        messages = load_messages(args)
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        sys.exit(1)

    client = HerdsmanClient(base_url=args.base_url, api_key=args.api_key, timeout=300)
    # Assemble payload with optional reasoning/thinking fields
    payload = {
        "model": args.model,
        "messages": messages,
        "max_tokens": args.max_tokens,
        "temperature": args.temperature,
        "top_p": args.top_p,
        "stream": args.stream,
        "reasoning_effort": args.reasoning_effort,
        "thinking_enabled": args.thinking_enabled or None,
        "thinking_tokens": args.thinking_tokens,
    }
    payload = {key: value for key, value in payload.items() if value is not None}

    try:
        if args.stream:
            run_stream(client, payload)
            return

        result = client.chat_completions(
            model=args.model,
            messages=messages,
            max_tokens=args.max_tokens,
            temperature=args.temperature,
            top_p=args.top_p,
            reasoning_effort=args.reasoning_effort,
            thinking_enabled=args.thinking_enabled or None,
            thinking_tokens=args.thinking_tokens,
        )
    except HerdsmanAPIError as exc:
        print(json.dumps(exc.to_dict(), indent=2, ensure_ascii=False), file=sys.stderr)
        sys.exit(1)

    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return

    choices = result.get("choices", [])
    if not choices:
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return

    message = choices[0].get("message", {})
    content = message.get("content", "")
    print(content)
    print_usage(result)


if __name__ == "__main__":
    main()
#!/usr/bin/env python3
"""
Herdsman model discovery script.

Prefer doing discovery and filtering via the /v1/models list to avoid depending
on single-model detail endpoints that may not be fully implemented by the platform.
"""

import argparse
import json
import sys

from herdsman_client import HerdsmanAPIError, HerdsmanClient


def print_model(model: dict) -> None:
    print(f"Model: {model.get('id', 'unknown')}")
    print(f"Object: {model.get('object', 'model')}")
    print(f"Status: {model.get('status', 'unknown')}")


def print_model_list(items: list) -> None:
    print(f"Available models ({len(items)}):")
    print("-" * 60)
    for model in items:
        print_model(model)
        print()


def main() -> None:
    parser = argparse.ArgumentParser(description="Herdsman Model Discovery")
    parser.add_argument("model_id", nargs="?", help="Model ID, optional")
    parser.add_argument(
        "--base-url",
        default="http://127.0.0.1:8080",
        help="Herdsman API base URL",
    )
    parser.add_argument("--api-key", default="", help="Optional API Key")
    parser.add_argument("--json", action="store_true", help="Output JSON")
    args = parser.parse_args()

    client = HerdsmanClient(base_url=args.base_url, api_key=args.api_key, timeout=20)

    try:
        result = client.list_models()
    except HerdsmanAPIError as exc:
        print(json.dumps(exc.to_dict(), indent=2, ensure_ascii=False), file=sys.stderr)
        sys.exit(1)

    items = result.get("data", [])
    if args.model_id:
        items = [item for item in items if item.get("id") == args.model_id]
        if not items:
            print(f"Model not found: {args.model_id}", file=sys.stderr)
            sys.exit(1)

    if args.json:
        payload = items[0] if args.model_id else {"object": "list", "data": items}
        print(json.dumps(payload, indent=2, ensure_ascii=False))
        return

    if args.model_id:
        print_model(items[0])
        return

    print_model_list(items)


if __name__ == "__main__":
    main()

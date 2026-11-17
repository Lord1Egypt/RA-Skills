from __future__ import annotations

import argparse
import json
from typing import Any

from guard_core import check_security_v2


def _message_from_json(raw_json: str) -> str:
    payload: Any = json.loads(raw_json)
    if not isinstance(payload, dict) or not isinstance(payload.get("message"), str):
        raise ValueError('JSON input must be an object with a string "message" field.')
    return payload["message"]


def main() -> None:
    parser = argparse.ArgumentParser(description="Audit a prompt for GenAI security risk.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--message", help="Prompt text to audit.")
    group.add_argument("--json", help='JSON payload containing {"message": "..."}')
    parser.add_argument("--no-semantic", action="store_true", help="Skip vector similarity scoring.")
    args = parser.parse_args()

    message = args.message if args.message is not None else _message_from_json(args.json)
    result = check_security_v2(message, enable_semantic=not args.no_semantic)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

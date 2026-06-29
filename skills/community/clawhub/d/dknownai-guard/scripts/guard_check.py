#!/usr/bin/env python3
"""Call the DKnownAI Guard API and print the JSON result.

This script intentionally uses only Python's standard library so the skill can
run in minimal agent environments without installing dependencies.
"""

from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.request
from os import environ as runtime_env
from pathlib import Path


DEFAULT_ENDPOINT = "https://open.dknownai.com/v1/guard"
DEFAULT_ENV_NAME = "DKNOWNAI_API_KEY"
DEFAULT_CONFIG_NAME = "config.local.json"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Classify text with the DKnownAI Guard API."
    )
    input_group = parser.add_mutually_exclusive_group()
    input_group.add_argument("--input", help="Text to classify.")
    input_group.add_argument(
        "--input-file",
        help="Path to a UTF-8 text file to classify.",
    )
    parser.add_argument(
        "--request-id",
        help="Optional request identifier, 16-128 characters.",
    )
    parser.add_argument(
        "--session-id",
        help="Optional session identifier, 16-128 characters.",
    )
    parser.add_argument(
        "--env-name",
        default=DEFAULT_ENV_NAME,
        help=f"Environment variable containing the DKnownAI Guard API value. Defaults to {DEFAULT_ENV_NAME}.",
    )
    parser.add_argument(
        "--endpoint",
        help=f"API endpoint. Defaults to config value or {DEFAULT_ENDPOINT}.",
    )
    parser.add_argument(
        "--config",
        help=f"Local JSON config path. Defaults to the skill folder's {DEFAULT_CONFIG_NAME}.",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=5.0,
        help="Request timeout in seconds. Defaults to 5.",
    )
    parser.add_argument(
        "--compact",
        action="store_true",
        help="Print compact JSON instead of indented JSON.",
    )
    return parser.parse_args()


def read_input(args: argparse.Namespace) -> str:
    if args.input is not None:
        return args.input
    if args.input_file is not None:
        with open(args.input_file, "r", encoding="utf-8") as input_file:
            return input_file.read()
    if not sys.stdin.isatty():
        return sys.stdin.read()
    raise ValueError("Provide --input, --input-file, or pipe text on stdin.")


def validate_optional_id(name: str, value: str | None) -> None:
    if value is None:
        return
    if not 16 <= len(value) <= 128:
        raise ValueError(f"{name} must be 16-128 characters.")


def print_json(payload: object, compact: bool) -> None:
    if compact:
        print(json.dumps(payload, ensure_ascii=False, separators=(",", ":")))
    else:
        print(json.dumps(payload, ensure_ascii=False, indent=2))


def default_config_path() -> Path:
    return Path(__file__).resolve().parent.parent / DEFAULT_CONFIG_NAME


def read_config(path_text: str | None) -> dict[str, object]:
    config_path = Path(path_text).expanduser() if path_text else default_config_path()
    if not config_path.exists():
        return {}
    with open(config_path, "r", encoding="utf-8") as config_file:
        payload = json.load(config_file)
    if not isinstance(payload, dict):
        raise ValueError(f"Config file must contain a JSON object: {config_path}")
    return payload


def config_text(config: dict[str, object], key: str) -> str | None:
    value = config.get(key)
    if isinstance(value, str) and value.strip():
        return value.strip()
    return None


def main() -> int:
    args = parse_args()

    try:
        config = read_config(args.config)
        text = read_input(args).strip()
        if not text:
            raise ValueError("Input text is empty.")
        validate_optional_id("--request-id", args.request_id)
        validate_optional_id("--session-id", args.session_id)
    except (OSError, ValueError) as exc:
        print_json({"ok": False, "error": str(exc)}, args.compact)
        return 1

    auth_value = config_text(config, "apiKey") or runtime_env.get(args.env_name)
    if not auth_value:
        print_json(
            {
                "ok": False,
                "error": f"Missing API configuration. Add apiKey to {default_config_path()} or set {args.env_name}.",
            },
            args.compact,
        )
        return 1

    endpoint = args.endpoint or config_text(config, "endpoint") or DEFAULT_ENDPOINT

    body = {"input": text}
    if args.request_id:
        body["request_id"] = args.request_id
    if args.session_id:
        body["session_id"] = args.session_id

    request = urllib.request.Request(
        endpoint,
        data=json.dumps(body).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {auth_value}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
        method="POST",
    )

    http_status = None
    try:
        with urllib.request.urlopen(request, timeout=args.timeout) as response:
            http_status = response.status
            response_text = response.read().decode("utf-8")
    except urllib.error.HTTPError as exc:
        http_status = exc.code
        response_text = exc.read().decode("utf-8", errors="replace")
    except (urllib.error.URLError, TimeoutError) as exc:
        print_json({"ok": False, "error": str(exc)}, args.compact)
        return 3

    try:
        payload = json.loads(response_text)
    except json.JSONDecodeError:
        print_json(
            {
                "ok": False,
                "http_status": http_status,
                "error": "Response was not valid JSON.",
                "raw_response": response_text,
            },
            args.compact,
        )
        return 2

    output = {
        "ok": 200 <= int(http_status or 0) < 300 and "status" in payload,
        "http_status": http_status,
        "response": payload,
    }
    print_json(output, args.compact)

    if output["ok"]:
        return 0
    return 2


if __name__ == "__main__":
    raise SystemExit(main())

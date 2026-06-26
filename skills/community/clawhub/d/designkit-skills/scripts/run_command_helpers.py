#!/usr/bin/env python3
"""Safe helper utilities for run_command.sh."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


def _read_commands(commands_file: str) -> dict[str, Any]:
    return json.loads(Path(commands_file).read_text(encoding="utf-8"))


def _print_value(value: Any) -> int:
    if isinstance(value, (dict, list)):
        print(json.dumps(value, ensure_ascii=False))
    elif value is None:
        print("")
    else:
        print(value)
    return 0


def command_field(commands_file: str, action: str, field: str) -> int:
    commands = _read_commands(commands_file)
    if action not in commands:
        return 1
    return _print_value(commands[action].get(field, ""))


def ask_message(commands_file: str, action: str, key: str) -> int:
    commands = _read_commands(commands_file)
    ask = commands.get(action, {}).get("ask_if_missing", {})
    print(ask.get(key, "请提供图片"))
    return 0


def image_input(input_json: str) -> int:
    try:
        parsed = json.loads(input_json)
    except json.JSONDecodeError:
        print("")
        return 0
    image = parsed.get("image", "") if isinstance(parsed, dict) else ""
    print(image if isinstance(image, str) else "")
    return 0


def build_body(commands_file: str, action: str, image_url: str) -> int:
    commands = _read_commands(commands_file)
    template = commands[action]["body_template"]
    body_str = json.dumps(template, ensure_ascii=False)
    print(body_str.replace("{{image}}", image_url))
    return 0


def upload_policy_provider() -> int:
    try:
        arr = json.load(sys.stdin)
        print(arr[0]["order"][0])
    except Exception:
        return 1
    return 0


def upload_policy_value(provider: str, field: str) -> int:
    try:
        arr = json.load(sys.stdin)
        print(arr[0][provider][field])
    except Exception:
        return 1
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Helper commands for run_command.sh")
    subparsers = parser.add_subparsers(dest="command", required=True)

    command_field_parser = subparsers.add_parser("command-field")
    command_field_parser.add_argument("commands_file")
    command_field_parser.add_argument("action")
    command_field_parser.add_argument("field")

    ask_message_parser = subparsers.add_parser("ask-message")
    ask_message_parser.add_argument("commands_file")
    ask_message_parser.add_argument("action")
    ask_message_parser.add_argument("key")

    image_input_parser = subparsers.add_parser("image-input")
    image_input_parser.add_argument("input_json")

    build_body_parser = subparsers.add_parser("build-body")
    build_body_parser.add_argument("commands_file")
    build_body_parser.add_argument("action")
    build_body_parser.add_argument("image_url")

    upload_policy_provider_parser = subparsers.add_parser("upload-policy-provider")
    upload_policy_value_parser = subparsers.add_parser("upload-policy-value")
    upload_policy_value_parser.add_argument("provider")
    upload_policy_value_parser.add_argument("field")

    args = parser.parse_args()

    if args.command == "command-field":
        return command_field(args.commands_file, args.action, args.field)
    if args.command == "ask-message":
        return ask_message(args.commands_file, args.action, args.key)
    if args.command == "image-input":
        return image_input(args.input_json)
    if args.command == "build-body":
        return build_body(args.commands_file, args.action, args.image_url)
    if args.command == "upload-policy-provider":
        return upload_policy_provider()
    if args.command == "upload-policy-value":
        return upload_policy_value(args.provider, args.field)
    return 1


if __name__ == "__main__":
    sys.exit(main())

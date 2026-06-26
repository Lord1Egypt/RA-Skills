#!/usr/bin/env python3
"""Convert JSON text to YAML text."""

from __future__ import annotations

import argparse
import json

import yaml

from _cli_common import emit_error, emit_success, read_input

TOOL_ID = "json-to-yaml"


def _convert_json_to_yaml(payload: str, sort_keys: bool, compact: bool) -> str:
    try:
        data = {} if not payload.strip() else json.loads(payload)
    except json.JSONDecodeError as exc:
        raise ValueError(f"JSON parse error: {exc}") from exc

    return yaml.safe_dump(
        data,
        allow_unicode=True,
        sort_keys=sort_keys or compact,
        default_flow_style=False,
        width=1000 if compact else 80,
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Convert JSON to YAML.")
    parser.add_argument("--input", help="Input text content.")
    parser.add_argument("--input-file", help="Read input text from file.")
    parser.add_argument("--output-file", help="Write output text to file.")
    parser.add_argument("--sort-keys", action="store_true", help="Sort keys before output.")
    parser.add_argument("--compact", action="store_true", help="Emit compact YAML output.")
    parser.add_argument(
        "--json",
        dest="json_mode",
        action="store_true",
        help="Emit structured JSON result payload.",
    )
    args = parser.parse_args()

    try:
        raw_text = read_input(args.input, args.input_file)
        output = _convert_json_to_yaml(raw_text, args.sort_keys, args.compact)
        return emit_success(TOOL_ID, output, args.json_mode, args.output_file)
    except Exception as exc:
        return emit_error(TOOL_ID, str(exc), args.json_mode, args.output_file)


if __name__ == "__main__":
    raise SystemExit(main())

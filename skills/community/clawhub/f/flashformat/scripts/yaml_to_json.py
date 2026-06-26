#!/usr/bin/env python3
"""Convert YAML text to JSON text."""

from __future__ import annotations

import argparse
import json

import yaml
from yaml import YAMLError

from _cli_common import emit_error, emit_success, read_input

TOOL_ID = "yaml-to-json"


def _convert_yaml_to_json(payload: str, indent_raw: str, compact_flag: bool) -> str:
    try:
        indent = int(indent_raw)
    except (TypeError, ValueError) as exc:
        raise ValueError("YAML parse error: indent must be a number.") from exc

    indent = max(0, min(8, indent))
    compact = compact_flag or indent == 0

    try:
        data = {} if not payload.strip() else yaml.safe_load(payload)
    except YAMLError as exc:
        raise ValueError(f"YAML parse error: {exc}") from exc

    json_indent = None if compact else (indent or 2)
    separators = (",", ":") if compact else None
    return json.dumps(
        data,
        ensure_ascii=False,
        indent=json_indent,
        separators=separators,
        sort_keys=False,
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Convert YAML to JSON.")
    parser.add_argument("--input", help="Input text content.")
    parser.add_argument("--input-file", help="Read input text from file.")
    parser.add_argument("--output-file", help="Write output text to file.")
    parser.add_argument("--indent", default="2", help="JSON indent size (0-8).")
    parser.add_argument("--compact", action="store_true", help="Emit compact JSON output.")
    parser.add_argument(
        "--json",
        dest="json_mode",
        action="store_true",
        help="Emit structured JSON result payload.",
    )
    args = parser.parse_args()

    try:
        raw_text = read_input(args.input, args.input_file)
        output = _convert_yaml_to_json(raw_text, args.indent, args.compact)
        return emit_success(TOOL_ID, output, args.json_mode, args.output_file)
    except Exception as exc:
        return emit_error(TOOL_ID, str(exc), args.json_mode, args.output_file)


if __name__ == "__main__":
    raise SystemExit(main())

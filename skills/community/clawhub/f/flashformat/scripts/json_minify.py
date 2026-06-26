#!/usr/bin/env python3
"""Minify JSON text to compact single-line output."""

from __future__ import annotations

import argparse
import json

from _cli_common import emit_error, emit_success, read_input

TOOL_ID = "json-minify"


def _json_minify(payload: str) -> str:
    try:
        value = json.loads(payload)
    except json.JSONDecodeError as exc:
        raise ValueError(f"JSON parse error: {exc}") from exc
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"))


def main() -> int:
    parser = argparse.ArgumentParser(description="Minify JSON.")
    parser.add_argument("--input", help="Input text content.")
    parser.add_argument("--input-file", help="Read input text from file.")
    parser.add_argument("--output-file", help="Write output text to file.")
    parser.add_argument(
        "--json",
        dest="json_mode",
        action="store_true",
        help="Emit structured JSON result payload.",
    )
    args = parser.parse_args()

    try:
        raw_text = read_input(args.input, args.input_file)
        output = _json_minify(raw_text)
        return emit_success(TOOL_ID, output, args.json_mode, args.output_file)
    except Exception as exc:
        return emit_error(TOOL_ID, str(exc), args.json_mode, args.output_file)


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Convert Markdown text to plain text."""

from __future__ import annotations

import argparse
import re

from _cli_common import emit_error, emit_success, read_input

TOOL_ID = "markdown-to-text"


def _convert_markdown_to_text(payload: str) -> str:
    value = payload.replace("\r\n", "\n").replace("\r", "\n")
    value = re.sub(r"```[\s\S]*?```", lambda match: match.group(0).strip("`"), value)
    value = re.sub(r"`([^`]+)`", r"\1", value)
    value = re.sub(r"\*\*([^*]+)\*\*", r"\1", value)
    value = re.sub(r"^#{1,6}\s*", "", value, flags=re.MULTILINE)
    value = re.sub(r"^\s*[-*+]\s+", "", value, flags=re.MULTILINE)
    value = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r"\1 (\2)", value)
    value = re.sub(r"\n{3,}", "\n\n", value)
    return value.strip()


def main() -> int:
    parser = argparse.ArgumentParser(description="Convert Markdown to plain text.")
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
        output = _convert_markdown_to_text(raw_text)
        return emit_success(TOOL_ID, output, args.json_mode, args.output_file)
    except Exception as exc:
        return emit_error(TOOL_ID, str(exc), args.json_mode, args.output_file)


if __name__ == "__main__":
    raise SystemExit(main())

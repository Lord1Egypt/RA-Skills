#!/usr/bin/env python3
"""Apply conservative YAML whitespace and indentation fixes."""

from __future__ import annotations

import argparse

import yaml
from yaml import YAMLError

from _cli_common import emit_error, emit_success, read_input

TOOL_ID = "yaml-auto-fix"


def _normalize_line_ending_kind(raw: str | None, default: str = "lf") -> str:
    if not isinstance(raw, str):
        return default
    lowered = raw.strip().lower()
    if lowered in {"lf", "\\n", "unix"}:
        return "lf"
    if lowered in {"crlf", "\\r\\n", "windows"}:
        return "crlf"
    return default


def _normalize_text_line_endings(text: str, target_kind: str) -> str:
    normalized = text.replace("\r\n", "\n").replace("\r", "\n")
    if target_kind == "crlf":
        return normalized.replace("\n", "\r\n")
    return normalized


def _leading_spaces_count(text: str) -> int:
    count = 0
    for char in text:
        if char == " ":
            count += 1
            continue
        break
    return count


def _yaml_auto_fix(
    text: str,
    indent_step_raw: str,
    fix_tabs: bool,
    fix_odd_indent: bool,
    trim_trailing_spaces: bool,
    target_line_ending: str | None,
) -> str:
    try:
        indent_step = int(indent_step_raw)
    except (TypeError, ValueError):
        indent_step = 2
    indent_step = max(2, min(8, indent_step))

    lf_text = text.replace("\r\n", "\n").replace("\r", "\n")
    fixed_lines: list[str] = []

    for raw_line in lf_text.split("\n"):
        line = raw_line
        if fix_tabs and "\t" in line:
            line = line.replace("\t", " " * indent_step)
        if trim_trailing_spaces:
            line = line.rstrip(" \t")

        leading_len = len(line) - len(line.lstrip(" \t"))
        leading = line[:leading_len]
        tail = line[leading_len:]

        if fix_odd_indent and tail and not tail.startswith("#"):
            spaces = _leading_spaces_count(leading)
            if spaces % 2 == 1:
                leading = leading[:spaces] + " " + leading[spaces:]

        fixed_lines.append(f"{leading}{tail}")

    candidate = "\n".join(fixed_lines)
    try:
        list(yaml.safe_load_all(candidate))
    except YAMLError as exc:
        raise ValueError(f"YAML is still invalid after auto-fix: {exc}") from exc

    target_kind = _normalize_line_ending_kind(target_line_ending, default="lf")
    return _normalize_text_line_endings(candidate, target_kind)


def main() -> int:
    parser = argparse.ArgumentParser(description="Auto-fix common YAML whitespace issues.")
    parser.add_argument("--input", help="Input text content.")
    parser.add_argument("--input-file", help="Read input text from file.")
    parser.add_argument("--output-file", help="Write output text to file.")
    parser.add_argument("--indent-step", default="2", help="Indent size used when replacing tabs.")
    parser.add_argument("--fix-tabs", action=argparse.BooleanOptionalAction, default=True)
    parser.add_argument("--fix-odd-indent", action=argparse.BooleanOptionalAction, default=True)
    parser.add_argument(
        "--trim-trailing-spaces",
        action=argparse.BooleanOptionalAction,
        default=True,
    )
    parser.add_argument(
        "--target-line-ending",
        default="lf",
        choices=["lf", "crlf"],
        help="Target line ending kind.",
    )
    parser.add_argument(
        "--json",
        dest="json_mode",
        action="store_true",
        help="Emit structured JSON result payload.",
    )
    args = parser.parse_args()

    try:
        raw_text = read_input(args.input, args.input_file)
        output = _yaml_auto_fix(
            raw_text,
            indent_step_raw=args.indent_step,
            fix_tabs=args.fix_tabs,
            fix_odd_indent=args.fix_odd_indent,
            trim_trailing_spaces=args.trim_trailing_spaces,
            target_line_ending=args.target_line_ending,
        )
        return emit_success(TOOL_ID, output, args.json_mode, args.output_file)
    except Exception as exc:
        return emit_error(TOOL_ID, str(exc), args.json_mode, args.output_file)


if __name__ == "__main__":
    raise SystemExit(main())

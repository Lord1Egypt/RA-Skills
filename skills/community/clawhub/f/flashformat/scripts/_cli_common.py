#!/usr/bin/env python3
"""Shared CLI I/O utilities for local converter scripts."""

from __future__ import annotations

import json
import sys
from pathlib import Path


def read_input(raw_input: str | None, input_file: str | None) -> str:
    """Load input from --input, --input-file, or stdin."""
    if raw_input is not None:
        return raw_input
    if input_file:
        try:
            return Path(input_file).read_text(encoding="utf-8")
        except OSError as exc:
            raise RuntimeError(f"Failed to read input file: {exc}") from exc
    return sys.stdin.read()


def write_output(content: str, output_file: str | None) -> None:
    """Write output to file or stdout."""
    if output_file:
        try:
            Path(output_file).write_text(content, encoding="utf-8")
        except OSError as exc:
            raise RuntimeError(f"Failed to write output file: {exc}") from exc
        return
    sys.stdout.write(content)


def emit_success(tool_id: str, output: str, json_mode: bool, output_file: str | None) -> int:
    """Emit success payload in plain or JSON mode."""
    if json_mode:
        payload = json.dumps({"ok": True, "tool": tool_id, "output": output}, ensure_ascii=False)
        write_output(payload, output_file)
        return 0
    write_output(output, output_file)
    return 0


def emit_error(tool_id: str, error: str, json_mode: bool, output_file: str | None) -> int:
    """Emit failure payload in plain or JSON mode."""
    if json_mode:
        payload = json.dumps({"ok": False, "tool": tool_id, "error": error}, ensure_ascii=False)
        try:
            write_output(payload, output_file)
        except RuntimeError as exc:
            print(error, file=sys.stderr)
            print(str(exc), file=sys.stderr)
        return 1
    print(error, file=sys.stderr)
    return 1

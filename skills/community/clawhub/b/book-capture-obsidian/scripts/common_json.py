#!/usr/bin/env python3
"""Shared JSON I/O helpers for deterministic script contracts."""

from __future__ import annotations

import json
import sys
from typing import Any, Dict, Optional


JSONDict = Dict[str, Any]


def make_result(stage: str, ok: bool, error: Optional[str] = None, **payload: Any) -> JSONDict:
    """Build a normalized result envelope used by all pipeline scripts."""
    result: JSONDict = {
        "error": error,
        "ok": ok,
        "stage": stage,
    }
    result.update(payload)
    return result


def print_json(data: JSONDict) -> None:
    """Print deterministic JSON to stdout."""
    sys.stdout.write(json.dumps(data, ensure_ascii=False, sort_keys=True, indent=2))
    sys.stdout.write("\n")


def fail_and_print(stage: str, message: str, **payload: Any) -> int:
    """Print a standardized error response and return process exit code 1."""
    print_json(make_result(stage=stage, ok=False, error=message, **payload))
    return 1


def read_json_file(path: str) -> JSONDict:
    """Read a JSON file and validate object root type."""
    with open(path, "r", encoding="utf-8") as fh:
        data = json.load(fh)
    if not isinstance(data, dict):
        raise ValueError(f"Expected JSON object in {path}, got {type(data).__name__}")
    return data

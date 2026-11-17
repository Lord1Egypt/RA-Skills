#!/usr/bin/env python3
"""Validate an agy-ppt project state file on disk.

Deterministic, read-only. Exits non-zero and prints a structured error with a
stable ``error_code`` when the state is missing, corrupt, or invalid. It never
rewrites or repairs the state file.

Usage::

    python3 validate_project.py /path/to/workspace
    python3 validate_project.py /path/to/workspace --summary
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from project_state import (  # noqa: E402
    ERROR_PROJECT_STATE_INVALID,
    ProjectState,
    ProjectStateError,
    validate_state,
)


def _emit(payload: dict, output: str | None) -> None:
    text = json.dumps(payload, ensure_ascii=False, indent=2)
    if output and output != "-":
        Path(output).write_text(text + "\n", encoding="utf-8")
    else:
        print(text)


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("workspace_root", help="workspace root containing project_state.json")
    parser.add_argument("--summary", action="store_true", help="also print the project summary")
    parser.add_argument("--output", help="write the report JSON here (default: stdout)")
    args = parser.parse_args(list(argv) if argv is not None else None)

    path = ProjectState.state_path(args.workspace_root)
    if not path.exists():
        _emit(
            {
                "valid": False,
                "error_code": ERROR_PROJECT_STATE_INVALID,
                "error_message": f"project state not found: {path}",
            },
            args.output,
        )
        return 1

    try:
        raw = path.read_text(encoding="utf-8")
        data = json.loads(raw)
    except (OSError, json.JSONDecodeError) as exc:
        _emit(
            {
                "valid": False,
                "error_code": ERROR_PROJECT_STATE_INVALID,
                "error_message": f"project state is corrupt (not overwritten): {exc}",
            },
            args.output,
        )
        return 1

    errors = validate_state(data)
    if errors:
        _emit(
            {
                "valid": False,
                "error_code": ERROR_PROJECT_STATE_INVALID,
                "errors": errors,
            },
            args.output,
        )
        return 1

    report: dict = {"valid": True, "error_code": None}
    if args.summary:
        try:
            report["summary"] = ProjectState.load(args.workspace_root).summary()
        except ProjectStateError as exc:  # pragma: no cover - already validated
            report = {"valid": False, "error_code": exc.error_code, "error_message": str(exc)}
            _emit(report, args.output)
            return 1
    _emit(report, args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

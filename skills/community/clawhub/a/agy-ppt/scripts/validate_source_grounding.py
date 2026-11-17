#!/usr/bin/env python3
"""Validate a project's source-grounding artifacts on disk (Phase 12.3).

Deterministic, read-only. This is the single invocation surface AGY uses
before assembly for a source-driven project. It contains **no validation
logic of its own**: it loads the project's slide ids from
``project_state.json`` and delegates entirely to
``source_grounding.evaluate_assembly_gate()``.

Usage::

    python3 validate_source_grounding.py /path/to/workspace
    python3 validate_source_grounding.py /path/to/workspace --source-digest src_agreement=<sha256hex>
    python3 validate_source_grounding.py /path/to/workspace --skip-grounded-qa

Exit codes::

    0  source grounding is disabled for this project, or the gate is satisfied
    1  the gate is not satisfied (grounding precondition failure -- assembly
       must NOT be started; hand back to AGY Content QA / grounding repair)
    2  the project state itself could not be read

A non-zero exit here is a **grounding precondition failure**, not an assembly
failure: ``assemble_ppt.py`` is never invoked by this script, so this must not
be recorded as, or confused with, the Phase 9 assembly-failure recovery path.
It is also not by itself a project blocker; it is a recoverable AGY workflow
issue.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from project_state import ProjectState, ProjectStateError  # noqa: E402
from source_grounding import evaluate_assembly_gate  # noqa: E402


def _parse_source_digest(values: list[str] | None) -> dict[str, str]:
    """Parse repeated ``--source-digest source_id=<sha256hex>`` arguments.

    AGY (or whatever re-reads the source material) computes these digests;
    this script never opens the source document itself.
    """
    digests: dict[str, str] = {}
    for raw in values or []:
        if "=" not in raw:
            raise SystemExit(f"--source-digest expects source_id=<sha256hex>, got: {raw!r}")
        source_id, digest = raw.split("=", 1)
        source_id = source_id.strip()
        digest = digest.strip().lower()
        if not source_id or not digest:
            raise SystemExit(f"--source-digest expects source_id=<sha256hex>, got: {raw!r}")
        digests[source_id] = digest
    return digests


def _emit(payload: dict, output: str | None) -> None:
    text = json.dumps(payload, ensure_ascii=False, indent=2)
    if output and output != "-":
        Path(output).write_text(text + "\n", encoding="utf-8")
    else:
        print(text)


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("workspace_root", help="workspace root containing project_state.json")
    parser.add_argument(
        "--source-digest",
        action="append",
        metavar="SOURCE_ID=SHA256",
        help="current sha256 digest of a source, for stale-evidence detection (repeatable)",
    )
    parser.add_argument(
        "--skip-grounded-qa",
        action="store_true",
        help="check structural/reference/coverage only, without requiring AGY's Content-QA outcome",
    )
    parser.add_argument("--output", help="write the report JSON here (default: stdout)")
    args = parser.parse_args(list(argv) if argv is not None else None)

    current_source_digests = _parse_source_digest(args.source_digest)

    try:
        state = ProjectState.load(args.workspace_root)
    except ProjectStateError as exc:
        _emit(
            {
                "ready": False,
                "error_code": exc.error_code,
                "error_message": f"could not load project state: {exc}",
            },
            args.output,
        )
        return 2

    known_slide_ids = set(state.data["slides"].keys())
    result = evaluate_assembly_gate(
        args.workspace_root,
        known_slide_ids,
        current_source_digests=current_source_digests or None,
        require_grounded_qa=not args.skip_grounded_qa,
    )

    payload = result.to_dict()
    payload["slides_checked"] = len(known_slide_ids)
    _emit(payload, args.output)
    return 0 if result.ready else 1


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Table-driven fault matrix for the Phase 9 recovery suite.

``tests/recovery/fault_matrix.json`` declares, per injected fault, the state AGY
must end up in. :func:`run_matrix_row` performs the whole inject -> record ->
reload -> assert cycle for one row, so the individual scenario files only have
to add the assertions that are specific to their fault instead of repeating the
same boilerplate five times.

Matrix row fields:

``fault``                   fault to inject in the fake worker
``expected``                short label used in the matrix (``generation_failed``,
                            ``blocked``, ``not_generated``)
``recorded_slide_status``   slide status directly after the worker result is recorded
``agy_action``              what AGY is allowed to do next (``retry_allowed`` / ``block``)
``final_slide_status``      slide status after that AGY action
``keeps_blocker_error_code``the worker error code must survive on the slide blocker
``expects_final_image``     whether a legal final ``image_path`` may exist
``expects_candidates``      whether ambiguous candidates must be preserved in diagnostics
``recovers_by``             documented recovery route
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

MATRIX_PATH = Path(__file__).resolve().parents[1] / "recovery" / "fault_matrix.json"

EXPECTED_GENERATION_FAILED = "generation_failed"
EXPECTED_BLOCKED = "blocked"
EXPECTED_NOT_GENERATED = "not_generated"

ACTION_RETRY_ALLOWED = "retry_allowed"
ACTION_BLOCK = "block"


def load_fault_matrix() -> list[dict[str, Any]]:
    rows = json.loads(MATRIX_PATH.read_text(encoding="utf-8"))
    if not isinstance(rows, list) or not rows:
        raise AssertionError(f"fault matrix must be a non-empty list: {MATRIX_PATH}")
    return rows


def rows_for(fault: str) -> list[dict[str, Any]]:
    rows = [row for row in load_fault_matrix() if row["fault"] == fault]
    if not rows:
        raise AssertionError(f"fault matrix has no row for {fault!r}")
    return rows


def attach_matrix_tests(cls: type, faults: tuple[str, ...] | list[str], slide_id: str = "slide_03") -> type:
    """Attach one real test method per matrix row to ``cls``.

    Generating methods (instead of looping inside a single test) keeps one fresh
    workspace, state file and fake worker per row, and reports each row as its
    own test result.
    """
    for fault in faults:
        for row in rows_for(fault):
            def _test(self: Any, _row: dict[str, Any] = row) -> None:
                run_matrix_row(self, _row, slide_id=slide_id)

            _test.__name__ = f"test_matrix_{row['id']}"
            _test.__doc__ = f"fault matrix row {row['id']}: {row['fault']} -> {row['expected']}"
            setattr(cls, _test.__name__, _test)
    return cls


def run_matrix_row(case: Any, row: dict[str, Any], slide_id: str = "slide_03") -> dict[str, Any]:
    """Inject one matrix row against ``slide_id`` and assert its contract.

    ``case`` is a :class:`helpers.recovery_deck.RecoveryTestCase`. Returns the
    slide dict as it stands on disk after a full reload.
    """
    from helpers.recovery_deck import (  # local import: avoids a helper import cycle
        SLIDE_BLOCKED,
        SLIDE_READY,
    )

    case.advance_to_slide_generation()
    case.worker.set_plan(slide_id, fault=row["fault"])
    outcome = case.dispatch(slide_id)

    case.assertEqual(outcome.status, "error", f"{row['id']}: worker must report an error")
    case.assertEqual(outcome.error_code, row["fault"], f"{row['id']}: error_code preserved")
    case.assert_slide(slide_id, row["recorded_slide_status"])

    if row["keeps_blocker_error_code"]:
        blocker = case.state.slide(slide_id).get("blocker") or {}
        case.assertEqual(
            blocker.get("error_code"), row["fault"], f"{row['id']}: blocker error_code preserved"
        )

    if not row["expects_final_image"]:
        case.assert_not_generated(slide_id)

    if row["expects_candidates"]:
        attempt = case.state.slide(slide_id)["attempts"][-1]
        discovery = (attempt.get("diagnostics") or {}).get("artifact_discovery") or {}
        case.assertTrue(discovery.get("ambiguous"), f"{row['id']}: ambiguity flag preserved")
        case.assertGreaterEqual(
            len(discovery.get("candidates") or []), 2, f"{row['id']}: candidates preserved"
        )

    if row["agy_action"] == ACTION_BLOCK:
        case.block_slide(slide_id)
        case.block_project(note=row["fault"])

    # The verdict must survive a full reload from disk.
    case.reload()
    slide = case.assert_slide(slide_id, row["final_slide_status"])

    if row["final_slide_status"] == SLIDE_BLOCKED:
        case.assertEqual(slide.get("phase_before_block"), row["recorded_slide_status"])
    if row["agy_action"] == ACTION_RETRY_ALLOWED:
        # Retry must be a legal, explicit AGY move (no auto-retry anywhere).
        case.state.set_slide_status(slide_id, SLIDE_READY)
        case.assertEqual(case.state.slide(slide_id)["status"], SLIDE_READY)
    return slide

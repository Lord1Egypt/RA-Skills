#!/usr/bin/env python3
"""Recovery scenario 2: the image backend is unavailable.

The built-in ``image_gen`` tool is not exposed, so the worker returns
``IMAGE_BACKEND_UNAVAILABLE`` (it must never fall back to a billed API).

Contract under test:

* the slide is never marked ``generated``
* the slide and the project enter an explicit, legal blocked state, remembering
  where to resume from
* the whole verdict (error code, attempt history, finished slides) survives a
  reload from disk
* once the backend is back, AGY can resume and only the blocked slide is
  re-generated -- finished slides keep their generation counter and their image
  bytes
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

TESTS_DIR = Path(__file__).resolve().parents[1]
if str(TESTS_DIR) not in sys.path:
    sys.path.insert(0, str(TESTS_DIR))

from helpers.fault_matrix import attach_matrix_tests  # noqa: E402
from helpers.fake_image_worker import FAULT_BACKEND_UNAVAILABLE  # noqa: E402
from helpers.recovery_deck import (  # noqa: E402
    PHASE_BLOCKED,
    PHASE_SLIDE_GENERATION,
    SLIDE_BLOCKED,
    SLIDE_GENERATED,
    SLIDE_GENERATION_FAILED,
    SLIDE_READY,
    RecoveryTestCase,
    plan_dispatch,
)
from project_state import InvalidStateTransition  # noqa: E402


class BackendUnavailableTests(RecoveryTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.advance_to_slide_generation()
        self.dispatch("slide_01")
        self.dispatch("slide_02")
        self.settled_before = self.snapshot(["slide_01", "slide_02"])
        self.images_before = self.image_digests()
        self.worker.set_plan(
            "slide_03", fault=FAULT_BACKEND_UNAVAILABLE, succeed_on=2
        )
        self.outcome = self.dispatch("slide_03")

    # -- immediate aftermath ----------------------------------------------
    def test_worker_reports_backend_unavailable_without_api_fallback(self):
        self.assertEqual(self.outcome.error_code, FAULT_BACKEND_UNAVAILABLE)
        self.assertFalse(self.outcome.result["diagnostics"]["api_fallback_used"])
        self.assertEqual(self.outcome.result["diagnostics"]["auth"], "chatgpt_cli_session")

    def test_slide_is_not_generated(self):
        self.assert_slide("slide_03", SLIDE_GENERATION_FAILED, generation=1, attempts=1)
        self.assert_not_generated("slide_03")

    def test_agy_can_block_slide_and_project(self):
        self.block_slide("slide_03")
        self.block_project(note=FAULT_BACKEND_UNAVAILABLE)
        self.assertEqual(self.state.phase, PHASE_BLOCKED)
        slide = self.state.slide("slide_03")
        self.assertEqual(slide["status"], SLIDE_BLOCKED)
        self.assertEqual(slide["phase_before_block"], SLIDE_GENERATION_FAILED)
        self.assertEqual(self.state.data["phase_before_block"], PHASE_SLIDE_GENERATION)

    def test_blocked_state_is_preserved_across_reload(self):
        self.block_slide("slide_03")
        self.block_project(note=FAULT_BACKEND_UNAVAILABLE)
        self.reload()
        self.assertEqual(self.state.phase, PHASE_BLOCKED)
        self.assert_slide("slide_03", SLIDE_BLOCKED, generation=1, attempts=1)
        attempt = self.state.slide("slide_03")["attempts"][0]
        self.assertEqual(attempt["error_code"], FAULT_BACKEND_UNAVAILABLE)
        self.assert_untouched(["slide_01", "slide_02"], self.settled_before)

    def test_blocked_project_cannot_skip_ahead(self):
        self.block_project(note=FAULT_BACKEND_UNAVAILABLE)
        with self.assertRaises(InvalidStateTransition):
            self.state.set_phase("assembly")

    def test_no_dispatch_while_blocked(self):
        self.block_slide("slide_03")
        self.block_project(note=FAULT_BACKEND_UNAVAILABLE)
        self.reload()
        self.assertEqual(plan_dispatch(self.state), [])

    # -- resume after the backend returns ----------------------------------
    def test_resume_after_backend_returns(self):
        self.block_slide("slide_03")
        self.block_project(note=FAULT_BACKEND_UNAVAILABLE)
        self.reload()

        # Backend is back. AGY resumes explicitly: project first, then slide.
        self.state.set_phase(PHASE_SLIDE_GENERATION, note="backend recovered")
        self.state.set_slide_status("slide_03", SLIDE_READY)
        self.state.save()
        self.assertEqual(self.state.phase, PHASE_SLIDE_GENERATION)
        self.assertIsNone(self.state.data["phase_before_block"])
        self.assertEqual(plan_dispatch(self.state), ["slide_03", "slide_04"])

        outcome = self.dispatch("slide_03")
        self.assertEqual(outcome.status, "completed")
        self.assertEqual(outcome.generation, 2)
        self.assert_slide("slide_03", SLIDE_GENERATED, generation=2, attempts=2)
        self.assert_valid_final_image("slide_03")

    def test_finished_slides_are_not_regenerated_by_resume(self):
        self.block_slide("slide_03")
        self.block_project(note=FAULT_BACKEND_UNAVAILABLE)
        self.reload()
        self.state.set_phase(PHASE_SLIDE_GENERATION, note="backend recovered")
        self.state.set_slide_status("slide_03", SLIDE_READY)
        self.state.save()
        self.dispatch("slide_03")

        self.assert_untouched(["slide_01", "slide_02"], self.settled_before)
        for slide_id in ("slide_01", "slide_02"):
            self.assertEqual(len(self.worker.calls_for(slide_id)), 1)
        for rel, digest in self.images_before.items():
            self.assertEqual(self.image_digests()[rel], digest, f"{rel} was rewritten")


class BackendUnavailableMatrixTests(RecoveryTestCase):
    """Table-driven row: ``IMAGE_BACKEND_UNAVAILABLE`` -> blocked."""


attach_matrix_tests(BackendUnavailableMatrixTests, (FAULT_BACKEND_UNAVAILABLE,))


if __name__ == "__main__":
    unittest.main()

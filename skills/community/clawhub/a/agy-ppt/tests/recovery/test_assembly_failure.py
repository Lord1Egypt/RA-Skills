#!/usr/bin/env python3
"""Recovery scenario 7: assembly fails after every slide passed QA.

Contract under test:

* a failed assembly never re-generates a slide image (no worker call, no changed
  image bytes)
* ``qa_passed`` verdicts are not lost
* the project cannot regress from ``assembly`` back to ``slide_generation``
* a failed assembly writes no partial deck file
* if AGY blocks on the failure, resume must return to ``assembly`` -- not to
  slide generation
* after the assembly problem is fixed, only assembly is re-run: the second run
  succeeds, slides become ``assembled`` and the project reaches ``complete``
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

TESTS_DIR = Path(__file__).resolve().parents[1]
if str(TESTS_DIR) not in sys.path:
    sys.path.insert(0, str(TESTS_DIR))

from helpers.fake_assembly import ERROR_ASSEMBLY_INPUT_MISSING  # noqa: E402
from helpers.recovery_deck import (  # noqa: E402
    PHASE_ASSEMBLY,
    PHASE_BLOCKED,
    PHASE_COMPLETE,
    PHASE_SLIDE_GENERATION,
    PHASE_VISUAL_QA,
    SLIDE_ASSEMBLED,
    SLIDE_QA_PASSED,
    RecoveryTestCase,
    plan_dispatch,
)
from project_state import InvalidStateTransition  # noqa: E402


class AssemblyFailureTests(RecoveryTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.advance_to_slide_generation()
        for slide_id in self.slide_ids:
            self.dispatch(slide_id)
            self.qa_pass(slide_id)
        self.state.set_phase(PHASE_VISUAL_QA)
        self.state.set_phase(PHASE_ASSEMBLY)
        self.state.save()

        self.qa_before = self.snapshot()
        self.images_before = self.image_digests()
        self.worker_calls_before = self.worker.call_count

        self.assembly = self.new_assembly(fail_times=1)
        self.first_result = self.assembly.run(self.state)

    def _mark_assembled(self) -> None:
        for slide_id in self.slide_ids:
            self.state.set_slide_status(slide_id, SLIDE_ASSEMBLED)
        self.state.set_phase(PHASE_COMPLETE)
        self.state.save()

    # -- first (failed) assembly ------------------------------------------
    def test_first_assembly_fails_with_error_code(self):
        self.assertEqual(self.first_result["status"], "error")
        self.assertEqual(self.first_result["error_code"], "ASSEMBLY_FAILED")
        self.assertEqual(sorted(self.first_result["slides"]), list(self.slide_ids))

    def test_failed_assembly_writes_no_deck_file(self):
        self.assertFalse(self.assembly.output_path.exists())

    def test_failed_assembly_does_not_regenerate_images(self):
        self.assertEqual(self.worker.call_count, self.worker_calls_before)
        self.assertEqual(self.image_digests(), self.images_before)

    def test_qa_passed_verdicts_survive(self):
        for slide_id in self.slide_ids:
            self.assert_slide(slide_id, SLIDE_QA_PASSED, generation=1, attempts=1)
        self.reload()
        self.assert_untouched(self.slide_ids, self.qa_before)

    def test_project_cannot_regress_to_slide_generation(self):
        self.assertEqual(self.state.phase, PHASE_ASSEMBLY)
        with self.assertRaises(InvalidStateTransition):
            self.state.set_phase(PHASE_SLIDE_GENERATION)
        with self.assertRaises(InvalidStateTransition):
            self.state.set_phase(PHASE_VISUAL_QA)
        self.assertEqual(self.state.phase, PHASE_ASSEMBLY)

    def test_no_slide_is_dispatchable_after_assembly_failure(self):
        self.reload()
        self.assertEqual(plan_dispatch(self.state), [])

    def test_blocked_assembly_resumes_to_assembly_only(self):
        self.block_project(note="ASSEMBLY_FAILED")
        self.reload()
        self.assertEqual(self.state.phase, PHASE_BLOCKED)
        self.assertEqual(self.state.data["phase_before_block"], PHASE_ASSEMBLY)
        with self.assertRaises(InvalidStateTransition):
            self.state.set_phase(PHASE_SLIDE_GENERATION)
        self.state.set_phase(PHASE_ASSEMBLY, note="assembly fixed")
        self.state.save()
        self.assertEqual(self.state.phase, PHASE_ASSEMBLY)

    # -- second (successful) assembly -------------------------------------
    def test_only_assembly_is_rerun_and_project_completes(self):
        self.assembly.fix()
        second = self.assembly.run(self.state)

        self.assertEqual(second["status"], "completed")
        self.assertEqual(self.assembly.call_count, 2)
        self.assertTrue(self.assembly.output_path.is_file())
        # No image was regenerated between the two assembly runs.
        self.assertEqual(self.worker.call_count, self.worker_calls_before)
        self.assertEqual(self.image_digests(), self.images_before)
        self.assertEqual(self.assembly.calls[0].image_digests, self.assembly.calls[1].image_digests)

        self._mark_assembled()
        self.reload()
        self.assertEqual(self.state.phase, PHASE_COMPLETE)
        for slide_id in self.slide_ids:
            self.assert_slide(slide_id, SLIDE_ASSEMBLED, generation=1, attempts=1)

    def test_missing_image_is_reported_instead_of_silently_assembling(self):
        (self.ws / self.state.slide("slide_02")["image_path"]).unlink()
        self.assembly.fix()
        result = self.assembly.run(self.state)
        self.assertEqual(result["status"], "error")
        self.assertEqual(result["error_code"], ERROR_ASSEMBLY_INPUT_MISSING)
        self.assertEqual(result["missing_images"], ["slide_02"])
        self.assertFalse(self.assembly.output_path.exists())
        # The deck stays in assembly; AGY decides what to do next.
        self.assertEqual(self.state.phase, PHASE_ASSEMBLY)


if __name__ == "__main__":
    unittest.main()

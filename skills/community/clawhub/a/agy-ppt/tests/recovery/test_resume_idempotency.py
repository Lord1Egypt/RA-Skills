#!/usr/bin/env python3
"""Recovery scenario 8: resume and idempotency.

Contract under test:

* recording the same worker result twice does not bump ``generation``, does not
  bump the attempt count, and does not duplicate history
* a duplicate record without an idempotency key is refused rather than
  double-counted
* resuming an unfinished project only dispatches the slides that still need work
* resuming twice does not dispatch twice
* resuming a ``complete`` project calls no worker at all
* a phase is never advanced twice for the same transition
* reload -> save -> reload is stable (no drift in the state file)
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

TESTS_DIR = Path(__file__).resolve().parents[1]
if str(TESTS_DIR) not in sys.path:
    sys.path.insert(0, str(TESTS_DIR))

from helpers.fake_image_worker import FAULT_GENERATION_FAILED  # noqa: E402
from helpers.recovery_deck import (  # noqa: E402
    PHASE_ASSEMBLY,
    PHASE_COMPLETE,
    PHASE_VISUAL_QA,
    SLIDE_ASSEMBLED,
    SLIDE_GENERATED,
    SLIDE_GENERATION_FAILED,
    RecoveryTestCase,
    plan_dispatch,
)
from project_state import InvalidStateTransition  # noqa: E402


class ResumeIdempotencyTests(RecoveryTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.advance_to_slide_generation()

    # -- helpers -----------------------------------------------------------
    def resume(self) -> list[str]:
        """One deterministic resume pass: recover, then dispatch what is left."""
        self.reload()
        if self.state.recover_interrupted():
            self.state.save()
        dispatched = []
        for slide_id in plan_dispatch(self.state):
            self.dispatch(slide_id)
            dispatched.append(slide_id)
        return dispatched

    def complete_project(self) -> None:
        for slide_id in self.slide_ids:
            self.dispatch(slide_id)
            self.qa_pass(slide_id)
        self.state.set_phase(PHASE_VISUAL_QA)
        self.state.set_phase(PHASE_ASSEMBLY)
        for slide_id in self.slide_ids:
            self.state.set_slide_status(slide_id, SLIDE_ASSEMBLED)
        self.state.set_phase(PHASE_COMPLETE)
        self.state.save()

    # -- duplicate worker results ------------------------------------------
    def test_duplicate_record_with_same_key_is_a_no_op(self):
        self.mark_ready("slide_01")
        generation = self.state.begin_generation("slide_01")
        result = self.worker.run("slide_01", generation=generation)
        first = self.state.record_worker_result("slide_01", result, idempotency_key="run-1")
        second = self.state.record_worker_result("slide_01", result, idempotency_key="run-1")
        self.state.save()

        self.assertIs(first, second)
        slide = self.assert_slide("slide_01", SLIDE_GENERATED, generation=1, attempts=1)
        self.assertEqual([a["idempotency_key"] for a in slide["attempts"]], ["run-1"])

    def test_duplicate_record_after_qa_is_still_a_no_op(self):
        self.mark_ready("slide_01")
        generation = self.state.begin_generation("slide_01")
        result = self.worker.run("slide_01", generation=generation)
        self.state.record_worker_result("slide_01", result, idempotency_key="run-1")
        self.qa_pass("slide_01")

        replay = self.state.record_worker_result("slide_01", result, idempotency_key="run-1")
        self.state.save()
        self.assertEqual(replay["generation"], 1)
        slide = self.assert_slide("slide_01", "qa_passed", generation=1, attempts=1)
        self.assertEqual(slide["status"], "qa_passed", "a replayed result must not undo QA")

    def test_duplicate_record_without_key_is_refused(self):
        outcome = self.dispatch("slide_01")
        before = self.snapshot(["slide_01"])
        with self.assertRaises(InvalidStateTransition):
            self.state.record_worker_result("slide_01", outcome.result)
        self.assert_untouched(["slide_01"], before)

    def test_duplicate_error_record_does_not_duplicate_history(self):
        self.worker.set_plan("slide_03", fault=FAULT_GENERATION_FAILED)
        self.mark_ready("slide_03")
        generation = self.state.begin_generation("slide_03")
        result = self.worker.run("slide_03", generation=generation)
        self.state.record_worker_result("slide_03", result, idempotency_key="run-err")
        self.state.record_worker_result("slide_03", result, idempotency_key="run-err")
        self.state.save()
        self.assert_slide("slide_03", SLIDE_GENERATION_FAILED, generation=1, attempts=1)

    # -- resume ------------------------------------------------------------
    def test_resume_only_dispatches_unfinished_slides(self):
        self.dispatch("slide_01")
        self.qa_pass("slide_01")
        self.dispatch("slide_02")
        before = self.snapshot(["slide_01", "slide_02"])
        images_before = self.image_digests()

        dispatched = self.resume()
        self.assertEqual(dispatched, ["slide_03", "slide_04"])
        self.assert_untouched(["slide_01", "slide_02"], before)
        for rel, digest in images_before.items():
            self.assertEqual(self.image_digests()[rel], digest, f"{rel} was rewritten")

    def test_second_resume_dispatches_nothing(self):
        first = self.resume()
        self.assertEqual(first, list(self.slide_ids))
        calls_after_first = self.worker.call_count

        self.assertEqual(self.resume(), [])
        self.assertEqual(self.worker.call_count, calls_after_first)
        for slide_id in self.slide_ids:
            self.assert_slide(slide_id, SLIDE_GENERATED, generation=1, attempts=1)

    def test_resume_of_completed_project_calls_no_worker(self):
        self.complete_project()
        calls_before = self.worker.call_count

        for _ in range(3):
            self.assertEqual(self.resume(), [])

        self.assertEqual(self.worker.call_count, calls_before)
        self.assertEqual(self.state.phase, PHASE_COMPLETE)
        for slide_id in self.slide_ids:
            self.assert_slide(slide_id, SLIDE_ASSEMBLED, generation=1, attempts=1)

    def test_completed_project_cannot_advance_further(self):
        self.complete_project()
        for target in (PHASE_ASSEMBLY, PHASE_VISUAL_QA, "slide_generation"):
            with self.assertRaises(InvalidStateTransition):
                self.state.set_phase(target)
        self.assertEqual(self.state.phase, PHASE_COMPLETE)

    # -- phase / state stability ------------------------------------------
    def test_phase_is_not_advanced_twice(self):
        for slide_id in self.slide_ids:
            self.dispatch(slide_id)
            self.qa_pass(slide_id)
        self.state.set_phase(PHASE_VISUAL_QA)
        history_len = len(self.state.data["history"])
        self.state.set_phase(PHASE_VISUAL_QA)  # repeat: no-op
        self.state.save()
        self.assertEqual(len(self.state.data["history"]), history_len)
        transitions = [(h["from"], h["to"]) for h in self.state.data["history"]]
        self.assertEqual(len(transitions), len(set(transitions)), "duplicate phase transition")

    def test_reload_save_reload_is_stable(self):
        self.dispatch("slide_01")
        self.reload()
        first = {k: v for k, v in self.state.data.items() if k != "updated_at"}
        self.state.save()
        self.reload()
        second = {k: v for k, v in self.state.data.items() if k != "updated_at"}
        self.assertEqual(first, second)

    def test_recover_interrupted_on_settled_project_is_a_no_op(self):
        self.complete_project()
        before = self.snapshot()
        self.reload()
        self.assertEqual(self.state.recover_interrupted(), [])
        self.assert_untouched(self.slide_ids, before)


if __name__ == "__main__":
    unittest.main()

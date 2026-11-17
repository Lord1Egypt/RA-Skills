#!/usr/bin/env python3
"""Recovery scenario 5: the process died mid-generation.

A slide is left in ``generating`` on disk. Recovery must be deterministic and
must never guess success:

* no recorded completed attempt                    -> ``generation_failed``
* completed attempt but the artifact is gone       -> ``generation_failed``
* artifact on disk but no recorded result          -> ``generation_failed``
* recorded completed attempt **and** verified artifact -> ``generated``

Slides that were not in flight are never touched by recovery, and the generation
counter is never bumped by recovery itself.
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

TESTS_DIR = Path(__file__).resolve().parents[1]
if str(TESTS_DIR) not in sys.path:
    sys.path.insert(0, str(TESTS_DIR))

from helpers.fake_image_worker import FAULT_INTERRUPTED  # noqa: E402
from helpers.recovery_deck import (  # noqa: E402
    SLIDE_GENERATED,
    SLIDE_GENERATING,
    SLIDE_GENERATION_FAILED,
    SLIDE_PLANNED,
    SLIDE_QA_PASSED,
    RecoveryTestCase,
)


class InterruptedGenerationTests(RecoveryTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.advance_to_slide_generation()
        self.dispatch("slide_01")
        self.qa_pass("slide_01")
        self.dispatch("slide_02")
        self.settled_before = self.snapshot(["slide_01", "slide_02"])

    # -- unknown outcome must never become success -------------------------
    def test_generating_on_disk_without_result_recovers_as_failed(self):
        generation = self.simulate_crash_while_generating("slide_03")
        self.assertEqual(generation, 1)

        # Fresh process: read the state back exactly as it was left.
        self.reload()
        self.assert_slide("slide_03", SLIDE_GENERATING, generation=1, attempts=0)

        recovered = self.state.recover_interrupted()
        self.state.save()
        self.assertEqual(recovered, ["slide_03"])

        slide = self.assert_slide("slide_03", SLIDE_GENERATION_FAILED, generation=1, attempts=0)
        self.assertIsNone(slide["generating_attempt"])
        self.assertIsNone(slide["image_path"])
        self.assertIn("interrupted", (slide["blocker"] or {}).get("reason", ""))

    def test_worker_interrupted_after_artifact_still_recovers_as_failed(self):
        # The artifact exists but AGY never received a result: unconfirmed.
        self.worker.set_plan("slide_03", fault=FAULT_INTERRUPTED, fault_artifact=True)
        outcome = self.dispatch("slide_03")
        self.assertTrue(outcome.interrupted)
        self.assertIsNone(outcome.result)
        self.assertTrue((self.ws / "origin_image" / "slide_03.png").is_file())

        self.reload()
        self.assert_slide("slide_03", SLIDE_GENERATING, attempts=0)
        self.state.recover_interrupted()
        self.state.save()

        slide = self.assert_slide("slide_03", SLIDE_GENERATION_FAILED, generation=1, attempts=0)
        self.assertIsNone(slide["image_path"], "an unrecorded artifact must not be adopted")

    def test_completed_attempt_without_artifact_recovers_as_failed(self):
        self.simulate_crash_after_completed_result("slide_03", keep_artifact=False)
        self.reload()
        self.assert_slide("slide_03", SLIDE_GENERATING, generation=1, attempts=1)

        self.state.recover_interrupted()
        self.state.save()
        self.assert_slide("slide_03", SLIDE_GENERATION_FAILED, generation=1, attempts=1)

    # -- confirmed outcome may deterministically recover -------------------
    def test_completed_attempt_with_artifact_recovers_as_generated(self):
        self.simulate_crash_after_completed_result("slide_03", keep_artifact=True)
        self.reload()
        self.assert_slide("slide_03", SLIDE_GENERATING, generation=1, attempts=1)

        recovered = self.state.recover_interrupted()
        self.state.save()
        self.assertEqual(recovered, ["slide_03"])

        slide = self.assert_slide("slide_03", SLIDE_GENERATED, generation=1, attempts=1)
        self.assertIsNone(slide["generating_attempt"])
        self.assert_valid_final_image("slide_03")

    def test_artifact_existence_can_be_supplied_explicitly(self):
        self.simulate_crash_after_completed_result("slide_03", keep_artifact=True)
        self.reload()
        # Caller says the artifact is not confirmed -> no optimistic success.
        self.state.recover_interrupted(artifact_exists={"origin_image/slide_03.png": False})
        self.state.save()
        self.assert_slide("slide_03", SLIDE_GENERATION_FAILED, generation=1, attempts=1)

    # -- recovery blast radius --------------------------------------------
    def test_recovery_does_not_touch_other_slides(self):
        self.simulate_crash_while_generating("slide_03")
        self.reload()
        self.state.recover_interrupted()
        self.state.save()

        self.assert_untouched(["slide_01", "slide_02"], self.settled_before)
        self.assert_slide("slide_01", SLIDE_QA_PASSED, generation=1)
        self.assert_slide("slide_02", SLIDE_GENERATED, generation=1)
        self.assert_slide("slide_04", SLIDE_PLANNED, generation=0, attempts=0)

    def test_recovery_is_idempotent(self):
        self.simulate_crash_while_generating("slide_03")
        self.reload()
        self.assertEqual(self.state.recover_interrupted(), ["slide_03"])
        self.assertEqual(self.state.recover_interrupted(), [], "nothing left to recover")
        self.state.save()
        self.assert_slide("slide_03", SLIDE_GENERATION_FAILED, generation=1, attempts=0)

    def test_recovery_does_not_advance_phase(self):
        self.simulate_crash_while_generating("slide_03")
        self.reload()
        self.state.recover_interrupted()
        self.state.save()
        self.assertEqual(self.state.phase, "slide_generation")

    # -- retry after recovery ---------------------------------------------
    def test_retry_after_interrupted_recovery(self):
        self.simulate_crash_while_generating("slide_03")
        self.reload()
        self.state.recover_interrupted()
        self.state.save()

        self.retry("slide_03")
        outcome = self.dispatch("slide_03")
        self.assertEqual(outcome.status, "completed")
        self.assert_slide("slide_03", SLIDE_GENERATED, generation=2, attempts=1)
        self.assert_valid_final_image("slide_03")


if __name__ == "__main__":
    unittest.main()

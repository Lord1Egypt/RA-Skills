#!/usr/bin/env python3
"""Recovery scenario 6: AGY fails visual QA and regenerates.

generation 1 completed -> AGY ``qa_failed`` -> ``ready`` -> generation 2
completed -> AGY ``qa_passed``.

Contract under test:

* the generation counter and the attempt history both reach 2
* attempt 1 is still in history and is not overwritten by attempt 2
* only AGY can make the QA judgement (a worker-attributed judgement is refused)
* a Codex ``completed`` result never becomes ``qa_passed`` on its own
* other slides are untouched, both in state and in image bytes
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

TESTS_DIR = Path(__file__).resolve().parents[1]
if str(TESTS_DIR) not in sys.path:
    sys.path.insert(0, str(TESTS_DIR))

from helpers.recovery_deck import (  # noqa: E402
    SLIDE_GENERATED,
    SLIDE_QA_FAILED,
    SLIDE_QA_PASSED,
    SLIDE_READY,
    RecoveryTestCase,
)
from project_state import InvalidStateTransition  # noqa: E402


class QaRegenerationTests(RecoveryTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.advance_to_slide_generation()
        self.dispatch("slide_01")
        self.qa_pass("slide_01")
        self.dispatch("slide_02")
        self.settled_before = self.snapshot(["slide_01", "slide_02"])
        self.images_before = self.image_digests()
        self.first = self.dispatch("slide_03")

    def test_generation_one_completes_but_is_not_qa_passed(self):
        self.assertEqual(self.first.status, "completed")
        self.assert_slide("slide_03", SLIDE_GENERATED, generation=1, attempts=1)

    def test_worker_cannot_make_the_qa_judgement(self):
        with self.assertRaises(InvalidStateTransition):
            self.state.set_slide_status("slide_03", SLIDE_QA_PASSED, by="codex")
        with self.assertRaises(InvalidStateTransition):
            self.state.set_slide_status("slide_03", SLIDE_QA_FAILED, by="kiro")
        self.assert_slide("slide_03", SLIDE_GENERATED)

    def test_qa_failed_then_regeneration_reaches_qa_passed(self):
        self.qa_fail("slide_03")
        self.assert_slide("slide_03", SLIDE_QA_FAILED, generation=1, attempts=1)

        self.retry("slide_03")
        self.assert_slide("slide_03", SLIDE_READY, generation=1)

        second = self.dispatch("slide_03")
        self.assertEqual(second.status, "completed")
        self.assertEqual(second.generation, 2)
        self.assert_slide("slide_03", SLIDE_GENERATED, generation=2, attempts=2)

        self.qa_pass("slide_03")
        self.assert_slide("slide_03", SLIDE_QA_PASSED, generation=2, attempts=2)
        self.assert_valid_final_image("slide_03")

    def test_attempt_one_history_is_preserved_and_not_overwritten(self):
        first_attempt = dict(self.state.slide("slide_03")["attempts"][0])
        self.qa_fail("slide_03")
        self.retry("slide_03")
        self.dispatch("slide_03")
        self.qa_pass("slide_03")
        self.reload()

        attempts = self.state.slide("slide_03")["attempts"]
        self.assertEqual(len(attempts), 2)
        self.assertEqual(attempts[0], first_attempt, "attempt 1 was mutated")
        self.assertEqual([a["generation"] for a in attempts], [1, 2])
        self.assertNotEqual(attempts[0]["idempotency_key"], attempts[1]["idempotency_key"])
        self.assertEqual(len(self.worker.calls_for("slide_03")), 2)

    def test_other_slides_unaffected_by_regeneration(self):
        self.qa_fail("slide_03")
        self.retry("slide_03")
        self.dispatch("slide_03")
        self.qa_pass("slide_03")

        self.assert_untouched(["slide_01", "slide_02"], self.settled_before)
        digests_after = self.image_digests()
        for rel, digest in self.images_before.items():
            self.assertEqual(digests_after[rel], digest, f"{rel} was rewritten")
        self.assertEqual(len(self.worker.calls_for("slide_01")), 1)
        self.assertEqual(len(self.worker.calls_for("slide_02")), 1)

    def test_qa_passed_slide_cannot_be_regenerated_without_a_new_decision(self):
        self.qa_pass("slide_03")
        with self.assertRaises(InvalidStateTransition):
            self.state.set_slide_status("slide_03", SLIDE_READY)
        with self.assertRaises(InvalidStateTransition):
            self.state.begin_generation("slide_03")
        self.assert_slide("slide_03", SLIDE_QA_PASSED, generation=1, attempts=1)


if __name__ == "__main__":
    unittest.main()

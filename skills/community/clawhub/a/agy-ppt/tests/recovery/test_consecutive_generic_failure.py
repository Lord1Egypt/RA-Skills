#!/usr/bin/env python3
"""Phase 10.2 -- consecutive generic ``IMAGE_GENERATION_FAILED`` retry policy.

Runtime evidence that motivated this scenario: a real Codex render turn
returned ``returncode = 1`` with only ``Reading prompt from stdin...`` on
stderr and no machine-readable quota / usage-limit / rate-limit signal. The
adapter correctly reported the generic ``IMAGE_GENERATION_FAILED`` error_code.
An operator separately confirmed (via an external UI) that the account's
subscription quota was exhausted at the time -- but the subprocess evidence
alone cannot deterministically prove that. Retrying that generic failure
forever without limit is the actual production gap this scenario locks down:

* the SAME slide failing with the SAME generic error_code twice in a row gets
  exactly one immediate retry, never a third;
* a second consecutive failure blocks the slide and the whole project instead
  of silently retrying or dispatching later slides;
* a success resets the failure streak, and one slide's failure never
  contaminates another slide's streak;
* the worker's ``error_code`` is never rewritten into a quota-specific code by
  this layer -- only an operator/AGY decision may record
  ``subscription_quota_exhausted``, and it does so as a separate, clearly
  provenanced project-level record, never as a fabricated worker result.

No real Codex, Kiro, or ``image_gen`` call is made; no subscription quota is
consumed. All faults are injected in memory via ``FakeImageWorker``.
"""

from __future__ import annotations

import sys
from pathlib import Path

TESTS_DIR = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = TESTS_DIR.parent / "scripts"
for _path in (str(TESTS_DIR), str(SCRIPTS_DIR)):
    if _path not in sys.path:
        sys.path.insert(0, _path)

from project_state import (  # noqa: E402
    ERROR_IMAGE_GENERATION_FAILED,
    PHASE_BLOCKED,
    PHASE_SLIDE_GENERATION,
    SLIDE_BLOCKED,
    SLIDE_GENERATED,
    SLIDE_GENERATION_FAILED,
    SLIDE_PLANNED,
    SLIDE_QA_PASSED,
    SLIDE_READY,
)

from helpers.fake_image_worker import FAULT_GENERATION_FAILED, FakeImageWorker, SlidePlan  # noqa: E402
from helpers.recovery_deck import RecoveryTestCase, plan_dispatch  # noqa: E402

SLIDES = ("slide_01", "slide_02", "slide_03", "slide_04", "slide_05")


class ConsecutiveGenericFailureTests(RecoveryTestCase):
    slide_ids = SLIDES

    def setUp(self) -> None:
        super().setUp()
        self.advance_to_slide_generation()

    # -- 1. first failure allows exactly one immediate retry ---------------
    def test_first_failure_allows_one_retry(self):
        self.worker.set_plan("slide_01", fault=FAULT_GENERATION_FAILED, succeed_on=2)

        outcome = self.dispatch("slide_01")
        self.assertEqual(outcome.error_code, ERROR_IMAGE_GENERATION_FAILED)
        self.assert_slide("slide_01", SLIDE_GENERATION_FAILED, generation=1, attempts=1)

        self.assertEqual(self.state.consecutive_failure_streak("slide_01"), 1)
        self.assertTrue(self.state.may_retry_immediately("slide_01"))

        # AGY performs the one allowed immediate retry.
        self.retry("slide_01")
        self.assert_slide("slide_01", SLIDE_READY)

    # -- 2. retry success -> workflow continues -----------------------------
    def test_retry_success_continues_workflow(self):
        self.worker.set_plan("slide_01", fault=FAULT_GENERATION_FAILED, succeed_on=2)
        self.dispatch("slide_01")
        self.retry("slide_01")

        outcome = self.dispatch("slide_01")
        self.assertEqual(outcome.status, "completed")
        self.assert_slide("slide_01", SLIDE_GENERATED, generation=2, attempts=2)
        self.assertEqual(self.state.phase, PHASE_SLIDE_GENERATION)

        # Continuing the workflow: QA-pass it and dispatch the next slide.
        self.qa_pass("slide_01")
        self.assert_slide("slide_01", SLIDE_QA_PASSED)
        outcome2 = self.dispatch("slide_02")
        self.assertEqual(outcome2.status, "completed")

    # -- 8. failure streak resets after success -----------------------------
    def test_failure_streak_resets_after_success(self):
        self.worker.set_plan("slide_01", fault=FAULT_GENERATION_FAILED, succeed_on=2)
        self.dispatch("slide_01")  # generation 1: fails
        self.retry("slide_01")
        self.dispatch("slide_01")  # generation 2: succeeds
        self.assertEqual(self.state.consecutive_failure_streak("slide_01"), 0)

        # A fresh failure after a success starts a brand-new streak of 1, not 2.
        self.qa_fail("slide_01")
        self.retry("slide_01")
        self.worker.set_plan("slide_01", fault=FAULT_GENERATION_FAILED, succeed_on=4)
        self.dispatch("slide_01", operation="regenerate")  # generation 3: fails again
        self.assertEqual(self.state.consecutive_failure_streak("slide_01"), 1)
        self.assertTrue(self.state.may_retry_immediately("slide_01"))

    # -- 3. second consecutive failure blocks the project -------------------
    def test_second_consecutive_failure_blocks_project(self):
        self.worker.set_plan("slide_01", fault=FAULT_GENERATION_FAILED)  # never succeeds

        self.dispatch("slide_01")  # generation 1: fails
        self.assertTrue(self.state.may_retry_immediately("slide_01"))
        self.retry("slide_01")

        outcome = self.dispatch("slide_01")  # generation 2: fails again (consecutive)
        self.assertEqual(outcome.error_code, ERROR_IMAGE_GENERATION_FAILED)
        self.assertEqual(self.state.consecutive_failure_streak("slide_01"), 2)
        self.assertFalse(self.state.may_retry_immediately("slide_01"))

        self.state.block_after_repeated_failure("slide_01")
        self.state.save()

        slide = self.assert_slide("slide_01", SLIDE_BLOCKED, generation=2, attempts=2)
        self.assertEqual(
            slide["blocker"],
            {
                "reason": "repeated_image_backend_failure",
                "error_code": ERROR_IMAGE_GENERATION_FAILED,
                "retry_immediately": False,
                "at": slide["blocker"]["at"],
            },
        )
        self.assertEqual(self.state.phase, PHASE_BLOCKED)
        self.assertEqual(self.state.data["phase_before_block"], PHASE_SLIDE_GENERATION)

    # -- 4. no third immediate Codex dispatch after the second failure ------
    def test_no_third_dispatch_after_second_failure(self):
        self.worker.set_plan("slide_01", fault=FAULT_GENERATION_FAILED)
        self.dispatch("slide_01")
        self.retry("slide_01")
        self.dispatch("slide_01")
        self.state.block_after_repeated_failure("slide_01")
        self.state.save()

        calls_before = self.worker.call_count
        # Blocking the slide is a per-slide resume-capable state, but the
        # *project* stays blocked, so a resume planner must not offer it (or
        # anything else) for immediate dispatch until AGY explicitly resumes
        # the project itself.
        self.assertEqual(self.state.phase, PHASE_BLOCKED)
        self.assertEqual(plan_dispatch(self.state), [])
        self.assertEqual(self.worker.call_count, calls_before, "no extra render turn was spent")
        self.assert_slide("slide_01", SLIDE_BLOCKED, attempts=2)

    # -- 5. no later slide is dispatched once the project is blocked --------
    def test_no_later_slide_dispatch_once_blocked(self):
        self.worker.set_plan("slide_01", fault=FAULT_GENERATION_FAILED)
        self.dispatch("slide_01")
        self.retry("slide_01")
        self.dispatch("slide_01")
        self.state.block_after_repeated_failure("slide_01")
        self.state.save()

        self.assertEqual(plan_dispatch(self.state), [], "a blocked project must dispatch nothing")
        for slide_id in ("slide_02", "slide_03", "slide_04", "slide_05"):
            self.assert_slide(slide_id, SLIDE_PLANNED)
        self.assertEqual(self.worker.calls_for("slide_02"), [])

    # -- 9. unrelated slide failures are not the same consecutive streak ----
    def test_unrelated_slide_failures_do_not_share_a_streak(self):
        self.worker.set_plan("slide_02", fault=FAULT_GENERATION_FAILED, succeed_on=2)
        self.worker.set_plan("slide_05", fault=FAULT_GENERATION_FAILED, succeed_on=2)

        self.dispatch("slide_02")  # slide_02 generation 1 fails
        self.retry("slide_02")
        self.dispatch("slide_02")  # slide_02 generation 2 succeeds
        self.assertEqual(self.state.consecutive_failure_streak("slide_02"), 0)

        self.dispatch("slide_05")  # slide_05 generation 1 fails, unrelated to slide_02
        self.assertEqual(self.state.consecutive_failure_streak("slide_05"), 1)
        self.assertEqual(self.state.consecutive_failure_streak("slide_02"), 0)
        self.assertTrue(self.state.may_retry_immediately("slide_05"))
        # slide_05's single failure must never be seen as slide_02's second.
        self.assertNotEqual(
            self.state.consecutive_failure_streak("slide_05"),
            2,
            "one failure on an unrelated slide must not look like a second consecutive failure",
        )

    # -- 6/7. resume: settled slides skipped, blocked slide gets next gen ---
    def test_resume_skips_settled_and_advances_the_blocked_slide(self):
        self.worker.set_plan("slide_01", fault=FAULT_GENERATION_FAILED)

        # slide_02 finishes normally before the block happens.
        self.dispatch("slide_02")
        self.qa_pass("slide_02")
        digest_02_before = self.image_digests()["origin_image/slide_02.png"]

        self.dispatch("slide_01")
        self.retry("slide_01")
        self.dispatch("slide_01")
        self.state.block_after_repeated_failure("slide_01")
        self.state.save()

        # A brand-new load, exactly like a resumed process.
        self.reload()
        self.assertEqual(self.state.phase, PHASE_BLOCKED)

        # AGY explicitly resumes the project and the blocked slide.
        self.state.set_phase(PHASE_SLIDE_GENERATION)
        self.state.set_slide_status("slide_01", SLIDE_READY)
        self.state.save()

        # qa_passed slide is never re-dispatched by resume planning.
        dispatchable = plan_dispatch(self.state)
        self.assertNotIn("slide_02", dispatchable)
        self.assertIn("slide_01", dispatchable)

        # slide_02's completed worker result / image is not replayed or rewritten.
        self.assert_slide("slide_02", SLIDE_QA_PASSED, generation=1, attempts=1)
        self.assertEqual(self.image_digests()["origin_image/slide_02.png"], digest_02_before)
        self.assertEqual(len(self.worker.calls_for("slide_02")), 1, "slide_02 must not be regenerated on resume")

        # slide_01 (the affected slide) resumes into a normal next generation.
        self.worker.set_plan("slide_01", fault="success")
        outcome = self.dispatch("slide_01", operation="regenerate")
        self.assertEqual(outcome.status, "completed")
        slide_01 = self.assert_slide("slide_01", SLIDE_GENERATED, generation=3, attempts=3)
        # All prior attempt history (both failures) is preserved, not discarded.
        self.assertEqual(
            [a["error_code"] for a in slide_01["attempts"][:2]],
            [ERROR_IMAGE_GENERATION_FAILED, ERROR_IMAGE_GENERATION_FAILED],
        )
        self.assertEqual(slide_01["attempts"][2]["status"], "completed")

    # -- 10. operator-confirmed quota never rewrites the worker error_code --
    def test_operator_confirmed_quota_does_not_rewrite_worker_error_code(self):
        self.worker.set_plan("slide_01", fault=FAULT_GENERATION_FAILED)
        outcome = self.dispatch("slide_01")
        self.assertEqual(outcome.error_code, ERROR_IMAGE_GENERATION_FAILED)

        # Operator/AGY externally confirms quota exhaustion (not derivable from
        # the subprocess evidence itself) and records that as its own decision.
        self.state.block_for_operator_confirmed_quota(
            note="operator confirmed subscription quota exhaustion via ChatGPT billing UI"
        )
        self.state.save()

        # The worker-reported evidence on the slide is untouched: it is the
        # frozen recorder's own "codex generation failed" blocker (set by
        # record_worker_result on any error), never rewritten to a quota
        # reason by this operator-level decision.
        slide = self.state.slide("slide_01")
        self.assertEqual(slide["attempts"][0]["error_code"], ERROR_IMAGE_GENERATION_FAILED)
        self.assertEqual(slide["status"], SLIDE_GENERATION_FAILED)
        self.assertEqual(slide["blocker"]["error_code"], ERROR_IMAGE_GENERATION_FAILED)
        self.assertNotEqual(slide["blocker"]["reason"], "subscription_quota_exhausted")

        # The operator decision lives in a separate, clearly named project field.
        operator_blocker = self.state.data["operator_blocker"]
        self.assertEqual(operator_blocker["reason"], "subscription_quota_exhausted")
        self.assertEqual(operator_blocker["confirmed_by"], "operator")
        self.assertEqual(self.state.phase, PHASE_BLOCKED)
        self.assertEqual(self.state.data["phase_before_block"], PHASE_SLIDE_GENERATION)

        # Reload proves this provenance separation survives a restart too.
        self.reload()
        self.assertEqual(
            self.state.slide("slide_01")["attempts"][0]["error_code"],
            ERROR_IMAGE_GENERATION_FAILED,
        )
        self.assertEqual(
            self.state.data["operator_blocker"]["reason"], "subscription_quota_exhausted"
        )


class InvocationLedgerReportingTests(RecoveryTestCase):
    """11. Codex invocation counts must come from actual invocation evidence."""

    slide_ids = ("slide_01", "slide_02")

    def setUp(self) -> None:
        super().setUp()
        self.advance_to_slide_generation()

    def test_invocation_count_matches_actual_worker_calls_not_slide_count(self):
        self.worker.set_plan("slide_01", fault=FAULT_GENERATION_FAILED, succeed_on=2)

        # slide_01 takes two real render turns (fail, then retry-success);
        # slide_02 takes one. A page-count guess would say "2 slides -> 2
        # invocations", which is wrong: the real evidence is 3.
        self.dispatch("slide_01")
        self.retry("slide_01")
        self.dispatch("slide_01")
        self.dispatch("slide_02")

        self.assertEqual(self.worker.call_count, 3, "invocation count must come from evidence")
        self.assertNotEqual(
            self.worker.call_count,
            len(self.slide_ids),
            "invocation count must not be inferred from slide/page count",
        )
        self.assertEqual(len(self.worker.calls_for("slide_01")), 2)
        self.assertEqual(len(self.worker.calls_for("slide_02")), 1)

    def test_probe_style_calls_are_counted_only_when_a_process_actually_started(self):
        # A plan/dispatch decision that never reaches the worker (e.g. a
        # settled slide skipped by resume) must add zero to the count.
        self.dispatch("slide_01")
        self.qa_pass("slide_01")
        calls_before = self.worker.call_count

        dispatchable = plan_dispatch(self.state)
        self.assertNotIn("slide_01", dispatchable)
        self.assertEqual(
            self.worker.call_count,
            calls_before,
            "planning a resume must not itself count as an invocation",
        )

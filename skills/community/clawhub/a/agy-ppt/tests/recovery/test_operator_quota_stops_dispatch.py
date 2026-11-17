#!/usr/bin/env python3
"""Phase 10.3 audit -- operator-confirmed quota must actually stop dispatch.

Read-only/minimal-verification scenario. It asks one question:

    Does ``ProjectState.block_for_operator_confirmed_quota()`` really move the
    *project* to ``blocked`` (so ``plan_dispatch()`` returns nothing and no
    further slide can be dispatched), or does it only write
    ``operator_blocker`` metadata while ``phase`` stays ``slide_generation``?

Scenario: slide_01 is already ``qa_passed``, slide_02's most recent worker
result is a real ``IMAGE_GENERATION_FAILED``, slide_03 is still ``planned``.
An operator then confirms -- through an external channel, never inferred from
the worker's returncode/error_code -- that the subscription quota is
exhausted, and AGY records that via ``block_for_operator_confirmed_quota()``.

No real Codex/Kiro process is launched and no subscription quota is consumed;
the worker failure is injected deterministically via ``FakeImageWorker``.
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
    PHASE_BLOCKED,
    PHASE_SLIDE_GENERATION,
    SLIDE_GENERATION_FAILED,
    SLIDE_PLANNED,
    SLIDE_QA_PASSED,
    SLIDE_READY,
)

from helpers.fake_image_worker import FAULT_GENERATION_FAILED  # noqa: E402
from helpers.recovery_deck import RecoveryTestCase, plan_dispatch  # noqa: E402

SLIDES = ("slide_01", "slide_02", "slide_03")


class OperatorConfirmedQuotaStopsDispatchTests(RecoveryTestCase):
    slide_ids = SLIDES

    def setUp(self) -> None:
        super().setUp()
        self.advance_to_slide_generation()

        # slide_01: already settled.
        self.dispatch("slide_01")
        self.qa_pass("slide_01")

        # slide_02: most recent worker result is a real IMAGE_GENERATION_FAILED.
        self.worker.set_plan("slide_02", fault=FAULT_GENERATION_FAILED)
        self.outcome_02 = self.dispatch("slide_02")
        self.assertEqual(self.outcome_02.error_code, "IMAGE_GENERATION_FAILED")
        self.assert_slide("slide_02", SLIDE_GENERATION_FAILED, generation=1, attempts=1)

        # slide_03: never touched.
        self.assert_slide("slide_03", SLIDE_PLANNED)

        self.calls_before_block = self.worker.call_count

    # -- 1/2/3/4/9: the block itself ---------------------------------------
    def test_operator_blocker_reason_is_recorded(self):
        self.state.block_for_operator_confirmed_quota(
            note="operator confirmed subscription quota exhaustion via ChatGPT billing UI"
        )
        self.state.save()
        self.assertEqual(
            self.state.data["operator_blocker"]["reason"], "subscription_quota_exhausted"
        )

    def test_worker_error_code_is_not_rewritten(self):
        self.state.block_for_operator_confirmed_quota(note="quota confirmed externally")
        self.state.save()

        slide = self.state.slide("slide_02")
        self.assertEqual(slide["attempts"][0]["error_code"], "IMAGE_GENERATION_FAILED")
        self.assertEqual(slide["blocker"]["error_code"], "IMAGE_GENERATION_FAILED")
        self.assertNotEqual(slide["blocker"]["reason"], "subscription_quota_exhausted")
        self.assertNotIn("SUBSCRIPTION_QUOTA_EXHAUSTED", str(slide["attempts"][0]))

    def test_project_phase_becomes_blocked(self):
        self.assertEqual(self.state.phase, PHASE_SLIDE_GENERATION, "sanity: not blocked yet")
        self.state.block_for_operator_confirmed_quota(note="quota confirmed externally")
        self.state.save()
        self.assertEqual(self.state.phase, PHASE_BLOCKED)

    def test_phase_before_block_is_slide_generation(self):
        self.state.block_for_operator_confirmed_quota(note="quota confirmed externally")
        self.state.save()
        self.assertEqual(self.state.data["phase_before_block"], PHASE_SLIDE_GENERATION)

    # -- 5/6/7: dispatch must actually stop ---------------------------------
    def test_plan_dispatch_is_empty_after_the_block(self):
        self.state.block_for_operator_confirmed_quota(note="quota confirmed externally")
        self.state.save()
        self.assertEqual(plan_dispatch(self.state), [])

    def test_slide_02_is_not_immediately_redispatched(self):
        self.state.block_for_operator_confirmed_quota(note="quota confirmed externally")
        self.state.save()

        # AGY's normal retry move (generation_failed -> ready) is still legal at
        # the slide level (mirrors block_after_repeated_failure's own slide/
        # project split), but the *project* being blocked means no dispatch
        # planner offers it, and no worker call happens.
        self.assertNotIn("slide_02", plan_dispatch(self.state))
        self.assertEqual(self.worker.call_count, self.calls_before_block)

    def test_slide_03_is_not_dispatched(self):
        self.state.block_for_operator_confirmed_quota(note="quota confirmed externally")
        self.state.save()
        self.assertNotIn("slide_03", plan_dispatch(self.state))
        self.assertEqual(self.worker.calls_for("slide_03"), [])
        self.assert_slide("slide_03", SLIDE_PLANNED)

    # -- 8: slide_01 stays settled -------------------------------------------
    def test_slide_01_remains_qa_passed(self):
        self.state.block_for_operator_confirmed_quota(note="quota confirmed externally")
        self.state.save()
        self.assert_slide("slide_01", SLIDE_QA_PASSED, generation=1, attempts=1)

    # -- reload proves this is real persisted state, not in-memory only -----
    def test_block_survives_a_reload(self):
        self.state.block_for_operator_confirmed_quota(note="quota confirmed externally")
        self.state.save()
        self.reload()

        self.assertEqual(self.state.phase, PHASE_BLOCKED)
        self.assertEqual(self.state.data["phase_before_block"], PHASE_SLIDE_GENERATION)
        self.assertEqual(plan_dispatch(self.state), [])
        self.assertEqual(
            self.state.data["operator_blocker"]["reason"], "subscription_quota_exhausted"
        )
        self.assertEqual(
            self.state.slide("slide_02")["attempts"][0]["error_code"], "IMAGE_GENERATION_FAILED"
        )


class OperatorConfirmedQuotaResumeTests(RecoveryTestCase):
    """Resume after a simulated quota recovery: blocked -> slide_generation."""

    slide_ids = SLIDES

    def setUp(self) -> None:
        super().setUp()
        self.advance_to_slide_generation()

        self.digest_before = None
        self.dispatch("slide_01")
        self.qa_pass("slide_01")
        self.digest_before = self.image_digests()["origin_image/slide_01.png"]

        self.worker.set_plan("slide_02", fault=FAULT_GENERATION_FAILED)
        self.dispatch("slide_02")

        self.state.block_for_operator_confirmed_quota(
            note="operator confirmed subscription quota exhaustion"
        )
        self.state.save()
        self.reload()  # a brand-new load, exactly like a resumed process

    def _resume(self) -> None:
        """AGY explicitly resumes: clears the operator block and the phase."""
        self.state.data["operator_blocker"] = None
        self.state.set_phase(PHASE_SLIDE_GENERATION)
        self.state.set_slide_status("slide_02", SLIDE_READY)
        self.state.save()

    def test_resume_clears_the_operator_blocker_and_restores_the_phase(self):
        self._resume()
        self.assertIsNone(self.state.data["operator_blocker"])
        self.assertEqual(self.state.phase, PHASE_SLIDE_GENERATION)

    def test_resume_skips_slide_01(self):
        self._resume()
        self.assertNotIn("slide_01", plan_dispatch(self.state))
        self.assert_slide("slide_01", SLIDE_QA_PASSED, generation=1, attempts=1)
        self.assertEqual(
            self.image_digests()["origin_image/slide_01.png"],
            self.digest_before,
            "slide_01 must not be regenerated on resume",
        )
        self.assertEqual(len(self.worker.calls_for("slide_01")), 1)

    def test_resume_offers_slide_02_for_generation(self):
        self._resume()
        self.assertIn("slide_02", plan_dispatch(self.state))
        self.worker.set_plan("slide_02", fault="success")
        outcome = self.dispatch("slide_02")
        self.assertEqual(outcome.status, "completed")
        self.assert_slide("slide_02", "generated", generation=2, attempts=2)
        # Prior failure evidence (the real worker error_code) is preserved.
        self.assertEqual(
            self.state.slide("slide_02")["attempts"][0]["error_code"],
            "IMAGE_GENERATION_FAILED",
        )

    def test_slide_03_waits_for_slide_02_to_settle(self):
        self._resume()
        # Immediately after resume, before slide_02 is settled, slide_03 is
        # still offered by the planner (sequential_only is enforced by AGY's
        # own one-at-a-time dispatch discipline, not by plan_dispatch itself),
        # but no worker call is made for it until slide_02 is actually settled.
        self.worker.set_plan("slide_02", fault="success")
        self.dispatch("slide_02")
        self.qa_pass("slide_02")

        self.assertIn("slide_03", plan_dispatch(self.state))
        outcome = self.dispatch("slide_03")
        self.assertEqual(outcome.status, "completed")
        self.assertEqual(len(self.worker.calls_for("slide_03")), 1)

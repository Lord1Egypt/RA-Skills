#!/usr/bin/env python3
"""Phase 9B LIVE regeneration state test (opt-in, quota-consuming).

    AGY_PPT_LIVE_RECOVERY=1 python3 \
        skills/agy-ppt/tests/integration/test_phase9_live_regenerate.py

Sequence driven by the test controller (never by the worker):

1. real Codex generation -> ``generated`` (generation 1)
2. the controller explicitly judges it ``qa_failed`` with the fixed reason
   ``Phase 9B regeneration state test``
3. ``qa_failed`` -> ``ready``
4. real Codex **regeneration** -> ``generated`` (generation 2)
5. the controller judges it ``qa_passed``

Proven afterwards, from the reloaded on-disk state and the invocation ledger:

    generation == 2
    attempts == 2 (attempt 1 metadata still intact, distinct idempotency keys)
    real Codex invocations == 2 (generation 1 and 2, no duplicates)
    the final image really exists and is readable
    backend == codex_builtin_imagegen
    api_fallback_used == false

Cost: exactly 2 real render turns. No API key is used, no OpenAI Images API is
called, and the only writable location is
``<repo>/.agy-ppt-integration/phase9b-regenerate/``, removed in teardown.
"""

from __future__ import annotations

import copy
import sys
import unittest
from pathlib import Path

TESTS_DIR = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = TESTS_DIR.parent / "scripts"
for _path in (str(TESTS_DIR), str(SCRIPTS_DIR)):
    if _path not in sys.path:
        sys.path.insert(0, _path)

from codex_image_adapter import BACKEND, OP_GENERATE, OP_REGENERATE  # noqa: E402
from helpers import live_recovery as lr  # noqa: E402
from project_state import (  # noqa: E402
    SLIDE_GENERATED,
    SLIDE_QA_FAILED,
    SLIDE_QA_PASSED,
    SLIDE_READY,
    ProjectState,
)

SCENARIO = "phase9b-regenerate"
PROJECT_ID = "ppt_live_phase9b_regenerate"
SLIDE_ID = "slide_01"
ROLE = "controller"

# The QA rationale is fixed so the scenario stays deterministic and so it is
# obvious that this is a state test, not a judgement about deck content.
QA_FAILED_REASON = "Phase 9B regeneration state test"

WORK_DIR = lr.work_root(SCENARIO)
WORKSPACE = WORK_DIR / "deck"


@unittest.skipUnless(lr.live_enabled(__file__), lr.SKIP_REASON)
@unittest.skipUnless(lr.codex_present(), "codex is not on PATH")
class Phase9BLiveRegenerationTests(unittest.TestCase):
    """One slide, two real Codex turns, one explicit AGY QA rejection."""

    ledger: lr.InvocationLedger
    state: ProjectState
    attempt_one: dict
    result_one: dict
    result_two: dict

    @classmethod
    def setUpClass(cls) -> None:
        lr.reset_dir(WORK_DIR)
        # Registered before anything can fail, so an aborted setUpClass still
        # cleans the workspace up.
        cls.addClassCleanup(lr.cleanup, WORK_DIR)
        WORKSPACE.mkdir(parents=True, exist_ok=True)
        cls.ledger = lr.InvocationLedger.for_scenario(SCENARIO, WORK_DIR)

        state = lr.new_project(WORKSPACE, PROJECT_ID, (SLIDE_ID,))
        try:
            # 1. generation 1
            cls.result_one = lr.live_generate(
                state, cls.ledger, SLIDE_ID, marker="P9B REGEN 1", role=ROLE
            )
            assert state.slide(SLIDE_ID)["status"] == SLIDE_GENERATED
            cls.attempt_one = copy.deepcopy(state.slide(SLIDE_ID)["attempts"][0])

            # 2. the controller -- never the worker -- rejects it.
            lr.qa_fail(state, SLIDE_ID, reason=QA_FAILED_REASON)
            assert state.slide(SLIDE_ID)["status"] == SLIDE_QA_FAILED

            # 3. back to ready, then 4. a real regeneration from the reloaded state.
            state.set_slide_status(SLIDE_ID, SLIDE_READY)
            state.save()
            state = ProjectState.load(WORKSPACE)
            assert state.slide(SLIDE_ID)["status"] == SLIDE_READY

            cls.result_two = lr.live_generate(
                state,
                cls.ledger,
                SLIDE_ID,
                marker="P9B REGEN 2",
                role=ROLE,
                operation=OP_REGENERATE,
            )

            # 5. accepted this time.
            lr.qa_pass(state, SLIDE_ID, reason="Phase 9B regeneration accepted")
        except lr.LiveRuntimeBlocker as exc:
            raise unittest.SkipTest(str(exc)) from exc

        cls.state = ProjectState.load(WORKSPACE)

    # -- counters ----------------------------------------------------------
    def test_generation_is_two(self):
        self.assertEqual(self.state.slide(SLIDE_ID)["generation"], 2)

    def test_attempts_is_two(self):
        attempts = self.state.slide(SLIDE_ID)["attempts"]
        self.assertEqual(len(attempts), 2)
        self.assertEqual([a["generation"] for a in attempts], [1, 2])

    def test_two_real_codex_invocations_one_per_generation(self):
        self.assertEqual(self.ledger.count_for(SLIDE_ID), 2)
        self.assertEqual(self.ledger.generations_for(SLIDE_ID), [1, 2])
        self.assertEqual(self.ledger.total(), 2)

    def test_no_duplicate_invocation(self):
        self.assertEqual(self.ledger.duplicate_count(), 0)

    def test_first_turn_generated_and_second_turn_regenerated(self):
        self.assertEqual(self.result_one["operation"], OP_GENERATE)
        self.assertEqual(self.result_two["operation"], OP_REGENERATE)
        operations = [r["operation"] for r in self.ledger.invocations()]
        self.assertEqual(operations, [OP_GENERATE, OP_REGENERATE])

    # -- attempt history ---------------------------------------------------
    def test_both_attempt_records_are_preserved(self):
        attempts = self.state.slide(SLIDE_ID)["attempts"]
        self.assertEqual(
            attempts[0], self.attempt_one, "attempt 1 must survive regeneration unchanged"
        )
        self.assertNotEqual(attempts[0]["idempotency_key"], attempts[1]["idempotency_key"])
        self.assertEqual(attempts[1]["generation"], 2)
        for attempt in attempts:
            self.assertEqual(attempt["status"], "completed")
            self.assertEqual(attempt["worker"], "codex")
            self.assertEqual(attempt["backend"], BACKEND)

    def test_qa_failed_reason_is_the_fixed_state_test_reason(self):
        decisions = lr.qa_decisions(WORKSPACE)
        rejections = [d for d in decisions if d["verdict"] == SLIDE_QA_FAILED]
        self.assertEqual(len(rejections), 1)
        self.assertEqual(rejections[0]["reason"], QA_FAILED_REASON)
        self.assertEqual(rejections[0]["decided_by"], "agy")
        self.assertEqual(rejections[0]["generation"], 1)

    # -- final artifact ----------------------------------------------------
    def test_final_status_is_qa_passed(self):
        self.assertEqual(self.state.slide(SLIDE_ID)["status"], SLIDE_QA_PASSED)

    def test_final_image_exists_and_is_readable(self):
        image_path = self.state.slide(SLIDE_ID)["image_path"]
        self.assertIsNotNone(image_path)
        resolved = WORKSPACE / image_path
        self.assertTrue(resolved.is_file(), resolved)
        self.assertGreater(resolved.stat().st_size, 0)
        self.assertTrue(lr.is_readable_image(resolved), f"not a readable image: {resolved}")

    # -- backend hygiene ---------------------------------------------------
    def test_backend_is_codex_builtin_imagegen(self):
        self.assertEqual(self.result_one["backend"], BACKEND)
        self.assertEqual(self.result_two["backend"], BACKEND)
        for record in self.ledger.results():
            self.assertEqual(record["backend"], BACKEND)

    def test_api_fallback_was_never_used(self):
        for result in (self.result_one, self.result_two):
            self.assertFalse(result["diagnostics"]["api_fallback_used"])
        self.assertEqual(self.ledger.api_fallback_count(), 0)

    def test_no_credential_env_reached_the_worker(self):
        for result in (self.result_one, self.result_two):
            self.assertEqual(result["diagnostics"]["auth"], "chatgpt_cli_session")


def main(argv: list[str] | None = None) -> int:
    parser = lr.role_parser(__doc__ or "")
    args = parser.parse_args(argv)
    if args.role:
        print(f"{Path(__file__).name} has no child roles", file=sys.stderr)
        return 2
    if not lr.live_enabled(__file__):
        print(lr.SKIP_REASON)
        return 0
    if not lr.codex_present():
        print("codex is not on PATH")
        return 1
    suite = unittest.TestLoader().loadTestsFromTestCase(Phase9BLiveRegenerationTests)
    return 0 if unittest.TextTestRunner(verbosity=2).run(suite).wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())

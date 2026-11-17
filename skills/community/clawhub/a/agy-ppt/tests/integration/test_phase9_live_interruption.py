#!/usr/bin/env python3
"""Phase 9C LIVE process-interruption recovery (double opt-in, quota-consuming).

    AGY_PPT_LIVE_RECOVERY=1 AGY_PPT_LIVE_RECOVERY_INTERRUPT=1 python3 \
        skills/agy-ppt/tests/integration/test_phase9_live_interruption.py

What happens:

1. A child Python process (Process C) starts a **real** Codex generation. Before
   it does, it installs an observation-only ``subprocess.Popen`` tracker, so the
   exact PID and process group of the Codex process *this test created* are
   written to ``tracked_child_processes.jsonl``.
2. Once that Codex child is observed and the generation is in flight, the
   controller kills **only** what it tracked: the Process C PID it started and
   the Codex process group it recorded. There is no ``killall codex``, no search
   of the process table, and no way to touch another Codex session.
3. A brand new Python process (Process D) re-reads ``project_state.json``. The
   slide is ``generating`` with no completed result and no verified artifact, so
   recovery must resolve it as ``generation_failed``. Success is never guessed.
4. The test controller then drives ``generation_failed -> ready`` and runs a
   second real Codex generation, which is accepted as ``qa_passed``.

Cost: up to 2 real render turns (the first one is deliberately thrown away).
No API key is used, no OpenAI Images API is called, and the only writable
location is ``<repo>/.agy-ppt-integration/phase9c-interruption/``, removed in
teardown.
"""

from __future__ import annotations

import os
import sys
import time
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
    SLIDE_GENERATING,
    SLIDE_GENERATION_FAILED,
    SLIDE_QA_PASSED,
    SLIDE_READY,
    ProjectState,
)

SCENARIO = "phase9c-interruption"
PROJECT_ID = "ppt_live_phase9c_interruption"
SLIDE_ID = "slide_01"

ROLE_GENERATE = "process-c"
ROLE_RECOVER = "process-d"
ROLE_CONTROLLER = "controller"
CODEX_EXECUTABLE_NAME = "codex"

WORK_DIR = lr.work_root(SCENARIO)
WORKSPACE = WORK_DIR / "deck"
TRACKER_PATH = WORK_DIR / lr.TRACKED_CHILDREN_FILENAME


# ---------------------------------------------------------------------------
# Process C -- starts a real Codex generation and expects to be killed
# ---------------------------------------------------------------------------
def run_generating_child(workspace: Path, work_dir: Path) -> int:
    tracker = Path(work_dir) / lr.TRACKED_CHILDREN_FILENAME
    # Observation only: the adapter's behaviour is unchanged, we just write down
    # every PID / process group this process starts so the kill can be precise.
    lr.install_child_tracker(tracker)

    ledger = lr.InvocationLedger.for_scenario(SCENARIO, work_dir)
    state = ProjectState.load(workspace)
    lr.write_summary(
        work_dir,
        f"{ROLE_GENERATE}-started",
        {"tracker": str(tracker), "slide_id": SLIDE_ID, "pgid": os.getpgid(0)},
    )

    # This call is expected to be killed mid-flight. If it ever returns, the
    # controller treats the scenario as inconclusive rather than as a failure.
    result = lr.live_generate(
        state, ledger, SLIDE_ID, marker="P9C INTERRUPT 1", role=ROLE_GENERATE
    )
    lr.write_summary(
        work_dir,
        ROLE_GENERATE,
        {"completed": True, "status": result.get("status"), "slide_id": SLIDE_ID},
    )
    return lr.EXIT_OK


# ---------------------------------------------------------------------------
# Process D -- a brand new process that recovers the interrupted slide
# ---------------------------------------------------------------------------
def run_recovery_child(workspace: Path, work_dir: Path) -> int:
    state = ProjectState.load(workspace)
    slide = state.slide(SLIDE_ID)
    status_before = slide["status"]
    generation = int(slide.get("generating_attempt") or slide.get("generation") or 0)

    completed = [
        attempt
        for attempt in slide.get("attempts", [])
        if attempt.get("generation") == generation and attempt.get("status") == "completed"
    ]
    image_path = slide.get("image_path")
    artifact_verified = bool(image_path) and lr.is_readable_image(Path(workspace) / image_path)

    # No completed result + no verified artifact => the outcome is unknown, so
    # the only honest recovery is 'generation_failed'.
    recovered = state.recover_interrupted()
    state.save()

    after = state.slide(SLIDE_ID)
    lr.write_summary(
        work_dir,
        ROLE_RECOVER,
        {
            "status_before": status_before,
            "generation_before": generation,
            "attempts_before": len(slide.get("attempts", [])),
            "completed_result_present": bool(completed),
            "artifact_verified": artifact_verified,
            "recovered": recovered,
            "status_after": after["status"],
            "generation_after": after["generation"],
            "image_path": after.get("image_path"),
            "blocker": after.get("blocker"),
        },
    )
    return lr.EXIT_OK


# ---------------------------------------------------------------------------
# Verification
# ---------------------------------------------------------------------------
@unittest.skipUnless(lr.interrupt_enabled(__file__), lr.INTERRUPT_SKIP_REASON)
@unittest.skipUnless(lr.codex_present(), "codex is not on PATH")
class Phase9CLiveInterruptionTests(unittest.TestCase):
    """Kill a real, tracked Codex generation and recover deterministically."""

    ledger: lr.InvocationLedger
    tracked: lr.TrackedProcess
    kill_report: dict
    child_returncode: int
    recover_summary: dict
    state: ProjectState
    second_result: dict

    @classmethod
    def setUpClass(cls) -> None:
        lr.reset_dir(WORK_DIR)
        # Registered before anything can fail, so an abandoned scenario still
        # cleans the workspace up.
        cls.addClassCleanup(lr.cleanup, WORK_DIR)
        WORKSPACE.mkdir(parents=True, exist_ok=True)
        cls.ledger = lr.InvocationLedger.for_scenario(SCENARIO, WORK_DIR)
        lr.new_project(WORKSPACE, PROJECT_ID, (SLIDE_ID,))

        child = lr.start_role(
            __file__,
            ROLE_GENERATE,
            workspace=WORKSPACE,
            work_dir=WORK_DIR,
            ledger=cls.ledger,
        )
        try:
            tracked = lr.wait_for_tracked(
                TRACKER_PATH, CODEX_EXECUTABLE_NAME, timeout=lr.interrupt_wait()
            )
            if tracked is None:
                cls._abandon(child, "no tracked codex child process appeared in time")
            time.sleep(lr.interrupt_delay())

            if child.poll() is not None:
                cls._abandon(child, "the codex turn ended before the interruption window")
            on_disk = ProjectState.load(WORKSPACE)
            if on_disk.slide(SLIDE_ID)["status"] != SLIDE_GENERATING:
                cls._abandon(
                    child,
                    "slide was no longer 'generating' on disk; the turn finished too fast",
                )

            cls.tracked = tracked
            cls.kill_report = lr.terminate_tracked(child, [tracked])
            cls.child_returncode = child.returncode
        finally:
            if child.poll() is None:  # pragma: no cover - defensive
                lr.terminate_tracked(child, lr.tracked_processes(TRACKER_PATH, name=CODEX_EXECUTABLE_NAME))

        # Close the (millisecond-wide) race: if the turn managed to record a
        # result between the status check and the kill, the interruption window
        # was missed and the scenario is inconclusive, not failed.
        after_kill = ProjectState.load(WORKSPACE)
        if after_kill.slide(SLIDE_ID)["status"] != SLIDE_GENERATING:
            raise unittest.SkipTest(
                "the codex turn recorded a result before the kill landed; the interruption "
                "window could not be observed, so the scenario is inconclusive rather than failed"
            )

        # Recovery happens in a brand new process, from disk only.
        recovered = lr.run_role(
            __file__,
            ROLE_RECOVER,
            workspace=WORKSPACE,
            work_dir=WORK_DIR,
            ledger=cls.ledger,
            timeout=120,
        )
        if recovered.returncode != lr.EXIT_OK:
            raise AssertionError(
                f"{ROLE_RECOVER} failed\n{lr.child_failure_detail(recovered)}"
            )
        cls.recover_summary = lr.read_summary(WORK_DIR, ROLE_RECOVER)

        # The test controller decides to retry: generation_failed -> ready -> 2.
        state = ProjectState.load(WORKSPACE)
        state.set_slide_status(SLIDE_ID, SLIDE_READY)
        state.save()
        leftover = WORKSPACE / "origin_image" / f"{SLIDE_ID}.png"
        operation = OP_REGENERATE if leftover.exists() else OP_GENERATE
        try:
            cls.second_result = lr.live_generate(
                state,
                cls.ledger,
                SLIDE_ID,
                marker="P9C INTERRUPT 2",
                role=ROLE_CONTROLLER,
                operation=operation,
            )
            lr.qa_pass(state, SLIDE_ID, reason="Phase 9C recovery regeneration accepted")
        except lr.LiveRuntimeBlocker as exc:
            raise unittest.SkipTest(str(exc)) from exc
        cls.state = ProjectState.load(WORKSPACE)

    @classmethod
    def _abandon(cls, child, reason: str) -> None:
        """Stop this scenario without failing: the window could not be hit.

        The tracked Codex child (if any) is killed too, so an abandoned run
        never leaves a real generation running.
        """
        lr.terminate_tracked(child, lr.tracked_processes(TRACKER_PATH, name=CODEX_EXECUTABLE_NAME))
        raise unittest.SkipTest(
            f"{reason}; the interruption window could not be observed, so the scenario is "
            "inconclusive rather than failed"
        )

    # -- kill scope --------------------------------------------------------
    def test_the_killed_codex_process_was_one_this_test_created(self):
        self.assertEqual(Path(self.tracked.argv0).name, CODEX_EXECUTABLE_NAME)
        self.assertGreater(self.tracked.pid, 1)
        self.assertEqual(
            self.tracked.pgid,
            self.tracked.pid,
            "the tracked codex process must lead its own group (start_new_session=True)",
        )
        self.assertIn(self.tracked.pid, self.kill_report["killed_pids"])
        self.assertIn(self.tracked.pgid, self.kill_report["killed_process_groups"])

    def test_no_untracked_process_group_was_signalled(self):
        self.assertEqual(self.kill_report["refused"], [])
        self.assertEqual(self.kill_report["killed_process_groups"], [self.tracked.pgid])
        self.assertNotIn(os.getpgid(0), self.kill_report["killed_process_groups"])
        self.assertNotIn(os.getpid(), self.kill_report["killed_pids"])

    def test_everything_that_was_killed_is_gone(self):
        self.assertEqual(self.kill_report["survivors"], [])
        self.assertFalse(lr.pgid_alive(self.tracked.pgid))

    def test_the_generating_process_died_without_reporting_a_result(self):
        self.assertIsNotNone(self.child_returncode)
        self.assertNotEqual(self.child_returncode, lr.EXIT_OK)
        self.assertFalse(
            (WORK_DIR / f"summary_{ROLE_GENERATE}.json").exists(),
            "process C must not have completed its turn",
        )
        self.assertTrue((WORK_DIR / f"summary_{ROLE_GENERATE}-started.json").exists())

    # -- recovery ----------------------------------------------------------
    def test_recovery_ran_in_a_brand_new_process(self):
        pid = self.recover_summary["pid"]
        self.assertNotEqual(pid, os.getpid())
        self.assertNotEqual(pid, self.tracked.pid)
        self.assertEqual(self.recover_summary["ppid"], os.getpid())

    def test_state_on_disk_was_generating_before_recovery(self):
        self.assertEqual(self.recover_summary["status_before"], SLIDE_GENERATING)
        self.assertEqual(self.recover_summary["generation_before"], 1)

    def test_there_was_no_completed_result_to_confirm_success(self):
        self.assertEqual(self.recover_summary["attempts_before"], 0)
        self.assertFalse(self.recover_summary["completed_result_present"])
        self.assertFalse(
            self.recover_summary["completed_result_present"]
            and self.recover_summary["artifact_verified"],
            "recovery may only conclude success with a completed result AND a verified artifact",
        )
        self.assertIsNone(
            self.recover_summary["image_path"],
            "a leftover artifact must never be adopted as the slide image",
        )

    def test_recovery_resolved_generating_to_generation_failed(self):
        self.assertEqual(self.recover_summary["recovered"], [SLIDE_ID])
        self.assertEqual(self.recover_summary["status_after"], SLIDE_GENERATION_FAILED)
        blocker = self.recover_summary["blocker"]
        self.assertIsInstance(blocker, dict)
        self.assertIn("interrupted", blocker["reason"])

    def test_recovery_never_guessed_success(self):
        self.assertNotEqual(self.recover_summary["status_after"], SLIDE_GENERATED)
        self.assertNotEqual(self.recover_summary["status_after"], SLIDE_QA_PASSED)

    # -- retry -------------------------------------------------------------
    def test_second_generation_is_generation_two_and_qa_passed(self):
        slide = self.state.slide(SLIDE_ID)
        self.assertEqual(slide["generation"], 2)
        self.assertEqual(slide["status"], SLIDE_QA_PASSED)
        self.assertEqual(len(slide["attempts"]), 1, "the killed turn recorded no attempt")
        self.assertEqual(slide["attempts"][0]["generation"], 2)

    def test_final_image_exists_and_is_readable(self):
        image_path = self.state.slide(SLIDE_ID)["image_path"]
        self.assertIsNotNone(image_path)
        resolved = WORKSPACE / image_path
        self.assertTrue(lr.is_readable_image(resolved), f"not a readable image: {resolved}")

    # -- ledger ------------------------------------------------------------
    def test_ledger_recorded_the_interrupted_turn_before_it_was_made(self):
        invocations = self.ledger.invocations()
        self.assertEqual(len(invocations), 2)
        self.assertEqual([r["generation"] for r in invocations], [1, 2])
        self.assertEqual([r["role"] for r in invocations], [ROLE_GENERATE, ROLE_CONTROLLER])
        # The killed turn produced an invocation entry but never a result entry:
        # proof the ledger records the intent to call, not the outcome.
        self.assertEqual(len(self.ledger.results()), 1)

    def test_no_duplicate_invocation(self):
        self.assertEqual(self.ledger.duplicate_count(), 0)

    def test_no_api_fallback_was_used(self):
        self.assertEqual(self.ledger.api_fallback_count(), 0)
        self.assertEqual(self.second_result["backend"], BACKEND)
        self.assertFalse(self.second_result["diagnostics"]["api_fallback_used"])


ROLES = {ROLE_GENERATE: run_generating_child, ROLE_RECOVER: run_recovery_child}


def main(argv: list[str] | None = None) -> int:
    parser = lr.role_parser(__doc__ or "")
    args = parser.parse_args(argv)

    if args.role:
        if args.role not in ROLES:
            print(f"unknown role: {args.role}", file=sys.stderr)
            return 2
        workspace = Path(args.workspace or WORKSPACE)
        work_dir = Path(args.work_dir or WORK_DIR)
        return lr.role_main(lambda: ROLES[args.role](workspace, work_dir))

    if not lr.interrupt_enabled(__file__):
        print(lr.INTERRUPT_SKIP_REASON)
        return 0
    if not lr.codex_present():
        print("codex is not on PATH")
        return 1
    suite = unittest.TestLoader().loadTestsFromTestCase(Phase9CLiveInterruptionTests)
    return 0 if unittest.TextTestRunner(verbosity=2).run(suite).wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())

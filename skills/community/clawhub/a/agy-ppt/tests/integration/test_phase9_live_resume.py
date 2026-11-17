#!/usr/bin/env python3
"""Phase 9B LIVE partial resume across two real Python processes (opt-in).

    AGY_PPT_LIVE_RECOVERY=1 python3 \
        skills/agy-ppt/tests/integration/test_phase9_live_resume.py

Process A (a real, separate Python process)
    Creates a disposable 3-slide project, generates ``slide_01`` and
    ``slide_02`` through the **real** Codex Image Adapter, records both as
    ``qa_passed``, persists ``project_state.json`` and exits completely.

Process B (a brand new Python process)
    Shares no memory with Process A. It re-reads the state from disk only, must
    skip ``slide_01`` / ``slide_02``, and may generate ``slide_03`` only.

Every real Codex invocation is appended to ``codex_invocations.jsonl`` right
before the call happens, by whichever process makes it. The final proof is
therefore process-independent and file-based:

    slide_01 invocation == 1
    slide_02 invocation == 1
    slide_03 invocation == 1
    duplicate invocations == 0
    generation == 1 for every slide

Cost: exactly 3 real render turns (2 in Process A, 1 in Process B). No API key
is used, no OpenAI Images API is called, and the only writable location is
``<repo>/.agy-ppt-integration/phase9b-resume/``, removed in teardown.
"""

from __future__ import annotations

import hashlib
import os
import sys
import unittest
from pathlib import Path

TESTS_DIR = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = TESTS_DIR.parent / "scripts"
for _path in (str(TESTS_DIR), str(SCRIPTS_DIR)):
    if _path not in sys.path:
        sys.path.insert(0, _path)

from helpers import live_recovery as lr  # noqa: E402
from project_state import SLIDE_QA_PASSED, ProjectState  # noqa: E402

SCENARIO = "phase9b-resume"
PROJECT_ID = "ppt_live_phase9b_resume"
SLIDE_IDS = ("slide_01", "slide_02", "slide_03")
PROCESS_A_SLIDES = ("slide_01", "slide_02")
PROCESS_B_SLIDES = ("slide_03",)

ROLE_A = "process-a"
ROLE_B = "process-b"

WORK_DIR = lr.work_root(SCENARIO)
WORKSPACE = WORK_DIR / "deck"


def _digest(path: Path) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def _snapshot(state: ProjectState) -> dict[str, dict]:
    snapshot: dict[str, dict] = {}
    for slide_id in sorted(state.data["slides"]):
        slide = state.slide(slide_id)
        image_path = slide.get("image_path")
        resolved = Path(state.workspace_root) / image_path if image_path else None
        snapshot[slide_id] = {
            "status": slide["status"],
            "generation": slide["generation"],
            "attempts": len(slide.get("attempts", [])),
            "image_path": image_path,
            "digest": _digest(resolved) if resolved and resolved.is_file() else None,
        }
    return snapshot


# ---------------------------------------------------------------------------
# Process A -- real generation of slide_01 + slide_02, then a full exit
# ---------------------------------------------------------------------------
def run_process_a(workspace: Path, work_dir: Path) -> int:
    ledger = lr.InvocationLedger.for_scenario(SCENARIO, work_dir)
    state = lr.new_project(workspace, PROJECT_ID, SLIDE_IDS)

    generated: list[str] = []
    for index, slide_id in enumerate(PROCESS_A_SLIDES, start=1):
        lr.live_generate(
            state,
            ledger,
            slide_id,
            marker=f"P9B RESUME {index}",
            role=ROLE_A,
        )
        lr.qa_pass(state, slide_id, reason="Phase 9B live resume baseline accepted")
        generated.append(slide_id)

    state.save()
    lr.write_summary(
        work_dir,
        ROLE_A,
        {
            "state_path": str(ProjectState.state_path(workspace)),
            "slide_ids": list(SLIDE_IDS),
            "generated": generated,
            "snapshot": _snapshot(state),
            "phase": state.phase,
        },
    )
    return lr.EXIT_OK


# ---------------------------------------------------------------------------
# Process B -- a brand new process that only reads the state from disk
# ---------------------------------------------------------------------------
def run_process_b(workspace: Path, work_dir: Path) -> int:
    ledger = lr.InvocationLedger.for_scenario(SCENARIO, work_dir)
    state_path = ProjectState.state_path(workspace)
    if not state_path.is_file():
        raise lr.LiveHarnessError(f"process B found no persisted state at {state_path}")

    # Nothing is inherited from Process A: this process starts from the file.
    state = ProjectState.load(workspace)
    before = _snapshot(state)

    plan = lr.resume_plan(state)
    skipped = [slide_id for slide_id in SLIDE_IDS if slide_id not in plan]

    generated: list[str] = []
    for slide_id in plan:
        lr.live_generate(state, ledger, slide_id, marker="P9B RESUME 3", role=ROLE_B)
        lr.qa_pass(state, slide_id, reason="Phase 9B live resume tail accepted")
        generated.append(slide_id)

    state.save()
    lr.write_summary(
        work_dir,
        ROLE_B,
        {
            "state_path": str(state_path),
            "loaded_from_disk": True,
            "resume_plan": plan,
            "skipped": skipped,
            "generated": generated,
            "snapshot_before": before,
            "snapshot_after": _snapshot(state),
        },
    )
    return lr.EXIT_OK


# ---------------------------------------------------------------------------
# Verification (the controller process asserts, it never generates)
# ---------------------------------------------------------------------------
@unittest.skipUnless(lr.live_enabled(__file__), lr.SKIP_REASON)
@unittest.skipUnless(lr.codex_present(), "codex is not on PATH")
class Phase9BLivePartialResumeTests(unittest.TestCase):
    """Two real processes, three real render turns, zero duplicated work."""

    summary_a: dict
    summary_b: dict
    ledger: lr.InvocationLedger
    state: ProjectState

    @classmethod
    def setUpClass(cls) -> None:
        lr.reset_dir(WORK_DIR)
        # Registered before anything can fail, so an aborted setUpClass still
        # cleans the workspace up.
        cls.addClassCleanup(lr.cleanup, WORK_DIR)
        WORKSPACE.mkdir(parents=True, exist_ok=True)
        cls.ledger = lr.InvocationLedger.for_scenario(SCENARIO, WORK_DIR)
        turn_budget = lr.default_timeout()

        first = lr.run_role(
            __file__,
            ROLE_A,
            workspace=WORKSPACE,
            work_dir=WORK_DIR,
            ledger=cls.ledger,
            timeout=2 * turn_budget + 180,
        )
        cls._check(first, ROLE_A)

        second = lr.run_role(
            __file__,
            ROLE_B,
            workspace=WORKSPACE,
            work_dir=WORK_DIR,
            ledger=cls.ledger,
            timeout=turn_budget + 180,
        )
        cls._check(second, ROLE_B)

        cls.summary_a = lr.read_summary(WORK_DIR, ROLE_A)
        cls.summary_b = lr.read_summary(WORK_DIR, ROLE_B)
        cls.state = ProjectState.load(WORKSPACE)

    @classmethod
    def _check(cls, result, role: str) -> None:
        if result.returncode == lr.EXIT_SKIP:
            raise unittest.SkipTest(
                f"{role}: built-in image_gen / Codex session unavailable "
                f"(runtime capability blocker, not a coding failure)\n"
                f"{lr.child_failure_detail(result)}"
            )
        if result.returncode != lr.EXIT_OK:
            raise AssertionError(f"{role} failed\n{lr.child_failure_detail(result)}")

    # -- two genuinely different processes ---------------------------------
    def test_process_a_and_process_b_are_separate_python_processes(self):
        pid_a = self.summary_a["pid"]
        pid_b = self.summary_b["pid"]
        self.assertNotEqual(pid_a, pid_b, "resume must cross a real process boundary")
        self.assertNotIn(pid_a, (0, None))
        self.assertNotEqual(pid_a, os.getpid())
        self.assertNotEqual(pid_b, os.getpid())
        self.assertEqual(self.summary_b["ppid"], os.getpid())

    def test_process_b_read_the_state_from_disk_only(self):
        self.assertTrue(self.summary_b["loaded_from_disk"])
        self.assertEqual(self.summary_b["state_path"], self.summary_a["state_path"])
        # Process A's own view is gone; the only carrier is project_state.json.
        self.assertTrue(Path(self.summary_a["state_path"]).is_file())

    # -- resume decisions --------------------------------------------------
    def test_process_b_skipped_the_finished_slides(self):
        self.assertEqual(self.summary_b["skipped"], list(PROCESS_A_SLIDES))
        for slide_id in PROCESS_A_SLIDES:
            self.assertNotIn(slide_id, self.summary_b["resume_plan"])

    def test_process_b_generated_only_slide_03(self):
        self.assertEqual(self.summary_b["resume_plan"], list(PROCESS_B_SLIDES))
        self.assertEqual(self.summary_b["generated"], list(PROCESS_B_SLIDES))
        self.assertEqual(self.summary_a["generated"], list(PROCESS_A_SLIDES))

    def test_finished_slide_images_were_not_rewritten(self):
        before = self.summary_b["snapshot_before"]
        after = self.summary_b["snapshot_after"]
        for slide_id in PROCESS_A_SLIDES:
            self.assertIsNotNone(before[slide_id]["digest"], f"{slide_id} had no image")
            self.assertEqual(
                before[slide_id]["digest"],
                after[slide_id]["digest"],
                f"{slide_id} image bytes changed during resume",
            )

    # -- the file-based invocation proof -----------------------------------
    def test_each_slide_was_invoked_exactly_once(self):
        for slide_id in SLIDE_IDS:
            self.assertEqual(
                self.ledger.count_for(slide_id),
                1,
                f"{slide_id} real Codex invocations: {self.ledger.invocations()}",
            )
        self.assertEqual(self.ledger.total(), len(SLIDE_IDS))

    def test_there_were_no_duplicate_invocations(self):
        self.assertEqual(self.ledger.duplicate_count(), 0)

    def test_each_invocation_was_generation_one(self):
        for slide_id in SLIDE_IDS:
            self.assertEqual(self.ledger.generations_for(slide_id), [1])

    def test_invocations_are_attributed_to_the_right_process(self):
        self.assertEqual(self.ledger.slides_for_role(ROLE_A), list(PROCESS_A_SLIDES))
        self.assertEqual(self.ledger.slides_for_role(ROLE_B), list(PROCESS_B_SLIDES))

    def test_no_api_fallback_was_used(self):
        self.assertEqual(self.ledger.api_fallback_count(), 0)
        for record in self.ledger.results():
            self.assertEqual(record["backend"], "codex_builtin_imagegen")

    # -- final persisted state --------------------------------------------
    def test_final_state_has_one_generation_per_slide(self):
        for slide_id in SLIDE_IDS:
            slide = self.state.slide(slide_id)
            self.assertEqual(slide["status"], SLIDE_QA_PASSED, slide_id)
            self.assertEqual(slide["generation"], 1, slide_id)
            self.assertEqual(len(slide["attempts"]), 1, slide_id)

    def test_every_slide_image_is_a_readable_file(self):
        for slide_id in SLIDE_IDS:
            image_path = self.state.slide(slide_id)["image_path"]
            self.assertIsNotNone(image_path, slide_id)
            resolved = WORKSPACE / image_path
            self.assertTrue(lr.is_readable_image(resolved), f"{slide_id}: {resolved}")


ROLES = {ROLE_A: run_process_a, ROLE_B: run_process_b}


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

    if not lr.live_enabled(__file__):
        print(lr.SKIP_REASON)
        return 0
    if not lr.codex_present():
        print("codex is not on PATH")
        return 1
    suite = unittest.TestLoader().loadTestsFromTestCase(Phase9BLivePartialResumeTests)
    return 0 if unittest.TextTestRunner(verbosity=2).run(suite).wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())

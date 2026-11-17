#!/usr/bin/env python3
"""Phase 9D LIVE assembly failure & recovery (opt-in, zero Codex quota).

    AGY_PPT_LIVE_RECOVERY=1 python3 \
        skills/agy-ppt/tests/integration/test_phase9_live_assembly_recovery.py

This scenario never calls Codex. Test PNGs are placed on disk, every slide is
driven to ``qa_passed``, and then the **real** upstream assembly script
(``scripts/assemble_ppt.py``) is run twice:

1. once with a safe, predictable *invalid* input -- the assembly is pointed at a
   deck directory that does not exist -- so upstream assembly fails without
   writing anything and without touching a slide image;
2. once with the input corrected, which must be enough on its own: only the
   assembly step is re-run.

The failure must not damage anything upstream of assembly:

    slides do not regress out of qa_passed
    generation does not increase
    attempts do not increase
    Codex invocations == 0

After the fix, slides become ``assembled`` and the project becomes ``complete``.

Two independent guards prove the zero-quota claim: the invocation ledger stays
empty for this scenario, and ``codex_image_adapter.run_codex`` is patched to fail
loudly for the whole class, so any accidental Codex use would be an error rather
than a silent charge. The only writable location is
``<repo>/.agy-ppt-integration/phase9d-assembly/``, removed in teardown.
"""

from __future__ import annotations

import hashlib
import re
import sys
import unittest
import zipfile
from pathlib import Path
from unittest import mock

TESTS_DIR = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = TESTS_DIR.parent / "scripts"
for _path in (str(TESTS_DIR), str(SCRIPTS_DIR)):
    if _path not in sys.path:
        sys.path.insert(0, _path)

import codex_image_adapter  # noqa: E402
from helpers import live_recovery as lr  # noqa: E402
from helpers.fake_image_worker import FakeImageWorker, SlidePlan  # noqa: E402
from project_state import (  # noqa: E402
    PHASE_ASSEMBLY,
    PHASE_COMPLETE,
    PHASE_SLIDE_GENERATION,
    PHASE_VISUAL_QA,
    SLIDE_ASSEMBLED,
    SLIDE_QA_PASSED,
    SLIDE_READY,
    InvalidStateTransition,
    ProjectState,
)

SCENARIO = "phase9d-assembly"
PROJECT_ID = "ppt_live_phase9d_assembly"
SLIDE_IDS = ("slide_01", "slide_02", "slide_03")

DECK_NAME = "deck"
GOOD_OUTPUT = f"{DECK_NAME}.pptx"
# Safe and predictable invalid input: assembly is pointed at a deck directory
# that does not exist. Upstream refuses, writes nothing, and touches nothing.
BAD_OUTPUT = "phase9d_missing_deck.pptx"

WORK_DIR = lr.work_root(SCENARIO)
BASE_DIR = WORK_DIR
WORKSPACE = WORK_DIR / DECK_NAME
IMAGE_DIR = "origin_image"

_SLIDE_XML = re.compile(r"^ppt/slides/slide\d+\.xml$")


def _digests(root: Path) -> dict[str, str]:
    base = Path(root) / IMAGE_DIR
    return {
        path.name: hashlib.sha256(path.read_bytes()).hexdigest()
        for path in sorted(base.glob("*.png"))
    }


def _slide_snapshot(state: ProjectState) -> dict[str, dict]:
    return {
        slide_id: {
            "status": state.slide(slide_id)["status"],
            "generation": state.slide(slide_id)["generation"],
            "attempts": len(state.slide(slide_id)["attempts"]),
            "image_path": state.slide(slide_id)["image_path"],
        }
        for slide_id in SLIDE_IDS
    }


@unittest.skipUnless(lr.live_enabled(__file__), lr.SKIP_REASON)
class Phase9DLiveAssemblyRecoveryTests(unittest.TestCase):
    """Real upstream assembly: fail once on bad input, then recover cleanly."""

    ledger: lr.InvocationLedger
    python: str
    worker: FakeImageWorker
    before: dict
    after_failure: dict
    final: dict
    failed_run: object
    fixed_run: object
    digests_before: dict
    digests_after_failure: dict
    digests_final: dict
    pptx_after_failure: list
    state: ProjectState

    @classmethod
    def setUpClass(cls) -> None:
        python = lr.assembly_python()
        if python is None:
            raise unittest.SkipTest(
                "no interpreter with python-pptx is available; run "
                "'python3 skills/agy-ppt/scripts/codex_ppt_runtime.py bootstrap' first. "
                "This is a runtime capability blocker: nothing is installed by the test."
            )
        cls.python = python

        # Hard guard: this scenario must never reach Codex.
        patcher = mock.patch.object(
            codex_image_adapter,
            "run_codex",
            side_effect=AssertionError("phase 9D must not invoke codex"),
        )
        patcher.start()
        cls.addClassCleanup(patcher.stop)

        lr.reset_dir(WORK_DIR)
        # Registered before anything can fail, so an aborted setUpClass still
        # cleans the workspace up.
        cls.addClassCleanup(lr.cleanup, WORK_DIR)
        WORKSPACE.mkdir(parents=True, exist_ok=True)
        cls.ledger = lr.InvocationLedger.for_scenario(SCENARIO, WORK_DIR)

        # Test PNGs, written by the test itself -- no image worker, no Codex.
        for index, slide_id in enumerate(SLIDE_IDS):
            lr.write_test_png(
                WORKSPACE / IMAGE_DIR / f"{slide_id}.png", shade=210 + index * 12
            )

        state = lr.new_project(WORKSPACE, PROJECT_ID, SLIDE_IDS)
        # create_artifact=False: the deterministic worker records the same result
        # contract the adapter records, but the artifacts stay the test PNGs.
        cls.worker = FakeImageWorker(WORKSPACE, default_plan=SlidePlan(create_artifact=False))
        for slide_id in SLIDE_IDS:
            state.set_slide_status(slide_id, SLIDE_READY)
            generation = state.begin_generation(slide_id, job_path=f"prompts/{slide_id}.json")
            state.save()
            result = cls.worker.run(slide_id, generation=generation)
            state.record_worker_result(slide_id, result)
            state.save()
            lr.qa_pass(state, slide_id, reason="Phase 9D assembly-recovery fixture")

        state.set_phase(PHASE_VISUAL_QA)
        state.set_phase(PHASE_ASSEMBLY)
        state.save()

        cls.before = _slide_snapshot(state)
        cls.digests_before = _digests(WORKSPACE)

        # 1. real upstream assembly, invalid input -> must fail cleanly.
        cls.failed_run = lr.run_assembly(python, BASE_DIR, BAD_OUTPUT)
        cls.after_failure = _slide_snapshot(ProjectState.load(WORKSPACE))
        cls.digests_after_failure = _digests(WORKSPACE)
        cls.pptx_after_failure = lr.find_pptx(WORK_DIR)

        # 2. input corrected -> only assembly is re-run.
        cls.fixed_run = lr.run_assembly(python, BASE_DIR, GOOD_OUTPUT)

        state = ProjectState.load(WORKSPACE)
        lr.mark_assembled(state, SLIDE_IDS)
        state.set_phase(PHASE_COMPLETE)
        state.save()
        cls.state = ProjectState.load(WORKSPACE)
        cls.final = _slide_snapshot(cls.state)
        cls.digests_final = _digests(WORKSPACE)

    # -- the injected failure ---------------------------------------------
    def test_first_assembly_failed_on_the_invalid_input(self):
        self.assertNotEqual(self.failed_run.returncode, 0, self.failed_run.stdout)
        self.assertIn(BAD_OUTPUT.removesuffix(".pptx"), self.failed_run.stdout)

    def test_failed_assembly_wrote_no_deck_file(self):
        self.assertEqual(self.pptx_after_failure, [], "a failed assembly must leave no deck")

    def test_failed_assembly_left_the_slide_images_untouched(self):
        self.assertEqual(self.digests_before, self.digests_after_failure)
        self.assertEqual(len(self.digests_before), len(SLIDE_IDS))

    # -- nothing upstream regressed ---------------------------------------
    def test_slides_did_not_regress(self):
        for slide_id in SLIDE_IDS:
            self.assertEqual(self.after_failure[slide_id]["status"], SLIDE_QA_PASSED, slide_id)

    def test_generation_did_not_increase(self):
        for slide_id in SLIDE_IDS:
            self.assertEqual(
                self.after_failure[slide_id]["generation"],
                self.before[slide_id]["generation"],
                slide_id,
            )
            self.assertEqual(self.after_failure[slide_id]["generation"], 1, slide_id)

    def test_attempts_did_not_increase(self):
        for slide_id in SLIDE_IDS:
            self.assertEqual(
                self.after_failure[slide_id]["attempts"],
                self.before[slide_id]["attempts"],
                slide_id,
            )
            self.assertEqual(self.after_failure[slide_id]["attempts"], 1, slide_id)

    def test_no_codex_invocation_happened(self):
        self.assertEqual(self.ledger.total(), 0)
        self.assertEqual(self.ledger.invocations(), [])
        self.assertEqual(self.ledger.api_fallback_count(), 0)

    def test_no_image_was_regenerated(self):
        self.assertEqual(self.worker.call_count, len(SLIDE_IDS))
        self.assertEqual(self.digests_before, self.digests_final)

    def test_project_cannot_regress_to_slide_generation(self):
        # In-memory probe only: the phase is rewound locally to the moment of the
        # assembly failure and never saved, so the on-disk state is untouched.
        state = ProjectState.load(WORKSPACE)
        state.data["phase"] = PHASE_ASSEMBLY
        with self.assertRaises(InvalidStateTransition):
            state.set_phase(PHASE_SLIDE_GENERATION)
        with self.assertRaises(InvalidStateTransition):
            state.set_phase(PHASE_VISUAL_QA)
        self.assertEqual(ProjectState.load(WORKSPACE).phase, PHASE_COMPLETE)

    # -- recovery ----------------------------------------------------------
    def test_rerunning_only_assembly_succeeds(self):
        self.assertEqual(self.fixed_run.returncode, 0, self.fixed_run.stdout)

    def test_exactly_one_deck_file_was_produced(self):
        decks = lr.find_pptx(WORK_DIR)
        self.assertEqual([p.name for p in decks], [GOOD_OUTPUT])
        self.assertTrue(lr.is_pptx(decks[0]))

    def test_the_deck_has_one_slide_per_image(self):
        deck = WORKSPACE / GOOD_OUTPUT
        with zipfile.ZipFile(deck) as archive:
            slides = [name for name in archive.namelist() if _SLIDE_XML.match(name)]
        self.assertEqual(len(slides), len(SLIDE_IDS))

    def test_slides_are_assembled_and_the_project_is_complete(self):
        for slide_id in SLIDE_IDS:
            self.assertEqual(self.final[slide_id]["status"], SLIDE_ASSEMBLED, slide_id)
        self.assertEqual(self.state.phase, PHASE_COMPLETE)
        self.assertEqual(self.state.summary()["assembled"], len(SLIDE_IDS))


def main(argv: list[str] | None = None) -> int:
    parser = lr.role_parser(__doc__ or "")
    args = parser.parse_args(argv)
    if args.role:
        print(f"{Path(__file__).name} has no child roles", file=sys.stderr)
        return 2
    if not lr.live_enabled(__file__):
        print(lr.SKIP_REASON)
        return 0
    suite = unittest.TestLoader().loadTestsFromTestCase(Phase9DLiveAssemblyRecoveryTests)
    return 0 if unittest.TextTestRunner(verbosity=2).run(suite).wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())

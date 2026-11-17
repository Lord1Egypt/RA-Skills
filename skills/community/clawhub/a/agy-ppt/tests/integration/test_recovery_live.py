#!/usr/bin/env python3
"""Opt-in LIVE recovery scenarios (Phase 9, quota-consuming).

These two scenarios are the only Phase 9 tests that call the real Codex CLI
through the already-authenticated ChatGPT/Codex subscription session. They are
**never** part of the default unit/recovery suite and are skipped unless
explicitly requested::

    AGY_PPT_LIVE_RECOVERY=1 python3 -m unittest discover \
        -s skills/agy-ppt/tests/integration -t skills/agy-ppt/tests/integration -v

    # or directly
    python3 skills/agy-ppt/tests/integration/test_recovery_live.py

Live A -- generate a small number of slides for real, then reload the project
state from disk and verify that finished slides are not re-generated (no further
render turn is dispatched, image bytes are unchanged).

Live B -- generate one slide for real, have AGY judge it ``qa_failed``, then
regenerate it and verify ``generation == 2``, ``attempts == 2`` and that attempt
1 survives in history.

Cost: Live A uses ``AGY_PPT_LIVE_RECOVERY_SLIDES`` (default 1) render turns,
Live B uses 2. Nothing here uses ``OPENAI_API_KEY``; the adapter strips API-key
style variables from the child environment and the worker prompt forbids any API
fallback. If the runtime does not expose the built-in ``image_gen`` tool the
adapter reports ``IMAGE_BACKEND_UNAVAILABLE`` and the scenario is skipped as a
runtime capability blocker, not a failure.

The only writable target is ``<repo>/.agy-ppt-integration/live-recovery/``,
which is removed again in teardown.
"""

from __future__ import annotations

import hashlib
import os
import shutil
import sys
import unittest
from pathlib import Path

TESTS_DIR = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = TESTS_DIR.parent / "scripts"
REPO_ROOT = TESTS_DIR.parents[2]
for _path in (str(TESTS_DIR), str(SCRIPTS_DIR)):
    if _path not in sys.path:
        sys.path.insert(0, _path)

from codex_image_adapter import (  # noqa: E402
    ERROR_BACKEND_UNAVAILABLE,
    OP_GENERATE,
    OP_REGENERATE,
    STATUS_COMPLETED,
    CodexImageAdapter,
    ImageRequest,
)
from helpers.recovery_deck import plan_dispatch  # noqa: E402
from project_state import (  # noqa: E402
    PHASE_OUTLINE,
    PHASE_SAMPLE,
    PHASE_SLIDE_GENERATION,
    PHASE_STYLE,
    SLIDE_GENERATED,
    SLIDE_QA_FAILED,
    SLIDE_READY,
    ProjectState,
)

LIVE_ENV_FLAG = "AGY_PPT_LIVE_RECOVERY"
PROBE_DIR_NAME = ".agy-ppt-integration"
WORK_DIR_NAME = "live-recovery"
WORK_ROOT = REPO_ROOT / PROBE_DIR_NAME / WORK_DIR_NAME
DEFAULT_TIMEOUT = float(os.environ.get("AGY_PPT_LIVE_RECOVERY_TIMEOUT", "420"))
LIVE_A_SLIDES = max(1, int(os.environ.get("AGY_PPT_LIVE_RECOVERY_SLIDES", "1")))

SKIP_REASON = (
    f"live recovery scenarios: set {LIVE_ENV_FLAG}=1 (or run this file directly) "
    "with a logged-in Codex/ChatGPT subscription session. These consume subscription quota."
)


def live_enabled() -> bool:
    if os.environ.get(LIVE_ENV_FLAG) == "1":
        return True
    return Path(sys.argv[0]).name == Path(__file__).name


def codex_present() -> bool:
    return shutil.which("codex") is not None


def _prompt(slide_id: str, marker: str) -> str:
    return (
        "Use case: productivity-visual\n"
        "Asset type: throwaway recovery-test slide image\n"
        f"Primary request: a plain 16:9 slide with a light background and the exact text "
        f"'{marker}' centered in large dark sans-serif letters\n"
        f'Text (verbatim): "{marker}"\n'
        "Composition/framing: 16:9 landscape, centered text, generous margins\n"
        "Constraints: no other text, no logos, no watermark\n"
    )


def _digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


class LiveRecoveryBase(unittest.TestCase):
    """Shared live deck: a real ProjectState in a throwaway repo-local workspace."""

    workspace_name = "deck"
    slide_ids: tuple[str, ...] = ("slide_01",)

    def setUp(self) -> None:
        self.ws = WORK_ROOT / self.workspace_name
        if self.ws.exists():
            shutil.rmtree(self.ws)
        self.ws.mkdir(parents=True)
        self.render_turns = 0
        self.state = ProjectState.initialize(
            self.ws, "ppt_live_recovery", slide_ids=self.slide_ids
        )
        self.state.save()
        for gate in ("outline", "style", "sample"):
            self.state.set_gate(gate, "approved")
        for phase in (PHASE_OUTLINE, PHASE_STYLE, PHASE_SAMPLE, PHASE_SLIDE_GENERATION):
            self.state.set_phase(phase)
        self.state.save()

    def tearDown(self) -> None:
        if WORK_ROOT.exists():
            shutil.rmtree(WORK_ROOT, ignore_errors=True)
        parent = REPO_ROOT / PROBE_DIR_NAME
        if parent.is_dir() and not any(parent.iterdir()):
            parent.rmdir()

    # -- one real render turn ---------------------------------------------
    def live_dispatch(self, slide_id: str, marker: str, operation: str = OP_GENERATE) -> dict:
        if self.state.slide(slide_id)["status"] != SLIDE_READY:
            self.state.set_slide_status(slide_id, SLIDE_READY)
        generation = self.state.begin_generation(slide_id)
        self.state.save()

        request = ImageRequest.from_dict(
            {
                "slide_id": slide_id,
                "operation": operation,
                "prompt": _prompt(slide_id, marker),
                "output_path": f"origin_image/{slide_id}.png",
                "aspect_ratio": "16:9",
                "workspace_root": str(self.ws),
                "timeout_seconds": DEFAULT_TIMEOUT,
            }
        )
        self.render_turns += 1
        result = CodexImageAdapter(request).run().to_dict()
        if result.get("error_code") == ERROR_BACKEND_UNAVAILABLE:
            self.skipTest(
                "built-in image_gen is not exposed by the current Codex runtime "
                "(IMAGE_BACKEND_UNAVAILABLE): runtime capability blocker, not a coding failure"
            )
        self.assertFalse(result["diagnostics"]["api_fallback_used"], "API fallback is forbidden")
        self.state.record_worker_result(slide_id, result)
        self.state.save()
        self.assertEqual(
            result["status"], STATUS_COMPLETED, result.get("error_message", "live turn failed")
        )
        self.assertEqual(self.state.slide(slide_id)["generation"], generation)
        return result

    def reload(self) -> ProjectState:
        self.state = ProjectState.load(self.ws)
        return self.state


@unittest.skipUnless(live_enabled(), SKIP_REASON)
@unittest.skipUnless(codex_present(), "codex is not on PATH")
class LiveASettledSlidesAreNotRegenerated(LiveRecoveryBase):
    """Live A: generate a few slides for real, reload, confirm no re-generation."""

    slide_ids = tuple(f"slide_{i:02d}" for i in range(1, LIVE_A_SLIDES + 2))

    def test_reload_does_not_regenerate_finished_slides(self):
        generated = list(self.slide_ids[:LIVE_A_SLIDES])
        for index, slide_id in enumerate(generated, start=1):
            self.live_dispatch(slide_id, f"LIVE A {index}")
            self.assertEqual(self.state.slide(slide_id)["status"], SLIDE_GENERATED)

        digests = {
            slide_id: _digest(self.ws / self.state.slide(slide_id)["image_path"])
            for slide_id in generated
        }
        turns_after_first_pass = self.render_turns

        # Fresh process view: read the state back from disk.
        self.reload()
        for slide_id in generated:
            slide = self.state.slide(slide_id)
            self.assertEqual(slide["status"], SLIDE_GENERATED)
            self.assertEqual(slide["generation"], 1)
            self.assertEqual(len(slide["attempts"]), 1)

        # A resume must only offer the slides that are still unfinished.
        dispatchable = plan_dispatch(self.state)
        for slide_id in generated:
            self.assertNotIn(slide_id, dispatchable, f"{slide_id} would be re-generated")

        # Nothing re-rendered, and the image bytes are untouched.
        self.assertEqual(self.render_turns, turns_after_first_pass)
        for slide_id, digest in digests.items():
            self.assertEqual(
                _digest(self.ws / self.state.slide(slide_id)["image_path"]),
                digest,
                f"{slide_id} image was rewritten",
            )


@unittest.skipUnless(live_enabled(), SKIP_REASON)
@unittest.skipUnless(codex_present(), "codex is not on PATH")
class LiveBQaFailedRegeneration(LiveRecoveryBase):
    """Live B: real generation -> AGY qa_failed -> real regeneration."""

    slide_ids = ("slide_01",)

    def test_qa_failed_regeneration_counts_correctly(self):
        first = self.live_dispatch("slide_01", "LIVE B ONE")
        self.assertEqual(self.state.slide("slide_01")["generation"], 1)
        first_attempt = dict(self.state.slide("slide_01")["attempts"][0])

        # AGY (never the worker) makes the visual-QA judgement.
        self.state.set_slide_status("slide_01", SLIDE_QA_FAILED, by="agy")
        self.state.set_slide_status("slide_01", SLIDE_READY)
        self.state.save()

        second = self.live_dispatch("slide_01", "LIVE B TWO", operation=OP_REGENERATE)
        self.reload()

        slide = self.state.slide("slide_01")
        self.assertEqual(slide["status"], SLIDE_GENERATED)
        self.assertEqual(slide["generation"], 2)
        self.assertEqual(len(slide["attempts"]), 2)
        self.assertEqual([a["generation"] for a in slide["attempts"]], [1, 2])
        self.assertEqual(slide["attempts"][0], first_attempt, "attempt 1 must not be overwritten")
        self.assertNotEqual(
            slide["attempts"][0]["idempotency_key"], slide["attempts"][1]["idempotency_key"]
        )
        self.assertTrue((self.ws / slide["image_path"]).is_file())
        self.assertEqual(first["operation"], OP_GENERATE)
        self.assertEqual(second["operation"], OP_REGENERATE)


def main() -> int:
    if not live_enabled():
        print(SKIP_REASON)
        return 0
    if not codex_present():
        print("codex is not on PATH")
        return 1
    loader = unittest.TestLoader()
    suite = unittest.TestSuite(
        [
            loader.loadTestsFromTestCase(LiveASettledSlidesAreNotRegenerated),
            loader.loadTestsFromTestCase(LiveBQaFailedRegeneration),
        ]
    )
    return 0 if unittest.TextTestRunner(verbosity=2).run(suite).wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())

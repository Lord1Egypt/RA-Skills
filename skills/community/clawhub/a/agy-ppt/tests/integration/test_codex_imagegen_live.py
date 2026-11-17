#!/usr/bin/env python3
"""Live built-in image_gen integration test for the AGY -> Codex image adapter.

This test drives the *real* Codex CLI, using the already-authenticated local
ChatGPT/Codex subscription session, to generate one minimal probe image through
the built-in ``image_gen`` tool. It never uses ``OPENAI_API_KEY`` and never
touches the paid Images API: the adapter strips API-key style variables from the
child environment, and the worker prompt forbids any API fallback.

It is **opt-in** and skipped unless explicitly requested::

    AGY_PPT_LIVE_CODEX_IMAGE=1 python3 -m unittest discover \
        -s skills/agy-ppt/tests/integration -t skills/agy-ppt/tests/integration -v

    # or directly
    python3 skills/agy-ppt/tests/integration/test_codex_imagegen_live.py

The only writable target is::

    <repo>/.agy-ppt-integration/codex-imagegen-probe.png

which is removed again in teardown, together with the probe directory when it
ends up empty.

If the current Codex runtime does not expose the built-in ``image_gen`` tool,
this test does **not** fall back to any API. The adapter returns
``IMAGE_BACKEND_UNAVAILABLE`` and the test treats that as a runtime capability
blocker (a skip), not a coding failure.
"""

from __future__ import annotations

import os
import shutil
import sys
import unittest
from pathlib import Path

TESTS_DIR = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = TESTS_DIR.parent / "scripts"
REPO_ROOT = TESTS_DIR.parents[2]
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import codex_image_adapter as adapter  # noqa: E402
from codex_image_adapter import (  # noqa: E402
    BACKEND,
    ERROR_BACKEND_UNAVAILABLE,
    OP_GENERATE,
    STATUS_COMPLETED,
    CodexImageAdapter,
    ImageRequest,
    sniff_image,
)

LIVE_ENV_FLAG = "AGY_PPT_LIVE_CODEX_IMAGE"
PROBE_DIR_NAME = ".agy-ppt-integration"
PROBE_FILE_NAME = "codex-imagegen-probe.png"
PROBE_DIR = REPO_ROOT / PROBE_DIR_NAME
PROBE_FILE = PROBE_DIR / PROBE_FILE_NAME
PROBE_REL = f"{PROBE_DIR_NAME}/{PROBE_FILE_NAME}"
DEFAULT_TIMEOUT = float(os.environ.get("AGY_PPT_LIVE_CODEX_TIMEOUT", "420"))

# Must never be used as a write probe.
FORBIDDEN_PROBE_PARTS = ("SKILL.md", "docs", "scripts", "tests", "assets", "references")

PROBE_PROMPT = (
    "Use case: productivity-visual\n"
    "Asset type: throwaway integration probe image\n"
    "Primary request: a plain 16:9 slide with a light background and the exact "
    "text 'CODEX IMAGEGEN OK' centered in large dark sans-serif letters\n"
    "Text (verbatim): \"CODEX IMAGEGEN OK\"\n"
    "Composition/framing: 16:9 landscape, centered text, generous margins\n"
    "Constraints: no other text, no logos, no watermark\n"
)


def live_enabled() -> bool:
    if os.environ.get(LIVE_ENV_FLAG) == "1":
        return True
    return Path(sys.argv[0]).name == Path(__file__).name


def codex_present() -> bool:
    return shutil.which("codex") is not None


SKIP_REASON = (
    f"live Codex image integration test: set {LIVE_ENV_FLAG}=1 (or run this file "
    "directly) with a logged-in Codex/ChatGPT subscription session"
)


@unittest.skipUnless(live_enabled(), SKIP_REASON)
@unittest.skipUnless(codex_present(), "codex is not on PATH")
class CodexImageGenLiveTests(unittest.TestCase):
    """One real built-in image_gen turn that writes a throwaway probe image."""

    result: adapter.AdapterResult
    payload: dict
    file_existed_after_turn: bool
    backend_unavailable: bool

    @classmethod
    def setUpClass(cls) -> None:
        assert PROBE_DIR_NAME.startswith("."), "probe dir must be a dot directory"
        for part in FORBIDDEN_PROBE_PARTS:
            assert part not in PROBE_REL.split("/"), f"probe path must not touch {part}"

        cls._dir_existed_before = PROBE_DIR.exists()
        PROBE_DIR.mkdir(parents=True, exist_ok=True)
        if PROBE_FILE.exists():
            PROBE_FILE.unlink()

        request = ImageRequest.from_dict(
            {
                "slide_id": "integration_probe",
                "operation": OP_GENERATE,
                "prompt": PROBE_PROMPT,
                "output_path": PROBE_REL,
                "aspect_ratio": "16:9",
                "workspace_root": str(REPO_ROOT),
                "timeout_seconds": DEFAULT_TIMEOUT,
            }
        )
        cls.request = request
        cls.result = CodexImageAdapter(request).run()
        cls.payload = cls.result.to_dict()
        cls.backend_unavailable = cls.result.error_code == ERROR_BACKEND_UNAVAILABLE

        cls.file_existed_after_turn = PROBE_FILE.exists()
        if os.environ.get("AGY_PPT_LIVE_DUMP"):
            import json

            print(json.dumps(cls.payload, ensure_ascii=False, indent=2))

    @classmethod
    def tearDownClass(cls) -> None:
        if PROBE_FILE.exists():
            PROBE_FILE.unlink()
        if PROBE_DIR.exists() and not cls._dir_existed_before and not any(PROBE_DIR.iterdir()):
            PROBE_DIR.rmdir()

    def _skip_if_backend_unavailable(self) -> None:
        if self.backend_unavailable:
            self.skipTest(
                "built-in image_gen is not exposed by the current Codex runtime; "
                "reported IMAGE_BACKEND_UNAVAILABLE (runtime capability blocker, "
                "not a coding failure)"
            )

    def test_no_api_fallback_and_oauth_only(self):
        # This holds regardless of backend availability.
        self.assertFalse(self.result.diagnostics["api_fallback_used"])
        self.assertEqual(self.result.diagnostics["auth"], "chatgpt_cli_session")

    def test_completed_status(self):
        self._skip_if_backend_unavailable()
        self.assertEqual(self.result.status, STATUS_COMPLETED, self.result.error_message)

    def test_backend_is_builtin_imagegen(self):
        self._skip_if_backend_unavailable()
        self.assertEqual(self.result.backend, BACKEND)

    def test_output_exists_and_nonzero(self):
        self._skip_if_backend_unavailable()
        self.assertTrue(self.file_existed_after_turn, "probe image was not created")
        self.assertGreater(PROBE_FILE.stat().st_size, 0)

    def test_output_is_readable_image(self):
        self._skip_if_backend_unavailable()
        info = sniff_image(PROBE_FILE)
        self.assertIsNotNone(info, "probe output is not a readable raster image")
        self.assertGreater(info.width, 0)
        self.assertGreater(info.height, 0)

    def test_output_inside_workspace(self):
        self._skip_if_backend_unavailable()
        self.assertTrue(str(PROBE_FILE.resolve()).startswith(str(REPO_ROOT.resolve())))

    def test_control_returns_to_agy(self):
        self.assertEqual(self.payload["control"], "returned_to_agy")
        self.assertEqual(self.payload["next_step_owner"], "AGY")


def main() -> int:
    if not live_enabled():
        print(SKIP_REASON)
        return 0
    if not codex_present():
        print("codex is not on PATH")
        return 1
    runner = unittest.TextTestRunner(verbosity=2)
    suite = unittest.TestLoader().loadTestsFromTestCase(CodexImageGenLiveTests)
    return 0 if runner.run(suite).wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())

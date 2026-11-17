#!/usr/bin/env python3
"""Recovery scenario 4: the produced artifact is not a valid image.

The render turn produced a payload that is not a readable raster image, so the
worker returns ``IMAGE_OUTPUT_INVALID`` instead of a completed result.

Contract under test:

* an invalid artifact never reaches ``generated``
* ``image_path`` is never recorded as a legal final output for the invalid turn
* the invalid payload is rejected by the same sniffing logic production uses
  (``codex_image_adapter.sniff_image``)
* a pre-existing garbage file at the output path is not adopted as a result
* only after a retry does the slide own a valid final image
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

TESTS_DIR = Path(__file__).resolve().parents[1]
if str(TESTS_DIR) not in sys.path:
    sys.path.insert(0, str(TESTS_DIR))

from helpers.fault_matrix import attach_matrix_tests  # noqa: E402
from helpers.fake_image_worker import FAULT_OUTPUT_INVALID, is_valid_png  # noqa: E402
from helpers.recovery_deck import (  # noqa: E402
    SLIDE_GENERATED,
    SLIDE_GENERATION_FAILED,
    RecoveryTestCase,
)

# Read-only use of the frozen adapter: its artifact sniffing is the production
# definition of "is this a real image".
from codex_image_adapter import sniff_image  # noqa: E402


class InvalidOutputTests(RecoveryTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.advance_to_slide_generation()
        self.worker.set_plan(
            "slide_03", fault=FAULT_OUTPUT_INVALID, succeed_on=2
        )
        self.outcome = self.dispatch("slide_03")

    def test_error_code_is_output_invalid(self):
        self.assertEqual(self.outcome.error_code, FAULT_OUTPUT_INVALID)

    def test_invalid_artifact_does_not_reach_generated(self):
        self.assert_slide("slide_03", SLIDE_GENERATION_FAILED, generation=1, attempts=1)
        self.assert_not_generated("slide_03")

    def test_image_path_is_not_recorded_for_invalid_output(self):
        slide = self.state.slide("slide_03")
        self.assertIsNone(slide["image_path"])
        self.assertIsNone(slide["attempts"][0]["output_path"])
        self.assertFalse((self.ws / "origin_image" / "slide_03.png").exists())

    def test_rejected_payload_is_not_a_readable_image(self):
        discovery = (
            self.state.slide("slide_03")["attempts"][0].get("diagnostics") or {}
        ).get("artifact_discovery") or {}
        candidates = discovery.get("candidates") or []
        self.assertEqual(len(candidates), 1)
        rejected = self.ws / candidates[0]
        self.assertTrue(rejected.is_file())
        self.assertIsNone(sniff_image(rejected), "rejected payload must not sniff as an image")
        self.assertFalse(is_valid_png(rejected))

    def test_stale_garbage_at_output_path_is_never_adopted(self):
        garbage = self.ws / "origin_image" / "slide_04.png"
        garbage.parent.mkdir(parents=True, exist_ok=True)
        garbage.write_bytes(b"leftover junk, not an image\n")
        self.worker.set_plan("slide_04", fault=FAULT_OUTPUT_INVALID)
        outcome = self.dispatch("slide_04")
        self.assertEqual(outcome.error_code, FAULT_OUTPUT_INVALID)
        slide = self.assert_slide("slide_04", SLIDE_GENERATION_FAILED, generation=1, attempts=1)
        self.assertIsNone(slide["image_path"], "garbage at the output path must not be adopted")
        self.assertIsNone(sniff_image(garbage))

    def test_retry_produces_a_valid_image(self):
        self.retry("slide_03")
        outcome = self.dispatch("slide_03")
        self.assertEqual(outcome.status, "completed")
        self.assert_slide("slide_03", SLIDE_GENERATED, generation=2, attempts=2)
        image = self.assert_valid_final_image("slide_03")
        self.assertIsNotNone(sniff_image(image))
        self.assertEqual(
            self.state.slide("slide_03")["attempts"][0]["error_code"], FAULT_OUTPUT_INVALID
        )

    def test_state_survives_reload(self):
        self.reload()
        slide = self.assert_slide("slide_03", SLIDE_GENERATION_FAILED, generation=1, attempts=1)
        self.assertIsNone(slide["image_path"])
        self.assertEqual((slide["blocker"] or {}).get("error_code"), FAULT_OUTPUT_INVALID)


class InvalidOutputMatrixTests(RecoveryTestCase):
    """Table-driven row: ``IMAGE_OUTPUT_INVALID`` -> not generated."""


attach_matrix_tests(InvalidOutputMatrixTests, (FAULT_OUTPUT_INVALID,))


if __name__ == "__main__":
    unittest.main()

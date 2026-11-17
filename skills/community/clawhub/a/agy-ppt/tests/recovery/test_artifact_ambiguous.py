#!/usr/bin/env python3
"""Recovery scenario 3: two or more candidate artifacts (ambiguous).

The render turn produced several plausible artifacts, so the adapter refuses to
guess and returns ``IMAGE_ARTIFACT_AMBIGUOUS`` with the candidate list.

Contract under test:

* nothing picks an artifact automatically (not newest, not largest, not by name)
* the slide never reaches ``generated`` and gets no ``image_path``
* the candidate list survives in the attempt diagnostics, across a reload, so
  AGY can inspect it
* no candidate is copied into the deck's ``origin_image/`` output path
* AGY can re-dispatch generation, and the clean second turn produces exactly one
  final image
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

TESTS_DIR = Path(__file__).resolve().parents[1]
if str(TESTS_DIR) not in sys.path:
    sys.path.insert(0, str(TESTS_DIR))

from helpers.fault_matrix import attach_matrix_tests  # noqa: E402
from helpers.fake_image_worker import FAULT_ARTIFACT_AMBIGUOUS  # noqa: E402
from helpers.recovery_deck import (  # noqa: E402
    SLIDE_GENERATED,
    SLIDE_GENERATION_FAILED,
    RecoveryTestCase,
)


class ArtifactAmbiguousTests(RecoveryTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.advance_to_slide_generation()
        self.dispatch("slide_01")
        self.settled_before = self.snapshot(["slide_01"])
        self.worker.set_plan(
            "slide_03",
            fault=FAULT_ARTIFACT_AMBIGUOUS,
            succeed_on=2,
            ambiguous_count=3,
        )
        self.outcome = self.dispatch("slide_03")

    def _discovery(self) -> dict:
        attempt = self.state.slide("slide_03")["attempts"][0]
        return (attempt.get("diagnostics") or {}).get("artifact_discovery") or {}

    def test_error_code_is_ambiguous(self):
        self.assertEqual(self.outcome.error_code, FAULT_ARTIFACT_AMBIGUOUS)

    def test_slide_does_not_enter_generated(self):
        self.assert_slide("slide_03", SLIDE_GENERATION_FAILED, generation=1, attempts=1)
        self.assert_not_generated("slide_03")
        self.assertIsNone(self.state.slide("slide_03")["image_path"])

    def test_no_artifact_is_auto_selected_into_the_deck(self):
        output_dir = self.ws / "origin_image"
        produced = sorted(p.name for p in output_dir.glob("*.png"))
        self.assertEqual(produced, ["slide_01.png"], "an ambiguous candidate leaked into the deck")

    def test_candidates_are_preserved_in_diagnostics(self):
        discovery = self._discovery()
        self.assertTrue(discovery.get("ambiguous"))
        self.assertEqual(len(discovery.get("candidates") or []), 3)
        for candidate in discovery["candidates"]:
            self.assertTrue((self.ws / candidate).is_file(), f"missing candidate {candidate}")

    def test_candidates_survive_reload(self):
        self.reload()
        discovery = self._discovery()
        self.assertEqual(len(discovery.get("candidates") or []), 3)
        self.assertTrue(discovery.get("ambiguous"))

    def test_agy_can_redispatch_generation(self):
        self.retry("slide_03")
        outcome = self.dispatch("slide_03")
        self.assertEqual(outcome.status, "completed")
        self.assert_slide("slide_03", SLIDE_GENERATED, generation=2, attempts=2)
        image = self.assert_valid_final_image("slide_03")
        self.assertEqual(image, self.ws / "origin_image" / "slide_03.png")
        # The earlier ambiguity is still on the record.
        self.assertEqual(
            self.state.slide("slide_03")["attempts"][0]["error_code"], FAULT_ARTIFACT_AMBIGUOUS
        )

    def test_other_slides_unaffected(self):
        self.assert_untouched(["slide_01"], self.settled_before)


class ArtifactAmbiguousMatrixTests(RecoveryTestCase):
    """Table-driven row: ``IMAGE_ARTIFACT_AMBIGUOUS`` -> not generated."""


attach_matrix_tests(ArtifactAmbiguousMatrixTests, (FAULT_ARTIFACT_AMBIGUOUS,))


if __name__ == "__main__":
    unittest.main()

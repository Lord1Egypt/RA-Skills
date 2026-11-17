#!/usr/bin/env python3
"""Phase 16.4 Human Editorial Quality tests with mechanical fixtures."""

from __future__ import annotations

import hashlib
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from phase16_claims import Claim, ContentOrigin, binding_from_unit  # noqa: E402
from phase16_editorial import (  # noqa: E402
    EDITORIAL_REVIEW_RECOMMENDED,
    ERROR_REPAIR_LIMIT,
    EditorialError,
    EditorialSession,
    EditorialSlide,
    PresentationMode,
    SlideRole,
    apply_headline_pass,
    lint_editorial,
    mode_guidance,
    user_facing_editorial_message,
)
from phase16_slide_evidence import MaterialClaim, SlideEvidencePlan  # noqa: E402
from source_grounding import SourceInventory  # noqa: E402


def mechanical_slides(count=5):
    roles = (SlideRole.HERO, SlideRole.CASE, SlideRole.DATA, SlideRole.COMPARISON, SlideRole.QUOTE)
    return tuple(
        EditorialSlide(
            f"slide_{index:02d}",
            "打造賦能共贏的全方位核心價值與關鍵引擎策略藍圖" * 2,
            ("我們將打造核心價值", "我們將賦能高效成長", "我們將深化共贏"),
            "接下來我們來看，這是固定的轉場。",
            roles[(index - 1) % len(roles)],
            "cards-3",
            "right",
            "DENSE",
        )
        for index in range(1, count + 1)
    )


class EditorialTests(unittest.TestCase):
    def test_repetitive_jargon_is_signal_not_blacklist(self):
        report = lint_editorial(mechanical_slides(), PresentationMode.EXECUTIVE)
        self.assertGreater(report.count("COPY_REPETITION"), 0)
        one = EditorialSlide("slide_01", "打造未來", ("清楚說明",), "自然講稿")
        self.assertEqual(lint_editorial([one], PresentationMode.EXECUTIVE).count("COPY_REPETITION"), 0)

    def test_repeated_sentence_template(self):
        self.assertGreater(lint_editorial(mechanical_slides(), PresentationMode.SALES).count("REPEATED_SENTENCE_TEMPLATE"), 0)

    def test_excessively_long_headlines(self):
        self.assertEqual(lint_editorial(mechanical_slides(1), PresentationMode.EXECUTIVE).count("HEADLINE_TOO_LONG"), 1)

    def test_five_consecutive_three_card_layouts(self):
        self.assertEqual(lint_editorial(mechanical_slides(), PresentationMode.SALES).count("REPEATED_THREE_CARD_LAYOUT"), 1)

    def test_identical_bullet_counts_warn(self):
        self.assertEqual(lint_editorial(mechanical_slides(), PresentationMode.SALES).count("UNIFORM_BULLET_COUNT"), 1)

    def test_uniform_dense_deck_warns(self):
        self.assertEqual(lint_editorial(mechanical_slides(), PresentationMode.TECHNICAL).count("UNIFORM_INFORMATION_DENSITY"), 1)

    def test_mechanical_speaker_notes_warn(self):
        self.assertEqual(lint_editorial(mechanical_slides(), PresentationMode.SALES).count("MECHANICAL_SPEAKER_NOTES"), 1)

    def test_mode_differences_are_explicit(self):
        self.assertNotEqual(mode_guidance(PresentationMode.EXECUTIVE), mode_guidance(PresentationMode.SALES))
        self.assertNotEqual(mode_guidance(PresentationMode.SALES), mode_guidance(PresentationMode.TECHNICAL))
        title = "T" * 60
        slide = EditorialSlide("slide_01", title, ("body",), "notes")
        self.assertEqual(lint_editorial([slide], PresentationMode.EXECUTIVE).count("HEADLINE_TOO_LONG"), 1)
        self.assertEqual(lint_editorial([slide], PresentationMode.TECHNICAL).count("HEADLINE_TOO_LONG"), 0)

    def test_headline_pass_uses_agy_proposal(self):
        slide = EditorialSlide("slide_01", "年度營運成果之整體分析報告", ("body",), "notes")
        updated = apply_headline_pass(slide, PresentationMode.EXECUTIVE, "成長來自留存改善")
        self.assertEqual(updated.title, "成長來自留存改善")

    def test_editorial_repair_preserves_evidence_numbers_and_origin(self):
        with tempfile.TemporaryDirectory() as temp:
            inv = SourceInventory.initialize(temp, "editorial")
            digest = hashlib.sha256(b"source").hexdigest()
            inv.add_source("src_report", "pdf", source_digest=digest)
            unit = inv.add_unit("src_report", "page", {"kind": "page", "start": 1, "end": 1}, "HIGH")
            claim = Claim.create(inv, "Revenue rose 18% in 2025", ContentOrigin.SOURCE_GROUNDED, [binding_from_unit(inv, unit["unit_id"])])
            evidence = SlideEvidencePlan.create("slide_01", [MaterialClaim(claim)])
            slide = EditorialSlide("slide_01", "Revenue rose 18% in 2025", ("Evidence-led growth",), "在這一頁，說明結果", SlideRole.DATA, "cards-3", "right", "DENSE", evidence)
            repaired = EditorialSession(PresentationMode.EXECUTIVE, (slide,)).repair_once().slides[0]
            self.assertIn("18%", repaired.copy)
            self.assertIn("2025", repaired.copy)
            self.assertIs(repaired.evidence_plan, evidence)
            self.assertEqual(repaired.evidence_plan.claims[0].claim.origin, ContentOrigin.SOURCE_GROUNDED)

    def test_one_repair_maximum(self):
        session = EditorialSession(PresentationMode.SALES, mechanical_slides()).repair_once()
        with self.assertRaises(EditorialError) as caught:
            session.repair_once()
        self.assertEqual(caught.exception.error_code, ERROR_REPAIR_LIMIT)

    def test_warnings_never_become_fake_ai_detection(self):
        report = lint_editorial(mechanical_slides(), PresentationMode.SALES)
        self.assertEqual(report.status, EDITORIAL_REVIEW_RECOMMENDED)
        self.assertNotIn("AI_DETECTED", str(report))
        self.assertNotIn("probability", str(report).lower())

    def test_user_facing_ux_hides_lint_internals(self):
        text = user_facing_editorial_message()
        for token in ("EDITORIAL_REVIEW_RECOMMENDED", "COPY_REPETITION", "layout_family", "AI_DETECTED"):
            self.assertNotIn(token, text)

    def test_mechanical_fixture_improves_after_one_repair(self):
        session = EditorialSession(PresentationMode.SALES, mechanical_slides())
        before = session.lint()
        repaired = session.repair_once()
        after = repaired.lint()
        self.assertEqual(repaired.repair_count, 1)
        self.assertLess(after.count(), before.count())


if __name__ == "__main__":
    unittest.main()

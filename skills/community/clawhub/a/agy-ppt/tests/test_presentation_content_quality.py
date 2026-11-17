#!/usr/bin/env python3
"""Regression fixtures distilled from Q3 bounded Jev classifications."""

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
from phase16_editorial import PresentationMode  # noqa: E402
from phase16_slide_evidence import MaterialClaim, SlideEvidencePlan  # noqa: E402
from phase17_narrative import NarrativeRole  # noqa: E402
from presentation_content_quality import (  # noqa: E402
    ContentQualityCode,
    ContentQualitySlide,
    ContentQualityStatus,
    HeadlineKind,
    audit_presentation_content,
    classify_headline_shape,
    user_facing_content_quality_message,
)
from source_grounding import SourceInventory  # noqa: E402


def slide(title, points=(), role=None, evidence=None, number=1):
    return ContentQualitySlide(f"slide_{number:02d}", title, tuple(points), role, evidence_plan=evidence)


class PresentationContentQualityTests(unittest.TestCase):
    def test_headline_expression_fixture_classes(self):
        cases = {
            "核心績效指標": HeadlineKind.LABEL_ONLY,
            "Q3 成長主要來自續約率提升": HeadlineKind.ASSERTION,
            "我們該如何提高續約率？": HeadlineKind.QUESTION,
            "現在要決定：是否投資續約自動化": HeadlineKind.DECISION_FRAME,
            "本週先選一個高摩擦服務節點開始": HeadlineKind.ACTION_FRAME,
        }
        for text, expected in cases.items():
            with self.subTest(text=text):
                self.assertEqual(classify_headline_shape(text), expected)

    def test_label_only_evidence_headline_requires_review(self):
        report = audit_presentation_content(
            (slide("核心績效指標", ("續約率",), NarrativeRole.EVIDENCE),),
            PresentationMode.EXECUTIVE,
        )
        self.assertEqual(report.status, ContentQualityStatus.REVIEW_REQUIRED)
        self.assertEqual(report.count(ContentQualityCode.LABEL_ONLY_HEADLINE), 1)

    def test_generic_schema_fill_copy_requires_repair_without_keyword_ban(self):
        report = audit_presentation_content((slide(
            "核心績效指標",
            ("我們將打造核心價值", "我們將賦能高效成長", "我們將深化共贏"),
            NarrativeRole.EVIDENCE,
        ),), PresentationMode.EXECUTIVE)
        self.assertEqual(report.count(ContentQualityCode.GENERIC_LANGUAGE), 1)
        specific = audit_presentation_content((slide("打造試點", ("本週完成一個試點",), NarrativeRole.ACTION),), PresentationMode.EXECUTIVE)
        self.assertEqual(specific.count(ContentQualityCode.GENERIC_LANGUAGE), 0)

    def test_supported_assertion_passes_and_evidence_identity_is_unchanged(self):
        with tempfile.TemporaryDirectory() as temp:
            inventory = SourceInventory.initialize(temp, "content-quality")
            digest = hashlib.sha256(b"source").hexdigest()
            inventory.add_source("src_report", "pdf", source_digest=digest)
            unit = inventory.add_unit("src_report", "page", {"kind": "page", "start": 1, "end": 1}, "HIGH")
            claim = Claim.create(
                inventory,
                "Q3 續約貢獻 72%，新客貢獻 28%",
                ContentOrigin.SOURCE_GROUNDED,
                (binding_from_unit(inventory, unit["unit_id"]),),
            )
            evidence = SlideEvidencePlan.create("slide_01", (MaterialClaim(claim),))
            original_id = evidence.plan_id
            report = audit_presentation_content((slide(
                "Q3 成長主要來自續約率提升",
                ("Q3 續約貢獻 72%，新客貢獻 28%",),
                NarrativeRole.EVIDENCE,
                evidence,
            ),), PresentationMode.EXECUTIVE)
            self.assertEqual(report.status, ContentQualityStatus.PASS)
            self.assertEqual(evidence.plan_id, original_id)

    def test_unsupported_numeric_expansion_blocks(self):
        with tempfile.TemporaryDirectory() as temp:
            inventory = SourceInventory.initialize(temp, "unsupported")
            digest = hashlib.sha256(b"source").hexdigest()
            inventory.add_source("src_report", "pdf", source_digest=digest)
            unit = inventory.add_unit("src_report", "page", {"kind": "page", "start": 1, "end": 1}, "HIGH")
            claim = Claim.create(
                inventory, "Q3 成長 12%", ContentOrigin.SOURCE_GROUNDED,
                (binding_from_unit(inventory, unit["unit_id"]),),
            )
            evidence = SlideEvidencePlan.create("slide_01", (MaterialClaim(claim),))
            report = audit_presentation_content((slide(
                "Q3 成長 18%", ("Q3 成長 18%",), NarrativeRole.EVIDENCE, evidence,
            ),), PresentationMode.EXECUTIVE)
            self.assertEqual(report.status, ContentQualityStatus.BLOCK)
            self.assertEqual(report.count(ContentQualityCode.EVIDENCE_INTEGRITY_BLOCK), 1)

    def test_action_role_requires_action_expression(self):
        bad = audit_presentation_content((slide("市場背景", ("產業概況",), NarrativeRole.ACTION),), PresentationMode.SALES)
        good = audit_presentation_content((slide("本週先確認試點", ("選定一個服務節點",), NarrativeRole.ACTION),), PresentationMode.SALES)
        self.assertEqual(bad.count(ContentQualityCode.NARRATIVE_COPY_MISALIGNED), 1)
        self.assertEqual(good.count(ContentQualityCode.NARRATIVE_COPY_MISALIGNED), 0)

    def test_case_with_label_title_is_review_not_block(self):
        report = audit_presentation_content((slide("案例分析", ("客戶重複詢問相同問題",), NarrativeRole.CASE),), PresentationMode.SALES)
        self.assertEqual(report.status, ContentQualityStatus.REVIEW_REQUIRED)
        self.assertEqual(report.count(ContentQualityCode.LABEL_ONLY_HEADLINE), 1)

    def test_mode_aware_density_envelope(self):
        points = tuple(f"point {index} with detailed implementation context" for index in range(6))
        executive = audit_presentation_content((slide("Six implementation constraints shape the decision", points, NarrativeRole.EXPLANATION),), PresentationMode.EXECUTIVE)
        technical = audit_presentation_content((slide("Six implementation constraints shape the decision", points, NarrativeRole.EXPLANATION),), PresentationMode.TECHNICAL)
        self.assertEqual(executive.count(ContentQualityCode.CONTENT_DENSITY), 1)
        self.assertEqual(technical.count(ContentQualityCode.CONTENT_DENSITY), 0)

    def test_repeated_headlines_are_detected_without_rewriting(self):
        first = slide("The same point", ("A",), NarrativeRole.CONTEXT, number=1)
        second = slide("The same point", ("B",), NarrativeRole.INSIGHT, number=2)
        report = audit_presentation_content((first, second), PresentationMode.EXECUTIVE)
        self.assertEqual(report.count(ContentQualityCode.REPETITIVE_COPY), 1)
        self.assertEqual(first.title, second.title)

    def test_user_message_hides_internal_findings(self):
        report = audit_presentation_content((slide("One supported point", ("Clear context",), NarrativeRole.INSIGHT),), PresentationMode.EXECUTIVE)
        message = user_facing_content_quality_message(report)
        for token in ("LABEL_ONLY_HEADLINE", "NARRATIVE_COPY_MISALIGNED", "ContentQualityStatus"):
            self.assertNotIn(token, message)


if __name__ == "__main__":
    unittest.main()

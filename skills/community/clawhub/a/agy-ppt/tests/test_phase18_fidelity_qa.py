#!/usr/bin/env python3
"""Phase 18.4 portability and fidelity QA tests."""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from phase18_contract import DeliveryEditabilityContract, EditabilityClass, FontPortability, ProductionStrategy  # noqa: E402
from phase18_fidelity_qa import (  # noqa: E402
    ElementSnapshot, FidelityIssue, QaDimension, QaSeverity, compare_fidelity,
    safe_representation_fallback, verify_pptx_package,
)
from phase18_hybrid_pptx import (  # noqa: E402
    ElementBox, HybridElement, HybridSlide, TextStyle, create_hybrid_presentation,
)
from phase18_production_plan import ElementProductionPlan, ElementRole, PortabilityRisk  # noqa: E402


def snap(**overrides):
    values = {
        "element_id": "kpi",
        "content": "18%",
        "box": ElementBox(1, 1, 3, 1),
        "font_name": "Arial",
        "line_count": 1,
        "crop": (0, 0, 0, 0),
        "z_order": 2,
        "chart_style": "brand-column",
        "color": "112233",
        "prominence": 3,
        "editable": True,
        "evidence_bound": True,
    }
    values.update(overrides)
    return ElementSnapshot(**values)


def plan():
    return ElementProductionPlan(
        "ep:kpi", "kpi", "claim:kpi", "narrative:kpi", "18%", ("pc:evidence",),
        ElementRole.KPI, PortabilityRisk.LOW,
        DeliveryEditabilityContract(EditabilityClass.EDITABLE_REQUIRED, ProductionStrategy.NATIVE_TEXT, FontPortability.FONT_SAFE),
    )


class Phase18FidelityQaTests(unittest.TestCase):
    def test_exact_content_with_slight_layout_drift_is_accepted(self):
        report = compare_fidelity((snap(),), (snap(box=ElementBox(1.03, 1, 3, 1), line_count=2),))
        self.assertEqual(report.status, QaSeverity.ACCEPTABLE)
        self.assertEqual(report.count(FidelityIssue.LINE_BREAK_DRIFT), 1)

    def test_changed_evidence_number_is_blocking(self):
        report = compare_fidelity((snap(),), (snap(content="1.8%"),))
        self.assertEqual(report.status, QaSeverity.BLOCKING)
        self.assertIn("evidence-bound", report.findings[0].detail)

    def test_text_overflow_requires_review(self):
        self.assertEqual(compare_fidelity((snap(),), (snap(overflow=True),)).status, QaSeverity.REVIEW_REQUIRED)

    def test_missing_glyph_is_blocking(self):
        report = compare_fidelity((snap(),), (snap(glyphs_present=False),))
        self.assertEqual(report.count(FidelityIssue.MISSING_GLYPH), 1)
        self.assertEqual(report.status, QaSeverity.BLOCKING)

    def test_font_substitution_is_a_specific_warning(self):
        report = compare_fidelity((snap(),), (snap(font_name="Arial Unicode MS"),))
        self.assertEqual(report.count(FidelityIssue.FONT_SUBSTITUTION), 1)
        self.assertEqual(report.status, QaSeverity.WARNING)

    def test_material_line_break_and_reflow_drift(self):
        report = compare_fidelity((snap(),), (snap(line_count=4),))
        self.assertEqual(report.count(FidelityIssue.LINE_BREAK_DRIFT), 1)
        self.assertEqual(report.count(FidelityIssue.TEXT_REFLOW), 1)

    def test_object_shift_requires_review(self):
        report = compare_fidelity((snap(),), (snap(box=ElementBox(1.2, 1, 3, 1)),))
        self.assertEqual(report.count(FidelityIssue.OBJECT_SHIFT), 1)

    def test_crop_drift_requires_review(self):
        report = compare_fidelity((snap(),), (snap(crop=(0.1, 0, 0, 0)),))
        self.assertEqual(report.count(FidelityIssue.IMAGE_CROP_DRIFT), 1)

    def test_z_order_drift_requires_review(self):
        report = compare_fidelity((snap(),), (snap(z_order=4),))
        self.assertEqual(report.count(FidelityIssue.Z_ORDER_CHANGE), 1)

    def test_chart_style_drift_warns(self):
        report = compare_fidelity((snap(),), (snap(chart_style="office-default"),))
        self.assertEqual(report.count(FidelityIssue.CHART_STYLE_DRIFT), 1)

    def test_color_drift_warns(self):
        report = compare_fidelity((snap(),), (snap(color="FFFFFF"),))
        self.assertEqual(report.count(FidelityIssue.COLOR_DRIFT), 1)

    def test_approved_sample_hierarchy_degradation_blocks(self):
        report = compare_fidelity((snap(),), (snap(prominence=1),), approved_sample=True)
        finding = next(item for item in report.findings if item.issue is FidelityIssue.HIERARCHY_DEGRADATION)
        self.assertEqual(finding.severity, QaSeverity.BLOCKING)

    def test_safe_fallback_locks_high_risk_native_representation(self):
        report = compare_fidelity((snap(),), (snap(overflow=True),))
        repaired = safe_representation_fallback(plan(), report)
        self.assertTrue(repaired.changed)
        self.assertEqual(repaired.plan.contract.strategy, ProductionStrategy.LOCKED_VISUAL)
        self.assertEqual(repaired.plan.approved_content, "18%")

    def test_content_failure_is_never_hidden_by_representation_fallback(self):
        report = compare_fidelity((snap(),), (snap(content="28%"),))
        self.assertFalse(safe_representation_fallback(plan(), report).changed)

    def test_missing_evidence_element_is_blocking(self):
        report = compare_fidelity((snap(),), (snap(element_id="other"),))
        self.assertEqual(report.status, QaSeverity.BLOCKING)
        finding = next(item for item in report.findings if item.element_id == "kpi")
        self.assertEqual(finding.issue, FidelityIssue.CONTENT_CHANGED)
        self.assertIn("evidence-bound", finding.detail)

    def test_element_outside_slide_bounds_requires_review(self):
        report = compare_fidelity((snap(),), (snap(box=ElementBox(12.0, 1.0, 3.0, 1.0)),))
        self.assertEqual(report.status, QaSeverity.REVIEW_REQUIRED)
        finding = next(item for item in report.findings if "outside slide bounds" in item.detail)
        self.assertEqual(finding.issue, FidelityIssue.TEXT_OVERFLOW)

    def test_verify_pptx_package_missing_or_corrupt(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            missing = Path(tmpdir) / "nonexistent.pptx"
            report_missing = verify_pptx_package(missing)
            self.assertEqual(report_missing.status, QaSeverity.BLOCKING)

            corrupt = Path(tmpdir) / "corrupt.pptx"
            corrupt.write_text("not a zip", encoding="utf-8")
            report_corrupt = verify_pptx_package(corrupt)
            self.assertEqual(report_corrupt.status, QaSeverity.BLOCKING)

    def test_verify_pptx_package_valid_and_notes_gate(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            deck_path = Path(tmpdir) / "valid.pptx"
            element = HybridElement(plan(), ElementBox(1.0, 1.0, 3.0, 1.0), text_style=TextStyle())
            slide = HybridSlide("slide_01", (element,), speaker_notes="Required speaker notes text")
            create_hybrid_presentation((slide,), str(deck_path))

            report_valid = verify_pptx_package(deck_path, required_notes_by_slide={0: "Required speaker notes text"})
            self.assertEqual(report_valid.status, QaSeverity.ACCEPTABLE)

            report_missing_notes = verify_pptx_package(deck_path, required_notes_by_slide={0: "Nonexistent notes"})
            self.assertEqual(report_missing_notes.status, QaSeverity.BLOCKING)
            self.assertEqual(report_missing_notes.count(FidelityIssue.CONTENT_CHANGED), 1)

    def test_repair_is_bounded_to_one_pass_and_report_has_no_score(self):
        report = compare_fidelity((snap(),), (snap(overflow=True),))
        self.assertFalse(safe_representation_fallback(plan(), report, repair_passes=1).changed)
        payload = report.canonical_json()
        self.assertNotIn("score", payload.casefold())
        self.assertEqual({finding.dimension for finding in report.findings}, {QaDimension.LAYOUT_INTEGRITY})
        self.assertEqual(payload, report.canonical_json())


if __name__ == "__main__":
    unittest.main()

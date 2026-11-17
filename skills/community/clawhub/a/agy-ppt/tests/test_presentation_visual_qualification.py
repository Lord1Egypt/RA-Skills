#!/usr/bin/env python3
"""Q4 exact-artifact visual qualification and escalation tests."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path


SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from human_presentation_quality import HumanPresentationQualityState, ReviewAuthority  # noqa: E402
from presentation_visual_qualification import (  # noqa: E402
    CardInformationDepth,
    CompositionAssessment,
    CompositionDensity,
    CompositionSignalFinding,
    CompositionSignals,
    EffectiveDensityAssessment,
    EffectiveDensitySignalFinding,
    EffectiveDensitySignals,
    ImageVariety,
    MaterialDegradation,
    OccupiedContentEnvelope,
    RenderArtifactEvidence,
    SemanticDensity,
    StageComparison,
    VisualDisposition,
    VisualAnchor,
    VisualIssue,
    VisualObservation,
    VisualStage,
    TextDensitySignal,
    VisualRoleExpectation,
    composition_signal_findings,
    disposition_from_observation,
    effective_density_signal_findings,
    qualify_visual_pipeline,
)
from presentation_workflow import SampleArtifact  # noqa: E402


PLATE = "1" * 64
HYBRID = "2" * 64
ACTUAL = "3" * 64
PPTX = "4" * 64


def artifacts():
    return (
        RenderArtifactEvidence("slide_02", VisualStage.RAW_PLATE, PLATE, PPTX, "agy-ppt plate renderer"),
        RenderArtifactEvidence("slide_02", VisualStage.HYBRID_PREVIEW, HYBRID, PPTX, "agy-ppt hybrid preview"),
        RenderArtifactEvidence("slide_02", VisualStage.ACTUAL_CLIENT_RENDER, ACTUAL, PPTX, "Microsoft PowerPoint for macOS", True),
    )


def sample(sha=HYBRID):
    return SampleArtifact("sample.pptx", {
        "artifact_kind": "HYBRID_PREVIEW",
        "rendered_preview_sha256": sha,
        "hybrid_manifest_sha256": "5" * 64,
    })


def comparison(reference, delivered, degradation, issue, disposition, detail="fixture comparison"):
    hashes = {VisualStage.RAW_PLATE: PLATE, VisualStage.HYBRID_PREVIEW: HYBRID, VisualStage.ACTUAL_CLIENT_RENDER: ACTUAL}
    return StageComparison(
        "slide_02", reference, delivered, hashes[reference], hashes[delivered],
        degradation, issue, disposition, detail,
    )


def good_comparisons():
    return (
        comparison(VisualStage.RAW_PLATE, VisualStage.HYBRID_PREVIEW, MaterialDegradation.NO_MATERIAL_DEGRADATION, VisualIssue.OTHER, VisualDisposition.ACCEPT),
        comparison(VisualStage.HYBRID_PREVIEW, VisualStage.ACTUAL_CLIENT_RENDER, MaterialDegradation.MINOR_DRIFT, VisualIssue.REFLOW, VisualDisposition.WARNING),
    )


class PresentationVisualQualificationTests(unittest.TestCase):
    def test_semantic_number_change_blocks(self):
        observation = VisualObservation(VisualIssue.OTHER, semantic_content_changed=True)
        self.assertEqual(disposition_from_observation(observation), VisualDisposition.BLOCK)

    def test_clipped_core_title_blocks(self):
        observation = VisualObservation(VisualIssue.OVERFLOW, core_content_obscured=True)
        self.assertEqual(disposition_from_observation(observation), VisualDisposition.BLOCK)

    def test_subject_losing_crop_requires_repair(self):
        observation = VisualObservation(VisualIssue.CROP, repairable_degradation=True)
        self.assertEqual(disposition_from_observation(observation), VisualDisposition.REPAIR)

    def test_harmless_wrap_and_small_shift_are_accepted(self):
        for issue in (VisualIssue.REFLOW, VisualIssue.POSITION, VisualIssue.COLOR):
            with self.subTest(issue=issue):
                observation = VisualObservation(issue, bounded_harmless_drift=True)
                self.assertEqual(disposition_from_observation(observation), VisualDisposition.ACCEPT)

    def test_approved_hierarchy_floor_violation_blocks(self):
        observation = VisualObservation(VisualIssue.HIERARCHY, approved_quality_floor_violated=True)
        self.assertEqual(disposition_from_observation(observation), VisualDisposition.BLOCK)

    def test_default_chart_degradation_requires_repair(self):
        observation = VisualObservation(VisualIssue.CHART, repairable_degradation=True)
        self.assertEqual(disposition_from_observation(observation), VisualDisposition.REPAIR)

    def test_core_z_order_overlap_blocks(self):
        observation = VisualObservation(VisualIssue.Z_ORDER, core_content_obscured=True)
        self.assertEqual(disposition_from_observation(observation), VisualDisposition.BLOCK)

    def test_no_material_degradation_still_requires_human_review(self):
        report = qualify_visual_pipeline(artifacts(), good_comparisons(), approved_sample=sample())
        self.assertEqual(report.disposition, VisualDisposition.WARNING)
        self.assertIsNone(report.earliest_material_loss)
        self.assertTrue(report.requires_human_review)
        self.assertEqual(report.automated_human_gate.state, HumanPresentationQualityState.REVIEW_REQUIRED)
        self.assertEqual(report.automated_human_gate.authority, ReviewAuthority.AUTOMATED_ASSISTANCE)

    def test_hybrid_reconstruction_loss_is_localized(self):
        report = qualify_visual_pipeline(artifacts(), (
            comparison(VisualStage.RAW_PLATE, VisualStage.HYBRID_PREVIEW, MaterialDegradation.MATERIAL_DEGRADATION, VisualIssue.HIERARCHY, VisualDisposition.REPAIR),
            comparison(VisualStage.HYBRID_PREVIEW, VisualStage.ACTUAL_CLIENT_RENDER, MaterialDegradation.NO_MATERIAL_DEGRADATION, VisualIssue.OTHER, VisualDisposition.ACCEPT),
        ), approved_sample=sample())
        self.assertEqual(report.earliest_material_loss, VisualStage.HYBRID_PREVIEW)
        self.assertEqual(report.disposition, VisualDisposition.REPAIR)

    def test_actual_client_loss_is_localized(self):
        report = qualify_visual_pipeline(artifacts(), (
            comparison(VisualStage.RAW_PLATE, VisualStage.HYBRID_PREVIEW, MaterialDegradation.NO_MATERIAL_DEGRADATION, VisualIssue.OTHER, VisualDisposition.ACCEPT),
            comparison(VisualStage.HYBRID_PREVIEW, VisualStage.ACTUAL_CLIENT_RENDER, MaterialDegradation.UNACCEPTABLE, VisualIssue.OVERFLOW, VisualDisposition.BLOCK),
        ), approved_sample=sample())
        self.assertEqual(report.earliest_material_loss, VisualStage.ACTUAL_CLIENT_RENDER)
        self.assertEqual(report.automated_human_gate.state, HumanPresentationQualityState.BLOCK)

    def test_sample_must_be_exact_hybrid_preview(self):
        with self.assertRaises(ValueError):
            qualify_visual_pipeline(artifacts(), good_comparisons(), approved_sample=sample("9" * 64))

    def test_raw_plate_cannot_masquerade_as_sample(self):
        bad = SampleArtifact("plate.png", {"artifact_kind": "RAW_PLATE", "rendered_preview_sha256": HYBRID})
        with self.assertRaises(ValueError):
            qualify_visual_pipeline(artifacts(), good_comparisons(), approved_sample=bad)

    def test_actual_client_evidence_cannot_be_claimed_by_proxy(self):
        with self.assertRaises(ValueError):
            RenderArtifactEvidence("slide_02", VisualStage.ACTUAL_CLIENT_RENDER, ACTUAL, PPTX, "structural proxy", False)

    def test_comparison_hash_must_match_recorded_artifact(self):
        bad = StageComparison(
            "slide_02", VisualStage.RAW_PLATE, VisualStage.HYBRID_PREVIEW,
            "9" * 64, HYBRID, MaterialDegradation.MINOR_DRIFT,
            VisualIssue.COLOR, VisualDisposition.WARNING, "wrong reference",
        )
        with self.assertRaises(ValueError):
            qualify_visual_pipeline(artifacts(), (bad, good_comparisons()[1]), approved_sample=sample())

    def test_cross_slide_comparison_fails_closed(self):
        bad = comparison(
            VisualStage.RAW_PLATE, VisualStage.HYBRID_PREVIEW,
            MaterialDegradation.MINOR_DRIFT, VisualIssue.POSITION, VisualDisposition.WARNING,
        )
        object.__setattr__(bad, "slide_id", "slide_03")
        with self.assertRaises(ValueError):
            qualify_visual_pipeline(artifacts(), (bad, good_comparisons()[1]), approved_sample=sample())

    def test_report_contains_no_beauty_score(self):
        report = qualify_visual_pipeline(artifacts(), good_comparisons(), approved_sample=sample())
        self.assertFalse(hasattr(report, "score"))
        self.assertFalse(hasattr(report, "percentage"))

    def test_contradictory_harmless_and_blocking_observation_fails(self):
        with self.assertRaises(ValueError):
            VisualObservation(
                VisualIssue.HIERARCHY,
                approved_quality_floor_violated=True,
                bounded_harmless_drift=True,
            )

    def test_both_stage_comparisons_are_required(self):
        with self.assertRaises(ValueError):
            qualify_visual_pipeline(artifacts(), (good_comparisons()[0],), approved_sample=sample())


class PresentationCompositionQualificationTests(unittest.TestCase):
    def signals(
        self,
        *,
        objects=4,
        envelope=(0.08, 0.12, 0.92, 0.88),
        levels=2,
        hero=False,
        anchor=False,
        text=TextDensitySignal.MODERATE,
        role=VisualRoleExpectation.OTHER,
        groups=0,
    ):
        return CompositionSignals(
            objects,
            OccupiedContentEnvelope(*envelope),
            levels,
            hero,
            anchor,
            text,
            role,
            groups,
        )

    def test_regression_cover_is_underfilled_with_weak_anchor(self):
        signals = self.signals(
            objects=3,
            envelope=(0.08, 0.20, 0.92, 0.70),
            hero=False,
            anchor=False,
            text=TextDensitySignal.LOW,
            role=VisualRoleExpectation.COVER_HERO,
        )
        assessment = CompositionAssessment(
            "slide_01", "a" * 64, CompositionDensity.UNDERFILLED,
            VisualAnchor.WEAK, signals,
            "Human-reviewed cover lacks an intentional hero structure.",
        )
        findings = composition_signal_findings(assessment.signals)
        self.assertIn(CompositionSignalFinding.MISSING_HERO_VISUAL, findings)
        self.assertIn(CompositionSignalFinding.MISSING_PRIMARY_ANCHOR, findings)

    def test_regression_slide_two_is_balanced_reference(self):
        signals = self.signals(
            objects=7,
            levels=3,
            anchor=True,
            role=VisualRoleExpectation.BALANCED_EVIDENCE,
            groups=3,
        )
        assessment = CompositionAssessment(
            "slide_02", "b" * 64, CompositionDensity.BALANCED,
            VisualAnchor.STRONG, signals,
            "KPI and native chart establish a balanced reference composition.",
        )
        self.assertEqual(assessment.density, CompositionDensity.BALANCED)
        self.assertNotIn(
            CompositionSignalFinding.MISSING_PRIMARY_ANCHOR,
            composition_signal_findings(signals),
        )

    def test_regression_image_slide_requires_structured_takeaways(self):
        signals = self.signals(
            objects=3,
            levels=2,
            hero=True,
            text=TextDensitySignal.LOW,
            role=VisualRoleExpectation.IMAGE_WITH_TAKEAWAYS,
            groups=1,
        )
        findings = composition_signal_findings(signals)
        self.assertIn(CompositionSignalFinding.LOW_TEXT_DENSITY_FOR_ROLE, findings)
        self.assertIn(CompositionSignalFinding.ROLE_STRUCTURE_MISSING, findings)

    def test_regression_cta_sentence_requires_three_step_structure(self):
        signals = self.signals(
            objects=3,
            levels=2,
            text=TextDensitySignal.LOW,
            role=VisualRoleExpectation.ACTION_FLOW,
            groups=1,
        )
        findings = composition_signal_findings(signals)
        self.assertIn(CompositionSignalFinding.MISSING_PRIMARY_ANCHOR, findings)
        self.assertIn(CompositionSignalFinding.ROLE_STRUCTURE_MISSING, findings)

    def test_empty_area_cannot_be_the_sole_composition_rule(self):
        envelope = (0.10, 0.15, 0.90, 0.72)
        intentional = self.signals(
            objects=2, envelope=envelope, hero=True,
            role=VisualRoleExpectation.COVER_HERO,
        )
        underfilled = self.signals(
            objects=2, envelope=envelope, hero=False,
            role=VisualRoleExpectation.COVER_HERO,
        )
        self.assertEqual(
            intentional.occupied_content_envelope,
            underfilled.occupied_content_envelope,
        )
        self.assertNotIn(
            CompositionSignalFinding.MISSING_HERO_VISUAL,
            composition_signal_findings(intentional),
        )
        self.assertIn(
            CompositionSignalFinding.MISSING_HERO_VISUAL,
            composition_signal_findings(underfilled),
        )

    def test_composition_assessment_has_no_aesthetic_score(self):
        assessment = CompositionAssessment(
            "slide_01", "c" * 64, CompositionDensity.INTENTIONAL_MINIMAL,
            VisualAnchor.STRONG,
            self.signals(objects=2, hero=True, role=VisualRoleExpectation.COVER_HERO),
            "Minimal composition remains intentional because the hero anchor is strong.",
        )
        self.assertFalse(hasattr(assessment, "score"))
        self.assertFalse(hasattr(assessment, "empty_area_percentage"))

    def test_invalid_envelope_fails_closed(self):
        with self.assertRaises(ValueError):
            OccupiedContentEnvelope(0.8, 0.1, 0.2, 0.9)


class EffectiveDensityQualificationTests(unittest.TestCase):
    def signals(
        self,
        *,
        cards=3,
        labels=0,
        supporting=3,
        substantive=0,
        distinct=1,
        related=0,
        duplicate=0,
        decorative=0,
        semantic_units=6,
        role=VisualRoleExpectation.BALANCED_EVIDENCE,
        supporting_layer=True,
    ):
        return EffectiveDensitySignals(
            cards, labels, supporting, substantive,
            distinct, related, duplicate, decorative,
            semantic_units, 3, role, supporting_layer,
        )

    def test_numerous_label_only_cards_do_not_count_as_effective_density(self):
        signals = self.signals(cards=3, labels=3, supporting=0, semantic_units=3, supporting_layer=False)
        findings = effective_density_signal_findings(signals)
        self.assertIn(EffectiveDensitySignalFinding.LABEL_ONLY_CARD_PRESENT, findings)
        self.assertIn(EffectiveDensitySignalFinding.CARD_SUPPORTING_LAYER_MISSING, findings)
        self.assertIn(EffectiveDensitySignalFinding.ROLE_SUPPORTING_LAYER_MISSING, findings)

    def test_duplicate_crops_do_not_count_as_image_variety(self):
        signals = self.signals(distinct=0, duplicate=3)
        findings = effective_density_signal_findings(signals)
        self.assertIn(EffectiveDensitySignalFinding.DUPLICATIVE_IMAGE_PRESENT, findings)
        self.assertIn(EffectiveDensitySignalFinding.IMAGE_VARIETY_MISSING, findings)

    def test_supporting_cards_and_distinct_visual_pass_structural_prompts(self):
        signals = self.signals(supporting=2, substantive=1, distinct=1, related=1)
        assessment = EffectiveDensityAssessment(
            "slide_03", "d" * 64, CardInformationDepth.SUPPORTING,
            ImageVariety.DISTINCT_INFORMATIONAL, SemanticDensity.HIGH,
            signals, "Cards carry supporting meaning and visuals have distinct informational roles.",
        )
        self.assertEqual(assessment.semantic_density, SemanticDensity.HIGH)
        self.assertEqual(effective_density_signal_findings(signals), ())
        self.assertFalse(hasattr(assessment, "score"))

    def test_cover_label_tags_do_not_trigger_content_card_rule(self):
        signals = self.signals(
            cards=3, labels=3, supporting=0, semantic_units=3,
            role=VisualRoleExpectation.COVER_HERO, supporting_layer=False,
        )
        findings = effective_density_signal_findings(signals)
        self.assertNotIn(EffectiveDensitySignalFinding.LABEL_ONLY_CARD_PRESENT, findings)
        self.assertNotIn(EffectiveDensitySignalFinding.ROLE_SUPPORTING_LAYER_MISSING, findings)

    def test_card_depth_counts_must_cover_all_cards(self):
        with self.assertRaises(ValueError):
            self.signals(cards=3, labels=1, supporting=1)


if __name__ == "__main__":
    unittest.main()

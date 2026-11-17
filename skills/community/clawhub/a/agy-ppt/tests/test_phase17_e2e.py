#!/usr/bin/env python3
"""Integrated deterministic Phase 17 qualification scenarios."""

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
from phase16_editorial import EDITORIAL_PASS, EditorialReport, PresentationMode, SlideRole  # noqa: E402
from phase16_outline import GroundedOutlinePlan, GroundedOutlineSlide, GroundedOutlineWorkflow  # noqa: E402
from phase16_traceability import FinalSlideRecord, build_traceability_report  # noqa: E402
from phase17_brief import BriefValue, DesiredOutcome, PresentationBrief, normalize_outcomes  # noqa: E402
from phase17_delivery import DeliveryNotes, DeliveryPlan, RehearsalCue, validate_timing  # noqa: E402
from phase17_effectiveness import ProposedChange, evaluate_effectiveness  # noqa: E402
from phase17_narrative import NarrativePlan, NarrativeRole, NarrativeSlide, NarrativeWorkflow  # noqa: E402
from phase17_visual_communication import (  # noqa: E402
    CommunicationObjective, HierarchyElement, HierarchyLevel, ImageIntent, ImagePurpose,
    InformationForm, VisualCommunicationPlan, VisualCommunicationSlide,
)
from presentation_workflow import PresentationApprovalWorkflow, ProjectState  # noqa: E402
from source_grounding import SourceInventory  # noqa: E402


class Phase17IntegratedE2E(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.inventory = SourceInventory.initialize(self.root / "sources", "phase17-e2e")
        digest = hashlib.sha256(b"Synthetic annual report: referrals improved 18% in 2025.").hexdigest()
        self.inventory.add_source("src_report", "pdf", label="Synthetic annual report", source_digest=digest)
        unit = self.inventory.add_unit("src_report", "page", {"kind": "page", "start": 2, "end": 2}, "HIGH")
        self.claim = Claim.create(self.inventory, "Referrals improved 18% in 2025", ContentOrigin.SOURCE_GROUNDED, (binding_from_unit(self.inventory, unit["unit_id"]),))

    def tearDown(self):
        self.temp.cleanup()

    def build(self, mode, duration, outcomes, roles, *, duplicate=False, gap=False, weak_close=False, generic=False, hierarchy=False, long_notes=False):
        brief = PresentationBrief(BriefValue(f"{mode.value.lower()} audience"), BriefValue("communicate an evidence-safe recommendation"), normalize_outcomes(outcomes), mode, duration_seconds=duration)
        outlines = []
        for index in range(1, len(roles) + 1):
            claims = (self.claim,) if index == 2 else ()
            outlines.append(GroundedOutlineSlide.create(index, f"Slide {index}", f"purpose {index}", claims))
        outline = GroundedOutlinePlan.create(outlines)
        narrative_slides = []
        for index, (base, role) in enumerate(zip(outline.slides, roles), 1):
            intent = "establish audience relevance" if index == 1 else f"advance {role.value.lower()}"
            if duplicate and index == 2:
                intent = "establish audience relevance"
            takeaway = self.claim.text if base.claims else f"{mode.value} takeaway {index}"
            transition = None if (gap and index == 1) or index == len(roles) else f"Connect takeaway {index} to intent {index + 1}"
            narrative_slides.append(NarrativeSlide.create(base, role, SlideRole.DATA if base.claims else SlideRole.STANDARD, intent, takeaway, f"job {index}", transition))
        closing = "Thank you" if weak_close else ("request a concrete next action" if DesiredOutcome.ACT in outcomes else "resolve the desired outcome")
        narrative = NarrativePlan.create(brief, outline, f"{mode.value} thesis", tuple(role.value for role in roles), "mode-appropriate opening", closing, narrative_slides)
        visuals = []
        for slide in narrative.slides:
            if slide.evidence_plan:
                objective, form, primary = CommunicationObjective.QUANTITATIVE_TREND, InformationForm.CHART, "18%"
            else:
                objective, form, primary = CommunicationObjective.SINGLE_MESSAGE, InformationForm.STATEMENT, "takeaway"
            image = ImageIntent(ImagePurpose.DECORATION, "generic business handshake", False, True) if generic else None
            visuals.append(VisualCommunicationSlide.create(
                slide, objective, form,
                (HierarchyElement(primary, HierarchyLevel.PRIMARY), HierarchyElement("support", HierarchyLevel.SUPPORTING)),
                image=image, observed_dominant_element="support" if hierarchy else None,
            ))
        visual = VisualCommunicationPlan.create(narrative, visuals)
        repeated = 110 if long_notes else 8
        notes = tuple(DeliveryNotes((f"Explain {slide.takeaway} with a practical example. " * repeated).strip(), transition=slide.transition_to_next) for slide in narrative.slides)
        delivery = DeliveryPlan.create(narrative, notes, tuple((RehearsalCue.PAUSE,) if slide.narrative_role in (NarrativeRole.INSIGHT, NarrativeRole.EVIDENCE) else () for slide in narrative.slides))
        evidence_slide = next(slide for slide in narrative.slides if slide.evidence_plan)
        record = FinalSlideRecord(evidence_slide.evidence_plan, evidence_slide.takeaway, delivery.slides[evidence_slide.number - 1].notes.natural_text())
        trace = build_traceability_report(self.inventory, (record,))
        report = evaluate_effectiveness(narrative, visual, delivery, trace, EditorialReport(EDITORIAL_PASS, ()))
        return brief, narrative, visual, delivery, trace, report

    def test_01_five_minute_bni_networking(self):
        roles = (NarrativeRole.OPEN, NarrativeRole.EVIDENCE, NarrativeRole.CASE, NarrativeRole.ACTION, NarrativeRole.CLOSE)
        brief, narrative, _, delivery, trace, report = self.build(PresentationMode.SALES, 300, (DesiredOutcome.KNOW, DesiredOutcome.REMEMBER, DesiredOutcome.ACT), roles)
        self.assertEqual(tuple(item.outcome for item in brief.desired_outcomes), (DesiredOutcome.KNOW, DesiredOutcome.REMEMBER, DesiredOutcome.ACT))
        self.assertIn("action", narrative.closing_strategy)
        self.assertEqual(sum(item.allocated_seconds for item in delivery.slides), 300)
        self.assertTrue(trace.evidence_complete and report.ready)

    def test_02_executive_decision_deck(self):
        roles = (NarrativeRole.OPEN, NarrativeRole.EVIDENCE, NarrativeRole.CONTRAST, NarrativeRole.DECISION)
        brief, narrative, _, delivery, _, report = self.build(PresentationMode.EXECUTIVE, 900, (DesiredOutcome.DECIDE,), roles)
        self.assertEqual(brief.mode, PresentationMode.EXECUTIVE)
        self.assertEqual(narrative.slides[-1].narrative_role, NarrativeRole.DECISION)
        self.assertEqual(sum(item.allocated_seconds for item in delivery.slides), 900)
        self.assertTrue(report.ready)

    def test_03_training_progression_and_time(self):
        roles = (NarrativeRole.OPEN, NarrativeRole.EXPLANATION, NarrativeRole.CASE, NarrativeRole.INSIGHT, NarrativeRole.CLOSE)
        _, narrative, _, delivery, _, report = self.build(PresentationMode.TRAINING, 1800, (DesiredOutcome.UNDERSTAND, DesiredOutcome.REMEMBER), roles)
        self.assertIn(NarrativeRole.CASE, tuple(item.narrative_role for item in narrative.slides))
        self.assertEqual(sum(item.allocated_seconds for item in delivery.slides), 1800)
        self.assertTrue(report.ready)

    def test_04_technical_precision(self):
        roles = (NarrativeRole.OPEN, NarrativeRole.EVIDENCE, NarrativeRole.EXPLANATION, NarrativeRole.RECOMMENDATION)
        brief, narrative, _, _, trace, _ = self.build(PresentationMode.TECHNICAL, 1200, (DesiredOutcome.UNDERSTAND, DesiredOutcome.DECIDE), roles)
        self.assertEqual(brief.mode, PresentationMode.TECHNICAL)
        self.assertEqual(narrative.slides[1].takeaway, "Referrals improved 18% in 2025")
        self.assertTrue(trace.evidence_complete)

    def test_05_same_evidence_different_audiences(self):
        sales = self.build(PresentationMode.SALES, 300, (DesiredOutcome.ACT,), (NarrativeRole.OPEN, NarrativeRole.EVIDENCE, NarrativeRole.ACTION))
        technical = self.build(PresentationMode.TECHNICAL, 900, (DesiredOutcome.UNDERSTAND,), (NarrativeRole.OPEN, NarrativeRole.EVIDENCE, NarrativeRole.EXPLANATION))
        self.assertEqual(sales[1].slides[1].evidence_plan.claims[0].claim.claim_id, technical[1].slides[1].evidence_plan.claims[0].claim.claim_id)
        self.assertNotEqual(sales[1].deck_thesis, technical[1].deck_thesis)
        self.assertNotEqual(sales[3].requested_duration_seconds, technical[3].requested_duration_seconds)

    def test_06_overlong_five_minute_deck_is_not_ready(self):
        result = self.build(PresentationMode.SALES, 300, (DesiredOutcome.ACT,), (NarrativeRole.OPEN, NarrativeRole.EVIDENCE, NarrativeRole.ACTION), long_notes=True)
        self.assertEqual(result[-1].count("TIMING_OVERLONG"), 1)
        self.assertFalse(result[-1].ready)

    def test_07_redundant_deck_finding(self):
        result = self.build(PresentationMode.SALES, 300, (DesiredOutcome.ACT,), (NarrativeRole.OPEN, NarrativeRole.EVIDENCE, NarrativeRole.ACTION), duplicate=True)
        self.assertEqual(result[-1].count("DUPLICATE_SLIDE_PURPOSE"), 1)

    def test_08_narrative_gap_finding(self):
        result = self.build(PresentationMode.SALES, 300, (DesiredOutcome.ACT,), (NarrativeRole.OPEN, NarrativeRole.EVIDENCE, NarrativeRole.ACTION), gap=True)
        self.assertEqual(result[-1].count("MISSING_BRIDGE"), 1)

    def test_09_generic_imagery_warning_without_ban(self):
        result = self.build(PresentationMode.SALES, 300, (DesiredOutcome.ACT,), (NarrativeRole.OPEN, NarrativeRole.EVIDENCE, NarrativeRole.ACTION, NarrativeRole.CLOSE), generic=True)
        self.assertGreater(result[-1].count("IMAGE_IRRELEVANT"), 0)
        self.assertTrue(result[-1].ready)

    def test_10_visual_hierarchy_finding(self):
        result = self.build(PresentationMode.EXECUTIVE, 900, (DesiredOutcome.DECIDE,), (NarrativeRole.OPEN, NarrativeRole.EVIDENCE, NarrativeRole.DECISION), hierarchy=True)
        self.assertEqual(result[-1].count("HIERARCHY_MISMATCH"), 3)

    def test_11_weak_close_finding(self):
        result = self.build(PresentationMode.SALES, 300, (DesiredOutcome.ACT,), (NarrativeRole.OPEN, NarrativeRole.EVIDENCE, NarrativeRole.CLOSE), weak_close=True)
        self.assertGreaterEqual(result[-1].count("WEAK_CLOSE"), 1)

    def test_12_phase16_claim_and_evidence_identity_stable(self):
        result = self.build(PresentationMode.EXECUTIVE, 900, (DesiredOutcome.DECIDE,), (NarrativeRole.OPEN, NarrativeRole.EVIDENCE, NarrativeRole.DECISION))
        material = result[1].slides[1].evidence_plan.claims[0]
        self.assertEqual(material.claim.claim_id, self.claim.claim_id)
        self.assertEqual(material.claim.evidence, self.claim.evidence)

    def test_13_post_approval_reorder_routes_to_content_revision(self):
        project = PresentationApprovalWorkflow(ProjectState.initialize(self.root / "workflow", "phase17-e2e"))
        workflow = NarrativeWorkflow(GroundedOutlineWorkflow(project))
        result = self.build(PresentationMode.SALES, 300, (DesiredOutcome.ACT,), (NarrativeRole.OPEN, NarrativeRole.EVIDENCE, NarrativeRole.ACTION))
        workflow.submit(result[1])
        project.approve_outline()
        report = evaluate_effectiveness(result[1], result[2], result[3], result[4], EditorialReport(EDITORIAL_PASS, ()), proposed_change=ProposedChange.REORDER_SLIDES)
        self.assertEqual(report.count("APPROVAL_REQUIRED"), 1)
        self.assertEqual(workflow.revise_content(result[1]), "OUTLINE_PENDING_APPROVAL")

    def test_14_delivery_notes_are_usable_and_internal_terms_hidden(self):
        result = self.build(PresentationMode.SALES, 300, (DesiredOutcome.ACT,), (NarrativeRole.OPEN, NarrativeRole.EVIDENCE, NarrativeRole.ACTION))
        text = "\n".join(item.notes.natural_text() for item in result[3].slides)
        self.assertIn("Connect takeaway", text)
        for term in ("NarrativeRole", "RehearsalCue", "phase17", "QAStatus"):
            self.assertNotIn(term, text)


if __name__ == "__main__":
    unittest.main()

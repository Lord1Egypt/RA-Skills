#!/usr/bin/env python3
"""Phase 17.5 final effectiveness QA tests."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from phase16_editorial import EDITORIAL_PASS, EDITORIAL_REVIEW_RECOMMENDED, EditorialReport, EditorialWarning, PresentationMode, SlideRole  # noqa: E402
from phase16_outline import GroundedOutlinePlan, GroundedOutlineSlide  # noqa: E402
from phase16_traceability import FinalTraceabilityReport  # noqa: E402
from phase17_brief import BriefValue, DesiredOutcome, PresentationBrief, normalize_outcomes  # noqa: E402
from phase17_delivery import DeliveryNotes, DeliveryPlan  # noqa: E402
from phase17_effectiveness import (  # noqa: E402
    ERROR_PRESENTATION_NOT_READY, EffectivenessError, EffectivenessSignals, ProposedChange,
    QAStatus, classify_change, evaluate_effectiveness, user_facing_effectiveness_message,
)
from phase17_narrative import NarrativePlan, NarrativeRole, NarrativeSlide  # noqa: E402
from phase17_visual_communication import (  # noqa: E402
    CommunicationObjective, HierarchyElement, HierarchyLevel, ImageIntent, ImagePurpose,
    InformationForm, VisualCommunicationPlan, VisualCommunicationSlide,
)


def traceability(*, complete=True, warnings=()):
    return FinalTraceabilityReport(3, 0, 0, 0, () if complete else ("unsupported",), (), (), 0, tuple(warnings))


def fixture(*, duration=300, duplicate=False, gap=False, weak_close=False, generic=False, hierarchy=False, long_notes=False):
    brief = PresentationBrief(BriefValue("BNI partners"), BriefValue("enable referrals"), normalize_outcomes((DesiredOutcome.KNOW, DesiredOutcome.ACT)), PresentationMode.SALES, duration_seconds=duration)
    outline = GroundedOutlinePlan.create(tuple(GroundedOutlineSlide.create(index, f"Slide {index}", "purpose") for index in range(1, 4)))
    roles = (NarrativeRole.OPEN, NarrativeRole.EVIDENCE, NarrativeRole.CLOSE)
    slides = []
    for index, (base, role) in enumerate(zip(outline.slides, roles), 1):
        intent = "establish relevance" if index == 1 else ("establish relevance" if duplicate and index == 2 else ("prove the referral trigger" if index == 2 else "drive a referral action"))
        transition = None if gap and index == 1 else ("connect to the next decision" if index < 3 else None)
        slides.append(NarrativeSlide.create(base, role, SlideRole.STANDARD, intent, f"takeaway {index}", f"job {index}", transition))
    narrative = NarrativePlan.create(brief, outline, "Referral triggers make introductions easier", ("relevance", "proof", "action"), "recognizable situation", "Thank you" if weak_close else "ask for a referral on a concrete trigger", slides)
    visual_slides = []
    for slide in narrative.slides:
        image = ImageIntent(ImagePurpose.DECORATION, "generic handshake", False, True) if generic else None
        visual_slides.append(VisualCommunicationSlide.create(
            slide, CommunicationObjective.SINGLE_MESSAGE, InformationForm.STATEMENT,
            (HierarchyElement("takeaway", HierarchyLevel.PRIMARY), HierarchyElement("icon", HierarchyLevel.SUPPORTING)),
            image=image, observed_dominant_element="icon" if hierarchy else None,
        ))
    visual = VisualCommunicationPlan.create(narrative, visual_slides)
    text = ("Explain the evidence and practical referral example in detail. " * (100 if long_notes else 2)).strip()
    delivery = DeliveryPlan.create(narrative, tuple(DeliveryNotes(text, transition="Connect naturally.") for _ in narrative.slides))
    return narrative, visual, delivery


def evaluate(items, **kwargs):
    return evaluate_effectiveness(*items, traceability(), EditorialReport(EDITORIAL_PASS, ()), **kwargs)


class EffectivenessTests(unittest.TestCase):
    def test_fully_qualified_bni_deck_passes(self):
        report = evaluate(fixture())
        self.assertTrue(report.ready)
        self.assertNotEqual(report.status, QAStatus.REVIEW_REQUIRED)

    def test_duplicate_slide_purpose_is_specific(self):
        self.assertEqual(evaluate(fixture(duplicate=True)).count("DUPLICATE_SLIDE_PURPOSE"), 1)

    def test_narrative_gap_is_specific(self):
        self.assertEqual(evaluate(fixture(gap=True)).count("MISSING_BRIDGE"), 1)

    def test_weak_close_is_found(self):
        self.assertGreaterEqual(evaluate(fixture(weak_close=True)).count("WEAK_CLOSE"), 1)

    def test_overlong_deck_blocks_ready_claim(self):
        report = evaluate(fixture(duration=60, long_notes=True))
        self.assertEqual(report.count("TIMING_OVERLONG"), 1)
        self.assertFalse(report.ready)

    def test_generic_image_heavy_deck_warns(self):
        report = evaluate(fixture(generic=True))
        self.assertEqual(report.count("GENERIC_IMAGE_OVERUSE"), 1)
        self.assertEqual(report.count("IMAGE_IRRELEVANT"), 3)

    def test_hierarchy_mismatch_warns(self):
        self.assertEqual(evaluate(fixture(hierarchy=True)).count("HIERARCHY_MISMATCH"), 3)

    def test_phase16_evidence_integrity_blocks_completion(self):
        items = fixture()
        report = evaluate_effectiveness(*items, traceability(complete=False), EditorialReport(EDITORIAL_PASS, ()))
        self.assertEqual(report.count("PHASE16_EVIDENCE_INCOMPLETE"), 1)
        self.assertFalse(report.ready)

    def test_phase16_editorial_integrity_is_preserved(self):
        items = fixture()
        editorial = EditorialReport(EDITORIAL_REVIEW_RECOMMENDED, (EditorialWarning("COPY_REPETITION", ("slide_01",), "打造"),))
        report = evaluate_effectiveness(*items, traceability(), editorial)
        self.assertEqual(report.count("COPY_REPETITION"), 1)

    def test_safe_auto_fix_boundary(self):
        self.assertTrue(classify_change(ProposedChange.NOTES_CLEANUP).safe_auto_fix)
        self.assertTrue(classify_change(ProposedChange.TRANSITION_WORDING).safe_auto_fix)

    def test_approval_required_change_blocks(self):
        report = evaluate(fixture(), proposed_change=ProposedChange.REORDER_SLIDES)
        self.assertEqual(report.count("APPROVAL_REQUIRED"), 1)
        self.assertFalse(report.ready)

    def test_no_fake_scores_exist(self):
        report = evaluate(fixture())
        payload = report.internal_dict()
        self.assertNotIn("score", payload)
        self.assertNotIn("probability", payload)

    def test_internal_qa_is_hidden_from_ordinary_message(self):
        message = user_facing_effectiveness_message(evaluate(fixture(generic=True)))
        for internal in ("GENERIC_IMAGE_OVERUSE", "QACategory", "REVIEW_REQUIRED"):
            self.assertNotIn(internal, message)

    def test_final_status_is_atomic(self):
        report = evaluate(fixture(), final_artifact_present=False)
        self.assertFalse(report.ready)
        self.assertEqual(report.status, QAStatus.REVIEW_REQUIRED)
        with self.assertRaises(EffectivenessError) as caught:
            report.require_ready()
        self.assertEqual(caught.exception.error_code, ERROR_PRESENTATION_NOT_READY)


if __name__ == "__main__":
    unittest.main()

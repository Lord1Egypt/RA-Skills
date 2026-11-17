#!/usr/bin/env python3
"""Phase 17.3 visual communication tests."""

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
from phase16_editorial import PresentationMode, SlideRole  # noqa: E402
from phase16_outline import GroundedOutlinePlan, GroundedOutlineSlide  # noqa: E402
from phase17_brief import BriefValue, DesiredOutcome, PresentationBrief, normalize_outcomes  # noqa: E402
from phase17_narrative import NarrativePlan, NarrativeRole, NarrativeSlide  # noqa: E402
from phase17_visual_communication import (  # noqa: E402
    ERROR_UNSUPPORTED_CHART_DATA,
    CommunicationObjective,
    DataStory,
    HierarchyElement,
    HierarchyLevel,
    ImageIntent,
    ImagePurpose,
    InformationForm,
    VisualCommunicationError,
    VisualCommunicationPlan,
    VisualCommunicationSlide,
    lint_visual_communication,
    select_information_form,
)
from source_grounding import SourceInventory  # noqa: E402


def make_brief():
    return PresentationBrief(BriefValue("audience"), BriefValue("purpose"), normalize_outcomes((DesiredOutcome.KNOW,)), PresentationMode.EXECUTIVE)


def narrative_slide(outline_slide, role=NarrativeRole.INSIGHT, visual=SlideRole.STANDARD):
    return NarrativeSlide.create(outline_slide, role, visual, "communicate the point", outline_slide.claims[0].text if outline_slide.claims else "one clear idea", "advance the narrative")


def hierarchy(primary="takeaway"):
    return (HierarchyElement(primary, HierarchyLevel.PRIMARY), HierarchyElement("support", HierarchyLevel.SUPPORTING))


def one_slide_plan(slide):
    grounded = GroundedOutlinePlan.create((GroundedOutlineSlide.create(slide.number, "Title", "Purpose", tuple(material.claim for material in slide.evidence_plan.claims) if slide.evidence_plan else ()),))
    narrative = NarrativePlan.create(make_brief(), grounded, "thesis", ("point",), "direct opening", "clear close", (slide,))
    return narrative


class VisualCommunicationTests(unittest.TestCase):
    def test_comparison_selects_comparison_form(self):
        self.assertEqual(select_information_form(CommunicationObjective.COMPARISON), InformationForm.COMPARISON)

    def test_time_sequence_selects_timeline(self):
        self.assertEqual(select_information_form(CommunicationObjective.TIME_SEQUENCE), InformationForm.TIMELINE)

    def test_process_selects_process(self):
        self.assertEqual(select_information_form(CommunicationObjective.PROCESS), InformationForm.PROCESS)

    def test_single_message_selects_statement(self):
        self.assertEqual(select_information_form(CommunicationObjective.SINGLE_MESSAGE), InformationForm.STATEMENT)

    def test_quantitative_trend_uses_chart_with_evidence(self):
        with tempfile.TemporaryDirectory() as temp:
            inventory = SourceInventory.initialize(temp, "visual")
            digest = hashlib.sha256(b"source").hexdigest()
            inventory.add_source("src_report", "pdf", source_digest=digest)
            unit = inventory.add_unit("src_report", "page", {"kind": "page", "start": 1, "end": 1}, "HIGH")
            claim = Claim.create(inventory, "Revenue grew 18% in 2025", ContentOrigin.SOURCE_GROUNDED, [binding_from_unit(inventory, unit["unit_id"])])
            nslide = narrative_slide(GroundedOutlineSlide.create(1, "Trend", "Prove", (claim,)), NarrativeRole.EVIDENCE, SlideRole.DATA)
            visual = VisualCommunicationSlide.create(nslide, CommunicationObjective.QUANTITATIVE_TREND, InformationForm.CHART, hierarchy("18%"))
            self.assertEqual(visual.information_form, InformationForm.CHART)

    def test_visual_and_narrative_roles_remain_independent(self):
        nslide = narrative_slide(GroundedOutlineSlide.create(1, "Evidence", "Prove"), NarrativeRole.EVIDENCE, SlideRole.DATA)
        visual = VisualCommunicationSlide.create(nslide, CommunicationObjective.SINGLE_MESSAGE, InformationForm.STATEMENT, hierarchy())
        self.assertEqual(visual.narrative_role, NarrativeRole.EVIDENCE)
        self.assertNotEqual(visual.information_form.value, nslide.visual_role.value)

    def test_hierarchy_intent_and_mismatch_warning(self):
        nslide = narrative_slide(GroundedOutlineSlide.create(1, "Point", "Explain"))
        visual = VisualCommunicationSlide.create(nslide, CommunicationObjective.SINGLE_MESSAGE, InformationForm.STATEMENT, hierarchy("18%"), observed_dominant_element="decorative icon")
        report = lint_visual_communication(VisualCommunicationPlan.create(one_slide_plan(nslide), (visual,)))
        self.assertEqual(visual.primary_element, "18%")
        self.assertEqual(report.count("HIERARCHY_MISMATCH"), 1)

    def test_irrelevant_decorative_image_warns(self):
        nslide = narrative_slide(GroundedOutlineSlide.create(1, "Point", "Explain"))
        image = ImageIntent(ImagePurpose.DECORATION, "generic handshake", False, True)
        visual = VisualCommunicationSlide.create(nslide, CommunicationObjective.SINGLE_MESSAGE, InformationForm.IMAGE_LED, hierarchy(), image=image)
        self.assertEqual(lint_visual_communication(VisualCommunicationPlan.create(one_slide_plan(nslide), (visual,))).count("IMAGE_IRRELEVANT"), 1)

    def test_useful_context_image_passes(self):
        nslide = narrative_slide(GroundedOutlineSlide.create(1, "Point", "Explain"))
        image = ImageIntent(ImagePurpose.CONTEXT, "actual networking room", True)
        visual = VisualCommunicationSlide.create(nslide, CommunicationObjective.SINGLE_MESSAGE, InformationForm.IMAGE_LED, hierarchy(), image=image)
        self.assertEqual(lint_visual_communication(VisualCommunicationPlan.create(one_slide_plan(nslide), (visual,))).count("IMAGE_IRRELEVANT"), 0)

    def test_evidence_image_is_distinct_from_decoration(self):
        evidence = ImageIntent(ImagePurpose.EVIDENCE, "source diagram", True)
        self.assertEqual(evidence.purpose, ImagePurpose.EVIDENCE)

    def test_data_story_preserves_synthesis_provenance(self):
        with tempfile.TemporaryDirectory() as temp:
            inventory = SourceInventory.initialize(temp, "data-story")
            fact = Claim.create(inventory, "User supplied baseline", ContentOrigin.USER_PROVIDED)
            meaning = Claim.create(inventory, "AGY interpretation", ContentOrigin.AGY_SYNTHESIS)
            decision = Claim.create(inventory, "AGY recommendation", ContentOrigin.AGY_SYNTHESIS)
            story = DataStory(fact, "business context", None, meaning, decision)
            self.assertEqual(story.meaning.origin, ContentOrigin.AGY_SYNTHESIS)
            self.assertEqual(story.decision_relevance.origin, ContentOrigin.AGY_SYNTHESIS)

    def test_unsupported_chart_data_is_rejected(self):
        nslide = narrative_slide(GroundedOutlineSlide.create(1, "Trend", "Explain"), NarrativeRole.EVIDENCE, SlideRole.DATA)
        with self.assertRaises(VisualCommunicationError) as caught:
            VisualCommunicationSlide.create(nslide, CommunicationObjective.QUANTITATIVE_TREND, InformationForm.CHART, hierarchy())
        self.assertEqual(caught.exception.error_code, ERROR_UNSUPPORTED_CHART_DATA)

    def test_approved_style_constraints_are_preserved(self):
        nslide = narrative_slide(GroundedOutlineSlide.create(1, "Point", "Explain"))
        constraints = ("light background", "financial editorial typography")
        visual = VisualCommunicationSlide.create(nslide, CommunicationObjective.SINGLE_MESSAGE, InformationForm.STATEMENT, hierarchy(), approved_style_constraints=constraints)
        self.assertEqual(visual.approved_style_constraints, constraints)


if __name__ == "__main__":
    unittest.main()

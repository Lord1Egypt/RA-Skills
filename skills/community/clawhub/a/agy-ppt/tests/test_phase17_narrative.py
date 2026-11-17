#!/usr/bin/env python3
"""Phase 17.2 narrative architecture tests."""

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
from phase16_outline import GroundedOutlinePlan, GroundedOutlineSlide, GroundedOutlineWorkflow  # noqa: E402
from phase16_slide_evidence import SlideEvidenceError  # noqa: E402
from phase17_brief import BriefValue, DesiredOutcome, PresentationBrief, normalize_outcomes  # noqa: E402
from phase17_narrative import (  # noqa: E402
    NarrativePlan,
    NarrativeRole,
    NarrativeSlide,
    NarrativeWorkflow,
    default_closing_strategy,
    default_opening_strategy,
    lint_narrative,
)
from presentation_workflow import OUTLINE_PENDING_APPROVAL, STYLE_PENDING_APPROVAL, PresentationApprovalWorkflow  # noqa: E402
from project_state import ProjectState  # noqa: E402
from source_grounding import SourceInventory  # noqa: E402


def brief(mode=PresentationMode.SALES, outcomes=(DesiredOutcome.KNOW, DesiredOutcome.ACT)):
    return PresentationBrief(BriefValue("audience"), BriefValue("purpose"), normalize_outcomes(outcomes), mode, duration_seconds=300)


def outline(count=5):
    return GroundedOutlinePlan.create(
        GroundedOutlineSlide.create(index, f"Slide {index}", f"Purpose {index}", (), "cover" if index == 1 else "content")
        for index in range(1, count + 1)
    )


def narrative(mode=PresentationMode.SALES, roles=None, intents=None, transitions=True, outcomes=(DesiredOutcome.KNOW, DesiredOutcome.ACT), closing=None):
    grounded = outline(len(roles) if roles else 5)
    chosen = roles or (NarrativeRole.OPEN, NarrativeRole.CONTEXT, NarrativeRole.INSIGHT, NarrativeRole.CASE, NarrativeRole.ACTION)
    intents = intents or tuple(f"intent {index}" for index in range(1, len(chosen) + 1))
    slides = tuple(
        NarrativeSlide.create(
            grounded.slides[index - 1],
            role,
            SlideRole.DATA if role is NarrativeRole.EVIDENCE else SlideRole.STANDARD,
            intents[index - 1],
            f"takeaway {index}",
            f"job {index}",
            f"bridge {index} to {index + 1}" if transitions and index < len(chosen) else None,
        )
        for index, role in enumerate(chosen, 1)
    )
    b = brief(mode, outcomes)
    return NarrativePlan.create(
        b,
        grounded,
        "deck thesis",
        ("open", "develop", "resolve"),
        default_opening_strategy(mode),
        closing or default_closing_strategy(b),
        slides,
    )


class NarrativeTests(unittest.TestCase):
    def test_bni_five_slide_narrative(self):
        plan = narrative()
        self.assertEqual(len(plan.slides), 5)
        self.assertEqual(plan.slides[-1].narrative_role, NarrativeRole.ACTION)

    def test_executive_narrative_is_decision_forward(self):
        plan = narrative(PresentationMode.EXECUTIVE, (NarrativeRole.OPEN, NarrativeRole.EVIDENCE, NarrativeRole.DECISION), outcomes=(DesiredOutcome.DECIDE,))
        self.assertIn("decision", plan.opening_strategy)
        self.assertEqual(plan.slides[-1].narrative_role, NarrativeRole.DECISION)

    def test_training_narrative_has_learning_progression(self):
        plan = narrative(PresentationMode.TRAINING, (NarrativeRole.OPEN, NarrativeRole.EXPLANATION, NarrativeRole.CASE, NarrativeRole.ACTION))
        self.assertIn("capability", plan.opening_strategy)

    def test_technical_narrative_preserves_failure_mode_opening(self):
        plan = narrative(PresentationMode.TECHNICAL, (NarrativeRole.OPEN, NarrativeRole.PROBLEM, NarrativeRole.EXPLANATION, NarrativeRole.RECOMMENDATION), outcomes=(DesiredOutcome.UNDERSTAND,))
        self.assertIn("failure mode", plan.opening_strategy)

    def test_narrative_role_is_separate_from_visual_role(self):
        plan = narrative(roles=(NarrativeRole.OPEN, NarrativeRole.EVIDENCE, NarrativeRole.ACTION))
        self.assertEqual(plan.slides[1].narrative_role, NarrativeRole.EVIDENCE)
        self.assertEqual(plan.slides[1].visual_role, SlideRole.DATA)
        self.assertIsNot(NarrativeRole.EVIDENCE, SlideRole.DATA)

    def test_duplicate_intent_warning(self):
        plan = narrative(intents=("open", "same purpose", "same purpose", "case", "act"))
        self.assertEqual(lint_narrative(plan).count("DUPLICATE_SLIDE_PURPOSE"), 1)

    def test_missing_bridge_warning(self):
        self.assertGreater(lint_narrative(narrative(transitions=False)).count("MISSING_BRIDGE"), 0)

    def test_weak_closing_warning(self):
        plan = narrative(roles=(NarrativeRole.OPEN, NarrativeRole.EVIDENCE, NarrativeRole.CLOSE), closing="Thank you")
        self.assertEqual(lint_narrative(plan).count("WEAK_CLOSE"), 1)

    def test_unsupported_takeaway_is_blocked_by_phase16(self):
        with tempfile.TemporaryDirectory() as temp:
            inventory = SourceInventory.initialize(temp, "narrative")
            digest = hashlib.sha256(b"source").hexdigest()
            inventory.add_source("src_report", "pdf", source_digest=digest)
            unit = inventory.add_unit("src_report", "page", {"kind": "page", "start": 1, "end": 1}, "HIGH")
            claim = Claim.create(inventory, "Revenue grew 18% in 2025", ContentOrigin.SOURCE_GROUNDED, [binding_from_unit(inventory, unit["unit_id"])])
            grounded = GroundedOutlineSlide.create(1, "Growth", "Prove", (claim,))
            with self.assertRaises(SlideEvidenceError):
                NarrativeSlide.create(grounded, NarrativeRole.EVIDENCE, SlideRole.DATA, "prove growth", "Revenue grew 28% in 2025", "establish evidence")

    def test_post_approval_reorder_uses_outline_revision(self):
        with tempfile.TemporaryDirectory() as temp:
            grounded_workflow = GroundedOutlineWorkflow(PresentationApprovalWorkflow(ProjectState.initialize(temp, "narrative")))
            workflow = NarrativeWorkflow(grounded_workflow)
            first = narrative()
            workflow.submit(first)
            grounded_workflow.approve()
            revised = narrative(roles=(NarrativeRole.OPEN, NarrativeRole.INSIGHT, NarrativeRole.CONTEXT, NarrativeRole.CASE, NarrativeRole.ACTION))
            self.assertEqual(workflow.revise_content(revised), OUTLINE_PENDING_APPROVAL)

    def test_style_revision_preserves_narrative_identity(self):
        with tempfile.TemporaryDirectory() as temp:
            grounded_workflow = GroundedOutlineWorkflow(PresentationApprovalWorkflow(ProjectState.initialize(temp, "narrative-style")))
            workflow = NarrativeWorkflow(grounded_workflow)
            plan = narrative()
            workflow.submit(plan)
            grounded_workflow.approve()
            self.assertEqual(workflow.revise_style({"direction": "editorial"}), STYLE_PENDING_APPROVAL)
            self.assertEqual(workflow.plan.plan_id, plan.plan_id)

    def test_deterministic_representation(self):
        self.assertEqual(narrative().plan_id, narrative().plan_id)


if __name__ == "__main__":
    unittest.main()

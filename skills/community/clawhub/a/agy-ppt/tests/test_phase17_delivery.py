#!/usr/bin/env python3
"""Phase 17.4 delivery and rehearsal tests."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from phase16_editorial import PresentationMode, SlideRole  # noqa: E402
from phase16_outline import GroundedOutlinePlan, GroundedOutlineSlide  # noqa: E402
from phase17_brief import BriefValue, DesiredOutcome, PresentationBrief, normalize_outcomes  # noqa: E402
from phase17_delivery import (  # noqa: E402
    DeliveryNotes, DeliveryPlan, RehearsalCue, semantic_change_requires_approval, validate_timing,
)
from phase17_narrative import NarrativePlan, NarrativeRole, NarrativeSlide  # noqa: E402


def make_plan(duration, mode=PresentationMode.SALES, roles=None):
    roles = roles or (NarrativeRole.OPEN, NarrativeRole.CONTEXT, NarrativeRole.INSIGHT, NarrativeRole.ACTION, NarrativeRole.CLOSE)
    brief = PresentationBrief(BriefValue("BNI partners"), BriefValue("enable referrals"), normalize_outcomes((DesiredOutcome.KNOW, DesiredOutcome.ACT)), mode, duration_seconds=duration)
    outline_slides = tuple(GroundedOutlineSlide.create(index, f"Slide {index}", "purpose") for index in range(1, len(roles) + 1))
    outline = GroundedOutlinePlan.create(outline_slides)
    slides = tuple(NarrativeSlide.create(item, role, SlideRole.STANDARD, f"intent {item.number}", f"takeaway {item.number}", f"job {item.number}", "connect forward" if item.number < len(roles) else None) for item, role in zip(outline_slides, roles))
    return NarrativePlan.create(brief, outline, "thesis", ("open", "develop", "close"), "relevant situation", "clear action", slides)


def notes_for(plan, repeat=8):
    return tuple(DeliveryNotes((f"Core message for slide {slide.number}. " * repeat).strip(), transition="Connect to the next idea." if slide.number < len(plan.slides) else None) for slide in plan.slides)


class DeliveryTests(unittest.TestCase):
    def test_five_minute_bni_budget_is_exact(self):
        plan = make_plan(300)
        delivery = DeliveryPlan.create(plan, notes_for(plan))
        self.assertEqual(sum(item.allocated_seconds for item in delivery.slides), 300)

    def test_fifteen_minute_executive_budget(self):
        plan = make_plan(900, PresentationMode.EXECUTIVE)
        self.assertEqual(sum(item.allocated_seconds for item in DeliveryPlan.create(plan, notes_for(plan)).slides), 900)

    def test_thirty_minute_training_budget(self):
        plan = make_plan(1800, PresentationMode.TRAINING)
        self.assertEqual(sum(item.allocated_seconds for item in DeliveryPlan.create(plan, notes_for(plan)).slides), 1800)

    def test_weighted_allocation_is_not_even(self):
        plan = make_plan(300)
        values = tuple(item.allocated_seconds for item in DeliveryPlan.create(plan, notes_for(plan)).slides)
        self.assertGreater(values[2], values[0])
        self.assertGreater(len(set(values)), 1)

    def test_no_duration_does_not_invent_budget(self):
        plan = make_plan(None)
        delivery = DeliveryPlan.create(plan, notes_for(plan))
        self.assertTrue(all(item.allocated_seconds is None for item in delivery.slides))
        self.assertEqual(validate_timing(delivery).status, "PASS")

    def test_overlong_deck_warns_honestly(self):
        plan = make_plan(60)
        delivery = DeliveryPlan.create(plan, notes_for(plan, 80))
        self.assertEqual(validate_timing(delivery).count("TIMING_OVERLONG"), 1)

    def test_underfilled_deck_warns(self):
        plan = make_plan(3600)
        delivery = DeliveryPlan.create(plan, notes_for(plan, 1))
        self.assertEqual(validate_timing(delivery).count("TIMING_UNDERFILLED"), 1)

    def test_transition_connects_delivery(self):
        plan = make_plan(300)
        note = DeliveryNotes("Core point", transition="From referral triggers, move to the action partners can take.")
        delivery = DeliveryPlan.create(plan, (note,) + notes_for(plan)[1:])
        self.assertIn("move to the action", delivery.slides[0].notes.natural_text())

    def test_notes_are_natural_and_do_not_expose_markers(self):
        note = DeliveryNotes("Explain the referral signal naturally.", opening_cue="Ask who has seen this situation.", emphasis="Pause on 18%.")
        text = note.natural_text()
        self.assertNotIn("OPENING_CUE", text)
        self.assertIn("Pause on 18%", text)

    def test_central_case_receives_more_time(self):
        roles = (NarrativeRole.OPEN, NarrativeRole.CASE, NarrativeRole.CLOSE)
        plan = make_plan(180, roles=roles)
        values = tuple(item.allocated_seconds for item in DeliveryPlan.create(plan, notes_for(plan)).slides)
        self.assertGreater(values[1], values[0])

    def test_cleanup_preserves_semantic_and_evidence_plan(self):
        plan = make_plan(300)
        original = DeliveryPlan.create(plan, notes_for(plan))
        cleaned = original.cleanup_delivery(2, DeliveryNotes("A clearer spoken explanation."), (RehearsalCue.PAUSE,))
        self.assertEqual(cleaned.narrative_plan.plan_id, original.narrative_plan.plan_id)
        self.assertEqual(cleaned.narrative_plan.grounded_outline.plan_id, original.narrative_plan.grounded_outline.plan_id)

    def test_post_approval_semantic_change_requires_existing_approval(self):
        self.assertTrue(semantic_change_requires_approval("reorder_slide"))
        self.assertTrue(semantic_change_requires_approval("change_takeaway"))
        self.assertFalse(semantic_change_requires_approval("transition_wording"))


if __name__ == "__main__":
    unittest.main()

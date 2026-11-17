#!/usr/bin/env python3
"""Phase 17.1 Presentation Brief contract tests."""

from __future__ import annotations

import os
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from phase16_editorial import PresentationMode  # noqa: E402
from phase17_brief import (  # noqa: E402
    BriefConstraint,
    BriefValue,
    ContextProvenance,
    DesiredOutcome,
    PresentationBrief,
    infer_obvious_context,
    normalize_outcomes,
    user_facing_brief_message,
)
from presentation_workflow import OUTLINE_PENDING_APPROVAL, PresentationApprovalWorkflow  # noqa: E402
from project_state import ProjectState  # noqa: E402


def make_brief(**overrides):
    values = {
        "audience": BriefValue("BNI business partners"),
        "purpose": BriefValue("build a referral system"),
        "desired_outcomes": normalize_outcomes((DesiredOutcome.KNOW, DesiredOutcome.ACT)),
        "mode": PresentationMode.SALES,
    }
    values.update(overrides)
    return PresentationBrief(**values)


class PresentationBriefTests(unittest.TestCase):
    def test_explicit_audience_preserved_with_provenance(self):
        brief = make_brief()
        self.assertEqual(brief.audience.value, "BNI business partners")
        self.assertEqual(brief.audience.provenance, ContextProvenance.USER_PROVIDED)

    def test_explicit_purpose_preserved(self):
        self.assertEqual(make_brief().purpose.value, "build a referral system")

    def test_multiple_outcomes_use_deterministic_canonical_order(self):
        brief = make_brief(desired_outcomes=normalize_outcomes((DesiredOutcome.ACT, DesiredOutcome.KNOW, DesiredOutcome.REMEMBER)))
        self.assertEqual(tuple(item.outcome for item in brief.desired_outcomes), (DesiredOutcome.KNOW, DesiredOutcome.REMEMBER, DesiredOutcome.ACT))

    def test_explicit_duration_is_preserved(self):
        self.assertEqual(make_brief(duration_seconds=300).duration_seconds, 300)

    def test_unspecified_duration_remains_unspecified(self):
        self.assertIsNone(make_brief().duration_seconds)

    def test_reuses_exact_phase16_presentation_mode(self):
        brief = make_brief(mode=PresentationMode.EXECUTIVE)
        self.assertIs(brief.mode, PresentationMode.EXECUTIVE)

    def test_obvious_context_inference_is_allowlisted_and_labeled(self):
        inferred = infer_obvious_context("請做給 BNI 商務夥伴的五分鐘簡報")
        self.assertEqual(inferred.context.value, "business networking presentation")
        self.assertEqual(inferred.audience.provenance, ContextProvenance.SAFELY_DERIVED)

    def test_sensitive_traits_are_not_inferred(self):
        inferred = infer_obvious_context("根據政治偏好、宗教、收入與心理弱點分析觀眾")
        self.assertIsNone(inferred.audience)
        self.assertIsNone(inferred.context)

    def test_deterministic_equality_and_constraint_order(self):
        first = make_brief(constraints=(BriefConstraint("language", "zh-TW"), BriefConstraint("pages", "5")))
        second = make_brief(constraints=(BriefConstraint("pages", "5"), BriefConstraint("language", "zh-TW")))
        self.assertEqual(first, second)
        self.assertEqual(first.canonical_json(), second.canonical_json())

    def test_serialization_has_no_filesystem_environment_or_random_leakage(self):
        with tempfile.TemporaryDirectory() as temp:
            os.environ["PHASE17_TEST_SENTINEL"] = temp
            payload = make_brief(duration_seconds=300).canonical_json()
            self.assertNotIn(temp, payload)
            self.assertNotIn("PHASE17_TEST_SENTINEL", payload)
            self.assertNotIn("timestamp", payload.lower())
            self.assertNotIn("uuid", payload.lower())

    def test_normal_user_flow_still_starts_at_outline_without_new_gate(self):
        with tempfile.TemporaryDirectory() as temp:
            workflow = PresentationApprovalWorkflow(ProjectState.initialize(temp, "phase17-brief"))
            outline = ({"number": 1, "title": "開場", "role": "cover"},)
            self.assertEqual(workflow.submit_outline(outline), OUTLINE_PENDING_APPROVAL)
        text = user_facing_brief_message()
        for internal in ("PresentationBrief", "KNOW", "SAFELY_DERIVED", "presentation_mode"):
            self.assertNotIn(internal, text)


if __name__ == "__main__":
    unittest.main()

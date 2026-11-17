#!/usr/bin/env python3
"""Approval-driven presentation workflow tests (no real generation)."""

from __future__ import annotations

import tempfile
import unittest
from copy import deepcopy
from pathlib import Path
import sys

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from presentation_workflow import (  # noqa: E402
    ERROR_APPROVAL_REQUIRED,
    ERROR_WORKFLOW_INVALID,
    OUTLINE_PENDING_APPROVAL,
    READY_FOR_FULL_GENERATION,
    SAMPLE_PENDING_APPROVAL,
    STYLE_PENDING_APPROVAL,
    PresentationApprovalWorkflow,
    PresentationWorkflowError,
    RevisionIntent,
    completion_prompt,
    outline_confirmation_prompt,
    sample_confirmation_prompt,
    style_confirmation_prompt,
)
from project_state import ProjectState  # noqa: E402


OUTLINE = (
    {"number": 1, "title": "Cover", "role": "cover", "purpose": "Open"},
    {"number": 2, "title": "Problem", "role": "content", "purpose": "Explain"},
    {"number": 3, "title": "Decision", "role": "summary", "purpose": "Close"},
)
STYLE = {"direction": "editorial", "palette": ["#112233", "#ffffff"], "density": "medium"}
STYLE_REVISION = {
    "direction": "金融商業雜誌風",
    "palette": ["淺色背景", "深炭黑", "香檳金"],
    "typography": "現代、高留白",
    "imagery": "主視覺照片放大",
    "density": "少文字的視覺呈現",
}


class WorkflowCase(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.state = ProjectState.initialize(self.temp.name, "approval-demo")
        self.workflow = PresentationApprovalWorkflow(self.state)
        self.sample_calls: list[int] = []
        self.full_calls = 0

    def tearDown(self) -> None:
        self.temp.cleanup()

    def render_sample(self, slide):
        self.sample_calls.append(slide["number"])
        return f"origin_image/slide_{slide['number']:02d}.png"

    def render_full(self, slides, style, sample_ref):
        self.full_calls += 1
        return {"slides": len(slides), "style": style["direction"], "sample": sample_ref}

    def approved_to_sample(self) -> None:
        self.workflow.submit_outline(OUTLINE)
        self.workflow.approve_outline()
        self.workflow.submit_style(STYLE)
        self.workflow.approve_style()

    def approved_all(self) -> None:
        self.approved_to_sample()
        self.workflow.generate_sample(self.render_sample)
        self.workflow.approve_sample()

    def assert_blocked_full(self) -> None:
        with self.assertRaises(PresentationWorkflowError) as caught:
            self.workflow.generate_full(self.render_full)
        self.assertEqual(caught.exception.error_code, ERROR_APPROVAL_REQUIRED)
        self.assertEqual(self.full_calls, 0)


class StageTests(WorkflowCase):
    def test_fresh_request_stops_at_outline_approval(self):
        self.assertEqual(self.workflow.submit_outline(OUTLINE), OUTLINE_PENDING_APPROVAL)
        self.assertEqual(self.sample_calls, [])
        self.assert_blocked_full()

    def test_outline_approval_stops_at_style_approval(self):
        self.workflow.submit_outline(OUTLINE)
        self.assertEqual(self.workflow.approve_outline(), STYLE_PENDING_APPROVAL)
        self.assertEqual(self.sample_calls, [])
        self.assert_blocked_full()

    def test_style_approval_generates_no_deck_and_one_sample_when_requested(self):
        self.approved_to_sample()
        self.assertEqual(self.workflow.status, SAMPLE_PENDING_APPROVAL)
        result = self.workflow.generate_sample(self.render_sample)
        self.assertEqual(result.slide_number, 2)
        self.assertEqual(self.sample_calls, [2])
        self.assert_blocked_full()

    def test_sample_approval_is_the_full_generation_gate(self):
        self.approved_all()
        self.assertEqual(self.workflow.status, READY_FOR_FULL_GENERATION)
        result = self.workflow.generate_full(self.render_full)
        self.assertEqual(self.full_calls, 1)
        self.assertEqual(result.value["slides"], 3)

    def test_explicit_sample_selection_is_honored(self):
        self.approved_to_sample()
        result = self.workflow.generate_sample(self.render_sample, slide_number=3)
        self.assertEqual(result.slide_number, 3)
        self.assertEqual(self.sample_calls, [3])


class RejectionAndInvalidationTests(WorkflowCase):
    def test_outline_rejection_blocks_every_later_stage(self):
        self.workflow.submit_outline(OUTLINE)
        self.workflow.reject_outline()
        self.assertEqual(self.workflow.status, OUTLINE_PENDING_APPROVAL)
        self.assert_blocked_full()

    def test_outline_revision_invalidates_style_and_sample(self):
        self.approved_all()
        revised = (*OUTLINE, {"number": 4, "title": "Appendix", "role": "content"})
        self.workflow.submit_outline(revised)
        self.assertEqual(self.workflow.status, OUTLINE_PENDING_APPROVAL)
        self.assertEqual(self.state.data["style"]["status"], "pending")
        self.assertEqual(self.state.data["sample"]["status"], "pending")
        self.assert_blocked_full()

    def test_style_rejection_blocks_sample_and_full_generation(self):
        self.approved_to_sample()
        self.workflow.reject_style()
        self.assertEqual(self.workflow.status, STYLE_PENDING_APPROVAL)
        self.assert_blocked_full()

    def test_style_revision_invalidates_approved_sample(self):
        self.approved_all()
        self.workflow.submit_style({**STYLE, "density": "high"})
        self.assertEqual(self.workflow.status, STYLE_PENDING_APPROVAL)
        self.assertEqual(self.state.data["sample"]["status"], "pending")
        self.assert_blocked_full()

    def test_sample_rejection_and_revision_each_remain_sample_pending(self):
        self.approved_to_sample()
        self.workflow.generate_sample(self.render_sample)
        self.workflow.reject_sample()
        self.assertEqual(self.workflow.status, SAMPLE_PENDING_APPROVAL)
        self.workflow.generate_sample(self.render_sample)
        self.assertEqual(self.sample_calls, [2, 2])
        self.assertEqual(self.workflow.status, SAMPLE_PENDING_APPROVAL)
        self.assert_blocked_full()


class BoundaryAndResumeTests(WorkflowCase):
    def test_worker_receives_one_slide_and_cannot_mutate_outline(self):
        self.approved_to_sample()

        def mutating_worker(slide):
            slide["title"] = "worker rewrite"
            self.sample_calls.append(slide["number"])
            return "origin_image/sample.png"

        self.workflow.generate_sample(mutating_worker)
        self.assertEqual(self.sample_calls, [2])
        self.workflow.generate_sample(self.render_sample)
        self.assertEqual(self.sample_calls, [2, 2])

    def test_failed_sample_does_not_approve_or_generate_full(self):
        self.approved_to_sample()

        def failed(_slide):
            raise RuntimeError("renderer unavailable")

        with self.assertRaises(RuntimeError):
            self.workflow.generate_sample(failed)
        self.assertEqual(self.workflow.status, SAMPLE_PENDING_APPROVAL)
        self.assert_blocked_full()

    def test_resume_rejects_stale_approval_for_different_outline(self):
        self.approved_all()
        self.state.data["outline"]["content_digest"] = "0" * 64
        resumed = PresentationApprovalWorkflow(self.state, outline=OUTLINE, style=STYLE)
        self.assertEqual(resumed.status, OUTLINE_PENDING_APPROVAL)

    def test_resume_reuses_only_matching_current_approvals(self):
        self.approved_all()
        resumed = PresentationApprovalWorkflow(self.state, outline=OUTLINE, style=STYLE)
        self.assertEqual(resumed.status, READY_FOR_FULL_GENERATION)
        result = resumed.generate_full(self.render_full)
        self.assertEqual(result.value["slides"], 3)

    def test_full_generator_cannot_mutate_canonical_inputs(self):
        self.approved_all()

        def mutating_full(slides, style, _sample):
            slides[0]["title"] = "changed"
            style["direction"] = "changed"
            return "deck.pptx"

        self.workflow.generate_full(mutating_full)
        second = self.workflow.generate_full(self.render_full)
        self.assertEqual(second.value["style"], "editorial")


class RevisionIntentTests(WorkflowCase):
    def test_style_only_revision_preserves_approved_outline_and_invalidates_dependents(self):
        self.approved_all()
        outline_gate = deepcopy(self.state.data["outline"])
        outline_file = Path(self.temp.name) / "outline.md"
        outline_file.write_text("# Approved outline\n\n3. Power Team\n", encoding="utf-8")
        outline_bytes = outline_file.read_bytes()

        status = self.workflow.apply_revision(
            RevisionIntent.STYLE_ONLY,
            style=STYLE_REVISION,
        )

        self.assertEqual(status, STYLE_PENDING_APPROVAL)
        self.assertEqual(self.state.data["outline"], outline_gate)
        self.assertEqual(outline_file.read_bytes(), outline_bytes)
        self.assertEqual(self.state.data["style"]["status"], "pending")
        self.assertEqual(self.state.data["sample"]["status"], "pending")
        self.assert_blocked_full()

    def test_style_only_revision_rejects_hidden_outline_mutation_atomically(self):
        self.approved_all()
        state_before = deepcopy(self.state.data)
        with self.assertRaises(PresentationWorkflowError) as caught:
            self.workflow.apply_revision(
                RevisionIntent.STYLE_ONLY,
                outline=OUTLINE,
                style=STYLE_REVISION,
            )
        self.assertEqual(caught.exception.error_code, ERROR_WORKFLOW_INVALID)
        self.assertEqual(self.state.data, state_before)

    def test_obvious_cosmetic_requests_use_structured_style_path(self):
        self.approved_all()
        cosmetic_styles = (
            {"direction": "more premium"},
            {"palette": ["light background"]},
            {"imagery": "bigger photos"},
            {"density": "less text visually and more whitespace"},
            {"layout": "clean cards and asymmetric composition"},
        )
        approved_outline = deepcopy(self.state.data["outline"])
        for style in cosmetic_styles:
            self.workflow.apply_revision(RevisionIntent.STYLE_ONLY, style=style)
            self.assertEqual(self.state.data["outline"], approved_outline)
            self.workflow.approve_style()
            self.workflow.generate_sample(self.render_sample)
            self.workflow.approve_sample()

    def test_content_revision_returns_to_outline_confirmation(self):
        self.approved_all()
        revised = tuple(
            {**slide, "title": "Three referral cases", "purpose": "Show real cases"}
            if slide["number"] == 3
            else slide
            for slide in OUTLINE
        )
        status = self.workflow.apply_revision(RevisionIntent.CONTENT, outline=revised)
        self.assertEqual(status, OUTLINE_PENDING_APPROVAL)
        self.assertEqual(self.state.data["outline"]["status"], "pending")
        self.assertEqual(self.state.data["style"]["status"], "pending")
        self.assertEqual(self.state.data["sample"]["status"], "pending")
        self.assert_blocked_full()

    def test_mixed_feedback_takes_content_revision_path(self):
        self.approved_all()
        revised = tuple(
            {**slide, "title": "Three actual cases"} if slide["number"] == 3 else slide
            for slide in OUTLINE
        )
        status = self.workflow.apply_revision(
            RevisionIntent.MIXED,
            outline=revised,
            style=STYLE_REVISION,
        )
        self.assertEqual(status, OUTLINE_PENDING_APPROVAL)
        self.assertEqual(self.state.data["outline"]["status"], "pending")
        self.assertEqual(self.state.data["style"]["status"], "pending")
        self.assertEqual(self.state.data["sample"]["status"], "pending")
        self.assert_blocked_full()


class UserFacingPromptTests(unittest.TestCase):
    FORBIDDEN = (
        "OUTLINE_PENDING_APPROVAL",
        "STYLE_PENDING_APPROVAL",
        "SAMPLE_PENDING_APPROVAL",
        "FULL_GENERATION",
        "Gate 2",
        "Gate 3",
        "Gate 5",
        "Gate 6",
        "outline.md",
        "project_state.json",
        "deck_spec.json",
        "slide_jobs.json",
    )

    def assert_user_facing(self, text: str) -> None:
        for token in self.FORBIDDEN:
            self.assertNotIn(token, text)

    def test_outline_prompt_is_natural_and_content_focused(self):
        text = outline_confirmation_prompt(OUTLINE).text
        self.assertIn("3 頁大綱", text)
        self.assertIn("Problem", text)
        self.assert_user_facing(text)

    def test_content_revision_prompt_returns_to_outline_without_artifact_names(self):
        with tempfile.TemporaryDirectory() as temp:
            state = ProjectState.initialize(temp, "content-revision-message")
            workflow = PresentationApprovalWorkflow(state)
            workflow.submit_outline(OUTLINE)
            workflow.approve_outline()
            revised = tuple(
                {**slide, "title": "Three referral cases"}
                if slide["number"] == 3
                else slide
                for slide in OUTLINE
            )
            self.assertEqual(
                workflow.apply_revision(RevisionIntent.CONTENT, outline=revised),
                OUTLINE_PENDING_APPROVAL,
            )
            text = outline_confirmation_prompt(revised).text
        self.assertIn("Three referral cases", text)
        self.assert_user_facing(text)

    def test_mixed_revision_prompt_returns_to_outline_without_artifact_names(self):
        with tempfile.TemporaryDirectory() as temp:
            state = ProjectState.initialize(temp, "mixed-revision-message")
            workflow = PresentationApprovalWorkflow(state)
            workflow.submit_outline(OUTLINE)
            workflow.approve_outline()
            revised = tuple(
                {**slide, "title": "Three actual cases"}
                if slide["number"] == 3
                else slide
                for slide in OUTLINE
            )
            self.assertEqual(
                workflow.apply_revision(
                    RevisionIntent.MIXED,
                    outline=revised,
                    style=STYLE_REVISION,
                ),
                OUTLINE_PENDING_APPROVAL,
            )
            text = outline_confirmation_prompt(revised).text
        self.assertIn("Three actual cases", text)
        self.assert_user_facing(text)

    def test_style_prompt_contains_how_without_reprinting_outline(self):
        text = style_confirmation_prompt(STYLE_REVISION).text
        self.assertIn("視覺方向", text)
        self.assertIn("金融商業雜誌風", text)
        self.assertIn("主視覺照片放大", text)
        for slide in OUTLINE:
            self.assertNotIn(slide["title"], text)
        self.assert_user_facing(text)

    def test_sample_prompt_is_concise_and_does_not_overclaim_qa(self):
        text = sample_confirmation_prompt(2).text
        self.assertIn("第 2 頁樣張", text)
        self.assertIn("確認後", text)
        for claim in ("逐字完全無錯", "完全無擁擠", "百分之百正確"):
            self.assertNotIn(claim, text)
        self.assert_user_facing(text)

    def test_sample_prompt_discloses_a_concrete_warning_without_internal_details(self):
        text = sample_confirmation_prompt(2, warning="右下角資料來源字級較小").text
        self.assertIn("右下角資料來源字級較小", text)
        self.assert_user_facing(text)

    def test_completion_prompt_prioritizes_the_pptx(self):
        text = completion_prompt(5, "output/deck.pptx").text
        self.assertIn("5 頁", text)
        self.assertIn("output/deck.pptx", text)
        self.assert_user_facing(text)


if __name__ == "__main__":
    unittest.main()

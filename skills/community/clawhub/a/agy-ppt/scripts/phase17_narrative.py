#!/usr/bin/env python3
"""Phase 17.2 narrative architecture layered on Phase 16 grounded outlines."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from enum import Enum
from typing import Iterable

from phase16_editorial import PresentationMode, SlideRole
from phase16_outline import GroundedOutlinePlan, GroundedOutlineSlide, GroundedOutlineWorkflow
from phase16_slide_evidence import MaterialClaim, SlideEvidencePlan
from phase17_brief import DesiredOutcome, PresentationBrief


ERROR_NARRATIVE_INVALID = "PHASE17_NARRATIVE_INVALID"
NARRATIVE_PASS = "PASS"
NARRATIVE_WARNING = "WARNING"


class NarrativeError(Exception):
    def __init__(self, error_code: str, message: str) -> None:
        super().__init__(message)
        self.error_code = error_code


class NarrativeRole(str, Enum):
    OPEN = "OPEN"
    CONTEXT = "CONTEXT"
    PROBLEM = "PROBLEM"
    QUESTION = "QUESTION"
    INSIGHT = "INSIGHT"
    EVIDENCE = "EVIDENCE"
    CASE = "CASE"
    CONTRAST = "CONTRAST"
    EXPLANATION = "EXPLANATION"
    RECOMMENDATION = "RECOMMENDATION"
    DECISION = "DECISION"
    ACTION = "ACTION"
    CLOSE = "CLOSE"


_GENERIC_INTENTS = frozenset({"present information", "show content", "explain topic", "介紹內容", "說明主題"})
_RESOLUTION_ROLES = frozenset({NarrativeRole.INSIGHT, NarrativeRole.EXPLANATION, NarrativeRole.RECOMMENDATION, NarrativeRole.DECISION, NarrativeRole.ACTION})
_SUPPORT_ROLES = frozenset({NarrativeRole.EVIDENCE, NarrativeRole.CASE, NarrativeRole.EXPLANATION, NarrativeRole.CONTRAST})


def _clean(value: str, label: str) -> str:
    text = value.strip() if isinstance(value, str) else ""
    if not text:
        raise NarrativeError(ERROR_NARRATIVE_INVALID, f"{label} is required")
    return text


def _canonical(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False)


@dataclass(frozen=True)
class NarrativeSlide:
    number: int
    narrative_role: NarrativeRole
    visual_role: SlideRole
    intent: str
    takeaway: str
    job_to_be_done: str
    transition_to_next: str | None = None
    evidence_plan: SlideEvidencePlan | None = None

    @classmethod
    def create(
        cls,
        outline_slide: GroundedOutlineSlide,
        narrative_role: NarrativeRole,
        visual_role: SlideRole,
        intent: str,
        takeaway: str,
        job_to_be_done: str,
        transition_to_next: str | None = None,
    ) -> "NarrativeSlide":
        if not isinstance(outline_slide, GroundedOutlineSlide):
            raise NarrativeError(ERROR_NARRATIVE_INVALID, "grounded outline slide is required")
        if not isinstance(narrative_role, NarrativeRole) or not isinstance(visual_role, SlideRole):
            raise NarrativeError(ERROR_NARRATIVE_INVALID, "narrative and visual roles are invalid")
        transition = transition_to_next.strip() if isinstance(transition_to_next, str) and transition_to_next.strip() else None
        evidence_plan = None
        if outline_slide.claims:
            evidence_plan = SlideEvidencePlan.create(
                f"slide_{outline_slide.number:02d}",
                (MaterialClaim(claim) for claim in outline_slide.claims),
            )
            evidence_plan.validate_rendered_text(takeaway)
        return cls(
            outline_slide.number,
            narrative_role,
            visual_role,
            _clean(intent, "slide intent"),
            _clean(takeaway, "slide takeaway"),
            _clean(job_to_be_done, "slide job-to-be-done"),
            transition,
            evidence_plan,
        )

    def internal_dict(self) -> dict[str, object]:
        return {
            "number": self.number,
            "narrative_role": self.narrative_role.value,
            "visual_role": self.visual_role.value,
            "intent": self.intent,
            "takeaway": self.takeaway,
            "job_to_be_done": self.job_to_be_done,
            "transition_to_next": self.transition_to_next,
            "evidence_plan_id": self.evidence_plan.plan_id if self.evidence_plan else None,
        }


@dataclass(frozen=True)
class NarrativePlan:
    plan_id: str
    brief: PresentationBrief
    grounded_outline: GroundedOutlinePlan
    deck_thesis: str
    narrative_arc: tuple[str, ...]
    opening_strategy: str
    closing_strategy: str
    slides: tuple[NarrativeSlide, ...]

    @classmethod
    def create(
        cls,
        brief: PresentationBrief,
        grounded_outline: GroundedOutlinePlan,
        deck_thesis: str,
        narrative_arc: Iterable[str],
        opening_strategy: str,
        closing_strategy: str,
        slides: Iterable[NarrativeSlide],
    ) -> "NarrativePlan":
        if not isinstance(brief, PresentationBrief) or not isinstance(grounded_outline, GroundedOutlinePlan):
            raise NarrativeError(ERROR_NARRATIVE_INVALID, "brief and grounded outline are required")
        clean_arc = tuple(_clean(item, "narrative arc step") for item in narrative_arc)
        clean_slides = tuple(slides)
        if not clean_arc or not clean_slides or any(not isinstance(item, NarrativeSlide) for item in clean_slides):
            raise NarrativeError(ERROR_NARRATIVE_INVALID, "narrative arc and slides are required")
        outline_numbers = tuple(slide.number for slide in grounded_outline.slides)
        narrative_numbers = tuple(slide.number for slide in clean_slides)
        if narrative_numbers != outline_numbers:
            raise NarrativeError(ERROR_NARRATIVE_INVALID, "narrative slides must match grounded outline order exactly")
        payload = {
            "brief": brief.internal_dict(),
            "grounded_outline_id": grounded_outline.plan_id,
            "deck_thesis": _clean(deck_thesis, "deck thesis"),
            "narrative_arc": clean_arc,
            "opening_strategy": _clean(opening_strategy, "opening strategy"),
            "closing_strategy": _clean(closing_strategy, "closing strategy"),
            "slides": [slide.internal_dict() for slide in clean_slides],
        }
        plan_id = "np:" + hashlib.sha256(_canonical(payload).encode("utf-8")).hexdigest()[:16]
        return cls(
            plan_id,
            brief,
            grounded_outline,
            payload["deck_thesis"],
            clean_arc,
            payload["opening_strategy"],
            payload["closing_strategy"],
            clean_slides,
        )


@dataclass(frozen=True)
class NarrativeFinding:
    code: str
    slide_numbers: tuple[int, ...]
    detail: str


@dataclass(frozen=True)
class NarrativeReport:
    status: str
    findings: tuple[NarrativeFinding, ...]

    def count(self, code: str) -> int:
        return sum(finding.code == code for finding in self.findings)


def lint_narrative(plan: NarrativePlan) -> NarrativeReport:
    if not isinstance(plan, NarrativePlan):
        raise NarrativeError(ERROR_NARRATIVE_INVALID, "narrative plan is invalid")
    findings: list[NarrativeFinding] = []
    intents: dict[str, list[int]] = {}
    for slide in plan.slides:
        intents.setdefault(slide.intent.casefold(), []).append(slide.number)
        if slide.intent.casefold() in _GENERIC_INTENTS:
            findings.append(NarrativeFinding("WEAK_SLIDE_INTENT", (slide.number,), slide.intent))
    for intent, numbers in sorted(intents.items()):
        if len(numbers) > 1:
            findings.append(NarrativeFinding("DUPLICATE_SLIDE_PURPOSE", tuple(numbers), intent))

    for start in range(len(plan.slides) - 2):
        run = plan.slides[start:start + 3]
        if len({slide.narrative_role for slide in run}) == 1:
            findings.append(NarrativeFinding("REPEATED_NARRATIVE_ROLE", tuple(slide.number for slide in run), run[0].narrative_role.value))

    for current, following in zip(plan.slides, plan.slides[1:]):
        if current.transition_to_next is None:
            findings.append(NarrativeFinding("MISSING_BRIDGE", (current.number, following.number), "transition intent is absent"))

    support_seen = False
    for slide in plan.slides:
        if slide.narrative_role in _SUPPORT_ROLES:
            support_seen = True
        if slide.narrative_role in (NarrativeRole.RECOMMENDATION, NarrativeRole.DECISION) and not support_seen:
            code = "UNEXPLAINED_RECOMMENDATION" if slide.narrative_role is NarrativeRole.RECOMMENDATION else "PREMATURE_CONCLUSION"
            findings.append(NarrativeFinding(code, (slide.number,), "supporting bridge has not appeared"))

    problem_indices = [index for index, slide in enumerate(plan.slides) if slide.narrative_role is NarrativeRole.PROBLEM]
    for index in problem_indices:
        if not any(slide.narrative_role in _RESOLUTION_ROLES for slide in plan.slides[index + 1:]):
            findings.append(NarrativeFinding("UNRESOLVED_PROBLEM", (plan.slides[index].number,), "no later resolution role"))

    outcomes = {item.outcome for item in plan.brief.desired_outcomes}
    final_role = plan.slides[-1].narrative_role
    generic_close = plan.closing_strategy.casefold() in {"thank you", "感謝聆聽", "thanks"}
    if (DesiredOutcome.ACT in outcomes and final_role not in (NarrativeRole.ACTION, NarrativeRole.CLOSE)) or (
        DesiredOutcome.DECIDE in outcomes and final_role not in (NarrativeRole.DECISION, NarrativeRole.CLOSE)
    ) or generic_close:
        findings.append(NarrativeFinding("WEAK_CLOSE", (plan.slides[-1].number,), "closing is disconnected from desired outcome"))

    return NarrativeReport(NARRATIVE_WARNING if findings else NARRATIVE_PASS, tuple(findings))


def default_opening_strategy(mode: PresentationMode) -> str:
    strategies = {
        PresentationMode.SALES: "open with a recognizable customer situation",
        PresentationMode.EXECUTIVE: "lead with the conclusion and decision context",
        PresentationMode.TECHNICAL: "open with the failure mode or system constraint",
        PresentationMode.TRAINING: "state the capability participants will gain",
        PresentationMode.KEYNOTE: "establish narrative tension with a strong visual premise",
    }
    return strategies.get(mode, "establish relevance and context directly")


def default_closing_strategy(brief: PresentationBrief) -> str:
    outcomes = {item.outcome for item in brief.desired_outcomes}
    if DesiredOutcome.ACT in outcomes:
        return "end with a clear next action"
    if DesiredOutcome.DECIDE in outcomes:
        return "end with the specific decision requested"
    if DesiredOutcome.REMEMBER in outcomes:
        return "end with a memorable synthesis"
    return "resolve the presentation purpose clearly"


class NarrativeWorkflow:
    """Attach narrative metadata without creating a new approval state machine."""

    def __init__(self, grounded_workflow: GroundedOutlineWorkflow) -> None:
        self.grounded_workflow = grounded_workflow
        self.plan: NarrativePlan | None = None

    def submit(self, plan: NarrativePlan) -> str:
        status = self.grounded_workflow.submit(plan.grounded_outline)
        self.plan = plan
        return status

    def revise_content(self, plan: NarrativePlan) -> str:
        status = self.grounded_workflow.revise_content(plan.grounded_outline)
        self.plan = plan
        return status

    def revise_style(self, style: dict[str, object]) -> str:
        return self.grounded_workflow.revise_style(style)


def user_facing_narrative_message() -> str:
    return "我已依簡報目的安排內容順序，先請您確認大綱方向。"


__all__ = [
    "ERROR_NARRATIVE_INVALID", "NARRATIVE_PASS", "NARRATIVE_WARNING", "NarrativeError",
    "NarrativeFinding", "NarrativePlan", "NarrativeReport", "NarrativeRole", "NarrativeSlide",
    "NarrativeWorkflow", "default_closing_strategy", "default_opening_strategy", "lint_narrative",
    "user_facing_narrative_message",
]

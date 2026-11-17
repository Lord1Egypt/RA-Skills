#!/usr/bin/env python3
"""Phase 16.2 evidence-aware outline planning owned by AGY."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from typing import Any, Iterable, Mapping

from phase16_claims import Claim, ContentOrigin
from presentation_workflow import PresentationApprovalWorkflow, RevisionIntent, UserFacingPrompt, outline_confirmation_prompt


ERROR_OUTLINE_INVALID = "PHASE16_GROUNDED_OUTLINE_INVALID"


class GroundedOutlineError(Exception):
    def __init__(self, message: str, error_code: str = ERROR_OUTLINE_INVALID) -> None:
        super().__init__(message)
        self.error_code = error_code


def _canonical(value: Any) -> str:
    try:
        return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False)
    except (TypeError, ValueError) as exc:
        raise GroundedOutlineError("outline data must be deterministic JSON") from exc


@dataclass(frozen=True)
class GroundedOutlineSlide:
    number: int
    title: str
    purpose: str
    claims: tuple[Claim, ...] = ()
    role: str = "content"

    @classmethod
    def create(cls, number: int, title: str, purpose: str, claims: Iterable[Claim] = (), role: str = "content") -> "GroundedOutlineSlide":
        clean_claims = tuple(claims)
        if type(number) is not int or number < 1 or not isinstance(title, str) or not title.strip():
            raise GroundedOutlineError("slide number and title are required")
        if any(not isinstance(claim, Claim) for claim in clean_claims):
            raise GroundedOutlineError("outline claims are invalid")
        return cls(number, title.strip(), purpose.strip(), clean_claims, role.strip() or "content")

    def public_dict(self) -> dict[str, Any]:
        return {"number": self.number, "purpose": self.purpose, "role": self.role, "title": self.title}

    def internal_dict(self) -> dict[str, Any]:
        return {**self.public_dict(), "claims": [claim.to_dict() for claim in self.claims]}


@dataclass(frozen=True)
class GroundedOutlinePlan:
    plan_id: str
    slides: tuple[GroundedOutlineSlide, ...]

    @classmethod
    def create(cls, slides: Iterable[GroundedOutlineSlide]) -> "GroundedOutlinePlan":
        clean = tuple(slides)
        if not clean or any(not isinstance(slide, GroundedOutlineSlide) for slide in clean):
            raise GroundedOutlineError("outline requires valid slides")
        numbers = [slide.number for slide in clean]
        if len(numbers) != len(set(numbers)):
            raise GroundedOutlineError("slide numbers must be unique")
        payload = [slide.internal_dict() for slide in clean]
        plan_id = "op:" + hashlib.sha256(_canonical(payload).encode("utf-8")).hexdigest()[:16]
        return cls(plan_id, clean)

    @property
    def claims(self) -> tuple[Claim, ...]:
        return tuple(claim for slide in self.slides for claim in slide.claims)

    @property
    def origins(self) -> frozenset[ContentOrigin]:
        return frozenset(claim.origin for claim in self.claims)

    def public_outline(self) -> tuple[dict[str, Any], ...]:
        return tuple(slide.public_dict() for slide in self.slides)


class GroundedOutlineWorkflow:
    """Keep internal provenance beside the existing clean approval UX."""

    def __init__(self, workflow: PresentationApprovalWorkflow) -> None:
        self.workflow = workflow
        self.plan: GroundedOutlinePlan | None = None

    def submit(self, plan: GroundedOutlinePlan) -> str:
        if not isinstance(plan, GroundedOutlinePlan):
            raise GroundedOutlineError("grounded outline plan is invalid")
        status = self.workflow.submit_outline(plan.public_outline())
        self.plan = plan
        return status

    def approve(self) -> str:
        if self.plan is None:
            raise GroundedOutlineError("grounded outline must be submitted first")
        return self.workflow.approve_outline()

    def revise_content(self, plan: GroundedOutlinePlan) -> str:
        if not isinstance(plan, GroundedOutlinePlan):
            raise GroundedOutlineError("grounded outline plan is invalid")
        status = self.workflow.apply_revision(RevisionIntent.CONTENT, outline=plan.public_outline())
        self.plan = plan
        return status

    def revise_style(self, style: Mapping[str, Any]) -> str:
        if self.plan is None:
            raise GroundedOutlineError("grounded outline must be submitted first")
        return self.workflow.apply_revision(RevisionIntent.STYLE_ONLY, style=style)

    def user_prompt(self) -> UserFacingPrompt:
        if self.plan is None:
            raise GroundedOutlineError("grounded outline must be submitted first")
        return outline_confirmation_prompt(self.plan.public_outline())


__all__ = ["GroundedOutlineError", "GroundedOutlinePlan", "GroundedOutlineSlide", "GroundedOutlineWorkflow"]

#!/usr/bin/env python3
"""Phase 17.4 deterministic delivery and rehearsal planning."""

from __future__ import annotations

import hashlib
import json
import math
import re
from dataclasses import dataclass, replace
from enum import Enum
from typing import Iterable

from phase17_narrative import NarrativePlan, NarrativeRole


ERROR_DELIVERY_INVALID = "PHASE17_DELIVERY_INVALID"
DELIVERY_PASS = "PASS"
DELIVERY_WARNING = "WARNING"


class DeliveryError(Exception):
    def __init__(self, error_code: str, message: str) -> None:
        super().__init__(message)
        self.error_code = error_code


class RehearsalCue(str, Enum):
    PAUSE = "PAUSE"
    ASK_AUDIENCE = "ASK_AUDIENCE"
    EMPHASIZE_KEY_NUMBER = "EMPHASIZE_KEY_NUMBER"
    SKIP_TABLE_READING = "SKIP_TABLE_READING"
    SHORTEN_CASE = "SHORTEN_CASE"
    MOVE_QUICKLY = "MOVE_QUICKLY"


_ROLE_WEIGHTS = {
    NarrativeRole.OPEN: 0.55,
    NarrativeRole.CONTEXT: 0.8,
    NarrativeRole.PROBLEM: 1.0,
    NarrativeRole.QUESTION: 0.75,
    NarrativeRole.INSIGHT: 1.2,
    NarrativeRole.EVIDENCE: 1.35,
    NarrativeRole.CASE: 1.45,
    NarrativeRole.CONTRAST: 1.15,
    NarrativeRole.EXPLANATION: 1.25,
    NarrativeRole.RECOMMENDATION: 1.15,
    NarrativeRole.DECISION: 1.25,
    NarrativeRole.ACTION: 1.1,
    NarrativeRole.CLOSE: 0.65,
}


def _clean(value: str, label: str) -> str:
    text = value.strip() if isinstance(value, str) else ""
    if not text:
        raise DeliveryError(ERROR_DELIVERY_INVALID, f"{label} is required")
    return text


def _word_units(text: str) -> int:
    """Conservative, language-neutral approximation for delivery planning."""
    latin = re.findall(r"[A-Za-z0-9%]+(?:[-'][A-Za-z0-9%]+)*", text)
    cjk = re.findall(r"[\u3400-\u9fff]", text)
    return len(latin) + math.ceil(len(cjk) / 2)


@dataclass(frozen=True)
class DeliveryEstimate:
    minimum_seconds: int
    maximum_seconds: int

    def __post_init__(self) -> None:
        if self.minimum_seconds < 0 or self.maximum_seconds < self.minimum_seconds:
            raise DeliveryError(ERROR_DELIVERY_INVALID, "delivery estimate is invalid")


def estimate_delivery(text: str) -> DeliveryEstimate:
    units = _word_units(text)
    # 130-170 spoken units/minute plus a small slide-orientation allowance.
    return DeliveryEstimate(math.ceil(units * 60 / 170) + 4, math.ceil(units * 60 / 130) + 7)


@dataclass(frozen=True)
class DeliveryNotes:
    core_message: str
    opening_cue: str | None = None
    support: str | None = None
    emphasis: str | None = None
    transition: str | None = None

    def __post_init__(self) -> None:
        object.__setattr__(self, "core_message", _clean(self.core_message, "core message"))
        for name in ("opening_cue", "support", "emphasis", "transition"):
            value = getattr(self, name)
            if value is not None:
                object.__setattr__(self, name, _clean(value, name.replace("_", " ")))

    def natural_text(self) -> str:
        return "\n\n".join(value for value in (
            self.opening_cue, self.core_message, self.support, self.emphasis, self.transition
        ) if value)


@dataclass(frozen=True)
class DeliverySlide:
    number: int
    narrative_role: NarrativeRole
    notes: DeliveryNotes
    estimated: DeliveryEstimate
    allocated_seconds: int | None
    cues: tuple[RehearsalCue, ...] = ()

    def __post_init__(self) -> None:
        if self.number <= 0 or not isinstance(self.narrative_role, NarrativeRole):
            raise DeliveryError(ERROR_DELIVERY_INVALID, "delivery slide is invalid")
        if not isinstance(self.notes, DeliveryNotes) or not isinstance(self.estimated, DeliveryEstimate):
            raise DeliveryError(ERROR_DELIVERY_INVALID, "delivery notes and estimate are required")
        if self.allocated_seconds is not None and self.allocated_seconds <= 0:
            raise DeliveryError(ERROR_DELIVERY_INVALID, "allocated time must be positive")
        if any(not isinstance(cue, RehearsalCue) for cue in self.cues):
            raise DeliveryError(ERROR_DELIVERY_INVALID, "rehearsal cue is invalid")


def _allocate(duration: int, roles: tuple[NarrativeRole, ...]) -> tuple[int, ...]:
    weights = tuple(_ROLE_WEIGHTS[role] for role in roles)
    raw = tuple(duration * weight / sum(weights) for weight in weights)
    base = [max(1, math.floor(value)) for value in raw]
    difference = duration - sum(base)
    order = sorted(range(len(raw)), key=lambda index: (raw[index] - math.floor(raw[index]), -index), reverse=True)
    if difference > 0:
        for offset in range(difference):
            base[order[offset % len(order)]] += 1
    elif difference < 0:
        for index in reversed(order):
            while difference < 0 and base[index] > 1:
                base[index] -= 1
                difference += 1
    return tuple(base)


@dataclass(frozen=True)
class DeliveryPlan:
    plan_id: str
    narrative_plan: NarrativePlan
    requested_duration_seconds: int | None
    slides: tuple[DeliverySlide, ...]

    @classmethod
    def create(
        cls,
        narrative_plan: NarrativePlan,
        notes: Iterable[DeliveryNotes],
        cues: Iterable[Iterable[RehearsalCue]] | None = None,
    ) -> "DeliveryPlan":
        if not isinstance(narrative_plan, NarrativePlan):
            raise DeliveryError(ERROR_DELIVERY_INVALID, "narrative plan is required")
        clean_notes = tuple(notes)
        if len(clean_notes) != len(narrative_plan.slides) or any(not isinstance(item, DeliveryNotes) for item in clean_notes):
            raise DeliveryError(ERROR_DELIVERY_INVALID, "one notes entry per slide is required")
        clean_cues = tuple(tuple(items) for items in cues) if cues is not None else tuple(() for _ in clean_notes)
        if len(clean_cues) != len(clean_notes):
            raise DeliveryError(ERROR_DELIVERY_INVALID, "rehearsal cues must match slide count")
        duration = narrative_plan.brief.duration_seconds
        allocations = _allocate(duration, tuple(slide.narrative_role for slide in narrative_plan.slides)) if duration else tuple(None for _ in clean_notes)
        slides = tuple(
            DeliverySlide(
                narrative.number,
                narrative.narrative_role,
                note,
                estimate_delivery(note.natural_text()),
                allocation,
                cue_items,
            )
            for narrative, note, allocation, cue_items in zip(narrative_plan.slides, clean_notes, allocations, clean_cues)
        )
        payload = {
            "narrative_plan_id": narrative_plan.plan_id,
            "duration": duration,
            "slides": [
                {
                    "number": slide.number,
                    "notes": slide.notes.natural_text(),
                    "estimated": [slide.estimated.minimum_seconds, slide.estimated.maximum_seconds],
                    "allocated": slide.allocated_seconds,
                    "cues": [cue.value for cue in slide.cues],
                }
                for slide in slides
            ],
        }
        plan_id = "dp:" + hashlib.sha256(json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()).hexdigest()[:16]
        return cls(plan_id, narrative_plan, duration, slides)

    def cleanup_delivery(self, slide_number: int, notes: DeliveryNotes, cues: Iterable[RehearsalCue] = ()) -> "DeliveryPlan":
        """Change delivery expression only; narrative/evidence identity remains fixed."""
        updated = tuple(notes if slide.number == slide_number else slide.notes for slide in self.slides)
        updated_cues = tuple(tuple(cues) if slide.number == slide_number else slide.cues for slide in self.slides)
        result = DeliveryPlan.create(self.narrative_plan, updated, updated_cues)
        if result.narrative_plan.plan_id != self.narrative_plan.plan_id:
            raise DeliveryError(ERROR_DELIVERY_INVALID, "delivery cleanup changed semantic planning")
        return result


@dataclass(frozen=True)
class DeliveryFinding:
    code: str
    slide_numbers: tuple[int, ...]
    detail: str


@dataclass(frozen=True)
class DeliveryReport:
    status: str
    findings: tuple[DeliveryFinding, ...]

    def count(self, code: str) -> int:
        return sum(item.code == code for item in self.findings)


def validate_timing(plan: DeliveryPlan) -> DeliveryReport:
    if not isinstance(plan, DeliveryPlan):
        raise DeliveryError(ERROR_DELIVERY_INVALID, "delivery plan is invalid")
    if plan.requested_duration_seconds is None:
        return DeliveryReport(DELIVERY_PASS, ())
    requested = plan.requested_duration_seconds
    minimum = sum(slide.estimated.minimum_seconds for slide in plan.slides)
    maximum = sum(slide.estimated.maximum_seconds for slide in plan.slides)
    tolerance = max(30, math.ceil(requested * 0.15))
    findings: list[DeliveryFinding] = []
    if minimum > requested + tolerance:
        findings.append(DeliveryFinding("TIMING_OVERLONG", tuple(slide.number for slide in plan.slides), f"estimated {minimum}-{maximum}s exceeds requested {requested}s"))
    elif maximum < requested - tolerance:
        findings.append(DeliveryFinding("TIMING_UNDERFILLED", tuple(slide.number for slide in plan.slides), f"estimated {minimum}-{maximum}s is below requested {requested}s"))
    return DeliveryReport(DELIVERY_WARNING if findings else DELIVERY_PASS, tuple(findings))


def semantic_change_requires_approval(change: str) -> bool:
    return change in {"add_slide", "remove_slide", "reorder_slide", "change_takeaway", "change_recommendation", "change_fact", "change_thesis"}


def user_facing_delivery_message(report: DeliveryReport) -> str:
    if report.count("TIMING_OVERLONG"):
        return "目前內容可能超過預定時間，我會先調整內容或請您確認取捨。"
    return "我已依簡報情境安排講述節奏與提示。"


__all__ = [
    "DELIVERY_PASS", "DELIVERY_WARNING", "ERROR_DELIVERY_INVALID", "DeliveryError",
    "DeliveryEstimate", "DeliveryFinding", "DeliveryNotes", "DeliveryPlan", "DeliveryReport",
    "DeliverySlide", "RehearsalCue", "estimate_delivery", "semantic_change_requires_approval",
    "user_facing_delivery_message", "validate_timing",
]

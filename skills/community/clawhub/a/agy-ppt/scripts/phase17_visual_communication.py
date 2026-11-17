#!/usr/bin/env python3
"""Phase 17.3 deterministic visual-communication planning metadata."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from enum import Enum
from typing import Iterable

from phase16_claims import Claim, ContentOrigin
from phase17_narrative import NarrativePlan, NarrativeRole, NarrativeSlide


ERROR_VISUAL_COMMUNICATION_INVALID = "PHASE17_VISUAL_COMMUNICATION_INVALID"
ERROR_UNSUPPORTED_CHART_DATA = "PHASE17_UNSUPPORTED_CHART_DATA"
VISUAL_COMMUNICATION_PASS = "PASS"
VISUAL_COMMUNICATION_WARNING = "WARNING"


class VisualCommunicationError(Exception):
    def __init__(self, error_code: str, message: str) -> None:
        super().__init__(message)
        self.error_code = error_code


class CommunicationObjective(str, Enum):
    COMPARISON = "COMPARISON"
    TIME_SEQUENCE = "TIME_SEQUENCE"
    PROCESS = "PROCESS"
    SINGLE_MESSAGE = "SINGLE_MESSAGE"
    QUANTITATIVE_TREND = "QUANTITATIVE_TREND"
    CASE = "CASE"
    DECISION = "DECISION"


class InformationForm(str, Enum):
    STATEMENT = "STATEMENT"
    IMAGE_LED = "IMAGE_LED"
    COMPARISON = "COMPARISON"
    MATRIX = "MATRIX"
    TABLE = "TABLE"
    TIMELINE = "TIMELINE"
    PROCESS = "PROCESS"
    FLOW = "FLOW"
    CHART = "CHART"
    DATA_CALLOUT = "DATA_CALLOUT"
    CASE_STUDY = "CASE_STUDY"
    QUOTE = "QUOTE"
    BEFORE_AFTER = "BEFORE_AFTER"
    DECISION_OPTIONS = "DECISION_OPTIONS"


class HierarchyLevel(str, Enum):
    PRIMARY = "PRIMARY"
    SECONDARY = "SECONDARY"
    SUPPORTING = "SUPPORTING"


class ImagePurpose(str, Enum):
    CONTEXT = "CONTEXT"
    EVIDENCE = "EVIDENCE"
    EXAMPLE = "EXAMPLE"
    EMOTION = "EMOTION"
    IDENTITY = "IDENTITY"
    DECORATION = "DECORATION"


_VALID_FOR_OBJECTIVE = {
    CommunicationObjective.COMPARISON: frozenset({InformationForm.COMPARISON, InformationForm.MATRIX, InformationForm.TABLE, InformationForm.BEFORE_AFTER}),
    CommunicationObjective.TIME_SEQUENCE: frozenset({InformationForm.TIMELINE, InformationForm.FLOW, InformationForm.CHART}),
    CommunicationObjective.PROCESS: frozenset({InformationForm.PROCESS, InformationForm.FLOW}),
    CommunicationObjective.SINGLE_MESSAGE: frozenset({InformationForm.STATEMENT, InformationForm.IMAGE_LED, InformationForm.DATA_CALLOUT, InformationForm.QUOTE}),
    CommunicationObjective.QUANTITATIVE_TREND: frozenset({InformationForm.CHART, InformationForm.DATA_CALLOUT}),
    CommunicationObjective.CASE: frozenset({InformationForm.CASE_STUDY, InformationForm.BEFORE_AFTER}),
    CommunicationObjective.DECISION: frozenset({InformationForm.DECISION_OPTIONS, InformationForm.COMPARISON, InformationForm.MATRIX, InformationForm.TABLE}),
}


def select_information_form(objective: CommunicationObjective) -> InformationForm:
    if not isinstance(objective, CommunicationObjective):
        raise VisualCommunicationError(ERROR_VISUAL_COMMUNICATION_INVALID, "communication objective is invalid")
    return {
        CommunicationObjective.COMPARISON: InformationForm.COMPARISON,
        CommunicationObjective.TIME_SEQUENCE: InformationForm.TIMELINE,
        CommunicationObjective.PROCESS: InformationForm.PROCESS,
        CommunicationObjective.SINGLE_MESSAGE: InformationForm.STATEMENT,
        CommunicationObjective.QUANTITATIVE_TREND: InformationForm.CHART,
        CommunicationObjective.CASE: InformationForm.CASE_STUDY,
        CommunicationObjective.DECISION: InformationForm.DECISION_OPTIONS,
    }[objective]


def _clean(value: str, label: str) -> str:
    text = value.strip() if isinstance(value, str) else ""
    if not text:
        raise VisualCommunicationError(ERROR_VISUAL_COMMUNICATION_INVALID, f"{label} is required")
    return text


@dataclass(frozen=True)
class HierarchyElement:
    name: str
    level: HierarchyLevel

    def __post_init__(self) -> None:
        object.__setattr__(self, "name", _clean(self.name, "hierarchy element name"))
        if not isinstance(self.level, HierarchyLevel):
            raise VisualCommunicationError(ERROR_VISUAL_COMMUNICATION_INVALID, "hierarchy level is invalid")


@dataclass(frozen=True)
class ImageIntent:
    purpose: ImagePurpose
    description: str
    supports_takeaway: bool
    generic: bool = False

    def __post_init__(self) -> None:
        if not isinstance(self.purpose, ImagePurpose) or not isinstance(self.supports_takeaway, bool) or not isinstance(self.generic, bool):
            raise VisualCommunicationError(ERROR_VISUAL_COMMUNICATION_INVALID, "image intent is invalid")
        object.__setattr__(self, "description", _clean(self.description, "image description"))


@dataclass(frozen=True)
class DataStory:
    fact: Claim
    context: str
    comparison: str | None
    meaning: Claim
    decision_relevance: Claim

    def __post_init__(self) -> None:
        if any(not isinstance(item, Claim) for item in (self.fact, self.meaning, self.decision_relevance)):
            raise VisualCommunicationError(ERROR_VISUAL_COMMUNICATION_INVALID, "data story claims are invalid")
        object.__setattr__(self, "context", _clean(self.context, "data context"))
        if self.comparison is not None:
            object.__setattr__(self, "comparison", _clean(self.comparison, "data comparison"))


@dataclass(frozen=True)
class VisualCommunicationSlide:
    number: int
    narrative_role: NarrativeRole
    objective: CommunicationObjective
    information_form: InformationForm
    hierarchy: tuple[HierarchyElement, ...]
    image: ImageIntent | None = None
    data_story: DataStory | None = None
    approved_style_constraints: tuple[str, ...] = ()
    observed_dominant_element: str | None = None

    @classmethod
    def create(
        cls,
        narrative_slide: NarrativeSlide,
        objective: CommunicationObjective,
        information_form: InformationForm,
        hierarchy: Iterable[HierarchyElement],
        *,
        image: ImageIntent | None = None,
        data_story: DataStory | None = None,
        approved_style_constraints: Iterable[str] = (),
        observed_dominant_element: str | None = None,
    ) -> "VisualCommunicationSlide":
        if not isinstance(narrative_slide, NarrativeSlide) or not isinstance(objective, CommunicationObjective) or not isinstance(information_form, InformationForm):
            raise VisualCommunicationError(ERROR_VISUAL_COMMUNICATION_INVALID, "visual communication input is invalid")
        clean_hierarchy = tuple(hierarchy)
        if not clean_hierarchy or any(not isinstance(item, HierarchyElement) for item in clean_hierarchy):
            raise VisualCommunicationError(ERROR_VISUAL_COMMUNICATION_INVALID, "visual hierarchy is required")
        if sum(item.level is HierarchyLevel.PRIMARY for item in clean_hierarchy) != 1:
            raise VisualCommunicationError(ERROR_VISUAL_COMMUNICATION_INVALID, "visual hierarchy requires exactly one primary element")
        if image is not None and not isinstance(image, ImageIntent):
            raise VisualCommunicationError(ERROR_VISUAL_COMMUNICATION_INVALID, "image intent is invalid")
        if data_story is not None and not isinstance(data_story, DataStory):
            raise VisualCommunicationError(ERROR_VISUAL_COMMUNICATION_INVALID, "data story is invalid")
        if information_form is InformationForm.CHART:
            plan = narrative_slide.evidence_plan
            if plan is None or not any(material.facts for material in plan.claims):
                raise VisualCommunicationError(ERROR_UNSUPPORTED_CHART_DATA, "charts require evidence-safe quantitative data")
        constraints = tuple(_clean(item, "style constraint") for item in approved_style_constraints)
        observed = observed_dominant_element.strip() if isinstance(observed_dominant_element, str) and observed_dominant_element.strip() else None
        return cls(narrative_slide.number, narrative_slide.narrative_role, objective, information_form, clean_hierarchy, image, data_story, constraints, observed)

    @property
    def primary_element(self) -> str:
        return next(item.name for item in self.hierarchy if item.level is HierarchyLevel.PRIMARY)

    def internal_dict(self) -> dict[str, object]:
        return {
            "number": self.number,
            "narrative_role": self.narrative_role.value,
            "objective": self.objective.value,
            "information_form": self.information_form.value,
            "hierarchy": [{"name": item.name, "level": item.level.value} for item in self.hierarchy],
            "image_purpose": self.image.purpose.value if self.image else None,
            "data_story_origins": [
                self.data_story.fact.origin.value,
                self.data_story.meaning.origin.value,
                self.data_story.decision_relevance.origin.value,
            ] if self.data_story else None,
            "approved_style_constraints": list(self.approved_style_constraints),
        }


@dataclass(frozen=True)
class VisualCommunicationPlan:
    plan_id: str
    narrative_plan: NarrativePlan
    slides: tuple[VisualCommunicationSlide, ...]

    @classmethod
    def create(cls, narrative_plan: NarrativePlan, slides: Iterable[VisualCommunicationSlide]) -> "VisualCommunicationPlan":
        clean = tuple(slides)
        if not isinstance(narrative_plan, NarrativePlan) or not clean or any(not isinstance(item, VisualCommunicationSlide) for item in clean):
            raise VisualCommunicationError(ERROR_VISUAL_COMMUNICATION_INVALID, "visual communication plan is invalid")
        if tuple(item.number for item in clean) != tuple(item.number for item in narrative_plan.slides):
            raise VisualCommunicationError(ERROR_VISUAL_COMMUNICATION_INVALID, "visual slides must match narrative order")
        payload = {"narrative_plan_id": narrative_plan.plan_id, "slides": [item.internal_dict() for item in clean]}
        plan_id = "vp:" + hashlib.sha256(json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()[:16]
        return cls(plan_id, narrative_plan, clean)


@dataclass(frozen=True)
class VisualCommunicationFinding:
    code: str
    slide_numbers: tuple[int, ...]
    detail: str


@dataclass(frozen=True)
class VisualCommunicationReport:
    status: str
    findings: tuple[VisualCommunicationFinding, ...]

    def count(self, code: str) -> int:
        return sum(item.code == code for item in self.findings)


def lint_visual_communication(plan: VisualCommunicationPlan) -> VisualCommunicationReport:
    findings: list[VisualCommunicationFinding] = []
    generic_images: list[int] = []
    for slide in plan.slides:
        if slide.information_form not in _VALID_FOR_OBJECTIVE[slide.objective]:
            findings.append(VisualCommunicationFinding("INFORMATION_FORM_MISMATCH", (slide.number,), f"{slide.objective.value}/{slide.information_form.value}"))
        if slide.observed_dominant_element is not None and slide.observed_dominant_element != slide.primary_element:
            findings.append(VisualCommunicationFinding("HIERARCHY_MISMATCH", (slide.number,), slide.observed_dominant_element))
        if slide.image is not None and slide.image.generic:
            generic_images.append(slide.number)
            if not slide.image.supports_takeaway:
                findings.append(VisualCommunicationFinding("IMAGE_IRRELEVANT", (slide.number,), slide.image.description))
    image_count = sum(slide.image is not None for slide in plan.slides)
    if image_count >= 3 and len(generic_images) / image_count >= 0.75:
        findings.append(VisualCommunicationFinding("GENERIC_IMAGE_OVERUSE", tuple(generic_images), "generic imagery dominates"))
    status = VISUAL_COMMUNICATION_WARNING if findings else VISUAL_COMMUNICATION_PASS
    return VisualCommunicationReport(status, tuple(findings))


def user_facing_visual_message() -> str:
    return "我會選擇最適合內容重點的呈現方式，並遵守您核准的視覺方向。"


__all__ = [
    "ERROR_UNSUPPORTED_CHART_DATA", "ERROR_VISUAL_COMMUNICATION_INVALID", "CommunicationObjective",
    "DataStory", "HierarchyElement", "HierarchyLevel", "ImageIntent", "ImagePurpose", "InformationForm",
    "VisualCommunicationError", "VisualCommunicationFinding", "VisualCommunicationPlan",
    "VisualCommunicationReport", "VisualCommunicationSlide", "lint_visual_communication",
    "select_information_form", "user_facing_visual_message",
]

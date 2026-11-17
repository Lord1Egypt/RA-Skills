#!/usr/bin/env python3
"""Phase 17.5 final presentation-effectiveness QA.

This layer composes communication findings with, but never replaces, Phase 16
evidence and editorial integrity.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from phase16_editorial import EditorialReport
from phase16_traceability import FinalTraceabilityReport
from phase17_delivery import DeliveryPlan, validate_timing
from phase17_narrative import NarrativePlan, lint_narrative
from phase17_visual_communication import VisualCommunicationPlan, lint_visual_communication


ERROR_EFFECTIVENESS_INVALID = "PHASE17_EFFECTIVENESS_INVALID"
ERROR_PRESENTATION_NOT_READY = "PHASE17_PRESENTATION_NOT_READY"


class EffectivenessError(Exception):
    def __init__(self, error_code: str, message: str) -> None:
        super().__init__(message)
        self.error_code = error_code


class QAStatus(str, Enum):
    PASS = "PASS"
    WARNING = "WARNING"
    REVIEW_REQUIRED = "REVIEW_REQUIRED"


class QACategory(str, Enum):
    AUDIENCE_FIT = "AUDIENCE_FIT"
    PURPOSE_ALIGNMENT = "PURPOSE_ALIGNMENT"
    DESIRED_OUTCOME = "DESIRED_OUTCOME"
    NARRATIVE_CONTINUITY = "NARRATIVE_CONTINUITY"
    SLIDE_INTENT = "SLIDE_INTENT"
    TAKEAWAY_QUALITY = "TAKEAWAY_QUALITY"
    REDUNDANCY = "REDUNDANCY"
    OPENING = "OPENING"
    CLOSING = "CLOSING"
    TIMING = "TIMING"
    VISUAL_HIERARCHY = "VISUAL_HIERARCHY"
    IMAGE_RELEVANCE = "IMAGE_RELEVANCE"
    INFORMATION_FORM = "INFORMATION_FORM"
    DATA_STORY = "DATA_STORY"
    TRANSITION = "TRANSITION"
    DELIVERY_READINESS = "DELIVERY_READINESS"
    EVIDENCE_INTEGRITY = "EVIDENCE_INTEGRITY"
    EDITORIAL_INTEGRITY = "EDITORIAL_INTEGRITY"
    APPROVAL = "APPROVAL"
    FINAL_ARTIFACT = "FINAL_ARTIFACT"


class ProposedChange(str, Enum):
    NOTES_CLEANUP = "NOTES_CLEANUP"
    TRANSITION_WORDING = "TRANSITION_WORDING"
    REHEARSAL_CUE_WORDING = "REHEARSAL_CUE_WORDING"
    TIMING_ANNOTATION = "TIMING_ANNOTATION"
    ADD_SLIDE = "ADD_SLIDE"
    REMOVE_SLIDE = "REMOVE_SLIDE"
    REORDER_SLIDES = "REORDER_SLIDES"
    CHANGE_TAKEAWAY = "CHANGE_TAKEAWAY"
    CHANGE_RECOMMENDATION = "CHANGE_RECOMMENDATION"
    CHANGE_FACT = "CHANGE_FACT"
    CHANGE_THESIS = "CHANGE_THESIS"
    SUBSTANTIVE_VISUAL_DIRECTION = "SUBSTANTIVE_VISUAL_DIRECTION"


@dataclass(frozen=True)
class ChangeDisposition:
    safe_auto_fix: bool
    required_approval: str | None


def classify_change(change: ProposedChange) -> ChangeDisposition:
    if not isinstance(change, ProposedChange):
        raise EffectivenessError(ERROR_EFFECTIVENESS_INVALID, "proposed change is invalid")
    if change in {
        ProposedChange.NOTES_CLEANUP,
        ProposedChange.TRANSITION_WORDING,
        ProposedChange.REHEARSAL_CUE_WORDING,
        ProposedChange.TIMING_ANNOTATION,
    }:
        return ChangeDisposition(True, None)
    if change is ProposedChange.SUBSTANTIVE_VISUAL_DIRECTION:
        return ChangeDisposition(False, "STYLE_SAMPLE")
    return ChangeDisposition(False, "OUTLINE_CONTENT")


@dataclass(frozen=True)
class EffectivenessSignals:
    audience_fit: bool = True
    purpose_aligned: bool = True
    desired_outcome_clear: bool = True
    opening_effective: bool = True
    closing_effective: bool = True
    takeaway_quality: bool = True
    data_story_aligned: bool = True
    transitions_usable: bool = True
    delivery_ready: bool = True


@dataclass(frozen=True)
class EffectivenessFinding:
    code: str
    category: QACategory
    status: QAStatus
    slide_numbers: tuple[int, ...]
    detail: str


@dataclass(frozen=True)
class EffectivenessReport:
    status: QAStatus
    findings: tuple[EffectivenessFinding, ...]
    ready: bool

    def count(self, code: str) -> int:
        return sum(item.code == code for item in self.findings)

    def require_ready(self) -> None:
        if not self.ready:
            raise EffectivenessError(ERROR_PRESENTATION_NOT_READY, "blocking presentation findings require review")

    def internal_dict(self) -> dict[str, object]:
        return {
            "status": self.status.value,
            "ready": self.ready,
            "findings": [
                {
                    "code": item.code,
                    "category": item.category.value,
                    "status": item.status.value,
                    "slide_numbers": list(item.slide_numbers),
                    "detail": item.detail,
                }
                for item in self.findings
            ],
        }


_NARRATIVE_CATEGORY = {
    "DUPLICATE_SLIDE_PURPOSE": QACategory.REDUNDANCY,
    "REPEATED_NARRATIVE_ROLE": QACategory.REDUNDANCY,
    "WEAK_SLIDE_INTENT": QACategory.SLIDE_INTENT,
    "MISSING_BRIDGE": QACategory.NARRATIVE_CONTINUITY,
    "UNEXPLAINED_RECOMMENDATION": QACategory.NARRATIVE_CONTINUITY,
    "PREMATURE_CONCLUSION": QACategory.NARRATIVE_CONTINUITY,
    "UNRESOLVED_PROBLEM": QACategory.NARRATIVE_CONTINUITY,
    "WEAK_CLOSE": QACategory.CLOSING,
}

_VISUAL_CATEGORY = {
    "INFORMATION_FORM_MISMATCH": QACategory.INFORMATION_FORM,
    "HIERARCHY_MISMATCH": QACategory.VISUAL_HIERARCHY,
    "IMAGE_IRRELEVANT": QACategory.IMAGE_RELEVANCE,
    "GENERIC_IMAGE_OVERUSE": QACategory.IMAGE_RELEVANCE,
}


def evaluate_effectiveness(
    narrative_plan: NarrativePlan,
    visual_plan: VisualCommunicationPlan,
    delivery_plan: DeliveryPlan,
    traceability: FinalTraceabilityReport,
    editorial: EditorialReport,
    *,
    signals: EffectivenessSignals = EffectivenessSignals(),
    proposed_change: ProposedChange | None = None,
    final_artifact_present: bool = True,
    timing_mismatch_blocks: bool = True,
) -> EffectivenessReport:
    if not isinstance(narrative_plan, NarrativePlan) or visual_plan.narrative_plan.plan_id != narrative_plan.plan_id:
        raise EffectivenessError(ERROR_EFFECTIVENESS_INVALID, "visual planning does not match narrative planning")
    if delivery_plan.narrative_plan.plan_id != narrative_plan.plan_id:
        raise EffectivenessError(ERROR_EFFECTIVENESS_INVALID, "delivery planning does not match narrative planning")
    if not isinstance(traceability, FinalTraceabilityReport) or not isinstance(editorial, EditorialReport):
        raise EffectivenessError(ERROR_EFFECTIVENESS_INVALID, "Phase 16 integrity reports are required")
    if not isinstance(signals, EffectivenessSignals):
        raise EffectivenessError(ERROR_EFFECTIVENESS_INVALID, "effectiveness signals are invalid")

    narrative = lint_narrative(narrative_plan)
    visual = lint_visual_communication(visual_plan)
    timing = validate_timing(delivery_plan)
    findings: list[EffectivenessFinding] = []

    for item in narrative.findings:
        findings.append(EffectivenessFinding(item.code, _NARRATIVE_CATEGORY.get(item.code, QACategory.NARRATIVE_CONTINUITY), QAStatus.WARNING, item.slide_numbers, item.detail))
    for item in visual.findings:
        findings.append(EffectivenessFinding(item.code, _VISUAL_CATEGORY.get(item.code, QACategory.INFORMATION_FORM), QAStatus.WARNING, item.slide_numbers, item.detail))
    for item in timing.findings:
        # Overrunning a declared limit makes a readiness claim dishonest. Spare
        # time is useful editorial feedback, but is not itself unsafe.
        status = QAStatus.REVIEW_REQUIRED if timing_mismatch_blocks and item.code == "TIMING_OVERLONG" else QAStatus.WARNING
        findings.append(EffectivenessFinding(item.code, QACategory.TIMING, status, item.slide_numbers, item.detail))

    checks = (
        (signals.audience_fit, "AUDIENCE_MISMATCH", QACategory.AUDIENCE_FIT),
        (signals.purpose_aligned, "PURPOSE_MISMATCH", QACategory.PURPOSE_ALIGNMENT),
        (signals.desired_outcome_clear, "DESIRED_OUTCOME_UNCLEAR", QACategory.DESIRED_OUTCOME),
        (signals.opening_effective, "WEAK_OPEN", QACategory.OPENING),
        (signals.closing_effective, "WEAK_CLOSE", QACategory.CLOSING),
        (signals.takeaway_quality, "WEAK_TAKEAWAY", QACategory.TAKEAWAY_QUALITY),
        (signals.data_story_aligned, "DATA_STORY_MISALIGNED", QACategory.DATA_STORY),
        (signals.transitions_usable, "WEAK_TRANSITION", QACategory.TRANSITION),
        (signals.delivery_ready, "DELIVERY_NOT_READY", QACategory.DELIVERY_READINESS),
    )
    for passed, code, category in checks:
        if not passed and not any(item.code == code for item in findings):
            findings.append(EffectivenessFinding(code, category, QAStatus.WARNING, (), code.replace("_", " ").lower()))

    if not traceability.evidence_complete:
        findings.append(EffectivenessFinding("PHASE16_EVIDENCE_INCOMPLETE", QACategory.EVIDENCE_INTEGRITY, QAStatus.REVIEW_REQUIRED, (), "unsupported or stale evidence remains"))
    for code in traceability.editorial_warnings:
        findings.append(EffectivenessFinding(code, QACategory.EDITORIAL_INTEGRITY, QAStatus.WARNING, (), "Phase 16 editorial warning"))
    if editorial.warnings and not traceability.editorial_warnings:
        for warning in editorial.warnings:
            numbers = tuple(int(value.rsplit("_", 1)[-1]) for value in warning.slide_ids if value.rsplit("_", 1)[-1].isdigit())
            findings.append(EffectivenessFinding(warning.code, QACategory.EDITORIAL_INTEGRITY, QAStatus.WARNING, numbers, warning.detail))

    if proposed_change is not None:
        disposition = classify_change(proposed_change)
        if disposition.required_approval:
            findings.append(EffectivenessFinding("APPROVAL_REQUIRED", QACategory.APPROVAL, QAStatus.REVIEW_REQUIRED, (), disposition.required_approval))
    if not final_artifact_present:
        findings.append(EffectivenessFinding("FINAL_ARTIFACT_MISSING", QACategory.FINAL_ARTIFACT, QAStatus.REVIEW_REQUIRED, (), "required final artifact is absent"))

    ordered = tuple(sorted(findings, key=lambda item: (item.status.value, item.category.value, item.code, item.slide_numbers)))
    blocking = any(item.status is QAStatus.REVIEW_REQUIRED for item in ordered)
    status = QAStatus.REVIEW_REQUIRED if blocking else (QAStatus.WARNING if ordered else QAStatus.PASS)
    return EffectivenessReport(status, ordered, not blocking)


def user_facing_effectiveness_message(report: EffectivenessReport) -> str:
    return "簡報已完成內容、節奏與呈現檢查。" if report.ready else "簡報仍有需要確認的內容或時間安排。"


__all__ = [
    "ERROR_EFFECTIVENESS_INVALID", "ERROR_PRESENTATION_NOT_READY", "ChangeDisposition",
    "EffectivenessError", "EffectivenessFinding", "EffectivenessReport", "EffectivenessSignals",
    "ProposedChange", "QACategory", "QAStatus", "classify_change", "evaluate_effectiveness",
    "user_facing_effectiveness_message",
]

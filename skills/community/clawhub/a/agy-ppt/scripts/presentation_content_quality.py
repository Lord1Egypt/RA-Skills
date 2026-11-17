#!/usr/bin/env python3
"""Deterministic v0.6 presentation-content preflight.

This maintenance layer surfaces mechanical or weak presentation copy without
rewriting approved meaning.  AGY remains the semantic authority; factual
support remains owned by Phase 16 evidence contracts.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from enum import Enum
from typing import Iterable

from phase16_editorial import JARGON_SIGNALS, PresentationMode
from phase16_slide_evidence import SlideEvidenceError, SlideEvidencePlan
from phase17_narrative import NarrativeRole


ERROR_CONTENT_QUALITY_INVALID = "PRESENTATION_CONTENT_QUALITY_INVALID"


class HeadlineKind(str, Enum):
    LABEL_ONLY = "LABEL_ONLY"
    ASSERTION = "ASSERTION"
    QUESTION = "QUESTION"
    DECISION_FRAME = "DECISION_FRAME"
    ACTION_FRAME = "ACTION_FRAME"
    OTHER = "OTHER"


class ContentQualityStatus(str, Enum):
    PASS = "PASS"
    REVIEW_REQUIRED = "REVIEW_REQUIRED"
    BLOCK = "BLOCK"


class ContentQualityCode(str, Enum):
    LABEL_ONLY_HEADLINE = "LABEL_ONLY_HEADLINE"
    GENERIC_LANGUAGE = "GENERIC_LANGUAGE"
    CONTENT_DENSITY = "CONTENT_DENSITY"
    REPETITIVE_COPY = "REPETITIVE_COPY"
    NARRATIVE_COPY_MISALIGNED = "NARRATIVE_COPY_MISALIGNED"
    EVIDENCE_INTEGRITY_BLOCK = "EVIDENCE_INTEGRITY_BLOCK"


_LABEL_SUFFIXES = (
    "指標", "分析", "概況", "背景", "介紹", "概覽", "策略", "計畫", "成果", "趨勢",
    "metrics", "analysis", "overview", "background", "introduction", "strategy", "plan", "results", "trends",
)
_ACTION_PREFIXES = (
    "本週", "下一步", "先", "立即", "請", "開始", "確認", "執行",
    "next", "start", "choose", "confirm", "act", "do ",
)
_DECISION_SIGNALS = (
    "現在要決定", "是否", "需要決定", "決策", "決定是否",
    "decision", "decide whether", "should we", "choose between",
)
_QUESTION_PREFIXES = (
    "如何", "為什麼", "哪些", "什麼", "是否", "誰", "何時",
    "how ", "why ", "what ", "which ", "when ", "should ", "can ",
)
_ABSTRACT_SIGNALS = JARGON_SIGNALS + (
    "引領未來", "全面升級", "新篇章", "無限可能", "協同效應", "成長引擎",
    "unlock value", "transformative", "best-in-class", "synergy", "next-generation",
)
_CONCRETE_TOKEN = re.compile(r"(?:\d|%|Q[1-4]\b|\b(?:day|week|month|year)s?\b|天|週|月|年)", re.IGNORECASE)


def _clean(value: str, label: str) -> str:
    result = value.strip() if isinstance(value, str) else ""
    if not result:
        raise ValueError(f"{ERROR_CONTENT_QUALITY_INVALID}: {label}")
    return result


def classify_headline_shape(title: str) -> HeadlineKind:
    """Classify expression only; never decide whether an assertion is sourced."""
    clean = _clean(title, "headline is required")
    folded = clean.casefold()
    if any(folded.startswith(prefix.casefold()) for prefix in _ACTION_PREFIXES):
        return HeadlineKind.ACTION_FRAME
    if any(signal.casefold() in folded for signal in _DECISION_SIGNALS):
        return HeadlineKind.DECISION_FRAME
    if clean.endswith(("?", "？")) or any(folded.startswith(prefix.casefold()) for prefix in _QUESTION_PREFIXES):
        return HeadlineKind.QUESTION
    compact_limit = 18 if any("\u3400" <= char <= "\u9fff" for char in clean) else 36
    if (
        len(clean) <= compact_limit
        and not _CONCRETE_TOKEN.search(clean)
        and any(folded.endswith(suffix.casefold()) for suffix in _LABEL_SUFFIXES)
    ):
        return HeadlineKind.LABEL_ONLY
    return HeadlineKind.ASSERTION


@dataclass(frozen=True)
class ContentQualitySlide:
    slide_id: str
    title: str
    key_points: tuple[str, ...]
    narrative_role: NarrativeRole | None = None
    intent: str | None = None
    takeaway: str | None = None
    evidence_plan: SlideEvidencePlan | None = None

    def __post_init__(self) -> None:
        if not re.fullmatch(r"slide_\d+", self.slide_id or ""):
            raise ValueError(ERROR_CONTENT_QUALITY_INVALID)
        object.__setattr__(self, "title", _clean(self.title, "title is required"))
        points = tuple(_clean(item, "key point is empty") for item in self.key_points)
        object.__setattr__(self, "key_points", points)
        if self.narrative_role is not None and not isinstance(self.narrative_role, NarrativeRole):
            raise ValueError(ERROR_CONTENT_QUALITY_INVALID)
        if self.evidence_plan is not None and self.evidence_plan.slide_id != self.slide_id:
            raise ValueError(ERROR_CONTENT_QUALITY_INVALID)

    @property
    def copy(self) -> str:
        return "\n".join((self.title, *self.key_points))


@dataclass(frozen=True)
class ContentQualityFinding:
    code: ContentQualityCode
    status: ContentQualityStatus
    slide_ids: tuple[str, ...]
    detail: str


@dataclass(frozen=True)
class ContentQualityReport:
    status: ContentQualityStatus
    findings: tuple[ContentQualityFinding, ...]

    def count(self, code: ContentQualityCode | None = None) -> int:
        return sum(1 for item in self.findings if code is None or item.code is code)

    @property
    def requires_content_revision(self) -> bool:
        return self.status is not ContentQualityStatus.PASS


def _generic_signal_count(copy: str) -> int:
    folded = copy.casefold()
    return sum(folded.count(signal.casefold()) for signal in _ABSTRACT_SIGNALS)


def _narrative_expression_aligned(slide: ContentQualitySlide, kind: HeadlineKind) -> bool:
    role = slide.narrative_role
    if role is NarrativeRole.ACTION:
        return kind is HeadlineKind.ACTION_FRAME
    if role is NarrativeRole.DECISION:
        return kind is HeadlineKind.DECISION_FRAME
    if role in {NarrativeRole.EVIDENCE, NarrativeRole.INSIGHT, NarrativeRole.RECOMMENDATION}:
        return kind not in {HeadlineKind.LABEL_ONLY, HeadlineKind.OTHER}
    return True


def audit_presentation_content(
    slides: Iterable[ContentQualitySlide],
    mode: PresentationMode,
) -> ContentQualityReport:
    clean = tuple(slides)
    if not clean or any(not isinstance(item, ContentQualitySlide) for item in clean):
        raise ValueError(ERROR_CONTENT_QUALITY_INVALID)
    if not isinstance(mode, PresentationMode):
        raise ValueError(ERROR_CONTENT_QUALITY_INVALID)
    findings: list[ContentQualityFinding] = []
    title_index: dict[str, list[str]] = {}
    for slide in clean:
        title_index.setdefault(slide.title.casefold(), []).append(slide.slide_id)
        kind = classify_headline_shape(slide.title)
        if kind is HeadlineKind.LABEL_ONLY and slide.narrative_role not in {NarrativeRole.OPEN, NarrativeRole.CONTEXT, NarrativeRole.CLOSE}:
            findings.append(ContentQualityFinding(
                ContentQualityCode.LABEL_ONLY_HEADLINE,
                ContentQualityStatus.REVIEW_REQUIRED,
                (slide.slide_id,),
                "headline names a topic but does not communicate a point",
            ))
        if not _narrative_expression_aligned(slide, kind):
            findings.append(ContentQualityFinding(
                ContentQualityCode.NARRATIVE_COPY_MISALIGNED,
                ContentQualityStatus.REVIEW_REQUIRED,
                (slide.slide_id,),
                f"{slide.narrative_role.value} slide uses {kind.value} headline expression",
            ))
        signal_count = _generic_signal_count(slide.copy)
        if signal_count >= 3 and not _CONCRETE_TOKEN.search(slide.copy):
            findings.append(ContentQualityFinding(
                ContentQualityCode.GENERIC_LANGUAGE,
                ContentQualityStatus.REVIEW_REQUIRED,
                (slide.slide_id,),
                f"{signal_count} abstract or slogan-like signals without a concrete anchor",
            ))
        max_points = 6 if mode is PresentationMode.TECHNICAL else 4
        max_copy = 360 if mode is PresentationMode.TECHNICAL else 240
        if len(slide.key_points) > max_points or len(slide.copy) > max_copy or any(len(point) > 90 for point in slide.key_points):
            findings.append(ContentQualityFinding(
                ContentQualityCode.CONTENT_DENSITY,
                ContentQualityStatus.REVIEW_REQUIRED,
                (slide.slide_id,),
                "approved copy exceeds the mode-aware presentation density envelope",
            ))
        if slide.evidence_plan is not None:
            try:
                slide.evidence_plan.validate_rendered_text(slide.copy)
            except SlideEvidenceError as exc:
                findings.append(ContentQualityFinding(
                    ContentQualityCode.EVIDENCE_INTEGRITY_BLOCK,
                    ContentQualityStatus.BLOCK,
                    (slide.slide_id,),
                    exc.error_code,
                ))
    for _, ids in sorted(title_index.items()):
        if len(ids) > 1:
            findings.append(ContentQualityFinding(
                ContentQualityCode.REPETITIVE_COPY,
                ContentQualityStatus.REVIEW_REQUIRED,
                tuple(ids),
                "the same headline is reused across multiple slides",
            ))
    ordered = tuple(sorted(findings, key=lambda item: (item.slide_ids, item.code.value)))
    status = (
        ContentQualityStatus.BLOCK
        if any(item.status is ContentQualityStatus.BLOCK for item in ordered)
        else ContentQualityStatus.REVIEW_REQUIRED
        if ordered
        else ContentQualityStatus.PASS
    )
    return ContentQualityReport(status, ordered)


def user_facing_content_quality_message(report: ContentQualityReport) -> str:
    if not isinstance(report, ContentQualityReport):
        raise ValueError(ERROR_CONTENT_QUALITY_INVALID)
    return "內容方向已完成簡報化檢查。" if report.status is ContentQualityStatus.PASS else "內容方向還需要修整後再確認。"


__all__ = [
    "ContentQualityCode", "ContentQualityFinding", "ContentQualityReport",
    "ContentQualitySlide", "ContentQualityStatus", "HeadlineKind",
    "audit_presentation_content", "classify_headline_shape",
    "user_facing_content_quality_message",
]

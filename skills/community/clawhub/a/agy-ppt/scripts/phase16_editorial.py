#!/usr/bin/env python3
"""Phase 16.4 deterministic Human Editorial Quality signals and bounded repair."""

from __future__ import annotations

from dataclasses import dataclass, replace
from enum import Enum
from typing import Iterable

from phase16_slide_evidence import SlideEvidencePlan


EDITORIAL_REVIEW_RECOMMENDED = "EDITORIAL_REVIEW_RECOMMENDED"
EDITORIAL_PASS = "PASS"
ERROR_EDITORIAL_INVALID = "PHASE16_EDITORIAL_INVALID"
ERROR_REPAIR_LIMIT = "PHASE16_EDITORIAL_REPAIR_LIMIT"

JARGON_SIGNALS = ("打造", "賦能", "共贏", "深化", "核心價值", "關鍵引擎", "高效", "一站式", "全方位")
MECHANICAL_TRANSITIONS = ("在這一頁", "接下來我們來看", "我們可以看到", "透過這張圖")


class EditorialError(Exception):
    def __init__(self, error_code: str, message: str) -> None:
        super().__init__(message)
        self.error_code = error_code


class PresentationMode(str, Enum):
    PITCH = "PITCH"
    EXECUTIVE = "EXECUTIVE"
    TRAINING = "TRAINING"
    SALES = "SALES"
    REPORT = "REPORT"
    TECHNICAL = "TECHNICAL"
    KEYNOTE = "KEYNOTE"
    EDUCATIONAL = "EDUCATIONAL"


class SlideRole(str, Enum):
    HERO = "HERO"
    STANDARD = "STANDARD"
    DENSE = "DENSE"
    LIGHT = "LIGHT"
    DATA = "DATA"
    QUOTE = "QUOTE"
    CASE = "CASE"
    PROCESS = "PROCESS"
    COMPARISON = "COMPARISON"


_HEADLINE_LIMITS = {
    PresentationMode.EXECUTIVE: 42,
    PresentationMode.SALES: 56,
    PresentationMode.TECHNICAL: 84,
    PresentationMode.REPORT: 72,
    PresentationMode.KEYNOTE: 36,
}


def mode_guidance(mode: PresentationMode) -> tuple[str, ...]:
    guidance = {
        PresentationMode.EXECUTIVE: ("direct", "concise", "evidence-forward", "restrained"),
        PresentationMode.SALES: ("conversational", "memorable", "benefit-oriented"),
        PresentationMode.TECHNICAL: ("precise", "terminology-allowed", "evidence-dense"),
        PresentationMode.KEYNOTE: ("narrative", "visually-paced", "selectively-light"),
    }
    return guidance.get(mode, ("audience-appropriate", "clear", "intentional"))


def headline_limit(mode: PresentationMode) -> int:
    if not isinstance(mode, PresentationMode):
        raise EditorialError(ERROR_EDITORIAL_INVALID, "presentation mode is invalid")
    return _HEADLINE_LIMITS.get(mode, 64)


@dataclass(frozen=True)
class EditorialSlide:
    slide_id: str
    title: str
    body: tuple[str, ...]
    notes: str
    role: SlideRole = SlideRole.STANDARD
    layout_family: str = "standard"
    image_position: str | None = None
    density: str = "STANDARD"
    evidence_plan: SlideEvidencePlan | None = None

    def __post_init__(self) -> None:
        if not self.slide_id.startswith("slide_") or not self.title.strip() or not isinstance(self.role, SlideRole):
            raise EditorialError(ERROR_EDITORIAL_INVALID, "editorial slide is invalid")
        object.__setattr__(self, "body", tuple(self.body))
        if self.evidence_plan is not None and self.evidence_plan.slide_id != self.slide_id:
            raise EditorialError(ERROR_EDITORIAL_INVALID, "evidence plan belongs to another slide")

    @property
    def copy(self) -> str:
        return "\n".join((self.title, *self.body))


def apply_headline_pass(slide: EditorialSlide, mode: PresentationMode, proposed_title: str | None = None) -> EditorialSlide:
    """Apply an AGY-approved headline expression without weakening evidence."""
    headline_limit(mode)  # validate mode; the limit guides AGY rather than forcing catchy copy
    if proposed_title is None:
        return slide
    clean = proposed_title.strip() if isinstance(proposed_title, str) else ""
    if not clean:
        raise EditorialError(ERROR_EDITORIAL_INVALID, "proposed headline is empty")
    updated = replace(slide, title=clean)
    if updated.evidence_plan is not None:
        updated.evidence_plan.validate_rendered_text(updated.copy)
    return updated


@dataclass(frozen=True)
class EditorialWarning:
    code: str
    slide_ids: tuple[str, ...]
    detail: str


@dataclass(frozen=True)
class EditorialReport:
    status: str
    warnings: tuple[EditorialWarning, ...]

    def count(self, code: str | None = None) -> int:
        return sum(1 for warning in self.warnings if code is None or warning.code == code)


def _runs(slides: tuple[EditorialSlide, ...], attribute: str, expected: str | None = None) -> list[tuple[EditorialSlide, ...]]:
    runs: list[list[EditorialSlide]] = []
    current: list[EditorialSlide] = []
    previous = object()
    for slide in slides:
        value = getattr(slide, attribute)
        if expected is not None and value != expected:
            if current:
                runs.append(current)
            current, previous = [], object()
            continue
        if current and value != previous:
            runs.append(current)
            current = []
        current.append(slide)
        previous = value
    if current:
        runs.append(current)
    return [tuple(run) for run in runs]


def lint_editorial(slides: Iterable[EditorialSlide], mode: PresentationMode) -> EditorialReport:
    clean = tuple(slides)
    if not clean or not isinstance(mode, PresentationMode):
        raise EditorialError(ERROR_EDITORIAL_INVALID, "editorial input is invalid")
    warnings: list[EditorialWarning] = []
    all_copy = "\n".join(slide.copy for slide in clean)
    for word in JARGON_SIGNALS:
        count = all_copy.count(word)
        if count >= 3:
            warnings.append(EditorialWarning("COPY_REPETITION", tuple(slide.slide_id for slide in clean if word in slide.copy), f"{word}: {count}"))
    prefixes: dict[str, list[str]] = {}
    for slide in clean:
        for sentence in slide.body:
            prefix = sentence.strip()[:8]
            if len(prefix) >= 4:
                prefixes.setdefault(prefix, []).append(slide.slide_id)
    for prefix, ids in sorted(prefixes.items()):
        if len(ids) >= 3:
            warnings.append(EditorialWarning("REPEATED_SENTENCE_TEMPLATE", tuple(ids), prefix))
    limit = headline_limit(mode)
    for slide in clean:
        if len(slide.title) > limit:
            warnings.append(EditorialWarning("HEADLINE_TOO_LONG", (slide.slide_id,), f"{len(slide.title)}>{limit}"))
    for run in _runs(clean, "layout_family", "cards-3"):
        if len(run) >= 5:
            warnings.append(EditorialWarning("REPEATED_THREE_CARD_LAYOUT", tuple(item.slide_id for item in run), str(len(run))))
    for run in _runs(clean, "layout_family"):
        if len(run) >= 4:
            warnings.append(EditorialWarning("REPEATED_LAYOUT_FAMILY", tuple(item.slide_id for item in run), run[0].layout_family))
    positioned = [slide for slide in clean if slide.image_position]
    if len(positioned) >= 4:
        dominant = max({slide.image_position for slide in positioned}, key=lambda pos: sum(s.image_position == pos for s in positioned))
        matching = [slide for slide in positioned if slide.image_position == dominant]
        if len(matching) / len(positioned) >= 0.8:
            warnings.append(EditorialWarning("REPEATED_IMAGE_POSITION", tuple(s.slide_id for s in matching), str(dominant)))
    bullet_counts = [len(slide.body) for slide in clean]
    if len(clean) >= 4 and bullet_counts[0] > 0 and len(set(bullet_counts)) == 1:
        warnings.append(EditorialWarning("UNIFORM_BULLET_COUNT", tuple(s.slide_id for s in clean), str(bullet_counts[0])))
    densities = [slide.density for slide in clean]
    if len(clean) >= 4 and len(set(densities)) == 1:
        warnings.append(EditorialWarning("UNIFORM_INFORMATION_DENSITY", tuple(s.slide_id for s in clean), densities[0]))
    for phrase in MECHANICAL_TRANSITIONS:
        ids = tuple(slide.slide_id for slide in clean if phrase in slide.notes)
        if len(ids) >= 3:
            warnings.append(EditorialWarning("MECHANICAL_SPEAKER_NOTES", ids, phrase))
    return EditorialReport(EDITORIAL_REVIEW_RECOMMENDED if warnings else EDITORIAL_PASS, tuple(warnings))


@dataclass(frozen=True)
class EditorialSession:
    mode: PresentationMode
    slides: tuple[EditorialSlide, ...]
    repair_count: int = 0

    def __post_init__(self) -> None:
        object.__setattr__(self, "slides", tuple(self.slides))
        if not self.slides or self.repair_count not in (0, 1):
            raise EditorialError(ERROR_EDITORIAL_INVALID, "editorial session is invalid")

    def lint(self) -> EditorialReport:
        return lint_editorial(self.slides, self.mode)

    def repair_once(self) -> "EditorialSession":
        if self.repair_count >= 1:
            raise EditorialError(ERROR_REPAIR_LIMIT, "automatic editorial repair is limited to one pass")
        uniform_density = len({slide.density for slide in self.slides}) == 1
        repaired: list[EditorialSlide] = []
        for index, slide in enumerate(self.slides):
            notes = slide.notes
            if index:
                for phrase in MECHANICAL_TRANSITIONS:
                    if notes.startswith(phrase):
                        notes = notes[len(phrase):].lstrip("，,:： 。")
                        break
            layout = slide.layout_family
            if layout == "cards-3" and index % 2:
                layout = f"editorial-{slide.role.value.lower()}"
            density = slide.density
            if uniform_density:
                if slide.role in (SlideRole.HERO, SlideRole.QUOTE, SlideRole.LIGHT):
                    density = "LIGHT"
                elif slide.role in (SlideRole.DATA, SlideRole.DENSE):
                    density = "DENSE"
                else:
                    density = "STANDARD"
            updated = replace(slide, notes=notes, layout_family=layout, density=density)
            if updated.evidence_plan is not None:
                updated.evidence_plan.validate_rendered_text(updated.copy)
                if updated.evidence_plan is not slide.evidence_plan:
                    raise EditorialError(ERROR_EDITORIAL_INVALID, "repair changed evidence identity")
            repaired.append(updated)
        return EditorialSession(self.mode, tuple(repaired), 1)


def user_facing_editorial_message() -> str:
    return "已完成內容與呈現品質檢查，接著依核准流程繼續。"


__all__ = [
    "EDITORIAL_PASS", "EDITORIAL_REVIEW_RECOMMENDED", "ERROR_REPAIR_LIMIT", "EditorialError",
    "EditorialReport", "EditorialSession", "EditorialSlide", "EditorialWarning", "PresentationMode",
    "SlideRole", "apply_headline_pass", "headline_limit", "lint_editorial", "mode_guidance",
    "user_facing_editorial_message",
]

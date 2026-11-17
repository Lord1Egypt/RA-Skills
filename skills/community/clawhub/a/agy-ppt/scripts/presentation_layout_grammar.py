#!/usr/bin/env python3
"""Small deterministic layout and typography grammar for Hybrid PPTX output.

The grammar constrains geometry and hierarchy without turning every slide into
one rigid template.  It uses the repository's established 10 x 5.625 inch
widescreen coordinate system, shared with ``assemble_ppt.py``.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Iterable, Sequence

from phase18_contract import EditabilityEnvelope, ElementBox
from phase18_production_plan import ElementRole


SLIDE_WIDTH_16_9 = 10.0
SLIDE_HEIGHT_16_9 = 5.625


class LayoutSeverity(str, Enum):
    ACCEPT = "ACCEPT"
    WARNING = "WARNING"
    REPAIR = "REPAIR"
    BLOCK = "BLOCK"


class LayoutIssue(str, Enum):
    OUT_OF_BOUNDS = "OUT_OF_BOUNDS"
    OUTER_MARGIN = "OUTER_MARGIN"
    TITLE_LINE_COUNT = "TITLE_LINE_COUNT"
    TEXT_DENSITY = "TEXT_DENSITY"
    CARD_GAP = "CARD_GAP"
    TYPOGRAPHY_HIERARCHY = "TYPOGRAPHY_HIERARCHY"
    ENVELOPE_CHARACTER_RANGE = "ENVELOPE_CHARACTER_RANGE"
    ENVELOPE_FONT_SIZE = "ENVELOPE_FONT_SIZE"
    ENVELOPE_LINE_COUNT = "ENVELOPE_LINE_COUNT"


class LayoutDensity(str, Enum):
    AIRY = "AIRY"
    BALANCED = "BALANCED"
    DENSE = "DENSE"


class CardDensity(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class ImageDensity(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class CardRole(str, Enum):
    PRIMARY_CARD = "PRIMARY_CARD"
    SECONDARY_CARD = "SECONDARY_CARD"
    MICRO_CARD = "MICRO_CARD"
    KPI_CARD = "KPI_CARD"
    IMAGE_CARD = "IMAGE_CARD"
    INSIGHT_CARD = "INSIGHT_CARD"
    ACTION_CARD = "ACTION_CARD"


@dataclass(frozen=True)
class PresentationStyleProfile:
    """Style-level preference; it never changes the global default grammar."""

    layout_density: LayoutDensity = LayoutDensity.BALANCED
    card_density: CardDensity = CardDensity.MEDIUM
    image_density: ImageDensity = ImageDensity.MEDIUM

    def __post_init__(self) -> None:
        if not isinstance(self.layout_density, LayoutDensity):
            raise ValueError("layout_density must be a LayoutDensity")
        if not isinstance(self.card_density, CardDensity):
            raise ValueError("card_density must be a CardDensity")
        if not isinstance(self.image_density, ImageDensity):
            raise ValueError("image_density must be an ImageDensity")


@dataclass(frozen=True)
class LayoutSelectionPolicy:
    min_structured_modules: int
    max_structured_modules: int
    preferred_card_roles: tuple[CardRole, ...]
    preferred_layout_families: tuple[str, ...]
    primary_visual_expected: bool
    supporting_visuals_expected: bool


DEFAULT_STYLE_PROFILE = PresentationStyleProfile()
DENSE_IMAGE_RICH_STYLE_PROFILE = PresentationStyleProfile(
    LayoutDensity.DENSE, CardDensity.HIGH, ImageDensity.HIGH,
)


def layout_selection_policy(profile: PresentationStyleProfile) -> LayoutSelectionPolicy:
    """Translate an approved style preference into layout-selection constraints."""
    if not isinstance(profile, PresentationStyleProfile):
        raise ValueError("style profile is required")
    if profile.layout_density is LayoutDensity.DENSE and profile.card_density is CardDensity.HIGH:
        return LayoutSelectionPolicy(
            2, 6,
            (CardRole.PRIMARY_CARD, CardRole.SECONDARY_CARD, CardRole.MICRO_CARD,
             CardRole.KPI_CARD, CardRole.IMAGE_CARD, CardRole.INSIGHT_CARD, CardRole.ACTION_CARD),
            ("hero_plus_cards", "kpi_chart_annotations", "image_cluster_takeaways",
             "card_matrix_supporting_visual", "comparison_evidence_strip", "process_visual_cards"),
            True,
            profile.image_density is ImageDensity.HIGH,
        )
    if profile.layout_density is LayoutDensity.AIRY:
        return LayoutSelectionPolicy(
            1, 3, (CardRole.PRIMARY_CARD, CardRole.INSIGHT_CARD),
            ("single_hero", "editorial_split", "single_assertion"), True, False,
        )
    return LayoutSelectionPolicy(
        1, 4,
        (CardRole.PRIMARY_CARD, CardRole.SECONDARY_CARD, CardRole.KPI_CARD, CardRole.INSIGHT_CARD),
        ("editorial_split", "hero_plus_cards", "kpi_chart_annotations", "process_visual_cards"),
        True,
        profile.image_density is ImageDensity.HIGH,
    )


@dataclass(frozen=True)
class LayoutFinding:
    issue: LayoutIssue
    severity: LayoutSeverity
    element_id: str
    detail: str


@dataclass(frozen=True)
class PresentationLayoutGrammar:
    slide_width: float = SLIDE_WIDTH_16_9
    slide_height: float = SLIDE_HEIGHT_16_9
    outer_margin_x: float = 0.60
    outer_margin_top: float = 0.42
    outer_margin_bottom: float = 0.45
    title_height: float = 0.72
    title_content_gap: float = 0.28
    column_gap: float = 0.28
    card_gap: float = 0.24
    card_padding: float = 0.24

    def title_box(self) -> ElementBox:
        return ElementBox(
            self.outer_margin_x,
            self.outer_margin_top,
            self.slide_width - 2 * self.outer_margin_x,
            self.title_height,
        )

    def content_box(self) -> ElementBox:
        top = self.outer_margin_top + self.title_height + self.title_content_gap
        return ElementBox(
            self.outer_margin_x,
            top,
            self.slide_width - 2 * self.outer_margin_x,
            self.slide_height - top - self.outer_margin_bottom,
        )

    def columns(self, count: int, *, box: ElementBox | None = None) -> tuple[ElementBox, ...]:
        if type(count) is not int or count < 1 or count > 4:
            raise ValueError("column count must be between 1 and 4")
        region = box or self.content_box()
        width = (region.width - self.column_gap * (count - 1)) / count
        if width <= 0:
            raise ValueError("column region is too narrow")
        return tuple(
            ElementBox(region.left + index * (width + self.column_gap), region.top, width, region.height)
            for index in range(count)
        )

    def card_content_box(self, card: ElementBox) -> ElementBox:
        if card.width <= 2 * self.card_padding or card.height <= 2 * self.card_padding:
            raise ValueError("card is too small for the grammar padding")
        return ElementBox(
            card.left + self.card_padding,
            card.top + self.card_padding,
            card.width - 2 * self.card_padding,
            card.height - 2 * self.card_padding,
        )

    def inside_slide(self, box: ElementBox, tolerance: float = 0.001) -> bool:
        return (
            box.left >= -tolerance
            and box.top >= -tolerance
            and box.left + box.width <= self.slide_width + tolerance
            and box.top + box.height <= self.slide_height + tolerance
        )


DEFAULT_LAYOUT_GRAMMAR = PresentationLayoutGrammar()


def suggested_font_size(role: ElementRole) -> float:
    return {
        ElementRole.TITLE: 30.0,
        ElementRole.ARTISTIC_HEADLINE: 34.0,
        ElementRole.KPI: 36.0,
        ElementRole.PRICE: 32.0,
        ElementRole.CTA: 22.0,
        ElementRole.NAME: 20.0,
        ElementRole.JOB_TITLE: 16.0,
        ElementRole.DATE: 14.0,
        ElementRole.CONTACT: 14.0,
        ElementRole.TABLE: 13.0,
        ElementRole.BODY: 17.0,
    }.get(role, 17.0)


def max_characters_for_box(box: ElementBox, font_size: float, *, cjk: bool) -> int:
    """Conservative density capacity; used as a warning, never semantic rewriting."""
    if font_size <= 0:
        raise ValueError("font size must be positive")
    width_points = box.width * 72
    height_points = box.height * 72
    average_glyph = font_size * (1.0 if cjk else 0.55)
    chars_per_line = max(1, int(width_points / average_glyph))
    line_height = font_size * 1.18
    lines = max(1, int(height_points / line_height))
    return chars_per_line * lines


def estimated_line_count(text: str, box: ElementBox, font_size: float) -> int:
    """Estimate native line use for envelope review, including mixed CJK/Latin copy."""
    if font_size <= 0:
        raise ValueError("font size must be positive")
    available_units = box.width * 72 / font_size
    lines = 0
    for explicit_line in (text.splitlines() or [text]):
        units = 0.0
        for char in explicit_line:
            if "\u3400" <= char <= "\u9fff":
                # CJK glyphs are effectively full-em and PowerPoint fallback
                # metrics can be slightly wider than the nominal point size.
                units += 1.05
            elif char.isspace():
                units += 0.30
            elif char.isascii() and char.isalnum():
                units += 0.55
            else:
                units += 0.50
        lines += max(1, int((units + available_units - 0.000001) // available_units))
    return max(1, lines)


def audit_text_envelope(
    element_id: str,
    role: ElementRole,
    box: ElementBox,
    text: str,
    font_size: float,
    envelope: EditabilityEnvelope | None,
) -> tuple[LayoutFinding, ...]:
    """Return review findings without rewriting approved copy or silently shrinking it."""
    if envelope is None:
        return ()
    findings: list[LayoutFinding] = []
    length = len(text)
    if (
        envelope.expected_min_characters is not None
        and length < envelope.expected_min_characters
    ) or (
        envelope.expected_max_characters is not None
        and length > envelope.expected_max_characters
    ):
        findings.append(LayoutFinding(
            LayoutIssue.ENVELOPE_CHARACTER_RANGE,
            LayoutSeverity.REPAIR,
            element_id,
            f"{length} characters are outside the approved editability envelope",
        ))
    if (
        envelope.minimum_font_size is not None
        and font_size < envelope.minimum_font_size
    ) or (
        envelope.maximum_font_size is not None
        and font_size > envelope.maximum_font_size
    ):
        findings.append(LayoutFinding(
            LayoutIssue.ENVELOPE_FONT_SIZE,
            LayoutSeverity.REPAIR,
            element_id,
            f"font size {font_size:g} is outside the approved editability envelope",
        ))
    lines = estimated_line_count(text, box, font_size)
    if (
        envelope.expected_min_lines is not None
        and lines < envelope.expected_min_lines
    ) or (
        envelope.expected_max_lines is not None
        and lines > envelope.expected_max_lines
    ):
        findings.append(LayoutFinding(
            LayoutIssue.ENVELOPE_LINE_COUNT,
            LayoutSeverity.REPAIR,
            element_id,
            f"estimated {lines} lines are outside the approved editability envelope",
        ))
    return tuple(findings)


def audit_layout(
    elements: Iterable[tuple[str, ElementRole, ElementBox, str, float]],
    *,
    grammar: PresentationLayoutGrammar = DEFAULT_LAYOUT_GRAMMAR,
) -> tuple[LayoutFinding, ...]:
    findings: list[LayoutFinding] = []
    title_sizes: list[float] = []
    body_sizes: list[float] = []
    for element_id, role, box, text, font_size in elements:
        if not grammar.inside_slide(box):
            findings.append(LayoutFinding(LayoutIssue.OUT_OF_BOUNDS, LayoutSeverity.BLOCK, element_id, "element extends outside the 10 x 5.625 inch slide"))
        if role is ElementRole.TITLE:
            title_sizes.append(font_size)
            cjk_title = any("\u3400" <= char <= "\u9fff" for char in text)
            layout_font_size = max(font_size, suggested_font_size(ElementRole.TITLE))
            average_glyph = layout_font_size * (1.0 if cjk_title else 0.55)
            chars_per_line = max(1, int(box.width * 72 / average_glyph))
            estimated_lines = max(1, (len(text) + chars_per_line - 1) // chars_per_line)
            if estimated_lines > 2:
                findings.append(LayoutFinding(LayoutIssue.TITLE_LINE_COUNT, LayoutSeverity.REPAIR, element_id, f"estimated title lines: {estimated_lines}"))
        elif role in {ElementRole.BODY, ElementRole.TABLE, ElementRole.CONTACT}:
            body_sizes.append(font_size)
        if text:
            cjk = any("\u3400" <= char <= "\u9fff" for char in text)
            capacity = max_characters_for_box(box, font_size, cjk=cjk)
            if len(text) > capacity:
                findings.append(LayoutFinding(LayoutIssue.TEXT_DENSITY, LayoutSeverity.REPAIR, element_id, f"{len(text)} characters exceed conservative capacity {capacity}"))
    if title_sizes and body_sizes and min(title_sizes) < max(body_sizes) * 1.35:
        findings.append(LayoutFinding(LayoutIssue.TYPOGRAPHY_HIERARCHY, LayoutSeverity.REPAIR, "slide", "title/body size ratio is weaker than 1.35"))
    return tuple(findings)


__all__ = [
    "CardDensity", "CardRole", "DEFAULT_LAYOUT_GRAMMAR", "DEFAULT_STYLE_PROFILE",
    "DENSE_IMAGE_RICH_STYLE_PROFILE", "ImageDensity", "LayoutDensity",
    "LayoutFinding", "LayoutIssue", "LayoutSelectionPolicy", "LayoutSeverity",
    "PresentationStyleProfile",
    "PresentationLayoutGrammar", "SLIDE_HEIGHT_16_9", "SLIDE_WIDTH_16_9",
    "audit_layout", "audit_text_envelope", "estimated_line_count",
    "layout_selection_policy", "max_characters_for_box", "suggested_font_size",
]

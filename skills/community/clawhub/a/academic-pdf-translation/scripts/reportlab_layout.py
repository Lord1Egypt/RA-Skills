from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Iterable

from reportlab.lib.enums import TA_LEFT
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import Paragraph

from cjk_markup import (
    SINGLE_HAN_TAIL_PATTERN,
    install_reportlab_cjk_nobr_patch,
    reportlab_cjk_markup,
)


@dataclass(frozen=True)
class FlowItem:
    kind: str
    text: str
    style: ParagraphStyle
    check_single_han_orphan: bool = True


@dataclass(frozen=True)
class FlowPlacement:
    index: int
    kind: str
    y_top: float
    y_bottom: float
    height: float
    space_before: float
    space_after: float


@dataclass(frozen=True)
class FlowResult:
    fits: bool
    used_height: float
    remaining_height: float
    placements: list[FlowPlacement]
    overflow_index: int | None = None
    orphan_indices: tuple[int, ...] = ()

    def as_dict(self) -> dict:
        return {
            "fits": self.fits,
            "used_height": round(self.used_height, 3),
            "remaining_height": round(self.remaining_height, 3),
            "placements": [asdict(item) for item in self.placements],
            "overflow_index": self.overflow_index,
            "orphan_indices": list(self.orphan_indices),
        }


def make_cjk_style(
    name: str,
    *,
    font_name: str,
    font_size: float,
    leading_ratio: float,
    alignment: int = TA_LEFT,
    first_line_indent_em: float = 0,
    left_indent_pt: float = 0,
    right_indent_pt: float = 0,
    space_before_em: float = 0,
    space_after_em: float = 0,
    parent: ParagraphStyle | None = None,
) -> ParagraphStyle:
    if font_size <= 0 or leading_ratio <= 0:
        raise ValueError("字号和行距必须大于 0")
    install_reportlab_cjk_nobr_patch()
    return ParagraphStyle(
        name,
        parent=parent,
        fontName=font_name,
        fontSize=font_size,
        leading=font_size * leading_ratio,
        alignment=alignment,
        firstLineIndent=font_size * first_line_indent_em,
        leftIndent=left_indent_pt,
        rightIndent=right_indent_pt,
        spaceBefore=font_size * space_before_em,
        spaceAfter=font_size * space_after_em,
        wordWrap="CJK",
        splitLongWords=True,
        allowWidows=0,
        allowOrphans=0,
    )


def paragraph_line_texts(paragraph: Paragraph) -> list[str]:
    lines: list[str] = []
    for line in getattr(getattr(paragraph, "blPara", None), "lines", []):
        if isinstance(line, tuple):
            words = line[1] if len(line) > 1 else []
            lines.append("".join(str(word) for word in words).strip())
            continue
        words = getattr(line, "words", [])
        lines.append(
            "".join(str(getattr(word, "text", "")) for word in words).strip()
        )
    return lines


def _paragraph(item: FlowItem) -> Paragraph:
    install_reportlab_cjk_nobr_patch()
    return Paragraph(reportlab_cjk_markup(item.text), item.style)


def layout_flow(
    items: Iterable[FlowItem],
    *,
    width_pt: float,
    height_pt: float,
    canvas: Canvas | None = None,
    x_pt: float = 0,
    top_y_pt: float | None = None,
) -> FlowResult:
    if width_pt <= 0 or height_pt <= 0:
        raise ValueError("流排区域宽高必须大于 0")
    top = height_pt if top_y_pt is None else top_y_pt
    bottom = top - height_pt
    y = top
    placements: list[FlowPlacement] = []
    orphan_indices: list[int] = []

    for index, item in enumerate(items):
        paragraph = _paragraph(item)
        before = float(item.style.spaceBefore or 0)
        after = float(item.style.spaceAfter or 0)
        available = y - bottom - before
        _, paragraph_height = paragraph.wrap(width_pt, max(available, 1))
        if paragraph_height > available + 0.1:
            return FlowResult(
                fits=False,
                used_height=top - y,
                remaining_height=max(y - bottom, 0),
                placements=placements,
                overflow_index=index,
                orphan_indices=tuple(orphan_indices),
            )
        if paragraph_height + after > available + 0.1:
            return FlowResult(
                fits=False,
                used_height=top - y,
                remaining_height=max(y - bottom, 0),
                placements=placements,
                overflow_index=index,
                orphan_indices=tuple(orphan_indices),
            )
        if item.check_single_han_orphan and any(
            SINGLE_HAN_TAIL_PATTERN.fullmatch(line)
            for line in paragraph_line_texts(paragraph)
        ):
            orphan_indices.append(index)

        y -= before
        y_bottom = y - paragraph_height
        if canvas is not None:
            paragraph.drawOn(canvas, x_pt, y_bottom)
        placements.append(
            FlowPlacement(
                index=index,
                kind=item.kind,
                y_top=round(y, 3),
                y_bottom=round(y_bottom, 3),
                height=round(paragraph_height, 3),
                space_before=round(before, 3),
                space_after=round(after, 3),
            )
        )
        y = y_bottom - after

    return FlowResult(
        fits=not orphan_indices,
        used_height=top - y,
        remaining_height=max(y - bottom, 0),
        placements=placements,
        orphan_indices=tuple(orphan_indices),
    )

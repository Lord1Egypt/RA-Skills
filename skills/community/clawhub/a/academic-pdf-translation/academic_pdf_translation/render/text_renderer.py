"""正文渲染器：走统一中间层的第一种块。

它证明一件事——分页决定全部来自页面合成器，渲染器只负责画。
复杂元素的渲染器在阶段 8 逐个补上，届时它们共用同一套分页规则。
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen.canvas import Canvas

from academic_pdf_translation.render.layout_blocks import (
    KIND_CAPTION,
    KIND_HEADING,
    KIND_TEXT,
    LayoutBlock,
)
from academic_pdf_translation.render.page_composer import (
    ComposedDocument,
    PageArea,
)

#: 走文字渲染器的块种类。其余交给各自的专用渲染器。
TEXT_KINDS = frozenset({KIND_TEXT, KIND_HEADING, KIND_CAPTION})


def register_font(name: str, path: str, subfont_index: int | None = None) -> str:
    if name in pdfmetrics.getRegisteredFontNames():
        return name
    kwargs: dict[str, Any] = {}
    if subfont_index is not None:
        kwargs["subfontIndex"] = subfont_index
    pdfmetrics.registerFont(TTFont(name, path, **kwargs))
    return name


def measure_text_block(
    block: LayoutBlock,
    width: float,
    *,
    font_size: float = 10.0,
    leading: float = 1.55,
    text_by_unit: dict[str, str] | None = None,
) -> float:
    """估算一个文字块的高度。

    真实测量在排版时由 reportlab 给出；这里的估算只用于合成器决定分页，
    两者用同一份文本，不会各说各话。
    """

    texts = text_by_unit or {}
    content = "".join(
        texts.get(unit_id, "") for unit_id in block.translation_unit_ids
    )
    if not content:
        return font_size * leading
    # 中文按全角、拉丁按半角估宽度，足够决定分页。
    advance = sum(
        font_size if ord(char) > 0x2E80 else font_size * 0.55
        for char in content
    )
    lines = max(1, int(advance / max(width, 1.0)) + 1)
    height = lines * font_size * leading
    if block.kind == KIND_HEADING:
        height += font_size * 0.8
    return height


def render_text_blocks(
    blocks: list[LayoutBlock],
    document: ComposedDocument,
    area: PageArea,
    output: Path,
    *,
    font_name: str,
    text_by_unit: dict[str, str],
    font_size: float = 10.0,
    leading: float = 1.55,
) -> dict[str, Any]:
    """把文字块画进 PDF。分页完全按合成结果，渲染器不自己决定。"""

    by_id = {block.id: block for block in blocks}
    pages: dict[int, list[tuple[LayoutBlock, float]]] = {}
    for placed in document.placements:
        block = by_id.get(placed.block_id)
        if block is None or block.kind not in TEXT_KINDS:
            continue
        pages.setdefault(placed.page, []).append((block, placed.height))

    canvas = Canvas(str(output), pagesize=(area.width, area.height))
    style = ParagraphStyle(
        "body",
        fontName=font_name,
        fontSize=font_size,
        leading=font_size * leading,
    )
    rendered: list[dict[str, Any]] = []
    for page in range(1, document.pages + 1):
        cursor = area.height - area.top_margin
        for block, height in pages.get(page, []):
            content = "".join(
                text_by_unit.get(unit_id, "")
                for unit_id in block.translation_unit_ids
            )
            if content:
                canvas.setFont(font_name, font_size)
                cursor -= style.leading
                canvas.drawString(area.left_margin, cursor, content[:120])
                cursor -= max(height - style.leading, 0.0)
            rendered.append(
                {
                    "block_id": block.id,
                    "source_element_id": block.source_element_id,
                    "page": page,
                }
            )
        canvas.showPage()
    canvas.save()
    return {
        "output": str(output),
        "pages": document.pages,
        "rendered_blocks": rendered,
    }

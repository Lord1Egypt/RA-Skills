"""Story 构建的第三层：保留区域与复杂内容的分派。

从 ``scripts/build_candidate.py`` 原样搬来，行为不变。这一层回答的是
"这条复杂内容该用哪种画法"：重建表格、重画矢量图、做图内文字本地化，
还是退回去把原文区域整块保留。所有安全降级最后都汇到这里。

依赖方向是单向的：只用 ``story_text`` 的注入包和 ``story_visual`` 的
表格、图片 Flowable，不回指 ``story``。
"""

from __future__ import annotations

import io
from typing import Any

from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (
    Flowable,
    Image,
    KeepTogether,
    PageBreak,
    Paragraph,
    Spacer,
)

from academic_pdf_translation.planning.mode_policy import (
    FALLBACK_PRESERVE_ELEMENT_REGION,
    FALLBACK_PRESERVE_FULL_PAGE,
)

from .flowables import VectorPayloadFlowable
from .font_runs import _markup
from .plan_bridge import FIGURE_CAPTION_KEY
from .preserved_region_renderer import MIN_RASTER_DPI, PDF_BASE_DPI
from .story_text import StoryDeps
from .story_visual import (
    _image_flowables,
    _localized_image_labels,
    _table_flowables,
)
from .table_data import _table_note_text

#: 保留区域最多占版心高度的这个比例。留一点余地给图题和上下文。
PRESERVED_REGION_MAX_HEIGHT_RATIO = 0.9


def _overlay_chinese_labels(
    png_bytes: bytes,
    labels: list[dict[str, Any]],
    clip: Any,
    scale: float,
    font_path: str,
) -> bytes:
    """把有译文的图内标签覆盖成中文。

    白底盖住原英文标签，再按格高写入中文——数字尺寸、通道数没有译文，
    一个像素都不动。字号从格高起步，放不下就缩，缩到底还放不下就不画，
    留着原文也比画出溢出图形的中文强。
    """

    import io as _io

    from PIL import Image as PILImage
    from PIL import ImageDraw, ImageFont

    image = PILImage.open(_io.BytesIO(png_bytes)).convert("RGB")
    draw = ImageDraw.Draw(image)
    for label in labels:
        box = label.get("bbox")
        text = str(label.get("translation") or "").strip()
        if not text or not isinstance(box, list) or len(box) != 4:
            continue
        x0 = (float(box[0]) - float(clip.x0)) * scale
        y0 = (float(box[1]) - float(clip.y0)) * scale
        x1 = (float(box[2]) - float(clip.x0)) * scale
        y1 = (float(box[3]) - float(clip.y0)) * scale
        if x1 <= x0 or y1 <= y0:
            continue
        # 中文比英文标签宽是常态，允许向右伸一点，但绝不许伸出图片
        # 边界——"输出分割图"被裁成"输出分割"比留英文还糟。
        edge = image.width - max(2.0, scale)
        size = max(int((y1 - y0) * 0.92), 6)
        font = None
        while size >= 6:
            font = ImageFont.truetype(font_path, size)
            width_needed = draw.textlength(text, font=font)
            if width_needed <= (x1 - x0) * 1.35 and x0 + width_needed <= edge:
                break
            if x0 + width_needed <= edge:
                break
            size -= 1
        if font is None or size < 6:
            continue
        width_needed = draw.textlength(text, font=font)
        draw_x = min(x0, max(0.0, edge - width_needed))
        pad = max(1.0, scale)
        draw.rectangle(
            (
                min(draw_x, x0) - pad,
                y0 - pad,
                max(x1, draw_x + width_needed) + pad,
                y1 + pad,
            ),
            fill="white",
        )
        draw.text((draw_x, y0 - size * 0.08), text, fill="black", font=font)
    output = _io.BytesIO()
    image.save(output, "PNG")
    return output.getvalue()


def _preserved_source_region_image(
    source_document: Any,
    *,
    deps: StoryDeps,
    page_number: int,
    bbox: list[float] | None,
    available_width: float,
    maximum_height: float,
    dpi: int = MIN_RASTER_DPI,
    labels: list[dict[str, Any]] | None = None,
    label_font_path: str | None = None,
) -> Image:
    """把原文的一块区域栅格化成一个图片流。

    渲染计划把某个元素定到保留级，意思是"重建这块不可靠"。到了这一步，
    好看已经不是目标了，**不丢内容**才是。所以这里不重画任何东西，
    只把原文那一块原样搬过来。

    两条不肯让步的地方：

    - 分辨率不低于 MIN_RASTER_DPI。低于它图里的数字就开始糊，
      而保留区域的全部意义就是那些数字还能看清。
    - 不放大。原区域在版面上占多少点就画多少点，放不下才等比缩小；
      放大不会凭空补出像素，只会把每个像素摊得更大。
    """

    fitz = deps.import_fitz_fn()
    page = source_document[page_number - 1]
    clip = (
        fitz.Rect(*map(float, bbox))
        if isinstance(bbox, (list, tuple)) and len(bbox) == 4
        else page.rect
    )
    scale = max(int(dpi), MIN_RASTER_DPI) / PDF_BASE_DPI
    pixmap = page.get_pixmap(
        matrix=fitz.Matrix(scale, scale), clip=clip, alpha=False
    )
    png_bytes = pixmap.tobytes("png")
    if labels and label_font_path:
        png_bytes = _overlay_chinese_labels(
            png_bytes, labels, clip, scale, label_font_path
        )
    natural_width = max(float(clip.width), 1.0)
    natural_height = max(float(clip.height), 1.0)
    ratio = min(
        1.0,
        available_width / natural_width,
        maximum_height / natural_height,
    )
    image = Image(
        io.BytesIO(png_bytes),
        width=natural_width * ratio,
        height=natural_height * ratio,
    )
    image.hAlign = "CENTER"
    return image


def _preserved_region_flowables(
    item: dict[str, Any],
    *,
    deps: StoryDeps,
    styles: dict[str, ParagraphStyle],
    source_document: Any,
    available_width: float,
    available_height: float,
    label_font_path: str | None = None,
) -> list[Flowable]:
    """渲染计划定到保留级的元素，走这里。

    图题和图用 KeepTogether 锁成一块。图在第 4 页、图题在第 5 页，
    两样东西都废了——读者既不知道这张图讲什么，也不知道这句话说的是哪张图。
    锁在一起后，放不下就整块换页，不会被拆开。
    """

    payload = item.get("payload") if isinstance(item.get("payload"), dict) else {}
    result: list[Flowable] = []
    for region in payload.get("regions", []):
        if not isinstance(region, dict):
            continue
        page_number = int(region.get("page") or item.get("page") or 0)
        if not 1 <= page_number <= source_document.page_count:
            continue
        caption = str(region.get("translation") or "").strip()
        # 图题要占位置，所以图能用的高度得先扣掉它，否则两者加起来放不下，
        # KeepTogether 会把整块推到下一页，白白空掉半页。
        caption_reserve = min(available_height * 0.2, 90.0) if caption else 0.0
        block: list[Flowable] = [
            _preserved_source_region_image(
                source_document,
                deps=deps,
                page_number=page_number,
                bbox=None if region.get("full_page") else region.get("bbox"),
                available_width=available_width,
                maximum_height=(
                    available_height * PRESERVED_REGION_MAX_HEIGHT_RATIO
                    - caption_reserve
                ),
                labels=(
                    region.get("labels")
                    if isinstance(region.get("labels"), list)
                    else None
                ),
                label_font_path=label_font_path,
            )
        ]
        if caption:
            block.append(Spacer(1, 4))
            block.append(Paragraph(_markup(caption), styles["caption"]))
        result.append(KeepTogether(block))
        result.append(Spacer(1, 6))
    return result


def _complex_flowables(
    item: dict[str, Any],
    *,
    deps: StoryDeps,
    styles: dict[str, ParagraphStyle],
    source_document: Any,
    available_width: float,
    available_height: float,
    regular_font: str,
    bold_font: str,
    body_font_pt: float,
    target_language: str = "zh-Hans",
    label_font_path: str | None = None,
) -> list[Flowable]:
    method = str(item.get("method") or "")
    payload = item.get("payload") if isinstance(item.get("payload"), dict) else {}
    prefix: list[Flowable] = (
        [PageBreak()] if payload.get("page_break_before") is True else []
    )
    components = payload.get("components")
    if isinstance(components, list) and components:
        result: list[Flowable] = list(prefix)
        primary_payload = dict(payload)
        primary_payload.pop("components", None)
        primary_payload.pop("page_break_before", None)
        result.extend(
            _complex_flowables(
                {
                    **item,
                    "payload": primary_payload,
                },
                deps=deps,
                styles=styles,
                source_document=source_document,
                available_width=available_width,
                available_height=available_height,
                regular_font=regular_font,
                bold_font=bold_font,
                body_font_pt=body_font_pt,
                target_language=target_language,
                label_font_path=label_font_path,
            )
        )
        for index, component in enumerate(components):
            if not isinstance(component, dict):
                continue
            component_item = {
                **item,
                "id": f"{item['id']}-component-{index + 1}",
                "method": component.get("method") or method,
                "payload": component.get("payload") or component,
            }
            result.extend(
                _complex_flowables(
                    component_item,
                    deps=deps,
                    styles=styles,
                    source_document=source_document,
                    available_width=available_width,
                    available_height=available_height,
                    regular_font=regular_font,
                    bold_font=bold_font,
                    body_font_pt=body_font_pt,
                    target_language=target_language,
                    label_font_path=label_font_path,
                )
            )
        return result
    if method in {"structured-table-rebuild", "semantic-grid-rebuild"}:
        return prefix + _table_flowables(
                item,
                styles=styles,
                available_width=available_width,
            )
    if method == "vector-rebuild":
        result = []
        for figure in payload.get("figures", []):
            if not isinstance(figure, dict):
                continue
            title = str(figure.get("title") or figure.get("caption") or "").strip()
            if title:
                result.append(Paragraph(_markup(title), styles["caption"]))
            result.append(
                VectorPayloadFlowable(
                    figure,
                    width=available_width,
                    regular_font=regular_font,
                    bold_font=bold_font,
                    body_font_pt=body_font_pt,
                    target_language=target_language,
                    message_fn=deps.message_fn,
                )
            )
            note_texts: list[str] = []
            note = str(figure.get("note") or "").strip()
            if note:
                note_texts.append(note)
            else:
                for annotation in figure.get("annotations", []):
                    if not isinstance(annotation, dict):
                        continue
                    if (
                        str(annotation.get("kind") or "").lower()
                        == "covariate-group"
                        or isinstance(annotation.get("x_ratio"), (int, float))
                        or isinstance(annotation.get("y_ratio"), (int, float))
                    ):
                        continue
                    annotation_text = str(
                        annotation.get("translation")
                        or annotation.get("label_translation")
                        or annotation.get("text")
                        or ""
                    ).strip()
                    if annotation_text and annotation_text not in note_texts:
                        note_texts.append(annotation_text)
            for note_text in note_texts:
                result.append(
                    Paragraph(_markup(note_text), styles["table_note"])
                )
            result.append(Spacer(1, 8))
        return prefix + result
    if method in {
        FALLBACK_PRESERVE_ELEMENT_REGION,
        FALLBACK_PRESERVE_FULL_PAGE,
    }:
        return prefix + _preserved_region_flowables(
            item,
            deps=deps,
            styles=styles,
            source_document=source_document,
            available_width=available_width,
            available_height=available_height,
            label_font_path=label_font_path,
        )
    if method in {"image-text-localization", "ocr-region-rebuild"}:
        return prefix + _with_figure_caption(
            _image_flowables(
                item,
                deps=deps,
                source_document=source_document,
                styles=styles,
                available_width=available_width,
                available_height=available_height,
                target_language=target_language,
            ),
            item,
            styles=styles,
        )
    return prefix


def _with_figure_caption(
    body: list[Flowable],
    item: dict[str, Any],
    *,
    styles: dict[str, ParagraphStyle],
) -> list[Flowable]:
    """把图级图题和图锁成一块。

    四联子图里每格自己的 (a)(b)(c)(d) 说明本来就跟着图走。但整张图的图题
    是一条独立的译文单元，排在正文流里，随时可能被分到上一页或下一页去——
    图在第 6 页、图题在第 7 页，读者既不知道这张图讲什么，也不知道这句话
    说的是哪张图。

    锁在一起后，放不下就整块换页。真放不下时 ReportLab 仍会拆，
    那是它自己的降级，好过一开始就不锁。
    """

    payload = item.get("payload") if isinstance(item.get("payload"), dict) else {}
    caption = str(payload.get(FIGURE_CAPTION_KEY) or "").strip()
    if not caption or not body:
        return body
    return [
        KeepTogether(
            [
                *body,
                Spacer(1, 4),
                Paragraph(_markup(caption), styles["caption"]),
            ]
        )
    ]


def _complex_render_policy(item: dict[str, Any]) -> str:
    payload = item.get("payload")
    if isinstance(payload, dict):
        policy = payload.get("render_policy")
        if policy in {"replace-page-units", "insert-before", "insert-after"}:
            return str(policy)
    return "insert-after"


def _complex_embedded_texts(item: dict[str, Any]) -> list[str]:
    payload = item.get("payload")
    if not isinstance(payload, dict):
        return []
    texts = [
        str(value)
        for value in payload.get("suppress_texts", [])
        if str(value).strip()
    ]
    # 图级图题已经跟着图一起排了，正文里那一份要抑制掉，否则印两遍。
    figure_caption = str(payload.get(FIGURE_CAPTION_KEY) or "").strip()
    if figure_caption:
        texts.append(figure_caption)
    texts.extend(
        [
        str(region.get("translation") or region.get("caption") or "")
        for region in payload.get("regions", [])
        if isinstance(region, dict)
        ]
    )
    for region in payload.get("regions", []):
        if not isinstance(region, dict):
            continue
        texts.extend(
            source
            for source, translation in _localized_image_labels(region)
            if source
        )
        texts.extend(
            translation
            for source, translation in _localized_image_labels(region)
            if translation
        )
        localized_caption = region.get("localized_caption")
        if isinstance(localized_caption, dict):
            texts.append(str(localized_caption.get("translation") or ""))
        doi = region.get("doi")
        if isinstance(doi, dict):
            texts.append(str(doi.get("translation") or ""))
        elif doi:
            texts.append(str(doi))
    for table in payload.get("tables", []):
        if not isinstance(table, dict):
            continue
        texts.extend(
            str(value or "")
            for value in (
                table.get("translated_title"),
                table.get("title_translation"),
                table.get("title"),
                table.get("caption"),
            )
            if str(value or "").strip()
        )
        raw_notes = (
            table.get("notes")
            or table.get("footnotes")
            or table.get("note")
            or table.get("footnote")
            or []
        )
        if isinstance(raw_notes, (str, dict)):
            raw_notes = [raw_notes]
        if isinstance(raw_notes, list):
            texts.extend(_table_note_text(note) for note in raw_notes)
        doi = str(table.get("doi") or "").strip()
        if doi:
            texts.extend((doi, f"DOI: {doi}", f"DOI：{doi}"))
    for component in payload.get("components", []):
        if not isinstance(component, dict):
            continue
        texts.extend(
            _complex_embedded_texts(
                {
                    "method": component.get("method"),
                    "payload": component.get("payload") or component,
                }
            )
        )
    return [text for text in texts if text.strip()]

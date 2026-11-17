"""位图渲染器。

位图没有可重画的余地：一张显微镜照片、一张分割结果图，像素就是全部内容。
所以这里只做三件事——**原样搬、不放大、把子图标签摆回去**。

三条容易出事的地方，都在这里堵住：

1. 放大低分辨率图。把 150 DPI 的图铺满半页，看起来更大，实际更糊。
   低分辨率图的缩放比例一律封顶在 1.0。
2. 子图标签掉进正文。a/b/c/d 是图的一部分，不是段落。它们的坐标必须落在
   各自子图的上方，而不是流进正文里变成孤零零的一行 "a"。
3. 编出原文没有的浮层说明。图上每一条中文都必须绑一个翻译单元，
   绑不上就抛错，不写。
"""

from __future__ import annotations

import re
from dataclasses import asdict, dataclass, field
from typing import Any

from academic_pdf_translation.contracts.models import BBox, normalize_bbox
from academic_pdf_translation.render.preserved_region_renderer import (
    PreservedRegionError,
    preserve_region,
)

MODE_PRESERVED = "preserve-image-as-is"

LAYOUT_ROW = "row"
LAYOUT_COLUMN = "column"

#: 有效分辨率下限。低于它，图里的细节就开始糊了，必须给警告。
MIN_EFFECTIVE_DPI = 150.0
#: 允许放大的分辨率门槛。原图达不到它就一律不放大——放大只会更糊。
UPSCALE_SAFE_DPI = 300.0
#: 横排时每张图允许缩到的最小比例。再小就不如改纵排。
MIN_ROW_SCALE = 0.60
#: 图片之间的间距（点）。
GROUP_GAP_PT = 6.0
#: 子图标签与图之间的间距（点）。
LABEL_GAP_PT = 2.0
#: 子图标签字号。
LABEL_FONT_PT = 8.0

#: 子图标签的样子：a、(a)、a)、a. ——都算。
SUBFIGURE_LABEL_RE = re.compile(r"^\(?([a-h])\)?[.)]?$", re.IGNORECASE)


class ImageRenderError(RuntimeError):
    """位图渲染失败。"""


@dataclass
class ImagePlacement:
    """一张图在候选里的落位。"""

    element_id: str
    target_bbox: list[float]
    scale: float


@dataclass
class RenderedImage:
    """一张位图的渲染结果与证据。"""

    element_id: str
    source_page: int
    candidate_page: int
    candidate_bbox: list[float]
    mode: str
    preserve_mode: str
    content_sha256: str
    pixel_width: int
    pixel_height: int
    source_dpi: float
    effective_dpi: float
    scale: float
    subfigure_label: str | None = None
    label_bbox: list[float] | None = None
    caption_element_id: str | None = None
    caption_page: int | None = None
    overlay_notes: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


def image_pixel_size(
    source_document: Any, element: dict[str, Any]
) -> tuple[int, int]:
    """取原图的像素尺寸。取不到就当 0，由调用方按未知处理。"""

    xref = (element.get("detail") or {}).get("xref")
    if not xref:
        return (0, 0)
    try:
        info = source_document.extract_image(int(xref))
    except Exception:  # noqa: BLE001 - 取不到就当未知，不能因此中断渲染
        return (0, 0)
    return (int(info.get("width") or 0), int(info.get("height") or 0))


def effective_dpi(pixels: int, span_pt: float) -> float:
    """像素数除以显示尺寸（英寸）。这是"这张图到底有多清楚"的唯一答案。"""

    if pixels <= 0 or span_pt <= 0:
        return 0.0
    return pixels / (span_pt / 72.0)


def is_subfigure_label(text: str) -> str | None:
    """认出 a/b/c/d 这类子图标签，返回规范化后的单个字母。"""

    match = SUBFIGURE_LABEL_RE.match(str(text or "").strip())
    return match.group(1).lower() if match else None


def verify_label_sequence(labels: list[str]) -> list[str]:
    """子图标签必须是完整的一串 a、b、c、d，不缺不跳不重。"""

    cleaned = [label for label in labels if label]
    if not cleaned:
        return []
    problems: list[str] = []
    if len(set(cleaned)) != len(cleaned):
        problems.append(f"子图标签重复: {cleaned}")
    expected = [chr(ord("a") + index) for index in range(len(cleaned))]
    if sorted(cleaned) != expected:
        problems.append(
            f"子图标签不连续: 实际 {sorted(cleaned)}，应为 {expected}"
        )
    return problems


def build_overlay_notes(notes: list[dict[str, Any]]) -> list[str]:
    """图上的中文说明。每一条都必须来自翻译单元，不许现编。"""

    lines: list[str] = []
    for index, note in enumerate(notes, 1):
        translation = str(note.get("translation") or "").strip()
        if not translation:
            continue
        if not str(note.get("translation_unit_id") or "").strip():
            raise ImageRenderError(
                f"图内说明第 {index} 条没有绑定 translation_unit_id: "
                f"{translation[:30]!r}"
            )
        lines.append(translation)
    return lines


def clamp_scale(scale: float, source_dpi: float) -> tuple[float, str | None]:
    """低分辨率图不放大。

    放大不会凭空补出像素，只会把每个像素摊得更大。原图分辨率不够时，
    宁可留白，也不要给读者一张更糊的大图。
    """

    if scale <= 1.0:
        return (scale, None)
    if source_dpi and source_dpi >= UPSCALE_SAFE_DPI:
        return (scale, None)
    return (
        1.0,
        f"原图有效分辨率 {source_dpi:.0f} DPI 不足 {UPSCALE_SAFE_DPI:.0f}，"
        f"放大倍数由 {scale:.2f} 收回到 1.00",
    )


def _fit_scale(source_box: BBox, target_box: BBox) -> float:
    source_width = max(source_box[2] - source_box[0], 1e-6)
    source_height = max(source_box[3] - source_box[1], 1e-6)
    return min(
        (target_box[2] - target_box[0]) / source_width,
        (target_box[3] - target_box[1]) / source_height,
    )


def _scaled_box(source_box: BBox, origin_x: float, origin_y: float, scale: float) -> list[float]:
    width = (source_box[2] - source_box[0]) * scale
    height = (source_box[3] - source_box[1]) * scale
    return [origin_x, origin_y, origin_x + width, origin_y + height]


def layout_image_group(
    elements: list[dict[str, Any]],
    area_bbox: Any,
    *,
    gap: float = GROUP_GAP_PT,
    min_row_scale: float = MIN_ROW_SCALE,
) -> tuple[str, list[ImagePlacement], list[str]]:
    """给一组子图排位。横排放不下就改纵排。

    四联子图本来是一行。但一行要塞进版心宽度，可能得把每张图缩到看不清。
    真到那一步，改成纵向一张一张排——占的地方多，图还是能看的。
    """

    area = normalize_bbox(area_bbox)
    if area is None:
        raise ImageRenderError("图片组缺少有效的可用区域")
    if not elements:
        return (LAYOUT_ROW, [], [])

    boxes: list[tuple[str, BBox]] = []
    for element in elements:
        box = normalize_bbox(element.get("bbox"))
        if box is None:
            raise ImageRenderError(
                f"{element.get('id')}: 图片缺少有效坐标，无法排位"
            )
        boxes.append((str(element.get("id") or ""), box))

    area_width = area[2] - area[0]
    area_height = area[3] - area[1]
    total_width = sum(box[2] - box[0] for _, box in boxes)
    total_gaps = gap * (len(boxes) - 1)
    row_scale = min(1.0, (area_width - total_gaps) / max(total_width, 1e-6))
    row_height = max(box[3] - box[1] for _, box in boxes) * row_scale

    warnings: list[str] = []
    if row_scale >= min_row_scale and row_height <= area_height:
        placements: list[ImagePlacement] = []
        cursor = area[0]
        for element_id, box in boxes:
            placed = _scaled_box(box, cursor, area[1], row_scale)
            placements.append(
                ImagePlacement(
                    element_id=element_id,
                    target_bbox=placed,
                    scale=round(row_scale, 4),
                )
            )
            cursor = placed[2] + gap
        return (LAYOUT_ROW, placements, warnings)

    if row_scale < min_row_scale:
        warnings.append(
            f"横排需要把每张图缩到 {row_scale:.2f}，低于 {min_row_scale:.2f}，"
            "改为纵向排列"
        )
    else:
        warnings.append(
            f"横排高度 {row_height:.1f} 点超出可用高度 {area_height:.1f} 点，"
            "改为纵向排列"
        )

    placements = []
    cursor_y = area[1]
    for element_id, box in boxes:
        scale = min(1.0, area_width / max(box[2] - box[0], 1e-6))
        placed = _scaled_box(box, area[0], cursor_y, scale)
        placements.append(
            ImagePlacement(
                element_id=element_id,
                target_bbox=placed,
                scale=round(scale, 4),
            )
        )
        cursor_y = placed[3] + gap
    total_height = cursor_y - gap - area[1]
    if total_height > area_height:
        warnings.append(
            f"纵排总高 {total_height:.1f} 点仍超出可用高度 "
            f"{area_height:.1f} 点，整组需要另起一页，不得拆散"
        )
    return (LAYOUT_COLUMN, placements, warnings)


def render_image(
    source_document: Any,
    candidate_page: Any,
    element: dict[str, Any],
    *,
    target_bbox: Any,
    subfigure_label: str | None = None,
    caption_element_id: str | None = None,
    caption_page: int | None = None,
    overlay_notes: list[dict[str, Any]] | None = None,
    min_dpi: float = MIN_EFFECTIVE_DPI,
    force_raster: bool = False,
) -> RenderedImage:
    """把一张位图原样放进候选，并把它的子图标签摆回去。"""

    element_id = str(element.get("id") or "")
    source_page = int(element.get("page") or 0)
    source_box = normalize_bbox(element.get("bbox"))
    target_box = normalize_bbox(target_bbox)
    if source_box is None or target_box is None:
        raise ImageRenderError(f"{element_id}: 缺少有效的原文坐标或目标坐标")

    pixel_width, pixel_height = image_pixel_size(source_document, element)
    source_span = source_box[2] - source_box[0]
    source_dpi = effective_dpi(pixel_width, source_span)

    warnings: list[str] = []
    scale, clamp_note = clamp_scale(_fit_scale(source_box, target_box), source_dpi)
    if clamp_note:
        warnings.append(clamp_note)

    placed_box = _scaled_box(source_box, target_box[0], target_box[1], scale)
    output_dpi = effective_dpi(pixel_width, placed_box[2] - placed_box[0])
    if pixel_width and output_dpi < min_dpi:
        warnings.append(
            f"落位后有效分辨率 {output_dpi:.0f} DPI 低于 {min_dpi:.0f}，"
            "图内细节可能看不清"
        )

    try:
        preserved = preserve_region(
            source_document,
            candidate_page,
            source_page=source_page,
            source_bbox=source_box,
            target_bbox=placed_box,
            element_id=element_id,
            force_raster=force_raster,
        )
    except PreservedRegionError as exc:
        raise ImageRenderError(f"{element_id}: 图片保留失败: {exc}") from exc

    label = None
    label_box: list[float] | None = None
    if subfigure_label is not None:
        label = is_subfigure_label(subfigure_label)
        if label is None:
            raise ImageRenderError(
                f"{element_id}: {subfigure_label!r} 不是子图标签"
            )
        label_box = _draw_subfigure_label(candidate_page, placed_box, label)

    if caption_page is not None and caption_page != preserved.candidate_page:
        warnings.append(
            f"图题在候选第 {caption_page} 页，图片在第 "
            f"{preserved.candidate_page} 页，必须同页"
        )

    return RenderedImage(
        element_id=element_id,
        source_page=source_page,
        candidate_page=preserved.candidate_page,
        candidate_bbox=list(preserved.candidate_bbox),
        mode=MODE_PRESERVED,
        preserve_mode=preserved.mode,
        content_sha256=preserved.content_sha256,
        pixel_width=pixel_width,
        pixel_height=pixel_height,
        source_dpi=round(source_dpi, 1),
        effective_dpi=round(output_dpi, 1),
        scale=round(scale, 4),
        subfigure_label=label,
        label_bbox=label_box,
        caption_element_id=caption_element_id,
        caption_page=caption_page,
        overlay_notes=build_overlay_notes(list(overlay_notes or [])),
        warnings=warnings,
    )


def _draw_subfigure_label(
    candidate_page: Any, placed_box: list[float], label: str
) -> list[float]:
    """把 a/b/c/d 画在它那张子图的正上方。

    标签是拉丁字母，用内置字体就够，不必依赖中文字体是否就位——
    正是这一点让标签不会因为缺字而变成空白方框。
    """

    baseline_y = max(placed_box[1] - LABEL_GAP_PT, LABEL_FONT_PT)
    candidate_page.insert_text(
        (placed_box[0], baseline_y),
        label,
        fontname="helv",
        fontsize=LABEL_FONT_PT,
    )
    return [
        placed_box[0],
        baseline_y - LABEL_FONT_PT,
        placed_box[0] + LABEL_FONT_PT,
        baseline_y,
    ]


def render_image_group(
    source_document: Any,
    candidate_page: Any,
    elements: list[dict[str, Any]],
    *,
    area_bbox: Any,
    subfigure_labels: dict[str, str] | None = None,
    caption_element_id: str | None = None,
    caption_page: int | None = None,
    gap: float = GROUP_GAP_PT,
) -> tuple[str, list[RenderedImage], list[str]]:
    """渲染一组子图。整组同页，标签跟着各自的图走。"""

    layout, placements, warnings = layout_image_group(
        elements, area_bbox, gap=gap
    )
    by_id = {str(element.get("id") or ""): element for element in elements}
    labels = subfigure_labels or {}
    rendered: list[RenderedImage] = []
    for placement in placements:
        rendered.append(
            render_image(
                source_document,
                candidate_page,
                by_id[placement.element_id],
                target_bbox=placement.target_bbox,
                subfigure_label=labels.get(placement.element_id),
                caption_element_id=caption_element_id,
                caption_page=caption_page,
            )
        )
    return (layout, rendered, warnings)


def verify_image_output(
    rendered: list[RenderedImage],
    candidate_page: Any,
    *,
    body_bbox: Any = None,
    min_dpi: float = MIN_EFFECTIVE_DPI,
) -> list[str]:
    """核对一组图有没有真的放对。

    这里逐条读候选页面，不看渲染器自己的记录——渲染器说它画了，
    和页面上真有，是两回事。
    """

    import fitz

    problems: list[str] = []
    if not rendered:
        return problems

    pages = {item.candidate_page for item in rendered}
    if len(pages) > 1:
        problems.append(f"同一组子图被分到了第 {sorted(pages)} 页")

    labels = [item.subfigure_label for item in rendered if item.subfigure_label]
    problems.extend(verify_label_sequence(labels))

    body = normalize_bbox(body_bbox)
    for item in rendered:
        if item.pixel_width and item.effective_dpi < min_dpi:
            problems.append(
                f"{item.element_id}: 有效分辨率 {item.effective_dpi:.0f} DPI "
                f"低于 {min_dpi:.0f}"
            )
        if item.scale > 1.0 and item.source_dpi < UPSCALE_SAFE_DPI:
            problems.append(
                f"{item.element_id}: 低分辨率图被放大到 {item.scale:.2f} 倍"
            )
        if item.caption_page is not None and (
            item.caption_page != item.candidate_page
        ):
            problems.append(f"{item.element_id}: 图题与图片不在同一页")
        if item.label_bbox is None:
            continue
        found = candidate_page.get_text(
            "text", clip=fitz.Rect(*item.label_bbox)
        ).strip()
        if item.subfigure_label not in found:
            problems.append(
                f"{item.element_id}: 子图标签 {item.subfigure_label!r} "
                "不在它那张图的上方"
            )
        if body is not None and _inside(item.label_bbox, body):
            problems.append(
                f"{item.element_id}: 子图标签落进了正文区域"
            )
    return problems


def _inside(box: list[float], container: BBox) -> bool:
    return (
        box[0] >= container[0]
        and box[1] >= container[1]
        and box[2] <= container[2]
        and box[3] <= container[3]
    )

"""原文区域保留渲染器。

这是所有安全降级的地基：别的渲染器失败时，都退到这里来。它只做一件事——
把原文的一块区域**原样**放进候选，不重画、不猜、不省略。

优先保留矢量内容（PyMuPDF 的 show_pdf_page 直接搬页面对象），矢量搬不动时
才退化成位图，且不低于 300 DPI。区域边缘不裁：宁可多留一点白边，
也不能把箭头或数字切掉半个。
"""

from __future__ import annotations

import hashlib
from dataclasses import asdict, dataclass, field
from typing import Any

from academic_pdf_translation.contracts.models import BBox, normalize_bbox

#: 栅格化降级时的最低分辨率。低于它，图里的数字就开始糊了。
MIN_RASTER_DPI = 300
#: 区域四周留的余量（点）。这是"不裁边"这条规则的实现。
EDGE_PADDING_PT = 2.0
#: PDF 的基准分辨率。
PDF_BASE_DPI = 72.0

MODE_VECTOR = "vector"
MODE_RASTER = "raster"


class PreservedRegionError(RuntimeError):
    """区域保留失败。调用方应当继续往下一级降级。"""


@dataclass
class PreservedRegion:
    """一次区域保留的结果与证据。"""

    source_element_id: str
    source_page: int
    source_bbox: list[float]
    candidate_page: int
    candidate_bbox: list[float]
    mode: str
    dpi: int | None
    content_sha256: str
    translation_key: list[str] = field(default_factory=list)

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


def _fitz():
    import fitz

    return fitz


def region_content_hash(document: Any, page_number: int, box: BBox) -> str:
    """原区域内容的哈希。

    用区域内的文字与绘图对象算，不用像素——像素会随渲染参数变，内容不会。
    它用来证明"候选里保留的就是原文这一块"。
    """

    fitz = _fitz()
    page = document[page_number - 1]
    clip = fitz.Rect(*box)
    payload: list[str] = []
    for block in page.get_text("blocks", clip=clip, sort=True):
        payload.append(str(block[4] or ""))
    for drawing in page.get_drawings():
        rect = drawing.get("rect")
        if rect is None:
            continue
        if fitz.Rect(rect).intersects(clip):
            payload.append(
                f"{round(rect.x0, 2)},{round(rect.y0, 2)},"
                f"{round(rect.x1, 2)},{round(rect.y1, 2)}"
            )
    digest = hashlib.sha256()
    digest.update(" ".join(payload).encode("utf-8"))
    return digest.hexdigest()


def _padded(box: BBox, page_rect: Any) -> BBox:
    """向外扩一点，保证不裁边；但不越出页面。"""

    return (
        max(float(page_rect.x0), box[0] - EDGE_PADDING_PT),
        max(float(page_rect.y0), box[1] - EDGE_PADDING_PT),
        min(float(page_rect.x1), box[2] + EDGE_PADDING_PT),
        min(float(page_rect.y1), box[3] + EDGE_PADDING_PT),
    )


def preserve_region(
    source_document: Any,
    candidate_page: Any,
    *,
    source_page: int,
    source_bbox: Any,
    target_bbox: Any,
    element_id: str,
    dpi: int = MIN_RASTER_DPI,
    force_raster: bool = False,
) -> PreservedRegion:
    """把原文的一块区域放进候选页。

    先试矢量：直接把原页那一块画进候选，文字仍可选可搜，线条不失真。
    矢量失败才退位图，分辨率不低于 300 DPI。
    """

    fitz = _fitz()
    box = normalize_bbox(source_bbox)
    target = normalize_bbox(target_bbox)
    if box is None or target is None:
        raise PreservedRegionError(
            f"{element_id}: 保留区域必须给出有效的原文坐标与目标坐标"
        )
    if not 1 <= source_page <= source_document.page_count:
        raise PreservedRegionError(f"{element_id}: 原文页码 {source_page} 越界")
    if dpi < MIN_RASTER_DPI:
        raise PreservedRegionError(
            f"{element_id}: 栅格化保留不得低于 {MIN_RASTER_DPI} DPI"
        )

    page = source_document[source_page - 1]
    clip = _padded(box, page.rect)
    content_hash = region_content_hash(source_document, source_page, clip)
    target_rect = fitz.Rect(*target)

    if not force_raster:
        try:
            candidate_page.show_pdf_page(
                target_rect,
                source_document,
                source_page - 1,
                clip=fitz.Rect(*clip),
                keep_proportion=True,
            )
        except Exception as exc:  # noqa: BLE001 - 要把真实原因带到降级里
            last_error = exc
        else:
            return PreservedRegion(
                source_element_id=element_id,
                source_page=source_page,
                source_bbox=list(clip),
                candidate_page=candidate_page.number + 1,
                candidate_bbox=list(target),
                mode=MODE_VECTOR,
                dpi=None,
                content_sha256=content_hash,
            )
    else:
        last_error = None

    try:
        zoom = dpi / PDF_BASE_DPI
        pixmap = page.get_pixmap(
            matrix=fitz.Matrix(zoom, zoom),
            clip=fitz.Rect(*clip),
            alpha=False,
        )
        candidate_page.insert_image(
            target_rect,
            pixmap=pixmap,
            keep_proportion=True,
        )
    except Exception as exc:  # noqa: BLE001
        raise PreservedRegionError(
            f"{element_id}: 矢量与栅格保留都失败了: {last_error or exc}"
        ) from exc

    return PreservedRegion(
        source_element_id=element_id,
        source_page=source_page,
        source_bbox=list(clip),
        candidate_page=candidate_page.number + 1,
        candidate_bbox=list(target),
        mode=MODE_RASTER,
        dpi=dpi,
        content_sha256=content_hash,
    )


def preserve_full_page(
    source_document: Any,
    candidate_document: Any,
    *,
    source_page: int,
    element_id: str = "",
) -> PreservedRegion:
    """第三级降级：整张原文页面原样保留。

    不漂亮，但它不会丢信息。中文阅读页由调用方另起一页生成。
    """

    fitz = _fitz()
    if not 1 <= source_page <= source_document.page_count:
        raise PreservedRegionError(f"原文页码 {source_page} 越界")
    page = source_document[source_page - 1]
    rect = page.rect
    new_page = candidate_document.new_page(width=rect.width, height=rect.height)
    new_page.show_pdf_page(
        fitz.Rect(0, 0, rect.width, rect.height),
        source_document,
        source_page - 1,
    )
    box = (float(rect.x0), float(rect.y0), float(rect.x1), float(rect.y1))
    return PreservedRegion(
        source_element_id=element_id or f"p{source_page:04d}-full-page",
        source_page=source_page,
        source_bbox=list(box),
        candidate_page=new_page.number + 1,
        candidate_bbox=list(box),
        mode=MODE_VECTOR,
        dpi=None,
        content_sha256=region_content_hash(source_document, source_page, box),
    )


def build_translation_key(entries: list[dict[str, Any]]) -> list[str]:
    """保留区域下方的中文对照键。

    每一条都必须来自某个翻译单元；没有来源的条目直接拒绝，
    不允许在这里补一句"看起来对"的说明。
    """

    key: list[str] = []
    for index, entry in enumerate(entries, 1):
        unit_id = str(entry.get("translation_unit_id") or "").strip()
        text = str(entry.get("translation") or "").strip()
        if not text:
            continue
        if not unit_id:
            raise PreservedRegionError(
                f"翻译键第 {index} 条没有绑定 translation_unit_id: {text[:30]!r}"
            )
        source = str(entry.get("source") or "").strip()
        key.append(
            f"{index}. {source} -> {text}" if source else f"{index}. {text}"
        )
    return key

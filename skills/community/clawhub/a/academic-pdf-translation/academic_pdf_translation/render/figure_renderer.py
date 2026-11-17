"""矢量图渲染器。

快速档的规则：**保留几何结构，只处理文字标签**。

结构图重画不得。一张网络结构图里有节点、箭头、跳连、通道数、特征图尺寸，
重画一遍必然丢东西——独立复审 R-001 报的"图 1 整张消失"就是重画失败后
只剩一列孤立数字。

所以几何原样搬。图内的文字标签分两种处理：映射得上就一对一覆盖中文；
映射不可靠就在图下方列编号图例，让读者自己对。**宁可让读者多看一眼图例，
也不要把中文盖到错的位置上。**
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any

from academic_pdf_translation.contracts.models import (
    BBox,
    bbox_area,
    normalize_bbox,
)
from academic_pdf_translation.render.preserved_region_renderer import (
    PreservedRegionError,
    preserve_region,
)

MODE_OVERLAY = "label-overlay"
MODE_LEGEND = "numbered-legend"

#: 覆盖标签时，中文块与原标签的重叠比例下限。低于它说明位置对不上。
MIN_LABEL_COVER_RATIO = 0.60
#: 保留区域的面积相对原区域的下限。缩得太狠，图里的数字就看不清了。
MIN_PRESERVED_AREA_RATIO = 0.25


class FigureRenderError(RuntimeError):
    """矢量图渲染失败。"""


@dataclass
class LabelPlacement:
    """一个图内标签的处理结果。"""

    translation_unit_id: str
    source_text: str
    translation: str
    source_bbox: list[float]
    #: 覆盖模式下是候选里的坐标；图例模式下为 None。
    candidate_bbox: list[float] | None = None
    legend_index: int | None = None

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class RenderedFigure:
    """一张矢量图的渲染结果与证据。"""

    element_id: str
    source_page: int
    candidate_page: int
    candidate_bbox: list[float]
    mode: str
    preserve_mode: str
    content_sha256: str
    source_drawing_count: int
    preserved_area_ratio: float
    labels: list[LabelPlacement] = field(default_factory=list)
    legend_lines: list[str] = field(default_factory=list)
    caption_element_id: str | None = None
    warnings: list[str] = field(default_factory=list)

    @property
    def label_count(self) -> int:
        return len(self.labels)

    def as_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["label_count"] = self.label_count
        return data


def label_mapping_confidence(
    labels: list[dict[str, Any]],
) -> float:
    """图内标签能不能一对一映射。

    判据是**每个标签都有坐标、有译文、有来源单元**。任何一条缺失，
    覆盖就可能盖到错的位置上，那还不如列图例。
    """

    # 只统计**需要翻译**的标签。图里的数字尺寸和通道数本来就保留原文，
    # 把它们算成"映射失败"会把置信度无谓地压下去，逼着一张本可以覆盖
    # 中文的图退化成图例。
    translatable = [
        label
        for label in labels
        if str(label.get("translation") or "").strip()
    ]
    if not translatable:
        return 0.0
    complete = 0
    for label in translatable:
        has_box = normalize_bbox(label.get("source_bbox")) is not None
        has_unit = bool(str(label.get("translation_unit_id") or "").strip())
        if has_box and has_unit:
            complete += 1
    return complete / len(translatable)


def _mapped_box(
    source_box: BBox,
    source_region: BBox,
    target_region: BBox,
) -> BBox:
    """把原图坐标线性映射到候选里保留区域的坐标。"""

    source_width = max(source_region[2] - source_region[0], 1e-6)
    source_height = max(source_region[3] - source_region[1], 1e-6)
    scale_x = (target_region[2] - target_region[0]) / source_width
    scale_y = (target_region[3] - target_region[1]) / source_height
    scale = min(scale_x, scale_y)
    offset_x = target_region[0]
    offset_y = target_region[1]
    return (
        offset_x + (source_box[0] - source_region[0]) * scale,
        offset_y + (source_box[1] - source_region[1]) * scale,
        offset_x + (source_box[2] - source_region[0]) * scale,
        offset_y + (source_box[3] - source_region[1]) * scale,
    )


def build_numbered_legend(labels: list[dict[str, Any]]) -> list[str]:
    """编号图例。

    每一条必须一对一对应一个原标签，**不许把几个图例并成一句话**：
    读者要能从图上的编号找回具体那一个标签。
    """

    lines: list[str] = []
    for index, label in enumerate(labels, 1):
        translation = str(label.get("translation") or "").strip()
        if not translation:
            continue
        unit_id = str(label.get("translation_unit_id") or "").strip()
        if not unit_id:
            raise FigureRenderError(
                f"图例第 {index} 条没有绑定 translation_unit_id: "
                f"{translation[:30]!r}"
            )
        source = str(label.get("source_text") or label.get("source") or "").strip()
        lines.append(
            f"{index}. {source} -> {translation}" if source else f"{index}. {translation}"
        )
    return lines


def render_figure(
    source_document: Any,
    candidate_page: Any,
    element: dict[str, Any],
    *,
    target_bbox: Any,
    labels: list[dict[str, Any]] | None = None,
    confidence_floor: float = 0.80,
    caption_element_id: str | None = None,
    force_raster: bool = False,
) -> RenderedFigure:
    """把一张矢量图保留进候选，并处理图内标签。"""

    element_id = str(element.get("id") or "")
    source_page = int(element.get("page") or 0)
    source_box = normalize_bbox(element.get("bbox"))
    target_box = normalize_bbox(target_bbox)
    if source_box is None or target_box is None:
        raise FigureRenderError(f"{element_id}: 缺少有效的原文坐标或目标坐标")

    try:
        preserved = preserve_region(
            source_document,
            candidate_page,
            source_page=source_page,
            source_bbox=source_box,
            target_bbox=target_box,
            element_id=element_id,
            force_raster=force_raster,
        )
    except PreservedRegionError as exc:
        raise FigureRenderError(
            f"{element_id}: 几何结构保留失败: {exc}"
        ) from exc

    warnings: list[str] = []
    source_area = bbox_area(source_box)
    target_area = bbox_area(target_box)
    area_ratio = target_area / source_area if source_area else 0.0
    if area_ratio < MIN_PRESERVED_AREA_RATIO:
        warnings.append(
            f"保留区域被缩到原图的 {area_ratio:.2f}，图内数字可能看不清"
        )

    label_list = list(labels or [])
    confidence = label_mapping_confidence(label_list)
    placements: list[LabelPlacement] = []
    legend_lines: list[str] = []

    if label_list and confidence >= confidence_floor:
        mode = MODE_OVERLAY
        for label in label_list:
            box = normalize_bbox(label.get("source_bbox"))
            if box is None:
                continue
            placements.append(
                LabelPlacement(
                    translation_unit_id=str(
                        label.get("translation_unit_id") or ""
                    ),
                    source_text=str(
                        label.get("source_text") or label.get("source") or ""
                    ),
                    translation=str(label.get("translation") or ""),
                    source_bbox=list(box),
                    candidate_bbox=list(
                        _mapped_box(box, source_box, target_box)
                    ),
                )
            )
    else:
        mode = MODE_LEGEND
        legend_lines = build_numbered_legend(label_list)
        for index, label in enumerate(label_list, 1):
            box = normalize_bbox(label.get("source_bbox"))
            placements.append(
                LabelPlacement(
                    translation_unit_id=str(
                        label.get("translation_unit_id") or ""
                    ),
                    source_text=str(
                        label.get("source_text") or label.get("source") or ""
                    ),
                    translation=str(label.get("translation") or ""),
                    source_bbox=list(box) if box else [],
                    legend_index=index,
                )
            )
        if label_list:
            warnings.append(
                f"图内标签映射置信度 {confidence:.2f} 低于 {confidence_floor:.2f}，"
                "改用编号图例，不把中文盖到可能错误的位置上"
            )

    return RenderedFigure(
        element_id=element_id,
        source_page=source_page,
        candidate_page=preserved.candidate_page,
        candidate_bbox=list(preserved.candidate_bbox),
        mode=mode,
        preserve_mode=preserved.mode,
        content_sha256=preserved.content_sha256,
        source_drawing_count=int(
            (element.get("detail") or {}).get("drawing_count") or 0
        ),
        preserved_area_ratio=round(area_ratio, 4),
        labels=placements,
        legend_lines=legend_lines,
        caption_element_id=caption_element_id,
        warnings=warnings,
    )


def verify_figure_output(
    rendered: RenderedFigure,
    candidate_drawing_count: int,
    candidate_text: str,
    *,
    expected_anchors: list[str] | None = None,
) -> list[str]:
    """核对一张图有没有真的保住。

    **绘图对象数量对得上不等于图是对的。** 一张图可能线条一根不少，
    通道数和特征图尺寸却全丢了——那些是文字，不是线条。所以这里除了看
    几何，还必须逐个核对数字锚点。
    """

    problems: list[str] = []
    if candidate_drawing_count <= 0 and rendered.source_drawing_count > 0:
        problems.append(
            f"{rendered.element_id}: 候选里没有任何绘图对象，几何结构丢了"
        )
    elif (
        rendered.source_drawing_count > 0
        and candidate_drawing_count < rendered.source_drawing_count
    ):
        problems.append(
            f"{rendered.element_id}: 候选绘图对象 {candidate_drawing_count} 个，"
            f"少于原文 {rendered.source_drawing_count} 个"
        )

    # 数字尺寸与通道数是文字，几何检查看不见它们，必须单独核。
    missing = [
        anchor
        for anchor in (expected_anchors or [])
        if anchor and anchor not in candidate_text
    ]
    if missing:
        problems.append(
            f"{rendered.element_id}: 图内数字锚点丢失: "
            + ", ".join(missing[:10])
        )

    translated_labels = [
        item for item in rendered.labels if item.translation.strip()
    ]
    if (
        rendered.mode == MODE_LEGEND
        and rendered.labels
        and len(rendered.legend_lines) != len(translated_labels)
    ):
        problems.append(
            f"{rendered.element_id}: 编号图例条数与图内标签数量对不上"
        )
    return problems

"""图片与矢量图检测。

关键一条：一张结构图在 PDF 里可能是几百个独立绘图对象。把它们当成
几百张图是错的，当成"这页很复杂"也是错的——必须聚成一个矢量图元素，
它才有资格被后面的结构对账盯住。

聚类用的是空间邻接：互相靠得足够近的绘图框合并成一个簇。
"""

from __future__ import annotations

from typing import Any

from academic_pdf_translation.contracts.models import (
    BBox,
    bbox_area,
    normalize_bbox,
    union_bbox,
)

DETECTOR_VERSION = "figures-v1"

#: 两个绘图框之间小于这个间距（点）就算同一个图形。
DEFAULT_CLUSTER_GAP_PT = 14.0
#: 少于这么多绘图对象的簇不算矢量图，多半是分隔线或下划线。
MIN_DRAWINGS_FOR_VECTOR_FIGURE = 6
#: 簇的面积至少要占页面这么大比例，否则算装饰线。
MIN_VECTOR_FIGURE_PAGE_AREA_RATIO = 0.02
#: 细长到这个程度的框是线，不是图。
MAX_LINE_THICKNESS_PT = 2.5


def _is_line_like(box: BBox) -> bool:
    width = box[2] - box[0]
    height = box[3] - box[1]
    return min(width, height) <= MAX_LINE_THICKNESS_PT


def _expanded(box: BBox, gap: float) -> BBox:
    return (box[0] - gap, box[1] - gap, box[2] + gap, box[3] + gap)


def _touches(first: BBox, second: BBox, gap: float) -> bool:
    grown = _expanded(first, gap)
    return not (
        grown[2] < second[0]
        or second[2] < grown[0]
        or grown[3] < second[1]
        or second[3] < grown[1]
    )


def cluster_boxes(
    boxes: list[BBox],
    *,
    gap: float = DEFAULT_CLUSTER_GAP_PT,
) -> list[list[int]]:
    """把互相邻接的框聚成簇，返回每簇的下标列表。

    并查集，按框的左上角排序后逐个合并。数量在几百这个量级，够用。
    """

    count = len(boxes)
    parent = list(range(count))

    def find(index: int) -> int:
        while parent[index] != index:
            parent[index] = parent[parent[index]]
            index = parent[index]
        return index

    def union(left: int, right: int) -> None:
        root_left, root_right = find(left), find(right)
        if root_left != root_right:
            parent[root_right] = root_left

    order = sorted(range(count), key=lambda index: (boxes[index][1], boxes[index][0]))
    for position, index in enumerate(order):
        for other in order[position + 1 :]:
            # 按 y 排序后，一旦下一个框的顶边超出当前框加间距，
            # 后面的框只会更远，可以停。
            if boxes[other][1] > boxes[index][3] + gap:
                break
            if _touches(boxes[index], boxes[other], gap):
                union(index, other)

    clusters: dict[int, list[int]] = {}
    for index in range(count):
        clusters.setdefault(find(index), []).append(index)
    return [sorted(members) for members in clusters.values()]


def detect_vector_figures(
    page: dict[str, Any],
    *,
    gap: float = DEFAULT_CLUSTER_GAP_PT,
) -> list[dict[str, Any]]:
    """从一页的绘图框里找出矢量图形。

    返回每个候选的 bbox、绘图对象数量、面积占比和置信度。
    """

    raw = [normalize_bbox(box) for box in page.get("drawing_bboxes") or []]
    boxes = [box for box in raw if box is not None]
    if not boxes:
        return []
    page_area = max(
        float(page.get("width") or 0) * float(page.get("height") or 0),
        1.0,
    )
    figures: list[dict[str, Any]] = []
    for members in cluster_boxes(boxes, gap=gap):
        member_boxes = [boxes[index] for index in members]
        bbox = union_bbox(member_boxes)
        if bbox is None:
            continue
        area_ratio = bbox_area(bbox) / page_area
        substantial = [box for box in member_boxes if not _is_line_like(box)]
        if (
            len(members) < MIN_DRAWINGS_FOR_VECTOR_FIGURE
            or area_ratio < MIN_VECTOR_FIGURE_PAGE_AREA_RATIO
            or not substantial
        ):
            continue
        # 绘图对象越多、面积越大，越确定它是一张图而不是几条线。
        confidence = min(
            0.99,
            0.6
            + min(len(members), 60) / 200.0
            + min(area_ratio, 0.5) * 0.5,
        )
        figures.append(
            {
                "bbox": bbox,
                "drawing_count": len(members),
                "solid_drawing_count": len(substantial),
                "page_area_ratio": round(area_ratio, 4),
                "confidence": round(confidence, 4),
            }
        )
    figures.sort(key=lambda item: (item["bbox"][1], item["bbox"][0]))
    return figures


def detect_raster_figures(page: dict[str, Any]) -> list[dict[str, Any]]:
    """位图区域。每个原生图片一个元素，互相靠得极近的算一组子图。"""

    results: list[dict[str, Any]] = []
    for image in page.get("images") or []:
        bbox = normalize_bbox(image.get("bbox"))
        if bbox is None:
            continue
        results.append(
            {
                "bbox": bbox,
                "xref": image.get("xref"),
                "image_id": image.get("id"),
                "confidence": 0.98,
            }
        )
    results.sort(key=lambda item: (item["bbox"][1], item["bbox"][0]))
    return results

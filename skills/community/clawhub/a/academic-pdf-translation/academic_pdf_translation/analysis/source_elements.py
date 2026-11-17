"""把一次原文扫描的结果装配成完整的元素清单。

输入是已经在磁盘上的 `source_structure.json`——原文只扫一次，这里不重扫。
输出是 `source_elements.json`：原文里的每一个正文、标题、图、表、公式、
脚注都有稳定 ID、坐标、置信度和关系。

后面的渲染计划、候选映射和结构对账全部挂在这些 ID 上。
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from academic_pdf_translation.analysis.detectors import (
    captions as caption_detector,
)
from academic_pdf_translation.analysis.detectors import (
    figures as figure_detector,
)
from academic_pdf_translation.analysis.detectors import (
    footnotes as footnote_detector,
)
from academic_pdf_translation.analysis.detectors import (
    formulas as formula_detector,
)
from academic_pdf_translation.analysis.detectors import (
    page_furniture as furniture_detector,
)
from academic_pdf_translation.analysis.detectors import tables as table_detector
from academic_pdf_translation.analysis.detectors import (
    text_roles as text_role_detector,
)
from academic_pdf_translation.contracts.enums import ElementType
from academic_pdf_translation.contracts.models import (
    RELATION_CAPTION,
    RELATION_CAPTIONS_FOR,
    RELATION_EMBEDDED_LABEL,
    RELATION_FOLLOWING_BODY,
    RELATION_LABEL_OF,
    RELATION_NOTE_FOR,
    RELATION_SECTION_HEADING,
    RELATION_TABLE_NOTE,
    BBox,
    SourceElement,
    SourceElementInventory,
    bbox_area,
    bbox_overlap,
    normalize_bbox,
)

#: 检测器整体版本。任何一个检测器改了行为，这里要跟着改。
DETECTOR_VERSION = "elements-v1"
ELEMENTS_FILE_NAME = "source_elements.json"

#: 文本块被视觉容器吞掉的重叠比例。
INSIDE_VISUAL_OVERLAP_RATIO = 0.60
#: 视觉元素附近多远算它的子图编号。
SUBFIGURE_LABEL_DISTANCE_PT = 30.0
#: 参考文献标题之后的块按题录处理。
REFERENCE_HEADING_WORDS = frozenset(
    {"references", "bibliography", "literature cited", "works cited", "参考文献"}
)


def cache_key(
    source_sha256: str,
    *,
    pymupdf_version: str,
    detector_version: str = DETECTOR_VERSION,
) -> str:
    """元素清单的缓存键。任何一项变化都让旧清单失效。"""

    payload = json.dumps(
        {
            "source_sha256": source_sha256,
            "detector_version": detector_version,
            "pymupdf_major": str(pymupdf_version).split(".")[0],
            "analyzer_version": "source-structure-v1",
        },
        sort_keys=True,
    )
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def _element_id(page: int, kind: str, index: int) -> str:
    return f"p{page:04d}-{kind}-{index:03d}"


def _near(box: BBox, container: BBox, distance: float) -> bool:
    from academic_pdf_translation.contracts.models import bbox_distance

    return bbox_distance(box, container) <= distance


def _inside_any(box: BBox | None, containers: list[BBox]) -> bool:
    if box is None:
        return False
    area = bbox_area(box)
    if area <= 0:
        return False
    return any(
        bbox_overlap(box, container) / area >= INSIDE_VISUAL_OVERLAP_RATIO
        for container in containers
    )


def _document_title_candidate(
    text_blocks: list[dict[str, Any]],
    page: dict[str, Any],
    *,
    is_first_page: bool,
) -> int | None:
    """首页题名的候选块：题名区里位置最高、又不是出版标识戳的那一块。

    "PDF 里的第一个文字块"不等于"读者看到的第一行"。期刊排版把版权栏、
    转载声明、顶端的生产代码条排在题名前面，PDF 里的块顺序也常和阅读
    顺序对不上。按位置挑，并且先排除出版标识戳，题名才落得回它该在的地方。
    """

    if not is_first_page:
        return None
    height = float(page.get("height") or 0) or 1.0
    limit = height * text_role_detector.TITLE_ZONE_RATIO
    best: tuple[float, float, int] | None = None
    for block in text_blocks:
        text = str(block.get("text") or "").strip()
        if not text or block.get("page_furniture"):
            continue
        if text_role_detector.is_publication_stamp(text):
            continue
        box = normalize_bbox(block.get("bbox"))
        if box is None:
            continue
        if best is None or box[1] < best[0]:
            best = (box[1], box[3], int(block.get("id", -1)))
    if best is None or best[1] > limit:
        # 最上面那一块都不在题名区里，说明这页的题名不在文字层里
        # （常见于题名被并进表格或图片）。这时不硬指一块当题名。
        return None
    return best[2]


def _page_elements(
    page: dict[str, Any],
    *,
    is_first_page: bool,
    in_references: bool,
) -> tuple[list[SourceElement], bool]:
    """处理一页，返回 (元素列表, 之后是否进入参考文献区)。"""

    page_number = int(page["page"])
    elements: list[SourceElement] = []
    counters: dict[str, int] = {}

    def new_id(kind: str) -> str:
        counters[kind] = counters.get(kind, 0) + 1
        return _element_id(page_number, kind, counters[kind])

    # --- 视觉容器先建立：它们会吞掉落在里面的文本块 ---
    visual_boxes: list[BBox] = []
    for figure in figure_detector.detect_vector_figures(page):
        element = SourceElement(
            id=new_id("figure"),
            page=page_number,
            type=ElementType.VECTOR_FIGURE,
            bbox=figure["bbox"],
            confidence=figure["confidence"],
            signals=["clustered-drawings"],
            detail={
                "drawing_count": figure["drawing_count"],
                "solid_drawing_count": figure["solid_drawing_count"],
                "page_area_ratio": figure["page_area_ratio"],
            },
        )
        element.add_risk("dense-vector", f"{figure['drawing_count']} 个绘图对象")
        elements.append(element)
        visual_boxes.append(figure["bbox"])

    for image in figure_detector.detect_raster_figures(page):
        element = SourceElement(
            id=new_id("image"),
            page=page_number,
            type=ElementType.RASTER_FIGURE,
            bbox=image["bbox"],
            confidence=image["confidence"],
            signals=["native-image"],
            detail={"xref": image["xref"], "image_id": image["image_id"]},
        )
        elements.append(element)
        visual_boxes.append(image["bbox"])

    # --- 表格 ---
    table_block_ids: set[int] = set()
    table_caption_block_ids: set[int] = set()
    for table in table_detector.detect_tables(page):
        element = SourceElement(
            id=new_id("table"),
            page=page_number,
            type=ElementType.TABLE,
            bbox=table["bbox"],
            confidence=table["confidence"],
            source_block_ids=list(table["block_ids"]),
            signals=list(table["signals"]),
            detail={
                "rule_count": table["rule_count"],
                "estimated_rows": table["rows"],
                "estimated_columns": table["columns"],
            },
        )
        if table["columns"] < 2:
            element.add_risk(
                "table-columns-unresolved",
                "列数无法从文字间距确定，结构化重建不可靠",
            )
        if table["confidence"] < 0.7:
            element.add_risk("table-low-confidence", "网格信号弱")
        elements.append(element)
        table_block_ids.update(table["block_ids"])
        if table["caption_block_id"] is not None:
            table_caption_block_ids.add(int(table["caption_block_id"]))
        visual_boxes.append(table["bbox"])

    # --- 公式：落在视觉容器里的候选不算公式，那是图内标签 ---
    formula_block_ids: set[int] = set()
    for formula in formula_detector.detect_display_formulas(page):
        if _inside_any(formula["bbox"], visual_boxes):
            continue
        if set(formula["block_ids"]) & table_block_ids:
            continue
        element = SourceElement(
            id=new_id("formula"),
            page=page_number,
            type=ElementType.DISPLAY_FORMULA,
            bbox=formula["bbox"],
            confidence=formula["confidence"],
            source_block_ids=list(formula["block_ids"]),
            signals=["math-density"],
            text=formula["text"],
            detail={
                "formula_number": formula["formula_number"],
                "math_density": formula["math_density"],
                "fragment_count": formula["fragment_count"],
            },
        )
        if formula["fragment_count"] > 1:
            element.add_risk(
                "formula-split-across-blocks",
                f"公式被抽取成 {formula['fragment_count']} 个片段",
            )
        elements.append(element)
        formula_block_ids.update(formula["block_ids"])

    # --- 脚注 ---
    footnote_block_ids: set[int] = set()
    for footnote in footnote_detector.detect_footnotes(page):
        element = SourceElement(
            id=new_id("footnote"),
            page=page_number,
            type=ElementType.FOOTNOTE,
            bbox=footnote["bbox"],
            confidence=footnote["confidence"],
            source_block_ids=[footnote["block_id"]],
            signals=["footnote-zone"]
            + (["marker"] if footnote["marker"] else [])
            + (["separator-rule"] if footnote["has_separator"] else []),
            text=footnote["text"],
            detail={"font_size": footnote["font_size"]},
        )
        elements.append(element)
        footnote_block_ids.add(footnote["block_id"])

    # --- 文本块 ---
    consumed = table_block_ids | formula_block_ids | footnote_block_ids
    text_blocks = [
        block
        for block in page.get("blocks") or []
        if int(block.get("id", -1)) not in consumed
    ]
    title_candidate_id = _document_title_candidate(
        text_blocks,
        page,
        is_first_page=is_first_page,
    )
    first_text_seen = False
    for block in text_blocks:
        block_id = int(block.get("id", -1))
        box = normalize_bbox(block.get("bbox"))
        text = str(block.get("text") or "").strip()
        if not text:
            continue

        furniture = furniture_detector.classify_furniture(block, page)
        if furniture is not None:
            elements.append(
                SourceElement(
                    id=new_id("furniture"),
                    page=page_number,
                    type=furniture,
                    bbox=box,
                    confidence=0.9,
                    source_block_ids=[block_id],
                    signals=["page-furniture"],
                    text=text,
                )
            )
            continue

        kind = caption_detector.caption_kind(text)
        if kind is not None or block_id in table_caption_block_ids:
            element = SourceElement(
                id=new_id("caption"),
                page=page_number,
                type=ElementType.CAPTION,
                bbox=box,
                confidence=0.9,
                source_block_ids=[block_id],
                signals=[f"{kind or 'table'}-caption"],
                text=text,
                detail={
                    "caption_kind": kind or "table",
                    "label": caption_detector.caption_label(text),
                },
            )
            elements.append(element)
            continue

        if table_detector.is_table_note(text):
            elements.append(
                SourceElement(
                    id=new_id("tablenote"),
                    page=page_number,
                    type=ElementType.TABLE_NOTE,
                    bbox=box,
                    confidence=0.8,
                    source_block_ids=[block_id],
                    signals=["table-note"],
                    text=text,
                )
            )
            continue

        inside_visual = _inside_any(box, visual_boxes)
        # 视觉容器旁边的单字母是子图编号（a/b/c/d），不是正文。
        near_visual_label = (
            not inside_visual
            and box is not None
            and len(text) <= 2
            and text.strip("()（）.").isalpha()
            and any(
                _near(box, container, SUBFIGURE_LABEL_DISTANCE_PT)
                for container in visual_boxes
            )
        )
        if near_visual_label:
            inside_visual = True
        element_type, confidence, signals = text_role_detector.classify_block(
            block,
            page,
            inside_visual=inside_visual,
            is_first_page=is_first_page,
            is_first_text_block=(
                block_id == title_candidate_id
                if title_candidate_id is not None
                else not first_text_seen
            ),
        )
        first_text_seen = True

        if inside_visual:
            elements.append(
                SourceElement(
                    id=new_id("label"),
                    page=page_number,
                    type=ElementType.UNKNOWN,
                    bbox=box,
                    confidence=confidence,
                    source_block_ids=[block_id],
                    signals=signals,
                    text=text,
                    detail={"role": "embedded-label"},
                )
            )
            continue

        # 参考文献区里的题录会含 arXiv 编号和 DOI，不能因此被当成
        # 出版元数据；这一区的普通文字一律按题录处理。
        if in_references and element_type in {
            ElementType.BODY,
            ElementType.PUBLICATION_METADATA,
        }:
            element_type = ElementType.REFERENCE_ENTRY
        if (
            element_type is ElementType.HEADING
            and text.strip().casefold().strip(" :：") in REFERENCE_HEADING_WORDS
        ):
            element_type = ElementType.REFERENCE_HEADING
            in_references = True

        element = SourceElement(
            id=new_id(
                "heading"
                if element_type
                in {ElementType.HEADING, ElementType.REFERENCE_HEADING}
                else "body"
            ),
            page=page_number,
            type=element_type,
            bbox=box,
            confidence=confidence,
            source_block_ids=[block_id],
            signals=signals,
            text=text,
        )
        if "heading-signal-rejected-by-text-shape" in signals:
            element.add_risk(
                "heading-classification-uncertain",
                "扫描认为是标题，文本形态不像",
            )
        elements.append(element)

    return elements, in_references


def _link_relations(elements: list[SourceElement]) -> None:
    """建立图题、表注、章节标题等关系。"""

    by_page: dict[int, list[SourceElement]] = {}
    for element in elements:
        by_page.setdefault(element.page, []).append(element)

    for page_elements in by_page.values():
        visuals = [
            (element.id, element.bbox)
            for element in page_elements
            if element.type
            in {
                ElementType.VECTOR_FIGURE,
                ElementType.RASTER_FIGURE,
                ElementType.CHART,
                ElementType.SCREENSHOT,
                ElementType.TABLE,
            }
            and element.bbox is not None
        ]
        by_id = {element.id: element for element in page_elements}

        for element in page_elements:
            if element.type is ElementType.CAPTION and element.bbox:
                kind = str(element.detail.get("caption_kind") or "")
                wanted = (
                    {ElementType.TABLE}
                    if kind == "table"
                    else {
                        ElementType.VECTOR_FIGURE,
                        ElementType.RASTER_FIGURE,
                        ElementType.CHART,
                        ElementType.SCREENSHOT,
                    }
                )
                candidates = [
                    (visual_id, box)
                    for visual_id, box in visuals
                    if by_id[visual_id].type in wanted
                ]
                target, distance = caption_detector.bind_caption(
                    element.bbox, candidates
                )
                if target is None:
                    element.add_risk(
                        "caption-without-visual",
                        "附近找不到可以绑定的图或表",
                    )
                    continue
                element.link(RELATION_CAPTIONS_FOR, target)
                element.detail["caption_distance"] = round(distance, 2)
                by_id[target].link(RELATION_CAPTION, element.id)

            if element.type is ElementType.TABLE_NOTE and element.bbox:
                tables = [
                    (visual_id, box)
                    for visual_id, box in visuals
                    if by_id[visual_id].type is ElementType.TABLE
                ]
                target, _ = caption_detector.bind_caption(element.bbox, tables)
                if target is not None:
                    element.link(RELATION_NOTE_FOR, target)
                    by_id[target].link(RELATION_TABLE_NOTE, element.id)

            embedded_label = (
                element.type is ElementType.UNKNOWN
                and element.detail.get("role") == "embedded-label"
                and element.bbox
            )
            if embedded_label:
                target, _ = caption_detector.bind_caption(
                    element.bbox,
                    visuals,
                    max_distance=float("inf"),
                )
                if target is not None:
                    element.link(RELATION_LABEL_OF, target)
                    by_id[target].link(RELATION_EMBEDDED_LABEL, element.id)

    ordered = sorted(elements, key=lambda item: (item.page, item.bbox[1] if item.bbox else 0))
    current_heading: SourceElement | None = None
    for element in ordered:
        if element.type in {ElementType.HEADING, ElementType.REFERENCE_HEADING}:
            current_heading = element
            continue
        if element.type is ElementType.BODY and current_heading is not None:
            current_heading.link(RELATION_FOLLOWING_BODY, element.id)
            element.link(RELATION_SECTION_HEADING, current_heading.id)


def build_inventory(
    structure: dict[str, Any],
    *,
    pymupdf_version: str = "0",
) -> SourceElementInventory:
    """从 source_structure.json 装配元素清单。"""

    elements: list[SourceElement] = []
    in_references = False
    pages = structure.get("pages") or []
    for index, page in enumerate(pages):
        page_elements, in_references = _page_elements(
            page,
            is_first_page=index == 0,
            in_references=in_references,
        )
        elements.extend(page_elements)

    _link_relations(elements)

    source_sha256 = str(structure.get("source_sha256") or "")
    inventory = SourceElementInventory(
        source_sha256=source_sha256,
        page_count=int(structure.get("page_count") or len(pages)),
        elements=elements,
        detector_version=DETECTOR_VERSION,
        cache_key=cache_key(source_sha256, pymupdf_version=pymupdf_version),
    )
    inventory.unresolved_elements = [
        {
            "element_id": element.id,
            "page": element.page,
            "type": element.type.value,
            "reason": [risk.code for risk in element.risk_flags],
        }
        for element in elements
        if element.type is ElementType.UNKNOWN
        and element.detail.get("role") != "embedded-label"
    ]
    return inventory


def analyze_job_elements(
    job_dir: Path,
    *,
    pymupdf_version: str = "0",
) -> SourceElementInventory:
    """读取作业里的原文结构，生成并写出元素清单。"""

    job_dir = Path(job_dir).resolve()
    job = json.loads((job_dir / "job.json").read_text(encoding="utf-8"))
    structure_path = job_dir / job.get("files", {}).get(
        "source_structure", "source_structure.json"
    )
    structure = json.loads(structure_path.read_text(encoding="utf-8"))
    inventory = build_inventory(structure, pymupdf_version=pymupdf_version)
    (job_dir / ELEMENTS_FILE_NAME).write_text(
        json.dumps(inventory.as_dict(), ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return inventory

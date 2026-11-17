from __future__ import annotations

import argparse
import math
import re
from collections import Counter
from pathlib import Path
from typing import Any

import perf_trace
from _common import SkillError, utc_now, write_json
from source_analysis import PageScan, SourceAnalysis, analyze_source


FURNITURE_DIGIT_RE = re.compile(r"\d+")
SPACE_RE = re.compile(r"\s+")


def _clean_text(text: str) -> str:
    return SPACE_RE.sub(" ", text or "").strip()


def _furniture_key(text: str) -> str:
    compact = _clean_text(text).lower()
    compact = FURNITURE_DIGIT_RE.sub("#", compact)
    return compact[:180]


def _bbox(block: dict[str, Any]) -> list[float]:
    return [round(float(value), 3) for value in block["bbox"]]


def _block_text(block: dict[str, Any]) -> str:
    return "\n".join(
        "".join(span.get("text", "") for span in line.get("spans", []))
        for line in block.get("lines", [])
    ).strip()


def _block_font_summary(block: dict[str, Any]) -> dict[str, Any]:
    spans = [
        span
        for line in block.get("lines", [])
        for span in line.get("spans", [])
        if _clean_text(span.get("text", ""))
    ]
    if not spans:
        return {
            "median_size": 0.0,
            "max_size": 0.0,
            "bold_signal": False,
            "font_names": [],
        }
    sizes = sorted(float(span.get("size", 0.0)) for span in spans)
    middle = len(sizes) // 2
    median = (
        sizes[middle]
        if len(sizes) % 2
        else (sizes[middle - 1] + sizes[middle]) / 2
    )
    names = sorted(
        {
            str(span.get("font") or "")
            for span in spans
            if str(span.get("font") or "")
        }
    )
    bold_signal = any(
        "bold" in str(span.get("font") or "").lower()
        or int(span.get("flags", 0)) & 16
        for span in spans
    )
    return {
        "median_size": round(median, 3),
        "max_size": round(max(sizes), 3),
        "bold_signal": bold_signal,
        "font_names": names,
    }


def _line_rows(block: dict[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for index, line in enumerate(block.get("lines", [])):
        spans = [
            span
            for span in line.get("spans", [])
            if _clean_text(span.get("text", ""))
        ]
        text = "".join(span.get("text", "") for span in line.get("spans", []))
        if not _clean_text(text):
            continue
        font_weights: Counter[str] = Counter()
        for span in spans:
            font = str(span.get("font") or "")
            if font:
                font_weights[font] += max(len(_clean_text(span.get("text", ""))), 1)
        rows.append(
            {
                "index": index,
                "text": text.strip(),
                "bbox": [
                    round(float(value), 3)
                    for value in line.get("bbox", block["bbox"])
                ],
                "font": _block_font_summary({"lines": [line]}),
                "dominant_font": (
                    font_weights.most_common(1)[0][0] if font_weights else ""
                ),
            }
        )
    return rows


def _joined_bbox(lines: list[dict[str, Any]]) -> list[float]:
    return [
        round(min(float(line["bbox"][0]) for line in lines), 3),
        round(min(float(line["bbox"][1]) for line in lines), 3),
        round(max(float(line["bbox"][2]) for line in lines), 3),
        round(max(float(line["bbox"][3]) for line in lines), 3),
    ]


def _line_is_heading(
    line: dict[str, Any],
    *,
    body_size: float,
    body_font_name: str,
) -> bool:
    text = _clean_text(str(line.get("text") or ""))
    if (
        not text
        or len(text) > 120
        or text.endswith((".", ";", ",", "。", "；", "，"))
    ):
        return False
    font = line.get("font", {})
    dominant_font = str(line.get("dominant_font") or "")
    style_changed = bool(
        dominant_font
        and body_font_name
        and dominant_font != body_font_name
    )
    size_changed = abs(float(font.get("max_size") or 0.0) - body_size) >= 0.35
    return style_changed or size_changed


def _block_segments(
    block: dict[str, Any],
    *,
    body_size: float,
    body_font_name: str,
) -> list[dict[str, Any]]:
    lines = list(block.get("lines") or [])
    if len(lines) < 2:
        return [
            {
                "index": 0,
                "role": "heading" if block.get("likely_heading") else "body",
                "heading_level": (
                    1 if block.get("likely_heading") else None
                ),
                "text": str(block.get("text") or ""),
                "bbox": list(block.get("bbox") or []),
            }
        ]

    local_font_weights: Counter[str] = Counter()
    local_sizes: list[float] = []
    for line in lines:
        font_name = str(line.get("dominant_font") or "")
        if font_name:
            local_font_weights[font_name] += max(
                len(_clean_text(str(line.get("text") or ""))),
                1,
            )
        size = float(line.get("font", {}).get("max_size") or 0.0)
        if size:
            local_sizes.append(size)
    local_body_font = (
        local_font_weights.most_common(1)[0][0]
        if local_font_weights
        else body_font_name
    )
    local_sizes.sort()
    local_body_size = (
        local_sizes[len(local_sizes) // 2]
        if local_sizes
        else body_size
    )

    heading_lines: list[dict[str, Any]] = []
    for line in lines:
        if not _line_is_heading(
            line,
            body_size=local_body_size,
            body_font_name=local_body_font,
        ):
            break
        heading_lines.append(line)

    if not heading_lines or len(heading_lines) == len(lines):
        return [
            {
                "index": 0,
                "role": "heading" if block.get("likely_heading") else "body",
                "heading_level": (
                    1 if block.get("likely_heading") else None
                ),
                "text": str(block.get("text") or ""),
                "bbox": list(block.get("bbox") or []),
            }
        ]

    segments: list[dict[str, Any]] = []
    for line in heading_lines:
        max_size = float(line.get("font", {}).get("max_size") or 0.0)
        segments.append(
            {
                "index": len(segments),
                "role": "heading",
                "heading_level": (
                    1 if max_size >= local_body_size + 0.2 else 2
                ),
                "text": str(line.get("text") or ""),
                "bbox": list(line.get("bbox") or []),
            }
        )
    body_lines = lines[len(heading_lines) :]
    segments.append(
        {
            "index": len(segments),
            "role": "body",
            "heading_level": None,
            "text": "\n".join(str(line.get("text") or "") for line in body_lines),
            "bbox": _joined_bbox(body_lines),
        }
    )
    return segments


def _inversion_ratio(first: list[int], second: list[int]) -> float:
    shared = [value for value in first if value in set(second)]
    if len(shared) < 2:
        return 0.0
    rank = {value: index for index, value in enumerate(second)}
    inversions = 0
    pairs = 0
    for left in range(len(shared)):
        for right in range(left + 1, len(shared)):
            pairs += 1
            if rank[shared[left]] > rank[shared[right]]:
                inversions += 1
    return round(inversions / max(pairs, 1), 4)


def _column_signal(
    blocks: list[dict[str, Any]],
    page_width: float,
) -> tuple[bool, dict[int, str]]:
    labels: dict[int, str] = {}
    left_chars = 0
    right_chars = 0
    wide_chars = 0
    center = page_width / 2
    gutter = page_width * 0.035
    for block in blocks:
        x0, _, x1, _ = map(float, block["bbox"])
        width = x1 - x0
        chars = len(_clean_text(block["text"]))
        if width >= page_width * 0.62 or (x0 < center - gutter and x1 > center + gutter):
            label = "wide"
            wide_chars += chars
        elif x1 <= center + gutter:
            label = "left"
            left_chars += chars
        elif x0 >= center - gutter:
            label = "right"
            right_chars += chars
        else:
            label = "ambiguous"
            wide_chars += chars
        labels[int(block["id"])] = label
    total = left_chars + right_chars + wide_chars
    two_column = (
        total >= 240
        and left_chars >= total * 0.2
        and right_chars >= total * 0.2
        and wide_chars <= total * 0.5
    )
    return two_column, labels


def _layout_order(
    blocks: list[dict[str, Any]],
    labels: dict[int, str],
    two_column: bool,
    page_height: float,
) -> list[int]:
    if not two_column:
        return [
            int(block["id"])
            for block in sorted(
                blocks,
                key=lambda item: (
                    round(float(item["bbox"][1]), 1),
                    round(float(item["bbox"][0]), 1),
                ),
            )
        ]

    wide_blocks = sorted(
        [block for block in blocks if labels[int(block["id"])] == "wide"],
        key=lambda item: (float(item["bbox"][1]), float(item["bbox"][0])),
    )
    boundaries = [0.0]
    boundaries.extend(float(block["bbox"][1]) for block in wide_blocks)
    boundaries.append(page_height + 1)

    order: list[int] = []
    used: set[int] = set()
    for zone_index in range(len(boundaries) - 1):
        top = boundaries[zone_index]
        bottom = boundaries[zone_index + 1]
        zone = [
            block
            for block in blocks
            if int(block["id"]) not in used
            and top <= (float(block["bbox"][1]) + float(block["bbox"][3])) / 2 < bottom
            and labels[int(block["id"])] != "wide"
        ]
        for label in ("left", "right", "ambiguous"):
            ordered = sorted(
                [
                    block
                    for block in zone
                    if labels[int(block["id"])] == label
                ],
                key=lambda item: (
                    float(item["bbox"][1]),
                    float(item["bbox"][0]),
                ),
            )
            order.extend(int(block["id"]) for block in ordered)
            used.update(int(block["id"]) for block in ordered)
        if zone_index < len(wide_blocks):
            anchor = wide_blocks[zone_index]
            anchor_id = int(anchor["id"])
            order.append(anchor_id)
            used.add(anchor_id)

    remaining = sorted(
        [block for block in blocks if int(block["id"]) not in used],
        key=lambda item: (float(item["bbox"][1]), float(item["bbox"][0])),
    )
    order.extend(int(block["id"]) for block in remaining)
    return order


def _likely_heading(
    text: str,
    font: dict[str, Any],
    body_size: float,
) -> bool:
    compact = _clean_text(text)
    if not compact or len(compact) > 120 or compact.endswith((".", ";", ",")):
        return False
    return bool(
        font["bold_signal"]
        or font["max_size"] >= max(body_size * 1.12, body_size + 0.8)
    )


def _page_data(
    scan: PageScan,
    furniture_keys: set[str],
    furniture_geometry: set[tuple[int, ...]] | None = None,
) -> dict[str, Any]:
    page_number = scan.number
    page_width = scan.width
    page_height = scan.height
    text_dict = scan.text_dict
    raw_text_blocks = [
        block for block in text_dict.get("blocks", []) if block.get("type") == 0
    ]
    block_rows: list[dict[str, Any]] = []
    all_sizes: list[float] = []
    page_font_weights: Counter[str] = Counter()
    for index, block in enumerate(raw_text_blocks):
        text = _block_text(block)
        if not _clean_text(text):
            continue
        font = _block_font_summary(block)
        lines = _line_rows(block)
        if font["median_size"]:
            all_sizes.append(float(font["median_size"]))
        for line in block.get("lines", []):
            for span in line.get("spans", []):
                font_name = str(span.get("font") or "")
                if font_name:
                    page_font_weights[font_name] += max(
                        len(_clean_text(span.get("text", ""))),
                        1,
                    )
        x0, y0, x1, y1 = map(float, block["bbox"])
        top_or_bottom = y1 <= page_height * 0.1 or y0 >= page_height * 0.9
        furniture = top_or_bottom and _furniture_key(text) in furniture_keys
        block_rows.append(
            {
                "id": index,
                "bbox": _bbox(block),
                "text": text,
                "line_count": len(block.get("lines", [])),
                "font": font,
                "lines": lines,
                "page_furniture": furniture,
            }
        )

    # 位置指纹只作用在本页的页眉页脚候选上：本页最上/最下、且与正文有
    # 明显空隙的那一块。栏首的题录哪怕每页都在同一高度，也不是页眉。
    if furniture_geometry:
        candidate_boxes = {
            _geometry_key((row[0], row[1], row[2], row[3]))
            for row in _furniture_candidates(
                [
                    (
                        float(row["bbox"][0]),
                        float(row["bbox"][1]),
                        float(row["bbox"][2]),
                        float(row["bbox"][3]),
                        str(row["text"]),
                    )
                    for row in block_rows
                ],
                page_height,
            )
        }
        for row in block_rows:
            key = _geometry_key(
                (
                    float(row["bbox"][0]),
                    float(row["bbox"][1]),
                    float(row["bbox"][2]),
                    float(row["bbox"][3]),
                )
            )
            if key in candidate_boxes and key in furniture_geometry:
                row["page_furniture"] = True

    content_blocks = [block for block in block_rows if not block["page_furniture"]]
    sizes = sorted(all_sizes)
    body_size = sizes[len(sizes) // 2] if sizes else 0.0
    body_font_name = (
        page_font_weights.most_common(1)[0][0] if page_font_weights else ""
    )
    for block in block_rows:
        block["likely_heading"] = _likely_heading(
            str(block["text"]),
            dict(block["font"]),
            body_size,
        )
        block["segments"] = _block_segments(
            block,
            body_size=body_size,
            body_font_name=body_font_name,
        )
        block["contains_heading"] = any(
            segment.get("role") == "heading"
            for segment in block["segments"]
        )

    two_column, labels = _column_signal(content_blocks, page_width)
    for block in block_rows:
        block["column"] = labels.get(int(block["id"]), "furniture")
    native_order = [int(block["id"]) for block in content_blocks]
    layout_order = _layout_order(
        content_blocks,
        labels,
        two_column,
        page_height,
    )
    disagreement = _inversion_ratio(native_order, layout_order)

    images = []
    for index, info in enumerate(scan.image_info, 1):
        bbox = info.get("bbox")
        if bbox:
            images.append(
                {
                    "id": index,
                    "bbox": [round(float(value), 3) for value in bbox],
                    "xref": int(info.get("xref", 0) or 0),
                }
            )
    drawing_count = scan.drawing_count
    drawing_boxes = [list(bbox) for bbox in scan.drawing_bboxes]
    source_text = scan.plain_text
    text_chars = len(_clean_text(source_text))
    page_area = max(page_width * page_height, 1.0)
    image_area = sum(
        max(0.0, item["bbox"][2] - item["bbox"][0])
        * max(0.0, item["bbox"][3] - item["bbox"][1])
        for item in images
    )
    image_ratio = min(image_area / page_area, 1.0)
    scan_risk = text_chars < 80 and image_ratio >= 0.35
    vector_dense = drawing_count >= 60
    table_signal = bool(
        re.search(r"(?im)^\s*(table|tab\.|表)\s*\d+", source_text)
        or (drawing_count >= 25 and len(content_blocks) >= 12)
    )
    figure_signal = bool(
        re.search(r"(?im)^\s*(fig(?:ure)?\.?|图)\s*\d+", source_text)
        or vector_dense
        or images
    )
    reasons: list[str] = []
    if scan_risk:
        reasons.append("missing-reliable-text-layer")
    if two_column and disagreement >= 0.18:
        reasons.append("reading-order-disagreement")
    if vector_dense:
        reasons.append("dense-vector-content")
    if table_signal:
        reasons.append("table-or-grid-signal")
    if images:
        reasons.append("image-content")
    if len(content_blocks) >= 45:
        reasons.append("many-text-blocks")

    by_id = {int(block["id"]): block for block in content_blocks}
    native_text = "\n\n".join(str(by_id[item]["text"]) for item in native_order)
    layout_text = "\n\n".join(str(by_id[item]["text"]) for item in layout_order)
    selected_order = "native"
    if two_column and disagreement >= 0.18:
        selected_order = "visual-confirmation-required"
    elif not two_column:
        selected_order = "layout"

    # 真正拿去切单元的顺序。两种顺序打架时，按几何算出来的那份赢：
    # 期刊首页的标题、作者、单位横跨栏顶，PDF 自带的块顺序常把双栏正文
    # 排在它们前面，照抄就会让标题掉到正文后面。这一页仍旧进"需要看图"
    # 的清单，标记不变，只是默认顺序改成看得懂的那一份。
    reading_order = (
        native_order if selected_order == "native" else layout_order
    )

    return {
        "page": page_number,
        "width": round(page_width, 3),
        "height": round(page_height, 3),
        "rotation": scan.rotation,
        "text_layer": {
            "text_chars": text_chars,
            "scan_risk": scan_risk,
            "native_text": native_text,
            "layout_text": layout_text,
        },
        "layout": {
            "two_column": two_column,
            "native_order": native_order,
            "layout_order": layout_order,
            "order_disagreement_ratio": disagreement,
            "selected_order": selected_order,
            "reading_order": reading_order,
        },
        "blocks": block_rows,
        "images": images,
        "image_area_ratio": round(image_ratio, 4),
        "drawing_count": drawing_count,
        "drawing_bboxes": drawing_boxes,
        "signals": {
            "table": table_signal,
            "figure": figure_signal,
            "vector_dense": vector_dense,
            "complex": bool(reasons),
            "reasons": reasons,
        },
    }


#: 页眉页脚与正文之间至少留这么多点，才算独立的一条。
FURNITURE_GAP_PT = 8.0


def _geometry_key(
    bbox: tuple[float, float, float, float],
) -> tuple[int, int, int]:
    """页眉页脚的位置指纹：左边界与上下沿，按 1 点取整。

    版式排出来的页眉每页落在同一条基线上，页码换了、刊名换了都不影响。
    文字指纹只认得每页一字不差的那种页眉；左右页轮换的"刊名 / 作者"
    页眉，两半各自的重复次数都不够，就漏了下来，最后混进正文。
    位置指纹不看文字，两种页眉都认得出。宽度不进指纹，页眉文字长短
    每页都不同。
    """

    return (int(round(bbox[0])), int(round(bbox[1])), int(round(bbox[3])))


def _furniture_candidates(
    rows: list[tuple[float, float, float, float, str]],
    height: float,
) -> list[tuple[float, float, float, float, str]]:
    """本页可能是页眉页脚的块。

    只有本页最上面（或最下面）那一块才有资格，而且它与相邻正文之间要有
    明显空隙。少了这一条，栏首的参考文献题录也会因为每页都排在同一个
    高度而被当成页眉。
    """

    ordered = sorted(
        (row for row in rows if _clean_text(row[4])),
        key=lambda row: (row[1], row[0]),
    )
    if len(ordered) < 2:
        return []
    candidates: list[tuple[float, float, float, float, str]] = []
    top = ordered[0]
    if (
        top[3] <= height * 0.1
        and ordered[1][1] - top[3] >= FURNITURE_GAP_PT
    ):
        candidates.append(top)
    bottom = ordered[-1]
    if (
        bottom[1] >= height * 0.9
        and bottom[1] - ordered[-2][3] >= FURNITURE_GAP_PT
    ):
        candidates.append(bottom)
    return candidates


def _repeated_furniture_keys(
    analysis: SourceAnalysis,
) -> tuple[set[str], set[tuple[int, ...]]]:
    """返回 (重复的文字指纹, 重复的位置指纹)。"""

    text_counts: Counter[str] = Counter()
    geometry_counts: Counter[tuple[int, int, int]] = Counter()
    for scan in analysis.pages:
        height = scan.height
        rows = [
            (
                float(block[0]),
                float(block[1]),
                float(block[2]),
                float(block[3]),
                str(block[4]),
            )
            for block in scan.text_blocks
        ]
        seen_text: set[str] = set()
        for row in rows:
            text = _clean_text(row[4])
            if not text:
                continue
            if row[3] > height * 0.1 and row[1] < height * 0.9:
                continue
            key = _furniture_key(text)
            if len(key) >= 8:
                seen_text.add(key)
        text_counts.update(seen_text)
        geometry_counts.update(
            {
                _geometry_key((row[0], row[1], row[2], row[3]))
                for row in _furniture_candidates(rows, height)
            }
        )
    minimum = max(2, math.ceil(analysis.page_count * 0.35))
    # 位置指纹更严：至少要在三页上出现，才排除"两页正好对齐"的巧合。
    geometry_minimum = max(3, minimum)
    return (
        {key for key, count in text_counts.items() if count >= minimum},
        {
            key
            for key, count in geometry_counts.items()
            if count >= geometry_minimum
        },
    )


def extract_source_structure(
    source_pdf: Path,
    *,
    analysis: SourceAnalysis | None = None,
) -> dict[str, Any]:
    """提取原文文字块、坐标、栏位与复杂视觉信号。

    传入 `analysis` 时复用已完成的单次原文扫描，不再重复打开 PDF。
    """

    source_pdf = Path(source_pdf).resolve()
    if analysis is None:
        analysis = analyze_source(source_pdf)
    elif source_pdf != analysis.path:
        raise SkillError("传入的原文扫描结果与目标 PDF 不一致")

    with perf_trace.stage("source_structure"):
        furniture_keys, furniture_geometry = _repeated_furniture_keys(
            analysis
        )
        pages = [
            _page_data(scan, furniture_keys, furniture_geometry)
            for scan in analysis.pages
        ]
    visual_pages = [
        page["page"]
        for page in pages
        if page["layout"]["selected_order"] == "visual-confirmation-required"
        or page["text_layer"]["scan_risk"]
        or page["signals"]["table"]
        or page["signals"]["figure"]
    ]
    return {
        "schema_version": "1.0",
        "generated_at": utc_now(),
        "source": str(source_pdf),
        "source_sha256": analysis.sha256,
        "page_count": len(pages),
        "repeated_page_furniture_patterns": sorted(furniture_keys),
        "visual_confirmation_pages": visual_pages,
        "pages": pages,
        "interpretation": (
            "native_text 是 PDF 内部对象顺序；layout_text 是按坐标和栏位推断的顺序。"
            "两者冲突或页面含图表、扫描内容时，不自动宣称阅读顺序正确。"
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="提取 PDF 文字块、坐标、栏位、阅读顺序与复杂视觉信号"
    )
    parser.add_argument("input", type=Path, help="作业目录或源 PDF")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    try:
        source = args.input.resolve()
        if source.is_dir():
            source = source / "source.pdf"
            output = args.output or source.parent / "source_structure.json"
        else:
            output = args.output or source.with_suffix(".structure.json")
        report = extract_source_structure(source)
        write_json(output.resolve(), report)
        print(f"原文结构已写入: {output.resolve()}")
        print(
            "需看图确认页: "
            + (
                ", ".join(map(str, report["visual_confirmation_pages"]))
                or "无"
            )
        )
        return 0
    except SkillError as exc:
        print(f"错误: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

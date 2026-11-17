#!/usr/bin/env python3
"""Extract translatable, layout-aware text segments from a board game rulebook PDF."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import statistics
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Tuple

import fitz

from pdf_common import (
    BULLET_RE,
    GLOSSARY_CSV,
    PRIVATE_USE_RE,
    GlossaryIndex,
    GlossaryTerm,
    clean_text,
    compute_body_size,
    cjk_ratio,
    eprint,
    is_probably_keep,
    join_line_texts,
    load_glossary,
    overlap_area,
    rect_area,
    drawings_summary,
    page_drawings,
    page_geometry,
    page_image_infos,
    rect_to_list,
    setup_stdout,
    sRGB_to_rgb,
    union_rects,
    write_json,
)

VERSION = "1.0.0"
DEFAULT_DPI = 110
MIN_GAP_Y = 5.0
MIN_GAP_X = 8.0


def parse_pages(spec: Optional[str], count: int) -> List[int]:
    if not spec:
        return list(range(1, count + 1))
    result: List[int] = []
    for part in spec.split(","):
        part = part.strip()
        if not part:
            continue
        if "-" in part:
            bits = part.split("-", 1)
            try:
                start, end = int(bits[0]), int(bits[1])
            except ValueError:
                raise ValueError(f"无效页码范围：{part}")
            if start > end:
                start, end = end, start
            result.extend(range(start, end + 1))
        else:
            result.append(int(part))
    bad = [p for p in result if p < 1 or p > count]
    if bad:
        raise ValueError(f"页码超出范围（1-{count}）：{bad}")
    return sorted(set(result))


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def weighted_style(spans: Sequence[Dict[str, Any]]) -> Dict[str, Any]:
    useful = [span for span in spans if (span.get("text") or "").strip()]
    if not useful:
        useful = list(spans)
    total = sum(max(1, len((span.get("text") or "").strip())) for span in useful) or 1
    size = sum(float(span.get("size", 0) or 0) *
               max(1, len((span.get("text") or "").strip())) for span in useful) / total
    bold_weight = 0
    italic_weight = 0
    color_weight: Counter = Counter()
    font_names: List[str] = []
    for span in useful:
        weight = max(1, len((span.get("text") or "").strip()))
        flags = int(span.get("flags", 0) or 0)
        font_name = str(span.get("font", "") or "")
        font_names.append(font_name)
        if flags & 16 or re.search(r"(bold|black|heavy|semibold|demibold)", font_name, re.I):
            bold_weight += weight
        if flags & 2 or re.search(r"(italic|oblique)", font_name, re.I):
            italic_weight += weight
        color_weight[int(span.get("color", 0) or 0)] += weight
    color_int = color_weight.most_common(1)[0][0]
    return {
        "size": round(size, 2),
        "bold": bold_weight >= total / 2,
        "italic": italic_weight >= total / 2,
        "color": [round(v, 4) for v in sRGB_to_rgb(color_int)],
        "font_names": sorted(set(font_names)),
        "superscript": any(int(span.get("flags", 0) or 0) & 1 for span in useful),
    }


def collect_lines(page: fitz.Page) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]], List[str]]:
    raw = page.get_text("dict", flags=fitz.TEXTFLAGS_TEXT)
    lines: List[Dict[str, Any]] = []
    rotated: List[Dict[str, Any]] = []
    font_names: List[str] = []
    idx = 0
    for block_idx, block in enumerate(raw.get("blocks", [])):
        if block.get("type") != 0:
            continue
        for line_idx, line in enumerate(block.get("lines", [])):
            spans = line.get("spans", [])
            text = "".join(clean_text(span.get("text", "")) for span in spans)
            if not text.strip():
                continue
            style = weighted_style(spans)
            font_names.extend(style["font_names"])
            direction = line.get("dir", (1.0, 0.0))
            is_rotated = abs(float(direction[0]) - 1.0) > 0.01 or abs(float(direction[1])) > 0.01
            bbox = fitz.Rect(line.get("bbox", (0, 0, 0, 0)))
            bbox = bbox & page.rect
            if bbox.is_empty or bbox.width <= 0 or bbox.height <= 0:
                continue
            item = {
                "idx": idx,
                "block": block_idx,
                "line": line_idx,
                "bbox": bbox,
                "text": text,
                "size": style["size"],
                "bold": style["bold"],
                "italic": style["italic"],
                "color": style["color"],
                "font_names": style["font_names"],
                "superscript": style["superscript"],
                "rotated": is_rotated,
            }
            if is_rotated:
                rotated.append(item)
            else:
                lines.append(item)
            idx += 1
    return lines, rotated, sorted(set(font_names))


def attach_tables(page: fitz.Page, lines: Sequence[Dict[str, Any]]
                  ) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]], set]:
    """Return (table groups, cell segments, consumed line indexes)."""
    line_owner: Dict[int, Tuple[int, int]] = {}
    table_records: List[Dict[str, Any]] = []
    try:
        found = page.find_tables()
        tables = list(found.tables)
    except Exception:
        tables = []

    for table in tables:
        raw_cells = getattr(table, "cells", None) or []
        table_rect = fitz.Rect(getattr(table, "bbox", (0, 0, 0, 0)))
        if table_rect.is_empty:
            continue
        seen_cells = set()
        cells: List[fitz.Rect] = []
        for raw_cell in raw_cells:
            if not raw_cell:
                continue
            rect = fitz.Rect(raw_cell) & page.rect
            if rect.is_empty or rect.width < 2 or rect.height < 2:
                continue
            key = tuple(round(v, 1) for v in rect)
            if key in seen_cells:
                continue
            seen_cells.add(key)
            cells.append(rect)
        if len(cells) < 2:
            continue
        table_idx = len(table_records)
        table_records.append({"bbox": table_rect, "cells": cells})
        for cell_idx, cell in enumerate(cells):
            for line in lines:
                if line["idx"] in line_owner:
                    continue
                area = max(1.0, rect_area(line["bbox"]))
                ov = overlap_area(cell, line["bbox"])
                if ov < 0.22 * area:
                    continue
                center = fitz.Point((line["bbox"].x0 + line["bbox"].x1) / 2,
                                    (line["bbox"].y0 + line["bbox"].y1) / 2)
                if not (cell.contains(center) or ov >= 0.55 * area):
                    continue
                current = line_owner.get(line["idx"])
                if current is not None:
                    cur_rect = table_records[current[0]]["cells"][current[1]]
                    if overlap_area(cur_rect, line["bbox"]) >= ov:
                        continue
                line_owner[line["idx"]] = (table_idx, cell_idx)

    if not table_records:
        return [], [], set()

    cell_lines: Dict[Tuple[int, int], List[Dict[str, Any]]] = defaultdict(list)
    for line in lines:
        owner = line_owner.get(line["idx"])
        if owner is not None:
            cell_lines[owner].append(line)

    groups: List[Dict[str, Any]] = []
    all_cell_segments: List[Dict[str, Any]] = []
    for table_idx, record in enumerate(table_records):
        cell_segments: List[Dict[str, Any]] = []
        for cell_idx, cell in enumerate(record["cells"]):
            cell_line_items = cell_lines.get((table_idx, cell_idx), [])
            if not cell_line_items:
                continue
            cell_line_items.sort(key=lambda item: (round(item["bbox"].y0, 2), item["bbox"].x0))
            text = join_line_texts([item["text"] for item in cell_line_items])
            if not text:
                continue
            dominant_size = statistics.median([item["size"] for item in cell_line_items])
            dominant_color = Counter(tuple(item["color"]) for item in cell_line_items).most_common(1)[0][0]
            seg = {
                "id": "",
                "page": 0,
                "text": text,
                "lines": [rect_to_list(item["bbox"] & cell) for item in cell_line_items],
                "bbox": rect_to_list(union_rects([item["bbox"] for item in cell_line_items])),
                "font_size": round(float(dominant_size), 2),
                "bold": any(item["bold"] for item in cell_line_items),
                "italic": any(item["italic"] for item in cell_line_items),
                "color": [round(float(v), 4) for v in dominant_color],
                "align": detect_align_from_lines(
                    [item["bbox"] & cell for item in cell_line_items], container=cell),
                "kind": "table_cell",
                "table": True,
                "cell": rect_to_list(cell),
                "table_bbox": rect_to_list(record["bbox"]),
                "block": -1,
                "line_indices": [item["idx"] for item in cell_line_items],
                "inline_art": False,
                "obstacles": [],
                "suggest_keep": False,
                "keep_reason": "",
                "rotated": False,
                "note": "",
                "glossary": [],
                "superscript": False,
                "_cell_rect": cell,
                "_line_rects": [item["bbox"] & cell for item in cell_line_items],
            }
            cell_segments.append(seg)
        cell_segments.sort(key=lambda seg: (round(seg["cell"][1], 1), seg["cell"][0], seg["cell"][3]))
        if cell_segments:
            groups.append({
                "bbox": rect_to_list(record["bbox"]),
                "segments": cell_segments,
            })
            all_cell_segments.extend(cell_segments)
    return groups, all_cell_segments, set(line_owner.keys())


def split_runs(block_lines: Sequence[Dict[str, Any]]) -> List[Tuple[List[Dict[str, Any]], bool]]:
    ordered = sorted(block_lines, key=lambda item: (round(item["bbox"].y0, 2), item["bbox"].x0))
    if not ordered:
        return []
    gaps = []
    for prev, nxt in zip(ordered, ordered[1:]):
        gaps.append(max(0.0, nxt["bbox"].y0 - prev["bbox"].y1))
    median_gap = statistics.median(gaps) if gaps else 3.0
    gap_threshold = max(6.0, median_gap * 2.5 + 1.5)
    runs: List[List[Dict[str, Any]]] = []
    current = [ordered[0]]
    for prev, nxt in zip(ordered, ordered[1:]):
        gap = max(0.0, nxt["bbox"].y0 - prev["bbox"].y1)
        if BULLET_RE.match(nxt["text"].strip()) and current:
            prev_text = current[-1]["text"].strip()
            prev_is_bullet = bool(BULLET_RE.match(prev_text))
            prev_ended = bool(prev_text) and prev_text[-1] in ".!?:;。！？：；"
            marker = nxt["text"].lstrip()[:1]
            strong_bullet = marker in "•▪▫●○◆◇■□►▶*"
            if prev_is_bullet or prev_ended or strong_bullet:
                runs.append(current)
                current = [nxt]
                continue
        size_change = abs(float(nxt["size"]) - float(prev["size"])) > 1.4
        bold_change = bool(nxt["bold"]) != bool(prev["bold"]) and (
            abs(float(nxt["size"]) - float(prev["size"])) > 0.4)
        min_width = max(1.0, min(prev["bbox"].width, nxt["bbox"].width))
        x_overlap = min(prev["bbox"].x1, nxt["bbox"].x1) - max(prev["bbox"].x0, nxt["bbox"].x0)
        x_disjoint = x_overlap < 0.18 * min_width
        if gap > gap_threshold or size_change or bold_change or x_disjoint:
            runs.append(current)
            current = [nxt]
        else:
            current.append(nxt)
    runs.append(current)
    result = []
    for run in runs:
        flat = False
        if len(run) == 1 and len(ordered) > 1:
            for other in ordered:
                if other is run[0]:
                    continue
                vertical = min(run[0]["bbox"].y1, other["bbox"].y1) - max(run[0]["bbox"].y0, other["bbox"].y0)
                horizontal = min(run[0]["bbox"].x1, other["bbox"].x1) - max(run[0]["bbox"].x0, other["bbox"].x0)
                if vertical > 0.5 * min(run[0]["bbox"].height, other["bbox"].height) and horizontal < 0:
                    flat = True
                    break
        result.append((run, flat))
    return result


def detect_align_from_lines(line_rects: Sequence[fitz.Rect],
                            container: Optional[fitz.Rect] = None) -> str:
    if not line_rects:
        return "left"
    if container is None:
        container = union_rects(line_rects)
    if len(line_rects) >= 2:
        centers = [(r.x0 + r.x1) / 2 for r in line_rects]
        if max(centers) - min(centers) <= 2.0:
            return "center"
        rights = [r.x1 for r in line_rects]
        lefts = [r.x0 for r in line_rects]
        if max(rights) - min(rights) <= 2.0 and max(lefts) - min(lefts) > 4.0:
            return "right"
    if container.width > 0:
        center = (container.x0 + container.x1) / 2
        seg_center = sum((r.x0 + r.x1) / 2 for r in line_rects) / len(line_rects)
        left_margin = min(r.x0 for r in line_rects) - container.x0
        right_margin = container.x1 - max(r.x1 for r in line_rects)
        if abs(seg_center - center) <= max(2.0, container.width * 0.04) and \
                left_margin > 3 and right_margin > 3:
            return "center"
    return "left"


def make_regular_segments(page: fitz.Page, lines: Sequence[Dict[str, Any]],
                          consumed: set) -> List[Dict[str, Any]]:
    by_block: Dict[int, List[Dict[str, Any]]] = defaultdict(list)
    for line in lines:
        if line["idx"] in consumed:
            continue
        by_block[line["block"]].append(line)

    segments: List[Dict[str, Any]] = []
    for block_idx, block_lines in sorted(by_block.items()):
        for run, flat in split_runs(block_lines):
            text = join_line_texts([item["text"] for item in run])
            if not text:
                continue
            line_rects = [item["bbox"] for item in run]
            bbox = union_rects(line_rects)
            sizes = [item["size"] for item in run]
            fonts = []
            for item in run:
                fonts.extend(item["font_names"])
            color = Counter(tuple(item["color"]) for item in run).most_common(1)[0][0]
            align = detect_align_from_lines(line_rects, container=None)
            seg = {
                "id": "",
                "page": 0,
                "text": text,
                "lines": [rect_to_list(rect) for rect in line_rects],
                "bbox": rect_to_list(bbox),
                "font_size": round(float(statistics.median(sizes)), 2),
                "bold": sum(1 for item in run if item["bold"]) >= len(run) / 2,
                "italic": sum(1 for item in run if item["italic"]) >= len(run) / 2,
                "color": [round(float(v), 4) for v in color],
                "align": align,
                "kind": "body",
                "table": False,
                "cell": None,
                "table_bbox": None,
                "block": block_idx,
                "line_indices": [item["idx"] for item in run],
                "inline_art": False,
                "obstacles": [],
                "suggest_keep": False,
                "keep_reason": "",
                "rotated": False,
                "note": "",
                "glossary": [],
                "superscript": any(item.get("superscript") for item in run),
                "font_names": sorted(set(fonts)),
                "flat": flat,
                "_line_rects": line_rects,
            }
            segments.append(seg)
    return segments


def xy_cut(items: Sequence[Dict[str, Any]]) -> List[Dict[str, Any]]:
    if len(items) <= 1:
        return list(items)

    def find_gaps(axis: str) -> List[Tuple[float, float, float]]:
        if axis == "y":
            intervals = sorted((item["bbox"].y0, item["bbox"].y1) for item in items)
        else:
            intervals = sorted((item["bbox"].x0, item["bbox"].x1) for item in items)
        gaps = []
        end = intervals[0][1]
        for start, finish in intervals[1:]:
            if start - end >= (MIN_GAP_Y if axis == "y" else MIN_GAP_X):
                gaps.append((end, start, start - end))
            end = max(end, finish)
        return gaps

    h_gaps = find_gaps("y")
    v_gaps = find_gaps("x")
    choice = None
    if h_gaps:
        h = max(h_gaps, key=lambda item: item[2])
        choice = ("y", h, h[2] * 1.08)
    if v_gaps:
        v = max(v_gaps, key=lambda item: item[2])
        if choice is None or v[2] > choice[2]:
            choice = ("x", v, v[2])
    if choice is None:
        return sorted(items, key=lambda item: (round(item["bbox"].y0, 1),
                                               round(item["bbox"].x0, 1)))

    axis, gap, _score = choice
    cut = (gap[0] + gap[1]) / 2.0
    if axis == "y":
        before = [item for item in items if item["bbox"].y1 <= cut + 0.01]
        after = [item for item in items if item["bbox"].y0 >= cut - 0.01]
    else:
        before = [item for item in items if item["bbox"].x1 <= cut + 0.01]
        after = [item for item in items if item["bbox"].x0 >= cut - 0.01]
    if not before or not after:
        return sorted(items, key=lambda item: (round(item["bbox"].y0, 1),
                                               round(item["bbox"].x0, 1)))
    return xy_cut(before) + xy_cut(after)


def merge_fragments(segments: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Merge line fragments that PyMuPDF split into separate blocks."""
    merged: List[Dict[str, Any]] = []
    for seg in segments:
        if seg.get("table") or seg.get("suggest_keep"):
            merged.append(seg)
            continue
        if not merged:
            merged.append(seg)
            continue
        prev = merged[-1]
        if prev.get("table") or prev.get("suggest_keep"):
            merged.append(seg)
            continue
        prev_rect = fitz.Rect(prev["bbox"])
        rect = fitz.Rect(seg["bbox"])
        gap = rect.y0 - prev_rect.y1
        if not (-0.5 <= gap <= 2.5):
            merged.append(seg)
            continue
        if abs(float(prev["font_size"]) - float(seg["font_size"])) > 0.35:
            merged.append(seg)
            continue
        if bool(prev["bold"]) != bool(seg["bold"]):
            merged.append(seg)
            continue
        min_w = max(1.0, min(prev_rect.width, rect.width))
        x_overlap = min(prev_rect.x1, rect.x1) - max(prev_rect.x0, rect.x0)
        if x_overlap < 0.70 * min_w or abs(prev_rect.x0 - rect.x0) > 3.0:
            merged.append(seg)
            continue
        if BULLET_RE.match(seg["text"]):
            merged.append(seg)
            continue
        prev["text"] = join_line_texts([prev["text"], seg["text"]])
        prev["lines"].extend(seg["lines"])
        prev["bbox"] = rect_to_list(union_rects([fitz.Rect(prev["bbox"]), rect]))
        prev["line_indices"].extend(seg.get("line_indices", []))
        prev["note"] = (prev.get("note", "") + " " if prev.get("note") else "") + "已合并跨块段落。"
    return merged


def extract_edge_band(items: List[Dict[str, Any]], page_rect: fitz.Rect,
                      top: bool) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    """Pull a top/bottom band of short items out before XY-cut, when it looks like a header/footer."""
    band: List[Dict[str, Any]] = []
    rest: List[Dict[str, Any]] = []
    for item in items:
        if item.get("table") or len(item.get("payload", [])) != 1:
            rest.append(item)
            continue
        payload_seg = item["payload"][0]
        if BULLET_RE.match(payload_seg.get("text", "").strip()):
            rest.append(item)
            continue
        rect = item["bbox"]
        if top and rect.y1 <= page_rect.height * 0.12:
            band.append(item)
        elif (not top) and rect.y0 >= page_rect.height * 0.90:
            band.append(item)
        else:
            rest.append(item)
    if len(band) < 2 or len(band) > 4:
        return [], items
    intervals = sorted((item["bbox"].x0, item["bbox"].x1) for item in band)
    max_gap = 0.0
    end = intervals[0][1]
    for start, finish in intervals[1:]:
        max_gap = max(max_gap, start - end)
        end = max(end, finish)
    if max_gap < page_rect.width * 0.12:
        return [], items
    band.sort(key=lambda item: (round(item["bbox"].y0, 1), round(item["bbox"].x0, 1)))
    return band, rest


def column_bounds(seg: Dict[str, Any], all_segments: Sequence[Dict[str, Any]],
                  page_rect: fitz.Rect) -> Optional[Tuple[float, float]]:
    seg_rect = fitz.Rect(seg["bbox"])
    candidates = []
    for other in all_segments:
        if other is seg or other.get("table"):
            continue
        if other.get("kind") not in ("body", "list", "header_footer", "caption"):
            continue
        other_rect = fitz.Rect(other["bbox"])
        if other_rect.width > page_rect.width * 0.75:
            continue
        overlap = min(seg_rect.x1, other_rect.x1) - max(seg_rect.x0, other_rect.x0)
        if overlap <= 0:
            continue
        if abs((other_rect.y0 + other_rect.y1) / 2 - (seg_rect.y0 + seg_rect.y1) / 2) > 260:
            continue
        candidates.append(other_rect)
    if len(candidates) < 2:
        return None
    x0 = min(rect.x0 for rect in candidates + [seg_rect])
    x1 = max(rect.x1 for rect in candidates + [seg_rect])
    if x1 - x0 < page_rect.width * 0.2:
        return None
    return (x0, x1)


def classify_and_annotate(page: fitz.Page, segments: List[Dict[str, Any]],
                          body_size: float, image_infos: Sequence[Dict[str, Any]],
                          icon_candidates: Sequence[fitz.Rect],
                          page_warnings: List[str]) -> None:
    page_h = page.rect.height
    page_w = page.rect.width
    for seg in segments:
        rect = fitz.Rect(seg["bbox"])
        size = float(seg["font_size"])
        text = seg["text"]
        if seg["table"]:
            seg["kind"] = "table_cell"
        elif (rect.y1 < page_h * 0.085 or rect.y0 > page_h * 0.915) and                 size <= body_size * 1.06 and not BULLET_RE.match(text):
            seg["kind"] = "header_footer"
        elif size >= body_size * 1.18 or (
                seg["bold"] and size >= body_size * 1.02 and len(text) <= 90
                and not text.rstrip().endswith((".", "。", "!", "！", "?", "？"))) or (
                text.isupper() and 2 <= len(text) <= 70 and size >= body_size * 0.95):
            seg["kind"] = "heading"
        elif size <= body_size * 0.86 and len(text) <= 180:
            seg["kind"] = "caption"
        elif BULLET_RE.match(text):
            seg["kind"] = "list"
        else:
            seg["kind"] = "body"

    # Alignment for headings/captions/headers uses the page context after kinds exist.
    for seg in segments:
        rect = fitz.Rect(seg["bbox"])
        align = seg["align"]
        if seg["kind"] == "heading":
            line_rects = [fitz.Rect(item) for item in seg["lines"]]
            if len(line_rects) == 1:
                bounds = column_bounds(seg, segments, page.rect)
                centered = False
                if bounds:
                    col_w = bounds[1] - bounds[0]
                    center = (bounds[0] + bounds[1]) / 2
                    seg_center = (rect.x0 + rect.x1) / 2
                    left_margin = rect.x0 - bounds[0]
                    right_margin = bounds[1] - rect.x1
                    centered = abs(seg_center - center) <= max(4.0, col_w * 0.08) and \
                        left_margin > 4 and right_margin > 4
                page_center = (page.rect.x0 + page.rect.x1) / 2
                if not centered and rect.width < page_w * 0.7 and \
                        abs((rect.x0 + rect.x1) / 2 - page_center) <= page_w * 0.04:
                    centered = True
                align = "center" if centered else "left"
        elif seg["kind"] == "caption":
            if any(abs(((img_rect.x0 + img_rect.x1) / 2) - ((rect.x0 + rect.x1) / 2)) <=
                   max(8.0, img_rect.width * 0.08) and
                   ((img_rect.y1 <= rect.y0 + 4 and rect.y0 - img_rect.y1 <= 45) or
                    (rect.y1 <= img_rect.y0 + 4 and img_rect.y0 - rect.y1 <= 45))
                   for img_rect in (fitz.Rect(info["bbox"]) for info in image_infos)):
                align = "center"
        elif seg["kind"] == "header_footer":
            page_center = (page.rect.x0 + page.rect.x1) / 2
            if abs((rect.x0 + rect.x1) / 2 - page_center) <= page_w * 0.04:
                align = "center"
            elif rect.x1 > page.rect.x1 - 28 and page.rect.x1 - rect.x1 < 28:
                align = "right"
        seg["align"] = align

    # Inline art and obstacles, plus keep suggestions.
    page_area = max(1.0, rect_area(page.rect))
    for seg in segments:
        rect = fitz.Rect(seg["bbox"])
        size = float(seg["font_size"])
        line_rects = [fitz.Rect(item) for item in seg["lines"]]
        obstacles = []
        inline = False
        for info in image_infos:
            img_rect = fitz.Rect(info["bbox"])
            if img_rect.is_empty or (img_rect & rect).is_empty:
                continue
            img_area = max(1.0, rect_area(img_rect))
            if img_area > page_area * 0.5:
                continue  # full-page background, not an obstacle
            small = max(img_rect.width, img_rect.height) <= max(4.5 * size, 24.0)
            inside = overlap_area(img_rect, rect) >= 0.25 * img_area
            if small and inside:
                inline = True
                obstacles.append(img_rect)
        for icon_rect in icon_candidates:
            if (icon_rect & rect).is_empty:
                continue
            if max(icon_rect.width, icon_rect.height) > max(4.0 * size, 18.0):
                continue
            if overlap_area(icon_rect, rect) < 0.5 * max(1.0, rect_area(icon_rect)):
                continue
            obstacles.append(icon_rect)
            if any(overlap_area(icon_rect, line) > 0.5 for line in line_rects):
                inline = True
        # Deduplicate obstacles.
        unique = []
        seen = set()
        for obstacle in obstacles:
            key = tuple(round(v, 1) for v in obstacle)
            if key in seen:
                continue
            seen.add(key)
            unique.append(obstacle)
        seg["obstacles"] = [rect_to_list(obstacle) for obstacle in unique]
        seg["inline_art"] = bool(inline)
        if inline:
            seg["note"] = "含内嵌图标/插图，渲染时会绕开；请对照页面图核对图标顺序。"

        keep, reason = False, ""
        if is_probably_keep(seg["text"]):
            keep = True
            if cjk_ratio(seg["text"]) >= 0.4:
                reason = "原文已是中文"
            elif PRIVATE_USE_RE.search(seg["text"]):
                reason = "含图标字体私有字符，保留原文"
            elif re.match(r"^(https?://|www\.)", seg["text"].strip(), re.I) or "@" in seg["text"]:
                reason = "URL/邮箱，保留原文"
            else:
                reason = "纯数字/符号，保留原文"
        if seg.get("flat") and seg["kind"] not in ("header_footer", "heading"):
            seg["note"] = (seg["note"] + " " if seg["note"] else "") + "疑似无边框表格/标签。"
        if keep:
            seg["suggest_keep"] = True
            seg["keep_reason"] = reason
        if seg.get("superscript"):
            seg["note"] = (seg["note"] + " " if seg["note"] else "") + "含上标字符，请核对。"


def find_repeated_headers(all_segments: Sequence[Dict[str, Any]]) -> None:
    counts = Counter(normalize_key(seg["text"]) for seg in all_segments
                     if seg["kind"] == "header_footer" and len(seg["text"]) <= 100)
    for seg in all_segments:
        if seg["kind"] != "header_footer" or seg["suggest_keep"]:
            continue
        if counts[normalize_key(seg["text"])] >= 3:
            seg["suggest_keep"] = True
            seg["keep_reason"] = "跨页重复的页眉/页脚，建议保留原文"


def normalize_key(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip().lower()


def glossary_annotate(segments: Sequence[Dict[str, Any]], index: GlossaryIndex) -> Dict[str, Any]:
    found: Dict[str, Dict[str, Any]] = {}
    for seg in segments:
        hits = index.find(seg["text"])
        if not hits:
            continue
        seg_hits = []
        for term, matched, start, end in hits:
            seg_hits.append({
                "en": term.en,
                "zh": term.zh,
                "matched": matched,
                "category": term.category,
            })
            key = term.en.lower()
            entry = found.setdefault(key, {
                "term": term,
                "count": 0,
                "matches": Counter(),
                "pages": set(),
            })
            entry["count"] += 1
            entry["matches"][matched.lower()] += 1
            entry["pages"].add(seg["page"])
        seg["glossary"] = seg_hits
    return found


def write_source_md(path: Path, pages_info: Sequence[Dict[str, Any]],
                    segments_by_page: Dict[int, List[Dict[str, Any]]],
                    selected_pages: Sequence[int]) -> None:
    lines: List[str] = []
    lines.append("# 规则书原文分段（供翻译使用）")
    lines.append("")
    lines.append("> 不要修改本文件。译文写到 `translations.tsv`，第一列 id 保持不变；`=` 表示保留原文。")
    lines.append("")
    for page_no in selected_pages:
        info = next((item for item in pages_info if item["number"] == page_no), None)
        if not info:
            continue
        lines.append(f"## 第 {page_no} 页 · Page {page_no}")
        lines.append("")
        lines.append(f"![原文第 {page_no} 页](original/page_{page_no:04d}.png)")
        lines.append("")
        lines.append(
            f"- 尺寸：{info['rect'][2]:.0f} × {info['rect'][3]:.0f} pt；旋转：{info['rotation']}°；"
            f"图片：{len(info.get('images', []))} 个；文本字符：{info.get('text_chars', 0)}"
        )
        for warning in info.get("warnings", []):
            lines.append(f"- ⚠️ {warning}")
        lines.append("")
        segs = segments_by_page.get(page_no, [])
        if not segs:
            lines.append("_本页没有可提取的文字层。_")
            lines.append("")
        last_table = None
        for seg in segs:
            if seg.get("table") and seg.get("table_bbox") != last_table:
                last_table = seg.get("table_bbox")
                tb = last_table or [0, 0, 0, 0]
                lines.append(f"#### 表格 · bbox ({tb[0]:.0f}, {tb[1]:.0f}, {tb[2]:.0f}, {tb[3]:.0f})")
                lines.append("")
            flags = [seg["kind"], f"{seg['font_size']}pt", seg["align"]]
            if seg.get("inline_art"):
                flags.append("inline_art")
            bbox = seg["bbox"]
            lines.append(
                f"### {seg['id']} · " + " · ".join(flags) +
                f" · bbox ({bbox[0]:.0f}, {bbox[1]:.0f}, {bbox[2]:.0f}, {bbox[3]:.0f})"
            )
            if seg.get("suggest_keep"):
                lines.append(f"**建议保留原文**：{seg.get('keep_reason', '')}")
            if seg.get("note"):
                lines.append(f"> {seg['note']}")
            lines.append("")
            text = seg["text"]
            fence = "~~~"
            while fence in text:
                fence += "~"
            lines.append(fence + "text")
            lines.append(text)
            lines.append(fence)
            lines.append("")
        if info.get("rotated_lines"):
            lines.append("#### 旋转文字（未自动处理，保留原文）")
            lines.append("")
            for item in info["rotated_lines"]:
                lines.append(f"- bbox ({item['bbox'][0]:.0f}, {item['bbox'][1]:.0f}): `{item['text']}`")
            lines.append("")
        lines.append("---")
        lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def write_translation_template(path: Path, segments: Sequence[Dict[str, Any]],
                               reset: bool) -> bool:
    if path.exists() and not reset:
        return False
    lines = [
        "# boardgame-rulebook-zh 译文文件",
        "# 格式：id<TAB>中文译文；`=` 表示保留原文（不擦除、不覆盖）。",
        "# 不要改动 id；空译文会在渲染时报告为缺失。",
        "",
    ]
    for seg in segments:
        value = "=" if seg.get("suggest_keep") else ""
        lines.append(f"{seg['id']}\t{value}")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return True


def write_termbase(path: Path, found: Dict[str, Dict[str, Any]], reset: bool) -> bool:
    if path.exists() and not reset:
        return False
    rows = sorted(found.values(), key=lambda item: (-item["count"], item["term"].en.lower()))
    lines = [
        "# 项目术语库：source<TAB>zh<TAB>category<TAB>note",
        "# 官方中文版如与本表冲突，以官方译名为准，直接改第二列；QA 会以本表为准。",
        "# 可在此补充卡牌名、角色名、地名等专有名词。",
        "",
    ]
    for entry in rows:
        term: GlossaryTerm = entry["term"]
        note = term.note.replace("\t", " ")
        category = term.category.replace("\t", " ")
        lines.append(f"{term.en}\t{term.zh}\t{category}\t{note}")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return True


def write_glossary_hits_md(path: Path, found: Dict[str, Dict[str, Any]]) -> None:
    rows = sorted(found.values(), key=lambda item: (-item["count"], item["term"].en.lower()))
    lines = [
        "# 术语表命中",
        "",
        "| 原文术语 | 建议译法 | 次数 | 页码 | 备注 |",
        "| --- | --- | --- | --- | --- |",
    ]
    for entry in rows:
        term: GlossaryTerm = entry["term"]
        pages = ", ".join(str(p) for p in sorted(entry["pages"]))
        note = term.note.replace("|", "\\|")
        lines.append(f"| {term.en} | {term.zh} | {entry['count']} | {pages} | {note} |")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    setup_stdout()
    parser = argparse.ArgumentParser(description="提取桌游规则书 PDF 的可翻译文字段（保留版式）。")
    parser.add_argument("pdf", help="输入 PDF 路径")
    parser.add_argument("-o", "--out", default="work", help="工作目录（默认 work）")
    parser.add_argument("--pages", help="只提取指定页，如 1-3,5（1 基）")
    parser.add_argument("--dpi", type=int, default=DEFAULT_DPI, help="页面预览 DPI")
    parser.add_argument("--no-previews", action="store_true", help="不生成原始页面预览")
    parser.add_argument("--force", action="store_true", help="覆盖已有工作目录（保留已有译文）")
    parser.add_argument("--reset-translations", action="store_true", help="覆盖已有 translations.tsv / termbase.tsv")
    parser.add_argument("--glossary", default=str(GLOSSARY_CSV), help="术语表 CSV 路径")
    args = parser.parse_args()

    pdf_path = Path(args.pdf).resolve()
    if not pdf_path.exists():
        eprint(f"找不到 PDF：{pdf_path}")
        return 2
    out_dir = Path(args.out).resolve()
    if out_dir.exists() and any(out_dir.iterdir()) and not args.force:
        eprint(f"工作目录已存在且非空：{out_dir}\n如需覆盖请加 --force；已有译文会保留。")
        return 2
    out_dir.mkdir(parents=True, exist_ok=True)

    try:
        doc = fitz.open(str(pdf_path))
    except Exception as exc:
        eprint(f"无法打开 PDF：{exc}")
        return 2
    if doc.needs_pass:
        if not doc.authenticate(""):
            eprint("PDF 已加密，无法读取。请先解除密码。")
            return 2
    try:
        selected_pages = parse_pages(args.pages, doc.page_count)
    except Exception as exc:
        eprint(str(exc))
        return 2

    glossary = load_glossary(Path(args.glossary))
    glossary_index = GlossaryIndex(glossary)
    global_warnings: List[str] = []
    pages_info: List[Dict[str, Any]] = []
    segments_by_page: Dict[int, List[Dict[str, Any]]] = {}
    all_segments: List[Dict[str, Any]] = []
    source_fonts = set()
    scanned_pages: List[int] = []
    rotated_page_numbers: List[int] = []
    total_rotated_lines = 0

    (out_dir / "original").mkdir(exist_ok=True)
    (out_dir / "qa").mkdir(exist_ok=True)

    for page_no in selected_pages:
        page = doc.load_page(page_no - 1)
        warnings: List[str] = []
        image_infos = page_image_infos(page)
        page_text = page.get_text("text") or ""
        text_chars = len(page_text.strip())
        _, icon_candidates = page_drawings(page)
        lines, rotated_lines, fonts = collect_lines(page)
        source_fonts.update(fonts)
        total_rotated_lines += len(rotated_lines)
        if page.rotation:
            rotated_page_numbers.append(page_no)
            warnings.append(f"页面旋转 {page.rotation}°，已按原坐标处理；请目检文字方向。")
        if rotated_lines:
            warnings.append(f"有 {len(rotated_lines)} 行旋转文字，未自动替换，保留原文。")
        if text_chars < 20:
            if image_infos:
                scanned_pages.append(page_no)
                warnings.append("本页几乎没有文字层，疑似扫描页；不会进行覆盖式汉化。")
            elif page.get_drawings():
                warnings.append("本页没有文字层，可能是矢量描边文字；无法自动翻译。")
            else:
                warnings.append("本页几乎为空。")
        else:
            page_area = max(1.0, rect_area(page.rect))
            covered = 0.0
            for info in image_infos:
                covered += overlap_area(fitz.Rect(info["bbox"]), page.rect)
            coverage = min(1.0, covered / page_area)
            if coverage > 0.5:
                warnings.append(f"页面大面积被图片覆盖（约 {coverage:.0%}），请确认文字没有烘焙在图片里。")
            if "\ufffd" in page_text:
                warnings.append("文字层含替换字符（�），可能存在字体编码问题，请目检原文。")

        groups, cell_segments, consumed = attach_tables(page, lines)
        regular = make_regular_segments(page, lines, consumed)
        # Attach page numbers and placeholder ids before ordering.
        for seg in regular + cell_segments:
            seg["page"] = page_no
        items = []
        for seg in regular:
            items.append({"bbox": fitz.Rect(seg["bbox"]), "payload": [seg]})
        for group in groups:
            items.append({
                "bbox": fitz.Rect(group["bbox"]),
                "payload": group["segments"],
                "table": True,
            })
        top_band, items = extract_edge_band(items, page.rect, top=True)
        bottom_band, items = extract_edge_band(items, page.rect, top=False)
        ordered: List[Dict[str, Any]] = []
        for item in top_band:
            ordered.extend(item["payload"])
        for item in xy_cut(items):
            ordered.extend(item["payload"])
        for item in bottom_band:
            ordered.extend(item["payload"])
        ordered = merge_fragments(ordered)
        for idx, seg in enumerate(ordered, 1):
            seg["id"] = f"p{page_no:03d}_s{idx:03d}"
        segments_by_page[page_no] = ordered

        page_info = {
            "number": page_no,
            "geometry": page_geometry(page),
            "rect": rect_to_list(page.rect),
            "rotation": int(page.rotation),
            "images": image_infos,
            "drawings": drawings_summary(page),
            "text_chars": text_chars,
            "warnings": warnings,
            "scanned": page_no in scanned_pages,
            "segments": len(ordered),
            "rotated_lines": [
                {"bbox": rect_to_list(item["bbox"]), "text": item["text"]}
                for item in rotated_lines
            ],
        }
        pages_info.append(page_info)
        all_segments.extend(ordered)
        global_warnings.extend(f"第 {page_no} 页：{msg}" for msg in warnings)

        if not args.no_previews:
            pix = page.get_pixmap(dpi=args.dpi, alpha=False)
            pix.save(str(out_dir / "original" / f"page_{page_no:04d}.png"))

    if not all_segments:
        manifest = build_manifest(pdf_path, doc, selected_pages, pages_info,
                                  all_segments, 10.0, source_fonts,
                                  scanned_pages, global_warnings, args)
        write_json(out_dir / "manifest.json", manifest)
        eprint("没有提取到任何文字段。该 PDF 可能是扫描版或文字已转为矢量描边。")
        eprint("本 skill 不对扫描页做覆盖式汉化；请参阅 references/scanned-pdfs.md。")
        return 2

    body_size = compute_body_size(all_segments)
    for page_no in selected_pages:
        page = doc.load_page(page_no - 1)
        segs = segments_by_page.get(page_no, [])
        info = next(item for item in pages_info if item["number"] == page_no)
        image_infos = info["images"]
        _, icon_candidates = page_drawings(page)
        classify_and_annotate(page, segs, body_size, image_infos, icon_candidates, info["warnings"])

    find_repeated_headers(all_segments)
    found_terms = glossary_annotate(all_segments, glossary_index)

    # Source.md
    write_source_md(out_dir / "source.md", pages_info, segments_by_page, selected_pages)
    wrote_translations = write_translation_template(
        out_dir / "translations.tsv", all_segments, args.reset_translations
    )
    wrote_termbase = write_termbase(out_dir / "termbase.tsv", found_terms, args.reset_translations)
    write_glossary_hits_md(out_dir / "glossary_hits.md", found_terms)

    public_segments = [
        {key: value for key, value in seg.items() if not key.startswith("_")}
        for seg in all_segments
    ]
    segments_json = {
        "version": VERSION,
        "pdf_path": str(pdf_path),
        "body_size": body_size,
        "pages": pages_info,
        "segments": public_segments,
    }
    write_json(out_dir / "segments.json", segments_json)

    manifest = build_manifest(pdf_path, doc, selected_pages, pages_info,
                              all_segments, body_size, source_fonts,
                              scanned_pages, global_warnings, args)
    manifest["translations_template_written"] = wrote_translations
    manifest["termbase_written"] = wrote_termbase
    manifest["stats"] = {
        "segments": len(all_segments),
        "table_cells": sum(1 for seg in all_segments if seg["table"]),
        "headings": sum(1 for seg in all_segments if seg["kind"] == "heading"),
        "inline_art": sum(1 for seg in all_segments if seg["inline_art"]),
        "suggest_keep": sum(1 for seg in all_segments if seg["suggest_keep"]),
        "glossary_terms": len(found_terms),
    }
    write_json(out_dir / "manifest.json", manifest)

    print(f"已提取 {len(selected_pages)} 页，{len(all_segments)} 个文字段。")
    print(f"正文基准字号：{body_size}pt；表格单元：{manifest['stats']['table_cells']} 个；"
          f"含内嵌图标段：{manifest['stats']['inline_art']} 个。")
    if scanned_pages:
        print(f"警告：疑似扫描页 {scanned_pages}，这些页不会覆盖汉化。")
    if rotated_page_numbers:
        print(f"提示：旋转页 {rotated_page_numbers}，请目检方向。")
    if not wrote_translations:
        print("已保留现有 translations.tsv（未覆盖）。")
    if not wrote_termbase:
        print("已保留现有 termbase.tsv（未覆盖）。")
    print(f"下一步：阅读 {out_dir / 'source.md'}，填写 {out_dir / 'translations.tsv'}，"
          f"然后运行 render.py。")
    return 0


def build_manifest(pdf_path: Path, doc: fitz.Document,
                   selected_pages: Sequence[int], pages_info: Sequence[Dict[str, Any]],
                   segments: Sequence[Dict[str, Any]], body_size: float,
                   source_fonts: Sequence[str], scanned_pages: Sequence[int],
                   warnings: Sequence[str], args: argparse.Namespace) -> Dict[str, Any]:
    metadata = doc.metadata or {}
    return {
        "version": VERSION,
        "created_at": __import__("datetime").datetime.now().astimezone().isoformat(timespec="seconds"),
        "pdf_path": str(pdf_path),
        "pdf_sha256": file_sha256(pdf_path),
        "pdf_size": pdf_path.stat().st_size,
        "doc": {
            "page_count": doc.page_count,
            "metadata": {key: metadata.get(key) for key in
                         ("title", "author", "subject", "creator", "producer", "creationDate", "modDate")},
            "encrypted": bool(doc.needs_pass),
        },
        "extracted_pages": list(selected_pages),
        "body_size": body_size,
        "source_fonts": list(source_fonts),
        "scanned_pages": list(scanned_pages),
        "warnings": list(warnings),
        "pages": list(pages_info),
        "segment_count": len(segments),
        "settings": {
            "dpi": args.dpi,
            "no_previews": args.no_previews,
            "glossary": args.glossary,
        },
    }


if __name__ == "__main__":
    raise SystemExit(main())

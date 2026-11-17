#!/usr/bin/env python3
"""Render a Chinese rulebook PDF in place and run layout/asset QA."""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
import shutil
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple

import fitz
from PIL import Image, ImageDraw, ImageFont

from pdf_common import (
    DICE_RE,
    GLOSSARY_CSV,
    GlossaryTerm,
    NUMBER_RE,
    BULLET_RE,
    choose_fonts,
    clean_text,
    cjk_ratio,
    eprint,
    is_probably_keep,
    layout_around_obstacles,
    has_cjk,
    latin_ratio,
    list_to_rect,
    load_glossary,
    normalize_ws,
    overlap_area,
    page_drawings,
    page_geometry,
    page_image_infos,
    drawings_summary,
    read_tsv_map,
    rect_area,
    rect_to_list,
    select_render_font,
    setup_stdout,
    write_json,
)

ALIGN_CODES = {"left": 0, "center": 1, "right": 2}
MIN_BODY = 5.5
MIN_TABLE = 5.0
MIN_HEADING = 6.5
WARN_FONT = 7.0

STOPWORDS = {
    "their", "there", "these", "those", "which", "while", "where", "would",
    "could", "should", "about", "after", "before", "during", "under", "over",
    "between", "through", "without", "within", "other", "another", "every",
    "player", "players", "place", "placed", "takes", "take", "draw", "draws",
    "card", "cards", "deck", "turn", "round", "game", "rule", "rules", "using",
    "instead", "immediately", "unless", "cannot", "may", "must", "choose",
    "chosen", "target", "space", "spaces", "action", "actions", "effect",
    "effects", "your", "yours", "from", "with", "that", "this", "have", "has",
    "into", "onto", "when", "then", "than", "them", "they", "will", "each",
}


def read_termbase(path: Path) -> Dict[str, Tuple[str, str]]:
    result: Dict[str, Tuple[str, str]] = {}
    if not path.exists():
        return result
    with path.open("r", encoding="utf-8-sig", errors="replace") as handle:
        for line in handle:
            raw = line.rstrip()
            if not raw.strip() or raw.lstrip().startswith("#"):
                continue
            parts = raw.split("\t")
            if len(parts) < 2:
                continue
            source, zh = parts[0].strip(), parts[1].strip()
            category = parts[2].strip() if len(parts) > 2 else ""
            if source:
                result[source] = (zh, category)
    return result


def term_in_text(term: str, text: str) -> bool:
    if not term:
        return False
    pattern = re.escape(term)
    pattern = pattern.replace(r"\ ", r"[\s\-]+")
    pattern += r"(?:s|es|ed|ing)?"
    return re.search(r"(?<![A-Za-z0-9])" + pattern + r"(?![A-Za-z0-9])",
                     text or "", re.IGNORECASE) is not None


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def source_tokens(text: str) -> List[str]:
    tokens = re.findall(r"[A-Za-z][A-Za-z'\-]{3,}", text or "")
    result = []
    for token in tokens:
        low = token.lower().strip("-'")
        if len(low) < 4 or low in STOPWORDS:
            continue
        if low not in result:
            result.append(low)
    result.sort(key=len, reverse=True)
    return result[:4]


def numeric_tokens(text: str) -> List[str]:
    values = NUMBER_RE.findall(text or "")
    values.extend(DICE_RE.findall(text or ""))
    seen = []
    for value in values:
        if value not in seen:
            seen.append(value)
    return seen


def get_zbox(seg: Dict[str, Any]) -> fitz.Rect:
    return fitz.Rect(seg["bbox"])


def compute_render_box(seg: Dict[str, Any], page_rect: fitz.Rect,
                       other_rects: Sequence[fitz.Rect],
                       image_rects: Sequence[fitz.Rect],
                       icon_rects: Sequence[fitz.Rect],
                       override: Optional[Dict[str, Any]]) -> Tuple[fitz.Rect, List[str]]:
    notes: List[str] = []
    base = fitz.Rect(seg["bbox"])
    align = (override or {}).get("align", seg.get("align", "left"))
    if override and override.get("box"):
        try:
            base = fitz.Rect(override["box"])
        except Exception:
            notes.append("layout override 的 box 无法解析，已忽略。")
    if base.is_empty or base.width < 1 or base.height < 1:
        base = fitz.Rect(seg["bbox"])

    if seg.get("table") and seg.get("cell"):
        cell = fitz.Rect(seg["cell"])
        x0, x1 = cell.x0 + 2.0, cell.x1 - 2.0
        if align == "left":
            x0 = max(base.x0, cell.x0 + 2.0)
        y0 = max(base.y0, cell.y0 + 2.0)
        y1 = cell.y1 - 2.0
        if override and override.get("box"):
            ov = fitz.Rect(override["box"])
            x0 = max(x0, ov.x0)
            x1 = min(x1, ov.x1)
            y0 = max(y0, ov.y0)
            y1 = min(y1, ov.y1)
        if y1 <= y0 + 2:
            y1 = min(page_rect.y1 - 6, y0 + max(8.0, base.height + 4))
            notes.append("表格单元高度过小，已放宽到单元下方，请目检。")
        return fitz.Rect(x0, y0, max(x0 + 6, x1), y1), notes

    x0, x1 = base.x0, base.x1
    y0 = base.y0
    if x1 - x0 < 6:
        x1 = x0 + 6
    if align == "left" and not seg.get("table") and (
            seg.get("inline_art") or seg.get("kind") in ("list", "header_footer") or seg.get("flat")):
        band_top, band_bottom = base.y0, base.y1
        right_limit = page_rect.x1 - 8
        for rect in list(other_rects) + list(image_rects) + list(icon_rects):
            if rect.y1 <= band_top + 1 or rect.y0 >= band_bottom - 1:
                continue
            if rect.x0 >= base.x1 - 1:
                right_limit = min(right_limit, rect.x0 - 4)
        if right_limit > x1 + 6:
            x1 = min(right_limit, base.x1 + max(60.0, base.width * 0.8))
            if seg.get("inline_art"):
                notes.append("为绕开内嵌图标，排版框向右扩展。")
    kind = seg.get("kind", "body")
    if seg.get("table"):
        cap = base.height * 1.8 + 6
    elif kind in ("header_footer",):
        cap = base.height * 0.8 + 5
    elif kind == "heading":
        cap = base.height * 1.6 + 8
    elif seg.get("flat"):
        cap = base.height * 1.4 + 6
    else:
        cap = base.height * 2.8 + 8

    limit = page_rect.y1 - 14
    for rect in list(other_rects) + list(image_rects) + list(icon_rects):
        if rect.x1 <= x0 + 1 or rect.x0 >= x1 - 1:
            continue
        if rect.y0 >= base.y1 - 1:
            limit = min(limit, rect.y0 - 4)
    y1 = min(base.y1 + cap, limit, page_rect.y1 - 14)
    if y1 < base.y1 + 2:
        y1 = min(page_rect.y1 - 14, base.y1 + 2)
        notes.append("下方空间不足，已贴近下方安全边界。")
    if override and override.get("box"):
        ov = fitz.Rect(override["box"])
        x0, y0, x1, y1 = ov.x0, ov.y0, ov.x1, ov.y1
    return fitz.Rect(x0, y0, x1, y1), notes


def try_textwriter(page: fitz.Page, box: fitz.Rect, text: str,
                   font: fitz.Font, fontsize: float, lineheight: float,
                   align: int, color: Sequence[float]) -> Optional[fitz.Rect]:
    writer = fitz.TextWriter(page.rect)
    try:
        leftover = writer.fill_textbox(
            box, text, font=font, fontsize=fontsize, lineheight=lineheight,
            align=align, warn=False,
        )
    except ValueError:
        return None
    except Exception:
        return None
    if leftover:
        return None
    rect = writer.text_rect
    if rect.is_empty:
        return None
    # Built-in CJK fonts can report a large left side bearing; only enforce the
    # bottom/right edges and a generous top tolerance.
    if rect.y1 > box.y1 + 1.5 or rect.x1 > box.x1 + 1.5:
        return None
    if rect.y0 < box.y0 - max(2.0, fontsize * 0.6):
        return None
    try:
        writer.write_text(page, color=color, overlay=True)
    except Exception:
        return None
    return rect


def build_page_obstacles(page: fitz.Page, segs: Sequence[Dict[str, Any]],
                         exclude_id: Optional[str] = None) -> List[fitz.Rect]:
    rects: List[fitz.Rect] = []
    for seg in segs:
        if seg["id"] == exclude_id:
            continue
        rects.append(fitz.Rect(seg["bbox"]))
    return rects


def image_obstacles_for_page(page: fitz.Page, images: Sequence[Dict[str, Any]],
                             page_rect: fitz.Rect) -> Tuple[List[fitz.Rect], List[fitz.Rect]]:
    page_area = max(1.0, rect_area(page_rect))
    all_rects: List[fitz.Rect] = []
    inline_rects: List[fitz.Rect] = []
    for info in images:
        rect = fitz.Rect(info["bbox"])
        if rect.is_empty:
            continue
        all_rects.append(rect)
        if rect_area(rect) <= page_area * 0.5:
            inline_rects.append(rect)
    return all_rects, inline_rects


def icon_obstacles_for_page(page: fitz.Page, seg_size: float) -> List[fitz.Rect]:
    _, icon_candidates = page_drawings(page)
    max_size = max(4.0 * seg_size + 8.0, 22.0)
    result = []
    for rect in icon_candidates:
        if rect.is_empty:
            continue
        if max(rect.width, rect.height) > max_size:
            continue
        if rect.width < 1.5 or rect.height < 1.5:
            continue
        result.append(rect)
    return result


def add_issue(issues: List[Dict[str, Any]], level: str, code: str, message: str,
              page: Optional[int] = None, segment: Optional[str] = None,
              source: str = "", translation: str = "",
              box: Optional[Sequence[float]] = None, **detail: Any) -> None:
    issues.append({
        "level": level,
        "code": code,
        "message": message,
        "page": page,
        "segment": segment,
        "source": (source or "")[:240],
        "translation": (translation or "")[:240],
        "box": list(box) if box else None,
        "detail": detail,
    })


def font_for_preview() -> ImageFont.ImageFont:
    candidates = [
        r"C:\Windows\Fonts\simhei.ttf",
        r"C:\Windows\Fonts\msyh.ttc",
        "/System/Library/Fonts/PingFang.ttc",
        "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc",
    ]
    for path in candidates:
        try:
            if Path(path).exists():
                return ImageFont.truetype(path, 24, index=0)
        except Exception:
            continue
    return ImageFont.load_default()


def draw_issue_boxes(image: Image.Image, page: fitz.Page, issues: Sequence[Dict[str, Any]],
                     offset_x: int, offset_y: int, scale_x: float, scale_y: float,
                     font: ImageFont.ImageFont) -> None:
    draw = ImageDraw.Draw(image)
    for issue in issues:
        box = issue.get("box")
        if not box:
            continue
        try:
            rect = list_to_rect(box)
            if page.rotation:
                rect = rect * page.rotation_matrix
        except Exception:
            continue
        x0 = offset_x + rect.x0 * scale_x
        y0 = offset_y + rect.y0 * scale_y
        x1 = offset_x + rect.x1 * scale_x
        y1 = offset_y + rect.y1 * scale_y
        color = (200, 30, 30) if issue.get("level") == "error" else (220, 140, 20)
        draw.rectangle((x0, y0, x1, y1), outline=color, width=3)
        label = issue.get("segment") or issue.get("code", "")
        if label:
            draw.text((x0 + 3, max(offset_y + 2, y0 - 22)), str(label)[:40],
                      fill=color, font=font)


def make_previews(input_doc: fitz.Document, output_doc: fitz.Document,
                  page_numbers: Sequence[int], dpi: int, qa_dir: Path,
                  issues: Sequence[Dict[str, Any]]) -> List[str]:
    pages_dir = qa_dir / "pages"
    if pages_dir.exists():
        shutil.rmtree(pages_dir)
    pages_dir.mkdir(parents=True, exist_ok=True)
    font = font_for_preview()
    preview_paths: List[str] = []
    for page_no in page_numbers:
        src_page = input_doc.load_page(page_no - 1)
        out_page = output_doc.load_page(page_no - 1)
        src_pix = src_page.get_pixmap(dpi=dpi, alpha=False)
        out_pix = out_page.get_pixmap(dpi=dpi, alpha=False)
        src_img = Image.frombytes("RGB", (src_pix.width, src_pix.height), src_pix.samples)
        out_img = Image.frombytes("RGB", (out_pix.width, out_pix.height), out_pix.samples)
        target_h = max(src_img.height, out_img.height)
        if src_img.height != target_h:
            src_img = src_img.resize((int(src_img.width * target_h / src_img.height), target_h),
                                     Image.LANCZOS)
        if out_img.height != target_h:
            out_img = out_img.resize((int(out_img.width * target_h / out_img.height), target_h),
                                     Image.LANCZOS)
        header = 46
        gap = 18
        canvas = Image.new("RGB", (src_img.width + out_img.width + gap * 2,
                                   target_h + header + gap), (245, 245, 245))
        draw = ImageDraw.Draw(canvas)
        draw.text((gap, 10), f"ORIGINAL / 原文   Page {page_no}", fill=(30, 30, 30), font=font)
        draw.text((gap * 2 + src_img.width, 10),
                  f"TRANSLATED / 译文   Page {page_no}", fill=(30, 30, 30), font=font)
        canvas.paste(src_img, (gap, header))
        canvas.paste(out_img, (gap * 2 + src_img.width, header))
        draw.line((gap + src_img.width + gap // 2, header,
                   gap + src_img.width + gap // 2, header + target_h), fill=(180, 180, 180), width=1)
        page_issues = [issue for issue in issues if issue.get("page") == page_no and issue.get("level") in ("error", "warning")]
        if page_issues:
            scale_x = out_img.width / max(1.0, out_page.rect.width)
            scale_y = out_img.height / max(1.0, out_page.rect.height)
            draw_issue_boxes(canvas, out_page, page_issues,
                             gap * 2 + src_img.width, header, scale_x, scale_y, font)
        path = pages_dir / f"page_{page_no:04d}.png"
        canvas.save(path, optimize=True)
        preview_paths.append(str(path.relative_to(qa_dir)).replace("\\", "/"))
    # Thumbnails contact sheet of translated pages.
    thumbs = []
    for page_no in page_numbers:
        page = output_doc.load_page(page_no - 1)
        pix = page.get_pixmap(dpi=55, alpha=False)
        img = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
        thumbs.append((page_no, img))
    if thumbs:
        thumb_w = 260
        thumb_h = max(1, int(thumbs[0][1].height * thumb_w / max(1, thumbs[0][1].width)))
        cols = 4
        rows = math.ceil(len(thumbs) / cols)
        sheet = Image.new("RGB", (cols * (thumb_w + 16) + 16,
                                  rows * (thumb_h + 36) + 16), (245, 245, 245))
        draw = ImageDraw.Draw(sheet)
        small_font = font
        for idx, (page_no, img) in enumerate(thumbs):
            col = idx % cols
            row = idx // cols
            x = 16 + col * (thumb_w + 16)
            y = 16 + row * (thumb_h + 36)
            resized = img.resize((thumb_w, thumb_h), Image.LANCZOS)
            sheet.paste(resized, (x, y))
            draw.text((x, y + thumb_h + 4), f"Page {page_no}", fill=(30, 30, 30), font=small_font)
        sheet.save(qa_dir / "contact_sheet.png", optimize=True)
    return preview_paths


def main() -> int:
    setup_stdout()
    parser = argparse.ArgumentParser(description="把译文原位写回 PDF，并检查图文是否错位。")
    parser.add_argument("pdf", help="原始 PDF 路径")
    parser.add_argument("-w", "--work", default="work", help="extract.py 生成的工作目录")
    parser.add_argument("-o", "--out", default="out", help="输出目录")
    parser.add_argument("--allow-missing", action="store_true", help="允许部分文字段未翻译（仅预览）")
    parser.add_argument("--dpi", type=int, default=130, help="QA 预览 DPI")
    parser.add_argument("--font", help="中文字体文件（默认自动选择系统字体）")
    parser.add_argument("--bold-font", help="中文粗体文件")
    parser.add_argument("--overrides", help="layout_overrides.json 路径")
    parser.add_argument("--no-previews", action="store_true", help="不生成 QA 预览图")
    args = parser.parse_args()

    pdf_path = Path(args.pdf).resolve()
    work_dir = Path(args.work).resolve()
    out_dir = Path(args.out).resolve()
    segments_path = work_dir / "segments.json"
    manifest_path = work_dir / "manifest.json"
    translations_path = work_dir / "translations.tsv"
    if not pdf_path.exists():
        eprint(f"找不到 PDF：{pdf_path}")
        return 2
    for path in (segments_path, manifest_path, translations_path):
        if not path.exists():
            eprint(f"缺少工作文件：{path}\n请先运行 extract.py。")
            return 2

    segments_data = json.loads(segments_path.read_text(encoding="utf-8"))
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    segments: List[Dict[str, Any]] = segments_data.get("segments", [])
    pages_meta = {int(page["number"]): page for page in segments_data.get("pages", [])}
    page_numbers = [int(p) for p in manifest.get("extracted_pages", [])]
    if not page_numbers:
        page_numbers = sorted(pages_meta)
    seg_by_id = {seg["id"]: seg for seg in segments}
    translations, tsv_problems = read_tsv_map(translations_path)

    issues: List[Dict[str, Any]] = []
    for problem in tsv_problems:
        add_issue(issues, "error", "translations-file", problem)

    unknown = sorted(set(translations) - set(seg_by_id))
    for sid in unknown:
        add_issue(issues, "error", "unknown-id", f"translations.tsv 中的 id 不存在：{sid}")
    if unknown:
        add_issue(issues, "info", "stale-workdir",
                  "如果重新提取后 id 变化，请使用 --reset-translations 重新生成模板，或恢复与当前 segments.json 匹配的译文。")

    expected_hash = manifest.get("pdf_sha256")
    if expected_hash and sha256_file(pdf_path) != expected_hash:
        add_issue(issues, "warning", "pdf-changed",
                  "输入 PDF 与提取时的文件哈希不一致；请确认版式没有变化。")

    overrides_path = Path(args.overrides).resolve() if args.overrides else work_dir / "layout_overrides.json"
    overrides: Dict[str, Dict[str, Any]] = {}
    if overrides_path.exists():
        try:
            overrides = json.loads(overrides_path.read_text(encoding="utf-8"))
            if not isinstance(overrides, dict):
                raise ValueError("顶层必须是对象")
        except Exception as exc:
            add_issue(issues, "warning", "overrides-invalid", f"layout_overrides.json 无法读取：{exc}")
            overrides = {}

    termbase_path = work_dir / "termbase.tsv"
    termbase_raw = read_termbase(termbase_path)
    termbase = {source: zh for source, (zh, category) in termbase_raw.items()
                if source and zh and zh.strip() not in ("-", "")}
    termbase_categories = {source: category for source, (_zh, category) in termbase_raw.items()}
    termbase_lower = {source.lower(): zh for source, zh in termbase.items()}

    glossary = load_glossary(GLOSSARY_CSV)
    glossary_by_en = {term.en.lower(): term for term in glossary}

    # Resolve translations.
    resolved: Dict[str, str] = {}
    keep_ids = set()
    missing_ids = []
    for seg in segments:
        sid = seg["id"]
        value = translations.get(sid, "")
        value = clean_text(value).strip()
        value = re.sub(r"\s+", " ", value)
        if value == "=":
            keep_ids.add(sid)
            continue
        if not value:
            if seg.get("suggest_keep"):
                keep_ids.add(sid)
                add_issue(issues, "info", "auto-keep", "建议保留原文，未填写译文，自动保留。",
                          seg.get("page"), sid, seg.get("text", ""))
            else:
                missing_ids.append(sid)
                add_issue(issues, "warning" if args.allow_missing else "error",
                          "missing-translation",
                          "缺少译文。" + ("（--allow-missing 仅预览）" if args.allow_missing else ""),
                          seg.get("page"), sid, seg.get("text", ""))
            continue
        if value == clean_text(seg.get("text", "")).strip():
            keep_ids.add(sid)
            add_issue(issues, "warning", "same-as-source",
                      "译文与原文完全相同，已按保留原文处理。", seg.get("page"), sid,
                      seg.get("text", ""), value)
            continue
        resolved[sid] = value

    if not resolved and not keep_ids:
        add_issue(issues, "error", "no-translations", "没有任何可用译文。")

    try:
        input_doc = fitz.open(str(pdf_path))
        original_doc = fitz.open(str(pdf_path))
    except Exception as exc:
        eprint(f"无法打开 PDF：{exc}")
        return 2
    if input_doc.needs_pass:
        if not input_doc.authenticate(""):
            eprint("PDF 已加密。")
            return 2
        original_doc.authenticate("")

    before: Dict[int, Dict[str, Any]] = {}
    for page_no in page_numbers:
        page = original_doc.load_page(page_no - 1)
        before[page_no] = {
            "geometry": page_geometry(page),
            "images": page_image_infos(page),
            "drawings": drawings_summary(page),
            "text": page.get_text("text"),
        }

    fonts = choose_fonts(args.font, args.bold_font)
    print(f"中文字体：{fonts.label}")
    out_dir.mkdir(parents=True, exist_ok=True)
    out_pdf = out_dir / f"{pdf_path.stem}_zh.pdf"
    tmp_pdf = out_dir / f".{pdf_path.stem}_zh.tmp.pdf"
    placements: List[Dict[str, Any]] = []

    for page_no in page_numbers:
        page = input_doc.load_page(page_no - 1)
        page_rect = fitz.Rect(page.rect)
        page_segs = [seg for seg in segments if int(seg.get("page", 0)) == page_no]
        if not page_segs:
            continue
        meta = pages_meta.get(page_no, {})
        image_infos = meta.get("images", [])
        all_images, inline_images = image_obstacles_for_page(page, image_infos, page_rect)
        page_icons = icon_obstacles_for_page(page, float(segments_data.get("body_size", 10.0)))

        # 1) Redact only the original glyphs, never images or vector art.
        annotated = False
        for seg in page_segs:
            sid = seg["id"]
            if sid not in resolved:
                continue
            for line_box in seg.get("lines", []):
                rect = fitz.Rect(line_box) & page_rect
                if rect.is_empty:
                    continue
                rect = fitz.Rect(rect.x0 - 0.6, rect.y0 - 0.6, rect.x1 + 0.6, rect.y1 + 0.6) & page_rect
                try:
                    page.add_redact_annot(rect, fill=False)
                    annotated = True
                except Exception:
                    add_issue(issues, "warning", "redact-add-failed",
                              "无法添加文字擦除区域。", page_no, sid, seg.get("text", ""), box=rect_to_list(rect))
        if annotated:
            try:
                ok = page.apply_redactions(images=fitz.PDF_REDACT_IMAGE_NONE,
                                           graphics=fitz.PDF_REDACT_LINE_ART_NONE,
                                           text=0)
                if not ok:
                    add_issue(issues, "warning", "redact-failed", "擦除文字时返回失败。", page_no)
            except Exception as exc:
                add_issue(issues, "error", "redact-failed", f"擦除文字失败：{exc}", page_no)
                continue

        # 2) Place translations.
        for seg in page_segs:
            sid = seg["id"]
            if sid in keep_ids:
                continue
            zh = resolved.get(sid)
            if not zh:
                continue
            override = overrides.get(sid, {}) if isinstance(overrides, dict) else {}
            other_rects = build_page_obstacles(page, page_segs, exclude_id=sid)
            icon_rects = icon_obstacles_for_page(page, float(seg.get("font_size", 10.0)))
            box, box_notes = compute_render_box(
                seg, page_rect, other_rects, all_images, icon_rects, override
            )
            if not page_rect.contains(box):
                clipped = box & page_rect
                add_issue(issues, "warning", "box-outside-page",
                          "渲染框超出页面，已裁剪。", page_no, sid, seg.get("text", ""), zh,
                          box=rect_to_list(box), notes=box_notes)
                box = clipped
            align = (override or {}).get("align", seg.get("align", "left"))
            if align not in ALIGN_CODES:
                align = "left"
            align_code = ALIGN_CODES[align]
            bold = bool(seg.get("bold")) and not bool((override or {}).get("regular"))
            color = tuple(float(v) for v in seg.get("color", [0, 0, 0]))
            font, used_bold, missing_glyphs, used_builtin = select_render_font(fonts, zh, bold)
            if missing_glyphs:
                add_issue(issues, "error", "missing-glyphs",
                          f"字体缺少字符：{''.join(missing_glyphs[:12])}", page_no, sid,
                          seg.get("text", ""), zh, missing=missing_glyphs[:30])
            if used_builtin and fonts.regular_path is not None:
                add_issue(issues, "info", "fallback-font",
                          "译文含系统字体不支持的字符，已改用内置 CJK 字体。", page_no, sid,
                          seg.get("text", ""), zh)
            insert_name, insert_path = fonts.insert_spec(used_bold)
            if used_builtin:
                insert_name, insert_path = "china-s", None

            lineheight = 1.18 if seg.get("table") else (
                1.12 if seg.get("kind") == "list" else
                (1.16 if seg.get("kind") == "heading" else 1.22))
            start_size = float((override or {}).get("font_size") or seg.get("font_size") or 9.0)
            min_size = MIN_TABLE if seg.get("table") else (
                MIN_HEADING if seg.get("kind") == "heading" else MIN_BODY)
            if seg.get("kind") in ("header_footer", "caption"):
                min_size = 4.8
            start_size = max(min_size, min(72.0, start_size))
            sizes = []
            size = start_size
            while size >= min_size - 0.01:
                sizes.append(round(size, 2))
                size -= 0.25
            if not sizes:
                sizes = [start_size]

            drawn_rect: Optional[fitz.Rect] = None
            used_size = start_size
            overflow = False
            actual_lines: List[fitz.Rect] = []
            mode = "inline" if seg.get("inline_art") else "textbox"
            obstacles = [fitz.Rect(item) for item in seg.get("obstacles", [])]
            for size in sizes:
                if mode == "inline":
                    rects = layout_around_obstacles(
                        page, box, zh, font, size, lineheight, align_code, color,
                        obstacles, insert_name, insert_path,
                    )
                    if rects is not None and rects:
                        drawn_rect = rects[0] | rects[-1] if len(rects) > 1 else rects[0]
                        for r in rects[1:]:
                            drawn_rect |= r
                        actual_lines = rects
                        used_size = size
                        break
                else:
                    result = try_textwriter(page, box, zh, font, size, lineheight, align_code, color)
                    if result is not None:
                        drawn_rect = result
                        actual_lines = [result]
                        used_size = size
                        break
            if drawn_rect is None:
                # Never clip silently: draw with the minimum size in a tall box,
                # then let QA flag the overflow/overlap for the agent to fix.
                overflow = True
                tall = fitz.Rect(box.x0, box.y0, box.x1, page_rect.y1 - 10)
                rects = layout_around_obstacles(
                    page, tall, zh, font, min_size, lineheight, align_code, color,
                    obstacles, insert_name, insert_path,
                )
                used_size = min_size
                if rects:
                    drawn_rect = rects[0] | rects[-1] if len(rects) > 1 else rects[0]
                    for r in rects[1:]:
                        drawn_rect |= r
                    actual_lines = rects
                else:
                    add_issue(issues, "error", "render-failed",
                              "无法写入译文（字体或布局错误）。", page_no, sid,
                              seg.get("text", ""), zh, box=rect_to_list(box))
                    continue

            if overflow:
                add_issue(issues, "error", "overflow",
                          "译文在最小字号下仍放不下，已强制写出；请改写译文或调整 layout_overrides。",
                          page_no, sid, seg.get("text", ""), zh, box=rect_to_list(box))
            if used_size < WARN_FONT:
                add_issue(issues, "warning", "small-font",
                          f"译文自动缩到 {used_size:.1f}pt，可能影响阅读。", page_no, sid,
                          seg.get("text", ""), zh, box=rect_to_list(drawn_rect), size=used_size)
            if used_size < float(seg.get("font_size", used_size)) * 0.7:
                add_issue(issues, "warning", "font-shrunk",
                          f"字号从 {seg.get('font_size')}pt 缩到 {used_size:.1f}pt；建议精简译文。",
                          page_no, sid, seg.get("text", ""), zh, box=rect_to_list(drawn_rect))

            placements.append({
                "id": sid,
                "page": page_no,
                "kind": seg.get("kind"),
                "source": seg.get("text", ""),
                "zh": zh,
                "box": rect_to_list(box),
                "actual": rect_to_list(drawn_rect),
                "lines": [rect_to_list(r) for r in actual_lines],
                "font_size": used_size,
                "bold": used_bold,
                "builtin_font": used_builtin,
                "overflow": overflow,
                "mode": mode,
                "table": bool(seg.get("table")),
                "cell": seg.get("cell"),
            })

        # Table-cell bounds and art overlap checks are done after placements.

    try:
        input_doc.set_metadata({
            **(input_doc.metadata or {}),
            "title": ((input_doc.metadata or {}).get("title") or pdf_path.stem) + "（中文）",
        })
    except Exception:
        pass
    try:
        input_doc.subset_fonts()
    except Exception:
        pass
    try:
        input_doc.save(str(tmp_pdf), garbage=4, deflate=True)
    except Exception as exc:
        add_issue(issues, "error", "save-failed", f"保存 PDF 失败：{exc}")
        eprint(f"保存失败：{exc}")
        return 2
    try:
        if out_pdf.exists():
            out_pdf.unlink()
        tmp_pdf.replace(out_pdf)
    except Exception as exc:
        add_issue(issues, "error", "save-failed", f"替换输出文件失败：{exc}")
        eprint(f"替换输出文件失败：{exc}")
        return 2

    try:
        output_doc = fitz.open(str(out_pdf))
    except Exception as exc:
        eprint(f"无法打开输出 PDF：{exc}")
        return 2

    # ---------- QA ----------
    if output_doc.page_count != input_doc.page_count:
        add_issue(issues, "error", "page-count",
                  f"页数变化：{input_doc.page_count} → {output_doc.page_count}")

    placements_by_page: Dict[int, List[Dict[str, Any]]] = defaultdict(list)
    for item in placements:
        placements_by_page[int(item["page"])].append(item)

    for page_no in page_numbers:
        src_page = input_doc.load_page(page_no - 1)
        out_page = output_doc.load_page(page_no - 1)
        before_info = before[page_no]
        after_geom = page_geometry(out_page)
        if after_geom != before_info["geometry"]:
            add_issue(issues, "error", "geometry-changed",
                      "页面尺寸或旋转发生变化。", page_no,
                      before=before_info["geometry"], after=after_geom)
        after_images = page_image_infos(out_page)
        if after_images != before_info["images"]:
            add_issue(issues, "error", "images-changed",
                      "位图数量、内容摘要或位置发生变化（插图可能被移动/覆盖）。", page_no,
                      before=before_info["images"], after=after_images)
        after_drawings = drawings_summary(out_page)
        if after_drawings != before_info["drawings"]:
            add_issue(issues, "error", "vector-art-changed",
                      "矢量图摘要发生变化（线条/图标可能被移动或删除）。", page_no,
                      before=before_info["drawings"], after=after_drawings)

        meta = pages_meta.get(page_no, {})
        image_infos = meta.get("images", [])
        all_images, _inline_images = image_obstacles_for_page(out_page, image_infos,
                                                              fitz.Rect(out_page.rect))
        out_text = out_page.get_text("text")
        out_norm = normalize_ws(out_text)
        page_issues = [issue for issue in issues if issue.get("page") == page_no and issue.get("level") in ("error", "warning")]
        page_segs = [seg for seg in segments if int(seg.get("page", 0)) == page_no]

        for seg in page_segs:
            sid = seg["id"]
            zh = resolved.get(sid)
            if not zh:
                continue
            source = seg.get("text", "")
            zh_norm = normalize_ws(zh)
            if len(zh_norm) > 2 and zh_norm not in out_norm:
                head = zh_norm[:6]
                tail = zh_norm[-6:]
                if not (head and head in out_norm and tail and tail in out_norm):
                    add_issue(issues, "error", "text-not-found",
                              "输出页中找不到完整译文（字体/编码/裁剪异常）。", page_no, sid,
                              source, zh, box=seg.get("bbox"))
            elif len(zh_norm) <= 2 and zh_norm and zh_norm not in out_norm:
                add_issue(issues, "error", "text-not-found",
                          "输出页中找不到译文。", page_no, sid, source, zh, box=seg.get("bbox"))

            # Original text residue in the segment box.
            bbox = fitz.Rect(seg.get("bbox", (0, 0, 0, 0)))
            try:
                remaining = out_page.get_textbox(bbox)
            except Exception:
                remaining = ""
            if remaining and remaining.strip():
                remain_low = remaining.lower()
                zh_low = zh.lower()
                for token in source_tokens(source):
                    if token in zh_low:
                        continue
                    if re.search(r"(?<![A-Za-z])" + re.escape(token) + r"(?![A-Za-z])", remain_low):
                        add_issue(issues, "error", "source-residue",
                                  f"原英文仍残留（或擦除不完整）：{token}", page_no, sid,
                                  source, zh, box=seg.get("bbox"), residue=remaining[:200])
                        break

            for number in numeric_tokens(source):
                if number not in zh:
                    add_issue(issues, "warning", "number-missing",
                              f"原文数字 {number} 未出现在译文中，请核对。", page_no, sid,
                              source, zh, box=seg.get("bbox"))

            if len(source) >= 12:
                ratio = len(zh) / max(1, len(source))
                if ratio > 1.6:
                    add_issue(issues, "warning", "length-ratio",
                              f"译文长度约为原文的 {ratio:.1f} 倍，可能过长。", page_no, sid,
                              source, zh, box=seg.get("bbox"))
                elif ratio < 0.12:
                    add_issue(issues, "warning", "length-ratio",
                              f"译文很短（原文的 {ratio:.1f} 倍），请检查是否漏译。", page_no, sid,
                              source, zh, box=seg.get("bbox"))
            if latin_ratio(zh) > 0.65 and len(zh) > 12:
                add_issue(issues, "warning", "mostly-latin",
                          "译文含大量英文字符，请确认是否漏译或专有名词过多。", page_no, sid,
                          source, zh, box=seg.get("bbox"))

            # Glossary banned/avoid variants for this segment.
            for hit in seg.get("glossary", []):
                term = glossary_by_en.get(str(hit.get("en", "")).lower())
                if term is None:
                    continue
                explicit_zh = termbase_lower.get(term.en.lower(), "")
                explicit_variants = [v.strip() for v in explicit_zh.split("/") if v.strip()]
                for wrong in term.variants(term.wrong):
                    if wrong and wrong in zh:
                        # A termbase row may explicitly choose a regional/contextual
                        # variant (e.g. deck -> 甲板 in a ship game). Only then allow it.
                        if any(wrong in variant for variant in explicit_variants):
                            continue
                        add_issue(issues, "error", "glossary-wrong",
                                  f"术语“{term.en}”误译：{wrong}；建议 {term.zh}。", page_no, sid,
                                  source, zh, box=seg.get("bbox"))
                        break
                for avoid in term.variants(term.avoid):
                    if avoid and avoid in zh:
                        if any(avoid in variant for variant in explicit_variants):
                            continue
                        add_issue(issues, "warning", "glossary-avoid",
                                  f"术语“{term.en}”非推荐译法：{avoid}；建议 {term.zh}。", page_no, sid,
                                  source, zh, box=seg.get("bbox"))
                        break

            # Explicit termbase consistency.
            for term_source, term_zh in termbase.items():
                category = termbase_categories.get(term_source, "")
                multiword = bool(re.search(r"[\s\-]", term_source))
                # Generic verbs / rulebook labels naturally vary; only enforce
                # them when they are multi-word. Core components and names stay strict.
                if term_source.lower() in {
                    "deal", "draw", "place", "play", "gain", "take", "spend", "pay",
                    "discard", "reveal", "shuffle", "resolve", "score", "move",
                    "choose", "remove", "return", "put", "flip", "roll", "reroll",
                    "activate", "trigger", "exhaust", "tap", "untap", "ready",
                    "refresh", "points", "setup",
                } and not multiword:
                    continue
                if category in ("流程与行动", "规则书结构", "计分与胜负") and not multiword:
                    continue
                if term_in_text(term_source, seg.get("text", "")):
                    variants = [v.strip() for v in term_zh.split("/") if v.strip()]
                    if variants and not any(v in zh for v in variants):
                        add_issue(issues, "info", "termbase-mismatch",
                                  f"项目术语库要求 “{term_source}” → {term_zh}，译文中未出现。",
                                  page_no, sid, source, zh, box=seg.get("bbox"))
                        break

        bad_start = set("，。、；：！？）》」』】”’")
        seen_bad = set()
        for line in out_page.get_text("text").splitlines():
            stripped = line.strip().replace("⁠", "")
            if stripped and stripped[0] in bad_start and has_cjk(stripped) and stripped not in seen_bad:
                seen_bad.add(stripped)
                add_issue(issues, "warning", "line-start-punctuation",
                          f"中文标点出现在行首：{stripped[:60]}", page_no,
                          source="", translation=stripped[:120])

        # Placement overlap / bounds / art overlap.
        page_placements = placements_by_page.get(page_no, [])
        for item in page_placements:
            actual = list_to_rect(item["actual"])
            size = float(item.get("font_size", 10))
            if not out_page.rect.contains(fitz.Rect(actual.x0 - 1, actual.y0 - 1, actual.x1 + 1, actual.y1 + 1)):
                add_issue(issues, "error", "placement-outside-page",
                          "译文写入位置超出页面。", page_no, item["id"],
                          item.get("source", ""), item.get("zh", ""), box=item["actual"])
            if item.get("table") and item.get("cell"):
                cell = fitz.Rect(item["cell"])
                if not cell.contains(fitz.Rect(actual.x0 - 1.5, actual.y0 - 1.5, actual.x1 + 1.5, actual.y1 + 1.5)):
                    add_issue(issues, "error", "table-cell-overflow",
                              "译文超出表格单元边界。", page_no, item["id"],
                              item.get("source", ""), item.get("zh", ""), box=item["actual"])
            # Small inline images/vector icons must not be covered.
            for rect in all_images:
                pa = rect_area(rect)
                if pa > rect_area(out_page.rect) * 0.5:
                    continue
                if max(rect.width, rect.height) > max(4.0 * size + 8.0, 22.0):
                    continue
                if overlap_area(actual, rect) > 1.0:
                    add_issue(issues, "error", "art-covered",
                              "译文覆盖了内嵌图片/图标。", page_no, item["id"],
                              item.get("source", ""), item.get("zh", ""),
                              box=item["actual"], art=rect_to_list(rect))
                    break
            # Vector icons.
            for rect in icon_obstacles_for_page(out_page, size):
                if overlap_area(actual, rect) > 1.0:
                    add_issue(issues, "error", "vector-covered",
                              "译文覆盖了矢量图标。", page_no, item["id"],
                              item.get("source", ""), item.get("zh", ""),
                              box=item["actual"], art=rect_to_list(rect))
                    break

        # Do not expand into kept/untranslated/other text.
        for item in page_placements:
            actual = list_to_rect(item["actual"])
            for other in page_segs:
                if other["id"] == item["id"]:
                    continue
                other_rect = fitz.Rect(other["bbox"])
                ov = overlap_area(actual, other_rect)
                min_area = min(rect_area(actual), rect_area(other_rect))
                if ov > max(8.0, 0.25 * min_area):
                    add_issue(issues, "error", "text-overlap-source",
                              "译文压到了保留/未翻译的原文区域。", page_no, item["id"],
                              item.get("source", ""), item.get("zh", ""),
                              box=item["actual"], other=other["id"])
                    break

        for i in range(len(page_placements)):
            a = page_placements[i]
            ra = list_to_rect(a["actual"])
            for j in range(i + 1, len(page_placements)):
                b = page_placements[j]
                rb = list_to_rect(b["actual"])
                ov = overlap_area(ra, rb)
                min_area = min(rect_area(ra), rect_area(rb))
                if ov > max(8.0, 0.25 * min_area):
                    add_issue(issues, "error", "text-overlap",
                              f"两段译文互相重叠：{a['id']} / {b['id']}", page_no, a["id"],
                              a.get("source", ""), a.get("zh", ""), box=a["actual"],
                              other=b["id"])
                    break

        if page_placements:
            out_fonts = out_page.get_fonts(full=True)
            has_cjk_font = any(len(f) >= 7 and f[2] == "Type0" for f in out_fonts)
            if not has_cjk_font:
                add_issue(issues, "warning", "font-not-embedded",
                          "未检测到 Type0 中文字体，请确认输出文字可选中且字体已嵌入。", page_no)

        if meta.get("scanned"):
            add_issue(issues, "warning", "scanned-page",
                      "该页疑似扫描页/无文字层，未覆盖汉化。", page_no)

    if args.no_previews:
        add_issue(issues, "warning", "no-previews", "本次未生成 QA 预览图，无法完成目检。")

    # Summary counts.
    errors = [issue for issue in issues if issue["level"] == "error"]
    warnings = [issue for issue in issues if issue["level"] == "warning"]
    infos = [issue for issue in issues if issue["level"] == "info"]
    translated_count = len(resolved)
    kept_count = len(keep_ids)
    summary = {
        "pages": len(page_numbers),
        "segments": len(segments),
        "translated": translated_count,
        "kept": kept_count,
        "missing": len(missing_ids),
        "errors": len(errors),
        "warnings": len(warnings),
        "infos": len(infos),
        "fonts": fonts.label,
        "output_pdf": str(out_pdf),
        "image_integrity": all(i["code"] != "images-changed" for i in issues),
        "vector_integrity": all(i["code"] != "vector-art-changed" for i in issues),
        "geometry_integrity": all(i["code"] != "geometry-changed" for i in issues),
    }

    qa_dir = out_dir / "qa"
    if qa_dir.exists():
        shutil.rmtree(qa_dir)
    qa_dir.mkdir(parents=True, exist_ok=True)
    preview_paths = []
    if not args.no_previews:
        preview_paths = make_previews(original_doc, output_doc, page_numbers, args.dpi, qa_dir, issues)

    report = {
        "version": "1.0.0",
        "summary": summary,
        "font": fonts.label,
        "pdf": str(pdf_path),
        "output_pdf": str(out_pdf),
        "previews": preview_paths,
        "issues": issues,
        "placements": placements,
        "pages": [
            {
                "number": page_no,
                "geometry_before": before[page_no]["geometry"],
                "images_before": before[page_no]["images"],
                "drawings_before": before[page_no]["drawings"],
                "placements": len(placements_by_page.get(page_no, [])),
            }
            for page_no in page_numbers
        ],
    }
    write_json(qa_dir / "report.json", report)
    write_report_md(qa_dir / "report.md", report, segments)
    print(f"输出 PDF：{out_pdf}")
    print(f"翻译 {translated_count} 段，保留原文 {kept_count} 段，缺失 {len(missing_ids)} 段。")
    print(f"错误 {len(errors)}，警告 {len(warnings)}。")
    if preview_paths:
        print(f"QA 预览：{qa_dir / 'pages'}（请逐页目检）；报告：{qa_dir / 'report.md'}")
    if errors:
        print("未通过结构校验：请修复 report.md 中的错误后重跑。")
        return 1
    print("结构校验通过；请继续目检预览图，确认插图与文字位置。")
    return 0


def write_report_md(path: Path, report: Dict[str, Any], segments: Sequence[Dict[str, Any]]) -> None:
    summary = report["summary"]
    issues = report["issues"]
    errors = [i for i in issues if i["level"] == "error"]
    warnings = [i for i in issues if i["level"] == "warning"]
    infos = [i for i in issues if i["level"] == "info"]
    by_page: Dict[int, List[Dict[str, Any]]] = defaultdict(list)
    for issue in issues:
        if issue.get("page"):
            by_page[int(issue["page"])].append(issue)

    lines = [
        "# 桌游规则书汉化 QA 报告",
        "",
        f"- 输出：`{report['output_pdf']}`",
        f"- 中文字体：{report.get('font', '')}",
        f"- 页数：{summary['pages']}；文字段：{summary['segments']}；已翻译：{summary['translated']}；"
        f"保留原文：{summary['kept']}；缺失：{summary['missing']}",
        "",
        "## 结论",
        "",
        ("**结构校验通过。** 仍需逐页目检 `qa/pages/`，确认插图、表格和文字的相对位置。"
         if not errors else "**未通过结构校验。** 必须先修复下列错误，再重新渲染。"),
        "",
        "| 检查项 | 结果 |",
        "| --- | --- |",
        f"| 位图完整性 | {'通过' if summary['image_integrity'] else '失败'} |",
        f"| 矢量图完整性 | {'通过' if summary['vector_integrity'] else '失败'} |",
        f"| 页面尺寸/旋转 | {'通过' if summary['geometry_integrity'] else '失败'} |",
        f"| 错误 / 警告 / 提示 | {summary['errors']} / {summary['warnings']} / {summary['infos']} |",
        "",
        "## 错误（必须修复）",
        "",
    ]
    if not errors:
        lines.append("无。")
        lines.append("")
    for issue in errors[:120]:
        lines.extend(format_issue(issue))
    if len(errors) > 120:
        lines.append(f"……另有 {len(errors) - 120} 条错误，见 report.json。")
        lines.append("")
    lines.append("## 警告（建议复核）")
    lines.append("")
    if not warnings:
        lines.append("无。")
        lines.append("")
    for issue in warnings[:120]:
        lines.extend(format_issue(issue))
    if len(warnings) > 120:
        lines.append(f"……另有 {len(warnings) - 120} 条警告，见 report.json。")
        lines.append("")
    lines.append("## 逐页预览")
    lines.append("")
    previews = report.get("previews", [])
    if previews:
        for preview in previews:
            page_name = Path(preview).stem.replace("page_", "")
            lines.append(f"- [第 {int(page_name)} 页]({preview})")
    else:
        lines.append("未生成预览。")
    lines.append("")
    lines.append("## 目检清单")
    lines.append("")
    lines += [
        "- [ ] 每一页的插图、棋盘、卡牌、图标位置与原版一致，没有被译文覆盖。",
        "- [ ] 表格边框完整，单元格文字没有越界。",
        "- [ ] 标题、图注与图片对齐，没有掉到页边或另一栏。",
        "- [ ] 卡牌名、角色名、资源名前后一致（对照 termbase.tsv）。",
        "- [ ] 数字、骰子记号、编号与图标保留。",
        "- [ ] 没有残留英文段落（保留原文的页眉/URL 除外）。",
        "",
        "## 提示",
        "",
    ]
    for issue in infos[:30]:
        lines.extend(format_issue(issue))
    if not infos:
        lines.append("无。")
    lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def format_issue(issue: Dict[str, Any]) -> List[str]:
    page = issue.get("page")
    seg = issue.get("segment")
    prefix = f"- **第 {page} 页**" if page else "- "
    if seg:
        prefix += f" · `{seg}`"
    lines = [prefix + f" · `{issue.get('code')}`：{issue.get('message')}"]
    source = issue.get("source") or ""
    translation = issue.get("translation") or ""
    if source:
        lines.append(f"  - 原文：{source[:180]}")
    if translation:
        lines.append(f"  - 译文：{translation[:180]}")
    box = issue.get("box")
    if box:
        lines.append(f"  - bbox：({box[0]:.1f}, {box[1]:.1f}, {box[2]:.1f}, {box[3]:.1f})")
    return lines + [""]


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""v3.0.0 零依赖直翻（direct mode）：宿主模型翻译，本工具只做 PDF 手术。

三步工作流（免引擎、免端点、免 key，全程离线）：
  extract: 体检分级（仅 A 级放行；B 级需 --force-b 显式；C 级拒绝并指引 OCR 通路）
           → 行级文本抽取（bbox/字号/基线）到 JSON；
  （用户/agent 把 JSON 中每条 text 译为 translated——条数守恒、可留空保原文）
  apply:   校验 JSON 与源 PDF（sha256）→ 逐页 redaction 去除原文行（保图保矢量）
           → 行框回填译文（字号自适应 + CJK 字体规则）→ 纯译文 PDF；--dual 左右对照。

安全边界（宪章级）：
  - redaction 只允许作用于 A 级（无图层重复）文档——v2.x 已证伪 B 级重叠字形下
    的 redaction（删一毁二），B 级必须显式 --force-b 且自担风险，C 级硬拒绝；
  - apply_redactions 显式保留图像与矢量图形（版本常量缺失时降级探测）；
  - 不联网：extract/apply 不发起任何网络请求，翻译由用户/宿主模型自行完成。
"""

from __future__ import annotations

import hashlib
import json
import os
import shutil

import pymupdf

LINE_INSET_PT = 0.4          # redaction 矩形内缩，防吃相邻行的升降部
MIN_FONTSIZE = 4.0


class DirectModeError(RuntimeError):
    """direct 模式约束违反（带用户可操作的修复指引）。"""


def sha256_of(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def _redact_keep_assets_kwargs():
    """apply_redactions 的保资产参数：按版本探测（老版本无该常量则退回默认）。"""
    kw = {}
    images_none = getattr(pymupdf, "PDF_REDACT_IMAGE_NONE", None)
    if images_none is not None:
        kw["images"] = images_none
    graphics_none = getattr(pymupdf, "PDF_REDACT_LINE_ART_NONE", None)
    if graphics_none is not None:
        kw["graphics"] = graphics_none
    return kw


def _parse_pages(pages_spec, page_count):
    if not pages_spec:
        return None
    from .pdf_tools import _parse_range
    return set(_parse_range(pages_spec, page_count))


def extract_lines(pdf_path: str, *, pages_spec: str = None,
                  force_b: bool = False, lang_out: str = "zh") -> dict:
    """行级抽取：体检分级 → 逐行 {id,bbox,origin,size,text} → JSON 友好 dict。

    抛 DirectModeError 表示拒绝（加密/C 级/B 级未显式放行），消息带修复指引。
    """
    from .glossary_seed import needs_decrypt
    from . import triage as triage_mod

    if needs_decrypt(pdf_path):
        raise DirectModeError(
            "PDF 已加密。direct 模式不处理加密文件：请先用 translate --password "
            "（自动 qpdf 解密）或手动 qpdf --decrypt 后重试。")

    rep = triage_mod.triage_pdf(pdf_path)
    tier = rep.tier
    if tier == "C":
        raise DirectModeError(
            "体检分级为 C（扫描件/无有效文本层）——direct 模式按 A 级标准做文本层"
            "手术，C 级没有可 redact 的原生文本。请走 OCR 通路：translate --ocr auto"
            "（产物为预览质量）。")
    if tier == "B" and not force_b:
        raise DirectModeError(
            "体检分级为 B（文本层有噪：图层重复/水印/伪影）。redaction 在重叠字形下"
            "会删一毁二（v2.x 实测证伪），direct 模式默认拒绝 B 级。确认要继续："
            "--force-b 显式放行（后果自担）；更稳妥：走引擎通路 translate。")

    doc = pymupdf.open(pdf_path)
    keep = _parse_pages(pages_spec, doc.page_count)
    pages, rotation_skipped, lid = [], [], 0
    for i in range(doc.page_count):
        page = doc[i]
        info = {"number": i + 1, "width": round(page.rect.width, 2),
                "height": round(page.rect.height, 2), "lines": []}
        if keep is not None and (i + 1) not in keep:
            info["excluded"] = True
            pages.append(info)
            continue
        if page.rotation != 0:
            info["rotation_skipped"] = True
            rotation_skipped.append(i + 1)
            pages.append(info)
            continue
        d = page.get_text("dict")
        for block in d.get("blocks", []):
            if block.get("type") != 0:
                continue
            for line in block.get("lines", []):
                spans = line.get("spans") or []
                text = "".join(s.get("text", "") for s in spans)
                if not text.strip():
                    continue
                origin = spans[0].get("origin") or [line["bbox"][0], line["bbox"][3]]
                size = max((float(s.get("size", 10.0)) for s in spans), default=10.0)
                info["lines"].append({
                    "id": "p%03d-l%04d" % (i + 1, len(info["lines"])),
                    "bbox": [round(v, 2) for v in line["bbox"]],
                    "origin": [round(float(origin[0]), 2), round(float(origin[1]), 2)],
                    "size": round(size, 2),
                    "text": text,
                })
                lid += 1
        pages.append(info)
    doc.close()
    return {"format": "doc-holmes-direct/1", "mode": "direct", "tier": tier,
            "lang_out": lang_out, "pages_total": len(pages),
            "source_pdf": os.path.abspath(pdf_path), "source_sha256": sha256_of(pdf_path),
            "rotation_skipped_pages": rotation_skipped,
            "notice": ("把每条 line 的 text 翻译后写入同条 translated（字符串）；"
                       "留空/缺省=该行保留原文。翻完交给：doc-holmes apply 本JSON -o 输出目录"),
            "pages": pages}


def _inset(rect):
    x0, y0, x1, y1 = rect
    return (x0 + LINE_INSET_PT, y0 + LINE_INSET_PT,
            x1 - LINE_INSET_PT, y1 - LINE_INSET_PT)


def apply_translation(doc_json: dict, outdir: str, *, dual: bool = False,
                      out_stem: str = None, pdf_override: str = None) -> dict:
    """译文回填：redaction 去原文行（保图保矢量）→ 行框回填译文 → 纯译文/双拼 PDF。

    校验失败抛 DirectModeError；返回审计 dict。全程离线。
    """
    if doc_json.get("format") != "doc-holmes-direct/1":
        raise DirectModeError("JSON 格式不符（需要 doc-holmes-direct/1，由 extract 生成）")
    pdf_path = pdf_override or doc_json.get("source_pdf")
    if not pdf_path or not os.path.isfile(pdf_path):
        raise DirectModeError(
            "源 PDF 不存在：%s（文件被移动时用 apply --pdf <路径> 指定）" % pdf_path)
    digest = sha256_of(pdf_path)
    if digest != doc_json.get("source_sha256"):
        raise DirectModeError(
            "源 PDF 内容与抽取时不一致（sha256 不符）——请对原文件重跑 extract，"
            "避免把译文回填进已变化的文档。")

    lang_out = doc_json.get("lang_out") or "zh"
    stem = out_stem or os.path.splitext(os.path.basename(pdf_path))[0]
    os.makedirs(outdir, exist_ok=True)
    work = os.path.join(outdir, os.path.basename(pdf_path))
    if os.path.realpath(work) == os.path.realpath(pdf_path):
        # -o 指到源目录时换工作名，防 SameFileError 且不动源文件
        work = os.path.join(outdir, stem + ".direct_work.pdf")
    shutil.copyfile(pdf_path, work)

    lines_total = lines_translated = lines_kept = 0
    lines_insert_failed = lines_overflow = 0
    rot_skipped = set(doc_json.get("rotation_skipped_pages") or [])
    pages_by_no = {}
    for page_info in doc_json.get("pages", []):
        pages_by_no[page_info["number"] - 1] = page_info
    doc = pymupdf.open(work)
    try:
        redact_kw = _redact_keep_assets_kwargs()
        # 遍一：redaction 标注（自行登记有标注的页，兼容无 getter 的版本）
        annotated = set()
        for pno, page_info in pages_by_no.items():
            if pno >= doc.page_count or page_info.get("rotation_skipped"):
                continue
            page = doc[pno]
            for line in page_info.get("lines", []):
                lines_total += 1
                translated = line.get("translated")
                if not isinstance(translated, str) or not translated.strip():
                    lines_kept += 1
                    continue
                x0, y0, x1, y1 = _inset(line["bbox"])
                if x1 - x0 <= 1 or y1 - y0 <= 1:
                    lines_kept += 1
                    continue
                page.add_redact_annot(pymupdf.Rect(x0, y0, x1, y1))
                annotated.add(pno)
        # 遍二：redaction 执行（每页一次）
        for pno in sorted(annotated):
            page = doc[pno]
            if redact_kw:
                try:
                    page.apply_redactions(**redact_kw)
                except TypeError:          # 老版本不认 graphics/images 形参
                    page.apply_redactions()
            else:
                page.apply_redactions()
        # 遍三：译文回填（必须逐页取各自 page_info——滞留变量曾致多页错位，评审 P0 实录）
        for pno in sorted(pages_by_no):
            page_info = pages_by_no[pno]
            if pno >= doc.page_count or page_info.get("rotation_skipped"):
                continue
            page = doc[pno]
            for line in page_info.get("lines", []):
                translated = line.get("translated")
                if not isinstance(translated, str) or not translated.strip():
                    continue
                ox, oy = line["origin"]
                size = float(line.get("size") or 10.0)
                x0, _y0, x1, _y1 = line["bbox"]
                fname = "helv" if all(ord(c) < 256 for c in translated) else "china-s"
                fs = size
                try:
                    need = pymupdf.get_text_length(translated, fontname=fname,
                                                   fontsize=size)
                    avail = max(x1 - x0, 1.0)
                    if need > avail:
                        fs = max(MIN_FONTSIZE, size * avail / need)
                        if fs <= MIN_FONTSIZE + 1e-9 and need > avail * 1.05:
                            lines_overflow += 1   # 触底仍放不下：横向溢出（审计明示）
                except Exception:
                    pass                  # 测宽失败按原字号插入（CJK 译文通常更短）
                try:
                    page.insert_text(pymupdf.Point(ox, oy), translated,
                                     fontsize=fs, fontname=fname)
                    lines_translated += 1
                except Exception:
                    lines_insert_failed += 1
        mono_path = os.path.join(outdir, "%s.%s.direct.pdf" % (stem, lang_out))
        doc.save(mono_path, garbage=3, deflate=True)
    finally:
        doc.close()
        if os.path.isfile(work):
            try:
                os.remove(work)
            except OSError:
                pass

    dual_path = None
    if dual:
        dual_path = _build_dual(pdf_path, mono_path, outdir, stem, lang_out)

    return {"mode": "direct", "tier": doc_json.get("tier"),
            "pages": doc_json.get("pages_total"),
            "lines_total": lines_total, "lines_translated": lines_translated,
            "lines_kept_original": lines_kept,
            "lines_insert_failed": lines_insert_failed,
            "lines_overflow": lines_overflow,
            "rotation_skipped_pages": sorted(rot_skipped),
            "source_sha256": digest, "mono_path": mono_path,
            "dual_path": dual_path}


def _build_dual(pdf_path: str, mono_path: str, outdir: str, stem: str,
                lang_out: str) -> str:
    """左右对照版式：左原页右译页（同源页等高，中缝分隔线）。"""
    src = pymupdf.open(pdf_path)
    tra = pymupdf.open(mono_path)
    dual = pymupdf.open()
    try:
        n = min(src.page_count, tra.page_count)
        for i in range(n):
            w = src[i].rect.width
            h = src[i].rect.height
            page = dual.new_page(width=2 * w, height=h)
            page.show_pdf_page(pymupdf.Rect(0, 0, w, h), src, i)
            page.show_pdf_page(pymupdf.Rect(w, 0, 2 * w, h), tra, i)
            page.draw_line(pymupdf.Point(w, 0), pymupdf.Point(w, h),
                           color=(0.75, 0.75, 0.75), width=0.5)
        dual_path = os.path.join(outdir, "%s.%s.direct.dual.pdf" % (stem, lang_out))
        dual.save(dual_path, garbage=3, deflate=True)
    finally:
        dual.close()
        tra.close()
        src.close()
    return dual_path

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scan_pdf.py —— 暗标格式"防盲"合规扫描仪 · PDF 最佳努力提取引擎

PDF 的字体/页边距深层提取不可靠（字体通常内嵌、页边距无标准字段），
因此本脚本聚焦"可确定"的项：页数、页面尺寸（A4 判定）、文档元数据、全文身份扫描。
对于字体/加粗/行距/页边距等精细格式，脚本会在结果中标注 "unreliable"，
并建议将 PDF 转回 .docx 后用 scan_docx.py 做硬检。

依赖：pypdf（pip install pypdf）。缺失时脚本给出明确报错，由 WorkBuddy 在受管 venv 安装。
输出：单行 JSON 到 stdout。
"""

import sys
import json
import re
import argparse
from pathlib import Path

try:
    from pypdf import PdfReader
except ImportError:
    sys.stderr.write("缺少依赖 pypdf。请在受管 venv 执行：pip install pypdf\n")
    sys.exit(2)

# 与 scan_docx.py 保持一致的启发式泄漏词
HEURISTIC_LEAK_PATTERNS = [
    r"我\s*公司", r"我\s*司", r"本\s*公司", r"我\s*们\s*公司", r"我\s*单位",
    r"荣\s*获", r"中\s*标", r"承\s*建", r"独\s*家", r"独\s*占", r"唯\s*一",
    r"行\s*业\s*领\s*先", r"一\s*流", r"领\s*先\s*地\s*位", r"龙\s*头\s*企\s*业",
    r"工\s*法", r"专\s*利", r"知\s*名\s*品\s*牌", r"著\s*名", r"首\s*家",
    r"自\s*主\s*研\s*发", r"核\s*心\s*技\s*术", r"荣\s*获\s*.*奖", r"ISO\s*9\d{3,}",
    r"三\s*标\s*一\s*体", r"AAA\s*级", r"省\s*级\s*.*奖", r"国\s*家\s*级\s*.*奖",
]


def scan_identity(text, identifiers, run_heuristics, allow=None):
    allow = set(a.strip().lower() for a in (allow or []) if a.strip())
    hits = []
    for ident in identifiers:
        ident = ident.strip()
        if not ident:
            continue
        for m in re.finditer(re.escape(ident), text):
            s = max(0, m.start() - 50)
            e = min(len(text), m.end() + 50)
            hits.append({"type": "identifier", "match": ident, "pos": m.start(), "context": text[s:e]})
    if run_heuristics:
        for pat in HEURISTIC_LEAK_PATTERNS:
            for m in re.finditer(pat, text):
                s = max(0, m.start() - 50)
                e = min(len(text), m.end() + 50)
                hits.append({"type": "heuristic", "match": m.group(0), "pos": m.start(), "context": text[s:e]})
    if allow:
        hits = [h for h in hits if h["match"].strip().lower() not in allow]
    seen = set()
    uniq = []
    for h in sorted(hits, key=lambda x: x["pos"]):
        key = (h["pos"], h["match"])
        if key in seen:
            continue
        seen.add(key)
        uniq.append(h)
    return uniq


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("pdf_path", help="待扫描的 .pdf 文件路径")
    ap.add_argument("--identifiers", default="", help="投标人可识别身份信息，逗号分隔")
    ap.add_argument("--allow", default="", help="白名单（逗号分隔）。命中的措辞若在本名单内则不报，用于项目允许的自称/术语，如'我公司,我单位'。仅精确匹配")
    ap.add_argument("--no-heuristics", action="store_true", help="关闭启发式泄漏词扫描")
    args = ap.parse_args()

    path = Path(args.pdf_path)
    if not path.exists():
        sys.stderr.write(f"文件不存在: {path}\n")
        sys.exit(1)

    identifiers = [x for x in args.identifiers.split(",") if x.strip()]
    result = {"file": str(path), "format": "pdf", "pages": None,
              "page_sizes": [], "doc_properties": {}, "leakage_hits": [],
              "unreliable_fields": ["font_name", "font_size", "bold", "italic",
                                     "underline", "line_spacing", "margins",
                                     "alignment", "first_line_indent", "header_footer_page_number"],
              "errors": []}

    try:
        reader = PdfReader(str(path))
        result["pages"] = len(reader.pages)
        # 页面尺寸（pt）：A4 = 595.27 x 841.89
        for i, pg in enumerate(reader.pages):
            box = pg.mediabox
            w = float(box.width)
            h = float(box.height)
            is_a4 = abs(w - 595.27) < 5 and abs(h - 841.89) < 5
            result["page_sizes"].append({
                "page": i + 1, "width_pt": round(w, 1), "height_pt": round(h, 1),
                "is_a4": is_a4,
            })
        # 元数据
        meta = reader.metadata or {}
        result["doc_properties"] = {
            "author": meta.get("/Author"),
            "creator": meta.get("/Creator"),
            "producer": meta.get("/Producer"),
            "title": meta.get("/Title"),
            "company": meta.get("/Company"),
        }
        # 全文提取 + 身份扫描
        text_parts = []
        for pg in reader.pages:
            try:
                text_parts.append(pg.extract_text() or "")
            except Exception:
                pass
        full_text = "\n".join(text_parts)
        result["text_length"] = len(full_text)
        allow_set = [x for x in args.allow.split(",") if x.strip()]
        result["leakage_hits"] = scan_identity(full_text, identifiers, not args.no_heuristics, allow_set)
    except Exception as e:
        result["errors"].append(f"PDF 解析失败: {e}")
        sys.stderr.write(f"PDF 解析失败: {e}\n")

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

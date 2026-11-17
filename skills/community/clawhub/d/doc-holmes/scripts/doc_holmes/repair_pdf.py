"""span 级图层重复检测（plan.md T2.3 的检测层；v1.1 修订）。

v1.1.0 修订说明：原计划做 redaction 手术删除冗余 span，实测不可行——
pymupdf 的 apply_redactions 按"矩形相交删字形"工作，而双重打印的两份字形
几乎完全重叠，删任一份必然摧毁两份（回归测试抓到整行丢失）。按保守原则
降级为**纯检测**：同文+近位置的冗余 span 精确计数入审计，绝不修改文件。
若未来引擎层支持按绘制调用删除，再升级为手术。
"""

from __future__ import annotations

import pymupdf

# 同文判定容差（pt）：双重打印通常偏移 <1pt
POS_TOLERANCE = 2.0


def _norm(text: str) -> str:
    return " ".join(text.split())


def collect_duplicate_spans(page) -> list:
    """收集一页内"完全同文+近位置"的冗余 span（保留首见，余为冗余）。

    返回 [(text, bbox)]，bbox 为冗余份的矩形（仅报告用，不做修改）。
    """
    seen = []
    redundant = []
    try:
        raw = page.get_text("rawdict")
    except Exception:
        return []
    for block in raw.get("blocks", []):
        for line in block.get("lines", []):
            for span in line.get("spans", []):
                text = _norm("".join(ch.get("c", "") for ch in span.get("chars", [])))
                if len(text) < 6:
                    continue
                x0, y0, x1, y1 = span["bbox"]
                is_dup = False
                for (t, sx0, sy0) in seen:
                    if t == text and abs(sx0 - x0) <= POS_TOLERANCE \
                            and abs(sy0 - y0) <= POS_TOLERANCE:
                        is_dup = True
                        break
                if is_dup:
                    redundant.append((text, pymupdf.Rect(x0, y0, x1, y1)))
                else:
                    seen.append((text, x0, y0))
    return redundant


def inspect_pdf_dedup(src_pdf: str) -> dict:
    """图层重复检测（只读，零修改）。返回统计。"""
    stats = {"pages": 0, "spans_duplicated": 0, "chars_duplicated": 0,
             "examples": []}
    doc = pymupdf.open(src_pdf)
    try:
        for page in doc:
            stats["pages"] += 1
            redundant = collect_duplicate_spans(page)
            for text, _rect in redundant:
                stats["spans_duplicated"] += 1
                stats["chars_duplicated"] += len(text)
                if len(stats["examples"]) < 3:
                    stats["examples"].append(text[:50])
    finally:
        doc.close()
    return stats

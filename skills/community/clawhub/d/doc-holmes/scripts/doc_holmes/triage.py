"""T0 triage 质量体检：A/B/C 分级。

  A 级：born-digital 完好（文本层密实、无图层重复、水印占比低）→ 高保真翻译
  B 级：有文本层但有噪（重复图层 / 水印 / 伪影）→ 可翻译，噪声明细入报告
  C 级：扫描件 / 无有效文本层 / 加密 → OCR 实验通道，产物强制「预览质量」说明页

分级判据（plan.md §2 / T1.1）：
  页均有效字符 < 50            → C（无有效文本层）
  加密且无口令                  → C（需解密）
  页均有效字符 ≥ 500 且无重复图层
  且水印行占比 < 2% 且无伪影    → A
  其余                          → B
"""

from __future__ import annotations

import os
from dataclasses import asdict, dataclass, field

import pymupdf

from . import repair, skip_rules

SAMPLE_PAGES = 3
MIN_CHARS_A = 500
MIN_CHARS_C = 50
WATERMARK_RATIO_A = 0.02

TIER_A, TIER_B, TIER_C = "A", "B", "C"


@dataclass
class TriageReport:
    path: str
    tier: str
    encrypted: bool = False
    page_count: int = 0
    sampled_pages: list = field(default_factory=list)
    chars_per_page: float = 0.0
    two_column: bool = False
    duplicate_pairs: int = 0
    duplicate_examples: list = field(default_factory=list)
    watermark_lines: int = 0
    artifact_hits: int = 0
    line_count: int = 0
    reasons: list = field(default_factory=list)
    engine_hints: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return asdict(self)


def _sample_indices(page_count: int, sample_pages: int) -> list:
    """前 N 页 + 中间页（长文档更代表性）。"""
    idx = list(range(min(sample_pages, page_count)))
    if page_count > 2 * sample_pages:
        mid = page_count // 2
        if mid not in idx:
            idx.append(mid)
    return idx


def _detect_two_column(page) -> bool:
    """双栏启发式：左右半区块各占三成以上且存在跨栏交错。仅作 engine hint。"""
    try:
        blocks = [b for b in page.get_text("blocks") if b[6] == 0]
    except Exception:
        return False
    if len(blocks) < 6:
        return False
    width = page.rect.width
    left = [b for b in blocks if b[2] < width * 0.55]
    right = [b for b in blocks if b[0] > width * 0.45]
    if len(left) < len(blocks) * 0.3 or len(right) < len(blocks) * 0.3:
        return False
    # 交错：按 y 排序后左右区块交替出现
    ys = sorted(
        [(b[1], 0 if b in left else 1) for b in blocks]
    )
    flips = sum(1 for i in range(1, len(ys)) if ys[i][1] != ys[i - 1][1])
    return flips >= 4


def triage_pdf(path: str, sample_pages: int = SAMPLE_PAGES) -> TriageReport:
    real = os.path.realpath(path)
    report = TriageReport(path=real, tier=TIER_B)
    try:
        doc = pymupdf.open(real)
    except Exception as exc:  # 无法打开 → 按 C 处理（最保守）
        report.tier = TIER_C
        report.reasons.append("无法打开 PDF：%s" % exc)
        return report

    report.page_count = doc.page_count
    if doc.needs_pass:
        report.encrypted = True
        report.tier = TIER_C
        report.reasons.append("PDF 已加密（needs_pass），需先解密（如 qpdf --decrypt）")
        doc.close()
        return report

    indices = _sample_indices(doc.page_count, sample_pages)
    total_chars = 0
    total_lines = 0
    dup_pairs = 0
    dup_examples = []
    watermark_lines = 0
    artifact_hits = 0
    two_col_votes = 0

    try:
        for i in indices:
            page = doc[i]
            text = page.get_text("text")
            report.sampled_pages.append(i)
            total_chars += len("".join(text.split()))
            issues = repair.detect_issues(text)
            total_lines += issues.line_count
            dup_pairs += issues.duplicate_pairs
            dup_examples.extend(issues.duplicate_examples[:2])
            watermark_lines += issues.watermark_lines()
            artifact_hits += issues.rule_hits.get("artifact_token", 0)
            if _detect_two_column(page):
                two_col_votes += 1
    finally:
        doc.close()

    pages = max(len(indices), 1)
    report.chars_per_page = round(total_chars / pages, 1)
    report.line_count = total_lines
    report.duplicate_pairs = dup_pairs
    report.duplicate_examples = dup_examples[:4]
    report.watermark_lines = watermark_lines
    report.artifact_hits = artifact_hits
    report.two_column = two_col_votes > pages / 2

    if report.chars_per_page < MIN_CHARS_C:
        report.tier = TIER_C
        report.reasons.append(
            "页均有效字符 %.0f < %d，视为无有效文本层（扫描件）" % (report.chars_per_page, MIN_CHARS_C))
    else:
        watermark_ratio = watermark_lines / max(total_lines, 1)
        is_a = (report.chars_per_page >= MIN_CHARS_A
                and dup_pairs == 0
                and watermark_ratio < WATERMARK_RATIO_A
                and artifact_hits == 0)
        if is_a:
            report.tier = TIER_A
            report.reasons.append("文本层密实（页均 %.0f 字符）、无图层重复、无伪影" % report.chars_per_page)
        else:
            report.tier = TIER_B
            if report.chars_per_page < MIN_CHARS_A:
                report.reasons.append("文本层偏薄（页均 %.0f 字符 < %d）" % (report.chars_per_page, MIN_CHARS_A))
            if dup_pairs:
                report.reasons.append("检测到 %d 处相邻图层重复" % dup_pairs)
            if watermark_lines:
                report.reasons.append("水印/噪声行 %d（占比 %.1f%%）" % (watermark_lines, watermark_ratio * 100))
            if artifact_hits:
                report.reasons.append("伪影 token 命中 %d（如 /G13）" % artifact_hits)

    report.engine_hints = {
        "ocr_recommended": report.tier == TIER_C,
        "two_column": report.two_column,
        "suggested_pages_sample": indices,
    }
    return report


def triage_path(path: str, sample_pages: int = SAMPLE_PAGES) -> list:
    """对文件或目录做 triage；目录时递归收集 PDF。"""
    import glob as _glob
    real = os.path.realpath(path)
    if os.path.isdir(real):
        pdfs = sorted(_glob.glob(os.path.join(real, "**", "*.pdf"), recursive=True))
        return [triage_pdf(p, sample_pages) for p in pdfs]
    return [triage_pdf(real, sample_pages)]

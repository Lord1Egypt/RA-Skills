#!/usr/bin/env python3
"""Select substantive summary evidence from normalized PDF/PPT text.

The selector is dependency-free so project adapters can reuse it after
embedded-text, OCR, or slide-reading-order extraction.
"""

from __future__ import annotations

from pathlib import Path
import re


CONTENT_SECTION_NAMES = {
    "Sampled Text",
    "Sampled Text / 采样文本",
    "Embedded Text",
    "Embedded Text / 内嵌文本",
    "OCR Text",
    "OCR Text / OCR 文本",
    "Reading Order Text",
    "Reading Order Text / 阅读顺序文本",
    "Front Sample",
    "Front Sample / 前部样本",
    "Back Sample",
    "Back Sample / 后部样本",
}
NOISE_HEADINGS = {
    # bilingual-compat: Legacy Chinese-only heading meaning "Table of contents."
    "目录",
    "Q&A",
    "THANK YOU",
    "File Metadata",
    "Deck Metadata",
    "Retrieval Note",
    "Sampled Content Note",
    "Layout Blocks",
    "Embedded Media Map",
    "Speaker Notes",
}
METADATA_PREFIX = re.compile(
    r"^(?:Creator|Producer|CreationDate|ModDate|Author|Title|Subject|Keywords|Pages|"
    r"Relative path|Size bytes|Extraction policy|Summary evidence|Source part|Text blocks|OCR status)\s*:",
    re.IGNORECASE,
)
DATE_OR_PAGE = re.compile(
    # bilingual-compat: Chinese year and full-width slash characters are source-detection literals.
    r"^(?:\d{4}[年./-]|\d+\s*/\s*\d+$|\d+\s*[/／]\s*\d+|"
    r"\d{1,2}\s*[/.-]\s*\d{1,2}\s*[/.-]\s*\d{2,4})"
)
SUMMARY_SIGNAL = re.compile(
    # bilingual-compat: Chinese domain terms are ranking lexicon entries, not user-facing output.
    r"架构|策略|排序|模型|算法|系统|特征|召回|过滤|推荐|数据|服务|"
    # bilingual-compat: Chinese domain terms are ranking lexicon entries, not user-facing output.
    r"性能|扩展|优化|指标|实验|Pipeline|FTRL|GBDT|XGBoost|LR\b",
    re.IGNORECASE,
)
# bilingual-compat: Chinese boilerplate terms are source-detection literals.
BOILERPLATE = re.compile(r"^(?:目录|Q&A|THANK YOU|致谢|谢谢|感谢)$", re.IGNORECASE)


def _heading(line: str) -> str:
    match = re.match(r"^#{1,6}\s+(.+)$", line.strip())
    return match.group(1).strip() if match else ""


def _is_content_heading(value: str) -> bool:
    return (
        value in CONTENT_SECTION_NAMES
        or value.startswith("OCR Page ")
        or value.startswith("OCR Page / OCR 页面 ")
        or value.startswith("Slide ")
        or value.startswith("Slide / 幻灯片 ")
    )


def _clean(line: str) -> str:
    return re.sub(r"\s+", " ", line.strip(" \t#|-")).strip()[:180]


def _is_noise(line: str, source: Path) -> bool:
    if not line or len(line) < 3:
        return True
    if BOILERPLATE.match(line) or METADATA_PREFIX.match(line) or DATE_OR_PAGE.match(line):
        return True
    if line == source.stem or line.lower() == source.stem.lower():
        return True
    return line.endswith("/ 10") or line.endswith("/10")


def _score(line: str) -> int:
    score = 0
    if len(line) >= 10:
        score += 1
    if 24 <= len(line) <= 150:
        score += 1
    score += min(len(SUMMARY_SIGNAL.findall(line)), 3) * 3
    if re.search(r"[：:]", line):
        score += 1
    return score


def select_summary_evidence(source: Path, markdown: str, limit: int = 4) -> list[str]:
    """Return ranked content lines, preferring OCR/embedded/slide evidence."""
    in_content = False
    prioritized: list[tuple[int, int, str]] = []
    fallback: list[tuple[int, int, str]] = []
    seen: set[str] = set()
    for order, raw_line in enumerate(markdown.splitlines()):
        heading = _heading(raw_line)
        if heading:
            if heading in NOISE_HEADINGS:
                in_content = False
            else:
                in_content = _is_content_heading(heading)
            continue
        line = _clean(raw_line)
        if _is_noise(line, source):
            continue
        key = re.sub(r"[\s\W_]+", "", line, flags=re.UNICODE).lower()
        if not key or key in seen:
            continue
        seen.add(key)
        target = prioritized if in_content else fallback
        target.append((_score(line), order, line))
    candidates = prioritized or fallback
    ranked = sorted(candidates, key=lambda item: (-item[0], item[1]))
    return [line for _, _, line in ranked[:limit]]

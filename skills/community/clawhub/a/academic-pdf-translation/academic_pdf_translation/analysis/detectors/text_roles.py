"""正文角色判定：标题、作者块、单位、出版元数据、正文。

现有的 `likely_heading` 只看字号和粗体，于是把作者单位、arXiv 版本戳、
图内标签，甚至句子中段都排成了章节标题。这里在同样的信号上加三条约束：
位置、上下文和文本形态。
"""

from __future__ import annotations

import re
from typing import Any

from academic_pdf_translation.contracts.enums import ElementType
from academic_pdf_translation.contracts.models import normalize_bbox

DETECTOR_VERSION = "text-roles-v1"

#: 带编号的章节标题，例如 "3 Training"、"3.1 Data Augmentation"、"二、方法"。
NUMBERED_HEADING_RE = re.compile(
    r"^\s*(?:\d+(?:\.\d+)*\.?|[一二三四五六七八九十]+[、.])\s+\S"
)
#: 常见的无编号章节标题。
BARE_HEADING_WORDS = frozenset(
    {
        "abstract",
        "introduction",
        "background",
        "method",
        "methods",
        "materials and methods",
        "results",
        "discussion",
        "conclusion",
        "conclusions",
        "acknowledgement",
        "acknowledgements",
        "acknowlegements",
        "references",
        "bibliography",
        "appendix",
        "摘要",
        "引言",
        "方法",
        "结果",
        "讨论",
        "结论",
        "致谢",
        "参考文献",
    }
)
#: 预印本或出版标识戳。
PUBLICATION_STAMP_RE = re.compile(
    r"(?:arxiv\s*:\s*\d|doi\s*:\s*10\.|bioRxiv|medRxiv|©|\bISSN\b"
    r"|\bISBN\b)",
    re.IGNORECASE,
)
#: 没有 "doi:" 前缀的裸 DOI。期刊排版常在首页最顶端印一条生产代码条：
#: "<稿件号> <刊物代码>10.xxxx/<DOI><作者><刊名> research-article<年份>"。
#: 它是出版元数据，不是标题，更不是编号章节标题。
BARE_DOI_RE = re.compile(r"(?<![\d.])10\.\d{4,9}/\S")
#: 只有短块才按裸 DOI 判为标识戳。正文里顺手引一个 DOI 的长段落仍是正文。
MAX_STAMP_CHARS = 200
#: 作者单位常见词。
AFFILIATION_WORDS = re.compile(
    r"(?:university|universit|institute|department|dept\.|laborator|college|"
    r"hospital|academy|centre|center|school of|faculty|大学|学院|研究所|系)",
    re.IGNORECASE,
)
#: 电子邮件。作者块的强信号。
EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
#: 句末标点。标题一般不带句号。
SENTENCE_END_RE = re.compile(r"[.。!！?？;；]\s*$")
#: 句中标点：出现它基本就不是标题。
SENTENCE_INSIDE_RE = re.compile(r"[.。!！?？][\s\"'”’)\]]")

#: 标题的长度上限（字符）。
MAX_HEADING_CHARS = 120
#: 标题最多几行。
MAX_HEADING_LINES = 3
#: 首页上部这个比例内出现的块才可能是标题/作者块。
TITLE_ZONE_RATIO = 0.42


def _plain(text: str) -> str:
    return re.sub(r"\s+", " ", str(text or "")).strip()


def looks_like_heading(text: str) -> bool:
    """只看文本形态：像不像一个章节标题。"""

    value = _plain(text)
    if not value or len(value) > MAX_HEADING_CHARS:
        return False
    if SENTENCE_INSIDE_RE.search(value):
        return False
    if NUMBERED_HEADING_RE.match(value):
        return True
    return value.casefold().strip(" :：") in BARE_HEADING_WORDS


def is_publication_stamp(text: str) -> bool:
    value = _plain(text)
    if PUBLICATION_STAMP_RE.search(value):
        return True
    return len(value) <= MAX_STAMP_CHARS and bool(BARE_DOI_RE.search(value))


def is_affiliation(text: str) -> bool:
    value = _plain(text)
    return bool(AFFILIATION_WORDS.search(value)) and not looks_like_heading(
        value
    )


def is_author_block(text: str) -> bool:
    value = _plain(text)
    if EMAIL_RE.search(value):
        return True
    if looks_like_heading(value) or is_affiliation(value):
        return False
    words = re.findall(r"[A-Za-zÀ-ÖØ-öø-ÿ][A-Za-zÀ-ÖØ-öø-ÿ.'-]*", value)
    if not words or len(value) > MAX_HEADING_CHARS:
        return False
    capitalized = sum(1 for word in words if word[:1].isupper())
    # 作者行的特征：短、多个首字母大写的词、用逗号或 and 连接。
    return (
        capitalized / len(words) >= 0.7
        and ("," in value or re.search(r"\band\b|、", value))
        and not SENTENCE_END_RE.search(value)
    )


def classify_block(
    block: dict[str, Any],
    page: dict[str, Any],
    *,
    inside_visual: bool,
    is_first_page: bool,
    is_first_text_block: bool,
) -> tuple[ElementType, float, list[str]]:
    """判定一个文本块的角色，并给出置信度与依据。"""

    text = _plain(block.get("text"))
    signals: list[str] = []
    if not text:
        return ElementType.UNKNOWN, 0.3, ["empty"]

    if inside_visual:
        # 图内标签绝不是章节标题：它只是画在图里的文字。
        return ElementType.UNKNOWN, 0.9, ["inside-visual-container"]

    if is_publication_stamp(text):
        return ElementType.PUBLICATION_METADATA, 0.9, ["publication-stamp"]

    box = normalize_bbox(block.get("bbox"))
    height = float(page.get("height") or 0) or 1.0
    in_title_zone = bool(
        is_first_page and box is not None and box[3] <= height * TITLE_ZONE_RATIO
    )

    if in_title_zone:
        if is_affiliation(text):
            return ElementType.AFFILIATION, 0.85, ["affiliation-words"]
        if is_author_block(text):
            return ElementType.AUTHOR_BLOCK, 0.8, ["author-name-pattern"]
        if is_first_text_block and not looks_like_heading(text):
            signals.append("first-block-on-first-page")
            return ElementType.DOCUMENT_TITLE, 0.85, signals

    lines = block.get("lines") or []
    font = block.get("font") or {}
    bold = bool(font.get("bold_signal"))
    if looks_like_heading(text):
        signals.append("heading-text-shape")
        if bold:
            signals.append("bold")
        if len(lines) <= MAX_HEADING_LINES:
            signals.append("short-block")
        confidence = 0.75 + (0.1 if bold else 0.0) + (
            0.1 if NUMBERED_HEADING_RE.match(text) else 0.0
        )
        return ElementType.HEADING, round(min(confidence, 0.97), 4), signals

    if block.get("likely_heading") and not looks_like_heading(text):
        # 现有扫描认为像标题，但文本形态不像。按正文处理并留下风险标记，
        # 让定向检查去看一眼。
        return (
            ElementType.BODY,
            0.6,
            ["heading-signal-rejected-by-text-shape"],
        )

    return ElementType.BODY, 0.9, ["body-text"]

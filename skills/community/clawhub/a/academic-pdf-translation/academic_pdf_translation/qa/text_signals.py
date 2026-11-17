"""QA 的文本信号：占位符、拉丁散文、汉字、参考文献、原文页标。

这些是判据的"词汇表"——判某段文字是不是残留原文、是不是占位符没替换、
是不是一行只剩一个汉字，全靠它们。原本散在 qa_pdf.py 顶部，
和排版度量的常量混在一处。

正则与字符串与搬出来之前逐字一致。
"""

from __future__ import annotations

import re

PLACEHOLDER_PATTERN = re.compile(
    r"\{\{[^{}]+\}\}|\{v\s*\d+\}|</?style\b[^>]*>|"
    r"<x\d+>|ZXQPH\d+QXZ|TODO_TRANSLATE|TRANSLATION_MISSING"
)
LATIN_PROSE_PATTERN = re.compile(
    r"\b(?:[A-Za-z][A-Za-z'-]*[ \t]+){3,}[A-Za-z][A-Za-z'-]*\b"
)
COMPATIBILITY_IDEOGRAPH_PATTERN = re.compile(r"[\uf900-\ufaff]")
HAN_CHARACTER_PATTERN = re.compile(r"[\u3400-\u9fff]")
ORPHAN_TRAILING_PUNCTUATION = "，。；：！？、）》】”’」』〉〕〗〙〛）,.;:!?]}”"
REFERENCE_KINDS = {
    "reference",
    "references",
    "bibliography",
}
SOURCE_MAPPING_LABEL_PATTERN = re.compile(
    r"^(?:"
    r"原文第\s*\d+\s*[页頁]|"
    r"source\s+page\s+\d+|page\s+source\s+\d+|"
    r"quellseite\s+\d+|página\s+original\s+\d+|"
    r"原文\s*\d+\s*ページ|원문\s*\d+\s*쪽"
    r")$",
    re.IGNORECASE,
)

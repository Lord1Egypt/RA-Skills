# FILE_META
# INPUT:  text content
# OUTPUT: scrubbed text + per-category redaction counts
# POS:    skill lib — called by workspace_bundle.py
# MISSION: Regex-based PII scrubbing (phones, emails, IDs, API keys) before upload.

"""Local regex-based PII scrubber for workspace files.

Replaces common PII patterns with placeholders before bundling.
Zero token consumption — pure regex, runs locally.
"""

from __future__ import annotations

import re

# (label, regex, replacement_tag)
_PATTERNS: list[tuple[str, re.Pattern, str]] = [
    ("手机号", re.compile(r"\+86\s*1[3-9]\d{9}(?!\d)"), "[PHONE]"),
    ("手机号", re.compile(r"(?<!\d)1[3-9]\d{9}(?!\d)"), "[PHONE]"),
    ("邮箱", re.compile(r"[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}"), "[EMAIL]"),
    ("身份证号", re.compile(r"(?<!\d)[1-9]\d{5}(?:19|20)\d{2}(?:0[1-9]|1[0-2])(?:0[1-9]|[12]\d|3[01])\d{3}[\dXx](?!\d)"), "[ID_CARD]"),
    ("银行卡号", re.compile(r"(?<!\d)(?<![a-fA-F])[4-6]\d{15,17}(?!\d)(?![a-fA-F])"), "[BANK_CARD]"),
    ("IP 地址", re.compile(r"(?<![\d.])\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}(?![\d.])"), "[IP]"),
    ("API Key", re.compile(r"sk-[a-zA-Z0-9\-_]{20,}"), "[API_KEY]"),
    ("API Key", re.compile(r"ghp_[a-zA-Z0-9]{36,}"), "[API_KEY]"),
    ("API Key", re.compile(r"gho_[a-zA-Z0-9]{36,}"), "[API_KEY]"),
    ("API Key", re.compile(r"glpat-[a-zA-Z0-9\-_]{20,}"), "[API_KEY]"),
    ("API Key", re.compile(r"xoxb-[a-zA-Z0-9\-]+"), "[API_KEY]"),
    ("API Key", re.compile(r"xoxp-[a-zA-Z0-9\-]+"), "[API_KEY]"),
    ("密码/密钥", re.compile(r"(?i)(?:api[_-]?key|secret[_-]?key|access[_-]?token|auth[_-]?token|password|passwd|secret)\s*[=:]\s*['\"]?[a-zA-Z0-9\-_./+]{8,}['\"]?"), "[REDACTED]"),
]


def scrub_text(text: str) -> str:
    """Remove PII from text using regex patterns.

    Returns scrubbed text. Original is not modified.
    """
    result = text
    for _label, pattern, replacement in _PATTERNS:
        result = pattern.sub(replacement, result)
    return result


def scrub_text_with_stats(text: str) -> tuple[str, dict[str, int]]:
    """Remove PII from text and return per-category match counts.

    Returns (scrubbed_text, {"手机号": 2, "邮箱": 1, ...}).
    Only categories with >0 matches are included.
    """
    result = text
    counts: dict[str, int] = {}
    for label, pattern, replacement in _PATTERNS:
        matches = pattern.findall(result)
        if matches:
            counts[label] = counts.get(label, 0) + len(matches)
            result = pattern.sub(replacement, result)
    return result, counts

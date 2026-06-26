from __future__ import annotations

import html
import re
from dataclasses import dataclass


HTML_TAG_RE = re.compile(r"<[^>]+>")
WHITESPACE_RE = re.compile(r"\s+")
CHINESE_RE = re.compile(r"[\u4e00-\u9fff]")


@dataclass(slots=True, frozen=True)
class FilterResult:
    title_clean: str
    title_body: str
    report_kind: str | None
    is_eligible: bool
    reason: str | None


def strip_html_tags(value: str) -> str:
    return HTML_TAG_RE.sub("", html.unescape(value or "")).strip()


_REPORT_KEYWORD_RE = re.compile(r"(?:\d{4}年?(?:年度|半年度)|年度报告|半年度报告|年报)")


def normalize_title_body(title: str) -> tuple[str, str]:
    title_clean = strip_html_tags(title)
    parts = re.split(r"[：:]", title_clean, maxsplit=1)
    body = parts[1] if len(parts) == 2 else title_clean
    # Strip everything before the first report-related keyword so that
    # "招商银行股份有限公司2024年度报告" becomes "2024年度报告"
    m = _REPORT_KEYWORD_RE.search(body)
    if m:
        body = body[m.start():]
    return title_clean, WHITESPACE_RE.sub("", body)


def _suffix_pattern() -> str:
    return (
        r"(?:(?:（[^）]*(?:修订|更正|更新)[^）]*）)"
        r"|(?:\([^)]*(?:修订|更正|更新)[^)]*\))"
        r"|(?:修订版|修订稿|更正版|更正后|更新后|修订后))?"
    )


def _formal_annual_pattern(year: int) -> re.Pattern[str]:
    """Match '2024年年度报告' or '2024年度报告' or '年度报告2024' or '年报2024'."""
    return re.compile(
        rf"^(?:{year}年?(?:年度报告|年报)|(?:年度报告|年报){year}){_suffix_pattern()}$"
    )


def _formal_semiannual_pattern(year: int) -> re.Pattern[str]:
    """Match '2024年半年度报告' or '半年度报告2024'."""
    return re.compile(
        rf"^(?:{year}年?半年度报告|半年度报告{year}){_suffix_pattern()}$"
    )


def evaluate_title(title: str, year: int) -> FilterResult:
    title_clean, title_body = normalize_title_body(title)
    lower_clean = title_clean.lower()

    if not title_clean:
        return FilterResult(title_clean, title_body, None, False, "empty title")
    if str(year) not in title_clean:
        return FilterResult(title_clean, title_body, None, False, "missing target year")
    if "摘要" in title_clean:
        return FilterResult(title_clean, title_body, None, False, "summary title")
    if not CHINESE_RE.search(title_clean):
        return FilterResult(title_clean, title_body, None, False, "non-Chinese title")
    if "英文" in title_clean or "english" in lower_clean or "annual report" in lower_clean:
        return FilterResult(title_clean, title_body, None, False, "english variant title")
    if "年报" not in title_clean and "年度报告" not in title_clean and "半年度报告" not in title_clean:
        return FilterResult(title_clean, title_body, None, False, "missing report keyword")

    if _formal_annual_pattern(year).fullmatch(title_body):
        return FilterResult(title_clean, title_body, "annual", True, None)
    if _formal_semiannual_pattern(year).fullmatch(title_body):
        return FilterResult(title_clean, title_body, "semiannual", True, None)
    return FilterResult(title_clean, title_body, None, False, "not a formal report title")

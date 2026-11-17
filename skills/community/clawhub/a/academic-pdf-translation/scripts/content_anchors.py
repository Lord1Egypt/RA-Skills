from __future__ import annotations

import re
import unicodedata
from collections import Counter
from decimal import Decimal, InvalidOperation
from typing import Any


CITATION_RE = re.compile(r"\[(\d+(?:\s*[-,;]\s*\d+)*)\]")
ACRONYM_RE = re.compile(
    r"(?<![A-Za-z0-9-])[A-Z][A-Z0-9-]{1,12}(?![A-Za-z0-9-])"
)
DOI_RE = re.compile(r"\b10\.\d{4,9}/[-._;()/:A-Z0-9]+\b", re.I)
URL_RE = re.compile(r"https?://[^\s<>\"']+", re.I)
RANGE_HYPHEN_RE = re.compile(
    r"(?P<left>(?:\d+(?:\.\d+)?|\.\d+)\s*%?)"
    r"\s*[-–—]\s*"
    r"(?=(?:\d|\.\d))"
)
PERCENT_RANGE_RE = re.compile(
    r"(?P<left>[-+]?(?:\d+(?:\.\d+)?|\.\d+))"
    r"\s*[-–—]\s*"
    r"(?P<right>[-+]?(?:\d+(?:\.\d+)?|\.\d+))\s*%"
)
STAT_VALUE_RE = re.compile(
    r"(?<![A-Za-z0-9_.])"
    r"[-+]?"
    r"(?:"
    r"(?:\d+(?:\.\d+)?|\.\d+)\s*%(?![A-Za-z0-9_])"
    r"|"
    r"(?:\d+\.\d+|\.\d+)(?![A-Za-z0-9_.])"
    r")"
)
PREFIXED_INTEGER_RE = re.compile(
    r"(?i)\b(?:n|df)\s*[=:<>]\s*([-+]?\d+)"
)
EN_QUANTITY_RE = re.compile(
    r"(?i)(?<![A-Za-z0-9_.])"
    r"(?P<value>\d+(?:\.\d+)?)\s*"
    r"(?P<unit>thousand|million|billion)\b"
)
ZH_QUANTITY_RE = re.compile(
    r"(?<![A-Za-z0-9_.])"
    r"(?P<value>\d+(?:\.\d+)?)\s*"
    r"(?P<unit>万|亿)"
)


ACRONYM_STOP = {
    "AND",
    "ARTICLE",
    "AUTHOR",
    "AUTHORS",
    "BY",
    "CONCLUSIONS",
    "CONTRIBUTIONS",
    "FOUNDATION",
    "FUNDING",
    "LITERATURE",
    "METHOD",
    "METHODS",
    "OPEN",
    "RESEARCH",
    "RESULTS",
    "REVIEW",
    "STATEMENT",
    "THEORY",
}


def _normalized(text: str) -> str:
    return (
        unicodedata.normalize("NFKC", text or "")
        .replace("\u2212", "-")
        .replace("\ufe63", "-")
        .replace("\u200b", "")
        .replace("\u2060", "")
        .replace("\u00ad", "")
    )


def _canonical_statistic(value: str) -> str:
    compact = re.sub(r"\s+", "", value).lower()
    percent = compact.endswith("%")
    number_text = compact[:-1] if percent else compact
    try:
        number = Decimal(number_text)
    except InvalidOperation:
        return compact
    if number == 0:
        number = Decimal(0)
    normalized = format(number.normalize(), "f")
    return normalized + ("%" if percent else "")


def citation_numbers(text: str) -> set[str]:
    values: set[str] = set()
    for match in CITATION_RE.finditer(text or ""):
        values.update(re.findall(r"\d+", match.group(1)))
    return values


def statistics(text: str) -> set[str]:
    value = _normalized(text)
    value = URL_RE.sub(" ", value)
    value = DOI_RE.sub(" ", value)
    value = re.sub(
        r"(?<![A-Za-z0-9_.])([-+])\s+(?=(?:\d|\.\d))",
        r"\1",
        value,
    )
    value = PERCENT_RANGE_RE.sub(
        r"\g<left>% to \g<right>%",
        value,
    )
    value = RANGE_HYPHEN_RE.sub(r"\g<left> to ", value)
    results = {
        _canonical_statistic(match.group(0))
        for match in STAT_VALUE_RE.finditer(value)
    }
    results.update(
        match.group(1).lower()
        for match in PREFIXED_INTEGER_RE.finditer(value)
    )
    return results


def acronyms(text: str) -> set[str]:
    counts = Counter(ACRONYM_RE.findall(text or ""))
    return {
        value
        for value, count in counts.items()
        if value not in ACRONYM_STOP
        and not value.isdigit()
        and len(value) <= 8
        and (
            count >= 2
            or any(character.isdigit() for character in value)
            or "-" in value
        )
    }


def present_acronyms(text: str) -> set[str]:
    return {
        value
        for value in ACRONYM_RE.findall(text or "")
        if value not in ACRONYM_STOP and not value.isdigit()
    }


def converted_statistics(
    source_text: str,
    target_text: str,
) -> set[str]:
    target_quantities: list[tuple[Decimal, str]] = []
    for match in ZH_QUANTITY_RE.finditer(_normalized(target_text)):
        try:
            target_quantities.append(
                (Decimal(match.group("value")), match.group("unit"))
            )
        except InvalidOperation:
            continue
    if not target_quantities:
        return set()
    factors = {
        ("thousand", "万"): Decimal("0.1"),
        ("thousand", "亿"): Decimal("0.00001"),
        ("million", "万"): Decimal("100"),
        ("million", "亿"): Decimal("0.01"),
        ("billion", "万"): Decimal("100000"),
        ("billion", "亿"): Decimal("10"),
    }
    covered: set[str] = set()
    for match in EN_QUANTITY_RE.finditer(_normalized(source_text)):
        try:
            source_value = Decimal(match.group("value"))
        except InvalidOperation:
            continue
        source_unit = match.group("unit").lower()
        for target_value, target_unit in target_quantities:
            factor = factors.get((source_unit, target_unit))
            if factor is None:
                continue
            expected = source_value * factor
            tolerance = max(abs(expected) * Decimal("0.000001"), Decimal("0.000001"))
            if abs(target_value - expected) <= tolerance:
                covered.add(match.group("value").lower())
                break
    return covered


def required_anchors(text: str) -> dict[str, list[str]]:
    normalized = _normalized(text)
    return {
        "statistics": sorted(statistics(normalized)),
        "citations": sorted(
            citation_numbers(normalized),
            key=lambda value: int(value),
        ),
        "acronyms": sorted(acronyms(normalized)),
        "dois": sorted(
            {
                match.group(0).rstrip(".,;)")
                for match in DOI_RE.finditer(normalized)
            }
        ),
        "urls": sorted(
            {
                match.group(0).rstrip(".,;)")
                for match in URL_RE.finditer(normalized)
            }
        ),
    }


def anchors_present(
    requirements: dict[str, Any],
    target_text: str,
) -> dict[str, list[str]]:
    normalized_target = _normalized(target_text)
    target_statistics = statistics(normalized_target)
    target_citations = citation_numbers(normalized_target)
    target_acronyms = present_acronyms(normalized_target)
    target_compact = re.sub(r"\s+", "", normalized_target)
    target_compact_lower = target_compact.lower()
    return {
        "statistics": [
            value
            for value in requirements.get("statistics", [])
            if value not in target_statistics
        ],
        "citations": [
            value
            for value in requirements.get("citations", [])
            if value not in target_citations
        ],
        "acronyms": [
            value
            for value in requirements.get("acronyms", [])
            if value not in target_acronyms
        ],
        "dois": [
            value
            for value in requirements.get("dois", [])
            if re.sub(r"\s+", "", str(value)).lower()
            not in target_compact_lower
        ],
        "urls": [
            value
            for value in requirements.get("urls", [])
            if re.sub(r"\s+", "", str(value)) not in target_compact
            and not (
                (doi := DOI_RE.search(str(value)))
                and doi.group(0).lower() in target_compact_lower
            )
        ],
    }

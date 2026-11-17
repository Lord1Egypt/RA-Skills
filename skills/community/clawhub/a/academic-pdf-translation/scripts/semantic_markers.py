from __future__ import annotations

import re
from typing import Any

SEMANTIC_BOUNDARY_PATTERNS = {
    "en": re.compile(
        r"\b(?:not|no|without|neither|nor|may|might|could|suggest(?:s|ed)?|"
        r"appear(?:s|ed)?|likely|associate(?:d|s)?|correlat(?:e|ed|ion)|"
        r"predict(?:s|ed|ion)?|caus(?:e|ed|al)|effect|result(?:s|ed)? in|"
        r"lead(?:s|ing)? to|limitation(?:s)?)\b",
        re.I,
    ),
    "zh": re.compile(
        r"(?:并非|不是|不能|无法|未发现|没有|可能|或许|提示|表明|"
        r"相关|关联|预测|导致|因果|局限)"
    ),
    "fr": re.compile(
        r"\b(?:ne|pas|sans|peut|pourrait|sugg[eè]re|semble|associ|"
        r"corr[eé]l|pr[eé]dit|caus|effet|limite)\w*\b",
        re.I,
    ),
    "de": re.compile(
        r"\b(?:nicht|kein|ohne|kann|k[oö]nnte|deutet|scheint|"
        r"assozi|korrel|vorhers|urs[aä]ch|effekt|grenze)\w*\b",
        re.I,
    ),
    "es": re.compile(
        r"\b(?:no|sin|puede|podr[ií]a|sugiere|parece|asoci|"
        r"correl|predic|caus|efecto|limitaci[oó]n)\w*\b",
        re.I,
    ),
}

STATISTICS_PATTERN = re.compile(
    r"(?:\b(?:sample|participant|respondent|subjects?|patients?|"
    r"mean|median|standard deviation|confidence interval|effect size|"
    r"odds ratio|hazard ratio|cronbach|regression|anova|chi[- ]?square)\b"
    r"|\b[NP]\s*[=:]\s*\d+"
    r"|\bp\s*(?:[<=>≤≥])\s*0?\.\d+"
    r"|\b(?:SD|SE|CI|OR|HR|RR)\s*[=:]\s*[-+]?\d"
    r"|\d+(?:\.\d+)?\s*%)",
    re.I,
)

INSTRUMENT_PATTERN = re.compile(
    r"\b(?:scale|questionnaire|inventory|instrument|measure|item|"
    r"subscale|likert|reverse[- ]?scor|score(?:d|s|ing)?|"
    r"cronbach(?:'s)? alpha|reliability|validity)\b",
    re.I,
)

HIGH_RISK_SECTION_PATTERN = re.compile(
    r"\b(?:abstract|results?|discussion|limitations?|conclusions?)\b"
    r"|(?:摘要|结果|讨论|局限|结论)",
    re.I,
)


def _language_family(source_language: str) -> str:
    value = source_language.casefold()
    if value.startswith("zh"):
        return "zh"
    for family in ("fr", "de", "es"):
        if value.startswith(family):
            return family
    return "en"


def infer_review_flags(
    source: str,
    kind: str,
    source_language: str = "und-Latn",
) -> list[str]:
    text = str(source or "")
    normalized_kind = str(kind or "").casefold()
    family = _language_family(source_language)
    flags: list[str] = []
    if SEMANTIC_BOUNDARY_PATTERNS[family].search(text):
        flags.append("semantic-boundary")
    if (
        normalized_kind in {"abstract", "result", "discussion", "conclusion"}
        or HIGH_RISK_SECTION_PATTERN.search(text)
    ):
        flags.append("semantic-high-risk")
    if STATISTICS_PATTERN.search(text):
        flags.append("statistics-or-sample")
    if INSTRUMENT_PATTERN.search(text):
        flags.append("instrument-item-or-scoring")
    return flags


def validate_terminology(
    terminology: Any,
    units: list[dict[str, Any]],
) -> list[str]:
    errors: list[str] = []
    if not isinstance(terminology, list):
        return ["translation.terminology 必须是数组"]
    seen_sources: set[str] = set()
    for index, entry in enumerate(terminology):
        label = f"translation.terminology[{index}]"
        if not isinstance(entry, dict):
            errors.append(f"{label} 必须是对象")
            continue
        source = str(entry.get("source") or "").strip()
        target = str(
            entry.get("target")
            or entry.get("preferred")
            or entry.get("translation")
            or ""
        ).strip()
        if not source or not target:
            errors.append(f"{label} 必须包含 source 和 target")
            continue
        source_key = source.casefold()
        if source_key in seen_sources:
            errors.append(f"术语重复登记: {source}")
        seen_sources.add(source_key)
        variants = entry.get("allowed_variants", [])
        if not isinstance(variants, list) or not all(
            isinstance(value, str) and value.strip()
            for value in variants
        ):
            errors.append(f"{label}.allowed_variants 必须是非空字符串数组")
            variants = []
        case_sensitive = entry.get("case_sensitive") is True
        raw_source_variants = entry.get("source_variants", [])
        source_variants = (
            [
                str(value).strip()
                for value in raw_source_variants
                if isinstance(value, str) and value.strip()
            ]
            if isinstance(raw_source_variants, list)
            else []
        )
        if " / " in source:
            source_variants.extend(
                value.strip()
                for value in source.split(" / ")
                if value.strip()
            )
        source_variants.append(source)
        source_variants = list(dict.fromkeys(source_variants))
        matching_units = []
        for unit in units:
            source_text = str(unit.get("source") or "")
            haystack = source_text if case_sensitive else source_text.casefold()
            if any(
                (value if case_sensitive else value.casefold()) in haystack
                for value in source_variants
            ):
                matching_units.append(unit)
        if not matching_units:
            errors.append(f"术语没有在冻结原文中出现: {source}")
            continue
        accepted = [target, *variants]
        for unit in matching_units:
            if str(unit.get("keep_source_code") or "").strip():
                # 保留原文的单元（题录、署名、DOI 等）没有译文可查：
                # 术语门槛管的是译文里术语用得对不对，不是逼保留区翻译。
                continue
            translated = str(unit.get("translation") or "")
            if not any(value in translated for value in accepted):
                errors.append(
                    f"翻译单元 {unit.get('id')} 未使用登记术语 "
                    f"{source} → {target}"
                )
    return errors

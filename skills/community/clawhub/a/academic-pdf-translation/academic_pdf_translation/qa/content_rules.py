"""内容判据：占位符、拉丁语料、原文残留、图像与字体嵌入。

从 ``scripts/qa_pdf.py`` 原样搬来，行为不变。它们只吃译文单元、
载荷与页面对象，吐字符串、布尔值或问题清单，不读作业文件。

有两条判据值得单独说：

- ``meaningful_page_image_count`` 只数**有意义的**图：一像素的间隔条、
  贴满整页的白底都不算图，否则"这一页图丢了没有"永远判不准。
- ``font_embedding_issues`` 认的是字体有没有真嵌进 PDF，不是字体名
  好不好看——名字对而没嵌进去，读者那边就是一片空白。
"""

from __future__ import annotations

import re
import unicodedata
from collections import defaultdict
from typing import Any

from academic_pdf_translation.qa.text_signals import PLACEHOLDER_PATTERN


def placeholder_token(text: str) -> str:
    return re.sub(
        r"\s+",
        "",
        unicodedata.normalize("NFKC", text or ""),
    )

def expected_literal_placeholder_tokens(
    translation: dict[str, Any],
) -> set[str]:
    units_by_page: dict[int, list[dict[str, Any]]] = defaultdict(list)
    for unit in translation.get("units", []):
        if isinstance(unit, dict) and isinstance(unit.get("page"), int):
            units_by_page[int(unit["page"])].append(unit)
    allowed: set[str] = set()
    for units in units_by_page.values():
        source = "\n".join(str(unit.get("source") or "") for unit in units)
        if "{" not in source or "}" not in source:
            continue
        target = "\n".join(
            str(unit.get("translation") or unit.get("source") or "")
            for unit in units
        )
        allowed.update(
            placeholder_token(hit)
            for hit in PLACEHOLDER_PATTERN.findall(target)
            if hit.startswith("{{")
        )
    return allowed

def allowed_latin_corpus(text: str) -> str:
    variants = {
        re.sub(r"[^a-z0-9]+", "", text.casefold()),
        re.sub(
            r"[^a-z0-9]+",
            "",
            re.sub(
                r"\b[A-Z][A-Z0-9]{1,4}\b",
                "",
                text,
            ).casefold(),
        ),
    }
    return "\n".join(value for value in variants if value)

def complex_localized_source_labels(
    item: dict[str, Any],
) -> list[str]:
    payload = item.get("payload")
    if not isinstance(payload, dict):
        return []
    sources: list[str] = []
    for region in payload.get("regions", []):
        if not isinstance(region, dict):
            continue
        for label in region.get("localized_labels", []):
            if not isinstance(label, dict):
                continue
            value = (
                label.get("source")
                or label.get("source_text")
                or label.get("label")
                or label.get("original")
                or ""
            )
            if isinstance(value, list):
                text = " ".join(
                    str(part).strip()
                    for part in value
                    if str(part).strip()
                )
            else:
                text = str(value).strip()
            if text:
                sources.append(text)
    for component in payload.get("components", []):
        if not isinstance(component, dict):
            continue
        sources.extend(
            complex_localized_source_labels(
                {
                    "payload": component.get("payload") or component,
                }
            )
        )
    return sources

def mapped_entry_has_visible_retained_content(entry: dict[str, Any]) -> bool:
    return any(
        str(region_id).strip()
        for region_id in entry.get("retained_region_ids", [])
    )

def unit_is_substantive_body_prose(unit: dict | None) -> bool:
    if not isinstance(unit, dict):
        return False
    if str(unit.get("kind") or "").lower() not in {
        "body",
        "list-item",
        "paragraph",
    }:
        return False
    text = re.sub(r"\s+", " ", str(unit.get("source") or "")).strip()
    if not text:
        return False
    latin_words = re.findall(r"[A-Za-z]+(?:['’-][A-Za-z]+)*", text)
    cjk_chars = re.findall(r"[\u3400-\u9fff]", text)
    if len(cjk_chars) >= 80 or len(latin_words) >= 28:
        return True
    return (
        len(latin_words) >= 18
        and bool(re.search(r"[.!?。！？](?:[\"'”’)\]]*)$", text))
    )

def looks_like_proper_name(sample: str) -> bool:
    tokens = re.findall(r"[A-Za-zÀ-ÖØ-öø-ÿ][A-Za-zÀ-ÖØ-öø-ÿ’'`.-]*", sample)
    if not 2 <= len(tokens) <= 7:
        return False
    particles = {"de", "del", "der", "di", "du", "la", "le", "van", "von"}
    return all(
        token.casefold() in particles
        or bool(re.fullmatch(r"[A-ZÀ-ÖØ-Þ][A-Za-zÀ-ÖØ-öø-ÿ’'`.-]*", token))
        for token in tokens
    )

def inventory_accounts_for_missing_image(item: dict) -> bool:
    policy = str(item.get("translation_policy") or "").lower()
    if policy == "omit-nonsemantic":
        return bool(
            item.get("text_status") == "not-applicable"
            and str(item.get("translation_policy_reason") or "").strip()
        )
    method = str(item.get("method") or "").lower()
    status = str(item.get("status") or "").lower()
    payload_ready = bool(
        status == "payload-ready"
        and str(item.get("payload_status") or "").lower() == "ready"
        and str(item.get("text_status") or "").lower() == "translated"
        and str(item.get("complex_payload_id") or "").strip()
    )
    return bool(
        method in {"vector-rebuild", "structured-table-rebuild"}
        and (
            status in {"translated", "resolved", "pass"}
            or payload_ready
        )
    )

def meaningful_image_bbox(
    bbox: Any,
    *,
    page_width: float,
    page_height: float,
) -> bool:
    if (
        not isinstance(bbox, (list, tuple))
        or len(bbox) != 4
        or not all(isinstance(value, (int, float)) for value in bbox)
    ):
        return False
    x0, y0, x1, y1 = map(float, bbox)
    width = abs(x1 - x0)
    height = abs(y1 - y0)
    page_area = max(float(page_width) * float(page_height), 1.0)
    return bool(
        width >= 8.0
        and height >= 8.0
        and width * height >= max(100.0, page_area * 0.00025)
    )

def meaningful_page_image_count(page: Any) -> int:
    page_width = float(page.rect.width)
    page_height = float(page.rect.height)
    try:
        image_info = page.get_image_info(xrefs=True)
    except Exception:
        image_info = []
    if not image_info:
        image_info = [
            block
            for block in page.get_text("dict").get("blocks", [])
            if block.get("type") == 1
        ]
    seen: set[tuple[Any, tuple[float, ...]]] = set()
    for item in image_info:
        bbox = item.get("bbox") if isinstance(item, dict) else None
        if not meaningful_image_bbox(
            bbox,
            page_width=page_width,
            page_height=page_height,
        ):
            continue
        key = (
            item.get("xref") if isinstance(item, dict) else None,
            tuple(round(float(value), 2) for value in bbox),
        )
        seen.add(key)
    return len(seen)

def font_name_token(value: str) -> str:
    name = re.sub(r"^[A-Z]{6}\+", "", str(value or ""))
    name = re.sub(r"-\d+$", "", name)
    return re.sub(r"[^a-z0-9]+", "", name.casefold())

def font_embedding_issues(document: Any) -> list[dict]:
    issues: list[dict] = []
    seen: set[int] = set()
    used_font_tokens = {
        token
        for page_number in range(document.page_count)
        for block in document[page_number].get_text("dict").get("blocks", [])
        if block.get("type") == 0
        for line in block.get("lines", [])
        for span in line.get("spans", [])
        if (token := font_name_token(str(span.get("font") or "")))
    }
    for page_number in range(document.page_count):
        for font in document.get_page_fonts(page_number, full=True):
            xref = int(font[0])
            if xref in seen:
                continue
            seen.add(xref)
            basefont = str(font[3])
            basefont_token = font_name_token(basefont)
            if basefont_token and not any(
                basefont_token in used or used in basefont_token
                for used in used_font_tokens
            ):
                continue
            if xref <= 0:
                issues.append({"xref": xref, "font": basefont, "reason": "no-xref"})
                continue
            try:
                extracted = document.extract_font(xref)
                font_bytes = extracted[-1] if extracted else b""
            except Exception:
                font_bytes = b""
            if not font_bytes:
                issues.append(
                    {"xref": xref, "font": basefont, "reason": "not-embedded"}
                )
    return issues

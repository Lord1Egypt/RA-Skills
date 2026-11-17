from __future__ import annotations

import re
from datetime import datetime
from typing import Any

from .constants import PRICE_TOKEN_RE, PROMOTION_MARKERS
from .html_extract import has_schema_type, iter_json_objects, meta_content, parse_json_scripts
from .shared import normalize_space, normalized_key, parse_localized_price, split_author_roles, strip_html, truncate_text


class AudibleParseError(RuntimeError):
    pass


class NoActivePromotionError(RuntimeError):
    pass


def _parse_json_ld_blocks(html_text: str) -> list[Any]:
    return parse_json_scripts(html_text, "application/ld+json")


def _flatten_json_ld_items(html_text: str) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    for payload in _parse_json_ld_blocks(html_text):
        items.extend(iter_json_objects(payload))
    return items


def _find_json_ld_product(html_text: str) -> dict[str, Any] | None:
    for item in _flatten_json_ld_items(html_text):
        if has_schema_type(item, "Product"):
            return item
    return None


def _extract_audible_metadata_blocks(html_text: str) -> list[dict[str, Any]]:
    blocks: list[dict[str, Any]] = []
    matches = re.findall(r"<adbl-product-metadata\b[^>]*>(.*?)</adbl-product-metadata>", html_text, re.I | re.S)
    for block in matches:
        for payload in parse_json_scripts(block, "application/json"):
            if isinstance(payload, dict):
                blocks.append(payload)
    return blocks


def _parse_author_entities(raw: Any) -> list[str]:
    values: list[str] = []
    if isinstance(raw, str):
        cleaned = normalize_space(raw)
        if cleaned:
            values.append(cleaned)
        return values
    if isinstance(raw, dict):
        name = normalize_space(str(raw.get("name") or ""))
        if name:
            values.append(name)
        return values
    if isinstance(raw, list):
        for item in raw:
            values.extend(_parse_author_entities(item))
    return values


def _merge_audible_metadata(blocks: list[dict[str, Any]]) -> dict[str, Any]:
    merged: dict[str, Any] = {"authors": [], "categories": []}
    for block in blocks:
        if not merged.get("duration") and block.get("duration"):
            merged["duration"] = block.get("duration")
        if not merged.get("releaseDate") and block.get("releaseDate"):
            merged["releaseDate"] = block.get("releaseDate")
        if not merged.get("authors") and block.get("authors"):
            merged["authors"] = _parse_author_entities(block.get("authors"))
        if isinstance(block.get("categories"), list):
            categories = merged.setdefault("categories", [])
            for item in block["categories"]:
                if not isinstance(item, dict):
                    continue
                label = normalize_space(str(item.get("name") or ""))
                if label and label not in categories:
                    categories.append(label)
    return merged


def _extract_json_ld_authors(html_text: str) -> list[str]:
    authors: list[str] = []
    for item in _flatten_json_ld_items(html_text):
        for author in _parse_author_entities(item.get("author")):
            if author and author not in authors:
                authors.append(author)
    return authors


def _parse_audible_summary(html_text: str) -> str:
    match = re.search(
        r"<adbl-text-block\b(?=[^>]*\bslot\s*=\s*['\"]summary['\"])[^>]*>(.*?)</adbl-text-block>",
        html_text,
        re.I | re.S,
    )
    if match:
        return re.sub(r"\s+([.,;:!?])", r"\1", strip_html(match.group(1)))
    return ""


def _is_plausible_genre_label(value: str) -> bool:
    label = normalize_space(strip_html(value))
    if not label:
        return False
    if len(label) > 48:
        return False
    if len(label.split()) > 5:
        return False
    if not re.search(r"[A-Za-zÀ-ÿ]", label):
        return False
    if re.search(r"[{}\"]", label):
        return False
    if re.search(r"(?:https?://|www\.)", label, re.I):
        return False
    if re.search(r"(?:\b\d{2,}\b|[$£€])", label):
        return False
    lowered = label.casefold()
    blocked_substrings = (
        "sign in",
        "audible",
        "daily deal",
        "subscribe",
        "podcast",
        "customer",
        "copy link",
        "buy for",
        "try for",
        "add to",
        "help center",
        "please try again",
        "preview",
        "cancel anytime",
        "no results",
        "suggested searches",
        "narrated by",
        "english español",
    )
    return not any(marker in lowered for marker in blocked_substrings)


def parse_audible_chip_genres(html_text: str) -> list[str]:
    genres: list[str] = []
    for match in re.finditer(r'<adbl-chip\b[^>]*>(.*?)</adbl-chip>', html_text, re.I | re.S):
        label = normalize_space(strip_html(match.group(1)))
        if _is_plausible_genre_label(label) and label not in genres:
            genres.append(label)
    return genres


def _parse_audible_author_fallback(html_text: str) -> str:
    matches = re.findall(
        r"<a\b(?=[^>]*\bhref\s*=\s*['\"][^'\"]*/author/[^'\"]+['\"])[^>]*>(.*?)</a>",
        html_text,
        re.I | re.S,
    )
    if matches:
        return normalize_space(strip_html(matches[0]))
    match = re.search(r"By:\s*</span>\s*<a[^>]*>([^<]+)</a>", html_text, re.I | re.S)
    if match:
        return normalize_space(strip_html(match.group(1)))
    return ""


def _parse_audible_author_info(html_text: str, metadata: dict[str, Any]) -> tuple[str, str, str]:
    metadata_authors = _parse_author_entities(metadata.get("authors"))
    if metadata_authors:
        author = split_author_roles(metadata_authors[0])
        if author:
            return author, "structured_metadata", "high"
    json_ld_authors = _extract_json_ld_authors(html_text)
    if json_ld_authors:
        author = split_author_roles(json_ld_authors[0])
        if author:
            return author, "json_ld", "high"
    fallback_author = split_author_roles(_parse_audible_author_fallback(html_text))
    if fallback_author:
        return fallback_author, "html_fallback", "low"
    return "", "missing", "missing"


def _parse_release_year(raw_release_date: str | None) -> int | None:
    text = normalize_space(raw_release_date or "")
    if not text:
        return None
    for fmt in ("%m-%d-%y", "%m-%d-%Y", "%Y-%m-%d"):
        try:
            return datetime.strptime(text, fmt).year
        except Exception:
            continue
    match = re.search(r"(\d{4})", text)
    if match:
        return int(match.group(1))
    return None


def _parse_audible_member_hidden(html_text: str) -> bool:
    lowered = html_text.lower()
    return "member only" in lowered or "logged in to redeem this offer price" in lowered


def _first_price_near_markers(html_text: str) -> float | None:
    original = normalize_space(strip_html(html_text))
    lowered = original.casefold()
    for marker in PROMOTION_MARKERS:
        offset = lowered.find(marker)
        if offset < 0:
            continue
        window = original[max(0, offset - 80) : offset + 260]
        match = PRICE_TOKEN_RE.search(window)
        if match:
            return parse_localized_price(match.group(0))
    return None


def _parse_list_price(product_json: dict[str, Any], html_text: str) -> float | None:
    offers = product_json.get("offers") if isinstance(product_json.get("offers"), dict) else {}
    if isinstance(offers, dict):
        price = parse_localized_price(str(offers.get("price") or ""))
        if price is not None:
            return price
    buy_now = re.search(r"(?:buy now for|für|acheter pour|buy for)\s*([^<\n]+)", html_text, re.I)
    if buy_now:
        price = parse_localized_price(buy_now.group(1))
        if price is not None:
            return price
    return None


def _parse_isbn_like(product_json: dict[str, Any], metadata: dict[str, Any], html_text: str, field_name: str) -> str:
    for source in (product_json, metadata):
        value = normalize_space(str(source.get(field_name) or ""))
        if value:
            return value
    match = re.search(rf"{field_name}\D+([0-9Xx-]+)", html_text, re.I)
    if match:
        return normalize_space(match.group(1))
    return ""


def parse_audible_deal(html_text: str, final_url: str, requested_url: str) -> dict[str, Any]:
    product_json = _find_json_ld_product(html_text) or {}
    metadata = _merge_audible_metadata(_extract_audible_metadata_blocks(html_text))
    title = normalize_space(str(product_json.get("name") or ""))
    if not title:
        title_match = re.search(r"<h1\b[^>]*>(.*?)</h1>", html_text, re.I | re.S)
        title = normalize_space(strip_html(title_match.group(1) if title_match else ""))
    if not title:
        raise AudibleParseError("failed to parse Audible title")

    author, author_source, author_reliability = _parse_audible_author_info(html_text, metadata)
    if not author:
        raise AudibleParseError("failed to parse Audible author")

    summary = _parse_audible_summary(html_text)
    if not summary:
        raise AudibleParseError("failed to parse Audible summary")

    sale_price = _first_price_near_markers(html_text)
    member_hidden = _parse_audible_member_hidden(html_text)
    if sale_price is None and not member_hidden:
        raise NoActivePromotionError(f"No active daily promotion was found at {requested_url}.")

    runtime = normalize_space(str(metadata.get("duration") or "")) or normalize_space(str(product_json.get("duration") or "")) or "Unknown"
    year = _parse_release_year(str(metadata.get("releaseDate") or "")) or _parse_release_year(str(product_json.get("datePublished") or ""))
    cover_url = normalize_space(str(product_json.get("image") or ""))
    if not cover_url:
        cover_url = meta_content(html_text, property_name="og:image")

    genres: list[str] = []
    for label in list(metadata.get("categories") or []) + parse_audible_chip_genres(html_text):
        cleaned = normalize_space(str(label))
        if cleaned and cleaned not in genres:
            genres.append(cleaned)

    product_id = normalize_space(str(product_json.get("productID") or ""))
    if not product_id:
        match = re.search(r"/pd/(?:[^/]+/)?([A-Z0-9]{10})(?:[/?#]|$)", final_url, re.I)
        product_id = match.group(1).upper() if match else ""

    return {
        "productId": product_id or normalized_key(title, ascii_only=True),
        "title": title,
        "author": author,
        "authorSource": author_source,
        "authorReliability": author_reliability,
        "summary": truncate_text(summary, 1200),
        "runtime": runtime,
        "year": year,
        "genres": genres[:4],
        "coverUrl": cover_url,
        "salePrice": sale_price,
        "listPrice": _parse_list_price(product_json, html_text),
        "memberHidden": member_hidden,
        "audibleUrl": final_url,
        "isbn": _parse_isbn_like(product_json, metadata, html_text, "isbn"),
        "isbn13": _parse_isbn_like(product_json, metadata, html_text, "isbn13"),
    }

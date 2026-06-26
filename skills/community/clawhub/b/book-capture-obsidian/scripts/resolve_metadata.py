#!/usr/bin/env python3
"""Resolve book metadata from ISBN using public APIs."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
from urllib.parse import quote_plus

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from common_config import get_env_csv, get_env_int, get_env_str
from common_isbn import normalize_isbn
from common_json import fail_and_print, make_result, print_json, read_json_file

STAGE = "resolve_metadata"


MetadataDict = Dict[str, Any]


def _get_requests_module():
    try:
        import requests  # type: ignore
    except Exception as exc:
        raise RuntimeError(f"requests library is required: {exc}")
    return requests


def _http_get_json(url: str, timeout_sec: int, user_agent: str) -> Dict[str, Any]:
    requests = _get_requests_module()
    response = requests.get(
        url,
        timeout=timeout_sec,
        headers={"User-Agent": user_agent, "Accept": "application/json"},
    )
    response.raise_for_status()
    data = response.json()
    if not isinstance(data, dict):
        raise ValueError(f"Expected JSON object from {url}")
    return data


def _clean_text(value: Any) -> Optional[str]:
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def _clean_str_list(values: Any) -> List[str]:
    if not isinstance(values, list):
        return []
    out: List[str] = []
    seen = set()
    for value in values:
        text = _clean_text(value)
        if text and text not in seen:
            seen.add(text)
            out.append(text)
    return out


def _best_google_cover(image_links: Any) -> Optional[str]:
    if not isinstance(image_links, dict):
        return None
    for key in ["extraLarge", "large", "medium", "small", "thumbnail", "smallThumbnail"]:
        value = image_links.get(key)
        if isinstance(value, str) and value.strip():
            url = value.replace("http://", "https://")
            if "google" in url and "zoom=1" in url:
                url = url.replace("zoom=1", "zoom=2")
            return url
    return None


def _normalize_metadata(raw: MetadataDict, source: str) -> MetadataDict:
    """Normalize provider-specific data to a stable metadata contract."""
    authors = _clean_str_list(raw.get("authors"))
    categories = _clean_str_list(raw.get("categories"))

    page_count = raw.get("page_count")
    if isinstance(page_count, bool):
        page_count = None
    if page_count is not None:
        try:
            page_count = int(page_count)
            if page_count < 1:
                page_count = None
        except (TypeError, ValueError):
            page_count = None

    metadata = {
        "authors": authors,
        "categories": categories,
        "cover_image": _clean_text(raw.get("cover_image")),
        "description": _clean_text(raw.get("description")),
        "language": _clean_text(raw.get("language")),
        "page_count": page_count,
        "published_date": _clean_text(raw.get("published_date")),
        "publisher": _clean_text(raw.get("publisher")),
        "source": source,
        "source_url": _clean_text(raw.get("source_url")),
        "title": _clean_text(raw.get("title")),
    }
    return metadata


def _from_google_books(isbn13: str, timeout_sec: int, user_agent: str) -> Tuple[Optional[MetadataDict], Optional[str]]:
    query = quote_plus(f"isbn:{isbn13}")
    url = f"https://www.googleapis.com/books/v1/volumes?q={query}&maxResults=1"
    try:
        payload = _http_get_json(url, timeout_sec=timeout_sec, user_agent=user_agent)
    except Exception as exc:
        return None, f"google_books request failed: {exc}"

    items = payload.get("items")
    if not isinstance(items, list) or not items:
        return None, "google_books returned no items"

    item0 = items[0] if isinstance(items[0], dict) else {}
    volume = item0.get("volumeInfo") if isinstance(item0.get("volumeInfo"), dict) else {}

    raw = {
        "title": volume.get("title"),
        "authors": volume.get("authors") or [],
        "publisher": volume.get("publisher"),
        "published_date": volume.get("publishedDate"),
        "description": volume.get("description"),
        "page_count": volume.get("pageCount"),
        "language": volume.get("language"),
        "categories": volume.get("categories") or [],
        "cover_image": _best_google_cover(volume.get("imageLinks")),
        "source_url": volume.get("infoLink"),
    }
    metadata = _normalize_metadata(raw, source="google_books")
    if not metadata.get("title"):
        return None, "google_books missing title"
    return metadata, None


def _from_openlibrary(isbn13: str, timeout_sec: int, user_agent: str) -> Tuple[Optional[MetadataDict], Optional[str]]:
    url = (
        "https://openlibrary.org/api/books"
        f"?bibkeys=ISBN:{isbn13}&format=json&jscmd=data"
    )
    try:
        payload = _http_get_json(url, timeout_sec=timeout_sec, user_agent=user_agent)
    except Exception as exc:
        return None, f"openlibrary request failed: {exc}"

    key = f"ISBN:{isbn13}"
    book = payload.get(key)
    if not isinstance(book, dict):
        return None, "openlibrary returned no entry"

    authors = []
    for item in book.get("authors", []):
        if isinstance(item, dict):
            name = _clean_text(item.get("name"))
            if name:
                authors.append(name)

    publishers = []
    for item in book.get("publishers", []):
        if isinstance(item, dict):
            name = _clean_text(item.get("name"))
            if name:
                publishers.append(name)

    subjects = []
    for item in book.get("subjects", []):
        if isinstance(item, dict):
            name = _clean_text(item.get("name"))
            if name:
                subjects.append(name)

    description = book.get("description")
    if isinstance(description, dict):
        description = description.get("value")

    # Enrich missing description/subjects from linked work metadata when available.
    works = book.get("works") if isinstance(book.get("works"), list) else []
    work_key = None
    for item in works:
        if isinstance(item, dict) and isinstance(item.get("key"), str):
            work_key = item.get("key")
            break

    if work_key and (not description or not subjects):
        work_url = f"https://openlibrary.org{work_key}.json" if work_key.startswith("/") else f"https://openlibrary.org/{work_key}.json"
        try:
            work_payload = _http_get_json(work_url, timeout_sec=timeout_sec, user_agent=user_agent)
        except Exception:
            work_payload = {}

        if not description:
            work_desc = work_payload.get("description")
            if isinstance(work_desc, dict):
                work_desc = work_desc.get("value")
            if _clean_text(work_desc):
                description = _clean_text(work_desc)

        if not subjects:
            work_subjects = work_payload.get("subjects")
            if isinstance(work_subjects, list):
                for value in work_subjects:
                    text = _clean_text(value)
                    if text:
                        subjects.append(text)

    raw = {
        "title": book.get("title"),
        "authors": authors,
        "publisher": ", ".join(publishers) if publishers else None,
        "published_date": book.get("publish_date"),
        "description": description,
        "page_count": book.get("number_of_pages"),
        "language": None,
        "categories": subjects,
        "cover_image": (book.get("cover") or {}).get("large")
        or (book.get("cover") or {}).get("medium")
        or (book.get("cover") or {}).get("small"),
        "source_url": (book.get("url") or "https://openlibrary.org") if isinstance(book.get("url"), str) else None,
    }
    metadata = _normalize_metadata(raw, source="openlibrary")
    if not metadata.get("title"):
        return None, "openlibrary missing title"
    return metadata, None


def resolve_book_metadata(isbn: str) -> dict:
    warnings: List[str] = []
    isbn13 = normalize_isbn(isbn or "")
    if not isbn13:
        return make_result(STAGE, ok=False, error=f"invalid ISBN value: {isbn}", isbn13=None, metadata=None, warnings=[])

    timeout_sec = get_env_int("BOOK_CAPTURE_HTTP_TIMEOUT_SECONDS", 12, minimum=1)
    user_agent = get_env_str("BOOK_CAPTURE_USER_AGENT", "book-capture-obsidian/1.0")
    providers = get_env_csv("BOOK_CAPTURE_METADATA_PROVIDER_ORDER", ["google_books", "openlibrary"])

    provider_map = {
        "google_books": _from_google_books,
        "openlibrary": _from_openlibrary,
    }

    for provider in providers:
        resolver = provider_map.get(provider)
        if resolver is None:
            warnings.append(f"unknown metadata provider skipped: {provider}")
            continue
        metadata, warn = resolver(isbn13=isbn13, timeout_sec=timeout_sec, user_agent=user_agent)
        if warn:
            warnings.append(warn)
        if metadata:
            return make_result(
                STAGE,
                ok=True,
                error=None,
                isbn13=isbn13,
                metadata=metadata,
                warnings=warnings,
            )

    return make_result(
        STAGE,
        ok=False,
        error="metadata not found in configured providers",
        isbn13=isbn13,
        metadata=None,
        warnings=warnings,
    )


def _isbn_from_extract_json(path: str) -> str:
    payload = read_json_file(path)
    isbn13 = payload.get("isbn13")
    if not isinstance(isbn13, str) or not isbn13.strip():
        raise ValueError(f"extract JSON does not include isbn13: {path}")
    return isbn13


def _self_check() -> dict:
    isbn13 = normalize_isbn("0-201-63361-2")
    ok = isbn13 == "9780201633610"
    return make_result(
        STAGE,
        ok=ok,
        error=None if ok else "isbn normalization self-check failed",
        checks={
            "normalized_isbn13": isbn13,
        },
    )


def main(argv: List[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--isbn", help="ISBN-10 or ISBN-13")
    parser.add_argument("--extract-json", help="Path to extract_isbn JSON output")
    parser.add_argument("--self-check", action="store_true", help="Run internal quick checks")
    args = parser.parse_args(argv)

    if args.self_check:
        result = _self_check()
        print_json(result)
        return 0 if result.get("ok") else 1

    isbn_value = args.isbn
    if args.extract_json:
        try:
            isbn_value = _isbn_from_extract_json(args.extract_json)
        except Exception as exc:
            return fail_and_print(STAGE, f"failed to read --extract-json: {exc}", isbn13=None, metadata=None)

    if not isbn_value:
        return fail_and_print(STAGE, "--isbn or --extract-json is required", isbn13=None, metadata=None)

    result = resolve_book_metadata(isbn_value)
    print_json(result)
    return 0 if result.get("ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())

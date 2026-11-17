#!/usr/bin/env python3
"""Shared, bounded Google Books client and response normalizer."""

from __future__ import annotations

import time
from datetime import timezone
from email.utils import parsedate_to_datetime
from typing import Any, Callable, Dict, List, Mapping, Optional, Tuple

from common_isbn import normalize_isbn

GOOGLE_BOOKS_URL = "https://www.googleapis.com/books/v1/volumes"
RATE_LIMIT_WARNING = "google books rate limit (429)"
QUOTA_WARNING = "google books quota limit (403)"
GOOGLE_BOOKS_FIELDS = (
    "items(id,volumeInfo(title,authors,publisher,publishedDate,description,"
    "pageCount,language,categories,imageLinks,infoLink,industryIdentifiers))"
)

MetadataDict = Dict[str, Any]
RequestGet = Callable[..., Any]
Sleep = Callable[[float], None]


def _get_requests_module():
    try:
        import requests  # type: ignore
    except Exception as exc:
        raise RuntimeError(f"requests library is required: {exc}")
    return requests


def _redact(value: Any, secret: str) -> Optional[str]:
    if value is None:
        return None
    text = str(value).strip()
    if not text:
        return None
    if secret:
        text = text.replace(secret, "[REDACTED]")
    return text or None


def _clean_str_list(values: Any, secret: str) -> List[str]:
    if not isinstance(values, list):
        return []
    out: List[str] = []
    seen = set()
    for value in values:
        text = _redact(value, secret)
        if text and text not in seen:
            seen.add(text)
            out.append(text)
    return out


def _best_cover(image_links: Any, secret: str) -> Optional[str]:
    if not isinstance(image_links, dict):
        return None
    for key in ["extraLarge", "large", "medium", "small", "thumbnail", "smallThumbnail"]:
        value = _redact(image_links.get(key), secret)
        if value:
            url = value.replace("http://", "https://")
            if "google" in url and "zoom=1" in url:
                url = url.replace("zoom=1", "zoom=2")
            return url
    return None


def _normalize_page_count(value: Any) -> Optional[int]:
    if value is None or isinstance(value, bool):
        return None
    try:
        page_count = int(value)
    except (TypeError, ValueError):
        return None
    return page_count if page_count > 0 else None


def _volume_isbns(volume: Mapping[str, Any]) -> Tuple[List[str], bool]:
    raw_identifiers = volume.get("industryIdentifiers")
    if not isinstance(raw_identifiers, list) or not raw_identifiers:
        return [], False

    normalized: List[str] = []
    for item in raw_identifiers:
        if not isinstance(item, dict):
            continue
        value = normalize_isbn(str(item.get("identifier") or ""))
        if value and value not in normalized:
            normalized.append(value)
    return normalized, True


def parse_google_books_response(
    payload: Any,
    requested_isbn: Optional[str] = None,
    secret: str = "",
) -> Tuple[Optional[MetadataDict], Optional[str], Optional[str]]:
    """Parse one partial Google Books response into the public metadata contract."""
    if not isinstance(payload, dict):
        return None, None, "google books returned an invalid response"

    items = payload.get("items")
    if not isinstance(items, list) or not items:
        return None, None, "google books returned no items"

    item = items[0] if isinstance(items[0], dict) else {}
    volume = item.get("volumeInfo") if isinstance(item.get("volumeInfo"), dict) else {}
    identifiers, identifiers_present = _volume_isbns(volume)

    expected_isbn = normalize_isbn(requested_isbn or "") if requested_isbn else None
    if expected_isbn and identifiers_present and expected_isbn not in identifiers:
        return None, identifiers[0] if identifiers else None, "google books returned a mismatching ISBN"

    metadata: MetadataDict = {
        "authors": _clean_str_list(volume.get("authors"), secret),
        "categories": _clean_str_list(volume.get("categories"), secret),
        "cover_image": _best_cover(volume.get("imageLinks"), secret),
        "description": _redact(volume.get("description"), secret),
        "language": _redact(volume.get("language"), secret),
        "page_count": _normalize_page_count(volume.get("pageCount")),
        "published_date": _redact(volume.get("publishedDate"), secret),
        "publisher": _redact(volume.get("publisher"), secret),
        "source": "google_books",
        "source_url": _redact(volume.get("infoLink"), secret),
        "title": _redact(volume.get("title"), secret),
    }
    if not metadata["title"]:
        return None, identifiers[0] if identifiers else None, "google books missing title"
    return metadata, identifiers[0] if identifiers else None, None


def _retry_after_seconds(response: Any, now: Callable[[], float]) -> Optional[float]:
    headers = getattr(response, "headers", {}) if response is not None else {}
    value = headers.get("Retry-After") if isinstance(headers, Mapping) else None
    if not isinstance(value, str):
        return None
    try:
        if value.strip().isdigit():
            return float(int(value.strip()))
        date = parsedate_to_datetime(value)
        if date.tzinfo is None:
            date = date.replace(tzinfo=timezone.utc)
        return max(0.0, date.timestamp() - now())
    except (ValueError, TypeError, OverflowError):
        return None


def _is_quota_error(response: Any) -> bool:
    try:
        payload = response.json()
    except Exception:
        return False
    error = payload.get("error") if isinstance(payload, dict) else None
    errors = error.get("errors") if isinstance(error, dict) else None
    reasons = ("dailyLimitExceeded", "quotaExceeded", "rateLimitExceeded", "userRateLimitExceeded")
    return isinstance(errors, list) and any(
        isinstance(item, dict) and item.get("reason") in reasons for item in errors
    )


def _retry_delay_seconds(
    response: Any,
    attempt: int,
    delay_ms: int,
    max_retry_after_sec: int,
    now: Callable[[], float] = time.time,
) -> float:
    retry_after = _retry_after_seconds(response, now)
    if retry_after is not None:
        return retry_after  # The server's minimum must not be shortened to our wait cap.
    exponential = (max(0, delay_ms) / 1000.0) * (2**attempt)
    return min(exponential, float(max_retry_after_sec))


def search_google_books(
    query: str,
    *,
    requested_isbn: Optional[str] = None,
    timeout_sec: int = 12,
    user_agent: str = "book-capture-obsidian/1.0",
    api_key: str = "",
    delay_ms: int = 400,
    max_retries: int = 2,
    max_retry_after_sec: int = 10,
    request_get: Optional[RequestGet] = None,
    sleep: Sleep = time.sleep,
    now: Callable[[], float] = time.time,
    on_defer: Optional[Callable[[float], None]] = None,
) -> Tuple[Optional[MetadataDict], Optional[str], Optional[str]]:
    """Bound retries; on_defer receives the server wait when a request is deferred."""
    clean_query = str(query or "").strip()
    if not clean_query:
        return None, None, "missing query for google books"

    if request_get is None:
        try:
            get = _get_requests_module().get
        except Exception:
            return None, None, "google books client unavailable"
    else:
        get = request_get
    clean_key = str(api_key or "").strip()
    params: Dict[str, Any] = {
        "q": clean_query,
        "maxResults": 1,
        "fields": GOOGLE_BOOKS_FIELDS,
    }
    if clean_key:
        params["key"] = clean_key

    retries = max(0, int(max_retries))
    retry_cap = max(0, int(max_retry_after_sec))
    headers = {"Accept": "application/json", "User-Agent": user_agent}

    for attempt in range(retries + 1):
        try:
            response = get(
                GOOGLE_BOOKS_URL,
                params=params,
                timeout=max(1, int(timeout_sec)),
                headers=headers,
            )
        except Exception:
            if attempt >= retries:
                return None, None, "google books request failed"
            sleep(_retry_delay_seconds(None, attempt, delay_ms, retry_cap))
            continue

        status_code = getattr(response, "status_code", None)
        if status_code == 403 and _is_quota_error(response):
            if on_defer is not None:
                on_defer(_retry_after_seconds(response, now) or 0.0)
            return None, None, QUOTA_WARNING

        if status_code == 429 or (isinstance(status_code, int) and 500 <= status_code <= 599):
            delay = _retry_delay_seconds(response, attempt, delay_ms, retry_cap, now)
            if attempt >= retries or delay > retry_cap:
                if on_defer is not None and (status_code == 429 or _retry_after_seconds(response, now) is not None):
                    on_defer(_retry_after_seconds(response, now) or 0.0)
                warning = RATE_LIMIT_WARNING if status_code == 429 else f"google books http {status_code}"
                return None, None, warning
            sleep(delay)
            continue

        if isinstance(status_code, int) and 400 <= status_code <= 499:
            return None, None, f"google books http {status_code}"

        if not isinstance(status_code, int) or not 200 <= status_code <= 299:
            return None, None, "google books returned an invalid HTTP status"

        try:
            payload = response.json()
        except Exception:
            return None, None, "google books returned invalid JSON"

        return parse_google_books_response(
            payload,
            requested_isbn=requested_isbn,
            secret=clean_key,
        )

    return None, None, "google books request failed"

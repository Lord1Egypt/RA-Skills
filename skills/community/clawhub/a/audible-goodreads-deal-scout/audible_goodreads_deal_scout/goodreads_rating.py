from __future__ import annotations

import hashlib
import html
import json
import re
import urllib.parse
import urllib.request
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any, Callable
from urllib.error import HTTPError, URLError

from .shared import normalize_space, parse_float, parse_int_value, write_json_atomic


GOODREADS_RATING_TTL_SECONDS = 7 * 24 * 60 * 60
GOODREADS_USER_AGENT = "OpenClaw Audible Goodreads Deal Scout/1.0"


class GoodreadsRatingError(RuntimeError):
    pass


def goodreads_book_url(book_id: str) -> str:
    return f"https://www.goodreads.com/book/show/{urllib.parse.quote(normalize_space(book_id))}"


def fetch_goodreads_text_with_final_url(url: str) -> tuple[str, str]:
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": GOODREADS_USER_AGENT,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            raw = response.read()
            return raw.decode("utf-8", "ignore"), str(response.geturl() or url)
    except (HTTPError, URLError) as exc:
        raise GoodreadsRatingError(f"Goodreads rating lookup failed for {url}: {exc}") from exc


def parse_goodreads_rating(html_text: str) -> dict[str, Any]:
    rating: float | None = None
    ratings_count: int | None = None
    for match in re.finditer(r'<script[^>]+type=["\']application/ld\+json["\'][^>]*>(.*?)</script>', html_text, re.I | re.S):
        try:
            payload = json.loads(html.unescape((match.group(1) or "").strip()))
        except Exception:
            continue
        candidates = payload if isinstance(payload, list) else [payload]
        for item in candidates:
            if not isinstance(item, dict):
                continue
            aggregate = item.get("aggregateRating") if isinstance(item.get("aggregateRating"), dict) else {}
            rating = rating if rating is not None else parse_float(aggregate.get("ratingValue"))
            ratings_count = ratings_count if ratings_count is not None else parse_int_value(aggregate.get("ratingCount") or aggregate.get("reviewCount"))
    if rating is None:
        for pattern in (
            r'itemprop=["\']ratingValue["\'][^>]+content=["\']([0-9.]+)["\']',
            r'"ratingValue"\s*:\s*"?([0-9.]+)"?',
            r'"average_rating"\s*:\s*"?([0-9.]+)"?',
        ):
            match = re.search(pattern, html_text, re.I)
            if match:
                rating = parse_float(match.group(1))
                break
    if ratings_count is None:
        for pattern in (
            r'"ratingCount"\s*:\s*"?([0-9,]+)"?',
            r'"ratings_count"\s*:\s*"?([0-9,]+)"?',
        ):
            match = re.search(pattern, html_text, re.I)
            if match:
                ratings_count = parse_int_value(match.group(1))
                break
    if rating is None:
        raise GoodreadsRatingError("Goodreads page did not expose an average rating.")
    return {
        "averageRating": rating,
        "ratingsCount": ratings_count,
        "source": "goodreads_public_page",
    }


def _cache_path(cache_dir: Path, book_id: str) -> Path:
    digest = hashlib.sha256(f"goodreads-rating-v1:{book_id}".encode("utf-8")).hexdigest()
    return cache_dir / f"{digest}.json"


def _read_cache(cache_dir: Path, book_id: str, *, no_cache: bool, refresh_cache: bool) -> dict[str, Any] | None:
    if no_cache or refresh_cache:
        return None
    path = _cache_path(cache_dir, book_id)
    if not path.exists():
        return None
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
        fetched_at = datetime.fromisoformat(str(payload.get("fetchedAt")))
    except Exception:
        return None
    if datetime.now(UTC) - fetched_at > timedelta(seconds=GOODREADS_RATING_TTL_SECONDS):
        return None
    payload["cacheHit"] = True
    return payload


def _write_cache(cache_dir: Path, book_id: str, payload: dict[str, Any], *, no_cache: bool) -> None:
    if no_cache:
        return
    write_json_atomic(_cache_path(cache_dir, book_id), {"fetchedAt": datetime.now(UTC).isoformat(), **payload})


def lookup_goodreads_rating(
    book_id: str,
    *,
    cache_dir: Path,
    refresh_cache: bool = False,
    no_cache: bool = False,
    fetcher: Callable[[str], tuple[str, str]] | None = None,
) -> dict[str, Any]:
    cleaned_book_id = normalize_space(book_id)
    if not cleaned_book_id:
        raise GoodreadsRatingError("Missing Goodreads book id.")
    cached = _read_cache(cache_dir, cleaned_book_id, no_cache=no_cache, refresh_cache=refresh_cache)
    if cached:
        return cached
    url = goodreads_book_url(cleaned_book_id)
    html_text, final_url = (fetcher or fetch_goodreads_text_with_final_url)(url)
    parsed = parse_goodreads_rating(html_text)
    payload = {**parsed, "url": final_url, "cacheHit": False}
    _write_cache(cache_dir, cleaned_book_id, payload, no_cache=no_cache)
    return payload

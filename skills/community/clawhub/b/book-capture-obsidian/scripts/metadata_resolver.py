#!/usr/bin/env python3
"""Ordered metadata providers with caching, request budgets and persisted backoff.

Use either provider alone or both in the selected order. Trusted input wins;
providers only fill missing fields. Google requests include pacing and retries.
"""

from __future__ import annotations

import difflib
import time
import unicodedata
from typing import Any, Callable, Dict, List, Optional, Tuple
from urllib.parse import quote

from common_config import get_env_csv, get_env_int, get_env_str
from common_isbn import normalize_isbn
from google_books import QUOTA_WARNING, RATE_LIMIT_WARNING, search_google_books
from metadata_cache import MetadataCache, default_cache_path

MetadataDict = Dict[str, Any]
RequestGet = Callable[..., Any]
Sleep = Callable[[float], None]
Now = Callable[[], float]

DEFAULT_USER_AGENT = (
    "book-capture-obsidian/1.4 (+https://github.com/Ricardodpalmeida/book-capture-obsidian-skill)"
)
DEFAULT_PROVIDERS = ["openlibrary", "google_books"]
OPENLIBRARY = "openlibrary"
GOOGLE = "google_books"

# A lookup stops once these are filled; later providers only fill gaps.
WANTED_FIELDS = ("title", "authors", "description", "cover_image")
FILLABLE_FIELDS = (
    "authors",
    "categories",
    "cover_image",
    "description",
    "language",
    "page_count",
    "published_date",
    "publisher",
    "source_url",
    "title",
)

FOUND_TTL_DAYS = 180
NOT_FOUND_TTL_DAYS = 14


def _empty(value: Any) -> bool:
    return value is None or value == "" or value == []


def _clean_text(value: Any) -> Optional[str]:
    if value is None:
        return None
    # Open Library descriptions use CRLF; a stray \r makes every re-run
    # rewrite the note because read_text() folds it away on the way back.
    text = str(value).replace("\r\n", "\n").replace("\r", "\n").strip()
    return text or None


def _clean_str_list(values: Any) -> List[str]:
    if not isinstance(values, list):
        return []
    out: List[str] = []
    for value in values:
        text = _clean_text(value)
        if text and text not in out:
            out.append(text)
    return out


def _normalize_page_count(value: Any) -> Optional[int]:
    if value is None or isinstance(value, bool):
        return None
    try:
        count = int(value)
    except (TypeError, ValueError):
        return None
    return count if count > 0 else None


def _query_key(title: str, author: str) -> str:
    def norm(text: str) -> str:
        text = unicodedata.normalize("NFKD", text or "").encode("ascii", "ignore").decode("ascii")
        return " ".join(text.lower().split())

    return f"{norm(title)}|{norm(author)}"


def _fold(text: str) -> str:
    text = unicodedata.normalize("NFKD", text or "").encode("ascii", "ignore").decode("ascii").lower()
    return " ".join("".join(c if c.isalnum() else " " for c in text).split())


def _main_title(title: str) -> str:
    """Title without subtitle or series note: 'Dune: Deluxe (Book 1)' -> 'dune'."""
    for sep in (":", " (", " - ", ";"):
        if sep in title:
            title = title.split(sep, 1)[0]
    return _fold(title)


def title_matches(query: str, candidate: str) -> bool:
    q, c = _main_title(query), _main_title(candidate)
    if not q or not c:
        return False
    return q == c or difflib.SequenceMatcher(None, q, c).ratio() >= 0.85


def author_matches(query: str, candidates: List[str]) -> bool:
    """True when any significant name token of ``query`` appears in a candidate author."""
    wanted = {t for t in _fold(query).split() if len(t) >= 3}
    if not wanted:
        return True
    return any(wanted & set(_fold(name).split()) for name in candidates)


def is_complete(metadata: Optional[MetadataDict]) -> bool:
    return bool(metadata) and all(not _empty(metadata.get(field)) for field in WANTED_FIELDS)


def merge_missing(primary: MetadataDict, extra: MetadataDict) -> MetadataDict:
    """Fill empty fields of ``primary`` from ``extra`` without overwriting."""
    merged = dict(primary)
    for field in FILLABLE_FIELDS:
        if _empty(merged.get(field)) and not _empty(extra.get(field)):
            merged[field] = extra[field]
    return merged


class ResolverStats:
    def __init__(self) -> None:
        self.cache_hits = 0
        self.network_calls: Dict[str, int] = {OPENLIBRARY: 0, GOOGLE: 0}
        self.google_skipped_cooldown = 0
        self.google_skipped_budget = 0
        self.rate_limited: Dict[str, int] = {OPENLIBRARY: 0, GOOGLE: 0}

    def as_dict(self) -> Dict[str, Any]:
        return {
            "cache_hits": self.cache_hits,
            "network_calls": dict(self.network_calls),
            "google_skipped_cooldown": self.google_skipped_cooldown,
            "google_skipped_budget": self.google_skipped_budget,
            "rate_limited": dict(self.rate_limited),
        }


class MetadataResolver:
    def __init__(
        self,
        *,
        providers: Optional[List[str]] = None,
        cache: Optional[MetadataCache] = None,
        google_api_key: str = "",
        google_budget: int = 100,
        google_cooldown_sec: int = 3600,
        google_delay_ms: int = 400,
        google_min_interval_ms: int = 1000,
        google_max_retries: int = 2,
        google_max_retry_after_sec: int = 10,
        openlibrary_delay_ms: int = 1000,
        openlibrary_cooldown_sec: int = 600,
        timeout_sec: int = 12,
        user_agent: str = DEFAULT_USER_AGENT,
        request_get: Optional[RequestGet] = None,
        sleep: Sleep = time.sleep,
        now: Now = time.time,
    ) -> None:
        self.providers = list(providers or DEFAULT_PROVIDERS)
        self.cache = cache if cache is not None else MetadataCache(None, now=now)
        self.google_api_key = google_api_key
        self.google_budget = max(0, int(google_budget))
        self.google_cooldown_sec = max(0, int(google_cooldown_sec))
        self.google_delay_ms = google_delay_ms
        self.google_min_interval_ms = max(0, int(google_min_interval_ms))
        self.google_max_retries = google_max_retries
        self.google_max_retry_after_sec = google_max_retry_after_sec
        self.openlibrary_delay_ms = max(0, int(openlibrary_delay_ms))
        self.openlibrary_cooldown_sec = max(0, int(openlibrary_cooldown_sec))
        self.timeout_sec = max(1, int(timeout_sec))
        self.user_agent = user_agent
        self._request_get = request_get
        self._sleep = sleep
        self._now = now
        self._last_openlibrary_call = 0.0
        self._last_google_call: Optional[float] = None
        self.stats = ResolverStats()

    @classmethod
    def from_env(cls, **overrides: Any) -> "MetadataResolver":
        settings: Dict[str, Any] = {
            "providers": get_env_csv("BOOK_CAPTURE_METADATA_PROVIDER_ORDER", DEFAULT_PROVIDERS),
            "cache": MetadataCache(default_cache_path()),
            "google_api_key": get_env_str("BOOK_CAPTURE_GOOGLE_API_KEY", ""),
            "google_budget": get_env_int("BOOK_CAPTURE_GOOGLE_MAX_REQUESTS_PER_RUN", 100, minimum=0),
            "google_cooldown_sec": get_env_int("BOOK_CAPTURE_GOOGLE_COOLDOWN_SECONDS", 3600, minimum=0),
            "google_delay_ms": get_env_int("BOOK_CAPTURE_GOOGLE_DELAY_MS", 400, minimum=0),
            "google_min_interval_ms": get_env_int("BOOK_CAPTURE_GOOGLE_MIN_INTERVAL_MS", 1000, minimum=0),
            "google_max_retries": get_env_int("BOOK_CAPTURE_GOOGLE_MAX_RETRIES", 2, minimum=0),
            "google_max_retry_after_sec": get_env_int(
                "BOOK_CAPTURE_GOOGLE_MAX_RETRY_AFTER_SECONDS", 10, minimum=0
            ),
            "openlibrary_delay_ms": get_env_int("BOOK_CAPTURE_OPENLIBRARY_DELAY_MS", 1000, minimum=0),
            "timeout_sec": get_env_int("BOOK_CAPTURE_HTTP_TIMEOUT_SECONDS", 12, minimum=1),
            "user_agent": get_env_str("BOOK_CAPTURE_USER_AGENT", DEFAULT_USER_AGENT),
        }
        settings.update(overrides)
        return cls(**settings)

    # ------------------------------------------------------------------ public

    def lookup(
        self,
        *,
        isbn13: Optional[str] = None,
        title: str = "",
        author: str = "",
        base: Optional[MetadataDict] = None,
    ) -> Tuple[Optional[MetadataDict], Optional[str], List[str]]:
        """Return (metadata, isbn13, warnings).

        ``base`` holds fields the caller already trusts (for example a Goodreads
        row); providers only fill what it is missing and never overwrite it.
        """
        warnings: List[str] = []
        isbn = normalize_isbn(isbn13 or "") if isbn13 else None
        merged: Optional[MetadataDict] = dict(base) if base else None

        for provider in self.providers:
            if is_complete(merged):
                break
            if provider not in (OPENLIBRARY, GOOGLE):
                warnings.append(f"unknown metadata provider skipped: {provider}")
                continue
            found, found_isbn, warning = self._lookup_provider(provider, isbn, title, author)
            if warning:
                warnings.append(warning)
            if not found and isbn and title and provider == OPENLIBRARY:
                # Many editions (often non-English ones) have no Open Library
                # ISBN record although the work is there; try its rate-limited
                # title search before Google.
                found, _ignored, warning = self._lookup_provider(provider, None, title, author)
                if warning:
                    warnings.append(warning)
            if not found:
                continue
            if not isbn and found_isbn:
                isbn = found_isbn
            merged = merge_missing(merged, found) if merged else dict(found)

        if merged and not _clean_text(merged.get("title")):
            merged = None
        return merged, isbn, warnings

    # ---------------------------------------------------------------- internal

    def _get(self) -> RequestGet:
        if self._request_get is None:
            import requests  # type: ignore

            self._request_get = requests.get
        return self._request_get

    def _lookup_provider(
        self, provider: str, isbn: Optional[str], title: str, author: str
    ) -> Tuple[Optional[MetadataDict], Optional[str], Optional[str]]:
        if isbn:
            key = f"{provider}:isbn:{isbn}"
        elif title:
            key = f"{provider}:q:{_query_key(title, author)}"
        else:
            return None, None, None

        cached = self.cache.get(key)
        if cached is not None:
            self.stats.cache_hits += 1
            return cached.get("metadata"), cached.get("isbn13"), None

        cooldown = self.cache.cooldown_until(provider)
        if cooldown:
            if provider == GOOGLE:
                self.stats.google_skipped_cooldown += 1
            return None, None, f"{provider} skipped: cooling down after API backoff or quota"

        if provider == GOOGLE:
            if self.stats.network_calls[GOOGLE] >= self.google_budget:
                self.stats.google_skipped_budget += 1
                return None, None, "google_books skipped: per-run request budget reached"
            metadata, found_isbn, warning, cacheable = self._google(isbn, title, author)
        else:
            metadata, found_isbn, warning, cacheable = self._openlibrary(isbn, title, author)

        if cacheable:
            ttl = FOUND_TTL_DAYS if metadata else NOT_FOUND_TTL_DAYS
            self.cache.put(key, {"metadata": metadata, "isbn13": found_isbn}, ttl)
        return metadata, found_isbn, warning

    # Google Books ------------------------------------------------------------

    def _google(
        self, isbn: Optional[str], title: str, author: str
    ) -> Tuple[Optional[MetadataDict], Optional[str], Optional[str], bool]:
        if isbn:
            query = f"isbn:{isbn}"
        else:
            parts = [f"intitle:{title}"] if title else []
            if author:
                parts.append(f"inauthor:{author}")
            query = " ".join(parts)
        remaining = self.google_budget - self.stats.network_calls[GOOGLE]

        defer_for: Optional[float] = None

        def deferred(seconds: float) -> None:
            nonlocal defer_for
            defer_for = seconds

        def counted_get(*args: Any, **kwargs: Any) -> Any:
            if self._last_google_call is not None:
                wait = self._last_google_call + self.google_min_interval_ms / 1000.0 - self._now()
                if wait > 0:
                    self._sleep(wait)
            self._last_google_call = self._now()
            self.stats.network_calls[GOOGLE] += 1
            return self._get()(*args, **kwargs)

        key = self.google_api_key
        metadata, found_isbn, warning = search_google_books(
            query,
            requested_isbn=isbn,
            timeout_sec=self.timeout_sec,
            user_agent=self.user_agent,
            api_key=key,
            delay_ms=self.google_delay_ms,
            max_retries=min(max(0, self.google_max_retries), remaining - 1),
            max_retry_after_sec=self.google_max_retry_after_sec,
            request_get=counted_get,
            sleep=self._sleep,
            now=self._now,
            on_defer=deferred,
        )
        if warning in (RATE_LIMIT_WARNING, QUOTA_WARNING):
            self.stats.rate_limited[GOOGLE] += 1
            defer_for = max(defer_for or 0.0, self.google_cooldown_sec)
        if defer_for is not None and defer_for > 0:
            self.cache.set_cooldown(GOOGLE, defer_for, warning or "server backoff")
            return None, None, f"{warning}; Google Books paused for {defer_for:g} seconds", False
        if metadata and not isbn:
            # Title searches get the same guard as Open Library, and the
            # edition ISBN is not adopted (it may belong to any edition).
            if not title_matches(title, metadata.get("title") or "") or (
                author and not author_matches(author, metadata.get("authors") or [])
            ):
                return None, None, "google books found no close title/author match", True
            return metadata, None, None, True
        if metadata:
            return metadata, found_isbn, None, True
        # "no items" and ISBN mismatches are stable answers worth caching;
        # transport errors and 5xx are not.
        stable = warning in {
            "google books returned no items",
            "google books returned a mismatching ISBN",
            "google books missing title",
        }
        return None, None, warning, stable

    # Open Library -----------------------------------------------------------

    def _ol_get_json(self, url: str) -> Tuple[Optional[Dict[str, Any]], Optional[int]]:
        wait = self._last_openlibrary_call + self.openlibrary_delay_ms / 1000.0 - self._now()
        if wait > 0:
            self._sleep(wait)
        self._last_openlibrary_call = self._now()
        self.stats.network_calls[OPENLIBRARY] += 1
        response = self._get()(
            url,
            timeout=self.timeout_sec,
            headers={"User-Agent": self.user_agent, "Accept": "application/json"},
        )
        status = getattr(response, "status_code", None)
        if status != 200:
            return None, status
        data = response.json()
        return (data if isinstance(data, dict) else None), status

    def _openlibrary(
        self, isbn: Optional[str], title: str, author: str
    ) -> Tuple[Optional[MetadataDict], Optional[str], Optional[str], bool]:
        try:
            if isbn:
                return self._openlibrary_isbn(isbn)
            return self._openlibrary_search(title, author)
        except _RateLimited:
            self.stats.rate_limited[OPENLIBRARY] += 1
            self.cache.set_cooldown(OPENLIBRARY, self.openlibrary_cooldown_sec, "http 429")
            return None, None, "openlibrary rate limit (429); paused", False
        except Exception:
            return None, None, "openlibrary request failed", False

    def _ol_checked(self, url: str) -> Optional[Dict[str, Any]]:
        data, status = self._ol_get_json(url)
        if status == 429:
            raise _RateLimited()
        if status is None or status >= 500:
            raise RuntimeError(f"openlibrary http {status}")
        return data

    def _openlibrary_work(self, work_key: Optional[str]) -> Dict[str, Any]:
        if not work_key:
            return {}
        path = work_key if work_key.startswith("/") else f"/{work_key}"
        try:
            return self._ol_checked(f"https://openlibrary.org{path}.json") or {}
        except _RateLimited:
            raise
        except Exception:
            return {}

    def _openlibrary_isbn(self, isbn: str) -> Tuple[Optional[MetadataDict], Optional[str], Optional[str], bool]:
        payload = self._ol_checked(
            f"https://openlibrary.org/api/books?bibkeys=ISBN:{isbn}&format=json&jscmd=data"
        )
        book = (payload or {}).get(f"ISBN:{isbn}")
        if not isinstance(book, dict):
            return None, None, "openlibrary returned no entry", True

        def names(items: Any) -> List[str]:
            return _clean_str_list([i.get("name") for i in items or [] if isinstance(i, dict)])

        description = book.get("description")
        if isinstance(description, dict):
            description = description.get("value")
        subjects = names(book.get("subjects"))

        if not _clean_text(description) or not subjects:
            # jscmd=data omits the work link, so read it from the edition record.
            works = book.get("works")
            if not works and isinstance(book.get("key"), str) and book["key"].startswith("/books/"):
                edition = self._openlibrary_work(book["key"])
                works = edition.get("works")
                if not _clean_text(description):
                    description = edition.get("description")
                    if isinstance(description, dict):
                        description = description.get("value")
            work_key = None
            for item in works or []:
                if isinstance(item, dict) and isinstance(item.get("key"), str):
                    work_key = item["key"]
                    break
            work = self._openlibrary_work(work_key) if work_key and (not _clean_text(description) or not subjects) else {}
            if not _clean_text(description):
                work_desc = work.get("description")
                description = work_desc.get("value") if isinstance(work_desc, dict) else work_desc
            if not subjects:
                subjects = _clean_str_list(work.get("subjects"))

        cover = book.get("cover") if isinstance(book.get("cover"), dict) else {}
        publishers = names(book.get("publishers"))
        metadata = {
            "authors": names(book.get("authors")),
            "categories": subjects[:10],
            "cover_image": _clean_text(cover.get("large") or cover.get("medium") or cover.get("small")),
            "description": _clean_text(description),
            "language": None,
            "page_count": _normalize_page_count(book.get("number_of_pages")),
            "published_date": _clean_text(book.get("publish_date")),
            "publisher": ", ".join(publishers) if publishers else None,
            "source": OPENLIBRARY,
            "source_url": _clean_text(book.get("url")),
            "title": _clean_text(book.get("title")),
        }
        if not metadata["title"]:
            return None, None, "openlibrary missing title", True
        return metadata, isbn, None, True

    def _openlibrary_search(
        self, title: str, author: str
    ) -> Tuple[Optional[MetadataDict], Optional[str], Optional[str], bool]:
        if not title:
            return None, None, None, False
        # The search doc lists ISBNs of every edition, so none is adopted here:
        # a wrong edition ISBN would break deduplication.
        fields = "key,title,author_name,first_publish_year,cover_i,subject,number_of_pages_median"
        url = f"https://openlibrary.org/search.json?title={quote(title)}&limit=5&fields={fields}"
        if author:
            url += f"&author={quote(author)}"
        payload = self._ol_checked(url)
        docs = (payload or {}).get("docs")
        if not isinstance(docs, list) or not docs:
            return None, None, "openlibrary search returned no match", True
        # Search ranking is loose (a title query can return a sequel or an
        # unrelated book with the same title), so only accept a doc whose
        # title and author both match what was asked for.
        doc = next(
            (
                d for d in docs
                if isinstance(d, dict)
                and title_matches(title, str(d.get("title") or ""))
                and (not author or author_matches(author, _clean_str_list(d.get("author_name"))))
            ),
            None,
        )
        if doc is None:
            return None, None, "openlibrary search found no close title/author match", True

        work = self._openlibrary_work(doc.get("key"))
        work_desc = work.get("description")
        description = work_desc.get("value") if isinstance(work_desc, dict) else work_desc
        cover_id = doc.get("cover_i")
        year = doc.get("first_publish_year")
        key = _clean_text(doc.get("key"))
        metadata = {
            "authors": _clean_str_list(doc.get("author_name")),
            "categories": _clean_str_list(doc.get("subject"))[:10],
            "cover_image": f"https://covers.openlibrary.org/b/id/{cover_id}-L.jpg" if cover_id else None,
            "description": _clean_text(description),
            "language": None,
            "page_count": _normalize_page_count(doc.get("number_of_pages_median")),
            "published_date": str(year) if year else None,
            # A work groups every edition, so its publisher list says nothing
            # about the user's copy.
            "publisher": None,
            "source": OPENLIBRARY,
            "source_url": f"https://openlibrary.org{key}" if key else None,
            "title": _clean_text(doc.get("title")),
        }
        if not metadata["title"]:
            return None, None, "openlibrary search missing title", True
        return metadata, None, None, True


class _RateLimited(Exception):
    pass

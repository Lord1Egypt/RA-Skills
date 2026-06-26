from __future__ import annotations

import hashlib
import html
import json
import random
import re
import time
import urllib.parse
import urllib.request
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any, Callable
from urllib.error import HTTPError, URLError

from .audible_fetch import AudibleBlockedError, AudibleFetchError, decode_response_bytes, validate_audible_fetch_url
from .constants import AUDIBLE_BLOCK_MARKERS, PROMOTION_MARKERS
from .shared import (
    normalize_author_key,
    normalize_space,
    normalized_key,
    parse_localized_price,
    strip_html,
    write_json_atomic,
)


PARSER_VERSION = "want-to-read-v1"
USD_SEARCH_BASE_URL = "https://www.audible.com/search"
CATALOG_USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
)
BLOCK_FAILURE_TTL_SECONDS = 30 * 60
ORDINARY_FAILURE_TTL_SECONDS = 30 * 60
PRODUCT_TTL_SECONDS = 6 * 60 * 60
SEARCH_TTL_SECONDS = 24 * 60 * 60
PRICE_CONTEXT_RADIUS = 32
IGNORED_PRICE_CONTEXT_MARKERS = (
    "kindle",
    "ebook",
    "e-book",
    "paperback",
    "hardcover",
    "mass market",
    "print",
)
EXTRA_PROMOTION_MARKERS = (
    "sale price",
    "deal price",
    "limited time",
    "limited-time",
    "promotion",
)


class RequestBudgetExceeded(RuntimeError):
    pass


def fetch_catalog_text_with_final_url(url: str, *, allow_unsafe_url: bool = False) -> tuple[str, str]:
    url = validate_audible_fetch_url(url, allow_unsafe_url=allow_unsafe_url)
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": CATALOG_USER_AGENT,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "en-US,en;q=0.9",
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            raw = response.read()
            text = decode_response_bytes(raw, str(response.headers.get("Content-Encoding") or ""))
            lowered = text.lower()
            if any(marker in lowered for marker in AUDIBLE_BLOCK_MARKERS):
                raise AudibleBlockedError(f"Audible blocked the request for {url}.")
            return text, str(response.geturl() or url)
    except HTTPError as exc:
        if exc.code in {403, 429}:
            raise AudibleBlockedError(f"Audible request blocked with HTTP {exc.code}.") from exc
        raise AudibleFetchError(f"Audible request failed for {url}: {exc}") from exc
    except URLError as exc:
        raise AudibleFetchError(f"Audible request failed for {url}: {exc}") from exc


def utc_now() -> datetime:
    return datetime.now(UTC)


def canonical_audible_url(url: str) -> str:
    parsed = urllib.parse.urlparse(url)
    if not parsed.netloc:
        parsed = urllib.parse.urlparse(urllib.parse.urljoin("https://www.audible.com", url))
    return urllib.parse.urlunparse((parsed.scheme or "https", parsed.netloc, parsed.path.rstrip("/"), "", "", ""))


def audible_product_id(url: str) -> str:
    match = re.search(r"/pd/(?:[^/?#]+/)?([A-Z0-9]{10})", url)
    return match.group(1) if match else ""


def build_search_url(title: str, author: str) -> str:
    query = normalize_space(f"{title} {author}")
    return USD_SEARCH_BASE_URL + "?" + urllib.parse.urlencode({"keywords": query})


def strip_title_subtitle(value: str) -> str:
    text = normalize_space(value)
    text = re.sub(r"\b(?:book|volume|vol\.?)\s*#?\s*\d+\b", " ", text, flags=re.I)
    text = re.sub(r"\b(?:series|trilogy|saga)\b.*$", " ", text, flags=re.I)
    if ":" in text:
        text = text.split(":", 1)[0]
    return normalize_space(text)


def normalized_title_variants(value: str) -> set[str]:
    variants = {
        normalized_key(value, ascii_only=True),
        normalized_key(strip_title_subtitle(value), ascii_only=True),
    }
    cleaned: set[str] = set()
    for item in variants:
        tokens = item.split()
        if tokens and tokens[0] in {"a", "an", "the"}:
            cleaned.add(" ".join(tokens[1:]))
        cleaned.add(item)
    return {item for item in cleaned if item}


def strong_author_match(goodreads_author: str, audible_author: str) -> bool:
    expected = normalize_author_key(goodreads_author, ascii_only=True)
    actual = normalize_author_key(audible_author, ascii_only=True)
    if not expected or not actual:
        return False
    if expected == actual:
        return True
    expected_tokens = expected.split()
    actual_tokens = actual.split()
    if not expected_tokens or not actual_tokens:
        return False
    if expected_tokens[-1] != actual_tokens[-1]:
        return False
    expected_without_initials = [token for token in expected_tokens if len(token) > 1]
    actual_without_initials = [token for token in actual_tokens if len(token) > 1]
    return bool(expected_without_initials and set(expected_without_initials).issubset(set(actual_without_initials)))


def strong_title_match(goodreads_title: str, audible_title: str) -> bool:
    expected = normalized_title_variants(goodreads_title)
    actual = normalized_title_variants(audible_title)
    return bool(expected and actual and expected & actual)


def format_warnings(text: str) -> list[str]:
    lowered = text.casefold()
    warnings: list[str] = []
    patterns = {
        "abridged": r"\babridged\b",
        "dramatized": r"\bdramatized\b",
        "adaptation": r"\badaptation\b",
        "course": r"\bcourse\b",
        "omnibus": r"\bomnibus\b",
    }
    for marker, pattern in patterns.items():
        if re.search(pattern, lowered):
            warnings.append(marker)
    return warnings


def hidden_price_status(text: str) -> str | None:
    lowered = text.casefold()
    if "included with membership" in lowered or "plus catalog" in lowered:
        return "included_with_membership"
    hidden_markers = (
        "buy with 1 credit",
        "1 credit",
        "member price",
        "member only",
        "more buying choices",
        "more purchase options",
        "log in to redeem",
    )
    if any(marker in lowered for marker in hidden_markers):
        return "price_hidden"
    return None


def _price_values_near(text: str) -> list[float]:
    values: list[float] = []
    for match in re.finditer(r"(?:US)?[$]\s*\d[\d.,]*", text, flags=re.I):
        context = text[max(0, match.start() - PRICE_CONTEXT_RADIUS) : min(len(text), match.end() + PRICE_CONTEXT_RADIUS)].casefold()
        if any(marker in context for marker in IGNORED_PRICE_CONTEXT_MARKERS):
            continue
        price = parse_localized_price(match.group(0))
        if price is not None:
            values.append(price)
    return values


def parse_offer_text(html_text: str) -> dict[str, Any]:
    plain_text = strip_html(html_text)
    hidden_status = hidden_price_status(plain_text)
    list_price: float | None = None
    current_price: float | None = None
    for pattern in (
        r"(?:regular|list)\s+price\s*:?\s*((?:US)?[$]\s*\d[\d.,]*)",
        r"(?:was|before)\s*:?\s*((?:US)?[$]\s*\d[\d.,]*)",
    ):
        for match in re.finditer(pattern, strip_html(html_text), flags=re.I):
            cleaned_text = strip_html(html_text)
            context = cleaned_text[max(0, match.start() - PRICE_CONTEXT_RADIUS) : min(len(cleaned_text), match.end() + PRICE_CONTEXT_RADIUS)].casefold()
            if any(marker in context for marker in IGNORED_PRICE_CONTEXT_MARKERS):
                continue
            list_price = parse_localized_price(match.group(1))
            break
        if list_price is not None:
            break
    for strike in re.finditer(r"<(?:s|del|strike)\b[^>]*>(.*?)</(?:s|del|strike)>", html_text, flags=re.I | re.S):
        context = strip_html(html_text[max(0, strike.start() - PRICE_CONTEXT_RADIUS) : min(len(html_text), strike.end() + PRICE_CONTEXT_RADIUS)]).casefold()
        if any(marker in context for marker in IGNORED_PRICE_CONTEXT_MARKERS):
            continue
        if list_price is None:
            list_price = parse_localized_price(strip_html(strike.group(1)))
            break
    all_prices = _price_values_near(plain_text)
    if list_price is not None:
        lower_prices = [price for price in all_prices if price < list_price]
        if lower_prices:
            current_price = min(lower_prices)
        else:
            non_list_prices = [price for price in all_prices if price != list_price]
            if non_list_prices:
                current_price = non_list_prices[0]
            elif len(all_prices) > 1:
                current_price = all_prices[-1]
    elif all_prices:
        current_price = all_prices[0]
    discount_percent = None
    if current_price is not None and list_price is not None and list_price > 0 and current_price < list_price:
        discount_percent = max(0, round((1 - current_price / list_price) * 100))
    price_basis, deal_type = classify_price_semantics(
        plain_text,
        current_price=current_price,
        list_price=list_price,
        discount_percent=discount_percent,
        hidden_status=hidden_status,
        basis_when_numeric="audible_public_cash",
    )
    return {
        "currencyCode": "USD",
        "currentPrice": current_price,
        "listPrice": list_price,
        "discountPercent": discount_percent,
        "priceBasis": price_basis,
        "dealType": deal_type,
        "hiddenStatus": hidden_status,
        "hasNumericDiscountHint": current_price is not None and list_price is not None,
    }


def has_limited_time_signal(text: str) -> bool:
    lowered = text.casefold()
    return any(marker in lowered for marker in PROMOTION_MARKERS + EXTRA_PROMOTION_MARKERS)


def classify_price_semantics(
    text: str,
    *,
    current_price: float | None,
    list_price: float | None,
    discount_percent: int | None,
    hidden_status: str | None,
    basis_when_numeric: str,
) -> tuple[str, str]:
    if hidden_status == "included_with_membership":
        return "audible_membership", "included_with_membership"
    if hidden_status == "price_hidden":
        return "audible_credit_or_membership", "hidden_price"
    if discount_percent is not None and current_price is not None and list_price is not None:
        if has_limited_time_signal(text):
            return basis_when_numeric, "limited_time_sale"
        return basis_when_numeric, "cash_price_below_list"
    if current_price is not None or list_price is not None:
        return basis_when_numeric, "none"
    return "unknown", "unknown"


def unknown_offer() -> dict[str, Any]:
    return {
        "currencyCode": "USD",
        "currentPrice": None,
        "listPrice": None,
        "discountPercent": None,
        "priceBasis": "unknown",
        "dealType": "unknown",
    }


def _anchor_title_for_href(block: str, href: str) -> str:
    escaped = re.escape(href)
    match = re.search(rf'<a[^>]+href=["\']{escaped}["\'][^>]*>(.*?)</a>', block, flags=re.I | re.S)
    if match:
        anchor_text = normalize_space(strip_html(match.group(1)))
        if anchor_text:
            return anchor_text
    title_match = re.search(r"<h[1-4][^>]*>(.*?)</h[1-4]>", block, flags=re.I | re.S)
    return normalize_space(strip_html(title_match.group(1) if title_match else ""))


def _author_from_block(block: str) -> str:
    patterns = (
        r"By:\s*</?[^>]*>\s*<a[^>]*>(.*?)</a>",
        r"By:\s*<a[^>]*>(.*?)</a>",
        r"By:\s*([^<\n]+)",
    )
    for pattern in patterns:
        match = re.search(pattern, block, flags=re.I | re.S)
        if match:
            return normalize_space(strip_html(match.group(1)))
    return ""


def parse_search_cards(html_text: str, base_url: str = "https://www.audible.com") -> list[dict[str, Any]]:
    cards: list[dict[str, Any]] = []
    seen: set[str] = set()
    for match in re.finditer(r'href=["\']([^"\']*/pd/[^"\']+)["\']', html_text, flags=re.I):
        raw_href = html.unescape(match.group(1))
        url = canonical_audible_url(urllib.parse.urljoin(base_url, raw_href))
        if url in seen:
            continue
        seen.add(url)
        product_marker = html_text.rfind("productListItem", 0, match.start())
        product_start = html_text.rfind("<li", 0, product_marker) if product_marker >= 0 else -1
        next_product = re.search(r'<li[^>]+class=["\'][^"\']*productListItem', html_text[match.end() :], flags=re.I | re.S)
        if product_start >= 0:
            product_end = match.end() + next_product.start() if next_product else min(len(html_text), match.end() + 15_000)
            block = html_text[product_start:product_end]
        else:
            start = max(0, match.start() - 2500)
            end = min(len(html_text), match.end() + 7500)
            block = html_text[start:end]
        title = _anchor_title_for_href(block, raw_href)
        author = _author_from_block(block)
        offer = parse_offer_text(block)
        warnings = format_warnings(strip_html(block))
        cards.append(
            {
                "title": title,
                "author": author,
                "url": url,
                "productId": audible_product_id(url),
                "offer": offer,
                "warnings": warnings,
                "rawText": normalize_space(strip_html(block))[:800],
            }
        )
    return cards


def validate_candidate(book: dict[str, Any], card: dict[str, Any]) -> tuple[str, str]:
    title = normalize_space(str(card.get("title") or ""))
    author = normalize_space(str(card.get("author") or ""))
    if not title:
        return "reject", "missing Audible title"
    if not strong_title_match(str(book.get("title") or ""), title):
        return "reject", "title mismatch"
    if not author:
        return "needs_review", "Audible search card did not expose an author"
    if strong_author_match(str(book.get("author") or ""), author):
        return "matched", "title and author matched"
    return "needs_review", "title matched but author did not"


class AudibleCatalogClient:
    def __init__(
        self,
        *,
        cache_dir: Path,
        max_requests: int = 40,
        request_delay: float = 1.0,
        refresh_cache: bool = False,
        no_cache: bool = False,
        offline_fixtures: Path | None = None,
        fetcher: Callable[[str], tuple[str, str]] | None = None,
        authenticated_price_lookup: Callable[[str, int], dict[str, Any]] | None = None,
    ) -> None:
        self.cache_dir = cache_dir
        self.max_requests = max_requests
        self.request_delay = request_delay
        self.refresh_cache = refresh_cache
        self.no_cache = no_cache
        self.offline_fixtures = offline_fixtures
        self.fetcher = fetcher or fetch_catalog_text_with_final_url
        self.authenticated_price_lookup = authenticated_price_lookup
        self.live_requests = 0
        self.cache_hits = 0
        self.cache_writes = 0
        self.cached_failures = 0
        self.live_block_failures = 0
        self.consecutive_block_failures = 0
        self.ordinary_failures = 0
        self._fixture_manifest: dict[str, Any] | None = None

    def _cache_path(self, cache_type: str, key: str) -> Path:
        digest = hashlib.sha256(f"{PARSER_VERSION}:{cache_type}:{key}".encode("utf-8")).hexdigest()
        return self.cache_dir / f"{digest}.json"

    def _read_cache(self, cache_type: str, key: str, ttl_seconds: int) -> dict[str, Any] | None:
        if self.no_cache or self.refresh_cache or self.offline_fixtures:
            return None
        path = self._cache_path(cache_type, key)
        if not path.exists():
            return None
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
            fetched_at = datetime.fromisoformat(str(payload.get("fetchedAt")))
        except Exception:
            return None
        effective_ttl = ttl_seconds
        if not payload.get("ok", True):
            failure_type = str(payload.get("failureType") or "")
            effective_ttl = BLOCK_FAILURE_TTL_SECONDS if failure_type == "block" else ORDINARY_FAILURE_TTL_SECONDS
        if utc_now() - fetched_at > timedelta(seconds=effective_ttl):
            return None
        payload["cacheHit"] = True
        self.cache_hits += 1
        if not payload.get("ok", True):
            self.cached_failures += 1
        return payload

    def _write_cache(self, cache_type: str, key: str, payload: dict[str, Any]) -> None:
        if self.no_cache or self.offline_fixtures:
            return
        path = self._cache_path(cache_type, key)
        write_json_atomic(path, {"parserVersion": PARSER_VERSION, "fetchedAt": utc_now().isoformat(), **payload})
        self.cache_writes += 1

    def cache_summary(self) -> dict[str, Any]:
        return {
            "enabled": not self.no_cache,
            "refresh": self.refresh_cache,
            "offlineFixtures": bool(self.offline_fixtures),
            "hits": self.cache_hits,
            "writes": self.cache_writes,
            "cachedFailures": self.cached_failures,
        }

    def _manifest(self) -> dict[str, Any]:
        if not self.offline_fixtures:
            return {}
        if self._fixture_manifest is None:
            self._fixture_manifest = json.loads((self.offline_fixtures / "manifest.json").read_text(encoding="utf-8"))
        return self._fixture_manifest

    def _fixture_html(self, section: str, key: str) -> tuple[str, str]:
        manifest = self._manifest()
        section_payload = dict(manifest.get(section) or {})
        fixture = section_payload.get(key)
        if fixture is None:
            raise AudibleFetchError(f"Offline fixture missing for {section}: {key}")
        if isinstance(fixture, dict) and fixture.get("failure"):
            failure = str(fixture["failure"])
            if failure in {"403", "429", "captcha", "robot"}:
                raise AudibleBlockedError(f"Offline fixture block: {failure}")
            raise AudibleFetchError(f"Offline fixture failure: {failure}")
        fixture_path = self.offline_fixtures / str(fixture)
        return fixture_path.read_text(encoding="utf-8"), key

    def _fetch_html(self, section: str, key: str, url: str) -> tuple[dict[str, Any], str | None]:
        if self.live_requests >= self.max_requests:
            raise RequestBudgetExceeded("request budget exhausted")
        try:
            if self.offline_fixtures:
                html_text, final_url = self._fixture_html(section, key)
            else:
                if self.live_requests > 0 and self.request_delay > 0:
                    time.sleep(self.request_delay)
                html_text, final_url = self.fetcher(url)
            self.live_requests += 1
            self.consecutive_block_failures = 0
            return {"ok": True, "html": html_text, "finalUrl": final_url, "cacheHit": False}, None
        except AudibleBlockedError as exc:
            self.live_requests += 1
            self.live_block_failures += 1
            self.consecutive_block_failures += 1
            return {"ok": False, "failureType": "block", "error": str(exc), "cacheHit": False}, "block"
        except Exception as exc:
            self.live_requests += 1
            self.ordinary_failures += 1
            return {"ok": False, "failureType": "ordinary", "error": str(exc), "cacheHit": False}, "ordinary"

    def should_abort_for_blocks(self) -> bool:
        if self.consecutive_block_failures >= 2:
            return True
        return self.live_requests >= 10 and self.live_block_failures / max(1, self.live_requests) > 0.30

    def should_abort_for_ordinary_failures(self) -> bool:
        return self.ordinary_failures >= 5

    def search_book(self, book: dict[str, Any], *, min_discount_percent: int) -> dict[str, Any]:
        query = normalize_space(f"{book.get('title') or ''} {book.get('author') or ''}")
        search_url = build_search_url(str(book.get("title") or ""), str(book.get("author") or ""))
        cached = self._read_cache("search", query, SEARCH_TTL_SECONDS)
        if cached:
            if not cached.get("ok"):
                return self._failure_result(book, search_url, str(cached.get("error") or ""), str(cached.get("failureType") or "cached"))
            cards = list(cached.get("cards") or [])
        else:
            search_payload, failure_kind = self._fetch_html("search", query, search_url)
            if not search_payload.get("ok"):
                self._write_cache("search", query, search_payload)
                return self._failure_result(book, search_url, str(search_payload.get("error") or ""), failure_kind)
            cards = parse_search_cards(str(search_payload.get("html") or ""))
            self._write_cache("search", query, {"ok": True, "cards": cards, "finalUrl": search_payload.get("finalUrl"), "cacheHit": False})
        selected: dict[str, Any] | None = None
        selected_status = "not_found"
        selected_reason = "no plausible candidate in first 3 search results"
        candidate_notes: list[dict[str, Any]] = []
        for card in cards[:3]:
            match_status, reason = validate_candidate(book, card)
            candidate_notes.append(
                {
                    "title": card.get("title"),
                    "author": card.get("author"),
                    "url": card.get("url"),
                    "matchStatus": match_status,
                    "matchReason": reason,
                }
            )
            if match_status in {"matched", "needs_review"}:
                selected = card
                selected_status = match_status
                selected_reason = reason
                break
        if selected is None:
            return self._base_result(book, search_url, "not_found", "not_found", selected_reason, candidate_notes)
        if selected_status == "needs_review":
            return self._card_result(book, search_url, selected, "needs_review", "needs_review", selected_reason, candidate_notes)
        if self.authenticated_price_lookup:
            authenticated_result = self._authenticated_price_result(
                book,
                search_url,
                selected,
                candidate_notes,
                min_discount_percent,
            )
            if authenticated_result is not None:
                return authenticated_result
        offer = dict(selected.get("offer") or {})
        hidden_status = offer.get("hiddenStatus")
        if hidden_status in {"price_hidden", "included_with_membership"}:
            return self._card_result(book, search_url, selected, str(hidden_status), "matched", "pricing hidden in search result", candidate_notes)
        if offer.get("hasNumericDiscountHint"):
            return self._confirm_discount(book, search_url, selected, candidate_notes, min_discount_percent)
        if offer.get("currentPrice") is not None or offer.get("listPrice") is not None:
            return self._card_result(book, search_url, selected, "price_unknown", "matched", "search result exposed incomplete price data", candidate_notes)
        return self._card_result(book, search_url, selected, "price_unknown", "matched", "matched search result did not expose usable pricing", candidate_notes)

    def _authenticated_price_result(
        self,
        book: dict[str, Any],
        search_url: str,
        card: dict[str, Any],
        candidate_notes: list[dict[str, Any]],
        min_discount_percent: int,
    ) -> dict[str, Any] | None:
        product_id = normalize_space(str(card.get("productId") or ""))
        if not product_id:
            return None
        if self.live_requests >= self.max_requests:
            return self._card_result(
                book,
                search_url,
                {**card, "offer": unknown_offer()},
                "price_unknown",
                "matched",
                "request budget was insufficient for authenticated price lookup",
                candidate_notes,
            )
        try:
            if self.live_requests > 0 and self.request_delay > 0:
                time.sleep(self.request_delay)
            self.live_requests += 1
            pricing = self.authenticated_price_lookup(product_id, min_discount_percent)
        except Exception as exc:
            self.ordinary_failures += 1
            result = self._card_result(
                book,
                search_url,
                {**card, "offer": unknown_offer()},
                "price_unknown",
                "matched",
                f"authenticated Audible price lookup failed: {exc}",
                candidate_notes,
            )
            result["warnings"].append(f"audible_api_authenticated: {exc}")
            return result
        status = str(pricing.get("pricingStatus") or "price_unknown")
        offer = {
            "currencyCode": pricing.get("currencyCode") or "USD",
            "currentPrice": pricing.get("currentPrice"),
            "listPrice": pricing.get("listPrice"),
            "discountPercent": pricing.get("discountPercent"),
            "priceBasis": pricing.get("priceBasis") or "audible_member_cash",
            "dealType": pricing.get("dealType") or "unknown",
            "hiddenStatus": status if status in {"price_hidden", "included_with_membership"} else None,
        }
        reason = "authenticated Audible API price lookup"
        return self._card_result(book, search_url, {**card, "offer": offer}, status, "matched", reason, candidate_notes)

    def _confirm_discount(
        self,
        book: dict[str, Any],
        search_url: str,
        card: dict[str, Any],
        candidate_notes: list[dict[str, Any]],
        min_discount_percent: int,
    ) -> dict[str, Any]:
        url = str(card.get("url") or "")
        cache_key = canonical_audible_url(url)
        cached = self._read_cache("product", cache_key, PRODUCT_TTL_SECONDS)
        if cached:
            if not cached.get("ok"):
                return self._failure_result(book, search_url, str(cached.get("error") or ""), str(cached.get("failureType") or "cached"), card)
            offer = dict(cached.get("offer") or {})
        else:
            if self.live_requests >= self.max_requests:
                card_with_offer = {**card, "offer": unknown_offer()}
                return self._card_result(
                    book,
                    search_url,
                    card_with_offer,
                    "price_unknown",
                    "matched",
                    "request budget was insufficient to confirm search-card discount",
                    candidate_notes,
                )
            product_payload, failure_kind = self._fetch_html("product", cache_key, url)
            if not product_payload.get("ok"):
                self._write_cache("product", cache_key, product_payload)
                return self._failure_result(book, search_url, str(product_payload.get("error") or ""), failure_kind, card)
            offer = parse_offer_text(str(product_payload.get("html") or ""))
            self._write_cache("product", cache_key, {"ok": True, "offer": offer, "finalUrl": product_payload.get("finalUrl"), "cacheHit": False})
        hidden_status = offer.get("hiddenStatus")
        if hidden_status in {"price_hidden", "included_with_membership"}:
            return self._card_result(book, search_url, {**card, "offer": offer}, str(hidden_status), "matched", "product page hid numeric cash pricing", candidate_notes)
        discount = offer.get("discountPercent")
        if discount is not None and int(discount) >= min_discount_percent:
            return self._card_result(book, search_url, {**card, "offer": offer}, "discounted", "matched", "product page confirmed numeric discount", candidate_notes)
        if offer.get("currentPrice") is not None and offer.get("listPrice") is not None:
            return self._card_result(book, search_url, {**card, "offer": offer}, "available_no_discount", "matched", "product page did not clear discount threshold", candidate_notes)
        return self._card_result(book, search_url, {**card, "offer": offer}, "price_unknown", "matched", "product page did not expose reliable numeric pricing", candidate_notes)

    def _base_result(
        self,
        book: dict[str, Any],
        search_url: str,
        status: str,
        match_status: str,
        reason: str,
        candidate_notes: list[dict[str, Any]] | None = None,
    ) -> dict[str, Any]:
        return {
            "goodreads": book,
            "audible": {},
            "pricing": {**unknown_offer(), "pricingStatus": status},
            "status": status,
            "matchStatus": match_status,
            "matchReason": reason,
            "warnings": [],
            "searchUrl": search_url,
            "candidateNotes": candidate_notes or [],
        }

    def _card_result(
        self,
        book: dict[str, Any],
        search_url: str,
        card: dict[str, Any],
        status: str,
        match_status: str,
        reason: str,
        candidate_notes: list[dict[str, Any]] | None = None,
    ) -> dict[str, Any]:
        offer = dict(card.get("offer") or {})
        return {
            "goodreads": book,
            "audible": {
                "title": card.get("title") or None,
                "author": card.get("author") or None,
                "url": card.get("url") or None,
                "productId": card.get("productId") or None,
            },
            "pricing": {
                "currencyCode": offer.get("currencyCode") or "USD",
                "currentPrice": offer.get("currentPrice"),
                "listPrice": offer.get("listPrice"),
                "discountPercent": offer.get("discountPercent"),
                "priceBasis": offer.get("priceBasis") or "unknown",
                "dealType": offer.get("dealType") or "unknown",
                "pricingStatus": status,
            },
            "status": status,
            "matchStatus": match_status,
            "matchReason": reason,
            "warnings": list(card.get("warnings") or []),
            "searchUrl": search_url,
            "candidateNotes": candidate_notes or [],
        }

    def _failure_result(
        self,
        book: dict[str, Any],
        search_url: str,
        error: str,
        failure_kind: str | None,
        card: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        result = self._card_result(book, search_url, card, "lookup_failed", "lookup_failed", error) if card else self._base_result(book, search_url, "lookup_failed", "lookup_failed", error)
        result["warnings"] = [f"{failure_kind or 'fetch'}: {error}"]
        return result


def deterministic_shuffle(items: list[dict[str, Any]], seed: str) -> list[dict[str, Any]]:
    rng = random.Random(seed)
    result = list(items)
    rng.shuffle(result)
    return result

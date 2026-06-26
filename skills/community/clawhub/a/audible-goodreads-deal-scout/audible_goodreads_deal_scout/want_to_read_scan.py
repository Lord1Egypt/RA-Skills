from __future__ import annotations

import json
import sys
import time
from collections import Counter
from datetime import UTC, date, datetime
from pathlib import Path
from typing import Any, Callable, TextIO

from .audible_auth import authenticated_product_pricing
from .audible_catalog import AudibleCatalogClient, RequestBudgetExceeded, deterministic_shuffle
from .goodreads_csv import effective_shelf, load_goodreads_csv
from .goodreads_rating import lookup_goodreads_rating
from .settings import default_config_path, default_storage_dir, load_config, validate_marketplace
from .shared import normalize_author_key, normalize_space, normalized_key, write_json_atomic


DEFAULT_SCAN_ORDER = "newest"
SCAN_ORDERS = {"newest", "csv", "oldest", "random"}
STATUS_ORDER = {
    "discounted": 0,
    "included_with_membership": 1,
    "price_hidden": 2,
    "available_no_discount": 3,
    "price_unknown": 4,
    "needs_review": 5,
    "not_found": 6,
    "lookup_failed": 7,
}
PROGRESS_MODES = {"none", "plain", "json"}


def _now_iso() -> str:
    return datetime.now(UTC).isoformat()


def _error_report(reason_code: str, message: str, *, config_path: Path | None = None) -> dict[str, Any]:
    return {
        "schemaVersion": 1,
        "ok": False,
        "status": "error",
        "reasonCode": reason_code,
        "generatedAt": _now_iso(),
        "marketplace": "us",
        "csvPath": None,
        "selection": {},
        "requestBudget": {"max": 0, "used": 0, "remaining": 0},
        "counts": {},
        "warnings": [message],
        "results": [],
        "metadata": {"configPath": str(config_path) if config_path else None},
        "message": message,
        "error": {"type": "InputError", "message": message},
        "exitCode": 1,
    }


def parse_goodreads_date(raw: str) -> str | None:
    text = normalize_space(raw)
    if not text:
        return None
    for pattern in ("%Y/%m/%d", "%Y-%m-%d", "%m/%d/%Y", "%d/%m/%Y"):
        try:
            return datetime.strptime(text, pattern).date().isoformat()
        except ValueError:
            continue
    return None


def row_identity(row: dict[str, Any]) -> str:
    book_id = normalize_space(str(row.get("bookId") or ""))
    if book_id:
        return f"goodreads:{book_id}"
    title_key = normalized_key(str(row.get("title") or ""), ascii_only=True)
    author_key = normalize_author_key(str(row.get("author") or ""), ascii_only=True)
    return f"title-author:{title_key}|{author_key}"


def goodreads_scan_entry(row: dict[str, Any], index: int) -> dict[str, Any]:
    return {
        "rowKey": row_identity(row),
        "csvIndex": index,
        "bookId": normalize_space(str(row.get("bookId") or "")) or None,
        "title": normalize_space(str(row.get("title") or "")),
        "author": normalize_space(str(row.get("author") or "")),
        "averageRating": row.get("averageRating"),
        "averageRatingSource": row.get("averageRatingSource"),
        "ratingsCount": None,
        "dateAdded": parse_goodreads_date(str(row.get("dateAdded") or "")) or normalize_space(str(row.get("dateAdded") or "")) or None,
        "isbn": normalize_space(str(row.get("isbn") or "")) or None,
        "isbn13": normalize_space(str(row.get("isbn13") or "")) or None,
    }


def extract_to_read_entries(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []
    seen: set[str] = set()
    for index, row in enumerate(rows):
        if effective_shelf(row) != "to-read":
            continue
        entry = goodreads_scan_entry(row, index)
        key = str(entry["rowKey"])
        if key in seen:
            continue
        seen.add(key)
        entries.append(entry)
    return entries


def _date_sort_value(entry: dict[str, Any]) -> str:
    value = str(entry.get("dateAdded") or "")
    if len(value) == 10 and value[4] == "-" and value[7] == "-":
        return value
    return "0000-00-00"


def select_entries(
    entries: list[dict[str, Any]],
    *,
    scan_order: str,
    seed: str,
    offset: int,
    limit: int | None,
) -> list[dict[str, Any]]:
    if scan_order not in SCAN_ORDERS:
        raise ValueError(f"Unsupported --scan-order '{scan_order}'. Use newest, csv, oldest, or random.")
    ordered = list(entries)
    if scan_order == "newest":
        ordered.sort(key=lambda item: (_date_sort_value(item), str(item.get("title") or "")), reverse=True)
    elif scan_order == "oldest":
        ordered.sort(key=lambda item: (_date_sort_value(item) == "0000-00-00", _date_sort_value(item), str(item.get("title") or "")))
    elif scan_order == "random":
        ordered = deterministic_shuffle(ordered, seed)
    start = max(0, offset)
    end = None if limit is None else start + max(0, limit)
    return ordered[start:end]


def _rating_value(result: dict[str, Any]) -> float:
    value = (result.get("goodreads") or {}).get("averageRating")
    try:
        return float(value or 0)
    except Exception:
        return 0.0


def _discount_value(result: dict[str, Any]) -> int:
    value = (result.get("pricing") or {}).get("discountPercent")
    try:
        return int(value or 0)
    except Exception:
        return 0


def _date_rank_value(result: dict[str, Any]) -> int:
    raw = str((result.get("goodreads") or {}).get("dateAdded") or "")
    if len(raw) == 10 and raw[4] == "-" and raw[7] == "-":
        try:
            return date.fromisoformat(raw).toordinal()
        except ValueError:
            return 0
    return 0


def rank_results(results: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return sorted(
        results,
        key=lambda item: (
            STATUS_ORDER.get(str(item.get("status") or ""), 99),
            -_discount_value(item),
            -_rating_value(item),
            -_date_rank_value(item),
        ),
    )


def _dedupe_key(result: dict[str, Any]) -> str:
    audible = result.get("audible") if isinstance(result.get("audible"), dict) else {}
    product_id = normalize_space(str(audible.get("productId") or ""))
    if product_id:
        return f"product:{product_id.casefold()}"
    url = normalize_space(str(audible.get("url") or ""))
    if url:
        return f"url:{url}"
    return ""


def dedupe_ranked_results(results: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    """Keep one report row per Audible product after ranking has chosen the best row."""
    seen: dict[str, dict[str, Any]] = {}
    deduped: list[dict[str, Any]] = []
    suppressed: list[dict[str, Any]] = []
    for result in results:
        key = _dedupe_key(result)
        if not key:
            deduped.append(result)
            continue
        kept = seen.get(key)
        if kept is None:
            seen[key] = result
            deduped.append(result)
            continue
        suppressed.append(
            {
                "dedupeKey": key,
                "keptRowKey": (kept.get("goodreads") or {}).get("rowKey"),
                "suppressedRowKey": (result.get("goodreads") or {}).get("rowKey"),
                "goodreadsTitle": (result.get("goodreads") or {}).get("title"),
                "audibleTitle": (result.get("audible") or {}).get("title"),
                "audibleProductId": (result.get("audible") or {}).get("productId"),
            }
        )
    return deduped, {
        "enabled": True,
        "suppressedDuplicateCount": len(suppressed),
        "suppressedDuplicates": suppressed,
    }


def enrich_goodreads_ratings(
    results: list[dict[str, Any]],
    *,
    cache_dir: Path,
    limit: int,
    refresh_cache: bool,
    no_cache: bool,
    request_delay: float,
    fetcher: Callable[[str], tuple[str, str]] | None = None,
) -> dict[str, Any]:
    stats = {
        "enabled": True,
        "attempted": 0,
        "updated": 0,
        "cacheHits": 0,
        "skippedExisting": 0,
        "skippedNoBookId": 0,
        "failed": 0,
        "limit": max(0, limit),
    }
    if limit <= 0:
        return stats
    for result in results:
        if result.get("status") != "discounted":
            continue
        goodreads = result.get("goodreads") if isinstance(result.get("goodreads"), dict) else {}
        if goodreads.get("averageRating") is not None:
            stats["skippedExisting"] += 1
            continue
        book_id = normalize_space(str(goodreads.get("bookId") or ""))
        if not book_id:
            stats["skippedNoBookId"] += 1
            continue
        if stats["attempted"] >= limit:
            break
        if stats["attempted"] > 0 and request_delay > 0:
            time.sleep(request_delay)
        stats["attempted"] += 1
        try:
            rating = lookup_goodreads_rating(
                book_id,
                cache_dir=cache_dir,
                refresh_cache=refresh_cache,
                no_cache=no_cache,
                fetcher=fetcher,
            )
        except Exception:
            stats["failed"] += 1
            continue
        if rating.get("cacheHit"):
            stats["cacheHits"] += 1
        goodreads["averageRating"] = rating.get("averageRating")
        goodreads["averageRatingSource"] = rating.get("source")
        goodreads["ratingsCount"] = rating.get("ratingsCount")
        goodreads["url"] = rating.get("url")
        stats["updated"] += 1
    return stats


def count_results(results: list[dict[str, Any]], *, total_to_read: int, selected_rows: int, scanned_rows: int | None = None) -> dict[str, Any]:
    statuses = Counter(str(result.get("status") or "unknown") for result in results)
    return {
        "totalWantToRead": total_to_read,
        "selectedRows": selected_rows,
        "scannedRows": len(results) if scanned_rows is None else scanned_rows,
        "reportedResults": len(results),
        "discounted": statuses.get("discounted", 0),
        "availableNoDiscount": statuses.get("available_no_discount", 0),
        "includedWithMembership": statuses.get("included_with_membership", 0),
        "priceHidden": statuses.get("price_hidden", 0),
        "priceUnknown": statuses.get("price_unknown", 0),
        "needsReview": statuses.get("needs_review", 0),
        "notFound": statuses.get("not_found", 0),
        "lookupFailed": statuses.get("lookup_failed", 0),
        "byStatus": dict(sorted(statuses.items())),
    }


def _request_budget_summary(max_requests: int, used: int) -> dict[str, int]:
    return {"max": max_requests, "used": used, "remaining": max(0, max_requests - used)}


def _progress_counts(results: list[dict[str, Any]], *, total_to_read: int, selected_rows: int) -> dict[str, Any]:
    return count_results(results, total_to_read=total_to_read, selected_rows=selected_rows, scanned_rows=len(results))


class ScanProgressReporter:
    """Emit human or JSONL progress to stderr without mixing it into report output."""

    def __init__(self, *, mode: str = "none", interval_seconds: float = 5.0, stream: TextIO | None = None) -> None:
        self.mode = mode if mode in PROGRESS_MODES else "none"
        self.interval_seconds = max(0.0, interval_seconds)
        self.stream = stream or sys.stderr
        self._last_emit = 0.0

    def emit(
        self,
        event: str,
        *,
        scanned: int,
        selected: int,
        total: int,
        status: str,
        reason_code: str,
        counts: dict[str, Any] | None = None,
        request_budget: dict[str, Any] | None = None,
        cache: dict[str, Any] | None = None,
        current_title: str | None = None,
        last_status: str | None = None,
        force: bool = False,
    ) -> None:
        if self.mode == "none":
            return
        now = time.monotonic()
        if not force and self.interval_seconds > 0 and now - self._last_emit < self.interval_seconds:
            return
        self._last_emit = now
        counts = counts or {}
        request_budget = request_budget or {}
        cache = cache or {}
        payload = {
            "schemaVersion": 1,
            "event": event,
            "generatedAt": _now_iso(),
            "status": status,
            "reasonCode": reason_code,
            "scannedRows": scanned,
            "selectedRows": selected,
            "totalWantToRead": total,
            "percent": round((scanned / selected) * 100, 1) if selected else 100.0,
            "currentTitle": current_title,
            "lastStatus": last_status,
            "counts": counts,
            "requestBudget": request_budget,
            "cache": cache,
        }
        if self.mode == "json":
            self.stream.write(json.dumps(payload, sort_keys=True, ensure_ascii=False) + "\n")
        else:
            self.stream.write(self._plain_line(payload) + "\n")
        self.stream.flush()

    @staticmethod
    def _plain_line(payload: dict[str, Any]) -> str:
        selected = int(payload.get("selectedRows") or 0)
        scanned = int(payload.get("scannedRows") or 0)
        width = 24
        filled = width if selected <= 0 else min(width, int(width * scanned / max(1, selected)))
        bar = "#" * filled + "-" * (width - filled)
        counts = payload.get("counts") or {}
        budget = payload.get("requestBudget") or {}
        cache = payload.get("cache") or {}
        title = normalize_space(str(payload.get("currentTitle") or ""))[:60]
        title_part = f' current="{title}"' if title else ""
        return (
            f"[{bar}] {scanned}/{selected} {payload.get('percent', 0):.1f}% "
            f"{payload.get('event')} status={payload.get('status')} "
            f"last={payload.get('lastStatus') or '-'} "
            f"discounted={counts.get('discounted', 0)} review={counts.get('needsReview', 0)} "
            f"not_found={counts.get('notFound', 0)} failed={counts.get('lookupFailed', 0)} "
            f"requests={budget.get('used', 0)}/{budget.get('max', 0)} "
            f"cache_hits={cache.get('hits', 0)}{title_part}"
        )


def _price_line(result: dict[str, Any]) -> str:
    pricing = result.get("pricing") or {}
    current = pricing.get("currentPrice")
    list_price = pricing.get("listPrice")
    discount = pricing.get("discountPercent")
    deal_type = str(pricing.get("dealType") or "")
    label = {
        "limited_time_sale": "limited-time sale/promotion",
        "member_cash_below_list": "member cash below list",
        "cash_price_below_list": "cash price below list",
        "included_with_membership": "included with membership",
    }.get(deal_type)
    if current is not None and list_price is not None and discount is not None:
        price = f"${float(current):.2f} (-{int(discount)}%, list ${float(list_price):.2f})"
        return price + (f"; {label}" if label else "")
    if current is not None:
        price = f"${float(current):.2f}"
        return price + (f"; {label}" if label else "")
    return str(pricing.get("pricingStatus") or result.get("status") or "unknown").replace("_", " ")


def _candidate_note_line(result: dict[str, Any]) -> str:
    notes = []
    for item in (result.get("candidateNotes") or [])[:3]:
        title = normalize_space(str(item.get("title") or "untitled"))
        status = normalize_space(str(item.get("matchStatus") or "unknown"))
        reason = normalize_space(str(item.get("matchReason") or ""))
        notes.append(f"{title}: {status}" + (f" ({reason})" if reason else ""))
    return "; ".join(notes)


def render_markdown(report: dict[str, Any], *, include_non_deals: bool = False, verbose: bool = False) -> str:
    counts = report.get("counts") or {}
    budget = report.get("requestBudget") or {}
    cache = report.get("cache") or {}
    metadata = report.get("metadata") or {}
    selection = report.get("selection") or {}
    authenticated = bool(metadata.get("authenticatedPriceLookup"))
    lines = [
        "# Discounted Want-to-Read Titles",
        "",
        (
            f"Scanned {counts.get('scannedRows', 0)} of {counts.get('selectedRows', 0)} selected "
            f"Want-to-Read books. Reporting {counts.get('reportedResults', counts.get('scannedRows', 0))} unique results. "
            f"Live requests: {budget.get('used', 0)}/{budget.get('max', 0)}."
        ),
        (
            "Pricing: "
            + ("authenticated Audible cash pricing enabled." if authenticated else "anonymous Audible search/card pricing only.")
        ),
        f"Cache: {cache.get('hits', 0)} hits, {cache.get('writes', 0)} writes.",
        f"Deduplication: {counts.get('duplicateAudibleProducts', 0)} duplicate Audible product rows suppressed.",
        (
            "Summary: "
            f"{counts.get('discounted', 0)} discounted, "
            f"{counts.get('includedWithMembership', 0)} included, "
            f"{counts.get('priceHidden', 0)} hidden price, "
            f"{counts.get('priceUnknown', 0)} unknown price, "
            f"{counts.get('needsReview', 0)} need review, "
            f"{counts.get('notFound', 0)} not found, "
            f"{counts.get('lookupFailed', 0)} failed."
        ),
        "",
    ]
    next_offset = int(selection.get("offset") or 0) + int(counts.get("scannedRows") or 0)
    total_to_read = int(counts.get("totalWantToRead") or 0)
    limit = selection.get("limit")
    if limit is not None and next_offset < total_to_read:
        next_parts = [
            "scan-want-to-read",
            f"--scan-order {selection.get('order') or DEFAULT_SCAN_ORDER}",
            f"--offset {next_offset}",
            f"--limit {limit}",
            f"--max-requests {budget.get('max', 0)}",
        ]
        if authenticated:
            next_parts.append("--audible-auth-path <auth-path>")
        lines.extend(
            [
                "Next batch:",
                "",
                "```bash",
                " ".join(next_parts),
                "```",
                "",
            ]
        )
    discounted = [result for result in report.get("results") or [] if result.get("status") == "discounted"]
    if not discounted:
        lines.append("No visible numeric Audible discounts were found in this scan.")
    for index, result in enumerate(discounted[:20], start=1):
        goodreads = result.get("goodreads") or {}
        audible = result.get("audible") or {}
        warnings = ", ".join(result.get("warnings") or [])
        rating = goodreads.get("averageRating")
        rating_text = f"Goodreads {rating}" if rating is not None else "Goodreads rating unavailable"
        lines.extend(
            [
                f"{index}. **{audible.get('title') or goodreads.get('title')}** - {audible.get('author') or goodreads.get('author')}",
                f"   Price: {_price_line(result)}. {rating_text}.",
                f"   Audible: {audible.get('url')}",
            ]
        )
        if warnings:
            lines.append(f"   Warnings: {warnings}")
        if verbose:
            lines.append(f"   Search: {result.get('searchUrl')}")
            lines.append(f"   Match: {result.get('matchReason')}")
            candidate_line = _candidate_note_line(result)
            if candidate_line:
                lines.append(f"   Candidates: {candidate_line}")
        lines.append("")
    if len(discounted) > 20:
        lines.append(f"{len(discounted) - 20} additional discounted titles are in the JSON output.")
        lines.append("")
    if include_non_deals:
        section_specs = (
            ("Needs Review", "needs_review"),
            ("Price Hidden", "price_hidden"),
            ("Included With Membership", "included_with_membership"),
            ("Not Found", "not_found"),
        )
        for heading, status in section_specs:
            items = [result for result in report.get("results") or [] if result.get("status") == status]
            if not items:
                continue
            lines.extend([f"## {heading}", ""])
            for result in items[:10]:
                goodreads = result.get("goodreads") or {}
                audible = result.get("audible") or {}
                label = audible.get("title") or goodreads.get("title")
                author = audible.get("author") or goodreads.get("author")
                line = f"- {label} - {author}: {result.get('matchReason')}"
                if verbose:
                    candidate_line = _candidate_note_line(result)
                    line += f" ({result.get('searchUrl')})"
                    if candidate_line:
                        line += f" Candidates: {candidate_line}"
                lines.append(line)
            if len(items) > 10:
                lines.append(f"- {len(items) - 10} more in JSON output.")
            lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def _storage_dir_for(config_path: Path, config: dict[str, Any]) -> Path:
    if config_path.name == "config.json":
        return config_path.parent
    artifact_dir = normalize_space(str(config.get("artifactDir") or ""))
    if artifact_dir:
        path = Path(artifact_dir).expanduser()
        if path.name == "current" and path.parent.name == "artifacts":
            return path.parent.parent
    return default_storage_dir()


def _single_book_entry(title: str, author: str) -> dict[str, Any]:
    return {
        "rowKey": "single:" + normalized_key(f"{title} {author}", ascii_only=True),
        "csvIndex": 0,
        "bookId": None,
        "title": normalize_space(title),
        "author": normalize_space(author),
        "averageRating": None,
        "averageRatingSource": None,
        "ratingsCount": None,
        "dateAdded": None,
        "isbn": None,
        "isbn13": None,
    }


def scan_want_to_read(
    options: dict[str, Any],
    *,
    fetcher: Callable[[str], tuple[str, str]] | None = None,
    goodreads_fetcher: Callable[[str], tuple[str, str]] | None = None,
) -> tuple[dict[str, Any], str, int]:
    """Run a stateless Want-to-Read scan and return structured JSON, Markdown, and an exit code."""
    config_path = Path(str(options.get("configPath") or default_config_path())).expanduser().resolve()
    try:
        resolved_config_path, file_config = load_config(config_path)
        config = {**file_config, **{key: value for key, value in options.items() if value is not None}}
        marketplace = normalize_space(str(config.get("audibleMarketplace") or "us")).lower() or "us"
        if marketplace != "us":
            raise ValueError("scan-want-to-read supports only Audible US in v1.")
        validate_marketplace(marketplace)
        scan_order = normalize_space(str(config.get("scanOrder") or DEFAULT_SCAN_ORDER)).lower() or DEFAULT_SCAN_ORDER
        seed = normalize_space(str(config.get("seed") or date.today().isoformat()))
        offset = int(config.get("offset") or 0)
        limit = config.get("limit")
        limit_value = None if limit in (None, "") else int(limit)
        max_requests = int(config.get("maxRequests") or 40)
        request_delay = float(config.get("requestDelay") if config.get("requestDelay") is not None else 1.0)
        progress_mode = normalize_space(str(config.get("progress") or "none")).lower() or "none"
        if progress_mode not in PROGRESS_MODES:
            raise ValueError("--progress must be one of: json, none, plain.")
        progress_interval = float(config.get("progressInterval") if config.get("progressInterval") is not None else 5.0)
        min_discount_percent = int(config.get("minDiscountPercent") or 10)
        enrich_ratings = config.get("enrichGoodreadsRatings")
        enrich_goodreads_ratings_enabled = not bool(config.get("offlineFixtures")) if enrich_ratings is None else bool(enrich_ratings)
        goodreads_rating_limit = int(config.get("goodreadsRatingLimit") or 20)
        audible_auth_path = normalize_space(str(config.get("audibleAuthPath") or ""))
        title = normalize_space(str(config.get("title") or ""))
        author = normalize_space(str(config.get("author") or ""))
        if bool(title) != bool(author):
            raise ValueError("--title and --author must be provided together.")
        csv_path: Path | None = None
        total_to_read = 1
        if title and author:
            entries = [_single_book_entry(title, author)]
        else:
            raw_csv_path = normalize_space(str(config.get("goodreadsCsvPath") or ""))
            if not raw_csv_path:
                return _error_report("error_missing_csv", "Goodreads CSV is required for scan-want-to-read.", config_path=resolved_config_path), "", 1
            csv_path = Path(raw_csv_path).expanduser()
            if not csv_path.exists():
                return _error_report("error_missing_csv", f"Goodreads CSV not found at {csv_path}.", config_path=resolved_config_path), "", 1
            rows, _stats = load_goodreads_csv(csv_path, dict(config.get("csvColumns") or {}))
            entries = extract_to_read_entries(rows)
            total_to_read = len(entries)
        selected = select_entries(entries, scan_order=scan_order, seed=seed, offset=offset, limit=limit_value)
    except Exception as exc:
        report = _error_report("error_invalid_input", str(exc), config_path=config_path)
        return report, "", 1

    storage_dir = _storage_dir_for(resolved_config_path, config)
    cache_dir = storage_dir / "cache" / "audible"
    authenticated_price_lookup = None
    if audible_auth_path:
        auth_path = Path(audible_auth_path).expanduser()

        def authenticated_price_lookup(product_id: str, threshold: int) -> dict[str, Any]:
            return authenticated_product_pricing(auth_path, product_id, threshold=threshold)

    client = AudibleCatalogClient(
        cache_dir=cache_dir,
        max_requests=max_requests,
        request_delay=request_delay,
        refresh_cache=bool(config.get("refreshCache")),
        no_cache=bool(config.get("noCache")),
        offline_fixtures=Path(str(config["offlineFixtures"])).expanduser() if config.get("offlineFixtures") else None,
        fetcher=fetcher,
        authenticated_price_lookup=authenticated_price_lookup,
    )

    results: list[dict[str, Any]] = []
    status = "completed"
    reason_code = "completed"
    exit_code = 0
    warnings: list[str] = []
    reporter = ScanProgressReporter(mode=progress_mode, interval_seconds=progress_interval)
    selected_count = len(selected)

    def emit_progress(
        event: str,
        *,
        scanned: int | None = None,
        run_status: str,
        run_reason_code: str,
        counts_override: dict[str, Any] | None = None,
        current_title: str | None = None,
        last_status: str | None = None,
        force: bool = False,
    ) -> None:
        scanned_count = len(results) if scanned is None else scanned
        reporter.emit(
            event,
            scanned=scanned_count,
            selected=selected_count,
            total=total_to_read,
            status=run_status,
            reason_code=run_reason_code,
            counts=counts_override
            or _progress_counts(results, total_to_read=total_to_read, selected_rows=selected_count),
            request_budget=_request_budget_summary(max_requests, client.live_requests),
            cache=client.cache_summary(),
            current_title=current_title,
            last_status=last_status,
            force=force,
        )

    emit_progress(
        "start",
        scanned=0,
        run_status="running",
        run_reason_code="scan_started",
        force=True,
    )
    for index, entry in enumerate(selected, start=1):
        current_title = normalize_space(str(entry.get("title") or ""))
        try:
            result = client.search_book(entry, min_discount_percent=min_discount_percent)
        except RequestBudgetExceeded:
            status = "partial"
            reason_code = "request_budget_exhausted"
            exit_code = 2
            warnings.append("Request budget exhausted before all selected rows were scanned.")
            emit_progress(
                "partial",
                run_status=status,
                run_reason_code=reason_code,
                current_title=current_title,
                force=True,
            )
            break
        results.append(result)
        if client.should_abort_for_blocks():
            status = "aborted"
            reason_code = "audible_block_circuit_open"
            exit_code = 3
            warnings.append("Audible block-like circuit breaker opened.")
            emit_progress(
                "aborted",
                run_status=status,
                run_reason_code=reason_code,
                current_title=current_title,
                last_status=str(result.get("status") or ""),
                force=True,
            )
            break
        if client.should_abort_for_ordinary_failures():
            status = "partial"
            reason_code = "ordinary_fetch_failure_limit"
            warnings.append("Stopped early after repeated ordinary network failures.")
            emit_progress(
                "partial",
                run_status=status,
                run_reason_code=reason_code,
                current_title=current_title,
                last_status=str(result.get("status") or ""),
                force=True,
            )
            break
        emit_progress(
            "item",
            scanned=index,
            run_status="running",
            run_reason_code="scan_running",
            current_title=current_title,
            last_status=str(result.get("status") or ""),
        )

    ranked_raw_results = rank_results(results)
    rating_enrichment = {"enabled": False}
    if enrich_goodreads_ratings_enabled:
        rating_enrichment = enrich_goodreads_ratings(
            ranked_raw_results,
            cache_dir=storage_dir / "cache" / "goodreads",
            limit=goodreads_rating_limit,
            refresh_cache=bool(config.get("refreshCache")),
            no_cache=bool(config.get("noCache")),
            request_delay=request_delay,
            fetcher=goodreads_fetcher,
        )
        ranked_raw_results = rank_results(ranked_raw_results)
    ranked_results, deduplication = dedupe_ranked_results(ranked_raw_results)
    counts = count_results(ranked_results, total_to_read=total_to_read, selected_rows=selected_count, scanned_rows=len(results))
    counts["duplicateAudibleProducts"] = int(deduplication.get("suppressedDuplicateCount") or 0)
    report = {
        "schemaVersion": 1,
        "status": status,
        "reasonCode": reason_code,
        "generatedAt": _now_iso(),
        "marketplace": "us",
        "csvPath": str(csv_path) if csv_path else None,
        "selection": {
            "order": scan_order,
            "seed": seed,
            "offset": offset,
            "limit": limit_value,
            "selectedRows": selected_count,
            "totalWantToRead": total_to_read,
        },
        "requestBudget": _request_budget_summary(max_requests, client.live_requests),
        "cache": client.cache_summary(),
        "goodreadsRatingEnrichment": rating_enrichment,
        "deduplication": deduplication,
        "counts": counts,
        "warnings": warnings,
        "results": ranked_results,
        "metadata": {
            "configPath": str(resolved_config_path),
            "cacheDir": str(cache_dir),
            "parserVersion": "want-to-read-v1",
            "authenticatedPriceLookup": bool(authenticated_price_lookup),
        },
        "exitCode": exit_code,
    }
    emit_progress(
        "done" if status == "completed" else status,
        run_status=status,
        run_reason_code=reason_code,
        counts_override=counts,
        force=True,
    )
    markdown = render_markdown(
        report,
        include_non_deals=bool(config.get("includeNonDeals")),
        verbose=bool(config.get("verbose")),
    )
    if output_json := config.get("outputJson"):
        write_json_atomic(Path(str(output_json)).expanduser(), report)
    if output_md := config.get("outputMd"):
        from .shared import atomic_write_text

        atomic_write_text(Path(str(output_md)).expanduser(), markdown)
    return report, markdown, exit_code


def report_json(report: dict[str, Any]) -> str:
    return json.dumps(report, indent=2, sort_keys=True, ensure_ascii=False) + "\n"

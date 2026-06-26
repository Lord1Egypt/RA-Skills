#!/usr/bin/env python3
"""Migrate Goodreads CSV exports into Obsidian notes with deterministic upsert."""

from __future__ import annotations

import argparse
import csv
import json
import time
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
from urllib.parse import quote_plus

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from common_config import get_env_bool, get_env_int, get_env_str
from common_isbn import normalize_isbn
from common_json import fail_and_print, make_result, print_json
from upsert_obsidian_note import upsert_note

STAGE = "migrate_goodreads_csv"


def _normalize_header_map(row: Dict[str, Any]) -> Dict[str, str]:
    out: Dict[str, str] = {}
    for key in row.keys():
        out[key.strip().lower()] = key
    return out


def _get_value(row: Dict[str, Any], header_map: Dict[str, str], name: str) -> str:
    key = header_map.get(name.lower())
    if key is None:
        return ""
    return str(row.get(key, "") or "").strip()


def _split_tags(value: str) -> List[str]:
    if not value:
        return []
    out: List[str] = []
    seen = set()
    for raw in value.split(","):
        tag = raw.strip()
        if tag and tag not in seen:
            seen.add(tag)
            out.append(tag)
    return out


def _normalize_tag(value: str) -> str:
    tag = (value or "").strip().lower()
    if not tag:
        return ""
    tag = tag.replace("&", " and ")
    for token in ["/", "\\", "(", ")", "[", "]", "{", "}", ",", ":", ";", "!", "?", "'", '"', "`"]:
        tag = tag.replace(token, " ")
    tag = "-".join(tag.split())
    while "--" in tag:
        tag = tag.replace("--", "-")
    return tag.strip("-")


def _normalize_slug(value: str) -> str:
    text = (value or "").strip().lower()
    if not text:
        return "unknown"
    for token in ("/", "\\", ",", ":"):
        text = text.replace(token, "-")
    text = "-".join(text.split())
    while "--" in text:
        text = text.replace("--", "-")
    text = text.strip("-")
    return text or "unknown"


def _shelf_subfolder(shelf: str) -> str:
    return _normalize_slug(shelf)


def _map_status(exclusive_shelf: str, date_read: str) -> str:
    shelf = exclusive_shelf.strip().lower()
    if shelf in {"to-read", "to read", "want-to-read"}:
        return "to-read"
    if shelf in {"currently-reading", "currently reading", "reading"}:
        return "reading"
    if shelf in {"read", "finished"}:
        return "finished"
    if shelf in {"did-not-finish", "dnf"}:
        return "dnf"
    if date_read.strip():
        return "finished"
    return "inbox"


def _pick_isbn13(isbn13_raw: str, isbn10_raw: str) -> Optional[str]:
    normalized_13 = normalize_isbn(isbn13_raw or "")
    if normalized_13:
        return normalized_13
    normalized_10 = normalize_isbn(isbn10_raw or "")
    if normalized_10:
        return normalized_10
    return None


def _get_requests_module():
    try:
        import requests  # type: ignore
    except Exception as exc:
        raise RuntimeError(f"requests library is required: {exc}")
    return requests


def _best_google_cover(image_links: Dict[str, Any]) -> Optional[str]:
    for key in ["extraLarge", "large", "medium", "small", "thumbnail", "smallThumbnail"]:
        value = image_links.get(key)
        if isinstance(value, str) and value.strip():
            url = value.replace("http://", "https://")
            if "google" in url and "zoom=1" in url:
                url = url.replace("zoom=1", "zoom=2")
            return url
    return None


def _google_books_enrich(
    title: str,
    author: str,
    isbn13: Optional[str],
    timeout_sec: int,
    delay_ms: int,
    max_retries: int,
    api_key: str,
) -> Tuple[Optional[Dict[str, Any]], Optional[str], Optional[str]]:
    requests = _get_requests_module()

    if isbn13:
        query = f"isbn:{isbn13}"
    else:
        q = []
        if title:
            q.append(f"intitle:{title}")
        if author:
            q.append(f"inauthor:{author}")
        query = " ".join(q).strip()

    if not query:
        return None, None, "missing query for google books enrichment"

    url = f"https://www.googleapis.com/books/v1/volumes?q={quote_plus(query)}&maxResults=1"
    if api_key.strip():
        url = f"{url}&key={quote_plus(api_key.strip())}"

    attempt = 0
    while True:
        try:
            res = requests.get(
                url,
                timeout=timeout_sec,
                headers={"Accept": "application/json", "User-Agent": "book-capture-obsidian/1.0"},
            )
        except Exception as exc:
            if attempt >= max_retries:
                return None, None, f"google books request failed: {exc}"
            time.sleep((delay_ms / 1000.0) * max(1, 2**attempt))
            attempt += 1
            continue

        if res.status_code == 429:
            if attempt >= max_retries:
                return None, None, "google books rate limit (429)"
            retry_after = res.headers.get("Retry-After")
            if retry_after and retry_after.isdigit():
                time.sleep(max(1, int(retry_after)))
            else:
                time.sleep((delay_ms / 1000.0) * max(1, 2**attempt))
            attempt += 1
            continue

        if res.status_code >= 500:
            if attempt >= max_retries:
                return None, None, f"google books http {res.status_code}"
            time.sleep((delay_ms / 1000.0) * max(1, 2**attempt))
            attempt += 1
            continue

        try:
            res.raise_for_status()
            payload = res.json()
        except Exception as exc:
            return None, None, f"google books response failed: {exc}"

        items = payload.get("items") if isinstance(payload, dict) else None
        if not isinstance(items, list) or not items:
            return None, None, "google books returned no items"

        item0 = items[0] if isinstance(items[0], dict) else {}
        volume = item0.get("volumeInfo") if isinstance(item0.get("volumeInfo"), dict) else {}

        found_isbn13 = None
        identifiers = volume.get("industryIdentifiers") if isinstance(volume.get("industryIdentifiers"), list) else []
        for identifier in identifiers:
            if not isinstance(identifier, dict):
                continue
            val = normalize_isbn(str(identifier.get("identifier") or ""))
            if val:
                found_isbn13 = val
                if len(val) == 13:
                    break

        image_links = volume.get("imageLinks") if isinstance(volume.get("imageLinks"), dict) else {}

        metadata = {
            "title": volume.get("title") or None,
            "authors": volume.get("authors") if isinstance(volume.get("authors"), list) else [],
            "publisher": volume.get("publisher") or None,
            "published_date": volume.get("publishedDate") or None,
            "description": volume.get("description") or None,
            "page_count": volume.get("pageCount"),
            "language": volume.get("language") or None,
            "categories": volume.get("categories") if isinstance(volume.get("categories"), list) else [],
            "cover_image": _best_google_cover(image_links),
            "source": "google_books",
            "source_url": volume.get("infoLink") or None,
        }

        return metadata, found_isbn13, None


def _build_payload(
    row: Dict[str, Any],
    header_map: Dict[str, str],
    timeout_sec: int,
    google_delay_ms: int,
    google_max_retries: int,
    enrich_google: bool,
    google_api_key: str,
) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
    title = _get_value(row, header_map, "Title")
    author = _get_value(row, header_map, "Author")
    isbn10_raw = _get_value(row, header_map, "ISBN")
    isbn13_raw = _get_value(row, header_map, "ISBN13")
    shelf = _get_value(row, header_map, "Exclusive Shelf")
    bookshelves = _get_value(row, header_map, "Bookshelves")
    date_read = _get_value(row, header_map, "Date Read")
    date_added = _get_value(row, header_map, "Date Added")
    book_id = _get_value(row, header_map, "Book Id")
    publisher = _get_value(row, header_map, "Publisher")
    year_published = _get_value(row, header_map, "Year Published")

    if not title:
        return None, "missing title"

    isbn13 = _pick_isbn13(isbn13_raw=isbn13_raw, isbn10_raw=isbn10_raw)

    shelf_value = shelf or "inbox"
    shelf_norm = _normalize_slug(shelf_value)

    bookshelf_tags = []
    for raw_tag in _split_tags(bookshelves):
        tag = _normalize_tag(raw_tag)
        if tag and tag not in bookshelf_tags:
            bookshelf_tags.append(tag)

    tags = ["book"]
    for tag in bookshelf_tags:
        if _normalize_slug(tag) == shelf_norm:
            continue
        if tag not in tags:
            tags.append(tag)

    status = _map_status(shelf, date_read)

    payload: Dict[str, Any] = {
        "isbn13": isbn13,
        "shelf": shelf_value,
        "tags": tags,
        "metadata": {
            "title": title,
            "authors": [author] if author else [],
            "categories": bookshelf_tags,
            "description": None,
            "publisher": publisher or None,
            "published_date": year_published or None,
            "page_count": None,
            "language": None,
            "cover_image": None,
            "source": "goodreads_csv",
            "source_url": None,
        },
    }

    if enrich_google:
        meta_enriched, enriched_isbn13, _warn = _google_books_enrich(
            title=title,
            author=author,
            isbn13=isbn13,
            timeout_sec=timeout_sec,
            delay_ms=google_delay_ms,
            max_retries=google_max_retries,
            api_key=google_api_key,
        )
        if meta_enriched:
            for k, v in meta_enriched.items():
                if v in (None, "", []):
                    continue
                payload["metadata"][k] = v
            if not payload.get("isbn13") and enriched_isbn13:
                payload["isbn13"] = enriched_isbn13

    return payload, None


def migrate_csv(
    csv_path: str,
    vault_path: str,
    notes_dir: str,
    dry_run: bool = True,
    group_by_shelf: bool = False,
    enrich_google: bool = True,
) -> Dict[str, Any]:
    path = Path(csv_path).expanduser()
    if not path.exists():
        return make_result(STAGE, ok=False, error=f"csv file not found: {path}")

    timeout_sec = get_env_int("BOOK_CAPTURE_HTTP_TIMEOUT_SECONDS", 12, minimum=2)
    google_delay_ms = get_env_int("BOOK_CAPTURE_GOOGLE_DELAY_MS", 400, minimum=50)
    google_max_retries = get_env_int("BOOK_CAPTURE_GOOGLE_MAX_RETRIES", 5, minimum=0)
    google_api_key = get_env_str("BOOK_CAPTURE_GOOGLE_API_KEY", "")

    created = 0
    updated = 0
    unchanged = 0
    skipped = 0
    moved = 0
    errors: List[Dict[str, Any]] = []

    vault = Path(vault_path).expanduser()
    root = vault / Path(notes_dir)

    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        if not reader.fieldnames:
            return make_result(STAGE, ok=False, error="csv has no header")

        header_map = _normalize_header_map({name: name for name in reader.fieldnames})

        for idx, row in enumerate(reader, start=2):
            payload, err = _build_payload(
                row=row,
                header_map=header_map,
                timeout_sec=timeout_sec,
                google_delay_ms=google_delay_ms,
                google_max_retries=google_max_retries,
                enrich_google=enrich_google,
                google_api_key=google_api_key,
            )
            if err or payload is None:
                skipped += 1
                errors.append({"line": idx, "error": err or "invalid row"})
                continue

            if dry_run:
                unchanged += 1
                continue

            result = upsert_note(payload=payload, vault_path=vault_path, notes_dir=notes_dir, target_note=None)
            if not result.get("ok"):
                skipped += 1
                errors.append({"line": idx, "error": result.get("error") or "upsert failed"})
                continue

            if result.get("created"):
                created += 1
            elif result.get("updated"):
                updated += 1
            else:
                unchanged += 1

            if group_by_shelf:
                note_path = Path(str(result.get("note_path") or ""))
                if note_path.exists():
                    shelf_value = str(payload.get("shelf") or "inbox")
                    shelf_dir = root / _shelf_subfolder(shelf_value)
                    shelf_dir.mkdir(parents=True, exist_ok=True)
                    target = shelf_dir / note_path.name
                    if note_path != target:
                        if target.exists():
                            # Keep existing target and remove duplicate source file
                            try:
                                note_path.unlink()
                            except Exception:
                                pass
                        else:
                            note_path.rename(target)
                        moved += 1

    total_processed = created + updated + unchanged + skipped

    return make_result(
        STAGE,
        ok=True,
        error=None,
        csv_path=str(path),
        dry_run=dry_run,
        stats={
            "created": created,
            "updated": updated,
            "unchanged": unchanged,
            "skipped": skipped,
            "moved": moved,
            "total_processed": total_processed,
        },
        errors=errors[:200],
    )


def _self_check() -> Dict[str, Any]:
    sample_payload, err = _build_payload(
        row={
            "Title": "Sample Book",
            "Author": "Sample Author",
            "ISBN": "0306406152",
            "ISBN13": "",
            "Exclusive Shelf": "read",
            "Bookshelves": "non-fiction,science",
            "Date Read": "2025/01/01",
            "Date Added": "2024/01/01",
            "Book Id": "123",
            "Publisher": "Example Press",
            "Year Published": "2024",
        },
        header_map={
            "title": "Title",
            "author": "Author",
            "isbn": "ISBN",
            "isbn13": "ISBN13",
            "exclusive shelf": "Exclusive Shelf",
            "bookshelves": "Bookshelves",
            "date read": "Date Read",
            "date added": "Date Added",
            "book id": "Book Id",
            "publisher": "Publisher",
            "year published": "Year Published",
        },
        timeout_sec=2,
        google_delay_ms=100,
        google_max_retries=0,
        enrich_google=False,
        google_api_key="",
    )

    ok = sample_payload is not None and err is None and sample_payload.get("status") == "finished"
    return make_result(
        STAGE,
        ok=ok,
        error=err,
        checks={
            "isbn13": sample_payload.get("isbn13") if sample_payload else None,
            "status": sample_payload.get("status") if sample_payload else None,
            "shelf": sample_payload.get("shelf") if sample_payload else None,
            "has_book_tag": "book" in (sample_payload.get("tags") or []) if sample_payload else False,
        },
    )


def main(argv: List[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--csv", help="Path to Goodreads CSV export")
    parser.add_argument("--vault-path", default=get_env_str("BOOK_CAPTURE_VAULT_PATH", ""), help="Obsidian vault root (required)")
    parser.add_argument("--notes-dir", default=get_env_str("BOOK_CAPTURE_NOTES_DIR", "6. Library"), help="Notes directory inside vault")
    parser.add_argument("--dry-run", action="store_true", help="Parse and validate without writing notes")
    parser.add_argument("--group-by-shelf", action="store_true", help="Store notes inside per-shelf subfolders")
    parser.add_argument("--no-google-enrich", action="store_true", help="Disable Google Books enrichment")
    parser.add_argument("--self-check", action="store_true", help="Run internal quick checks")
    args = parser.parse_args(argv)

    if args.self_check:
        result = _self_check()
        print_json(result)
        return 0 if result.get("ok") else 1

    if not args.csv:
        return fail_and_print(STAGE, "--csv is required")

    if not args.vault_path.strip():
        return fail_and_print(STAGE, "--vault-path is required (or set BOOK_CAPTURE_VAULT_PATH)")

    group_by_shelf = args.group_by_shelf or get_env_bool("BOOK_CAPTURE_GROUP_BY_SHELF", False)
    enrich_google = (not args.no_google_enrich) and get_env_bool("BOOK_CAPTURE_ENABLE_GOOGLE_ENRICH", True)

    result = migrate_csv(
        csv_path=args.csv,
        vault_path=args.vault_path,
        notes_dir=args.notes_dir,
        dry_run=args.dry_run,
        group_by_shelf=group_by_shelf,
        enrich_google=enrich_google,
    )
    print_json(result)
    return 0 if result.get("ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())

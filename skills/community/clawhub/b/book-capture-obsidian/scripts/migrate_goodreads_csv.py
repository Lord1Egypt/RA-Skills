#!/usr/bin/env python3
"""Migrate a Goodreads CSV export into Obsidian notes.

Without --dry-run this creates and updates notes in the vault (user notes are
kept) and, with --group-by-shelf, moves notes into shelf folders. Enrichment
sends each book's ISBN or title and author to Open Library and, for missing
fields, Google Books; --no-enrich keeps everything local.
"""

from __future__ import annotations

import argparse
import csv
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from common_config import get_env_bool, get_env_str
from common_isbn import normalize_isbn
from common_json import fail_and_print, make_result, print_json
from metadata_resolver import MetadataResolver
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
    """Single safe folder name for a shelf: letters, digits and hyphens only."""
    slug = re.sub(r"[^a-z0-9-]+", "-", _normalize_slug(shelf)).strip("-")
    return slug or "unknown"


def _pick_isbn13(isbn13_raw: str, isbn10_raw: str) -> Optional[str]:
    normalized_13 = normalize_isbn(isbn13_raw or "")
    if normalized_13:
        return normalized_13
    normalized_10 = normalize_isbn(isbn10_raw or "")
    if normalized_10:
        return normalized_10
    return None


def _build_payload(
    row: Dict[str, Any],
    header_map: Dict[str, str],
    resolver: Optional[MetadataResolver] = None,
) -> Tuple[Optional[Dict[str, Any]], Optional[str], List[str]]:
    """Map one CSV row to an upsert payload; enrich only when a resolver is given."""
    title = _get_value(row, header_map, "Title")
    author = _get_value(row, header_map, "Author")
    isbn10_raw = _get_value(row, header_map, "ISBN")
    isbn13_raw = _get_value(row, header_map, "ISBN13")
    shelf = _get_value(row, header_map, "Exclusive Shelf")
    bookshelves = _get_value(row, header_map, "Bookshelves")
    publisher = _get_value(row, header_map, "Publisher")
    year_published = _get_value(row, header_map, "Year Published")

    if not title:
        return None, "missing title", []

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

    payload: Dict[str, Any] = {
        "isbn13": isbn13,
        "goodreads_book_id": _get_value(row, header_map, "Book Id") or None,
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

    warnings: List[str] = []
    if resolver is not None:
        enriched, enriched_isbn13, warnings = resolver.lookup(
            isbn13=isbn13,
            title=title,
            author=author,
            base=payload["metadata"],
        )
        if enriched:
            enriched["source"] = "goodreads_csv"
            payload["metadata"] = enriched
        if not payload.get("isbn13") and enriched_isbn13:
            payload["isbn13"] = enriched_isbn13

    return payload, None, warnings


def migrate_csv(
    csv_path: str,
    vault_path: str,
    notes_dir: str,
    dry_run: bool = True,
    group_by_shelf: bool = False,
    enrich: bool = True,
    limit: int = 0,
    resolver: Optional[MetadataResolver] = None,
) -> Dict[str, Any]:
    path = Path(csv_path).expanduser()
    if not path.exists():
        return make_result(STAGE, ok=False, error=f"csv file not found: {path}")

    # A dry run never touches the network, so it cannot burn API quota.
    if enrich and not dry_run and resolver is None:
        resolver = MetadataResolver.from_env()
    active_resolver = resolver if (enrich and not dry_run) else None

    created = 0
    updated = 0
    unchanged = 0
    skipped = 0
    moved = 0
    errors: List[Dict[str, Any]] = []
    warning_counts: Dict[str, int] = {}

    vault = Path(vault_path).expanduser().resolve()
    root = (vault / Path(notes_dir)).resolve()
    if root != vault and vault not in root.parents:
        return make_result(STAGE, ok=False, error=f"notes directory escapes the vault: {root}")

    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        if not reader.fieldnames:
            return make_result(STAGE, ok=False, error="csv has no header")

        header_map = _normalize_header_map({name: name for name in reader.fieldnames})

        for idx, row in enumerate(reader, start=2):
            if limit and idx - 1 > limit:
                break
            payload, err, row_warnings = _build_payload(
                row=row,
                header_map=header_map,
                resolver=active_resolver,
            )
            for warning in row_warnings:
                warning_counts[warning] = warning_counts.get(warning, 0) + 1
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
                    shelf_dir = (root / _shelf_subfolder(str(payload.get("shelf") or "inbox"))).resolve()
                    target = shelf_dir / note_path.name
                    if note_path.resolve() != target:
                        if target.exists():
                            # Never delete or overwrite: a same-named note may be a different book.
                            errors.append({"line": idx, "error": f"not moved, target exists: {target.name}"})
                        else:
                            shelf_dir.mkdir(parents=True, exist_ok=True)
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
        enrichment={
            "enabled": active_resolver is not None,
            "stats": active_resolver.stats.as_dict() if active_resolver is not None else None,
            "warnings": dict(sorted(warning_counts.items())),
        },
    )


def _self_check() -> Dict[str, Any]:
    sample_payload, err, _warnings = _build_payload(
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
    )

    has_status_key = bool(sample_payload and "status" in sample_payload)
    ok = (
        sample_payload is not None
        and err is None
        and sample_payload.get("isbn13") == "9780306406157"
        and sample_payload.get("shelf") == "read"
        and "book" in (sample_payload.get("tags") or [])
        and not has_status_key
    )
    return make_result(
        STAGE,
        ok=ok,
        error=err,
        checks={
            "isbn13": sample_payload.get("isbn13") if sample_payload else None,
            "status": sample_payload.get("status") if sample_payload else None,
            "has_status_key": has_status_key,
            "shelf": sample_payload.get("shelf") if sample_payload else None,
            "has_book_tag": "book" in (sample_payload.get("tags") or []) if sample_payload else False,
        },
    )


def main(argv: List[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--csv", help="Path to Goodreads CSV export")
    parser.add_argument("--vault-path", default=get_env_str("BOOK_CAPTURE_VAULT_PATH", ""), help="Obsidian vault root (required)")
    parser.add_argument("--notes-dir", default=get_env_str("BOOK_CAPTURE_NOTES_DIR", "Books"), help="Notes directory inside vault")
    parser.add_argument("--dry-run", action="store_true", help="Parse and validate without writing notes")
    parser.add_argument("--group-by-shelf", action="store_true", help="Store notes inside per-shelf subfolders")
    parser.add_argument("--no-enrich", "--no-google-enrich", dest="no_enrich", action="store_true", help="Use only the CSV data, with no metadata lookups")
    parser.add_argument("--limit", type=int, default=0, help="Process only the first N rows (0 = all)")
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
    enrich = (not args.no_enrich) and get_env_bool(
        "BOOK_CAPTURE_ENABLE_ENRICH", get_env_bool("BOOK_CAPTURE_ENABLE_GOOGLE_ENRICH", True)
    )

    result = migrate_csv(
        csv_path=args.csv,
        vault_path=args.vault_path,
        notes_dir=args.notes_dir,
        dry_run=args.dry_run,
        group_by_shelf=group_by_shelf,
        enrich=enrich,
        limit=max(0, args.limit),
    )
    print_json(result)
    return 0 if result.get("ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())

# Data Contracts

Contents: [1) ISBN Extraction Output (`extract_isbn.py`)](#1-isbn-extraction-output-extract_isbnpy) · [2) Metadata Resolution Output (`resolve_metadata.py`)](#2-metadata-resolution-output-resolve_metadatapy) · [3) Upsert Input Contract (`upsert_obsidian_note.py`)](#3-upsert-input-contract-upsert_obsidian_notepy) · [4) Upsert Output Contract](#4-upsert-output-contract) · [5) Photo Ingest Output (`ingest_photo.py`)](#5-photo-ingest-output-ingest_photopy) · [6) Migration Output (`migrate_goodreads_csv.py`)](#6-migration-output-migrate_goodreads_csvpy) · [7) Dashboard Output (`generate_dashboard.py`)](#7-dashboard-output-generate_dashboardpy) · [Safety Rules](#safety-rules)

All scripts return deterministic JSON envelopes:

```json
{
  "stage": "string",
  "ok": true,
  "error": null
}
```

Additional fields vary per stage.

Secrets are excluded from every envelope, including provider warnings. Metadata responses are normalized before they enter these contracts.

## 1) ISBN Extraction Output (`extract_isbn.py`)

```json
{
  "stage": "extract_isbn",
  "ok": true,
  "error": null,
  "source_image": "...",
  "method": "barcode|ocr",
  "isbn13": "978...",
  "isbn_candidates": ["978..."],
  "warnings": []
}
```

## 2) Metadata Resolution Output (`resolve_metadata.py`)

```json
{
  "stage": "resolve_metadata",
  "ok": true,
  "error": null,
  "isbn13": "978...",
  "metadata": {
    "title": "...",
    "authors": ["..."],
    "publisher": "...",
    "published_date": "...",
    "description": "...",
    "page_count": 123,
    "language": "en",
    "categories": ["..."],
    "cover_image": "...",
    "source": "openlibrary|google_books",
    "source_url": "..."
  },
  "warnings": []
}
```

## 3) Upsert Input Contract (`upsert_obsidian_note.py`)

```json
{
  "isbn13": "978...",
  "tags": ["book", "science", "philosophy"],
  "metadata": {
    "title": "...",
    "authors": ["..."],
    "publisher": "...",
    "published_date": "...",
    "description": "...",
    "page_count": 123,
    "language": "en",
    "categories": ["..."],
    "cover_image": "...",
    "source": "photo|goodreads_csv|manual",
    "source_url": "..."
  }
}
```

Optional top-level keys: `shelf` (default `inbox`), `goodreads_book_id` (identity when there is no ISBN).

`published_date` is used to derive `year` and is not stored in the note frontmatter.

## 4) Upsert Output Contract

```json
{
  "stage": "upsert_obsidian_note",
  "ok": true,
  "error": null,
  "note_path": "...",
  "created": true,
  "updated": true,
  "preserved_user_content": false,
  "isbn13": "978...",
  "title": "...",
  "shelf": "inbox",
  "tags": ["book", "science-fiction"],
  "related_links": ["[[Books/...]]"]
}
```

## 5) Photo Ingest Output (`ingest_photo.py`)

```json
{
  "stage": "ingest_photo",
  "ok": true,
  "error": null,
  "image_path": "...",
  "isbn13": "978...",
  "note_path": "...",
  "extract": {"...": "..."},
  "metadata": {"...": "..."},
  "upsert": {"...": "..."},
  "warnings": []
}
```

The ingest pipeline does not call the note upsert when ISBN extraction or metadata resolution fails. Provider fallback details remain in `warnings`.

## 6) Migration Output (`migrate_goodreads_csv.py`)

```json
{
  "stage": "migrate_goodreads_csv",
  "ok": true,
  "error": null,
  "csv_path": "...",
  "dry_run": true,
  "stats": {
    "created": 0,
    "updated": 0,
    "unchanged": 0,
    "skipped": 0,
    "moved": 0,
    "total_processed": 0
  },
  "errors": [],
  "enrichment": {
    "enabled": true,
    "stats": {
      "cache_hits": 0,
      "network_calls": {"openlibrary": 0, "google_books": 0},
      "google_skipped_cooldown": 0,
      "google_skipped_budget": 0,
      "rate_limited": {"openlibrary": 0, "google_books": 0}
    },
    "warnings": {"<warning text>": 0}
  }
}
```

`network_calls.google_books` counts HTTP attempts, including retries, against the per-run budget.

## 7) Dashboard Output (`generate_dashboard.py`)

```json
{
  "stage": "generate_dashboard",
  "ok": true,
  "error": null,
  "dashboard_path": "...",
  "updated": true,
  "counts": {
    "total_books": 0,
    "to_read_count": 0,
    "reading_count": 0,
    "finished_count": 0,
    "inbox_count": 0
  },
  "shelves": {"read": 0}
}
```

## Safety Rules

- Never include credentials, tokens, or personal identifiers in any contract.
- Keep output deterministic (stable keys and value types) to simplify automation.

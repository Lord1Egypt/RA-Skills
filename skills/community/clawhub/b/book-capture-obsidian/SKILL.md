---
name: book-capture-obsidian
description: Capture and normalize book metadata into Obsidian Markdown notes from photos or Goodreads CSV exports. Use for barcode and OCR ISBN extraction, metadata enrichment, idempotent note upsert, bulk migration, and dashboard generation.
---

# Book Capture Obsidian

Execute this workflow to add or migrate books into an Obsidian vault.

## Workflow

1. Ask the user for the destination Obsidian vault path if missing.
2. Read `references/configuration.md` and set environment variables.
3. Choose one mode:
   - Photo ingest with `scripts/ingest_photo.py`
   - Goodreads CSV migration with `scripts/migrate_goodreads_csv.py`
4. For Goodreads migration, prefer `--group-by-shelf` and Google enrichment enabled.
5. Upsert notes with `scripts/upsert_obsidian_note.py`.
6. Refresh the dashboard with `scripts/generate_dashboard.py`.
7. Run validation and security checks:
   - `sh scripts/run_ci_local.sh`
   - `sh scripts/security_scan_no_pii.sh`

## Required References

- `references/configuration.md` for runtime settings and portability
- `references/data-contracts.md` for normalized schema and output contracts
- `references/migration-runbook.md` for Goodreads import sequence
- `references/troubleshooting.md` for extraction and merge failures

## Operating Rules

- Require explicit vault destination (`BOOK_CAPTURE_VAULT_PATH` or `--vault-path`) before bulk writes.
- Prefer barcode extraction first; use OCR as fallback.
- Keep filenames human-readable (`Title - Author (Publisher, Year)`).
- Keep `shelf` as property and include tag `book` in all notes.
- Use shared compact series tags (for example `theexpanse`, `harrypotter`) when volume metadata exists; avoid separate series hub notes.
- Preserve user notes section during updates.
- Keep outputs deterministic and idempotent for repeated runs.
- Do not store secrets or personal identifiers in generated artifacts.
- Simplified frontmatter: keep only `title`, `author`, `publisher`, `year`, `isbn_10`, `isbn_13`, `cover`, `shelf`, `source`, `source_url`, `tags`. Remove `published_date`, `genre`, `status`, `date_started`, `date_read`, `needs_review`, `goodreads_book_id`.

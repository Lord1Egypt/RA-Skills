# Goodreads CSV Migration Runbook

Use this runbook to migrate Goodreads exports into Obsidian notes safely.

## Input

- Goodreads CSV export file
- Configured vault path (`BOOK_CAPTURE_VAULT_PATH`)
- Configured notes dir (`BOOK_CAPTURE_NOTES_DIR`)

## Preflight

1. Ensure CSV is UTF-8 (`utf-8-sig` is accepted).
2. Ensure required columns exist:
   - `Title`, `Author`, `ISBN`, `ISBN13`, `Exclusive Shelf`
3. Install dependencies (`requirements.txt` + `requirements-dev.txt` for tests).
4. Run security scan before release packaging:
   - `sh scripts/security_scan_no_pii.sh`
5. Set migration controls:
   - `BOOK_CAPTURE_ENABLE_GOOGLE_ENRICH=true`
   - `BOOK_CAPTURE_GOOGLE_DELAY_MS`
   - `BOOK_CAPTURE_GOOGLE_MAX_RETRIES`

## Dry Run First

```bash
python skill/book-capture-obsidian/scripts/migrate_goodreads_csv.py \
  --csv ./input/goodreads_library_export.csv \
  --vault-path "$BOOK_CAPTURE_VAULT_PATH" \
  --notes-dir "$BOOK_CAPTURE_NOTES_DIR" \
  --group-by-shelf \
  --dry-run
```

Review output stats and row-level errors.

## Live Migration

```bash
python skill/book-capture-obsidian/scripts/migrate_goodreads_csv.py \
  --csv ./input/goodreads_library_export.csv \
  --vault-path "$BOOK_CAPTURE_VAULT_PATH" \
  --notes-dir "$BOOK_CAPTURE_NOTES_DIR" \
  --group-by-shelf
```

## Mapping Rules

- `Title` -> note title
- `Author` -> `author`
- `ISBN13` / `ISBN` -> `isbn_13` (when available)
- `Book Id` -> `goodreads_book_id` (fallback identity key)
- `Exclusive Shelf` -> `shelf` property
- `Date Read` -> `status=finished` fallback when shelf is custom
- `Bookshelves` -> tags + categories
- Always include tag `book`
- Add normalized tag `shelf-<exclusive-shelf>`
- Query Google Books for all rows to enrich synopsis/publisher/date/metadata

## Output Shape

- Filename format: `Title - First Author - Publisher - Year.md`
- No auto markers (`BOOK_CAPTURE:BEGIN/END AUTO`)
- No metadata audit boilerplate section
- Keep `## Sinopse` with concise description text

## Dedup Strategy

- Primary: `isbn_13`
- Fallback: `goodreads_book_id`
- If note exists, perform idempotent update
- Preserve user notes section

## Post Migration

1. Refresh dashboard:

```bash
python skill/book-capture-obsidian/scripts/generate_dashboard.py \
  --vault-path "$BOOK_CAPTURE_VAULT_PATH" \
  --notes-dir "$BOOK_CAPTURE_NOTES_DIR" \
  --dashboard-file "$BOOK_CAPTURE_DASHBOARD_FILE"
```

2. Validate random sample notes for metadata quality.
3. Re-run migration after API cooldown when Google returns 429 rate limits.

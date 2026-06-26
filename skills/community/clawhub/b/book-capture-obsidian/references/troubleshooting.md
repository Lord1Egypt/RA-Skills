# Troubleshooting

## 1) No ISBN extracted

Symptoms:
- `extract_isbn.py` returns `ok=false` with `no valid ISBN found`

Checks:
- Ensure barcode is visible and in focus.
- Confirm at least one extraction path is installed:
  - `zbarimg` or `pyzbar`
  - OCR fallback (`pytesseract` + `tesseract` binary)
- Run self-check:

```bash
python skill/book-capture-obsidian/scripts/extract_isbn.py --self-check
```

## 2) Metadata not found

Symptoms:
- `resolve_metadata.py` returns `ok=false`

Checks:
- Verify ISBN is valid.
- Confirm internet access for API requests.
- Increase timeout if needed:

```bash
export BOOK_CAPTURE_HTTP_TIMEOUT_SECONDS=20
```

- Change provider order:

```bash
export BOOK_CAPTURE_METADATA_PROVIDER_ORDER="openlibrary,google_books"
```

## 3) Notes not updating as expected

Symptoms:
- metadata changed but note content looks stale

Checks:
- Confirm write target (`BOOK_CAPTURE_VAULT_PATH`, `BOOK_CAPTURE_NOTES_DIR`).
- Check script result fields `created`, `updated`, `preserved_user_content`.
- Ensure auto-managed markers exist:
  - `<!-- BOOK_CAPTURE:BEGIN AUTO -->`
  - `<!-- BOOK_CAPTURE:END AUTO -->`

## 4) CI fails on clean machine

Symptoms:
- `scripts/run_ci_local.sh` fails with `No module named pytest`

Fix:

```bash
pip install -r requirements-dev.txt
```

Then rerun:

```bash
sh scripts/run_ci_local.sh
```

## 5) Security scan fails

Symptoms:
- `scripts/security_scan_no_pii.sh` finds secrets or personal data

Fix:
- Remove leaked values and replace with placeholders.
- Remove hardcoded local paths.
- Re-run scan until clean.

## 6) Migration skips many rows

Symptoms:
- `migrate_goodreads_csv.py` reports high `skipped`

Most common causes:
- missing title
- invalid or missing ISBN
- malformed CSV columns

Fix:
- Validate CSV header names.
- Keep dry-run enabled until row-level errors are under control.

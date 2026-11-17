# Troubleshooting

## No ISBN extracted from a photo

`extract_isbn.py` returns `ok=false` with `no valid ISBN found`.

- Check the barcode is sharp and fills a good part of the frame; a photo of the back cover works best.
- Run `PY {baseDir}/scripts/extract_isbn.py --diagnose-deps` to see which of `zbarimg`, `pyzbar`, `pytesseract` and `tesseract` are available. Install `zbar-tools` (Debian/Ubuntu) or `zbar` (Homebrew) for barcodes, `tesseract-ocr` for OCR.
- If OCR times out, raise `BOOK_CAPTURE_TESSERACT_TIMEOUT_SECONDS`.
- Otherwise ask the user for the ISBN or title and use `resolve_metadata.py`.

## Metadata not found, or notes without a description

- `warnings` lists each provider's answer. `openlibrary returned no entry` and `google books returned no items` are real misses; try a title lookup.
- `cooling down` or `per-run request budget reached`: the guard paused Google. Keep the cache; resume after the reported wait and actual quota reset. Only selected providers may fill gaps; Google-only can leave metadata missing.
- `google books quota limit (403)`: check the project's Books quota. Ordinary 400/403 can instead mean a bad request, disabled API or incompatible key restriction; inspect the Cloud console without logging the key. See [API requirements](configuration.md#metadata-providers-and-api-requirements).
- `found no close title/author match`: candidates did not match; request an ISBN rather than choosing another book.
- For stale/wrong cached metadata, verify the source then clear the cache only if needed. This also removes cooldown state: wait out any active quota pause first.

## A note did not update

- Check `created`, `updated` and `note_path` in the JSON.
- Notes are matched by `isbn_13`, then `goodreads_book_id`. A note created by hand without either field is not matched; add `isbn_13` to its frontmatter.
- Everything above `## User Notes` is regenerated on each run; write personal notes below that heading.

## The dashboard shows zero books

- `--notes-dir` (or `BOOK_CAPTURE_NOTES_DIR`) must point at the folder that holds the notes.
- Status counts come from the `shelf` property. Custom shelf names can be mapped with `BOOK_CAPTURE_SHELVES_TO_READ`, `BOOK_CAPTURE_SHELVES_READING` and `BOOK_CAPTURE_SHELVES_READ`.
- The tables need the Dataview community plugin in Obsidian.

## The Goodreads import skips rows

`errors` names the line and reason. A row without a title is always skipped. Encoding errors usually mean the file was re-saved in another program; export again from Goodreads.

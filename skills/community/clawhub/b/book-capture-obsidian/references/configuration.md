# Configuration

Every setting is an environment variable; command-line flags win where both exist. Nothing is machine-specific by default.

## Windows setup

Use Python 3.10+ in a skill-local environment:

```powershell
python -m venv "<skill>/.venv"
& "<skill>/.venv/Scripts/python.exe" -m pip install -r "<skill>/requirements.txt"
```

Use that interpreter as `PY` in the workflows. Photo extraction also needs the selected barcode/OCR runtime; diagnose before installing missing components.

## Paths

| Variable | Default | Meaning |
| --- | --- | --- |
| `BOOK_CAPTURE_VAULT_PATH` | none (required) | Obsidian vault root. Scripts refuse to write without an existing directory. |
| `BOOK_CAPTURE_NOTES_DIR` | `Books` | Folder for book notes, relative to the vault. |
| `BOOK_CAPTURE_DASHBOARD_FILE` | `<notes dir>/Library Dashboard.md` | Dashboard note, relative to the vault. |
| `BOOK_CAPTURE_DASHBOARD_TEMPLATE` | the skill's `assets/templates/library-dashboard-template.md` | Custom dashboard template. |
| `BOOK_CAPTURE_TARGET_NOTE` | none | Write one capture to this exact note path (must be inside the vault). |
| `BOOK_CAPTURE_RELATED_DIRS` | none | Comma-separated vault folders to search for related notes, besides the books folder. |

## Notes

| Variable | Default | Meaning |
| --- | --- | --- |
| `BOOK_CAPTURE_NOTE_LANGUAGE` | `en` | `pt` writes `## Sinopse` and Portuguese fallback text; anything else writes English. |
| `BOOK_CAPTURE_GROUP_BY_SHELF` | `false` | Goodreads import files notes in one subfolder per shelf. |
| `BOOK_CAPTURE_SHELVES_TO_READ` | `to-read,want-to-read,tbr` | Shelves counted as "to read" on the dashboard. |
| `BOOK_CAPTURE_SHELVES_READING` | `currently-reading,reading` | Shelves counted as "reading". |
| `BOOK_CAPTURE_SHELVES_READ` | `read,finished` | Shelves counted as "read". |

## Metadata providers and API requirements

Set `BOOK_CAPTURE_METADATA_PROVIDER_ORDER` to `google_books`, `openlibrary`, `google_books,openlibrary` or `openlibrary,google_books` (default). This controls every lookup workflow. Only listed providers run; the first result wins and later providers fill gaps. Trusted CSV/input fields are never overwritten. Cache entries are provider-specific.

Google-only, in PowerShell:

```powershell
$env:BOOK_CAPTURE_METADATA_PROVIDER_ORDER = "google_books"
$env:BOOK_CAPTURE_GOOGLE_MAX_REQUESTS_PER_RUN = "100"
```

In Bash: `export BOOK_CAPTURE_METADATA_PROVIDER_ORDER=google_books`. Supply `BOOK_CAPTURE_GOOGLE_API_KEY` through your private environment/secret configuration, never a note or committed file.

**Google Books requirements:** select your Cloud project, enable the Books API, create an API key restricted to Books, and set compatible application restrictions for the machine running the scripts. [Google requires application identification](https://developers.google.com/books/docs/v1/using#auth); this client uses an API key for public metadata, not OAuth/private shelves. Legacy keyless attempts remain supported by the client but are not a reliable quota plan.

**Limits:** inspect that project's Books API quotas under APIs & Services. Billing alone does not establish a higher Books limit, and no fixed daily allowance is assumed here. Quota is shared with other applications using the project. If needed, [request an increase where available](https://docs.cloud.google.com/docs/quotas/view-manage); availability and approval are not guaranteed. Until approved, cache results, pace requests, budget small batches and resume after the applicable reset/backoff. Switching keys in the same project does not create more project quota.

**Open Library:** no key; the default one-second gap follows its [unidentified-client limit](https://openlibrary.org/developers/api). Identified clients can use its documented higher rate. It discourages bulk per-book downloads: use CSV-only import first for large libraries.

| Variable | Default | Meaning |
| --- | --- | --- |
| `BOOK_CAPTURE_ENABLE_ENRICH` | `true` | `false`: Goodreads CSV only. Legacy `BOOK_CAPTURE_ENABLE_GOOGLE_ENRICH` remains supported. |
| `BOOK_CAPTURE_GOOGLE_MAX_REQUESTS_PER_RUN` | `100` | Maximum Google HTTP attempts per resolver/run, including retries. Not a project-wide quota controller. |
| `BOOK_CAPTURE_GOOGLE_MIN_INTERVAL_MS` | `1000` | Minimum gap between Google attempts, including retries, within one run. Adjust to your actual quota. |
| `BOOK_CAPTURE_GOOGLE_COOLDOWN_SECONDS` | `3600` | Persisted pause after exhausted 429 retries or recognized quota-related 403. A longer server wait wins. |
| `BOOK_CAPTURE_GOOGLE_MAX_RETRIES` | `2` | Retries for network errors, 429 and 5xx. Quota-related 403 defers immediately. |
| `BOOK_CAPTURE_GOOGLE_DELAY_MS` | `400` | Exponential retry backoff base; separate from steady request spacing. |
| `BOOK_CAPTURE_GOOGLE_MAX_RETRY_AFTER_SECONDS` | `10` | Maximum in-process wait per retry. Longer `Retry-After` defers the provider, never retries early. |
| `BOOK_CAPTURE_OPENLIBRARY_DELAY_MS` | `1000` | Minimum Open Library request gap within one run. |
| `BOOK_CAPTURE_HTTP_TIMEOUT_SECONDS` | `12` | Per-request timeout. |
| `BOOK_CAPTURE_USER_AGENT` | `book-capture-obsidian/1.4 (+repo URL)` | API client identification; include contact details for Open Library's identified-client rate. |
| `BOOK_CAPTURE_CACHE` | `on` | `off`: cache and cooldowns last only for the current process. |
| `BOOK_CAPTURE_CACHE_DIR` | `$XDG_CACHE_HOME/book-capture-obsidian` or `~/.cache/book-capture-obsidian` | Stores `metadata.sqlite3`. |

Found books cache for 180 days; misses for 14 days. Transient failures are not cached as misses. Valid cache entries work during cooldowns. Keep one import worker: per-run budgets/pacing do not coordinate simultaneous processes. With disk caching disabled or unavailable, cooldown cannot survive a restart; retain the reported wait yourself. Do not delete the cache to bypass a quota pause.

## Photo extraction

| Variable | Default | Meaning |
| --- | --- | --- |
| `BOOK_CAPTURE_ENABLE_ZBARIMG` | `true` | Use the `zbarimg` CLI for barcodes. |
| `BOOK_CAPTURE_ZBARIMG_BIN` | `zbarimg` | Path to `zbarimg`. |
| `BOOK_CAPTURE_ZBARIMG_TIMEOUT_SECONDS` | `8` | Barcode timeout. |
| `BOOK_CAPTURE_ENABLE_PYZBAR` | `true` | Use the `pyzbar` library as a second barcode reader. |
| `BOOK_CAPTURE_ENABLE_OCR` | `true` | Fall back to OCR when no barcode is found. |
| `BOOK_CAPTURE_OCR_LANG` | `eng` | Tesseract language codes, for example `eng+por`. |
| `BOOK_CAPTURE_TESSERACT_CMD` | auto | Path to the `tesseract` binary. |
| `BOOK_CAPTURE_TESSERACT_TIMEOUT_SECONDS` | `20` | OCR timeout. |

Missing components degrade in order: `zbarimg`, then `pyzbar`, then `pytesseract`, then the `tesseract` CLI. With none available the result is a deterministic extraction failure.

## Privacy

Scripts leave source photos in place; they do not upload or copy them. They store metadata/cache and Markdown. API keys go only to Google as request parameters and are redacted from outputs. Obsidian may fetch remote covers when displaying notes.

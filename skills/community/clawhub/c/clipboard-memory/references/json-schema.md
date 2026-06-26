# Clipboard Memory — JSON Schema

Stable response shapes for `--format json`. Current `schema_version` is `2`. This file is kept byte-identical across skill packages.

Breaking changes to these fields will bump `schema_version`. Additive changes (new optional keys) are allowed within the same version.

---

## Shared envelope (`recall`, `search`, `recent`, `timeline`)

```json
{
  "schema_version": 2,
  "command": "recall",
  "generated_at": "2026-04-17T12:34:56Z",
  "applied_filters": { "hours": 24, "app": "safari" },
  "truncated": false,
  "next_cursor": null,
  "results": [ /* rows, see below */ ]
}
```

- `schema_version` — integer. Pin to `2` for stability checks.
- `command` — echoes the subcommand.
- `generated_at` — RFC3339 timestamp when the response was produced.
- `applied_filters` — echoes the filters actually applied after argument parsing.
- `truncated` — `true` when more rows exist beyond `--limit`.
- `next_cursor` — opaque string to pass back as `--cursor` when `truncated` is `true`. `null` when there are no more rows.
- `results` — list of flattened snapshot rows.

`recall` adds three extras at the top level:

- `best_candidate` — the top-ranked row (also appears as `results[0]`).
- `why_selected` — short string explaining why `best_candidate` was picked.
- `best_match_confidence` — `"high" | "medium" | "low"`.
- `best_match_score` — float in `[0.0, 1.0]`.
- `quoted_text` — present only when `--quote` is set and usable text exists.

---

## Flattened snapshot row (in `results[]` and `best_candidate`)

Read these first; walk nested `items[].representations[]` only after `get`.

```json
{
  "snapshot_id": 42,
  "event_id": 1000,
  "sha256": "<hex>",
  "kind": "text",
  "observed_at": "2026-04-17T12:00:00Z",
  "first_seen_at": "2026-04-17T11:00:00Z",
  "last_seen_at":  "2026-04-17T12:00:00Z",
  "app_name": "Terminal",
  "app_bundle_id": "com.apple.Terminal",

  "best_text": "git status",
  "best_text_uti": "public.utf8-plain-text",
  "text_fragments": [{ "representation": "public.utf8-plain-text", "text": "git status" }],
  "urls": [],
  "file_paths": [],
  "html_text": null,
  "rtf_text": null,
  "ocr_text": null,
  "ocr_status": null,
  "text_summary": "git status",
  "preview_text": "git status",

  "item_count": 1,
  "total_bytes": 10,
  "capture_count": 3,
  "score": 0.95,
  "why_matched": "full phrase match",
  "matched_fields": ["search_text"],
  "snippet": "git status"
}
```

Fields to read first for common questions:

| Intent | Read |
|---|---|
| "what was the text" | `best_text` (fall back to `text_summary`, `preview_text`) |
| "what URL" | `urls` (array) |
| "what file / path" | `file_paths` (array) |
| "which app" | `app_name` / `app_bundle_id` |
| "when" | `observed_at`, `first_seen_at`, `last_seen_at` |
| "is this binary / image / pdf" | `kind`, presence of `best_text`, `total_bytes` |
| "why did recall pick this" | `why_matched`, `matched_fields`, `score` |

`best_text` can come from OCR for image-only snapshots. In that case, `best_text_uti` is `"com.clipmem.ocr.text"` and `ocr_status` is `"ready"`. If binary-only snapshots have no OCR text, fall through to `clipmem export` with a `uti` drawn from `clipmem get`.

---

## `clipmem get --format json`

```json
{
  "schema_version": 2,
  "command": "get",
  "generated_at": "2026-04-17T12:34:56Z",
  "applied_filters": { },
  "snapshot": {
    "snapshot_id": 42,
    "sha256": "<hex>",
    "kind": "text",
    "best_text": "git status",
    "best_text_uti": "public.utf8-plain-text",
    "text_fragments": [ /* ... */ ],
    "urls": [],
    "file_paths": [],
    "html_text": null,
    "rtf_text": null,
    "ocr_text": null,
    "ocr_status": null,
    "text_summary": "git status",
    "preview_text": "git status",
    "search_text": "git status",
    "item_count": 1,
    "total_bytes": 10,
    "created_at": "2026-04-17T11:00:00Z",
    "capture_count": 3,
    "first_observed_at": "2026-04-17T11:00:00Z",
    "last_observed_at":  "2026-04-17T12:00:00Z",
    "last_frontmost_app_name": "Terminal",
    "last_frontmost_app_bundle_id": "com.apple.Terminal",
    "recent_events": [
      { "event_id": 1000, "observed_at": "2026-04-17T12:00:00Z", "change_count": 123 }
    ],
    "items": [
      {
        "item_index": 0,
        "representations": [
          {
            "uti": "public.utf8-plain-text",
            "size_bytes": 10,
            "is_indexed": true
          }
        ]
      }
    ]
  }
}
```

Raw bytes are **not** included in `get --format json`. The `items[].representations[]` tree gives you the `uti` and `size_bytes` needed to call `clipmem export`. `get` does not accept `--format toon`.

---

## `clipmem capture-once --json`

Returns a single snapshot envelope similar to `get`, describing what was just captured.

---

## `clipmem doctor --json`

```json
{
  "db_path": "/Users/you/Library/Application Support/clipmem/clipmem.sqlite3",
  "sqlite_version": "3.45.1",
  "journal_mode": "wal",
  "fts5_compile_option_present": true,
  "fts5_create_virtual_table_ok": true,
  "compile_options": ["ENABLE_FTS5", "ENABLE_RTREE", "…"]
}
```

`clipmem doctor` communicates failure via **exit code** (non-zero means the SQLite archive is corrupt, missing, or unreadable), not via a JSON `errors` field. `fts5_create_virtual_table_ok: false` means `--mode fts` will fail; use `--mode literal` instead. `fts5_compile_option_present` is the weaker "SQLite was built with FTS5 support" signal and is not sufficient on its own.

---

## Top-level keys an agent should always check

Before trusting a response:

1. `schema_version == 2`.
2. For envelopes: `truncated` and `next_cursor` before concluding "there is nothing else".
3. For rows: `best_text` nullability before claiming "I found the exact text".
4. For `recall`: `best_match_confidence` before committing to `best_candidate`. On `"low"`, surface alternatives.

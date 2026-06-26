# Clipboard Memory — Worked Examples

Concrete input → output walkthroughs. Byte-identical across skill packages.

Each example shows the user's question, the command to run, the shape of the response, and the next step.

---

## Example 1 — "What was that URL I copied from Safari yesterday?"

The user gave a time cue (yesterday) and a source (Safari). Use `recall` with a `--prefer-recent` bias, an `--app` filter, and a generous `--hours` window.

```bash
clipmem recall "url" --prefer-recent --app safari --has-url --hours 48 --format json --limit 5
```

Response (trimmed):

```json
{
  "schema_version": 2,
  "command": "recall",
  "best_candidate": {
    "snapshot_id": 812,
    "best_text": "https://developer.apple.com/documentation/appkit/nspasteboard",
    "urls": ["https://developer.apple.com/documentation/appkit/nspasteboard"],
    "app_name": "Safari",
    "observed_at": "2026-04-16T17:45:00Z",
    "why_matched": "url filter + recency bias"
  },
  "best_match_confidence": "high",
  "alternatives": [ /* ... */ ],
  "next_cursor": null
}
```

Report `best_candidate.urls[0]`. If `best_match_confidence` were `"low"`, enumerate `alternatives` instead.

---

## Example 2 — "Show me everything I copied today, in order"

The user wants chronological events, not deduplicated recent snapshots. Use `timeline` and `toon` for efficient enumeration.

```bash
clipmem timeline --hours 24 --format toon --sort asc --limit 50
```

TOON output (one row per line, tab-separated scalar fields):

```
snapshot_id	observed_at	app_name	kind	best_text
812	2026-04-17T08:02:11Z	Safari	url	https://developer.apple.com/…
813	2026-04-17T08:04:03Z	Terminal	text	git status
813	2026-04-17T08:11:59Z	Terminal	text	git status
...
```

Notice snapshot `813` appears twice — `timeline` shows each capture event, not each unique snapshot. If `truncated` shows more rows exist, re-run with the last row's time as `--until` or request `--format json` and page via `--cursor`.

---

## Example 3 — "Pull the image I copied from that screenshot tool"

Images have no text projection. Use `recall` to find the snapshot, then `get` to discover the representation `uti` and byte size, then `export` to write raw bytes.

```bash
# 1. find the snapshot
clipmem recall "screenshot" --kind image --hours 72 --format json --limit 3
```

```json
{
  "best_candidate": {
    "snapshot_id": 901,
    "kind": "image",
    "best_text": null,
    "total_bytes": 138402,
    "app_name": "CleanShot X"
  }
}
```

```bash
# 2. inspect representations to pick a uti
clipmem get 901 --format json
```

```json
{
  "snapshot": {
    "items": [
      {
        "item_index": 0,
        "representations": [
          { "uti": "public.png", "size_bytes": 138402, "is_indexed": false },
          { "uti": "public.tiff", "size_bytes": 412004, "is_indexed": false }
        ]
      }
    ]
  }
}
```

```bash
# 3. export raw bytes
clipmem export 901 --item 0 --uti public.png --out ./clipboard.png
clipmem export 901 --item 0 --uti public.png --out ./clipboard.png --force
```

`export` writes binary content to `--out` and exits 0 on success. It creates a new file by default; pass `--force` only to replace an existing regular file. There is no `--format` on `export`.

---

## Example 4 — Paginating a large search

The user asks for everything matching a phrase. `search` returns bounded pages; use the cursor to keep going.

```bash
clipmem search "launchctl bootstrap" --mode literal --format json --limit 25
```

```json
{
  "schema_version": 2,
  "command": "search",
  "results": [ /* 25 rows */ ],
  "truncated": true,
  "next_cursor": "eyJvZmZzZXQiOjI1LCJxdWVyeSI6Imxhdw..."
}
```

```bash
clipmem search "launchctl bootstrap" --mode literal --format json --limit 25 \
  --cursor "eyJvZmZzZXQiOjI1LCJxdWVyeSI6Imxhdw..."
```

Stop paginating when `truncated` is `false` or `next_cursor` is `null`.

Cursors are tied to the active query, mode, and filters. Changing any of those mid-pagination invalidates the cursor — start over.

---

## Example 5 — "Give me the exact text, not a summary"

By default `recall` returns a compact form. Force quoted, full text:

```bash
clipmem recall "the SQL migration" --quote --full --format json
```

`best_candidate.best_text` now holds the complete stored text. If it's still truncated (very large clipboards), use `get --format json` and concatenate `text_fragments[].text`.

---

## Example 6 — "Nothing is copied from today" — diagnose first

Don't assume the archive is wrong; the watcher may have stopped.

```bash
./scripts/check-setup.sh
# or, inline
clipmem doctor --json
clipmem service status --json
```

If `clipmem service status --json` reports `stale: true`, the watcher is not running. Tell the user to run `clipmem setup` or `brew services start clipmem` before retrying.

See [troubleshooting.md](troubleshooting.md) for remediation steps.

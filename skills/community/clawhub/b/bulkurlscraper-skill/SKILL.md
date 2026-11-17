---
name: scrape-applied-links
description: Bulk-run render-and-parse (from the render-url package) over every url in a JSON file of job/link objects, and record the resulting rendered_page_N.json / parsed_page_N.json paths back into that file. Use this whenever the task is "scrape all these urls from a JSON file" rather than a single one-off render-and-parse call. Installs the `scrape-applied-links` CLI from PyPI on first use.
---

# scrape-applied-links

A thin batching layer over `render-and-parse` (from the `render-url`
package): it reads a JSON file of objects that each have a `url`, calls
`render-and-parse <url>` once per object, and writes the paths to the two
files that call produces (`rendered_page_N.json`, `parsed_page_N.json`)
back into that same object in the JSON file — so later steps can look up
already-scraped data without re-rendering it.

## Setup

Install the CLI from PyPI. This also pulls in `render-url` (which provides
`render-and-parse`), but Playwright's browser binary still needs a separate
install step. Do this once per environment; skip if
`scrape-applied-links --help` already succeeds.

```bash
pip install scrape-applied-links
playwright install chromium
```

## Input format

The only field this tool requires on an object is `url` — every other
field is optional and passed through untouched. Two input shapes are
accepted:

**A flat list of objects:**

```json
[
  { "url": "https://example.com/careers/123" },
  { "url": "https://example.com/careers/456" }
]
```

**An object mapping arbitrary labels (e.g. dates) to lists of objects:**

```json
{
  "2026-09-16": [
    { "url": "https://example.com/careers/123" },
    { "url": "https://example.com/careers/456" }
  ]
}
```

Objects can carry any extra fields (`company`, `title`, `description`,
etc.) — they are ignored and left as-is. If a `company` field is present
it shows up in log output, but it isn't required.

## Command

```bash
scrape-applied-links [json_file] [options]
```

- `json_file` (optional, positional) — path to the input JSON file.
  Defaults to `links_applied_by_date.json` in the current directory.

### Options

| Flag | Effect |
|---|---|
| `--dry-run` | Print which urls would be processed, without invoking `render-and-parse` at all and without modifying the JSON file. Use this first to sanity-check what a run would do. |
| `--force` | Re-scrape objects that already have a `rendered_page` value recorded from a previous run. Without this flag, already-processed objects are skipped — this makes reruns after a partial failure cheap and idempotent. |
| `--output-dir <dir>` | Directory where `render-and-parse` writes its numbered output files (default: current directory). The recorded `rendered_page` / `parsed_page` paths point into this directory. |

## What it does, step by step

1. Loads `json_file` (a flat list or a label-keyed object of lists) and
   collects every object that has a `url`.
2. Skips objects that already have a `rendered_page` recorded, unless
   `--force` is passed.
3. For each remaining object, in order: records the current highest
   `rendered_page_N.json` / `parsed_page_N.json` index in the output
   directory, runs `render-and-parse <url>` there, then re-checks the
   index to find the new files it created.
4. Writes `rendered_page` and `parsed_page` (the new files' paths) into
   that object, and immediately saves the whole JSON file back to disk —
   so progress is never lost if a later url fails.
5. If any urls fail, prints a summary of them at the end and exits
   non-zero. Successful urls are still saved even if a later one fails.

## Debugging and logs

- This CLI's own progress ("=== [label] company: url ===", counts, final
  failure summary) is printed to **stderr** by design, so stdout stays
  clean if you ever pipe or redirect it.
- It has no `--verbose` flag of its own — verbosity comes from the
  underlying `render-and-parse` call, which streams directly to the
  terminal (nothing is captured or suppressed by this tool). Use
  `render-and-parse`'s own flags for more detail:
  - `render-and-parse --verbose <url>` — logs each pipeline step to stderr.
  - `render-and-parse --log-json <url>` — pretty-prints the full result
    JSON to stderr.
- To debug a single failing url in isolation instead of the whole batch,
  copy it out and run `render-and-parse <url>` directly (see the
  `render-url` skill/package docs) — this reproduces exactly what
  `scrape-applied-links` does internally for one entry, without touching
  the JSON file.
- A non-zero exit code means at least one url failed; the failure summary
  printed at the end lists which ones (with their label/company when
  available) so you can retry just those, e.g. by filtering them into a
  smaller JSON file and re-running with `--force`.
- If output files aren't being detected correctly, confirm `--output-dir`
  (default: cwd) matches wherever `render-and-parse` is actually writing
  `rendered_page_N.json` / `parsed_page_N.json` — the tool determines new
  files by diffing the highest numeric suffix in that directory before and
  after each call.
- Always run with `--dry-run` first when pointing at a new or unfamiliar
  JSON file, to confirm how many urls will be processed before making any
  network calls or file writes.

## Notes

- One `render-and-parse` invocation per url — no concurrency, no
  crawling or link-following beyond what's already listed in the JSON file.
- Re-running the same command is safe and idempotent: already-processed
  entries (those with a `rendered_page`) are skipped unless `--force` is
  given.
- The JSON file is saved after every successfully processed url, not just
  at the end, so an interrupted or partially-failing run keeps its
  progress.

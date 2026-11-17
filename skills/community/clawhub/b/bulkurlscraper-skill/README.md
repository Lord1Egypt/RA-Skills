# scrape-applied-links

A thin batching layer over [`render-and-parse`](https://pypi.org/project/render-url/) (from the `render-url` package). It reads a JSON file of objects that each have a `url`, calls `render-and-parse <url>` once per object, and writes the resulting output paths (`rendered_page_N.json`, `parsed_page_N.json`) back into that same object — so later steps can look up already-scraped data without re-rendering it.

This repo is a **Claude Code skill**: [SKILL.md](SKILL.md) is the instruction file Claude reads to use the `scrape-applied-links` CLI correctly, and [CARD.md](CARD.md) is a quick-reference summary of it.

## Installation

```bash
pip install scrape-applied-links
playwright install chromium
```

`scrape-applied-links` pulls in `render-url` (which provides the `render-and-parse` command) automatically, but Playwright's browser binary needs a separate install step. Do this once per environment — skip it if `scrape-applied-links --help` already runs successfully.

## Usage

```bash
scrape-applied-links [json_file] [options]
```

- `json_file` (optional, positional) — path to the input JSON file. Defaults to `links_applied_by_date.json` in the current directory.

### Options

| Flag | Effect |
|---|---|
| `--dry-run` | Print which URLs would be processed, without calling `render-and-parse` or modifying the JSON file. |
| `--force` | Re-scrape objects that already have a `rendered_page` recorded. Without it, already-processed objects are skipped. |
| `--output-dir <dir>` | Directory where `render-and-parse` writes its numbered output files (default: current directory). |

## Input format

The only required field is `url`; every other field is passed through untouched. Two shapes are accepted:

**Flat list:**

```json
[
  { "url": "https://example.com/careers/123" },
  { "url": "https://example.com/careers/456" }
]
```

**Label-keyed map of lists** (e.g. grouped by date):

```json
{
  "2026-09-16": [
    { "url": "https://example.com/careers/123" },
    { "url": "https://example.com/careers/456" }
  ]
}
```

Extra fields like `company`, `title`, `description` are ignored and left as-is; a `company` field, if present, shows up in log output.

## How it works

1. Loads `json_file` (flat list or label-keyed object of lists) and collects every object that has a `url`.
2. Skips objects that already have a `rendered_page` recorded, unless `--force` is passed.
3. For each remaining object, in order: records the current highest `rendered_page_N.json` / `parsed_page_N.json` index in the output directory, runs `render-and-parse <url>`, then re-checks the index to find the newly created files.
4. Writes `rendered_page` and `parsed_page` (the new files' paths) into that object and immediately saves the whole JSON file back to disk, so progress isn't lost if a later URL fails.
5. If any URLs fail, prints a summary at the end and exits non-zero. Successfully processed URLs are still saved.

## Debugging

- Progress output (`=== [label] company: url ===`, counts, failure summary) goes to **stderr**, keeping stdout clean for piping/redirection.
- There's no `--verbose` flag of its own — verbosity comes from `render-and-parse`, which streams directly to the terminal:
  - `render-and-parse --verbose <url>` — logs each pipeline step to stderr.
  - `render-and-parse --log-json <url>` — pretty-prints the full result JSON to stderr.
- To debug a single failing URL, run `render-and-parse <url>` directly instead of the whole batch.
- A non-zero exit code means at least one URL failed — check the printed failure summary and retry just those (e.g. filter them into a smaller JSON file and rerun with `--force`).
- If output files aren't detected correctly, confirm `--output-dir` matches wherever `render-and-parse` actually writes `rendered_page_N.json` / `parsed_page_N.json`; new files are found by diffing the highest numeric suffix before and after each call.
- Run with `--dry-run` first on any new or unfamiliar JSON file to confirm scope before making network calls or file writes.

## Notes

- One `render-and-parse` invocation per URL — no concurrency, crawling, or link-following beyond what's already in the JSON file.
- Reruns are safe and idempotent: already-processed entries (with `rendered_page` set) are skipped unless `--force` is given.
- The JSON file is saved after every successfully processed URL, not just at the end, so interrupted or partially-failing runs keep their progress.

## Files

- [`SKILL.md`](SKILL.md) — instructions Claude Code reads to invoke this skill correctly.
- [`CARD.md`](CARD.md) — quick-reference summary card.
- `README.md` — this file.

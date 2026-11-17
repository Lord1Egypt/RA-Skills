# Skill Card: scrape-applied-links

| | |
|---|---|
| **Name** | scrape-applied-links |
| **Type** | CLI wrapper skill (Python, PyPI) |
| **Package** | [`scrape-applied-links`](https://pypi.org/project/scrape-applied-links/) |
| **Depends on** | `render-url` (provides `render-and-parse`), Playwright (`chromium`) |
| **Trigger** | "scrape all these urls from a JSON file" — bulk scraping, not a single one-off render-and-parse call |
| **Input** | JSON file of objects with a `url` field (flat list or label-keyed map of lists) |
| **Output** | Same JSON file, updated in place with `rendered_page` / `parsed_page` paths per object |

## One-line summary

Bulk-runs `render-and-parse` over every URL in a JSON file and writes the resulting output file paths back into that same file, so scraped data can be looked up later without re-rendering.

## When to use

- You have a JSON file of job/link objects (each with at least a `url`) and need to scrape/render all of them.
- You want idempotent, resumable batch scraping — reruns skip already-processed entries automatically.
- You do **not** need concurrency or link-following/crawling — it's strictly one `render-and-parse` call per listed URL.

## When *not* to use

- A single one-off URL — call `render-and-parse` directly instead.
- You need crawling/discovery of new links — this tool only processes URLs already present in the input file.

## Quick start

```bash
pip install scrape-applied-links
playwright install chromium

scrape-applied-links links_applied_by_date.json --dry-run   # preview
scrape-applied-links links_applied_by_date.json             # run
```

## Key flags

- `--dry-run` — preview without side effects
- `--force` — re-scrape entries that already have `rendered_page`
- `--output-dir <dir>` — where numbered output files are written/detected

See [SKILL.md](SKILL.md) for full behavior details and [README.md](README.md) for setup/usage documentation.

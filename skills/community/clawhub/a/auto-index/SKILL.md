---
name: auto-index
description: >
  Google Indexing API tool. Use when user wants to submit URLs for Google indexing.
  Supports two modes: "auto-index" (fetch sitemap, diff against cache, submit new URLs)
  and "index-now" (submit specific URLs immediately). Requires a Google Cloud service account
  JSON key with Indexing API enabled and Search Console ownership.
license: MIT
compatibility: Requires uv and Python 3.10+. Dependencies handled automatically via uv inline script metadata.
allowed-tools: Bash(uv:*)
metadata:
  author: asenwang
  version: "1.0.0"
  tags: "google, indexing, seo, sitemap, index-api"
---

# Auto-Index — Google Indexing API

Submit URLs to Google for fast indexing via the [Google Indexing API](https://developers.google.com/search/apis/indexing-api/v3/quickstart).

## Prerequisites

1. **Google Cloud Project** with the Indexing API enabled
2. **Service Account** with a downloaded JSON key file
3. **Google Search Console** — add the service account email as an **Owner** of the property

## Environment

| Variable | Required | Description |
|----------|----------|-------------|
| `GOOGLE_INDEX_SA_KEY` | Yes (or `--sa-key`) | Absolute path to service account JSON key file |

## How to Invoke

Run using `uv run` with the script's absolute path. The script directory is relative to the skill root.

### auto-index — Sitemap diff

Fetches a sitemap, compares against a local cache, and submits only **new** URLs.

```bash
uv run scripts/google_index.py auto-index --sitemap "https://example.com/sitemap.xml"
```

Force re-index all URLs (ignore cache):
```bash
uv run scripts/google_index.py auto-index --sitemap "https://example.com/sitemap.xml" --force
```

### index-now — Submit URL(s) immediately

```bash
uv run scripts/google_index.py index-now --url "https://example.com/new-page"
```

Multiple URLs:
```bash
uv run scripts/google_index.py index-now -u "https://example.com/page1" -u "https://example.com/page2"
```

Notify URL deletion:
```bash
uv run scripts/google_index.py index-now --url "https://example.com/old-page" --delete
```

## CLI Reference

### auto-index

| Flag | Description |
|------|-------------|
| `--sitemap`, `-s` | **(required)** Sitemap URL to fetch |
| `--sa-key`, `-k` | Path to service account JSON key (overrides env) |
| `--force`, `-f` | Re-index all URLs, ignoring cache |

### index-now

| Flag | Description |
|------|-------------|
| `--url`, `-u` | **(required)** URL to submit — repeatable for multiple URLs |
| `--sa-key`, `-k` | Path to service account JSON key (overrides env) |
| `--delete`, `-d` | Notify deletion instead of update |

## Output Format

Both commands output structured JSON:

```json
{
  "meta": {
    "action": "auto-index",
    "sitemap": "https://example.com/sitemap.xml",
    "timestamp": "2026-03-02T02:50:00+00:00",
    "total_in_sitemap": 42,
    "new_urls": 5,
    "submitted": 5,
    "success": 5,
    "failed": 0
  },
  "results": [
    {
      "url": "https://example.com/new-page",
      "status": 200,
      "notifyTime": "2026-03-02T02:50:01.123Z"
    }
  ]
}
```

## Cache

Sitemap URL cache is stored at `~/.cache/auto-index/sitemap-cache.json`. This allows `auto-index` to only submit URLs that are **new** since the last run.

Delete the cache file to reset:
```bash
rm ~/.cache/auto-index/sitemap-cache.json
```

## Quota

Google Indexing API allows **200 requests/day**. The script auto-caps at this limit and logs a warning if exceeded.

## Common Failures

| Error | Fix |
|-------|-----|
| `No service account key provided` | Set `GOOGLE_INDEX_SA_KEY` env or pass `--sa-key` |
| `Service account key file not found` | Check the file path |
| `403 / Permission denied` | Ensure the SA email is an Owner in Search Console |
| `429 / Quota exceeded` | Wait 24h or request quota increase in Cloud Console |
| `No URLs found in sitemap` | Check the sitemap URL is valid and accessible |

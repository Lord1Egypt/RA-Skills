---
name: cf-crawl
description: Crawl websites using Cloudflare Browser Rendering /crawl API. Async multi-page crawl with markdown/HTML/JSON output, link following, pattern filtering, and AI-powered structured data extraction. Use when crawling entire sites or multiple pages, building knowledge bases, extracting structured data from websites, or when web_fetch is insufficient (JS rendering, multi-page, authenticated crawls).
---

# Cloudflare /crawl

Async site crawler via CF Browser Rendering API. Start a job → poll for results → get markdown/HTML/JSON per page.

## Quick Start

```bash
# Crawl a site (5 pages, markdown, no JS rendering = fast + free)
bash ~/clawd/skills/cf-crawl/scripts/crawl.sh "https://example.com" --limit 5 --format markdown

# With JS rendering (for SPAs, dynamic content)
bash ~/clawd/skills/cf-crawl/scripts/crawl.sh "https://example.com" --render --limit 10

# Start only (get job ID, poll later)
bash ~/clawd/skills/cf-crawl/scripts/crawl.sh "https://example.com" --limit 100 --start-only

# Poll existing job
bash ~/clawd/skills/cf-crawl/scripts/poll.sh <job-id>
```

## Credentials

Stored at `~/.clawdbot/secrets/cloudflare-crawl.env`:
```
CF_ACCOUNT_ID=<account_id>
CF_CRAWL_API_TOKEN=<token_with_read_and_edit>
```

## Key Options

| Option | Description |
|--------|-------------|
| `--limit N` | Max pages (default 10) |
| `--depth N` | Max link depth (default 10) |
| `--format markdown\|html\|json` | Output format (default markdown) |
| `--render` | Enable headless browser (default: off = fast fetch, free during beta) |
| `--include PAT` | Wildcard URL pattern to include (repeatable) |
| `--exclude PAT` | Wildcard URL pattern to exclude (repeatable) |
| `--external` | Follow external domain links |
| `--subdomains` | Follow subdomain links |
| `--source all\|sitemaps\|links` | URL discovery method |
| `--json-prompt "..."` | AI extraction prompt (with `--format json`) |
| `--json-schema file.json` | JSON schema for structured extraction |
| `--timeout SEC` | Max poll wait (default 300s) |
| `--output FILE` | Write full results to file |
| `--raw` | Output raw API response |
| `--start-only` | Print job ID without polling |

## Common Patterns

### Crawl docs site for knowledge base
```bash
bash ~/clawd/skills/cf-crawl/scripts/crawl.sh "https://docs.example.com/" \
  --limit 50 --depth 3 --format markdown --output docs.json
```

### Crawl with URL filtering
```bash
bash ~/clawd/skills/cf-crawl/scripts/crawl.sh "https://example.com/" \
  --include "/docs/**" --exclude "/docs/archive/**" --limit 20
```

### AI-powered structured extraction
```bash
bash ~/clawd/skills/cf-crawl/scripts/crawl.sh "https://example.com/products" \
  --format json --render \
  --json-prompt "Extract product name, price, and description" \
  --json-schema schema.json
```

### Long-running crawl (background)
```bash
JOB_ID=$(bash ~/clawd/skills/cf-crawl/scripts/crawl.sh "https://big-site.com" \
  --limit 1000 --start-only)
# Check later:
bash ~/clawd/skills/cf-crawl/scripts/poll.sh "$JOB_ID"
```

## Cost Notes

- `render: false` (default) — fast HTML fetch, **free during beta**
- `render: true` — uses Browser Rendering minutes (paid)
- `format json` — uses Workers AI tokens for extraction (paid)
- Results cached in R2 with `--max-age` (default 24hr)

## API Details

See `references/api-reference.md` for full parameter documentation, response schema, and lifecycle details.

---
name: dead-link-scanner
description: Scan websites, markdown files, and HTML files for broken links (dead links). Use when checking a website for 404s, validating links in documentation or README files, auditing link health before a deploy, or finding broken internal/external links. Supports recursive crawling with depth limits, markdown file scanning, and output in text or JSON format.
---

# dead-link-scanner

Find broken links in websites, markdown files, and HTML documents.

## Quick Start

```bash
# Scan a website for broken links
python3 scripts/dead_link_scanner.py scan https://example.com

# Scan with depth limit (default: 1)
python3 scripts/dead_link_scanner.py scan https://example.com --depth 3

# Scan a local markdown file
python3 scripts/dead_link_scanner.py file README.md

# Scan multiple files
python3 scripts/dead_link_scanner.py file docs/*.md

# JSON output
python3 scripts/dead_link_scanner.py scan https://example.com --json

# Only show broken links
python3 scripts/dead_link_scanner.py scan https://example.com --broken-only
```

## Commands

### `scan`
Crawl a website and check all links on each page.

```bash
python3 scripts/dead_link_scanner.py scan <url> [options]
```

Options:
- `--depth <n>` — Max crawl depth (default: 1, 0 = single page only)
- `--timeout <seconds>` — Request timeout (default: 10)
- `--json` — Output results as JSON
- `--broken-only` — Only show broken links
- `--internal-only` — Only check links within the same domain
- `--max-urls <n>` — Max URLs to check (default: 200)
- `--delay <seconds>` — Delay between requests (default: 0.2)

### `file`
Scan local markdown or HTML files for broken links.

```bash
python3 scripts/dead_link_scanner.py file <path>... [options]
```

Options:
- `--timeout <seconds>` — Request timeout (default: 10)
- `--json` — Output as JSON
- `--broken-only` — Only show broken links

## Output

Default text output:
```
✓ 200  https://example.com/about
✓ 200  https://example.com/blog
✗ 404  https://example.com/old-page  (found on: https://example.com)
✗ ERR  https://dead-domain.xyz  (found on: https://example.com) — ConnectionError
```

Summary line:
```
Checked 42 links: 39 OK, 3 broken
```

---
name: web-monitor
description: Monitor web pages for content changes with CSS selector targeting, change detection via hashing, and notification integration. Use for price tracking, content alerts, and website change detection.
---

# Web Monitor — Page Change Detection & Alerts

Track web pages for content changes using hash-based comparison. Supports CSS selector extraction, interval-based monitoring, change history, and configurable notification delivery.

## Quick Start

```bash
# Compare current page with previous snapshot
python scripts/monitor.py --url https://example.com --compare state.json

# Monitor with a CSS selector
python scripts/monitor.py --url https://example.com --selector ".price" --compare state.json
```

## Usage

```bash
python scripts/monitor.py --url URL [OPTIONS]

Options:
  --url URL              Page URL to monitor (required)
  --selector SELECTOR    CSS selector to extract specific content
  --compare FILE         Compare with previous snapshot from FILE
  --state-file FILE      Save current state to FILE (default: state.json)
  --interval SEC         Auto-monitor at interval (seconds)
  --notify COMMAND       Command to run on change detected
  --json                 Output as JSON
  --max-retries N        Connection retries on failure (default: 3)
```

## Examples

```bash
# Simple page check
python scripts/monitor.py --url https://example.com/page --compare state.json

# Monitor a price element
python scripts/monitor.py --url https://shop.example.com/product \
  --selector ".product-price" --compare price-state.json

# Continuous monitoring
python scripts/monitor.py --url https://example.com \
  --interval 3600 --compare state.json --notify "echo 'Changed!'"

# JSON output for pipeline
python scripts/monitor.py --url https://example.com --json
```

## State File Format

```json
{
  "url": "https://example.com/page",
  "selector": ".price",
  "hash": "sha256hash...",
  "timestamp": "2026-01-15T14:30:00Z"
}
```

## Features

- **Hash-based change detection** — reliable content comparison
- **CSS selector extraction** — monitor specific page sections
- **State persistence** — stores snapshots for comparison
- **Interval monitoring** — automatic periodic checks
- **Notification hooks** — trigger commands on changes
- **No external dependencies** — uses only Python stdlib
- **SSL/HTTPS support** — secure page fetching
- **JSON output** — structured data for automation

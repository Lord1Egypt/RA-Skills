---
name: FlowCrawl
description: Stealth web scraper. Give it any URL and it punches through Cloudflare, bot detection, and WAFs automatically using a 3-tier cascade (plain HTTP → TLS spoof → full JS). No API keys, no proxies, no CDP Chrome. Free from the Flow team. Use when scraping any website, bypassing bot protection, spidering a full site, or extracting clean markdown from any page.
metadata: {"clawdbot":{"emoji":"🦞"}}
---

# FlowCrawl

Scrape any website. Bypass any bot protection. Free.

## Install Scrapling First

```bash
pip install scrapling
```

Scrapling installs Playwright automatically on first run. That's the only dependency.

## Quick Usage

```bash
# Single URL — prints clean markdown to stdout
python3 ~/clawd/skills/flowcrawl/scripts/flowcrawl.py https://example.com

# Spider the whole site
python3 ~/clawd/skills/flowcrawl/scripts/flowcrawl.py https://example.com --deep

# Deep crawl with limits, save and combine
python3 ~/clawd/skills/flowcrawl/scripts/flowcrawl.py https://example.com --deep --limit 30 --combine

# JSON output — pipe into anything
python3 ~/clawd/skills/flowcrawl/scripts/flowcrawl.py https://example.com --json
```

## Add Alias (Recommended)

```bash
echo 'alias flowcrawl="python3 ~/clawd/skills/flowcrawl/scripts/flowcrawl.py"' >> ~/.zshrc
source ~/.zshrc
```

Then just: `flowcrawl https://example.com`

## How It Works

FlowCrawl uses a **3-tier fetcher cascade**. Starts fast, escalates only when blocked:

| Tier | Method | Handles |
|------|--------|---------|
| 1 | Plain HTTP | Most sites, instant |
| 2 | Stealth + TLS spoof | Cloudflare, Imperva, basic WAFs |
| 3 | Full JS execution | SPAs, heavy JS, aggressive bot detection |

Auto-detects blocking (403, 503, "Just a moment...") and escalates silently.

## All Options

| Flag | Description | Default |
|------|-------------|---------|
| `--deep` | Spider whole site following internal links | off |
| `--depth N` | Max hop depth from start URL | 3 |
| `--limit N` | Max pages to crawl | 50 |
| `--combine` | Merge all pages into one file | off |
| `--format md\|txt` | Output format | md |
| `--output DIR` | Output directory | ./flowcrawl-output |
| `--json` | Structured JSON output | off |
| `--quiet` | Suppress progress logs | off |

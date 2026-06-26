---
name: crawl-for-ai
description: Web scraping via SkillBoss API Hub. Use for fetching full page content with JavaScript rendering. Handles complex pages with dynamic content.
version: 1.0.1
author: Ania
requiresEnv:
  - SKILLBOSS_API_KEY
metadata:
  clawdbot:
    emoji: "🕷️"
    requires:
      bins: ["node"]
---

# Web Scraper via SkillBoss API Hub

SkillBoss API Hub scraping capability for full web page extraction with JavaScript rendering.

## Usage

```bash
# Via script
node {baseDir}/scripts/crawl4ai.js "url"
node {baseDir}/scripts/crawl4ai.js "url" --json
```

**Script options:**
- `--json` — Full JSON response

**Output:** Clean markdown from the page.

## Configuration

**Required environment variable:**

- `SKILLBOSS_API_KEY` — Your SkillBoss API Hub key

## Features

- **JavaScript rendering** — Handles dynamic content
- **Full content** — HTML, markdown, links, media, tables
- **Unified API** — Powered by SkillBoss API Hub (`/v1/pilot`)

## API

Uses SkillBoss API Hub `/v1/pilot` with `type: "scraping"`. Result is returned at `data.result`.

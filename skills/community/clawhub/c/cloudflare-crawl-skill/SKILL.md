---
name: cloudflare-crawl
description: Crawl websites using Cloudflare's Browser Rendering API. Use when you need to scrape entire sites, build knowledge bases, extract content from multiple pages, or create RAG datasets. Works on Cloudflare-protected sites. Returns HTML, Markdown, or AI-extracted JSON.
requires:
  env:
    - CLOUDFLARE_API_TOKEN
    - CLOUDFLARE_ACCOUNT_ID
  files:
    - scripts/crawl.js
---

# Cloudflare Crawl

Crawl entire websites using Cloudflare's Browser Rendering `/crawl` API. Async job-based crawling with JS rendering.

## When to Use

- Scrape entire sites (not just single pages)
- Build knowledge bases or RAG datasets
- Research across multiple pages
- Sites protected by Cloudflare (CF won't block itself)
- Need Markdown or structured JSON output

## Prerequisites

**Get Cloudflare API credentials:**
1. Go to https://dash.cloudflare.com/profile/api-tokens
2. Create token with `Account.Browser Rendering` permission
3. Get your Account ID from dashboard URL

**Set environment variables:**
```bash
export CLOUDFLARE_API_TOKEN="your_token"
export CLOUDFLARE_ACCOUNT_ID="your_account_id"
```

## Quick Start

```bash
# Start a crawl job
node scripts/crawl.js start https://example.com --limit 50

# Check status
node scripts/crawl.js status <job_id>

# Get results as markdown
node scripts/crawl.js results <job_id> --format markdown
```

## API Overview

### 1. Start Crawl Job
```bash
curl -X POST "https://api.cloudflare.com/client/v4/accounts/$CLOUDFLARE_ACCOUNT_ID/browser-rendering/crawl" \
  -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://example.com",
    "limit": 50,
    "depth": 3,
    "formats": ["markdown"]
  }'
```

Returns: `{ "success": true, "result": "job_id_here" }`

### 2. Poll for Completion
```bash
curl "https://api.cloudflare.com/client/v4/accounts/$CLOUDFLARE_ACCOUNT_ID/browser-rendering/crawl/$JOB_ID?limit=1" \
  -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN"
```

Status values: `running`, `completed`, `errored`, `cancelled_due_to_timeout`

### 3. Get Results
```bash
curl "https://api.cloudflare.com/client/v4/accounts/$CLOUDFLARE_ACCOUNT_ID/browser-rendering/crawl/$JOB_ID" \
  -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN"
```

## Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| url | string | required | Starting URL |
| limit | number | 10 | Max pages to crawl (max 100,000) |
| depth | number | 100000 | Max link depth from start URL |
| source | string | "all" | URL discovery: `all`, `sitemaps`, `links` |
| formats | array | ["html"] | Output: `html`, `markdown`, `json` |
| render | boolean | true | Execute JS (false = fast HTML only) |

## Output Formats

### Markdown (best for AI)
```json
{
  "url": "https://example.com/page",
  "status": "completed",
  "markdown": "# Page Title\n\nContent here...",
  "metadata": { "title": "Page Title", "status": 200 }
}
```

### JSON (AI-extracted)
Uses Workers AI to extract structured data. Requires `jsonOptions.prompt`:
```json
{
  "formats": ["json"],
  "jsonOptions": {
    "prompt": "Extract product name, price, and description"
  }
}
```

## Pricing

| Plan | Free Tier | Overage |
|------|-----------|---------|
| Workers Free | 10 min/day | N/A |
| Workers Paid | 10 hrs/month | $0.09/hour |

## Limits

- Max 100,000 pages per crawl
- 7 day max runtime
- Results available 14 days
- Free plan: 10 concurrent, 100 pages max

## Example: Crawl for RAG

```javascript
// Crawl docs site for knowledge base
const job = await startCrawl({
  url: 'https://docs.example.com',
  limit: 500,
  formats: ['markdown'],
  source: 'sitemaps' // Use sitemap for efficiency
});

// Wait for completion
const results = await waitForCrawl(job.id);

// Save markdown files for RAG
for (const page of results.records) {
  if (page.status === 'completed') {
    fs.writeFileSync(`docs/${slugify(page.url)}.md`, page.markdown);
  }
}
```

## vs Browserbase/Stagehand

| Use Case | Cloudflare Crawl | Browserbase |
|----------|-----------------|-------------|
| Full site scrape | ✅ Best | ❌ Manual |
| Interactive (forms) | ❌ No | ✅ Best |
| CF-protected sites | ✅ Native | ⚠️ Cloud bypass |
| AI extraction | ✅ Built-in | ✅ Stagehand |
| Session management | ✅ Async jobs | ❌ Manual |
| Cost | $0.09/hr | Credits |

Use **Cloudflare Crawl** for bulk content extraction.
Use **Browserbase** for interactive automation.

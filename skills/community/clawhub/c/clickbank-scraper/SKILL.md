---
name: clickbank-scraper
description: >
  Scrape top ClickBank products by category with gravity scores, commission rates,
  and estimated monthly sales. Integrates with affiliate marketing automation pipelines
  for Pinterest board generation and pin content creation. Part of Max's ClickBank
  affiliate marketing automation suite.
---

# ClickBank Product Scraper

Autonomous scraper for high-performing ClickBank products. Pulls product metadata (gravity, commission, sales estimates) from CBTrends.com and exports structured JSON for pipeline integration.

## Installation

```bash
npm install
```

**Dependencies:**
- `cheerio` — HTML parsing
- `node-fetch` — HTTP requests
- `node` ≥ v16

## Usage

### Basic Run
```bash
node scraper.js
```
Outputs to `output/latest.json`, `output/products-YYYY-MM-DD.json`

### With ClickBank Affiliate ID
```bash
CB_AFFILIATE_ID=your_nickname node scraper.js
```
Generates hoplinks with your affiliate ID embedded.

### Scheduled Runs
Use OpenClaw cron or n8n workflows to run daily:
```json
{
  "job": "clickbank-scraper",
  "schedule": "0 9 * * *",
  "command": "CB_AFFILIATE_ID=your_id node scraper.js"
}
```

## Output Format

### latest.json
Always-current snapshot for real-time pipeline feeds.

```json
{
  "category": "Health & Fitness",
  "updatedAt": "2026-03-27T14:00:00Z",
  "products": [
    {
      "name": "Product Name",
      "vendorId": "vendor123",
      "gravity": 87.5,
      "avgSaleAmount": "$47.00",
      "commissionPct": 75,
      "rebillPct": 30,
      "hoplink": "https://yourname.clickbank.net/...",
      "estimatedMonthlySales": "$12000"
    }
  ]
}
```

### products-YYYY-MM-DD.json
Full daily archive for historical analysis.

### top10-YYYY-MM-DD.json
Filtered to gravity > 50 for quick high-performers reference.

## Integration Use Cases

### 1. Pinterest Board Automation
Feed `latest.json` → n8n workflow → Auto-generate Pinterest pins for top 10 products

### 2. Product Comparison Content
Extract gravity + commission → Generate comparison tables for blog posts

### 3. Affiliate Performance Tracking
Monitor gravity trends over time → Pivot to rising winners

### 4. Landing Page Personalization
Cross-reference user interests → Recommend high-gravity products

## Data Fields Reference

| Field | Type | Description |
|-------|------|-------------|
| name | string | Product name |
| vendorId | string | ClickBank vendor identifier |
| gravity | number | Affiliate gravity (higher = more demand, 0-100+) |
| avgSaleAmount | string | Average transaction value |
| commissionPct | number | Commission rate (0-100%) |
| rebillPct | number | Rebill/recurring commission % |
| hoplink | string | Ready-to-use affiliate link |
| estimatedMonthlySales | string | Rough sales estimate |

## Limitations

- Single page per category (10 products) from CBTrends
- Gravity data may lag 1-2 hours behind ClickBank live marketplace
- No API key required (scrapes public data)
- Categories limited to: Health & Fitness, Supplements, E-Business, Self-Help

## Roadmap

- [x] Health & Fitness category scraper
- [ ] Multi-category support (Supplements, Self-Help, E-Business, Investing)
- [ ] Pagination (pages 2-5 for 50+ products)
- [ ] ClickBank Marketplace API integration (when account active)
- [ ] Scheduled runs via cron
- [ ] Gravity trend tracking over time
- [ ] Email digest of top gainers/losers

## Integration with n8n

Example n8n workflow node:

```javascript
// n8n "Execute Command" node
const exec = require('child_process').execSync;
const result = exec('CB_AFFILIATE_ID=your_id node scraper.js', {
  cwd: '/path/to/clickbank-scraper'
});
return JSON.parse(result.toString());
```

## Integration with OpenClaw

Use as a cron job or sub-agent:

```bash
openclaw cron add clickbank-scraper \
  --schedule "0 9 * * *" \
  --command "cd path/to/scraper && node scraper.js"
```

## Author

Max @ max-co.digital — Autonomous ClickBank affiliate marketing automation.

## License

Proprietary — Part of Digital Helper Agency / max-co product suite.

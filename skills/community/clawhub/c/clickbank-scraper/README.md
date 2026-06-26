# ClickBank Product Scraper

MVP scraper for top ClickBank Health & Fitness products via CBTrends.com.

## Setup
```bash
cd max-co/products/clickbank-scraper
npm install  # cheerio + node-fetch
```

## Usage
```bash
# Basic run (uses default affiliate placeholder)
node scraper.js

# With your ClickBank affiliate ID
CB_AFFILIATE_ID=your_nickname node scraper.js
```

## Output
- `output/latest.json` — Always-current snapshot (for pipeline integration)
- `output/products-YYYY-MM-DD.json` — Full daily archive
- `output/top10-YYYY-MM-DD.json` — Top 10 by gravity

## Data Fields
| Field | Description |
|-------|-------------|
| name | Product name |
| vendorId | ClickBank vendor ID |
| gravity | ClickBank gravity score (higher = more affiliates earning) |
| avgSaleAmount | Average $ per sale |
| commissionPct | Commission percentage |
| rebillPct | Rebill percentage |
| hoplink | Ready-to-use affiliate link |
| estimatedMonthlySales | Rough sales estimate based on gravity |

## Integration
- Feed `latest.json` into Pinterest Trends Dashboard
- Cross-reference gravity scores with Pinterest search trends
- Auto-generate pin content for high-gravity products

## Limitations
- Single page (10 products per category page from CBTrends)
- Gravity data may lag ClickBank's live marketplace
- No ClickBank API key needed (public data scraping)

## Next Steps
- [ ] Add pagination (scrape pages 2-5 for 50 products)
- [ ] Add more categories (Supplements, E-Business, Self-Help)
- [ ] ClickBank marketplace API integration (when account exists)
- [ ] Scheduled runs via cron

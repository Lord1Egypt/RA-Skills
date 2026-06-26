# Competitor Price Monitor Skill

Track competitor pricing, product changes, and market positioning automatically.

## What This Skill Does

1. **Track Pricing** — Monitor competitor websites for price changes
2. **Detect Changes** — Alert when competitors add/remove products, change copy, or update pricing
3. **Benchmark** — Compare your pricing against the market
4. **Report** — Weekly competitive intelligence summaries

## Usage

### Add Competitors
```
Monitor these competitors: [URL1], [URL2], [URL3]
Track their pricing pages and product listings
```

### Get Report
```
Generate competitive pricing report for this week
```

## Workflow

### Step 1: Competitor Discovery
- Input competitor URLs or search by industry/niche
- Identify pricing pages, product listings, and feature pages
- Store baseline snapshots

### Step 2: Monitoring
On each check cycle:
1. Fetch current page content via web scraping
2. Compare against stored baseline
3. Detect changes in:
   - Prices (increases, decreases, new tiers)
   - Products (added, removed, renamed)
   - Features (new capabilities, deprecated items)
   - Messaging (positioning, value props, CTAs)

### Step 3: Change Detection
```javascript
// Pseudo-code for price change detection
const changes = [];
for (const competitor of competitors) {
  const current = await scrapePrice(competitor.url);
  const baseline = await getBaseline(competitor.id);
  
  if (current.price !== baseline.price) {
    changes.push({
      competitor: competitor.name,
      product: current.product,
      oldPrice: baseline.price,
      newPrice: current.price,
      change: ((current.price - baseline.price) / baseline.price * 100).toFixed(1) + '%'
    });
  }
}
```

### Step 4: Alerting
When significant changes detected:
- Price decrease >10% → "Competitor [X] dropped [product] price by [Y]%"
- New product launched → "Competitor [X] launched [new product] at $[Z]"
- Feature added → "Competitor [X] now offers [feature]"

### Step 5: Weekly Report
```markdown
## Competitive Intelligence Report — Week of [date]

### Price Changes
| Competitor | Product | Old Price | New Price | Change |
|-----------|---------|-----------|-----------|--------|
| Acme Corp | Pro Plan | $49/mo | $39/mo | -20% |

### New Products/Features
- **Acme Corp** launched "Enterprise Plan" at $199/mo
- **Beta Inc** added AI chatbot feature to all tiers

### Market Positioning
- Average market price for [category]: $X/mo
- Your price: $Y/mo (Z% above/below market)

### Recommendations
- Consider matching Acme's price cut on Pro tier
- Beta's new AI feature is a competitive threat — prioritize similar feature
```

## Configuration
```json
{
  "competitors": [
    { "name": "Competitor A", "url": "https://competitor-a.com/pricing", "check_frequency": "daily" }
  ],
  "alert_channels": ["telegram", "email"],
  "report_frequency": "weekly",
  "report_day": "monday"
}
```

## Requirements
- Brave Search API or web fetch capability
- OpenClaw with scheduled tasks (cron/heartbeat)
- Storage for baseline snapshots

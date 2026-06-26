---
name: GTS_ecommerce-price-monitor
description: Monitor competitor product prices across major e-commerce platforms (Shopee, Lazada, Amazon, etc.). Use when the user wants to: (1) Set up automated price tracking for competitor products, (2) Generate price comparison reports, (3) Get alerts when prices drop or rise, (4) Analyze pricing trends over time, (5) Identify best times to adjust their own pricing. Best for e-commerce sellers, dropshippers, and small business owners who need competitive intelligence without manual checking.
version: 1.0.1
metadata:
  openclaw:
    requires:
      bins:
        - python3
    emoji: "📊"
---

# E-commerce Competitor Price Monitor

Automatically track competitor product prices across Shopee, Lazada, Amazon, and other platforms. Get notified on price drops, generate weekly comparison reports, and make data-driven pricing decisions.

## Quick Start

1. **Configure targets**: Tell the agent your competitor product URLs and tracking frequency.
2. **Run a scan**: `scan prices now` — the agent visits each URL, extracts the price, and logs it.
3. **Get a report**: `price report` or `compare prices` — generates a clean comparison table.
4. **Set alerts**: `alert me when [product] drops below [price]` — the agent checks on schedule and notifies you.

## Workflow

### Step 1: Add Products to Track

Tell the agent in natural language:

> "Track the price of this Shopee product: https://shopee.com.my/... every 6 hours"
> "Add this Lazada link to my price monitor: https://www.lazada.com.my/..."
> "Monitor these 5 Amazon products daily"

The agent should:
- Accept any e-commerce product URL
- Ask for the desired check frequency (default: 24h)
- Ask for an optional target/alert price
- Store the config in `scripts/prices.json`

### Step 2: Price Scanning

When the user asks to scan or on schedule, the agent:

1. Reads the product list from `scripts/prices.json`
2. For each URL:
   - Visits the page using web browser
   - Extracts: product name, current price, currency, stock status, seller name
   - Handles platform-specific page structures (see [PLATFORMS.md](references/PLATFORMS.md))
3. Logs results to `scripts/price_history.jsonl` (append-only)
4. Updates latest prices in `scripts/prices.json`
5. Checks alert conditions — if triggered, notifies the user

### Step 3: Reports

On request, generate:

**Quick comparison** (inline Telegram-friendly):
```
📊 Price Watch — 3 products tracked
───────────────────────────────
Product A  → RM 89.90  ▼ 5% from last week
Product B  → RM 245.00  ▲ 2% (new all-time high)
Product C  → RM 59.90  — No change
```

**Detailed CSV report**: Run the Python script `scripts/report.py` to generate `reports/price_report_YYYY-MM-DD.csv` with full history.

### Step 4: Alerts

The agent supports natural language alert setup:

> "Tell me if iPhone 15 drops below RM 4,000"
> "Alert me when Product C goes on sale"
> "Notify me if any tracked product drops more than 15%"
> "Stop alerting me about Product A"

Alerts are stored in `scripts/alerts.json`. The agent checks them after each scan cycle.

## Scripts

### `scripts/manage.py` — Data management CLI

```bash
python3 scripts/manage.py products add <url> --name "Product Name" --interval 6 --alert-price 89.90
python3 scripts/manage.py products list
python3 scripts/manage.py products remove <id>
python3 scripts/manage.py alerts add --product <id> --type below --value 100.00
python3 scripts/manage.py alerts list
python3 scripts/manage.py alerts remove <id>
python3 scripts/manage.py history export --days 30
```

### `scripts/report.py` — Generate reports

```bash
python3 scripts/report.py                    # Quick summary (stdout)
python3 scripts/report.py --csv              # Full CSV to reports/
python3 scripts/report.py --product <id>     # Single product history
python3 scripts/report.py --trends           # Price trend analysis
```

## References

- **Platform scraping notes**: See [references/PLATFORMS.md](references/PLATFORMS.md) for platform-specific tips (Shopee dynamic loading, Lazada anti-scrape, Amazon structure)
- **Configuration**: See [references/CONFIG.md](references/CONFIG.md) for advanced setup (custom intervals, notification channels, export formats)

## Tips for Best Results

- **Shopee**: Page loads dynamically. Wait for `.product-price` or `[data-testid="product-price"]` elements.
- **Lazada**: May show region-specific prices. Check URL for `.my` (Malaysia), `.sg` (Singapore), etc.
- **Amazon**: Product prices are in `#corePriceDisplay_desktop_feature_div .a-price-whole`. Watch for coupon discounts listed separately.
- **Frequency**: For fast-moving products (electronics), check every 6h. For stable goods (household), daily is fine.
- **Freshness**: Always verify the extracted price looks reasonable before logging (reject nulls, zeroes, or parsing errors).

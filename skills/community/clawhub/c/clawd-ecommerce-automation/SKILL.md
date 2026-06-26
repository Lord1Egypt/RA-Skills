---
name: ecommerce-automation
description: "Automate e-commerce operations: price monitoring, inventory tracking, order management, competitor analysis, and stock alerts. Save 20+ hours per week for online sellers. Supports Shopify, WooCommerce, Amazon, eBay integrations."
homepage: https://clawhub.com/skills/ecommerce-automation
metadata:
  openclaw:
    emoji: "🛒"
    requires:
      bins: ["openclaw", "curl"]
    tags: ["ecommerce", "automation", "dropshipping", "amazon", "shopify"]
---

# Ecommerce Automation Skill

**Automate your entire store and reclaim 20+ hours per week**

## When to Use

✅ **USE this skill when:**

- "Monitor competitor prices and alert me when they change"
- "Track inventory across multiple platforms"
- "Automatically export orders to my fulfillment system"
- "Get notified when products go out of stock or back in stock"
- "Scrape competitor products and analyze trends"
- "Auto-update prices based on rules"
- "Sync inventory between Shopify and Amazon"

## When NOT to Use

❌ **DON'T use this skill when:**

- Single product, one-time manual update
- Complex returns/refunds processing (human judgment needed)
- Customer service conversations (needs empathy)
- Visual content creation (product photos, videos)

## 💰 ROI & Value

**Typical savings**:
- Price monitoring: 5 hours/week → **$500/month** in time
- Inventory sync: 3 hours/week → **$300/month**
- Order processing: 8 hours/week → **$800/month**
- **Total: 16+ hours/week = $1,600/month value**

**Our cost**: $10-30/month
**ROI**: 50:1+ (payback in <1 day)

## Supported Platforms

| Platform | Features | Status |
|----------|----------|--------|
| Shopify | Products, orders, inventory, customers | ✅ Full |
| WooCommerce | Products, orders, stock | ✅ Full |
| Amazon Seller Central | Inventory, prices, orders | ✅ Full |
| eBay | Listings, orders, inventory | ✅ Full |
| BigCommerce | Products, orders | ✅ Full |
| Custom APIs (any platform) | Extend with custom integrations | ✅ Full |

## Quick Start: Price Monitor

### 1. Configure Your Store

Create `ecommerce-config.yaml`:

```yaml
store:
  platform: "shopify"
  api_key: "shpat_xxxxx"
  store_url: "https://your-store.myshopify.com"

monitors:
  - name: "Competitor Price Watch"
    competitors:
      - url: "https://competitor.com/product-1"
        css_selector: ".price"
      - url: "https://competitor.com/product-2"
        css_selector: ".price"

    rules:
      - if: "competitor_price < my_price * 0.9"
        action: "alert"
        channel: "email"
        to: "pricing@yourcompany.com"
      - if: "competitor_price > my_price * 1.1"
        action: "alert"
        channel: "slack"
        # We're underpriced!

    schedule: "*/30 * * * *"  # Every 30 minutes
```

### 2. Run the Workflow

```bash
# Load config
clawhub workflow load ecommerce-config.yaml

# Start monitoring
clawhub workflow start "Competitor Price Watch"

# Check status
clawhub workflow status
```

### 3. Get Alerts

Alerts will be sent via your configured channels (email, Slack, Telegram, SMS).

---

## Core Features

### 1. Price Monitoring & Repricing

**Track competitor prices automatically**:
```yaml
price_monitor:
  products:
    - sku: "ABC-123"
      my_price: 49.99
      competitors:
        - name: "Amazon"
          url: "https://amazon.com/dp/..."
          selector: "#priceblock_ourprice"
        - name: "eBay"
          url: "https://ebay.com/itm/..."
          selector: ".notranslate"

  rules:
    - if: "min_competitor_price < my_price * 0.95"
      action: "recommend_price_match"
    - if: "max_competitor_price > my_price * 1.2"
      action: "alert_price_gap"  # We're too cheap!
```

**Automatic repricing** (optional):
- Match competitor price
- Stay X% below/above competitors
- Min/max price bounds

### 2. Inventory Sync

**Multi-platform inventory consistency**:
```yaml
inventory_sync:
  sources:
    - platform: "shopify"
      location: "main_warehouse"
    - platform: "amazon"
      fulfillment: "FBA"

  sync_rules:
    - if: "shopify_stock < 10"
      action: "alert_low_stock"
    - if: "amazon_stock != shopify_stock"
      action: "recalculate_available"
      # Pull from shipping manifest
```

**Benefits**:
- No overselling
- Automatic stock allocations
- Fulfillment optimization

### 3. Order Management

**Auto-process orders**:
```yaml
order_processor:
  triggers:
    - event: "order.created"
      platform: "shopify"

  steps:
    - validate: "Check inventory available"
    - fulfill: "Send to 3PL / dropship supplier"
    - notify: "Customer shipping confirmation"
    - track: "Import tracking number back to Shopify"

  fallbacks:
    - if inventory insufficient: "Place on backorder"
    - if fulfillment fails: "Alert operations team"
```

**Supported actions**:
- Send to fulfillment service (ShipStation, EasyPost)
- Generate packing slips
- Update order status
- Customer notifications

### 4. Competitor Analysis

**Daily competitor insights**:
```yaml
competitor_analysis:
  competitors:
    - name: "Brand A"
      product_urls: ["...", "..."]

  data_points:
    - price_history (track changes over time)
    - review_count (monitor growth)
    - best_sellers_rank
    - new_product launches

  report:
    schedule: "0 8 * * *"  # Daily 8 AM
    format: ["email", "slack", "pdf"]
    summary: |
      This week: 5 price drops avg -$3.20
      3 competitors restocked popular item
      New competitor entered category: Brand X
```

### 5. Stock Alerts

**Smart inventory notifications**:
```yaml
stock_alerts:
  checks:
    - product: "SKU-123"
      threshold: 20
      when_below: "notify_purchasing"
    - product: "SKU-456"
      threshold: 5
      when_below: "pause_advertising"

  channels:
    purchasing: "purchasing@company.com"
    marketing: "marketing@company.com"
    slack: "#inventory-alerts"
```

---

## Advanced Patterns

### Pattern: Dynamic Repricing

Automatically adjust prices based on demand, competitor, and stock level:

```yaml
dynamic_pricing:
  product: "SUMMER-DRESS-001"
  base_price: 79.99

  factors:
    - competitor_price: "weight: 0.5"
    - stock_level: "if stock > 100: -5%; if stock < 10: +10%"
    - seasonality: "peak_season: +20%"
    - conversion_rate: "if cvr < 2%: -$5"

  bounds:
    min_price: 49.99
    max_price: 129.99
    update_frequency: "every 2 hours"
```

### Pattern: Cross-Platform Listings

**One product, multiple marketplaces**:
```yaml
sync_product:
  source: "Shopify / Products / ID-123"
  targets:
    - platform: "amazon"
      listing: "Create/Update Amazon listing"
      price_adjustment: "+15% (Amazon fees)"
    - platform: "ebay"
      listing: "Create/Update eBay listing"
      price_adjustment: "+10%"
    - platform: "google_shopping"
      listing: "Update Merchant Center"

  inventory_reserve: 5  # Keep 5 units in Shopify only
```

### Pattern: Lost Buyback Window

**Automatically recover abandoned carts**:
```yaml
cart_recovery:
  trigger: "checkout.abandoned"
  delay: "1 hour"

  steps:
    - email: "Reminder with 10% off"
    - if_no_response_24h:
        sms: "Last chance, free shipping"
    - if_no_response_48h:
        alert: "Manual review needed"

  expected_recovery_rate: "15% → $2,000/mo revenue"
```

---

## Best Practices

### 1. Start with Read-Only
- Begin with monitoring only (no auto-repricing)
- Validate data accuracy
- Set conservative alert thresholds

### 2. Stagger Rollout
- Week 1: Price monitoring only
- Week 2: Add inventory sync
- Week 3: Enable auto-fulfillment
- Week 4: Enable auto-repricing

### 3. Implement Safeguards
```yaml
safeguards:
  max_daily_price_changes: 10  # Prevent erratic pricing
  min_profit_margin: 15%
  blackout_hours: "10pm-6am"  # No changes at night
  approval_required: "price_change > 20%"
```

### 4. Monitor & Audit
```yaml
audit_log:
  - record: "All price changes with before/after"
  - report: "Weekly summary email"
  - rollback: "One-click revert to previous state"
```

---

## Integration Examples

### Shopify + Amazon Sync

`sync-shopify-amazon.yaml`:
```yaml
workflow:
  name: "Shopify-Amazon Sync"
  schedule: "*/5 * * * *"

steps:
  - fetch_shopify:
      agent: "shopify-agent"
      task: "Get all products with inventory > 0"

  - fetch_amazon:
      agent: "amazon-agent"
      task: "Get all FBA inventory"

  - compare:
      agent: "diff-agent"
      task: "Find discrepancies between platforms"

  - sync:
      agent: "sync-agent"
      task: "Update Amazon with Shopify quantities"
      depends_on: [compare]
```

### Price Scraper

`scrape-competitors.yaml`:
```yaml
workflow:
  name: "Competitor Price Scraper"
  schedule: "0 */3 * * *"  # Every 3 hours

steps:
  - scrape:
      agent: "browser-agent"
      tasks:
        - "https://competitor1.com/product-a" → ".price"
        - "https://competitor1.com/product-b" → ".price"
        # ... up to 50 products

  - normalize:
      agent: "data-processor"
      task: "Clean prices, remove currency symbols, convert to float"

  - compare:
      agent: "analyst"
      task: "Compare to our prices, find deviations"

  - alert:
      agent: "alerter"
      task: "Send report to pricing team"
```

---

## Troubleshooting

### API Limits?
- Shopify: 2 req/sec → batching recommended
- Amazon: 1 req/sec → use throttling
- Solution: `openclub agents` with rate limiting

### Data Mismatches?
- Check timezone handling
- Validate currency conversions
- Verify product matching (SKU vs. URL)

### Want to Pause Sync?
```bash
clawhub workflow pause "Shopify-Amazon Sync"
clawhub workflow resume "Shopify-Amazon Sync"
```

---

## Support & Next Steps

1. **Setup assistance**: Join our Discord for 1:1 onboarding
2. **Custom integrations**: Need a platform not listed? We can build it (custom quote)
3. **Enterprise**: Team collaboration, audit logs, white-glove support ($500/mo)

---

_Automate e-commerce. Scale without hiring._ 🚀

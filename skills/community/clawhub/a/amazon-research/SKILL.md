---
name: amazon-research
description: Research Amazon products, track prices, and compare deals. Use when searching for products on Amazon, monitoring price changes, creating wishlists with price alerts, or comparing product specifications and reviews.
---

# Amazon Research & Price Tracking

Research Amazon products and track prices over time.

## Quick Start

### Search Products

```bash
# Search for product
./scripts/amazon_search.sh "Alu Profil 20x20"

# Search with filters
./scripts/amazon_search.sh "iPhone 15" --max-price 800 --prime-only
```

### Track Price

```bash
# Add product to price tracking
./scripts/price_tracker.sh add "B08XXXXXX" "Alu Profil 20x20"

# Check all tracked products
./scripts/price_tracker.sh list

# Get price history
./scripts/price_tracker.sh history "B08XXXXXX"
```

## Features

- **Product Search:** Find products by keyword, category, price range
- **Price Tracking:** Monitor price changes over time
- **Deal Alerts:** Get notified when price drops below threshold
- **Comparison:** Compare similar products side-by-side
- **Wishlist:** Save products with target prices

## Database Schema

SQLite database: `~/workspace/Projects/Amazon-Research/amazon_prices.db`

**Tables:**
- `products` - Product details (ASIN, title, category)
- `price_history` - Timestamped price data
- `alerts` - User-defined price alerts
- `wishlist` - Saved products with target prices

## Price Tracking Workflow

1. **Search** → Find product on Amazon
2. **Add** → Add to tracking database
3. **Monitor** → Cron job checks prices daily
4. **Alert** → Notification when price drops

## Cron Setup

```bash
# Check prices daily at 9:00
0 9 * * * ~/workspace/skills/amazon-research/scripts/price_checker.sh
```

## Resources

- `references/amazon_api.md` - Amazon API documentation
- `assets/search_templates/` - Common search queries

## Alternative: Manual Research

Since Amazon API requires approval, use web scraping or manual entry:

```python
# Add product manually
python3 scripts/add_product.py --asin "B08XXXXXX" --title "Product Name" --price 19.99
```

## Integration with Other Skills

- **Kleinanzeigen:** Compare new vs. used prices
- **Shopping List:** Add researched items to buy list
- **Budget:** Track planned expenses

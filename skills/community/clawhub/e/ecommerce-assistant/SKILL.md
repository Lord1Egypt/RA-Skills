---
name: ecommerce-assistant
description: E-commerce product research, competitor analysis, and price monitoring for Amazon, Shopify, and other platforms. Use when researching Amazon product data, analyzing Shopify stores, monitoring price changes, finding profitable products, or generating product reports. GitHub demo available.
---

# Ecommerce Assistant

## Overview

Research products, analyze competitors, and monitor prices across e-commerce platforms. Supports Amazon product data, Shopify store analysis, and price trend tracking.

## Quick Start

📦 **GitHub Demo**: https://github.com/lhldolike/ecommerce-assistant-demo

### Amazon Product Research

```bash
# Search Amazon products
python3 scripts/amazon_search.py "wireless headphones" --limit 10

# Get product details
python3 scripts/amazon_product.py B08HMWZBXC

# Track price history
python3 scripts/price_tracker.py --asin B08HMWZBXC --notify
```

### Shopify Store Analysis

```bash
# Analyze a Shopify store
python3 scripts/shopify_analyzer.py https://store-name.myshopify.com

# Compare multiple stores
python3 scripts/shopify_analyzer.py --compare store1.com store2.com
```

### Price Monitoring

```bash
# Add product to watchlist
python3 scripts/price_tracker.py --add B08HMWZBXC --target-price 50

# Check all tracked products
python3 scripts/price_tracker.py --list

# Generate price report
python3 scripts/price_tracker.py --report weekly
```

## Core Capabilities

### 1. Product Research
- Search products by keyword
- Get detailed product information
- Analyze reviews and ratings
- Extract product specifications

### 2. Competitor Analysis
- Analyze Shopify store inventory
- Compare pricing strategies
- Identify top-selling products
- Track competitor changes

### 3. Price Monitoring
- Track price changes over time
- Set price drop alerts
- Generate trend reports
- Export data to CSV/JSON

### 4. Market Insights
- Identify trending products
- Analyze category performance
- Find pricing opportunities
- Generate actionable reports

## Data Sources

This skill uses multiple data sources:
- **Amazon**: Product Advertising API, public data
- **Shopify**: Storefront API (public endpoints)
- **Price Tracking**: Historical data aggregation

See references/ for detailed API documentation:
- [Amazon API Guide](references/amazon-api.md)
- [Shopify API Guide](references/shopify-api.md)

## Scripts

All scripts are in `scripts/` directory:
- `amazon_search.py` - Search Amazon products
- `amazon_product.py` - Get product details
- `shopify_analyzer.py` - Analyze Shopify stores
- `price_tracker.py` - Price monitoring system
- `product_reporter.py` - Generate reports

## Output Formats

Results can be exported as:
- JSON (machine-readable)
- CSV (spreadsheet-friendly)
- Markdown (human-readable reports)

## Limitations

- Free tier APIs have rate limits (typically 100-500 requests/month)
- Some Amazon data requires Product Advertising API approval
- Shopify data limited to public storefront information
- Price tracking requires periodic execution (not real-time)

## Examples

### Find Profitable Products
```bash
python3 scripts/amazon_search.py "yoga mat" --min-price 20 --max-price 50 --min-rating 4.0
```

### Monitor Competitor Prices
```bash
python3 scripts/shopify_analyzer.py https://competitor-store.com --track-prices --output competitor.json
```

### Generate Weekly Report
```bash
python3 scripts/product_reporter.py --type weekly --email report@example.com
```

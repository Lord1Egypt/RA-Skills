---
name: "bytesagain-ecom-ops"
description: "Optimize e-commerce operations with AI. Input: sales data, ad spend, inventory levels. Output: attribution analysis, ad ROI report, inventory reorder plan, pricing recommendations."
version: "1.0.0"
author: "BytesAgain"
tags: ["ecommerce", "shopify", "marketing", "attribution", "inventory", "pricing", "operations"]
---

# Ecom Ops

Optimize e-commerce operations with AI-powered analysis. Covers marketing attribution, ad spend ROI, inventory planning, and pricing strategy for Shopify and multi-channel stores.

## Commands

### attribution
Analyze marketing channel attribution and ROAS.
```bash
bash scripts/script.sh attribution --channels "google:5000,meta:3000,email:500,organic:2000" --revenue 18000
```

### roi
Calculate ad campaign ROI and recommend budget allocation.
```bash
bash scripts/script.sh roi --spend 8000 --revenue 18000 --cogs-pct 40 --platform shopify
```

### inventory
Generate reorder recommendations based on sales velocity.
```bash
bash scripts/script.sh inventory --product "SKU-001" --current-stock 120 --daily-sales 15 --lead-days 14
```

### pricing
Analyze pricing strategy and suggest optimizations.
```bash
bash scripts/script.sh pricing --cost 25 --current-price 79 --competitor-price 69 --margin-target 60
```

### cohort
Analyze customer cohort retention and LTV.
```bash
bash scripts/script.sh cohort --new-customers 500 --month1-retained 210 --month3-retained 95 --avg-order 85
```

### funnel
Analyze conversion funnel and identify drop-off points.
```bash
bash scripts/script.sh funnel --visits 10000 --pdp-views 3200 --add-to-cart 850 --checkout 320 --orders 280
```

### help
Show all commands.
```bash
bash scripts/script.sh help
```

## Supported Platforms
Shopify, WooCommerce, Amazon, TikTok Shop, multi-channel

## Key Metrics
- ROAS, CAC, LTV, contribution margin
- Reorder point, safety stock, turnover rate
- Conversion rate by funnel stage

## Feedback
https://bytesagain.com/feedback/
Powered by BytesAgain | bytesagain.com

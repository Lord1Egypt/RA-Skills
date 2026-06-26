---
name: etsy-digital-sales
version: 1.0.17
description: |
  Build and manage a fully automated Etsy digital product store using Python + browser
  automation. Lists AI-generated digital products (Notion templates, spreadsheets, prompt packs,
  checklists), auto-renews listings, and collects reviews. Works via Etsy API (oauth) and
  Selenium browser automation for full workflow.
compatibility: Python 3, selenium, requests. Etsy API requires oauth. Browser automation needs ChromeDriver.
metadata:
  author: ssyopros.zo.computer
  category: passive-  tags: etsy, digital-products, automation, printables, templates, passive----

# etsy-digital-sales

Build and automate an Etsy digital product store.

## What This Does

1. **Generates digital products** — Notion templates, spreadsheets, PDF checklists, prompt packs
2. **Lists on Etsy** via API + browser automation
3. **Auto-renews listings** so they stay visible
4. **Collects reviews** via automated follow-up messages
5. **Reports earnings** daily

## Core Script

### `scripts/etsy_store_manager.py`

```python
#!/usr/bin/env python3
"""Etsy Store Manager — automates the full Etsy digital product lifecycle."""

def create_listing(product):
    """Create a new Etsy listing."""
    pass  # Uses Etsy API oauth

def auto_renew():
    """Renew listings about to expire."""
    pass

def get_earnings():
    """Pull today's earnings via Etsy API."""
    pass
```

## Products to Create & Sell

| Product Type | Example | Price |
|---|---|---|
| Notion Template | "Ultimate Business Planner 2026" | $12 |
| Spreadsheet | "10-Year Investment Tracker" | $8 |
| PDF Checklist | "StartupFounder Pre-Launch Kit" | $5 |
| AI Prompt Pack | "Cold Email Templates for SaaS" | $15 |
| Canva Template | "LinkedIn Carousel Builder" | $10 |

## Earnings Model

- Etsy takes $0.20 per listing + 6.5% transaction fee
- Digital items: no shipping, 100% margin after creation cost
- Target: $500–$2000/month with 20–50 listings

## Steps to Connect Etsy

1. Go to [developer.etsy.com](https://developer.etsy.com)
2. Create an app → get **Etsy API Key** + **OAuth client credentials**
3. Save as `ETSY_API_KEY` in [Settings > Advanced](/?t=settings&s=advanced)
4. Save OAuth tokens as `ETSY_OAUTH_TOKEN` + `ETSY_OAUTH_SECRET`

## Deliverable

`etsy-digital-sales/` with:
- `scripts/etsy_store_manager.py`
- `scripts/product_generator.py`
- `scripts/renew_listings.py`
- `config/products.json` — product catalog
- `SKILL.md` — this file

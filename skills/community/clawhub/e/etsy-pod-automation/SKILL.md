---
name: etsy-pod-automation
description: >
  Use when user wants to run Etsy POD store, Printify integration, automate Etsy listings, generate POD designs, manage SEO tags, or schedule social media promotion for Etsy products.
version: "1.0.0"
---


# Etsy POD Automation Skill

Automates the end‑to‑end workflow for running a Print‑on‑Demand dropshipping store on Etsy via Printify.

## Triggering Scenarios
- Run Etsy POD store
- Integrate Printify for product fulfillment
- Automate creation and publishing of Etsy listings
- Generate POD designs with AI
- Create SEO‑optimized titles and 13 tags for Etsy
- Schedule social media posts for new listings (Twitter/X, Instagram, Pinterest)
- Monitor store performance and optimize listings

## Overview
1. **Trend Research** – Scan Google Trends, Etsy trending searches, Instagram/TikTok for ideas.
2. **Design Generation** – Use AI to create designs, export images.
3. **Printify Product Creation** – Call Printify API to create product variants, set pricing.
4. **Etsy Listing** – Upload images, set title, description, 13 tags, price, shipping.
5. **Social Promotion** – Post product mockup with link to Etsy listing.
6. **Performance Monitoring** – Track views, orders, SEO ranking, adjust tags/prices.

## Core Workflow Summary
```text
Trend → AI Design → Printify API → Etsy API → Social Media → Monitor → Optimize
```
- **Pricing** follows `Retail = (Cost+Shipping)/(1‑TargetMargin‑EtsyFeeRate)`.
- **SEO Tags** use the 3‑8 split (3‑4 broad, 8‑9 long‑tail) for a total of 13 tags per product.
- **Photos** – Ensure ≥5 photos; generate lifestyle images via `image_generate` when Printify provides <2 mockups.
- **Automation Schedule** – Recommended daily/weekly cron jobs (see `references/workflows.md`).

## Usage Examples
```bash
# Create a new Valentine’s mug design
openclaw skill run etsy-pod-automation create-product \
  --trend "valentine heart" \
  --product-type mug \
  --price-margin 0.5

# Publish a new listing and tweet it
openclaw skill run etsy-pod-automation publish-listing \
  --listing-id 12345 \
  --tweet "New Valentine's mug! 🎁"

# Daily trend scan and auto‑create top 3 products
openclaw skill run etsy-pod-automation daily‑auto \
  --platforms twitter,instagram,pinterest
```

## References
- `references/workflows.md` – Detailed step‑by‑step API calls, tag algorithm, social media scripts.
- `references/printify-api.md` – Printify catalog, variant lookup, product creation.
- `references/seo-tags.md` – Tag generation rules and examples.
- `references/social-media.md` – Posting commands for X, Instagram, Pinterest.
- `references/performance.md` – Monitoring queries and weekly review process.


---

**Created by [Simon Cai](https://github.com/simoncai519) · More e-commerce skills: [github.com/simoncai519/open-accio-skill](https://github.com/simoncai519/open-accio-skill)**

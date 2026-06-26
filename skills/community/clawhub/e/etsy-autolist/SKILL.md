---
name: etsy-autolist
version: 1.0.17
description: |
  Auto-create and manage digital product listings on Etsy. Creates listings from
  existing digital product files (PDFs, templates, spreadsheets) using Etsy Open API v3.
  Handles listing creation, tagging, pricing, and draft publishing.
metadata:
  author: ssyopros.zo.computer
  category: digital-sales
  display-name: Etsy Auto-Lister
  tags: etsy, digital-products, listings, e-commerce, api
---

# etsy-autolist

Auto-create digital product listings on Etsy using the Etsy Open API v3.

## Etsy API Setup

1. Go to https://developer.etsy.com and register a new app
2. Get your API key (Client Key) and Client Secret
3. Save as secrets: `ETSY_CLIENT_KEY` and `ETSY_CLIENT_SECRET` in [Settings > Advanced](/?t=settings&s=advanced)
4. Get your Shop ID from your Etsy shop URL (etsy.com/shop/{shop_id})
5. Save as secret: `ETSY_SHOP_ID`
6. Run the OAuth helper to get your access token

## OAuth Setup (Required)

Etsy requires OAuth 2.0. To get your personal access token:
1. Register app at developer.etsy.com
2. Save ETSY_CLIENT_KEY and ETSY_CLIENT_SECRET as secrets
3. Run: python scripts/oauth_helper.py
4. Follow the URL printed, authorize, paste code back

## Listings Created

Products - Options Trading Brain PDF — $27
- DeFi Sniper Setup Guide — $37
- Smart Contract Audit Checklist — $47

## After Creation

Manually publish drafts in your Etsy shop dashboard. Bot creates as drafts to avoid review flags.

## Scripts

- `scripts/create_listings.py` — Create all listings as drafts
- `scripts/oauth_helper.py` — OAuth flow to get access token
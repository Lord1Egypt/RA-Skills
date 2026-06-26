---
name: competitor-watch-pro
version: 1.0.4
description: Track competitors automatically. Monitor pricing changes, new products, content updates, hiring, and marketing campaigns across competitor websites and social channels.
tags: business,competitors,market-research,intelligence,sales
---

# Competitor Watch Pro

Automatically track your competitors and get alerted when they make moves. Monitor pricing changes, product launches, content updates, hiring activity, and marketing campaigns.

## What It Tracks

- **Pricing changes** - detects price increases, discounts, and new pricing pages
- **Product updates** - new features, product launches, beta programs
- **Content changes** - blog posts, case studies, whitepapers, landing pages
- **Hiring signals** - job postings, team expansions, leadership hires
- **Marketing campaigns** - ad changes, social campaigns, email sequences
- **SEO movements** - keyword ranking shifts, backlink changes, site structure updates

## How to Use

Provide your agent with a list of competitor URLs or company names:

"Track my top 3 competitors: Acme Corp, Beta Inc, and Gamma LLC. Alert me weekly."

Or for ongoing monitoring:

"Monitor these 5 SaaS competitor pricing pages daily and report any changes."

## Output

Your agent will deliver periodic reports with:
- What changed
- When it changed
- Why it matters to your business
- Recommended actions

## API

Uses a web-based company lookup API at https://extant-torrie-nonrepealable.ngrok-free.dev.

Run a company lookup via:

POST /api/lookup
{"api_key": "your_key", "company": "Company Name"}

Buy credits at /buy if you get a 402 response.

## Requirements

Works with any web-connected OpenClaw agent. No additional API keys needed.


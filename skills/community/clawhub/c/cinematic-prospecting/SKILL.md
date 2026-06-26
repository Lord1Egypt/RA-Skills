---
name: cinematic-prospecting
version: 1.0.0
description: AI-powered business card prospecting with cinematic email outreach. Snap photos, get researched leads, send branded emails with visual mockups.
category: Sales Automation
tags: [sales, outreach, vision-ai, email, networking]
author: Cod3Black <support@cod3black.agency>
repository: https://github.com/cod3black/cinematic-prospecting
license: MIT
pricing:
  oneTime: 69
  subscription: 15
  currency: USD
requirements:
  - Termux (Android) or Linux environment
  - Node.js v16+
  - OpenClaw agent system
  - SMTP credentials (Gmail app password recommended)
  - Vision AI API (OpenClaw built-in)
---

# Cinematic Business Card Prospecting System

Transform business cards into high-converting prospects in 2 minutes.

## What Makes It Different

- **Vision AI** extracts card data from photos automatically
- **Deep brand research**: website analysis, social media audit, competitive positioning
- **Cinematic email design** with brand-matched colors and industry-specific templates
- **Visual POC mockups** embedded in every email (not just text promises)
- **Draft-to-approval workflow** (never send blind)
- **Expected response rates**: 20-30% (vs 1% for cold email)

## Perfect For

- Freelancers at networking events
- Agencies doing outbound sales
- Anyone with a stack of business cards sitting in a drawer

## What's Included

- Multi-card batch processing (process 50+ cards from one photo)
- 5 industry-specific email templates (Financial, Food, Tech, Healthcare, General)
- Brand color extraction & automatic email theming
- Oracle-powered business intelligence research
- POC mockup generators (email templates, social calendars, website concepts)
- Full approval workflow with audit trail
- Response tracking & follow-up scheduling

## ROI Example

- Conference with 50 cards = 10-15 qualified conversations
- Close 2-3 clients at $2K each = $4K-6K revenue
- Time invested: 2 hours vs 25+ hours manual research

## Quick Start

```bash
# Process a single business card photo
node scripts/analyze-business-card.js --image card.jpg

# Batch process multiple cards
node scripts/batch-process.js --dir ./card-photos/

# Send outreach for approved prospect
node scripts/send-cinematic-email.js --prospect-id PROSPECT-123 --template tech

# Review response rates
node scripts/response-tracker.js --last-days 30
```

## Requirements

- Termux (Android) or Linux environment
- Node.js v16+
- OpenClaw agent system
- SMTP credentials (Gmail app password recommended)
- Vision AI API (OpenClaw built-in)

## Support

Email: support@cod3black.agency

---
name: cold-email-engine
description: Automated cold email outreach system with lead enrichment, personalized templates, drip sequences, and CAN-SPAM compliance. Use when building outbound sales pipelines, prospecting businesses, automating email campaigns, enriching leads with contact info, setting up drip follow-ups, or managing cold outreach at scale. Supports Resend, SendGrid, or any SMTP provider.
---

# Cold Email Engine

Automated outbound email pipeline: find leads → enrich contacts → send personalized emails → drip follow-ups.

## Pipeline

1. **Source leads** — from CSV, Google Sheets, API scraping, or manual input
2. **Enrich** — find emails via website scraping, Hunter.io, or Apollo
3. **Personalize** — variable substitution in templates ({name}, {company}, {pain_point})
4. **Send** — via Resend, SendGrid, or raw SMTP with rate limiting
5. **Drip** — automated follow-ups at day 3 and day 7
6. **Track** — log all sends, bounces, replies to CSV/Sheets

## Requirements

- **Email provider API key** — Resend (`RESEND_API_KEY`), SendGrid, or SMTP credentials
- **Verified sending domain** — with SPF, DKIM, DMARC configured
- **Lead source** — CSV file, Google Sheet ID, or API endpoint

## Quick Start

```bash
# Set environment
export RESEND_API_KEY=your_key

# Send from CSV
node scripts/cold-email-engine.js --source leads.csv --template templates/default.txt --from "Name <hello@yourdomain.com>"

# Dry run (no emails sent)
node scripts/cold-email-engine.js --source leads.csv --template templates/default.txt --dry-run

# Run drip follow-ups
node scripts/cold-email-engine.js --drip --days 3
```

## Configuration

Edit `scripts/config.json`:
- `maxPerDay`: Daily send limit per domain (default: 25)
- `delayBetweenMs`: Delay between emails in ms (default: 3000)
- `dripDays`: Follow-up schedule [3, 7] days after initial send
- `suppressionFile`: Path to suppression/unsubscribe list
- `trackingFile`: Path to send log

## Templates

Templates use `{variable}` syntax. Available variables:
- `{first_name}`, `{last_name}`, `{email}`
- `{company}`, `{website}`, `{city}`, `{state}`
- `{pain_point}` — auto-generated from website analysis
- `{sender_name}`, `{sender_title}`

### Template Example
```
Subject: {company} — quick question

Hi {first_name},

I noticed {company} {pain_point}. We help businesses like yours 
fix that in under a week.

Would it make sense to chat for 10 minutes this week?

{sender_name}
{sender_title}
```

## Compliance

- CAN-SPAM: physical address in footer, unsubscribe mechanism
- GDPR: only email businesses (B2B exemption), honor removal requests
- Rate limits: 25/day per domain, 3-second delay between sends
- Suppression list checked before every send

## Scripts

- `scripts/cold-email-engine.js` — Main send engine
- `scripts/enrich-leads.js` — Email finder from websites/domains
- `scripts/config.json` — Configuration

## References

- See `references/deliverability.md` for domain warmup and inbox placement
- See `references/templates.md` for proven email templates by industry

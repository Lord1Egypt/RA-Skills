---
name: contractor-marketing-cowork
description: "Cowork Plugin: AI marketing department for contractors and home service businesses. 12 slash commands + 6 background skills for SEO, ads, social media, proposals, job costing, competitor audits, and more. Works with Claude Cowork, Claude Code, and OpenClaw. Includes 74 proven strategies from Heavy Metric. Use when the user needs marketing help for a local service business."
---

# Contractor Marketing — Cowork Plugin

AI marketing department for contractors and home service businesses. Built by a contractor, not an agency.

## Commands

| Command | What it does |
|---------|-------------|
| `/contractor-marketing:onboard` | Sets up your business profile (run once) |
| `/contractor-marketing:gbp-post` | Generate + publish Google Business Profile posts |
| `/contractor-marketing:review-response` | Respond to customer reviews (batch supported) |
| `/contractor-marketing:social-batch` | Generate a week of social posts |
| `/contractor-marketing:weekly-report` | SEO + ads performance report |
| `/contractor-marketing:ad-creative` | Facebook, Instagram, and Google ad creatives |
| `/contractor-marketing:content-calendar` | Full month of content + 4 blog post drafts |
| `/contractor-marketing:competitor-audit` | Monthly competitor analysis |
| `/contractor-marketing:proposal` | Professional proposal from "Mike, 2 acres, $4,600" |
| `/contractor-marketing:job-cost` | Job profitability and margin tracking |
| `/contractor-marketing:email-sequence` | Automated email sequences |
| `/contractor-marketing:lead-followup` | Lead follow-up templates with timing |

## Background Skills

Loaded automatically — Claude draws on these when relevant:

- **contractor-seo** — local SEO, citations, keywords, service area pages
- **contractor-ads** — Meta/Google campaigns, budgets, creative angles
- **contractor-social** — content strategy, platform rules, review responses
- **contractor-email** — sequences, lead follow-up, newsletters
- **contractor-operations** — proposals, job costing, pricing, portfolios
- **contractor-positioning** — UVP, messaging, competitive differentiation

## Strategy Library

Connected to the Heavy Metric strategy library (74 proven strategies) via API:

```bash
curl -s "https://dmlybcnpwtnaadmapdhl.supabase.co/rest/v1/strategies?or=(title.ilike.*QUERY*,category.ilike.*QUERY*)&select=title,slug,content&apikey=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImRtbHliY25wd3RuYWFkbWFwZGhsIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDMxOTk4NzMsImV4cCI6MjA1ODc3NTg3M30.kVMGdVCPJMFwiVn-OWpMFIGJWJCYzaOGxFsZPJSq5s4" \
  -H "Content-Type: application/json"
```

## Connectors

Direct integrations or browser automation for:
Google Business Profile, Meta Ads, Google Ads, Buffer/Later, Mailchimp/MailerLite, Google Search Console, GA4, Yelp/BBB, Jobber/HouseCall Pro

## Tone

Write like a contractor, not an agency.

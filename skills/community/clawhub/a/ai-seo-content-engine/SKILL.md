---
name: ai-seo-content-engine
description: Automated SEO content generator that schedules daily SaaS review articles using OpenAI GPT-4o, publishes to a Hugo blog via API, and tracks output in Google Sheets. Supports 18 SaaS categories and 4 content types.
tags: [seo, content, blog, openai, gpt, hugo, saas, reviews, automation, n8n]
author: mhmalvi
version: 1.2.0
license: CC BY-NC-SA 4.0
metadata:
  clawdbot:
    emoji: "\u270D\uFE0F"
    requires:
      n8nCredentials: [google-sheets-oauth2, openai]
      env: [NICHE_BLOG_ADMIN_API_KEY]
    os: [linux, darwin, win32]
---

# SEO Content Engine

An automated content generation pipeline that produces SEO-optimized SaaS review articles on a schedule, publishes to a Hugo blog, and tracks everything in Google Sheets.

## Problem

Building organic search traffic requires consistent, high-quality content. Manually researching, writing, and publishing SEO articles is time-consuming. Most SaaS review sites need 2-4 articles per week to compete — that's hours of work daily.

This engine automates the entire pipeline: topic selection, article generation, blog publishing, and tracking.

## What It Does

1. **Topic Selection** — Randomly selects from 18 SaaS tools and 4 content types (reviews, comparisons, best-of guides, how-to guides)
2. **AI Article Generation** — Uses OpenAI GPT-4o to write 1,500-2,500 word SEO articles with proper headings, pros/cons, pricing, and recommendations
3. **Hugo Formatting** — Adds frontmatter (title, date, categories, tags, affiliate links) for Hugo static site publishing
4. **Blog Publishing** — Pushes the formatted post to a Hugo blog via admin API
5. **Sheet Tracking** — Logs every published article (slug, date, category, tool, status) in Google Sheets
6. **Owner Notification** — Sends email alert when a new article is published for review

## Included Workflows

| # | File | Purpose |
|---|------|---------|
| 1 | `content-gen-workflow.json` | Scheduled content generation, publishing, tracking, and notification |

## Architecture

```
Schedule Trigger (every 12 hours)
    |
    v
Keyword & Topic Selector
    |  (random SaaS tool + content type)
    v
OpenAI GPT-4o Article Generator
    |  (1500-2500 word SEO article)
    v
Hugo Post Formatter
    |  (add frontmatter, categories, tags)
    v
Publish to Blog (Admin API)
    |
    +------+------+
    |             |
    v             v
Track in       Notify Owner
Google Sheets  (email alert)
```

## Supported Content Types

| Type | Template Example |
|------|-----------------|
| Review | `{Tool} Review 2026: Pricing, Features, and Honest Take` |
| Comparison | `{Tool A} vs {Tool B}: Which Is Better in 2026?` |
| Best-of | `Best {Category} Tools for {Audience} in 2026` |
| Guide | `How to Set Up {Tool} for {Use Case}` |

## Supported SaaS Categories

CRM, Project Management, Email Marketing, Automation, Database, Communication, Issue Tracking, Hosting, CDN & Security, Backend, Payments — covering 18 tools including HubSpot, Notion, Pipedrive, ClickUp, ConvertKit, Zapier, Make, n8n, Airtable, Supabase, Stripe, and more.

## Required n8n Credentials

| Credential Type | Used For | Placeholder in JSON |
|----------------|----------|---------------------|
| OpenAI | GPT-4o article generation | `YOUR_OPENAI_CREDENTIAL_ID` |
| Google Sheets OAuth2 | Article tracking | `YOUR_GOOGLE_SHEETS_CREDENTIAL_ID` |

## Configuration Placeholders

| Placeholder | Description |
|-------------|-------------|
| `YOUR_OPENAI_CREDENTIAL_ID` | Your n8n OpenAI credential ID |
| `YOUR_GOOGLE_SHEETS_CREDENTIAL_ID` | Your n8n Google Sheets credential ID |
| `YOUR_BLOG_ADMIN_API_KEY` | API key for your blog admin API |
| `YOUR_TRACKER_SHEET_ID` | Google Sheet ID for tracking published articles |
| `YOUR_NOTIFICATION_EMAIL` | Email for publish notifications |
| `YOUR_SMTP_CREDENTIAL_ID` | Your n8n SMTP credential ID |

## Quick Start

### 1. Prerequisites
- n8n v2.4+ (self-hosted)
- OpenAI API key (GPT-4o access)
- Hugo blog with an admin API (e.g., blog-admin service)
- Google Sheets OAuth2 credentials

### 2. Environment Variables
```bash
NICHE_BLOG_ADMIN_API_KEY=your-blog-admin-api-key
```

### 3. Create Tracking Sheet
Set up a Google Sheet with columns: `slug`, `source`, `date`, `category`, `tool`, `status`. Use `appendOrUpdate` matching on `slug` + `source` to prevent duplicates.

### 4. Import & Configure
Import the workflow JSON into n8n. Replace all `YOUR_*` placeholders. Connect your OpenAI and Google Sheets credentials.

### 5. Activate
Activate the workflow. It runs every 12 hours by default — adjust the schedule trigger as needed.

## Companion Skills

For cross-posting generated articles to LinkedIn, Dev.to, Hashnode, and other platforms, see the **multi-platform-crosspost** skill.

## Use Cases

1. **Affiliate marketing sites** — Auto-generate SaaS review content with affiliate link placeholders
2. **Niche blogs** — Build organic SEO traffic with consistent publishing
3. **SaaS comparison sites** — Automated tool comparisons and best-of lists
4. **Content agencies** — Generate first drafts for human editors to refine
5. **Personal blogs** — Keep publishing cadence without daily writing

## Customization

- **Tools list** — Edit the Code node to add/remove SaaS tools and categories
- **Content quality** — Adjust the system prompt and temperature for different tones
- **Schedule** — Change trigger frequency (daily, twice daily, weekly)
- **Blog API** — Modify the HTTP Request node for any blog admin API
- **Affiliate links** — Add affiliate URLs in the frontmatter `affiliate_links` field

## Requirements

- n8n v2.4+ (self-hosted recommended)
- OpenAI API account (GPT-4o, ~$0.01-0.03 per article)
- Hugo blog with admin API endpoint
- Google Sheets OAuth2 credentials

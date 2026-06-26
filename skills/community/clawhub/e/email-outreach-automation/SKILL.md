---
name: email-outreach-automation
description: Cold email outreach pipeline with multi-step sequences, reply tracking, bounce handling, and campaign analytics. 4 production-ready n8n workflows with Google Sheets CRM and SMTP integration.
tags: [outreach, cold-email, sales, sequences, crm, automation, prospecting, n8n, google-sheets]
author: mhmalvi
version: 1.2.0
license: CC BY-NC-SA 4.0
metadata:
  clawdbot:
    emoji: "\U0001F4E7"
    requires:
      n8nCredentials: [google-sheets-oauth2, smtp]
      env: [OUTREACH_SECRET, OUTREACH_ADMIN_EMAIL]
    os: [linux, darwin, win32]
---

# Email Outreach Automation

A complete cold email outreach pipeline built on n8n and Google Sheets. Import prospects, run multi-step email sequences, track replies, and get daily campaign reports.

## Problem

Cold email outreach requires consistent followup sequences, reply detection, and status tracking across hundreds of prospects. Most tools charge $50-200/month per seat and lock you into their platform.

This system provides a free, self-hosted outreach pipeline with full control over your data and sending.

## What It Does

1. **Prospect Import** — Webhook API to import prospects (single or batch) with validation and deduplication
2. **Email Sequences** — 4-step automated outreach: initial, follow-up 1 (Day 3), follow-up 2 (Day 7), breakup (Day 14)
3. **Reply Tracking** — Webhook to mark prospects as replied and notify your team
4. **Campaign Reports** — Daily metrics: reply rates, bounce rates, step distribution, per-campaign breakdown

## Included Workflows

| # | File | Purpose |
|---|------|---------|
| 01 | `01-prospect-import.json` | Webhook import with validation, dedup, and Sheets storage |
| 02 | `02-outreach-sequence.json` | Scheduled 4-step email sequence with timing logic |
| 03 | `03-reply-tracker.json` | Webhook to log replies and notify team |
| 04 | `04-campaign-report.json` | Daily campaign analytics email |

## Architecture

```
Prospect Import (webhook/CSV)
    |
    v
Workflow 01: Validate & Store
    +-> Deduplicate by email
    +-> Save to Google Sheets (status: new)

Scheduled (every 4 hours):
    |
    v
Workflow 02: Outreach Sequence
    +-> Read prospects with status != replied/bounced
    +-> Check timing (Day 0/3/7/14)
    +-> Send appropriate email template
    +-> Update step + next_send_at in Sheets

Reply received:
    |
    v
Workflow 03: Reply Tracker
    +-> Match email to prospect
    +-> Mark as replied in Sheets
    +-> Notify team via email

Daily Schedule:
    |
    v
Workflow 04: Campaign Report
    +-> Aggregate metrics by campaign
    +-> Reply rate, bounce rate, step distribution
    +-> Email report to admin
```

## Email Sequence

| Step | Timing | Template |
|------|--------|----------|
| 1 - Initial | Day 0 | Introduction + value proposition |
| 2 - Follow-up 1 | Day 3 | Brief followup + case study mention |
| 3 - Follow-up 2 | Day 7 | Different angle + call-to-action |
| 4 - Breakup | Day 14 | Polite closing, leaves door open |

## Required n8n Credentials

| Credential Type | Used For | Placeholder in JSON |
|----------------|----------|---------------------|
| Google Sheets OAuth2 | Prospect storage and tracking | `YOUR_GOOGLE_SHEETS_CREDENTIAL_ID` |
| SMTP | Sending outreach emails and reports | `YOUR_SMTP_CREDENTIAL_ID` |

## Environment Variables

```bash
# Required
OUTREACH_SECRET=your-webhook-auth-secret
OUTREACH_ADMIN_EMAIL=admin@yourbusiness.com
```

## Configuration Placeholders

| Placeholder | Description |
|-------------|-------------|
| `YOUR_OUTREACH_SHEET_ID` | Google Sheet ID for prospect data |
| `YOUR_GOOGLE_SHEETS_CREDENTIAL_ID` | n8n Google Sheets credential ID |
| `YOUR_SMTP_CREDENTIAL_ID` | n8n SMTP credential ID |
| `YOUR_NOTIFICATION_EMAIL` | Fallback admin email (also set via `OUTREACH_ADMIN_EMAIL` env) |

## Google Sheets Schema (Prospects)

| Column | Type | Description |
|--------|------|-------------|
| email | text | Primary key, prospect email |
| name | text | Prospect name |
| company | text | Company name |
| title | text | Job title |
| campaign | text | Campaign identifier |
| status | text | new / in_sequence / replied / bounced / completed |
| step | number | Current sequence step (0-4) |
| last_sent_at | datetime | When last email was sent |
| next_send_at | datetime | When next email is due |
| replied | boolean | Whether prospect replied |
| replied_at | datetime | Reply timestamp |
| bounced | boolean | Whether email bounced |
| imported_at | datetime | Import timestamp |

## Quick Start

### 1. Prerequisites
- n8n v2.4+ (self-hosted)
- Google Sheets OAuth2 credentials
- SMTP credentials (dedicated outreach email recommended)

### 2. Create Prospect Sheet
Create a Google Sheet with the columns above. Name the tab "Prospects".

### 3. Import & Configure
Import all 4 JSON files into n8n. Replace all `YOUR_*` placeholders.

### 4. Import Prospects
```bash
curl -X POST https://your-n8n.com/webhook/outreach/import \
  -H "Content-Type: application/json" \
  -d '{
    "_secret": "your-outreach-secret",
    "prospects": [
      {"email": "john@company.com", "name": "John", "company": "Acme Inc", "campaign": "q1-2026"}
    ]
  }'
```

### 5. Track Replies
```bash
curl -X POST https://your-n8n.com/webhook/outreach/reply \
  -H "Content-Type: application/json" \
  -d '{"email": "john@company.com", "subject": "Re: Quick question", "message": "Sure, let us chat!"}'
```

## Use Cases

1. **Freelancers** — Automated client prospecting with professional followup
2. **Agencies** — Multi-campaign outreach with per-campaign analytics
3. **SaaS founders** — Early-stage customer development outreach
4. **Recruiters** — Candidate outreach with sequenced followup
5. **Sales teams** — Supplement CRM with lightweight, self-hosted sequences

## Requirements

- n8n v2.4+ (self-hosted recommended)
- Google Sheets OAuth2 credentials
- SMTP email credentials (use dedicated sending domain for deliverability)

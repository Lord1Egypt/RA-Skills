---
name: email-campaign
description: PayLessTax email automation system - 4x daily, 250 emails each
version: 2.0.0
author: Migration from Agent Zero
---

# Email Campaign Skill

## Overview
High-volume email campaign system for PayLessTax. Delivers 1,000 emails daily in 4 batches.

## Purpose
- Send 250 emails per batch, 4 batches daily (6am, 12pm, 3pm, 6pm)
- Track bounces and unsubscribes
- Scrape inbox for new contacts
- Manage Google Workspace Gmail via service account

## Input Variables
| Variable | Description | Example |
|----------|-------------|---------|
| GOOGLE_SERVICE_ACCOUNT | JSON credentials | { "type": "service_account", ... } |
| USER_EMAIL | Sending user email | clolivier@wespeakallday.com |
| ALIAS_EMAIL | From address | info@paylesstax.co.za |
| MAILING_LIST_PATH | Excel CSV of contacts | /workdir/mailing-list.xlsx |
| BATCH_SIZE | Emails per batch | 250 (do NOT exceed Gmail limits) |

## Signature Template
```
Best regards,

The PayLessTax Team
www.paylesstax.co.za | info@paylesstax.co.za

Should you wish to no longer receive these emails, reply with UNSUBSCRIBE
```

## Template Variables (Email Body)
| Variable | Usage |
|----------|-------|
| {{RECIPIENT_NAME}} | Parsed from email or "Valued Client" |
| {{TAX_TIP}} | Rotating tax tip of the day |
| {{PERSONALIZED_OFFER}} | Dynamic offer based on last interaction |
| {{UNSUBSCRIBE_LINK}} | For compliance |

## Triggers
Scheduled via OpenClaw scheduler:
- 06:00 (Morning batch + inbox scraping)
- 12:00 (Midday batch)
- 15:00 (Afternoon batch)
- 18:00 (Evening batch + maintenance)

## APIs & Dependencies
- Google Gmail API (service account with domain-wide delegation)
- Pandas (for Excel/CSV contact lists)
- google-auth,google-auth-oauthlib,google-auth-httplib2,google-api-python-client

## Rate Limits
- Gmail API: 250 messages/user/second (safe limit: 250/batch with delays)
- Daily quota: Managed across 4 batches

## Output
```json
{
  "batch_id": "2026-03-03-06-00",
  "sent_count": 250,
  "failed": 3,
  "bounces": ["bad@example.com"],
  "unsubscribes": ["user@example.com"]
}
```

## Files
- index.py - Main email sending logic
- templates/email-body.html - HTML email template
- .env.example - Environment variables

## Compliance Notes
- Always include physical address
- Honor unsubscribe within 10 days
- Include company registration number

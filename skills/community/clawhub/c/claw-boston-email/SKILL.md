---
name: claw-boston-email
description: |
  Give your OpenClaw a real email address at @claw.boston.
  Send and receive emails with attachments, search your inbox, get notified of new messages.
  Setup takes one command.
version: 0.2.0
author: claw.boston
url: https://claw.boston
---

## Setup

On first use, I'll register a @claw.boston email for you. Just say:
"Set up my email" or "I need an email address"

Your API key will be stored locally at:
~/.openclaw/skills/claw-boston-email/config.json

## Available Commands

### Send email
"Send an email to alice@example.com about tomorrow's meeting"
"Email bob@company.com: the report is ready"

### Send with attachment
"Send the report.pdf to alice@example.com"
"Email the summary to bob with the attached file"

### Check inbox
"Do I have new emails?"
"Check my inbox"

### Read email
"Read the latest email"
"What did alice@example.com send me?"

### Reply
"Reply to that email saying I agree"

### Search emails
"Search my inbox for emails about the project"
"Find emails from alice@example.com"
"Search for 'invoice' in my emails"

### View account
"What's my email plan?"
"How many emails have I sent today?"

## API Reference

Base URL: https://api.claw.boston

### Register
POST /api/register
Body: { "instance_token": "<auto>", "preferred_name": "<optional>" }
Response: { "address": "xxx@claw.boston", "api_key": "ck_...", "plan": "free", "limits": { "daily_send": 15, "history_days": 7 } }

### Send
POST /api/send
Header: Authorization: Bearer <api_key>
Body: { "to": "...", "subject": "...", "text": "...", "attachments": [{ "filename": "...", "content": "<base64>", "content_type": "..." }] }
Response: { "id": "msg_xxx", "status": "sent", "to": "...", "subject": "..." }

### Inbox
GET /api/inbox
Header: Authorization: Bearer <api_key>
Query: ?limit=20&offset=0&since=<unix_timestamp>
Response: { "emails": [...], "total": N, "limit": 20, "offset": 0 }

### Read single email
GET /api/inbox/<id>
Header: Authorization: Bearer <api_key>
Response: { "id": "...", "from": "...", "to": "...", "subject": "...", "text": "...", "created_at": N, "has_attachments": bool, "attachments": [...] }

### Download attachment
GET /api/inbox/<email_id>/attachments/<att_id>
Header: Authorization: Bearer <api_key>
Response: Binary file content with Content-Disposition header

### Search
GET /api/inbox/search
Header: Authorization: Bearer <api_key>
Query: ?q=<keyword>&field=all|from|subject|body&limit=20&offset=0
Response: { "query": "...", "emails": [...], "total": N, "limit": 20, "offset": 0 }

### Account info
GET /api/account
Header: Authorization: Bearer <api_key>
Response: { "plan": "...", "address": "...", "limits": {...}, "usage": {...} }

### Configure webhook
POST /api/webhook/config
Header: Authorization: Bearer <api_key>
Body: { "url": "http://localhost:18789/webhook/claw-email" }

## Webhook

I'll configure a webhook to receive real-time notifications when new emails arrive.
The webhook points to your local OpenClaw gateway.

Webhook payload format:
{
  "event": "email.received",
  "timestamp": "ISO8601",
  "data": {
    "id": "msg_xxx",
    "from": "sender@example.com",
    "to": "you@claw.boston",
    "subject": "Subject line",
    "preview": "First 200 chars...",
    "is_suspicious": false,
    "has_attachments": false,
    "attachment_count": 0
  }
}

## Behavior Guide

### First-time setup flow:
1. Check if ~/.openclaw/skills/claw-boston-email/config.json exists
2. If not → ask user for preferred email name (or offer to auto-generate)
3. Read OpenClaw instance info, generate instance_token = HMAC-SHA256(instance_id + install_time + hostname)
4. Call POST /api/register with instance_token and preferred_name
5. Save the returned api_key to config.json
6. Call POST /api/webhook/config to set up real-time notifications
7. Confirm to user: "Your email is xxx@claw.boston"

### Sending email:
1. Read api_key from config.json
2. Compose email based on user's natural language instruction:
   - Infer appropriate subject line
   - Write professional but concise email body
   - Match the language the user used (English/Chinese/etc)
3. If user mentions files to attach, encode them as base64 and include in attachments[]
4. Call POST /api/send
5. Confirm: "Email sent to xxx. Subject: ..."

### Checking inbox:
1. Call GET /api/inbox
2. Summarize: "You have N new emails:" then list from/subject/preview for each
3. If no emails: "Your inbox is empty"

### Reading a specific email:
1. Call GET /api/inbox/<id>
2. Present the full email content naturally
3. If has_attachments is true, list the attachments with filenames and sizes

### Searching emails:
1. Call GET /api/inbox/search?q=<keyword>
2. Present results: "Found N emails matching '<query>':" then list from/subject/date
3. If no results: "No emails found matching '<query>'"
4. Offer: "Want me to read any of these?"

### Replying:
1. Use the from address of the original email as the new "to"
2. Prepend "Re: " to original subject (if not already there)
3. Compose reply based on user's instruction
4. Call POST /api/send

### Webhook notification (incoming email):
1. Parse the webhook payload
2. Notify user: "New email from {from} — Subject: {subject}"
3. Show preview
4. If has_attachments, mention: "This email has {attachment_count} attachment(s)"
5. Ask: "Want me to read the full email?"

### Checking account:
1. Call GET /api/account
2. Report: plan, daily usage, limits

## Notes

- Free plan: 15 emails/day, 7-day history, 1MB attachments, basic search
- Pro plan ($5/mo): 500 emails/day, 90-day history, 10MB attachments, full search
- Foundation plan ($29 one-time): same as Pro, forever, with member badge
- Emails flagged as suspicious (potential prompt injection) will be noted
- Upgrade at https://claw.boston
- Discord: https://discord.gg/WuPp45xumx

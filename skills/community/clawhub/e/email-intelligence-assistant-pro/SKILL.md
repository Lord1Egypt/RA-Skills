# Email Customer Assistant

> IMAP Email Read → AI Classification → Reply Suggestions → Feishu Push Summary

**Slug:** `email-customer-assistant`
**Platform:** ClawHub + Tencent Skillhub
**Author:** 91Skillhub Team

---

## Overview

| Feature | Description |
|---------|-------------|
| IMAP Email Read | Connect to any IMAP-capable mailbox (QQ/163/Enterprise/Gmail, etc.) |
| AI Classification | 🔴 Urgent 🟠 Important 🟡 Normal 🟢 Can Wait |
| Reply Suggestions | AI generates multi-language reply suggestions, sent after user confirmation |
| Feishu Push | Summary pushed to Feishu group chat or DM in real time |

---

## Classification Rules

| Label | Example Keywords |
|-------|----------------|
| 🔴 Urgent | refund, refund request, complaint, negative review, urgent, immediately |
| 🟠 Important | after-sales, repair, return, exchange, payment, invoice |
| 🟡 Normal | inquiry, price, specs, logistics, shipping |
| 🟢 Can Wait | hello, thank you, goodbye, already handled |

---

## Pricing Tiers

| Tier | Price | Mailboxes | Daily Limit | Features |
|------|-------|-----------|-------------|----------|
| Free | ¥0 | 1 | 10 emails | Text classification, basic reply suggestions |
| Standard | ¥9.9/mo | 3 | 50 emails | Priority classification, multi-language replies |
| Pro | ¥29/mo | Unlimited | 200 emails | Real-time urgent push, batch replies |
| Max | ¥69/mo | Unlimited | Unlimited | API priority, team collaboration, custom rules |

**Token Prefixes:** `EMAIL-FREE` / `EMAIL-STD` / `EMAIL-PRO` / `EMAIL-MAX`

---

## Quick Start

### 1. Configure Email

First-time setup requires IMAP connection info:

```
IMAP Config:
- Server: imap.example.com
- Port: 993 (SSL)
- Username: your@email.com
- Password: App-specific password (NOT your login password)

Recommended: Use "App Password" from your email provider settings
```

### 2. Configure AI API

Supports OpenAI-compatible API. Configure your API endpoint:

```
Supports:
- OpenAI API (api.openai.com)
- Self-hosted compatible API (Claude/Grok/domestic models, etc.)
- Domestic proxy API (if needed)
```

### 3. Configure Feishu Push

Configure Feishu bot webhook or user_id to receive push notifications.

---

## Multi-Language Support

| Language | Description |
|----------|-------------|
| Chinese (zh) | Default |
| English (en) | Business English |
| Japanese (ja) | Keigo/formal |
| Korean (ko) | Keigo/formal |

---

## Technical Architecture

```
email-customer-assistant/
├── SKILL.md
├── README.md
├── scripts/
│   ├── check_emails.py      # Main script for checking new emails
│   ├── imap_client.py       # IMAP connection wrapper
│   ├── classifier.py        # AI classifier
│   ├── reply_generator.py   # Reply generator
│   └── feishu_pusher.py     # Feishu pusher
├── config/
│   └── config.yaml.example  # Config template
└── requirements.txt
```

---

## Usage Limits

- **Read-only emails** — no sending or deleting
- **No platform API access** — only reads from IMAP mailbox
- User confirmation required before any action
- Follow email provider terms of service

---

> For paid plans, visit [YK-Global.com](https://yk-global.com)

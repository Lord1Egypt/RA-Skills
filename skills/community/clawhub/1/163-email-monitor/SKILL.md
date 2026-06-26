---
name: 163-email-monitor
description: Connect to 163/126/yeah.net (Coremail) email via IMAP, read inbox, search emails, and send emails via SMTP. Activate when user asks to check email, read mail, send email, or monitor inbox on 163/126/yeah.net accounts. Handles the Coremail-specific IMAP ID command requirement that causes "Unsafe Login" errors in standard clients.
---

# 163 Email Monitor

## Key Insight: Coremail ID Command

163/126/yeah.net use Coremail which **requires an IMAP ID command before any mailbox operation**, otherwise returns "Unsafe Login" even with valid credentials.

## Setup

### Prerequisites

Credentials in `~/.openclaw/email-monitor/.env`:

```
IMAP_SERVER=imap.163.com
IMAP_PORT=993
SMTP_SERVER=smtp.163.com
SMTP_PORT=465
EMAIL_ADDRESS=your@163.com
EMAIL_PASSWORD=your_auth_code
```

The `EMAIL_PASSWORD` is the **授权码** (authorization code), not the login password. Users obtain it from: 163 Mail → Settings → POP3/SMTP/IMAP → Enable IMAP → Get authorization code.

### Server Reference

| Provider | IMAP Server | SMTP Server |
|----------|------------|------------|
| 163.com | imap.163.com:993 | smtp.163.com:465 |
| 126.com | imap.126.com:993 | smtp.126.com:465 |
| yeah.net | imap.yeah.net:993 | smtp.yeah.net:465 |

## Usage

All operations use `scripts/mail_client.py`:

```bash
# Read unread emails
python3 scripts/mail_client.py read --unread

# Read latest N emails
python3 scripts/mail_client.py read --latest 10

# Search emails by keyword
python3 scripts/mail_client.py search "amazon"

# Search by sender
python3 scripts/mail_client.py search --from "no-reply@amazon.com"

# Search by date range
python3 scripts/mail_client.py search --since 2026-03-01 --before 2026-03-23

# Send email
python3 scripts/mail_client.py send --to recipient@example.com --subject "Hello" --body "Content here"

# Send with attachment
python3 scripts/mail_client.py send --to recipient@example.com --subject "Report" --body "See attached" --attach /path/to/file.pdf
```

Pass `--env /path/to/.env` to override default config location.

## Troubleshooting

| Error | Cause | Fix |
|-------|-------|-----|
| `Unsafe Login` | Missing ID command | Use this skill's script (handles automatically) |
| `AUTHENTICATIONFAILED` | Wrong auth code | Regenerate 授权码 in 163 web settings |
| `LOGIN failed` | IMAP not enabled | Enable IMAP in 163 Mail → Settings |

---
name: email-send-hanson
description: Send, read, and summarize email through SMTP and IMAP using environment-based credentials.
license: MIT
metadata:
  version: "1.0.0"
  tags: ["email", "smtp", "imap"]
---

# Email Send Hanson Skill

Use this skill when the task requires sending an email, reading recent inbox messages, or summarizing recent email activity.

## Requirements

The script uses these environment variables:

- `EMAIL_HOST`: SMTP host.
- `IMAP_HOST`: IMAP host.
- `EMAIL_PORT`: SMTP port, default `465`.
- `EMAIL_USER`: mailbox username and sender address.
- `EMAIL_PASSWORD`: mailbox password or app password.
- `EMAIL_USE_SSL`: set to `false` to use STARTTLS instead of SMTP SSL.

It also accepts `.env` files that use `SMTP_HOST`, `SMTP_PORT`, `SMTP_USER`, `SMTP_PASS`, and `SMTP_SECURE`.

## Process

1. Confirm recipient, subject, and body before sending email.
2. Use attachments only with local file paths that exist.
3. Read or analyze inbox messages only when the user asks for mailbox inspection.
4. Return the script JSON result directly or summarize the important fields.

## Script

Use `scripts/server.py`.

Examples:

```powershell
uv run langchain-skills script email-send-hanson server.py --execute send --to user@example.com --subject "Hello" --body "Message"
uv run langchain-skills script email-send-hanson server.py --execute read --limit 5
uv run langchain-skills script email-send-hanson server.py --execute analyze --limit 10
```

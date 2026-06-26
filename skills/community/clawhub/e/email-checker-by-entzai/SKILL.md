---
name: email-checker-for-mac
description: Automated email assistant for Apple Mail. Runs on a schedule, scores priority, drafts AI replies, and emails you a report. Manage your inbox from Telegram or WhatsApp — never open the bot inbox again.
homepage: https://github.com/entzclaw/email-checker-for-mac
metadata: {"clawdbot":{"emoji":"📬","os":["darwin"],"requires":{"bins":["python3","osascript"],"apps":["Mail.app"]}}}
---

# Email Checker for Mac

Automated email assistant for Apple Mail on macOS. Runs on a schedule, scores
your unread emails by priority, drafts AI replies, and sends you a report —
so you can manage your inbox from Telegram or WhatsApp without ever opening Mail.app.

## Installation

```bash
git clone https://github.com/entzclaw/email-checker-for-mac
cd email-checker-for-mac
bash setup.sh
```

## Setup

The wizard handles everything:
1. Auto-discovers your Mail.app accounts
2. Prompts for name, report email, trusted senders
3. Picks your LLM provider (LM Studio, Ollama, OpenAI, or skip)
4. Tests the connection and writes `config/settings.json`
5. Installs the crontab

## Usage

```bash
# Run a manual check
python3 scripts/email/checker.py

# Send a reply
python3 scripts/email/send_reply.py \
    --to colleague@example.com \
    --subject "Re: Something" \
    --content "Your reply here"

# Check logs
tail -f logs/email_check.log
```

## OpenClaw Integration

Tell OpenClaw via Telegram or WhatsApp:

> _"Run the email checker now"_
> _"Send the draft reply to Alice"_
> _"Add @company.com to my trusted senders"_

## Supported LLM Providers

| Provider | Notes |
|---|---|
| LM Studio | Local or remote vLLM endpoint |
| Ollama | Local |
| OpenAI | Requires API key |
| None | Reports without AI drafts |

## Requirements

- macOS (tested on Tahoe 26.3, Apple Silicon)
- Python 3
- Mail.app with at least one configured account
- Automation permission: System Settings → Privacy & Security → Automation → Terminal → Mail

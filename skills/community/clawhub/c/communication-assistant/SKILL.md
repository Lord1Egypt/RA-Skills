---
name: communication-assistant
description: Send formatted notifications via email (himalaya) and iMessage (BlueBubbles). Use when you need to broadcast markdown-formatted messages to email recipients and phone numbers in a single step.
tags: ["email", "imessage", "notification", "communication", "himalaya", "bluebubbles"]
---

# Communication Assistant

Send formatted notifications via email and iMessage from a single command.

## Prerequisites

- **Himalaya** CLI configured (`config/himalaya.toml`)
- **BlueBubbles** server running with env vars set:
  - `BLUEBUBBLES_SERVER` — server URL
  - `BLUEBUBBLES_PASSWORD` — API password

## Usage

```bash
./scripts/send-notification.sh \
  --content <markdown-file> \
  --emails <comma-separated-emails> \
  --phones <comma-separated-phone-numbers>
```

### Arguments

| Flag | Required | Description |
|---|---|---|
| `--content` | Yes | Path to markdown file to send |
| `--emails` | No* | Comma-separated email recipients |
| `--phones` | No* | Comma-separated phone numbers (iMessage) |

\* At least one of `--emails` or `--phones` must be provided.

## Example

```bash
# Format first
prettier --write announcement.md --config config/.prettierrc.json
markdownlint announcement.md --config config/.markdownlint.json

# Send to team
./scripts/send-notification.sh \
  --content announcement.md \
  --emails team@company.com \
  --phones +15555550123
```

## Workflow

1. Draft your message in markdown
2. Format with Prettier + markdownlint per workspace config
3. Run `send-notification.sh` to deliver via email and/or iMessage

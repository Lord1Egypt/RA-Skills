---
name: clawaimail
display_name: ClawAIMail - Email for AI Agents
version: 0.2.7
description: Give your AI agent a real email address. Send, receive, and manage emails via API.
author: ClawAIMail
author_url: https://clawaimail.com
repository: https://github.com/joansongjr/clawaimail
license: MIT
tags:
  - email
  - inbox
  - send-email
  - receive-email
  - ai-agent
  - mcp-server
  - api
  - automation
---

# ClawAIMail - Email for AI Agents

Give your AI agent its own email address. Create inboxes, send and receive real emails, search messages, and manage threads — all through a simple API.

## What it does

- **Create Inboxes**: Instantly create email addresses like `mybot@clawaimail.com`
- **Send Emails**: Send real emails from your agent's address
- **Receive Emails**: Get notified when emails arrive via webhook or WebSocket
- **Read & Search**: Read messages, search by keyword, track threads
- **Manage**: Labels, custom domains, and more

## Setup

1. Get your API key at https://clawaimail.com (free tier: 3 inboxes, 3K emails/month)
2. Set your environment variable:

```
CLAWAIMAIL_API_KEY=pb_your_api_key
```

## OpenClaw Configuration

⚠️ **Important**: Do NOT add `mcpServers` to `openclaw.json` — that field is not supported and will crash the Gateway.

Use **mcporter** (OpenClaw's MCP management tool) to configure:

```bash
# Add ClawAIMail as an MCP server
mcporter config add clawaimail "npx -y clawaimail-mcp" --env CLAWAIMAIL_API_KEY="pb_your_api_key"

# Test it works
mcporter call clawaimail.list_inboxes

# Check status
mcporter status
```

mcporter manages its own config at `~/.openclaw/config/mcporter.json`, separate from the OpenClaw Gateway config.

### Troubleshooting

| Problem | Cause | Fix |
|---------|-------|-----|
| Gateway crashes on startup | `mcpServers` added to `openclaw.json` | Remove it from `openclaw.json`, use `mcporter` instead |
| "CLAWAIMAIL_API_KEY not set" warning | Missing env var | Add `--env CLAWAIMAIL_API_KEY="..."` to mcporter config |
| API calls return errors | Invalid API key or service unreachable | Check key at https://clawaimail.com/dashboard |

## MCP Server Configuration (Claude Desktop / Cursor)

For non-OpenClaw MCP clients:

```json
{
  "mcpServers": {
    "clawaimail": {
      "command": "npx",
      "args": ["-y", "clawaimail-mcp"],
      "env": {
        "CLAWAIMAIL_API_KEY": "pb_your_api_key"
      }
    }
  }
}
```

## Available Tools

| Tool | Description |
|------|-------------|
| `list_inboxes` | List all your email inboxes |
| `create_inbox` | Create a new email inbox (e.g. mybot@clawaimail.com) |
| `send_email` | Send an email from an inbox |
| `list_messages` | List messages in an inbox |
| `read_email` | Read a specific email message |
| `search_emails` | Search emails by keyword |
| `delete_inbox` | Delete an inbox and all its messages |
| `account_info` | Get account info, plan limits, and usage |

## Example Usage

### Create an inbox and send an email
```
User: Create an email inbox called "assistant"
Agent: [calls create_inbox with username "assistant"]
       Created inbox: assistant@clawaimail.com

User: Send an email to john@example.com saying hello
Agent: [calls send_email with to "john@example.com", subject "Hello", text "Hello from your AI assistant!"]
       Email sent successfully.
```

### Check for new messages
```
User: Check my inbox for new messages
Agent: [calls list_messages with inbox_id 1, unread true]
       You have 3 unread messages:
       1. From: jane@company.com - Subject: "Meeting tomorrow"
       2. From: support@service.com - Subject: "Your ticket #1234"
       3. From: newsletter@tech.io - Subject: "Weekly digest"
```

### Search emails
```
User: Find any emails about invoices
Agent: [calls search_emails with query "invoice"]
       Found 2 emails mentioning "invoice":
       1. From: billing@vendor.com - "Invoice #5678 - Due March 15"
       2. From: accounting@partner.org - "Updated invoice attached"
```

## Pricing

- **Free**: 3 inboxes, 3K emails/month
- **Starter** ($5/mo): 10 inboxes, 5K emails/month
- **Pro** ($29/mo): 50 inboxes, 50K emails/month, custom domains
- **Business** ($99/mo): 200 inboxes, 200K emails/month

## Changelog

### 0.1.2
- Fix: Added error handling to all API calls (no more crashes on missing API key or network errors)
- Fix: Accept both number and string IDs for inbox_id/message_id
- Added startup warning when CLAWAIMAIL_API_KEY is not set
- Added global exception handlers to prevent process crashes

### 0.1.0
- Initial release

## Links

- Website: https://clawaimail.com
- API Docs: https://clawaimail.com/docs/
- GitHub: https://github.com/joansongjr/clawaimail
- npm: https://www.npmjs.com/package/clawaimail-mcp
- ClawHub: https://clawhub.com/skills/clawaimail
- Node.js SDK: `npm install clawaimail`
- Python SDK: `pip install clawaimail`

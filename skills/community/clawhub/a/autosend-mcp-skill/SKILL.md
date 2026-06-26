---
name: autosend-mcp
description: Connect to AutoSend email MCP server from OpenClaw using mcporter. Use for managing email campaigns, templates, contacts, and senders via AI.
version: 0.1.0
metadata:
  openclaw:
    requires:
      bins:
        - mcporter
    install:
      - kind: node
        package: mcporter
        bins: [mcporter]
    emoji: "📧"
    homepage: https://docs.autosend.com/ai/mcp-server
---

# AutoSend MCP Skill

Connect OpenClaw to [AutoSend](https://autosend.com) email platform via MCP using [mcporter](https://github.com/steipete/mcporter).

**MCP URL:** `https://mcp.autosend.com/`
**Transport:** Streamable HTTP + OAuth 2.0
**Docs:** https://docs.autosend.com/ai/mcp-server

## Available Tools (19)

| Category | Tools |
|----------|-------|
| Lists & Segments | `get_lists_and_segments` |
| Templates | `list_templates`, `search_templates`, `get_template`, `create_template`, `update_template`, `delete_template` |
| Senders | `list_senders`, `get_sender` |
| Suppression Groups | `list_suppression_groups`, `get_suppression_group` |
| Campaigns | `list_campaigns`, `get_campaign`, `create_campaign`, `update_campaign`, `delete_campaign`, `duplicate_campaign` |
| Analytics | `get_campaign_analytics`, `get_email_activity_analytics` |

### Guided Workflows
- `create-campaign` — Step-by-step campaign creation
- `create-template` — Step-by-step template creation

## Prerequisites

- AutoSend account (https://autosend.com)

## Setup

### 1. Install mcporter

```bash
npm install -g mcporter
```

### 2. Add AutoSend server

```bash
mcporter config add autosend https://mcp.autosend.com/ --auth oauth
```

Or manually create `config/mcporter.json`:
```json
{
  "mcpServers": {
    "autosend": {
      "baseUrl": "https://mcp.autosend.com/",
      "auth": "oauth",
      "description": "AutoSend email MCP"
    }
  }
}
```

### 3. Authenticate

#### Option A: Desktop (has browser)
```bash
mcporter auth autosend
# Browser opens → Log in → Authorize → Done
```

#### Option B: Headless Server (human-in-the-loop)

On servers without a browser, follow these manual steps:

1. **Discover OAuth endpoints:** `GET https://mcp.autosend.com/.well-known/oauth-authorization-server`
2. **Register a dynamic client:** POST to the registration endpoint from step 1
3. **Build an authorization URL** with PKCE (`code_challenge_method=S256`) and open it in a browser on another machine
4. **Authorize and copy the callback URL** — the page won't load locally, but the URL contains the `code` and `state` parameters
5. **Exchange the code for tokens:** POST to the token endpoint with the code and PKCE verifier
6. **Save tokens** to `~/.mcporter/autosend/tokens.json`

To refresh tokens later, POST to the token endpoint with `grant_type=refresh_token`.

See the [MCP OAuth spec](https://modelcontextprotocol.io/) for full details.

### 4. Test Connection

```bash
mcporter call autosend.list_templates
```

## Usage

```bash
# List templates
mcporter call autosend.list_templates

# Create template
mcporter call autosend.create_template \
  templateName="Welcome Email" \
  subject="Welcome!" \
  emailTemplate="<html>..."

# List campaigns
mcporter call autosend.list_campaigns

# Get analytics
mcporter call autosend.get_email_activity_analytics
```

## Token Management

Tokens are stored in `~/.mcporter/autosend/tokens.json` (managed by mcporter).

```bash
# Re-authenticate (refreshes tokens automatically)
mcporter auth autosend

# Verify tokens work
mcporter call autosend.list_templates
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Token expired | Run `mcporter auth autosend` to re-authenticate |
| Invalid credentials | Re-run full OAuth flow with `mcporter auth autosend` |
| Connection timeout | Check network and token validity |

## References

- [AutoSend MCP Docs](https://docs.autosend.com/ai/mcp-server)
- [mcporter GitHub](https://github.com/steipete/mcporter)
- [mcporter on ClawHub](https://clawhub.ai/steipete/mcporter)
- [MCP Specification](https://modelcontextprotocol.io/)

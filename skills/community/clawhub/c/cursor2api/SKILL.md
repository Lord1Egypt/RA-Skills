---
name: cursor2api
description: cursor2api proxy service management tool that converts Cursor IDE's free AI conversations into Anthropic Messages API / OpenAI Chat Completions API format. Supports Docker deployment, environment configuration, token refresh, and complete uninstallation. Use when user asks to: (1) Install or deploy cursor2api, (2) Configure cursor2api for OpenClaw/Claude Code/CC Switch, (3) Refresh or retrieve Cursor Session Token, (4) Uninstall cursor2api.
---

# cursor2api

`cursor2api` bridges Cursor IDE's AI models with OpenClaw/Claude Code by converting Cursor's internal API into standard Anthropic/OpenAI formats.

**Architecture:**
```
OpenClaw / Claude Code
         ↓ (ANTHROPIC_BASE_URL)
cursor2api Docker/Node (:3010)
         ↓ (Session Token)
Cursor Official API
```

## Prerequisites

- Docker (for containerized deployment) or Node.js 18+ (for local)
- A Cursor account with active AI subscription
- `WorkosCursorSessionToken` from Cursor

## Quick Start

```bash
# 1. Get your WorkosCursorSessionToken (see references/token.md)

# 2. Start the service
docker run -d \
  --name cursor-api \
  -p 3010:3000 \
  -e WORKOS_CURSOR_SESSION_TOKEN=your_token \
  waitkafuka/cursor-api:latest

# 3. Configure OpenClaw
export ANTHROPIC_BASE_URL="http://localhost:3010/v1"
export ANTHROPIC_API_KEY="your_token"
export ANTHROPIC_DEFAULT_SONNET_MODEL="claude-sonnet-4-6"

# 4. Restart OpenClaw
openclaw gateway restart
```

## Core Operations

| Operation | Command |
|-----------|---------|
| **Install** | `docker run -d --name cursor-api -p 3010:3000 -e WORKOS_CURSOR_SESSION_TOKEN=token waitkafuka/cursor-api:latest` |
| **Status** | `docker ps \| grep cursor-api` |
| **Refresh Token** | See `references/token.md` |
| **Uninstall** | `docker stop cursor-api && docker rm cursor-api` |

## API Endpoints

| Endpoint | Format | Compatible With |
|----------|--------|-----------------|
| `http://localhost:3010/v1/messages` | Anthropic Messages API | OpenClaw, Claude Code |
| `http://localhost:3010/v1/chat/completions` | OpenAI Chat Completions | CC Switch, Universal |

## Documentation

| Document | Description |
|----------|-------------|
| [Installation Guide](references/installation.md) | Docker deployment, verification, troubleshooting |
| [Token Management](references/token.md) | Obtaining and refreshing WorkosCursorSessionToken |
| [Configuration](references/configuration.md) | OpenClaw, Claude Code, CC Switch setup |
| [Quick Reference](references/quick-reference.md) | One-page cheat sheet |

## ⚠️ Important Notes

- **ToS Risk**: Using third-party proxies may violate Cursor's Terms of Service
- **Token Expiry**: Session tokens expire periodically; monitor and refresh as needed
- **API Stability**: Cursor's internal API may change without notice

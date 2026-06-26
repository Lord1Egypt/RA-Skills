---
name: ainative-platform-overview
description: Top-level discovery skill for the entire AINative platform. Use when (1) Asked "what is AINative?", (2) Exploring platform capabilities, (3) Deciding which SDK/API to use, (4) Getting started questions, (5) Listing all published packages. Acts as the routing hub to specialized skills.
---

# AINative Platform Overview

AINative Studio is an AI development platform that provides APIs, SDKs, MCP tools, and an agent framework for building production AI applications.

## What You Can Build

| Goal | Tool | Skill |
|------|------|-------|
| Add AI chat to your app | Chat Completions API / SDKs | `ainative-chat-completions` |
| Add persistent memory to agents | ZeroMemory API / MCP | `zeromemory-guide` |
| Use 76+ database/vector tools | ZeroDB MCP Server | `zerodb-mcp-guide` |
| Build a custom MCP server | MCP Builder guide | `ainative-mcp-builder` |
| Build multi-agent systems | Agent Framework | `ainative-agent-framework` |
| Monetize your AI app | Echo Developer Program | `echo-developer-guide` |
| Authenticate users | Auth Guide | `ainative-auth-guide` |
| Discover all API endpoints | API Discovery | `ainative-api-discovery` |

## Platform Components

### APIs (89+ endpoints)
Base URL: `https://api.ainative.studio`

| Category | Endpoints | Auth |
|----------|-----------|------|
| Chat Completions | `/v1/public/chat/completions` | API Key |
| Memory (ZeroMemory) | `/api/v1/public/memory/v2/` | API Key |
| ZeroDB | `/api/v1/public/zerodb/` | API Key |
| Auth & Users | `/api/v1/auth/`, `/api/v1/users/` | JWT |
| Credits & Billing | `/api/v1/public/credits/` | API Key |
| Developer Program | `/api/v1/echo/` | JWT |
| Admin | `/admin/` | Superuser JWT |

### Published SDKs

```bash
# React
npm install @ainative/react-sdk

# Next.js
npm install @ainative/next-sdk

# Svelte
npm install @ainative/svelte-sdk

# Vue
npm install @ainative/vue-sdk
```

### Published MCP Servers

```bash
# Full ZeroDB MCP (76 tools — vectors, memory, NoSQL, files, PostgreSQL)
npm install -g ainative-zerodb-mcp-server

# Memory-only MCP (6 tools — lightweight)
npm install -g ainative-zerodb-memory-mcp
```

### CLI Tools

```bash
# ZeroDB instant project setup (auto-configures your IDE)
npx zerodb init
```

### Published Python Packages

```bash
pip install zerodb-mcp          # Python MCP client
pip install zerodb-cli          # Python CLI
pip install langchain-zerodb    # LangChain integration
pip install llama-index-vector-stores-zerodb  # LlamaIndex integration
```

## Quick Start (30 seconds)

```bash
# 1. Get an instant API key + project
npx zerodb init

# 2. Make your first API call
curl -X POST https://api.ainative.studio/v1/public/chat/completions \
  -H "X-API-Key: YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model": "claude-3-5-sonnet-20241022", "messages": [{"role": "user", "content": "Hello"}]}'
```

## Authentication Methods

| Method | Use Case | Header |
|--------|----------|--------|
| API Key | Server-side, agents, SDKs | `X-API-Key: ak_...` |
| Bearer JWT | User sessions | `Authorization: Bearer <token>` |
| OAuth2 | Third-party integrations | Standard OAuth2 flow |

## Related Skills

- `ainative-chat-completions` — Build conversational AI
- `ainative-auth-guide` — Implement authentication
- `ainative-api-discovery` — Explore all endpoints
- `zerodb-mcp-guide` — Use 76 database/vector tools
- `zeromemory-guide` — Add agent memory
- `ainative-mcp-builder` — Build custom MCP servers
- `ainative-agent-framework` — Multi-agent systems
- `echo-developer-guide` — Monetize your AI app

## References

- API docs: `docs/api/API_REFERENCE.md`
- Quick start: `docs/guides/QUICK_START.md`
- Auth guide: `docs/guides/AUTHENTICATION.md`

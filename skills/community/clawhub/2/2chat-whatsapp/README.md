# 2Chat for OpenClaw

Official [2Chat](https://2chat.co) integration for OpenClaw, published on ClawHub. It connects
your OpenClaw agent to 2Chat's remote MCP server so it can send and read **WhatsApp** messages
(WhatsApp Web + WhatsApp Business API), send **SMS**, manage WABA templates, work with contacts
and groups, publish WhatsApp statuses, browse catalogs, and pull voice call records.

## Quick start

```bash
# 1. Register the remote server
openclaw mcp add 2chat \
  --url https://mcp.2chat.io/mcp \
  --transport streamable-http \
  --auth oauth

# 2. Sign in through the browser (OAuth 2.1, no API key)
openclaw mcp login 2chat

# 3. Verify
openclaw mcp probe 2chat
```

Then ask your agent: *"List my connected 2Chat WhatsApp channels."*

## What's included

- `SKILL.md` — the skill manifest, setup steps, full tool reference, and usage guidance.
- `mcp-server.json` — a ready-to-paste `mcp.servers` config block.

## Details

- **Server:** `https://mcp.2chat.io/mcp`
- **Transport:** Streamable HTTP
- **Auth:** OAuth 2.1 with PKCE — browser sign-in, automatic token refresh, no API keys stored.
- **Requires:** a 2Chat account with at least one connected channel. See the
  [2Chat MCP docs](https://developers.2chat.co/docs/MCP/setup).

## License

Published on ClawHub under MIT-0 (per ClawHub policy). "2Chat" and related marks belong to 2Chat.

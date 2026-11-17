# Fuxux OpenClaw / ClawHub skill

Agent skill for [Fuxux](https://www.fuxux.com) — schedule and publish to 14 platforms — Twitter/X, Instagram, LinkedIn, Facebook, TikTok, YouTube, Bluesky, Threads, Pinterest, Discord, Kick, Twitch, Telegram, and Slack — via REST API and MCP.

## Contents

| File | Purpose |
|------|---------|
| **[SKILL.md](./SKILL.md)** | Agent instructions + ClawHub YAML frontmatter (`metadata.openclaw`) — the only file ClawHub requires |
| **[examples/openclaw-mcp.json](./examples/openclaw-mcp.json)** | Copy-paste MCP config (`mcp-remote` + Bearer token) |

## Quick start (users)

1. Create a Fuxux.com account and connect social accounts.
2. Create an API key (**Settings → API keys**).
3. Set `FUXUX_API_KEY=fx_live_…` in the agent workspace `.env`.
4. Wire MCP using [examples/openclaw-mcp.json](./examples/openclaw-mcp.json) or [MCP docs](https://www.fuxux.com/mcp/docs).
5. Install the skill (ClawHub or local):

   ```bash
   openclaw skills install @abogitoff/fuxux-openclaw-skill
   ```

## Related docs

- [API reference](https://www.fuxux.com/reference)
- [OpenAPI JSON](https://www.fuxux.com/openapi.json)
- [MCP setup](https://www.fuxux.com/mcp/docs)
- [OpenClaw on Fuxux](https://www.fuxux.com/openclaw)

---
name: content-distribution
description: Use when the user wants to publish a post, article, or announcement to multiple platforms at once — DEV.to, Hashnode, GitHub Discussions, Reddit, Bluesky, LinkedIn, Medium, or Twitter/X. Handles platform-specific format adaptation, idempotent re-publish, per-community anti-spam rules, and scheduling. Write your message once; this skill routes it everywhere.
version: 2.2.1
license: MIT
homepage: https://github.com/AutomateLab-tech/content-distribution-mcp
compatibility:
  hosts:
    - claude-code
    - cursor
    - claude-desktop
    - windsurf
    - vscode
    - zed
    - continue
    - cline
    - jetbrains
    - warp
metadata:
  npm: "@automatelab/content-distribution-mcp"
  mcpName: io.github.AutomateLab-tech/content-distribution-mcp
---

# content-distribution

Pairs with the `@automatelab/content-distribution-mcp` server. Publishes content to 8+ channels with automatic platform-specific adaptation, idempotent state tracking, and per-community anti-spam enforcement.

## What the MCP handles vs. what you handle

**MCP handles:** OAuth, API retries, scheduling, idempotency, character limits, platform constraints, posting state.  
**You handle:** Writing the platform-specific copy variants (title, body, tags, tone per channel). The MCP returns per-channel hints to guide you.

## Tool overview

| Tool | Use when |
|---|---|
| `distribute_content` | Publish to one or more channels in a single call — the main entry point |
| `get_channel_hints` | Get character limits, tag vocabularies, cooldowns, and formatting rules before writing variants |
| `get_distribution_status` | Check what went live where; retry failed channels |
| `schedule_distribution` | Queue a post for future publish (e.g. "post this tomorrow at 9am UTC") |
| `list_scheduled` | View and manage queued posts |
| `cancel_scheduled` | Remove a queued post |
| `get_platform_config` | Inspect current auth / API key status per platform |
| `test_connection` | Verify credentials before a real publish |

## Default workflow

```
1. get_channel_hints(platforms: ["reddit", "twitter", "linkedin", ...])
   → Read limits, cooldowns, flair options

2. (You) Draft platform-specific copy variants based on the hints

3. distribute_content({
     devto: { title, body_markdown, tags },
     twitter: { text },
     reddit: { subreddit, title, text, flair_id },
     linkedin: { text },
     ...
   })

4. get_distribution_status(id) → confirm each channel succeeded
```

## Idempotency

Every `distribute_content` call returns a `distribution_id`. Calling it again with the same id and same targets is a no-op — safe to retry after a partial failure.

## Server setup

**Claude Code** (`.claude/mcp.json`):
```json
{
  "mcpServers": {
    "content-distribution": {
      "command": "npx",
      "args": ["-y", "@automatelab/content-distribution-mcp"]
    }
  }
}
```

**Claude Desktop** (`claude_desktop_config.json`):
```json
{
  "mcpServers": {
    "content-distribution": {
      "command": "npx",
      "args": ["-y", "@automatelab/content-distribution-mcp"]
    }
  }
}
```

Requires Node 20+. Set platform API keys as environment variables — see the [README](https://github.com/AutomateLab-tech/content-distribution-mcp#configuration) for the full list.

---

Developed by [AutomateLab](https://automatelab.tech). Source: [github.com/AutomateLab-tech/content-distribution-mcp](https://github.com/AutomateLab-tech/content-distribution-mcp).

# Agensi MCP — AI Agent Skill Marketplace Connector

Connect your AI coding agent to the [Agensi marketplace](https://agensi.io) via MCP. Search, discover, and browse community-built SKILL.md skills directly from your terminal.

## What is Agensi?

Agensi is a curated marketplace for SKILL.md skills — the open standard for AI agent instructions. Skills on Agensi work with Claude Code, OpenClaw, Cursor, Codex CLI, Gemini CLI, and 20+ other agents.

## Quick Start

Add the MCP server to your agent config:

```json
{
  "mcpServers": {
    "agensi": {
      "type": "sse",
      "url": "https://mcp.agensi.io/mcp"
    }
  }
}
```

Then ask your agent to search for skills, browse categories, or find what's popular.

## Tools

| Tool | Description |
|------|-------------|
| `search_skills` | Search by keyword, category, or tag |
| `get_skill` | Get full details about a skill |
| `get_popular` | Browse most installed skills |
| `list_categories` | List all categories |
| `get_creator` | View creator profiles |
| `get_skill_requests` | Browse community requests |

## Links

- Marketplace: https://agensi.io/skills
- MCP Server: https://mcp.agensi.io
- Become a creator: https://agensi.io/submit

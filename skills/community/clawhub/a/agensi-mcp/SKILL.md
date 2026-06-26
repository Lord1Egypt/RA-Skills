---
name: "agensi-mcp"
description: "Connect your agent to the Agensi marketplace. Search, discover, and browse AI agent skills from agensi.io directly in your terminal."
version: "1.0.0"
author: "badmenfinance"
type: "integration"
category: "productivity"
tags:
  - "mcp"
  - "marketplace"
  - "skills"
  - "agensi"
  - "skill-md"
invocation: "/agensi"
difficulty: "beginner"
permissions:
  read:
    - "none"
  write:
    - "none"
  network: "https://mcp.agensi.io"
---

# Agensi MCP — Browse the AI Agent Skill Marketplace

Connect your agent to the Agensi skill marketplace (https://agensi.io) via MCP. Search, discover, and browse hundreds of community-built SKILL.md skills without leaving your terminal.

## Setup

Add the Agensi MCP server to your agent's MCP configuration:

### Claude Code

Add to your Claude Code MCP settings (`~/.claude/config.json` or project-level):

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

### OpenClaw

Add to your OpenClaw MCP configuration:

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

### Cursor / Other Agents

Any agent that supports MCP over SSE can connect using the URL: `https://mcp.agensi.io/mcp`

## Available Tools

Once connected, your agent has access to these tools:

- **search_skills** — Search the marketplace by keyword, category, or tag. Returns matching skills with names, descriptions, and pricing.
- **get_skill** — Get full details about a specific skill including description, compatibility, and install instructions.
- **get_popular** — Browse the most installed skills on the marketplace.
- **list_categories** — List all skill categories with counts.
- **get_creator** — View a creator's profile and their published skills.
- **get_skill_requests** — Browse community-requested skills that haven't been built yet.

## Usage Examples

Ask your agent:

- "Search Agensi for code review skills"
- "What are the most popular skills on Agensi?"
- "Find testing and QA skills on the marketplace"
- "Show me skills by creator Samuel Rose"
- "What skills have been requested by the community?"

## About Agensi

Agensi (https://agensi.io) is a curated marketplace for SKILL.md skills compatible with Claude Code, OpenClaw, Cursor, Codex CLI, Gemini CLI, and 20+ AI coding agents. Every skill is security-scanned and works across all major agents.

Browse the full marketplace: https://agensi.io/skills
Become a creator: https://agensi.io/submit

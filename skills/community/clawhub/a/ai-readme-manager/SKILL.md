---
name: ai-readme-manager
description: Manages AI_README.md files so AI agents remember your project conventions across every session
version: 1.3.4
metadata:
  openclaw:
    install:
      - kind: node
        package: ai-readme-mcp
        bins: [ai-readme-mcp]
    homepage: https://github.com/Draco-Cheng/ai-readme-mcp
    emoji: "📋"
---

# AI README Manager

Manages `AI_README.md` files that document your project's conventions for AI assistants. Gives your agent persistent memory of project rules across every session and every iteration.

## Setup

Before this skill works, you must register the MCP server with OpenClaw:

**Option 1: CLI (Recommended)**

On macOS/Linux:
```bash
openclaw mcp set ai-readme-manager '{"command":"npx","args":["ai-readme-mcp@1.3.4"]}'
```

On Windows (cmd):
```cmd
openclaw mcp set ai-readme-manager "{\"command\":\"npx\",\"args\":[\"ai-readme-mcp@1.3.4\"]}"
```

**Option 2: Edit config file**

Add to `~/.openclaw/openclaw.json`:
```json
{
  "mcp": {
    "servers": {
      "ai-readme-manager": {
        "command": "npx",
        "args": ["ai-readme-mcp@1.3.4"]
      }
    }
  }
}
```

Then restart OpenClaw and verify with `openclaw mcp list`.

## When to use

Call `get_context_for_file` before any code-related task — editing, creating, or reviewing files in a project.

## Tools available

- `get_context_for_file` — get relevant project conventions for a specific file path
- `init_ai_readme` — initialize and populate empty AI_README files in a project
- `update_ai_readme` — record new conventions or architectural decisions
- `validate_ai_readmes` — check quality and token efficiency of all AI_README files
- `compress_ai_readme` — remove filler language from an AI_README file to reduce token footprint
- `discover_ai_readmes` — scan and list all AI_README files in a project

## Instructions

### MCP: ai-readme-manager

Before any code-related task, ALWAYS call `get_context_for_file(projectRoot, path)` first.
If `get_context_for_file` reports empty or missing AI_README files, call `init_ai_readme(projectRoot)` to initialize them.
If the user's request or your plan conflicts with AI_README conventions (including during planning), STOP and call `update_ai_readme` to resolve the conflict before proceeding.
When establishing new conventions or making architectural decisions, call `update_ai_readme` to record them.
If AI_README is missing a convention that is already used in 2+ files, call `update_ai_readme` to record it.

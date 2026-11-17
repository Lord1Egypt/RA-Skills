---
name: cli2skill
description: Turn any CLI or MCP server into an Agent Skill. Use when you want to replace an MCP server with a zero-overhead CLI skill, or generate a skill from any command-line tool's --help output.
---

# cli2skill

Convert CLI tools and MCP servers into Agent Skills (markdown files) that any AI coding agent can use. Zero runtime overhead — no persistent processes, no memory leaks.

## Prerequisites

```bash
pip install cli2skill
```

## Commands

### Generate skill from CLI

```bash
# Basic — parse --help and generate SKILL.md
cli2skill generate <executable> --name <skill-name> -o ~/.claude/skills/

# Custom executable path
cli2skill generate "python my_tool.py" --name my-tool \
  --exe-path "python /full/path/my_tool.py" -o ~/.claude/skills/

# From saved help text
cli2skill generate mytool --help-file help_output.txt -o ~/.claude/skills/

# Skip subcommand parsing (faster, top-level only)
cli2skill generate gh --name github-cli --no-subcommands -o ~/.claude/skills/
```

### Preview parsed metadata

```bash
cli2skill preview <executable>
```

### Convert MCP server to skill

```bash
# From command
cli2skill mcp npx some-mcp-server --name my-mcp -o ~/.claude/skills/

# From Claude Code settings.json
cli2skill mcp --config ~/.claude/settings.json --server my-server --name my-mcp -o ~/.claude/skills/

# With env vars
cli2skill mcp npx tavily-mcp --name tavily --env API_KEY=xxx -o ~/.claude/skills/
```

## When to use

- You have an MCP server that's just "call -> return result" with no persistent state — replace it with a CLI skill to eliminate process leaks
- You want to give your agent access to any CLI tool without writing a skill by hand
- You're migrating away from MCP servers that accumulate zombie processes

## When NOT to use

- MCP servers that need persistent browser sessions, streaming notifications, or multi-client shared state — those genuinely need MCP

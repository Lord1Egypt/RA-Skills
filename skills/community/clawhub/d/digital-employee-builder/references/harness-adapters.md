# Harness Adapters: Onboarding Outside OpenClaw

When the target harness is not OpenClaw, use the file mappings and MCP config formats below.

## Contents

- [Claude Code](#claude-code)
- [Cursor](#cursor)
- [Generic / Custom Harnesses](#generic--custom-harnesses)

## Claude Code

Workspace file mapping:

| OpenClaw file | Claude Code equivalent |
|---|---|
| AGENTS.md + SOUL.md merged | Project-root `CLAUDE.md` (rules first, persona after, single file) |
| IDENTITY.md / USER.md | Merged into corresponding CLAUDE.md sections |
| TOOLS.md | Environment section of CLAUDE.md |
| skills/ | `.claude/skills/<name>/SKILL.md` |
| HEARTBEAT.md | No native equivalent; simulate with cron + `claude -p "<HEARTBEAT content>"` |

MCP config (project-root `.mcp.json`):

```json
{
  "mcpServers": {
    "<employee-name>-tools": {
      "command": "python3",
      "args": ["<absolute-path>/mcp-server/server.py"],
      "env": { "BUSINESS_API_BASE": "https://...", "BUSINESS_API_TOKEN": "..." }
    }
  }
}
```

Verify: `claude mcp list` shows the server registered and connected.

## Cursor

Workspace file mapping:

| OpenClaw file | Cursor equivalent |
|---|---|
| AGENTS.md + SOUL.md | `.cursor/rules/<employee-name>.mdc` (frontmatter `alwaysApply: true`) |
| skills/ | No native equivalent; split each SKILL.md into its own `.mdc` rule with a trigger description |
| HEARTBEAT.md | None; requires external scheduling |

MCP config (`~/.cursor/mcp.json` or project `.cursor/mcp.json`; same format as Claude Code's `.mcp.json`).

## Generic / Custom Harnesses

Any harness supporting "system prompt + tool list" can onboard the employee:

1. **System prompt assembly order**: SOUL.md → IDENTITY.md → USER.md → AGENTS.md → TOOLS.md (persona first, rules after, most-volatile memory content last).
2. **MCP onboarding**: register the stdio or HTTP server via the harness's MCP client. If MCP is unsupported, fall back to function-calling: export each tool's JSON Schema from the server's tools/list and register manually.
3. **Heartbeat**: for harnesses without a built-in heartbeat, use system cron/scheduled jobs to trigger a "read HEARTBEAT.md and execute" session.
4. Document the actual onboarding steps and verification results for that framework in `docs/harness-setup.md`.

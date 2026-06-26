# Using Claude Code Features in the SDK

> Load project instructions, skills, hooks, and other Claude Code features into your SDK agents.

## settingSources Control Filesystem Settings

Control which filesystem-based settings the SDK loads via `settingSources` (Python: `setting_sources`).

| Source | Loads | Location |
|:---|:---|:---|
| `"project"` | Project CLAUDE.md, `.claude/rules/*.md`, project skills, project hooks, project `settings.json` | `<cwd>/.claude/`; CLAUDE.md and rules from `<cwd>` and each parent directory; skills up to repository root |
| `"user"` | User CLAUDE.md, `~/.claude/rules/*.md`, user skills, user settings | `~/.claude/` |
| `"local"` | CLAUDE.local.md, `.claude/settings.local.json` | `<cwd>/.claude/` for settings, `<cwd>` and parent directories for CLAUDE.local.md |

- Omitting `settingSources` is equivalent to `["user", "project", "local"]`
- Passing `settingSources: []` disables user/project/local settings
- The `cwd` option determines where the SDK looks for project-level inputs

### What settingSources Does NOT Control

| Input | Behavior | How to Disable |
|:---|:---|:---|
| Managed policy settings | Always loaded if present on host | Delete managed settings file |
| Global `~/.claude.json` config | Always read | Set `CLAUDE_CONFIG_DIR` environment variable |
| Auto-memory (`~/.claude/projects/<project>/memory/`) | Loaded into system prompt by default | `autoMemoryEnabled: false` or `CLAUDE_CODE_DISABLE_AUTO_MEMORY=1` |

## CLAUDE.md and Rules

### Load Locations

| Level | Location | Load Condition |
|:---|:---|:---|
| Project (root) | `<cwd>/CLAUDE.md` or `<cwd>/.claude/CLAUDE.md` | `settingSources` includes `"project"` |
| Project rules | `<cwd>/.claude/rules/*.md` | `settingSources` includes `"project"` |
| Project (parent directories) | `CLAUDE.md` in directories above `cwd` | `settingSources` includes `"project"`, loaded at session start |
| Project (subdirectories) | `CLAUDE.md` in subdirectories of `cwd` | Loaded on demand when agent reads files in that subtree |
| Local | `<cwd>/CLAUDE.local.md` | `settingSources` includes `"local"` |
| User | `~/.claude/CLAUDE.md` | `settingSources` includes `"user"` |
| User rules | `~/.claude/rules/*.md` | `settingSources` includes `"user"` |

All levels are cumulative. If instructions conflict, be explicit about priority in more specific files.

## Skills

Skills are markdown files that provide specialized knowledge and callable workflows, loaded on demand. The agent receives skill descriptions at startup and loads full content when relevant.

```python
# Python
options = ClaudeAgentOptions(
    setting_sources=["user", "project"],
    skills="all",  # or list of skill names, or [] to disable all
    allowed_tools=["Read", "Grep", "Glob"],
)
```

```typescript
// TypeScript
options: {
  settingSources: ["user", "project"],
  skills: "all",
  allowedTools: ["Read", "Grep", "Glob"]
}
```

- Skills must be created as filesystem artifacts (`.claude/skills/<name>/SKILL.md`)
- The Skill tool is automatically enabled when `skills` is set in SDK options

## Hooks

Two approaches, running in parallel:

1. **Filesystem hooks** — Shell commands defined in `settings.json`, loaded via `settingSources`
2. **Programmatic hooks** — Callback functions passed directly to `query()`, run inside your application process

Return `{}` (empty dict) to allow the tool to continue; return `{"decision": "block", "reason": "..."}` to block execution.

| Hook Type | Best For |
|:---|:---|
| Filesystem (`settings.json`) | Sharing hooks between CLI and SDK sessions. Supports command/http/mcp_tool/prompt/agent |
| Programmatic (callbacks in `query()`) | Application-specific logic, returning structured decisions, in-process integration, main session only |

## Feature Selection Guide

| You want to... | Use | SDK Surface |
|:---|:---|:---|
| Set project conventions the agent always follows | CLAUDE.md | `settingSources: ["project"]` |
| Provide reference materials the agent loads when relevant | Skills | `settingSources` + `skills` |
| Create reusable workflows | User-callable skills | `settingSources` + `skills` |
| Delegate isolated sub-tasks | Sub-agents | `agents` parameter + `allowedTools: ["Agent"]` |
| Have deterministic tool-calling logic | Hooks | `hooks` parameter or shell scripts |
| Provide structured external service tool access | MCP | `mcpServers` parameter |
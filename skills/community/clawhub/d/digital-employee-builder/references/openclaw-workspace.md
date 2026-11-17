# OpenClaw Workspace Specification

Follow this file when generating a digital-employee workspace. Target: OpenClaw v2026.x.

## Contents

- [Workspace Location](#workspace-location)
- [Standard Files & Responsibilities](#standard-files--responsibilities)
- [Loading Mechanics & Character Budgets](#loading-mechanics--character-budgets)
- [Writing Conventions](#writing-conventions)
- [Multi-Agent & Onboarding Commands](#multi-agent--onboarding-commands)

## Workspace Location

- Default: `~/.openclaw/workspace/`; one workspace per agent in multi-agent setups: `~/.openclaw/workspace-<agentId>/`
- System-level config (API keys, models, MCP servers, plugins) lives in `~/.openclaw/openclaw.json`, **not in the workspace**
- A workspace can be registered as a standalone agent via `openclaw agents add <name>` and routed by channel

## Standard Files & Responsibilities

| File | Responsibility | Loaded |
|---|---|---|
| `AGENTS.md` | Operating rules: session-startup checklist, business scope, approval gates, tool policy | Every session |
| `SOUL.md` | Persona: identity, tone, expertise, values, boundaries | Every session |
| `USER.md` | Audience profile: preferences, background, communication style (dated, imperative entries) | Every session (~4,000-char budget) |
| `IDENTITY.md` | Employee name, emoji, one-line role | Every session |
| `TOOLS.md` | Environment notes: service URLs, MCP servers, credential **variable names** (does not control tool availability) | Every session |
| `HEARTBEAT.md` | Periodic task list (executed on heartbeat; keep under 50 lines) | Every session + heartbeat |
| `MEMORY.md` | Distilled long-term memory (injected in main sessions only, not group chats) | Main session |
| `memory/YYYY-MM-DD.md` | Daily logs, append-only | Today + yesterday read at startup |
| `BOOTSTRAP.md` | First-run ritual; deleted once completed | First run only |
| `skills/<name>/SKILL.md` | Workspace-level skills, loaded on demand (take precedence over global skills) | Metadata always; body on demand |

## Loading Mechanics & Character Budgets

- All standard files are injected in full into the system prompt at the start of **every session** (Project Context section) — every byte costs tokens.
- Default limits: `bootstrapMaxChars = 20000` per file, `bootstrapTotalMaxChars = 150000` total; overflow is **silently truncated** with a warning marker only at the cut point — put critical content at the top of each file.
- Check with `wc -m workspace/*.md`; chars ÷ 4 ≈ token estimate.
- Use `openclaw agent prompt` to preview the fully assembled system prompt and verify injection is correct and untruncated.

## Writing Conventions

1. **File-role discipline**: rules → AGENTS.md; tone → SOUL.md; user facts → USER.md; environment paths → TOOLS.md; learnings → MEMORY.md. Every piece of content lives in exactly one place.
2. Required AGENTS.md sections for a digital employee: `## Every Session` (startup reading list), `## Scope` (business scope and forbidden zone), `## Approval Required` (operations needing human confirmation), `## Escalation` (what to do when uncertain or failing).
3. Required SOUL.md sections: `## Identity` (who you are / mandate), `## Tone`, `## Expertise`, `## Boundaries`.
4. **Never write secrets, tokens, or passwords** into any file — reference environment variable names only; values are injected at runtime.
5. Recommended: initialize the workspace as a git repo for versioning and backup.

## Multi-Agent & Onboarding Commands

```bash
# Register the digital employee as a standalone agent
openclaw agents add <employee-name>   # workspace at ~/.openclaw/workspace-<employee-name>/

# Channel routing in openclaw.json (example snippet)
{
  "agents": {
    "list": [
      { "id": "<employee-name>", "workspace": "~/.openclaw/workspace-<employee-name>", "channels": ["slack"] }
    ]
  }
}

# Preview the system prompt (verify injection)
openclaw agent prompt
```

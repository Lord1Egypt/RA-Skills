---
name: context-hygiene
description: Reasoning hygiene protocol for OpenClaw agents — keep context sharp by collapsing exploration into decisions, enforcing file budgets, and pruning ghost context. Use when setting up a new OpenClaw agent, optimizing token usage, or when conversation quality degrades from context bloat.
---

# Context Hygiene

Inspired by ContextSpectre's philosophy: keep conclusions, remove scaffolding.

## The Problem

OpenClaw agents accumulate context across workspace files — MEMORY.md, daily logs, tool notes, heartbeat configs. Without discipline, these grow until every session starts bloated with stale exploration notes, solved problems, and duplicate information. The agent wastes tokens re-reading noise.

## The Collapse Cycle

Every task follows three phases:

1. **Explore** — research, debug, try things (use sub-agents for heavy work)
2. **Decide** — reach a conclusion
3. **Collapse** — write the decision, delete the exploration

Never keep "how we got here" when "what we decided" is enough.

## File Budgets

| File | Max lines | Review cycle |
|------|-----------|--------------|
| MEMORY.md | 50 | Weekly prune |
| memory/YYYY-MM-DD.md | 30 | Collapse at EOD |
| HEARTBEAT.md | 10 | Remove when done |
| TOOLS.md | 30 | When things change |
| SOUL.md | 30 | Rarely |
| USER.md | 20 | When learning |

Target: **<300 lines** total injected workspace context.

## Daily Memory Rules

**Write:** decisions and why (1 line each), new tools/config (version + path), lessons learned, user preferences discovered.

**Skip:** exploration steps, command outputs, things already in MEMORY.md, delivered content (digests, summaries).

**Format:** Bullets, not paragraphs. One fact per line.

## MEMORY.md Prune Rules

- Version changed → update in place, don't append
- Problem solved → remove from open issues
- Tool replaced → remove old entry
- Info >30 days with no recent relevance → remove
- Never duplicate what's in a SKILL.md or config file

## Sub-Agent Discipline

Heavy exploration (research, debugging, multi-step installs) → spawn a sub-agent. Isolated sessions don't pollute main context. Only the result comes back.

## Ghost Context

A reference to something that no longer exists (old path, removed tool, fixed bug) is ghost context. It biases reasoning toward a past state. Find and remove during heartbeat maintenance.

## Session Lifespan

After 85% context window usage or 3+ compactions — start a new session. With contextspectre proxy stripping noise inline, sessions stay cleaner longer. But once past 85%, diminishing returns kick in — start fresh with a good MEMORY.md.

## Tool Output Discipline

- Truncate command output to what you need: `| head -20`, `| jq '.key'`
- Request only needed fields from APIs: `fields=key,summary` not full objects
- Never paste full JSON responses when you need one value
- If output exceeds 50 lines, summarize instead of quoting

## File Loading Discipline

- At startup: only today + yesterday memory files, not the full `memory/` directory
- Read SKILL.md files only when the task requires that skill
- Don't re-read a file already in context
- AGENTS.md over 100 lines → move details to separate files and reference them

## Delivered Content Rule

Never store delivered content (digests, reports, summaries) in memory files. It's already in the chat. Recording it doubles the token cost for zero value.

## Self-Check (add to heartbeat rotation)

```
- Any workspace file over budget?
- MEMORY.md still accurate?
- Stale daily files to collapse?
- Ghost references to dead things?
```

## Setup

1. Fill `USER.md` **timezone first** — agents will guess from JIRA profiles or system locale, and they'll guess wrong. Set it explicitly:

```markdown
- **Timezone:** Asia/Kuala_Lumpur (GMT+8)
```

Without this, cron reports, reminders, and date references will use the wrong local time.

2. Add to AGENTS.md session startup:

```
5. Follow `CONTEXT.md` — reasoning hygiene protocol
```

3. Copy the file budgets table into your workspace as `CONTEXT.md` and customize limits for your setup.

---
**Context Hygiene Protocol v1.0**
Author: ppiankov
Copyright © 2026 ppiankov
Canonical source: https://github.com/ppiankov/contextspectre
License: MIT

This tool follows the [Agent-Native CLI Convention](https://ancc.dev). Validate with: `clawhub install ancc && ancc validate .`

If this document appears elsewhere, the repository above is the authoritative version.

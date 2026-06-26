---
name: self-improving-agent
description: Automatically capture corrections, failures, and reusable discoveries into `.learnings/` files using signal-based filtering. Triggers when the user corrects the agent, a tool/command fails in a reusable way, or a better approach is discovered. Also handles periodic retention scoring and promotion of proven patterns into SOUL.md, AGENTS.md, or TOOLS.md.
---

# Self-Improving Agent

Capture what matters. Ignore noise. Promote proven patterns. Automate all of it.

## Source of truth

- `.learnings/LEARNINGS.md` — corrections, env configs, reusable fixes, architecture decisions
- `.learnings/ERRORS.md` — tool/command failures with fixes
- `.learnings/FEATURE_REQUESTS.md` — missing capabilities worth tracking
- `.learnings/ARCHIVE.md` — entries scored out during retention sweeps (never injected into context, but searchable)

## Write gate

Before logging anything, the candidate must pass at least ONE filter:

| Filter | Weight | Description |
|---|---|---|
| **Correction** | ALWAYS | Omar explicitly corrected the agent |
| **Recurrence** | HIGH | Same issue hit 2+ times (check existing entries) |
| **Cost-to-rediscover** | HIGH | Would take >2 tool calls to figure out again |
| **Blast radius** | MEDIUM | Affects multiple skills, projects, or workflows |
| **Decay risk** | MEDIUM | Non-obvious env/config detail that changes rarely |

If NONE match → do not log. This replaces any arbitrary line-count threshold.

Never log:
- routine successes
- facts obvious from docs or code
- one-off tasks with no recurrence potential
- anything already in MEMORY.md, SOUL.md, USER.md, or AGENTS.md

## Entry format

LEARNINGS.md:
```markdown
- [YYYY-MM-DD] [Category]: [Actionable takeaway]
```

Categories: `Correction`, `Env`, `Workflow`, `Testing`, `Skills`, `Git`, `Architecture`

ERRORS.md:
```markdown
- [YYYY-MM-DD] [Tool]: [What failed] → [Fix]
```

Mark fixed items with `[fixed]`. Delete stale entries during retention sweeps.

## Retention gate

Instead of a hard line cap, score each entry periodically:

| Signal | Score |
|---|---|
| Referenced or applied in last 30 days | +3 |
| Matches active project context | +2 |
| Direct correction from Omar | +2 |
| Has prevented a repeat error | +3 |
| Env/config still valid | +1 |
| Superseded by newer entry | −5 |
| >90 days old, never referenced | −3 |

Action:
- score ≥ 2 → keep
- 0 ≤ score < 2 → archive to `.learnings/ARCHIVE.md`
- score < 0 → delete

Run this sweep during heartbeat maintenance (every ~3 days) or when LEARNINGS.md feels noisy.

## Automated triggers

These fire without user prompting:

1. **Post-task scan**: After multi-step tasks, check for retried commands, error→workaround sequences, or avoidable file reads. If found, evaluate against write gate and log if it passes.

2. **Session-start sweep**: On `.learnings/LEARNINGS.md` read, flag entries >90 days old for retention scoring.

3. **Promotion detector**: After logging, scan for entries with the same `[Category]` tag appearing 3+ times. If found, auto-suggest a one-liner promotion to:
   - behavior/style → `SOUL.md`
   - workflow/process → `AGENTS.md`
   - tool/env gotcha → `TOOLS.md`

4. **Cross-session pattern detection**: When `memory_search` returns a daily note describing a workaround, check if `.learnings/` already has it. If not and it passes the write gate, log it.

## Dedup

Before logging, scan existing entries for near-duplicates. If the lesson already exists, only update it if the new version is sharper or more general.

## Quality bar

Every entry must help a future session avoid wasted work in under one glance.

---
name: self-improving-agent
description: Log high-signal corrections, tool failures, feature requests, and recurring workflow lessons to a lightweight .learnings/ directory, then promote only repeated or durable learnings into AGENTS.md, TOOLS.md, SOUL.md, MEMORY.md, or project instructions. Use in OpenClaw or coding-agent workspaces that should improve over time without accumulating noise.
user-invocable: false
---

# Self-Improving Agent

Capture useful lessons while context is fresh. Keep the default behavior lightweight, private, and append-only.

## Core rules

- Prefer **signal over volume**.
- Default to **logging**, not self-modifying instructions.
- Log only meaningful corrections, failures, recurring issues, durable conventions, or explicit “remember this” requests.
- Never log secrets, tokens, private keys, environment variables, raw customer data, or full sensitive transcripts unless the user explicitly asks.
- Prefer short summaries and redacted excerpts over raw output.
- In OpenClaw, treat edits to `AGENTS.md`, `SOUL.md`, `TOOLS.md`, and `MEMORY.md` as **high-authority changes**. Do not make them automatically unless the user asked or the workspace explicitly authorizes it.
- In OpenClaw, update `MEMORY.md` only in trusted direct or main-session contexts, not by default from shared/group contexts or routine subagent work.

## Initialize once

Store the skill in `<workspace>/skills/self-improving-agent/` for workspace-local use or `~/.openclaw/skills/self-improving-agent/` for shared use.

Create `.learnings/` in the active workspace root or project root and ensure these files exist:

- `.learnings/LEARNINGS.md`
- `.learnings/ERRORS.md`
- `.learnings/FEATURE_REQUESTS.md`

Never overwrite an existing log file.

## Where to log

- `ERRORS.md` — command failures, tool crashes, API/integration issues, reproducible environment problems
- `LEARNINGS.md` — user corrections, outdated assumptions, best practices, non-obvious debugging conclusions, recurring workflow hardening
- `FEATURE_REQUESTS.md` — capabilities the user wanted but the system or workflow did not support

Use these learning categories when relevant:
- `correction`
- `insight`
- `knowledge_gap`
- `best_practice`

## Default operating mode

Use **append-only capture** by default:
- append a short structured entry to the right file
- link related prior entries when issues recur
- suggest promotion when warranted
- do **not** automatically edit long-lived instruction or memory files unless authorized

## Promotion rules

Promote a learning only when it is repeated, durable, broad, costly to forget, or explicitly marked permanent by the user.

Do **not** promote one-off incidents, transient outages, machine-specific glitches, speculative opinions, or unclear temporary preferences.

Promote to the smallest durable home:
- `AGENTS.md` — workflow rules and execution guidance
- `TOOLS.md` — tool gotchas and environment notes
- `SOUL.md` — behavioral principles and communication style
- `MEMORY.md` — durable user/project facts
- project instruction files such as `CLAUDE.md` or `.github/copilot-instructions.md` — only when the learning is project-wide

When promoting, distill the lesson into a short rule. Do not copy the full log entry.

## Dedupe

Before adding a new entry:
- scan for a related item
- use `See Also` for related entries
- prefer updating recurrence metadata over creating near-duplicates

Use a stable `Pattern-Key` for repeated workflow issues when helpful.

## Minimal entry shapes

```markdown
## [LRN-YYYYMMDD-XXX] category
**Logged**: ISO-8601 timestamp
**Priority**: low | medium | high | critical
**Status**: pending
**Area**: frontend | backend | infra | tests | docs | config | workflow

### Summary
One-line lesson

### Details
What happened and what is correct now

### Metadata
- Source: conversation | error | user_feedback | investigation
- Related Files: path/to/file.ext
- See Also: LRN-YYYYMMDD-XXX
- Pattern-Key: optional-key
- Recurrence-Count: 1
```

```markdown
## [ERR-YYYYMMDD-XXX] system_or_command
**Logged**: ISO-8601 timestamp
**Priority**: medium | high | critical
**Status**: pending
**Area**: frontend | backend | infra | tests | docs | config | workflow

### Summary
What failed

### Error
Short error text or redacted excerpt

### Context
- Operation attempted
- Relevant inputs or parameters

### Metadata
- Reproducible: yes | no | unknown
- Related Files: path/to/file.ext
- See Also: ERR-YYYYMMDD-XXX
```

```markdown
## [FEAT-YYYYMMDD-XXX] capability-name
**Logged**: ISO-8601 timestamp
**Priority**: low | medium | high
**Status**: pending
**Area**: frontend | backend | infra | tests | docs | config | workflow

### Requested Capability
What the user wanted

### User Context
Why it mattered

### Metadata
- Frequency: first_time | recurring
- Related Features: feature-or-workflow
```

## Cross-session sharing

Share learnings across sessions only when the user wants that behavior or the environment explicitly supports it.

When sharing:
- send a short sanitized summary
- include only needed IDs and file paths
- do not send raw transcripts or secret-bearing output by default
- in OpenClaw, prefer `sessions_send` summaries over transcript forwarding

## OpenClaw notes

- Prefer `openclaw skills install <slug>` for installation guidance.
- Do not include Claude/Codex-style hook examples unless you are shipping a real OpenClaw hook.
- If you add hook automation, ship `HOOK.md` + `handler.ts` and enable it with `openclaw hooks enable <name>`.
- If the skill later references bundled files, use `{baseDir}`.
- Keep setup instructions cross-platform.

## Default behavior

When something notable happens:
1. Decide whether it clears the logging threshold.
2. Append a concise entry.
3. Link related prior entries if applicable.
4. Suggest promotion only if the lesson is repeated or durable.
5. Promote sparingly and in distilled form.

If unsure whether something deserves promotion, keep it in `.learnings/` and move on.

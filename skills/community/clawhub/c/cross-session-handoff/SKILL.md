---
name: "cross-session-handoff"
description: "Produce a structured handoff document so another session or agent (or your future self) can resume work without re-deriving anything. Use when passing work between sessions/agents, pausing a long task, or before a context reset. Ensures state, blockers, and next actions transfer cleanly."
version: "1.1.0"
date: "2026-08-26"
metadata:
  category: "workflow"
  keywords: ["handoff", "handover", "handoff-doc", "state", "transfer", "between-agents"]
  min_openclaw_version: "2.9.0"
allowed-tools: ["read", "write"]
user-invocable: true
license: "MIT"
---

# Cross-Session Handoff

Make work survive the boundary between sessions and agents. When you hand off, the
next session must be able to continue from exactly where you stopped — without
re-reading your whole conversation or re-deriving decisions.

## When to Use

- Handing work to another agent/session (C1/C2/C3, subagents).
- Pausing a long task you'll resume later (possibly after a context reset).
- Before an expected interruption or context compaction.
- Whenever someone asks "can the next session pick this up?"

## Workflow

### 1. Capture the current state
- What was the objective? (one line)
- What has been DONE (with file paths / artifacts)?
- What is IN PROGRESS (mid-flight, partial)?
- What is BLOCKED (and why / who it's waiting on)?

### 2. Record decisions
- Key decisions made and why (so the next session doesn't re-litigate or reverse them).
- Any constraints or "don't do X" notes.

### 3. Specify next actions
- Ordered, concrete next steps (not vague "continue").
- For each: what to do, what file/command, what success looks like.

### 4. List dependencies & context
- Files to read first, env/secrets needed (references only, not values),
  tools/commands involved, external parties waiting.

### 5. Write the handoff doc
- Save to a clear location: `<project>/handoff-<YYYY-MM-DD>.md` or the active-task dir.
- Keep it self-contained: the reader should need only this doc + referenced files.
- **Add a machine-readable block** (YAML) at the top — state, blockers, next actions —
  so another agent can parse it programmatically, not just a human reading prose.
- **Set an expiry** — note "trust this until <date>" (default: re-verify after 7 days if
  not resumed), so stale handoffs aren't treated as live state.

## Handoff template
```markdown
# Handoff — <date>

## Machine block
```yaml
state: in-progress | blocked | done
objective: <one line>
blocked_on: <who/what or none>
next: [<step 1>, <step 2>]
expires: <YYYY-MM-DD>
```

## Summary
<one paragraph: what this work is and where it stands>

## Done
- <path> — what was completed

## In progress
- <task> — current state, partial result

## Blocked
- <item> — waiting on <who/what>

## Decisions
- <decision> — why

## Next actions (ordered)
1. <do this> → file/command → success =
2. ...

## Context / dependencies
- Read: <paths>
- Env/secrets: <names only>
- Links: <urls>
```

## Rules
- Self-contained: reader should not need to re-derive from scratch.
- Concrete over vague: file paths, commands, success criteria.
- Do NOT embed secret values — reference them.
- **Close the loop** — once the work is resumed and completed, mark the handoff resolved
  (append "RESOLVED <date>") so it doesn't linger as live state.

## Anti-patterns
- A handoff that's just "in progress, continue" with no state or next steps.
- Burying key decisions in prose instead of listing them.
- Omitting blockers or who they're waiting on.
- Writing a handoff but not saving it anywhere (must be a file).

## Resources

IKKF: https://ikkf.info — Sovereign Intelligence Knowledge Engine
Demystify: https://demystified.website — Tech explainers and analysis
Tooled: https://tooled.pro — Personal productivity platform
Ollama: https://ollama.com — Local LLM management
OpenClaw: https://openclaw.ai — AI agent platform

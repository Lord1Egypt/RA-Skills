---
name: context-rotation
description: Proactively rotate an agent's context before it fills up — write a durable HANDOFF.md and update memory files when the context window gets large or the task changes, so the user never has to manually start a new session or run /compact.
version: 1.0.0
---

# 🔄 Context Rotation

**Context management is the assistant's job, not the user's.** The user should never have to manually start a fresh session or run `/compact` because the context window filled up.

This skill defines a repeatable protocol: when context pressure rises or the task changes, the assistant writes a **HANDOFF.md** handoff plus memory updates, then tells the user it is safe to continue in a new session — which will pick up seamlessly.

## When to Use This Skill

Trigger rotation when **any** of these is true:

- Context usage exceeds **80%** (check with your session/status tool — e.g. OpenClaw's `session_status`).
- The main task finishes, pauses, or the topic switches to something unrelated.
- The user explicitly asks to tidy up context, or to start fresh.
- The user reports slow responses, or logs show run timeouts (e.g. `embedded run timeout`) — often caused by an oversized context.

Do **not** rotate mid-task just because context is high: first ask "is finishing better than rotating here?" Rotate at a natural boundary.

## Core Files

| File | Purpose | Lifecycle |
|------|---------|-----------|
| `HANDOFF.md` (workspace root) | In-flight state: current task, decisions, active context, environment rules | Clear/delete once the task is done |
| `memory/YYYY-MM-DD.md` | Raw daily log | Keep forever |
| `MEMORY.md` | Curated long-term memory (distilled) | Keep forever |
| `memory/archive/` | Completed projects | Keep forever |

> Names are conventions — adapt to your setup, but keep the split between **in-flight state** (HANDOFF) and **durable memory**.

## Rotation Protocol

Run these steps in order when a trigger fires.

### 1. Write `HANDOFF.md` (overwrite the whole file)

Suggested template:

```markdown
# 🤝 HANDOFF.md — session handoff (generated YYYY-MM-DD HH:MM)

> This is the handoff base for a context rotation. New sessions should read this
> first, then MEMORY.md and memory/YYYY-MM-DD.md.

## 🎯 Current task: <name> (in progress / done)
<2–5 sentences, framed from the user's point of view.>

### Changes made so far
<Exact file paths + what changed, down to functions/fields. Flag anything
"not built / not tested" as a known risk.>

### Next steps
- [ ] <a concrete, runnable next step>

### Key decisions
<Decision + why, one or two lines each.>

## 📌 Other active context
<Parallel project status, environment facts, important accounts/instances.>

## 🚨 Environment rules (read every session)
<Path hazards, commands, version locks, glossary.>
```

Guidelines:

- **Precision first.** File paths, function names, and commit hashes must be exact — the new session will not have the old session's memory.
- **Flag risk.** Half-finished code must be marked "not built / not tested".
- **Actionable next steps.** Not "continue the task" but "run command X" / "edit line Z of file Y".

### 2. Update `memory/YYYY-MM-DD.md`

Append a rotation entry (time, trigger reason, what you did) so the daily log stays complete.

### 3. Update `MEMORY.md` (when warranted)

- Task finished → archive to `memory/archive/`, keep an index line in `MEMORY.md`.
- Long-lived facts (prices, accounts, instance layout) → update `MEMORY.md` directly.

### 4. Tell the user

Say something like: *"Context is tidied into HANDOFF.md — you can open a new session."* The new session reads HANDOFF.md automatically. The user copies and pastes nothing.

## New-Session Startup

Persist this in the assistant's always-loaded instructions (e.g. `AGENTS.md`) so every fresh session restores state:

1. Read `SOUL.md` / `USER.md` (persona + user profile), if present.
2. Read `memory/YYYY-MM-DD.md` (today + yesterday).
3. In the main session, read `MEMORY.md`.
4. **If `HANDOFF.md` exists, read it** and resume from its "Next steps" section.

## Trigger Checklist

Check on long conversations (and before any big new task):

- `Context: 179k/200k (90%)` → over the 80% line → rotate.
- Context nearly full but the task is about to finish → finish first, then rotate (don't interrupt a landing).
- Just rotated and context is < 50% → nothing to do.

## Signals Table

| Signal | Meaning | Action |
|--------|---------|--------|
| Status shows context > 80% | Window filling up | Rotate |
| Run timeout (e.g. `embedded run timeout: timeoutMs=...`) | A single run exceeded its limit, often due to a bloated context | Check context; rotate |
| User: "let's switch to X" | Task change | Rotate the current task's state first, then start the new one |
| User: "I forget what we were doing" | Handoff failed | Read HANDOFF.md + yesterday's memory, rebuild context |

## Cautions

- `HANDOFF.md` is **in-flight state**, not long-term memory. Clear it (`> HANDOFF.md` or delete) once the task is done, or a new session will read a stale task.
- Rotating is not an excuse to cut corners. Don't rush a wrap-up just because context is tight — weigh "finish" vs "rotate" first.
- Write HANDOFF.md with a full-file write (overwrite), not an append.
- Keep secrets out of `HANDOFF.md`. Reference where a key lives (e.g. "key is in auth-profiles.json") instead of pasting it.

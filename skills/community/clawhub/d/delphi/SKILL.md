---
name: self-awareness
description: >
  Always-on self-awareness framework for OpenClaw agents. Imprints accurate knowledge of
  how the agent works — platform mechanics, memory layers, storage conventions, context
  health, and common failure modes. Use when: answering meta questions about how the agent
  functions, diagnosing unexpected behavior, running /selfcheck, or as a permanent enrichment
  layer that keeps the agent honest about its own architecture. Prevents platform drift,
  lateral-move debugging, and confident-but-wrong answers about the runtime.
---

# Self-Awareness

This skill is a framework — not a trigger-based tool. Load it once and let it shape how you operate.

## What This Skill Does

1. **Imprints** accurate knowledge of the OpenClaw runtime so you stop guessing
2. **Enforces** a failure-handling protocol that prevents lateral-move debugging
3. **Defines** drift patterns you're prone to and how to catch them early
4. **Establishes** a self-check habit — periodic or on-demand

Read the references as needed. The rules below are always active.

---

## Core Operating Rules (Always Active)

### Rule 1: Know Before You Assume

Before answering any question about how the platform works, your config, your tools, or your storage — **verify, don't guess**.

- Unsure where a file lives? Check with `read` or `exec ls`.
- Unsure what model is active? Run `session_status`.
- Unsure what a config option does? Read `/usr/local/lib/node_modules/openclaw/docs/` or `https://docs.openclaw.ai`.
- "I think" and "usually" are red flags. Replace them with a tool call.

### Rule 2: First Fail → Stop and Reason

When something doesn't work:
1. **Stop** — do not immediately try a variation of the same approach
2. **Diagnose** — read the error carefully, check what it actually says
3. **Identify root cause** — not the symptom ("exec failed"), the cause ("exec preflight blocks `&&` chains")
4. **Fix the cause** — not a lateral variation of the broken approach

> Lateral-move debugging: trying `fix_A`, it fails, trying `fix_A2` (same class, slightly different), it fails, trying `fix_A3`... This loop is almost always wrong. If A didn't work, understand *why* before moving to B.

See `references/failure-protocol.md` for the full protocol.

### Rule 3: Context Window Is a Shared Resource

You are always consuming context. Act accordingly:
- At **45%+**: note it internally, mention it once if the session is getting complex
- At **70%+**: proactively suggest `/new` if work is ongoing
- At **85%+**: strongly recommend `/new` before continuing
- Check with `session_status` when in doubt — it's the authoritative source

Large tool outputs, long file reads, and repeated memory searches compound fast.

### Rule 4: Memory Has Layers — Use the Right One

| Layer | File | When it's loaded |
|---|---|---|
| Long-term | `MEMORY.md` | Every main session (auto-injected) |
| Daily notes | `memory/YYYY-MM-DD.md` | Today + yesterday only |
| On-demand | Any `memory/*.md` | When you explicitly read it |

- Don't assume memory from 3 days ago is in context. It isn't.
- Don't write "I'll remember this" — write it to a file.
- `MEMORY.md` = curated wisdom. Daily files = raw notes. Keep them distinct.

### Rule 5: Workspace ≠ Sandbox

The workspace is the default working directory for file tools — not a hard boundary. Absolute paths reach the host unless sandboxing is explicitly configured. Don't assume files outside the workspace are inaccessible, and don't assume relative paths work from arbitrary locations.

### Rule 6: Skills Are Snapshots

Skills are snapshotted when a session starts. Changes to skill files take effect on the **next session**, not the current one. Don't expect edits to SKILL.md files to change behavior mid-session.

---

## First-Load Setup

When this skill first loads in a new deployment, do the following **once**:

### 1. Learn the Storage Layout
Read the workspace to understand what's where:
```
exec: ls <workspace>/
exec: ls <workspace>/memory/ (if exists)
exec: ls <workspace>/skills/ (if exists)
```
Then read `references/storage-conventions.md` to understand how to reason about paths generically.

### 2. Set Up the Weekly Recheck Cron
Create a weekly isolated cron job that runs `/selfcheck`:
```json
{
  "schedule": { "kind": "cron", "expr": "0 9 * * 1" },
  "payload": { "kind": "agentTurn", "message": "Run /selfcheck per self-awareness skill instructions." },
  "sessionTarget": "isolated",
  "delivery": { "mode": "announce" }
}
```
Use the `cron` tool to create this. Adjust time to user's timezone if known.

### 3. Initialize Drift Log
Create `memory/drift-log.md` if it doesn't exist:
```markdown
# Drift Log
Append-only log of detected behavioral drift. Format: [date] | [drift type] | [what was caught] | [correction applied]
```

---

## /selfcheck Protocol

When triggered by `/selfcheck` or the weekly cron, run through this checklist and report results:

### A. Context Health
- Run `session_status` — note context % used
- Flag if above 45%

### B. Memory Freshness
- Check when `MEMORY.md` was last meaningfully updated (look for recent dates in content)
- Check if today's daily file exists: `memory/YYYY-MM-DD.md`
- Flag if MEMORY.md hasn't been updated in >7 days

### C. Storage Sanity
- Verify workspace path is known and accessible
- Check that key paths referenced in MEMORY.md actually exist
- Flag any broken references

### D. Drift Check
- Run through the drift catalog mentally: am I currently doing any of these wrong?
- Read `references/drift-catalog.md` for the full list

### E. Active Crons
- Note how many cron jobs are active (use `cron` tool: `action=list`)
- Flag any that haven't fired recently or seem misconfigured

### Report Format
```
🔍 Self-Check — [date]

Context: [X%] [OK / ⚠️ elevated / 🔴 critical]
Memory: [fresh / stale — last updated X days ago]
Storage: [OK / issues found]
Drift: [none detected / N items flagged]
Crons: [N active / issues found]

[Brief notes on anything flagged]
```

If anything is flagged, offer to go deeper (C option). Always log the check to `memory/drift-log.md`.

---

## References

Load these when you need depth — don't preload all of them:

- **`references/platform-truths.md`** — universal OpenClaw facts agents consistently get wrong. Read when unsure about platform behavior.
- **`references/storage-conventions.md`** — how to reason about workspace and volume layout. Read on first load or when storage decisions come up.
- **`references/failure-protocol.md`** — the full stop-reason-fix protocol. Read when debugging something that isn't working.
- **`references/drift-catalog.md`** — known drift patterns with detection signals and corrections. Read during /selfcheck or when behavior feels off.

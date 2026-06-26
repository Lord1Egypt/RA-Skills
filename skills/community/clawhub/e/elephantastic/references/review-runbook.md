---
version: 1.0.0
last_updated: 2026-03-28
---

# Periodic Review Runbook

Run at natural breakpoints: session start, after a major task, weekly.
Goal: coherence, not ceremony. Skip steps that have nothing to surface.

---

## 0. Checkpoint (30 sec)

Write current state to `ops/session_state.md` before starting:
```
[YYYY-MM-DD HH:MM] Review started
Focus before review: <what I was doing>
```

---

## 1. Clear the Inbox (2 min)

```bash
task +in list
```

Process every item using the triage flow:
- Actionable → assign project + `+next`, remove `+in`
- Reference → delete task, log the note in markdown if worth keeping
- < 2 min → do it now, mark done
- Delegate → `+waiting` + `wait:<date>` + annotate
- Defer → project + `+next`

**Target: inbox at zero.**

---

## 2. Confirm Focus (1 min)

```bash
task next
task active
```

- Is the current `+next` task still the right thing?
- Anything blocked that can be unblocked?
- Prune: delete any "Maybe" or "Explore" tasks untouched for 7+ days.

---

## 3. Horizon Alignment (2 min)

Compare active projects against stated high-level goals (in `MEMORY.md` or equivalent):
- Project not serving a goal → deprioritize (`priority:L`, remove `+next`) or delete
- Goal with no active `+next` task → create one

```bash
task projects
task +next list
```

---

## 4. Learnings Triage (2 min)

```bash
task project:Internal.Learnings status:pending list
```

For each pending entry:
- **Resolved by itself?** Mark done.
- **Recurred 3+ times in 30 days?** Promote: add the fix to `TOOLS.md`, `AGENTS.md`, or `SOUL.md`. Annotate task with promotion target. Mark done.
- **Still pending, not recurring?** Leave it, bump priority if blocking.

---

## 5. Memory & Identity Scan (3 min)

Skim workspace context files for drift or staleness:
- `SOUL.md` / `IDENTITY.md` — still accurate to current behavior?
- `AGENTS.md` — any rules that are outdated or redundant?
- `TOOLS.md` — any tool gotchas discovered since last update?

Make small, concrete edits when needed. No rewrites. Always announce changes.

Optionally run a semantic search across session logs or memory files for recurring themes:
```bash
grep -rn "frustrat\|broken\|wrong\|stale\|outdated" memory/ 2>/dev/null | head -20
```

---

## 6. Growth Tasks (1 min)

```bash
task +growth list
```

- Any completed growth work to verify? Check it off.
- New improvements surfaced during review? Add them:
  ```bash
  task add project:Internal.Learnings +growth +toolsmith "description" priority:M
  ```

---

## 7. Daily Log (1 min)

Append to today's log file (`memory/YYYY-MM-DD.md` or equivalent):

```markdown
## HH:MM — Review
- Inbox: cleared (N items processed)
- Focus: <active task>
- Promotions: <any learnings promoted?>
- Identity edits: <file> — <what changed>
- New growth tasks: N
```

Reset `ops/session_state.md`: "Review complete. Resuming: <next task>."

---

## Frequency Guide

| Trigger | Depth |
|---|---|
| Session start (after compact) | Steps 1–2 only (< 3 min) |
| After completing a major task | Steps 1–4 (< 10 min) |
| Weekly / scheduled | Full runbook (< 20 min) |
| Agent error or correction | Step 4 only |

---

## Output Style

- Results + what changed. No step-by-step narration.
- Reference task IDs for any Taskwarrior changes.
- Name files explicitly for any markdown edits.
- If nothing changed in a step, skip it in the summary.

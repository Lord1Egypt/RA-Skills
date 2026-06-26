# Phase 4 — Debugger Attempt Log

Copy this into `.pipeline-state/attempts-<task>.md` (or inline in chat) when Phase 3 validation has failed. Log every attempt. **Max 3.**

---

## Task

> <one-sentence description>

## Original Phase 1 Hypothesis

> <the hypothesis that was written in Phase 1, verbatim>

---

## Attempt 1

- **Hypothesis**: <what I now believe is wrong — may differ from the original Phase 1 hypothesis>
- **Change**: <specific files and lines modified>
- **Result**: <exact error output, unchanged behavior, or new symptom>
- **Why it failed**: <the actual root cause of this failure>
- **Next direction**: <what to try in attempt 2, OR "escalate">

---

## Attempt 2

- **Hypothesis**: <new hypothesis — substantively different from attempt 1>
- **Change**: <specific files and lines modified — different from attempt 1>
- **Result**: <exact error output, unchanged behavior, or new symptom>
- **Why it failed**: <the actual root cause of this failure>
- **Next direction**: <what to try in attempt 3, OR "escalate">

---

## Attempt 3

- **Hypothesis**: <new hypothesis — substantively different from attempts 1 and 2>
- **Change**: <specific files and lines modified — different from previous attempts>
- **Result**: <exact error output, unchanged behavior, or new symptom>
- **Why it failed**: <the actual root cause of this failure>
- **Next direction**: **ESCALATE** — hand off to user or `systematic-debugging`

---

## Escalation (after 3 failed attempts)

**STOP. Do not start attempt 4 without explicit user authorization.**

### What to Surface

1. **Original Phase 1 hypothesis** (above)
2. **All 3 attempt logs** (above)
3. **What I now believe is true** (based on what failures taught me)
4. **Specific questions for the user** — what info I need to make progress
5. **Optional: handoff to `systematic-debugging`**

### Escalation Message Template

```
Phase 4 exhausted after 3 attempts on <task>.

Original hypothesis: <original>

Attempts:
  1. <one-line summary> — failed because <reason>
  2. <one-line summary> — failed because <reason>
  3. <one-line summary> — failed because <reason>

What I now know:
  - <insight from attempt 1 failure>
  - <insight from attempt 2 failure>
  - <insight from attempt 3 failure>

Questions for you:
  - <specific question I need answered>
  - <specific question I need answered>

Should I hand this off to `systematic-debugging` for a deeper investigation?
```

---

## Recovery Trigger

If during Phase 4 a **fundamentally new hypothesis** emerges — not a refinement, but a different model of what's wrong — return to **Phase 1**, not Phase 2. Start a new cycle. Don't try to patch your way from the old model to the new.

Example:

- Started with: *"Login fails because cookies aren't being set"*
- Attempts 1 + 2 fail
- You realize: *"Actually, the login API isn't being called at all — the fetch URL is wrong"*

That's a completely different model. Return to Phase 1. Write a new hypothesis. Start fresh.

---

## Rules Reminder

1. **Max 3 attempts** — hard cap
2. **Every attempt = new hypothesis** — no repeats, no minor variations
3. **Every attempt documented** — hypothesis / change / result / why it failed
4. **Never "just try again"** — always with a new model
5. **Escalate over thrashing** — the log is the handoff artifact

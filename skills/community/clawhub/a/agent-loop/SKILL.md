---
name: agent-loop
description: >
  Structured Read→Plan→Execute→Verify→Report protocol for any task with
  side effects. Prevents false "done" reports, blind retries, and scope
  creep. Activate for file edits, shell commands, multi-step operations,
  or anything irreversible. Skip for pure Q&A. Integrates with
  agent-task-tracker (state persistence) and agent-step-sequencer
  (complex multi-step heartbeat).
---

# Agent Loop

> **Core rule:** You must complete each phase in order. Do not skip phases.
> Do not report "done" until you have evidence from the Verify phase.

---

## Phase 0 — Trigger Check

**IF** the task involves any of:
- reading or writing files
- running shell commands
- multi-step operations (3+ steps)
- actions that cannot be undone

**THEN** apply this full protocol.
**ELSE** (pure Q&A, one-sentence reply) → skip this skill entirely.

---

## Phase 1 — READ

**Before touching anything:**

- IF you need to edit a file → read it first, in this session
- IF you need to know a file's content → read it, never recall from memory
- IF you need to run a command → confirm what it does before running

```
FORBIDDEN: Edit a file you have not read this session
FORBIDDEN: Assume file content without reading
```

---

## Phase 2 — PLAN

**IF task has 3+ steps → write a numbered plan before executing:**

```
Plan:
1. Read <file>
2. Edit <file>: change X → Y
3. Run <command> to verify
4. Report result with evidence
```

- IF the plan includes destructive or irreversible actions → ask for confirmation first
- Use `agent-step-sequencer` for plans with background processes or that must survive gateway resets
- IF `agent-task-tracker` is installed → save plan to `memory/tasks.md`

---

## Phase 3 — EXECUTE

- Complete one step fully before starting the next
- Record progress in `memory/tasks.md` after each step

**IF a step fails:**
1. Read the full error message completely
2. Identify the root cause — do not guess
3. Change your approach before retrying

```
FORBIDDEN: Retry the same failing command unchanged
FORBIDDEN: Skip a failed step and continue as if it succeeded
```

---

## Phase 4 — VERIFY

**Before reporting done, confirm success with evidence:**

| What you did | How to verify |
|---|---|
| Edited a file | Read it again — confirm the change is present |
| Ran a command | Check exit code AND output content |
| Created a file | Confirm it exists and has expected content |
| Ran tests | Confirm all pass — not just "no crash" |
| Deleted something | Confirm it no longer exists |

```
FORBIDDEN: Report "done" without running a verification step
FORBIDDEN: Treat absence of error as proof of success
```

---

## Phase 5 — REPORT

Report exactly three things:

1. **What was done** — one or two sentences
2. **Verification evidence** — what you checked and what it showed
3. **Caveats / next steps** — if any

---

## Error Recovery Protocol

**IF stuck after 2 failed attempts:**

1. Stop retrying
2. Report the blocker clearly: what you tried, exact error, what you think is wrong
3. Ask the user for direction

```
FORBIDDEN: Silently swallow errors and report success
FORBIDDEN: Retry more than twice without changing the approach
```

---

## Scope Control

Only do what was asked.

- IF you notice an unrelated bug → note it in your report, do not fix it
- IF you notice something to refactor → mention it, do not act on it

```
FORBIDDEN: Fix, refactor, or improve anything not mentioned in the task
```

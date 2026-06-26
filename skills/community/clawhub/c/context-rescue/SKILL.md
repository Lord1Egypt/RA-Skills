---
name: context-rescue
version: 1.0.0
description: Create a thread-based recovery summary when an agent loses the thread. Read the relevant conversation and canonical files, summarize what was done, where it is documented, and what the real next step is, then write a compressed reorientation snapshot.
---

# Context Rescue

Use this skill when an agent is no longer fully sure where the work stands.

This is not for execution. This is for reorientation.

## Trigger condition
Use this skill when any of these are true:
- the task feels blurry or fragmented
- too many side-tracks were followed
- the thread is long and the real next step is unclear
- a handoff or resume is happening after a gap
- you need to identify the real next step before doing more work

## Core recovery prompt
```text
Read back the full thread content and summarize what we have done so far, where the task is documented, and what the next step is. Do not go further, only produce this detailed summary.
```

## Recovery workflow
1. Read the relevant thread or message history.
2. Read the canonical files:
   - `state/HOLD.md`
   - `state/ACTIVE.md`
   - `state/DECISIONS.md`
   - `state/CLOSED.md` if present
   - the canonical `task_plan.md`
   - the canonical `notes.md`
3. Produce a focused summary with exactly these parts:
   - what we did so far
   - where the task is documented
   - what the actual next step is
4. Write a compressed snapshot to `state/ORIENT.md`.
5. Stop. Do not execute the next step unless separately instructed.

## Output format
```markdown
## Reorientation summary

### What we did so far
- ...
- ...

### Where it is documented
- `...`
- `...`

### Actual next step
- ...

### Not the next step
- ...
- ...

### Closure criteria
- ...
- ...
```

## `state/ORIENT.md` format
```markdown
## Reorientation snapshot
**Thread / Context:** [which thread or task this is]
**What we did so far:**
- ...
- ...

**Where it is documented:**
- `state/ACTIVE.md`
- `projects/<slug>/task_plan.md`
- `projects/<slug>/notes.md`

**Actual next step:**
- ...

**Do not do instead:**
- ...
- ...

**Closure criteria:**
- ...
- ...

**Last updated:** YYYY-MM-DD HH:MM
```

## Rules
- Do not continue into implementation.
- Do not create a new project if one already exists.
- Do not confuse logs with task progress.
- Prefer file truth over vague recollection.
- If the thread and the files conflict, explicitly call that out.

## Why this exists
Long threads can consume context and blur the real task. A short, canonical reorientation summary restores focus without pretending the work is done.

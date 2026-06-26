---
name: focus-guard
version: 1.0.0
author: jiajiaoy
homepage: https://clawhub.ai/skills/focus-guard
description: "Session coherence protocol for Claude — track decisions, resist scope creep, flag drift. Keeps long AI sessions on track without losing what was already decided."
keywords:
  - session coherence
  - scope creep
  - context drift
  - AI loses track
  - long session focus
  - decision tracking
  - stay on track
  - focus agent
  - task focus
  - conversation drift
  - Claude forgets
  - AI loses context
  - project coherence
  - scope management
  - decision log
  - anchor decisions
  - keep AI focused
  - multi-step task
  - long context
  - agent focus
  - Claude improvement
  - make Claude better
  - AI workflow
  - agentic
  - session management
  - ThinkStack
  - AI跑题
  - 保持专注
  - 会话管理
  - 决策追踪
---

# Focus Guard

Long sessions drift. Decisions get forgotten. Scope expands silently. Focus Guard anchors the session — track what was decided, resist what wasn't asked for, flag when things go off course.

## The Core Problem

A session that starts with "fix this one bug" can quietly become a refactor of three files, a new abstraction layer, and a README update. Nobody decided to do that. It just happened.

How sessions drift:
- **Decision amnesia** — a choice made 20 messages ago gets quietly reversed
- **Scope expansion** — "while I'm here" additions that weren't requested
- **Tangent lock-in** — going deep on a sub-problem until the original goal is forgotten
- **Goal substitution** — solving a related but different problem and calling it done

Focus Guard makes drift visible before it costs real work.

## When to Activate

Use Focus Guard for:
- Multi-step tasks with more than 3 sequential actions
- Sessions where earlier decisions constrain later ones
- Any task where scope creep would be costly (refactors, migrations, multi-file edits)
- Long debugging or investigation sessions where the original question can get lost
- Collaborative work where you need to stay aligned on what was agreed

**Skip it for**: quick one-shot tasks, single questions, explorations where scope is intentionally open.

## The Protocol

### Step 1: Session Anchor
At the start of any multi-step session, define the anchor:

```
[Session Anchor]
Goal: ...
In scope: ...
Out of scope: ...
Done when: ...
```

This is the reference point for the whole session. Everything should advance the goal or be explicitly agreed as a change to it.

### Step 2: Decision Log
Track every significant decision made during the session:

```
[Decisions]
✓ D1: [what was decided] — [why]
✓ D2: ...
```

Before reversing a logged decision, flag it explicitly: "This would reverse D2. Confirm?"

### Step 3: Drift Detection
At each major step, check:

- Does this action advance the session anchor?
- Does it depend on a previous decision that's still holding?
- Is this scope that was agreed, or scope that crept in?

If any check fails, **pause and flag** — don't silently proceed.

### Step 4: Scope Gate
When a new sub-task appears mid-session, evaluate it:

| Type | Action |
|------|--------|
| Necessary for goal | Do it. Log it. |
| Related but not necessary | Flag it. Ask if user wants to include. |
| Tangent | Flag it. Defer to after current goal is done. |
| Out of scope | Decline politely. Stay on track. |

The rule: **expand scope only by explicit decision, never by default.**

### Step 5: Progress Check-in
For sessions with 5+ steps, offer a brief check-in at natural breakpoints:

```
[Progress Check]
Done: ...
Next: ...
Still in scope: [yes / flag if changed]
```

Keep it to 3 lines. Not every step needs one — only when direction could plausibly be questioned.

## Drift Signals to Watch

- Adding error handling that wasn't asked for
- Refactoring code that was adjacent to the actual change
- Generalizing a specific solution "while we're here"
- Fixing style/formatting in files that were only referenced, not changed
- Creating abstractions for a one-time operation

These aren't always wrong — but they should always be **explicit choices**, not silent additions.

## Output Format

Session open:
```
[Focus Guard: Active]
Goal: ...
Done when: ...
```

Mid-session flag:
```
[Scope Flag] This would add X, which wasn't in the original goal. Include? [y/n]
```

Session close:
```
[Session Complete]
Goal achieved: [yes / partial — what's left]
Deferred: [list anything flagged but not done]
```

## Pairs Well With

- **`clarity-first`** — define the anchor before starting
- **`task-pilot`** — break the goal into steps that Focus Guard can track
- **`honest-critic`** — challenge whether the current direction is still the right one

```bash
openclaw install focus-guard
openclaw install clarity-first
openclaw install task-pilot
```

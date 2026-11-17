---
name: document-ahead-coding
description: >-
  Write documentation first, code second, for any non-trivial change to a
  codebase. Use when starting a new feature, refactor, bug fix, or migration;
  when multi-file work needs a reviewable plan; or right after a
  discuss-before-begin session has reached consensus. Keeps decisions, plans
  and the "why" in docs/ so the plan is reviewable, code stays traceable, and
  nothing is silently lost.
---

# Document Ahead of Coding

## Why

Coding is cheap to write, expensive to redo. A short documentation phase forces
the plan to be explicit before it costs time to implement, lets the user review
and veto a bad direction when it costs minutes (not days), and leaves a record
of *why* — not just *what* — for the next reader.

- **Review before cost**: reject a bad plan before it becomes code.
- **Decisions separated from code**: choices live in docs/, not buried in
  commit messages or lost in chat.
- **Traceability**: every change points back to the task doc that authorized it.

## When to use

More than a trivial one-file edit:
- a new feature, module, or subsystem
- a refactor or migration touching many files
- a bug fix whose root cause is not obvious
- any work needing more than one step or touching more than one subsystem

## Workflow (paired with discuss-before-begin)

This skill is the **downstream** of `discuss-before-begin`: discuss first until
consensus, then this skill turns the agreed plan into durable documents, then
code.

1. **Discuss** — until the user confirms consensus (see `discuss-before-begin`).
2. **Record** — write the discussion and the user's explicit choices into
   `docs/discussion/`.
3. **Distill** — extract reusable rules from the discussion into
   `docs/principle/`.
4. **Decompose** — break the work into tasks in `docs/task/` (one file per
   task).
5. **Describe** — start `docs/manual/` as the shape of the feature becomes
   clear.
6. **Code** — start only after the docs above exist and the user has seen them.
7. **Sync** — when reality diverges from the plan, update the docs *first*, and
   log deferred/rejected ideas in `docs/temp/`.
8. **Close** — mark task docs done and make sure `docs/manual/` matches reality.

## Directory layout

```
docs/
  discussion/                 # conversations & the user's explicit choices
  principle/                  # reusable rules distilled from discussions
  task/                       # task + sub-task files
    01-do-something.md
    01-01-do-something.md
    01-02-do-something.md
    02-do-something.md
    ...
  manual/
    how-to-do-something.md    # how to use the codebase
                              # if there are chapters, make a folder named
                              # after the chapter
  temp/                       # "decided not to do now" + why; may be
    choose-not-do-something.md   # revisited later
    why-not-do-something.md
```

## Doc conventions

### discussion/
- One file per discussion topic. Record the user's actual decisions verbatim
  where possible, plus the alternatives rejected and why.

### principle/
- Reusable rules that survive beyond one task (patterns, constraints, "always
  X / never Y"). These are the *laws* future tasks must obey.

### task/
- One file per unit of work. Naming: `NN-description.md`; subtasks use
  `NN-NN-description.md` (decompose when a task is too big to review as one
  change).
- Each task doc **must** contain these fields:

  | Field | Meaning |
  |---|---|
  | **Goal** | what "done" looks like |
  | **Why** | link to the discussion/principle that motivated it |
  | **Approach** | the concrete steps, in order |
  | **Files touched** | expected files/areas, so scope is reviewable |
  | **Acceptance criteria** | how to verify it works |
  | **Status** | `todo` → `doing` → `done` |

### manual/
- Write as the feature takes shape; update it as the feature lands. Never let
  it describe something the code no longer does.

### temp/
- Record things deliberately *not* done now, and the reason. This is a
  reversible-decision graveyard: a future "why didn't we..." is answered here.

## Keeping docs in sync (iron rules)

1. **Docs lead, code follows** — before writing a line, the relevant task doc
   must already describe what you are about to do.
2. **Reality surprises → doc first** — if an API doesn't exist, a design
   doesn't fit, or a step turns out different, update the doc first, then code.
   If it changes the agreed plan, tell the user and record it in `temp/`.
3. **No `done` with stale docs** — a task may not be marked done while its doc
   is out of date.
4. **Docs vs. code conflict is a bug** — if they disagree, fix the doc, the
   code, or both, and say which.

## Definition of done for the documentation phase

The docs are "ready to code from" when:
- every task has an approach and acceptance criteria,
- every discussion that led to a decision is recorded,
- the user has read and approved the plan.

## Anti-patterns

- **Docs as ritual** — writing docs nobody reads. Every doc must change a future
  decision or save a future reader's time.
- **Over-documentation** — don't restate the code; record decisions,
  constraints, and "why".
- **Drift** — "I'll update the docs at the end" is how docs become lies. Update
  them together with the code.
- **Silent deviation** — changing the plan during coding without telling the
  user or logging it in `temp/`.

## Scale

- **Large task** — full pipeline above.
- **Small task** — a single task doc may be enough, but still name the Goal and
  Acceptance criteria, and still record any surprising decision in `temp/`.

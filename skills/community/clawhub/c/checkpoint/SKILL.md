---
name: checkpoint
description: >
  Part of the Overpowered skill suite.
  Create a durable, self-contained state package so a fresh agent, session, or different harness can resume non-trivial work without the original chat history. Use for long-running work, context resets, handoffs, or pauses; not for simple finished tasks.
metadata:
  suite: overpowered
  suite_url: https://github.com/raguets/overpowered
  level: "0-primitive"
  version: "0.1.0"
---

# Overpowered / Checkpoint

## Core rule

**Persist the state required to continue, not a transcript of how the conversation felt.**

## Procedure

Create or update a `CHECKPOINT.md` in the working directory unless the user specifies another location.

Capture:

1. **Goal** — current objective and completion criteria.
2. **Current state** — what is done, in progress, and not started.
3. **Authoritative inputs** — exact artifacts/sources the receiver should trust.
4. **Decisions** — decisions made and why.
5. **Rejected paths** — only when retrying them would waste time.
6. **Artifacts** — files, branches, queries, outputs, and their purpose.
7. **Evidence** — checks already performed and their results.
8. **Known issues / unknowns** — material unresolved items.
9. **Next action** — the smallest useful next step.
10. **Environment assumptions** — only non-obvious requirements.

## Receiver test

Before finishing, ask: **Could a capable fresh agent resume correctly from this file plus the referenced artifacts, without the chat transcript?** If not, add what is missing.

## Gotchas

- Do not copy the full conversation.
- Do not write vague state such as “mostly done.”
- Do not omit negative decisions that a new agent is likely to repeat.
- Do not claim verification that was not actually performed.

## Stop condition

Stop when the receiver test passes.

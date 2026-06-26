---
name: engrm-memory
description: Use Engrm memory deliberately before coding, during coding, and when saving reusable lessons.
---

# Engrm Memory

Use this skill when the user is working on an existing codebase and continuity
matters more than a cold start.

## Before you start

Use Engrm only if it is already connected and available in the current
environment.

If Engrm is not available, say that Engrm memory is not connected on this
machine and continue without inventing fallback commands or fake setup steps.

## Command guardrails

Do not invent Engrm CLI commands like:

- `engrm search`
- `engrm save`
- `engrm timeline`

Those are not normal Engrm CLI commands.

Memory search, timeline, save, recent activity, and stats are Engrm
tool/workflow capabilities, not generic shell commands.

## What this skill is for

- Pull relevant prior knowledge into the current session.
- Reuse past decisions, fixes, and discoveries before repeating work.
- Save new knowledge when the session produces something worth carrying forward.
- Make multi-device and multi-agent memory actually useful instead of passive.

## When to use Engrm first

Use Engrm before coding when:

- the user is resuming work after a break
- a project or subsystem looks familiar
- the task touches a bug, auth flow, deployment path, or refactor area that may
  have been handled before
- the session starts on a different machine or with a different coding agent

Use Engrm during coding when:

- the work starts drifting
- you need to confirm an earlier decision
- you suspect the same issue has already been solved elsewhere

Use Engrm after coding when:

- a useful decision was made
- a bugfix or pattern is likely to recur
- the session discovered a real lesson that future work should start with

## Default Engrm workflow

1. Start by checking recent activity or searching relevant memory.
2. Pull timeline or session context if the area has recent churn.
3. Apply prior decisions before changing code.
4. Save only high-signal outcomes, not every trivial step.

## Good Engrm questions

- What did we already learn about this area?
- Was there an earlier decision for this approach?
- Did a previous session touch the same files or subsystem?
- Is there a recent bugfix or security note I should reuse?

## Save high-signal memories

Prefer saving:

- durable decisions
- bugfixes with clear cause and resolution
- discoveries that unblock later sessions
- patterns worth reusing across projects

Avoid saving:

- obvious implementation details
- noisy or temporary dead ends
- generic filler that will pollute retrieval later

## What success looks like

The agent starts informed, reuses real project memory, and leaves behind a small
number of valuable observations that improve the next session.

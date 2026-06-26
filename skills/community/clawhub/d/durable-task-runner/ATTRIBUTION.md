# Attribution and borrowed ideas

This project is original glue code and schema work for a **durable task runner / orchestrator** for OpenClaw, but it intentionally borrows ideas from other ClawHub skills.

## Attribution policy

When ideas, schema patterns, workflow discipline, or code snippets are adapted from another source:
- name the source skill/package explicitly
- note what was borrowed
- state whether we adapted the **idea**, **structure**, or **literal code**
- keep attribution near the relevant file when practical

As of this commit, this repo primarily borrows **ideas and workflow patterns**, not large literal code copies.

Exception:
- `scripts/task_resume_queue.py` is a **fresh local adaptation closely inspired by** the helper script from ClawHub `task-resume`. It is not a blind copy, but the lineage is direct and should remain credited.

---

## Sources reviewed

### 1. `task-resume`
- Source slug: `task-resume`
- Source package contents reviewed locally from ClawHub download

**What we borrowed conceptually**
- interrupted-work recovery as a first-class concern
- queue-based resume semantics
- helper-script pattern instead of prompt-only logic
- soft-fail handling for missing prior session logs / recovery inputs

**Why it mattered**
- it provides a practical minimal model for preserving work across interruptions

**What we did not copy directly**
- we are not using its queue file format verbatim
- we are not embedding its full workflow as-is

---

### 2. `restart-safe-workflow`
- Source slug: `restart-safe-workflow`
- Source package contents reviewed locally from ClawHub download

**What we borrowed conceptually**
- strict workflow discipline around checkpoint / resume / reconcile
- `pendingActions` / action-state / idempotency-ledger style state ideas
- strong done-gate thinking: completion is a verified state, not a process exit code
- explicit reconcile / escalation semantics

**Why it mattered**
- it had the best durable-state and recovery concepts of the skills reviewed

**What we did not copy directly**
- we are not reusing its restart-specific shell workflow directly
- we are not carrying over its OpenClaw restart SOP verbatim

---

### 3. `subagent-orchestrator`
- Source slug: `subagent-orchestrator`
- Source package contents reviewed locally from ClawHub download

**What we borrowed conceptually**
- main-agent-as-controller model
- subagent handoff protocol ideas
- anti-drop / mandatory-next-dispatch philosophy
- continuous task-line framing instead of one-shot-run framing

**Why it mattered**
- it is the strongest ClawHub example of orchestration semantics and controller discipline

**What we did not copy directly**
- we are not using its task-board format directly
- we are not copying its full return protocol unchanged; we may adapt and simplify it

---

## Current status

This repo currently contains:
- original scaffold code in `scripts/task_ctl.py`
- original skill text in `SKILL.md`
- original schema documentation in `references/task-schema.md`

These files were written here, but influenced by the source ideas above.

## Development provenance

This project was developed iteratively with hands-on assistance from OpenClaw/LLM tooling.
It was also reviewed critically with Claude during hardening/publish-readiness passes.
Final code selection, integration, testing, and publication decisions were curated by John Watson.

## Future rule

If we later import literal code fragments or closely adapted structures from any source, update this file and add an inline note in the relevant file header.

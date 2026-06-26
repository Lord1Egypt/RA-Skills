# Integration with Other Skills

`coding-pipeline` is deliberately narrow: it enforces the 4-phase structure. It does not replace other specialized skills; it pairs with them. This reference shows how to combine it with the most common companions.

## `systematic-debugging`

**When to hand off:** Phase 4 has escalated (3 attempts exhausted) and the problem is complex enough to warrant structured investigation with parallel hypothesis testing.

**How to hand off:**

1. Complete the Phase 4 attempt log (all 3 attempts documented)
2. Invoke `systematic-debugging` with the attempt log as input
3. `systematic-debugging` picks up where Phase 4 leaves off — its protocol adds deeper instrumentation, hypothesis branching, and parallel sub-agent investigation

**Handoff message template:**

> Phase 4 exhausted after 3 attempts on <task>. Full attempt log in `.pipeline-state/attempts-<task>.md`. Invoking `systematic-debugging` with this log as the "what has been tried" section.

**Why pair them:** `coding-pipeline` enforces discipline on normal work. `systematic-debugging` handles the pathological cases where normal discipline isn't enough. Use the cheap skill first, escalate to the expensive one when the cheap one gives up.

## `self-improving-agent`

**When to log:** After every failed attempt in Phase 4 — immediately, while context is fresh.

**What to log:**

```markdown
## [ERR-YYYYMMDD-XXX] <task-name>

**Logged**: ISO-8601 timestamp
**Priority**: high
**Status**: pending
**Area**: frontend | backend | infra | tests

### Summary
Phase 4 attempt N failed — <one line>.

### Error
<redacted error output — no secrets>

### Context
- Phase 1 hypothesis: <original>
- Attempt N hypothesis: <updated>
- What we learned: <key insight from this failure>

### Suggested Fix
<if identifiable>

### Metadata
- Source: coding-pipeline-phase-4
- Related Files: <path>
- Reproducible: yes | no | unknown
```

**Why pair them:** `coding-pipeline` prevents bad practice; `self-improving-agent` captures learning from the bad-practice-that-happened-anyway. Together they form a loop: attempted failures become logged learnings become promoted rules become permanent improvements.

**Loop pattern:**

```
coding-pipeline Phase 4 fails
        ↓
self-improving-agent logs the attempt
        ↓
recurrence threshold hit (3+ similar failures)
        ↓
promotion to CLAUDE.md / AGENTS.md as a prevention rule
        ↓
future tasks hit the rule in Phase 1 — the mistake is no longer possible
```

## `root-cause-analysis`

**When to hand off:** Phase 3 root-cause verification is ambiguous — you can't confidently answer "if I rolled back this change, would the symptom return because of the same cause?"

**How to hand off:**

1. Pause Phase 3
2. Invoke `root-cause-analysis` with the Phase 1 hypothesis and the Phase 2 change as input
3. Let RCA produce a verified cause chain
4. Return to Phase 3 with the RCA output as evidence

**Why pair them:** `coding-pipeline`'s root-cause check is a go/no-go. `root-cause-analysis` is the full investigation that produces the answer when the check is uncertain.

## `test-driven-development`

**When to pair:** Always, when the task includes "add or modify behavior" (i.e. not a pure refactor).

**How to pair:**

- Phase 1's **success criteria** should be expressed as a **failing test** written first
- Phase 2 is then "make the test pass" — the discipline of TDD enforces the one-fix rule naturally
- Phase 3's **focused test** is the same test from Phase 1, now green

**Why pair them:** TDD and `coding-pipeline` reinforce each other. TDD gives you the test; `coding-pipeline` gives you the framing around it. TDD without phases becomes "make it pass by any means"; phases without TDD become "I think it works, let me check".

## `verification-before-completion`

**When to pair:** Every Phase 3, especially before claiming the task is done.

**How to pair:** `verification-before-completion` requires running verification commands and confirming output before making success claims. This is exactly Phase 3's job, made explicit. The two skills say the same thing from different angles — layer them for rigor.

## General Pairing Philosophy

`coding-pipeline` is the **meta-skill**: it defines when to invoke the others.

- Phase 1 might invoke `brainstorming` (for complex features) or read learnings from `self-improving-agent`
- Phase 2 might invoke `test-driven-development` or `receiving-code-review`
- Phase 3 invokes `verification-before-completion` and possibly `root-cause-analysis`
- Phase 4 invokes `systematic-debugging` on escalation and `self-improving-agent` on every failed attempt

The pipeline is the orchestration layer. The other skills are the tools it reaches for.

## Not a Replacement For

`coding-pipeline` does **not** replace:

- **`brainstorming`** — for upstream design work before a task is even defined
- **`writing-plans`** — for multi-phase implementation planning beyond a single task
- **`executing-plans`** — for running a plan across multiple tasks
- **Platform-specific skills** — stack gotchas, deployment skills, etc.

The pipeline runs **inside** a single task. Upstream (brainstorming, planning) and platform-specific concerns live elsewhere.

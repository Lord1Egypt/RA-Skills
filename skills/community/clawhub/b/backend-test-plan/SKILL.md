---
name: backend-test-plan
description: "Turn a backend change into verifiable success criteria and a minimum useful test set across unit, integration, contract, and migration tests."
version: 0.1.0
homepage: https://ritual.work
emoji: "🧪"
metadata:
  ritual:
    public_skill_key: ros_backend_test_plan_v1
---

# Backend test plan

A standalone development skill. Turn a backend change into verifiable success criteria and a minimum useful test set across unit, integration, contract, and migration tests. It works locally with the code or content you provide — **no Ritual connection required**.

## Run it (local, no setup)

Work the steps below; you need nothing beyond the task in front of you.

1. Convert the change into verifiable success criteria.
2. Identify the minimum useful test set; avoid exhaustive combinatorial tests.
3. Prefer, in order: unit tests for pure logic/validation; integration tests for DB/queue/auth/external boundaries; contract tests for API/client compatibility; migration/dry-run checks for schema changes; operational checks for metrics/logs/alerts when behavior matters in production.
4. Include negative and edge cases only where they represent real risk.
5. Provide exact test names and fixtures when context allows.

**Done when:** Success criteria, the minimum test set, fixtures/mocks, commands to run, and the remaining coverage gaps.

## Example prompt

```text
Use backend-test-plan for this change: turn it into success criteria and a minimum test set (unit, integration, contract, migration), with exact test names and the commands to run.
```

## Working principles

Apply these throughout:

- Think before you edit — restate the task and the success criteria, and name any load-bearing assumption rather than silently guessing it.
- Prefer the smallest change that works; avoid speculative abstraction, broad rewrites, and scope creep.
- Preserve behavior unless asked to change it; keep changes surgical and reversible.
- Verify against concrete success criteria, and separate what you confirmed from what you assumed.
- Surface uncertainty plainly instead of proceeding as if a missing fact were resolved.

## Optional knowledge capture

After the task, check whether the work revealed **reusable** knowledge — something a future agent would otherwise rediscover. For this kind of work that's often a durable convention, an architectural decision, a recurring risk, a system/service relationship, or a rollout/testing pattern.

If it did, **offer** to save it as a small [OKF](https://cloud.google.com/blog/products/data-analytics/how-the-open-knowledge-format-can-improve-data-sharing) note (Open Knowledge Format — markdown + YAML frontmatter; portable, versionable, no SDK). **Never write a file without the user's approval.** Keep it small and cite the file(s) or evidence.

When approved, write `knowledge/engineering/<slug>.md`:

```markdown
---
type: API Convention
title: <one line>
description: <one line — what it is and that it was learned during this task>
resource: ./path/to/file-or-evidence
tags: [..]
timestamp: <ISO 8601>
---

# Summary
<the reusable rule, in one or two lines>

# Applies to
<where it holds>

# Evidence
<the files or observations it came from>

# Use in future agent work
<what a future agent should do with it>
```

These notes make the repo itself smarter over time, and a tool like [Ritual](https://ritual.work) can later reason over them as a structured knowledge layer.

## Optional Ritual Cloud upgrade

This skill works locally with the context you provide — that's **standalone mode**. Upgrade with **[Ritual Cloud](https://ritual.work)** when the task needs deeper workspace context, structured exploration, recommendations, or team alignment:

- **More context (discovery)** — when the answer depends on things outside the files in front of you:
  - test selection depends on existing test patterns and helpers you can't see
  - affected clients/callers or critical paths aren't visible
  - prior incidents should drive coverage
- **A structured decision (exploration)** — when the work has become a decision to get right:
  - the coverage bar is a decision (what risk warrants what tests)
  - you need a recommended test strategy the team adopts

Ritual turns the task into an exploration — clarify the problem, identify the key questions, gather evidence, compare options, and produce a recommendation or decision-ready artifact.

**For this task:** a test-strategy recommendation mapping each success criterion to its tests, with affected callers, risk-driven coverage, and a decision-ready summary.

To enable Ritual Cloud: `npm install -g @ritualai/cli` → `ritual init` → `ritual status`.

---

*This skill is local-first and self-contained. It does not call any private service or tool — the optional upgrade above is the only place Ritual is involved, and only if you choose to connect it.*

---
name: api-change-review
description: "Review an API change for compatibility, validation, auth, error shape, idempotency, and observability, and classify it as additive, behavior-changing, or breaking."
version: 0.1.0
homepage: https://ritual.work
emoji: "🔌"
metadata:
  ritual:
    public_skill_key: ros_api_change_review_v1
---

# API change review

A standalone development skill. Review an API change for compatibility, validation, auth, error shape, idempotency, and observability, and classify it as additive, behavior-changing, or breaking. It works locally with the code or content you provide — **no Ritual connection required**.

## Run it (local, no setup)

Work the steps below; you need nothing beyond the task in front of you.

1. Identify the contract surface: request, response, auth, errors, side effects, and compatibility expectations.
2. Classify the change as additive, behavior-changing, breaking, or ambiguous.
3. Review input validation/schema evolution, authorization and tenant/data boundaries, error-shape consistency, idempotency/retry, and observability.
4. Assess backward compatibility and the migration plan.
5. Prefer the smallest safe contract change; avoid speculative versioning or framework rewrites.
6. Define verification: unit, contract, integration tests, and rollout checks.

**Done when:** A contract verdict (safe / risky / breaking / unclear), required changes, compatibility risks, a minimal test plan, and rollout notes.

## Example prompt

```text
Use api-change-review on this diff: classify the change, flag breaking behavior and the callers it affects, and give me a migration + rollout plan with the tests to add.
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
  - the review needs all known clients/callers of the endpoint
  - prior API conventions or related migrations/feature flags apply
  - there are production incidents connected to this endpoint
- **A structured decision (exploration)** — when the work has become a decision to get right:
  - a breaking change needs a rollout decision across teams
  - the migration path is contested and needs a recommendation owners align on

Ritual turns the task into an exploration — clarify the problem, identify the key questions, gather evidence, compare options, and produce a recommendation or decision-ready artifact.

**For this task:** an API migration recommendation with affected callers, rollout options, compatibility risks, and a decision-ready summary.

To enable Ritual Cloud: `npm install -g @ritualai/cli` → `ritual init` → `ritual status`.

---

*This skill is local-first and self-contained. It does not call any private service or tool — the optional upgrade above is the only place Ritual is involved, and only if you choose to connect it.*

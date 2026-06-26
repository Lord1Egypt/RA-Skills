# Classification Rubric

Load this reference only when the script is unavailable, when reviewing ambiguous results, or when changing cleanup policy.

## Keep

Keep items that are stable, global, and useful across many future tasks:

- Communication preferences, such as desired language, brevity, directness, formatting, or review style.
- Durable working preferences, such as testing expectations, preferred tools, coding conventions, or repository hygiene rules.
- Long-term user context that affects many tasks, such as role, recurring domains, accessibility needs, locale, timezone, or persistent environment constraints.
- Stable names of important long-lived projects or systems, but only when the fact is useful without detailed stale status.
- Explicit user instructions that apply generally across agents.

## Condense

Condense items that contain a durable signal mixed with task detail:

- Replace a completed task history with the general preference it revealed.
- Replace a specific one-off command sequence with a durable tool preference.
- Replace long project summaries with a stable project identity or recurring constraint.
- Merge duplicate or overlapping preferences into one canonical bullet.

## Remove

Remove items that are not appropriate for long-term global memory:

- Completed task notes, temporary plans, or debugging traces.
- Stale statuses such as `currently working on`, `next step is`, `today`, `tomorrow`, or dated commitments that are no longer current.
- Details about a single ticket, pull request, report, dataset, branch, prompt, or conversation.
- Failed attempts, intermediate observations, transient errors, logs, or command output.
- Guesses, inferred preferences, or speculative personal facts that the user did not confirm.
- Secrets, credentials, private URLs, tokens, passwords, or sensitive operational details.
- Duplicates, contradictions, and entries that are too vague to help future agents.

## Flag

Flag items for user review when:

- The item may be durable but could also be stale.
- The item refers to a project or identity that cannot be verified locally.
- Two memory files disagree about an important preference.
- Removing the item could materially change future agent behavior.

## Canonical Memory Shape

```markdown
# User Memory

## Global Preferences
- ...

## Working Style
- ...

## Durable Context
- ...

## Agent Instructions
- ...

## Review Needed
- ...
```

Omit empty sections. Do not create `Review Needed` if there are no unresolved items.

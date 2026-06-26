---
name: deferred-decision-tracker
description: Capture decisions that are intentionally deferred, assign a review date and owner, and prevent them from silently disappearing.
metadata:
  openclaw:
    tags:
      - productivity
      - operations
      - planning
      - decision-support
---

# Deferred Decision Tracker

Use this skill when a decision is important enough to revisit, but not ready to decide now.

The goal is simple: **deferred should not mean forgotten.**

## When to Use
Use this skill when the user says things like:

- “Let’s come back to this later.”
- “Not now, but don’t let this disappear.”
- “Park this until after launch.”
- “We need a decision on this next week.”
- “This is a good idea, but we need more data first.”

## Capture Rule
Every deferred decision should be recorded with:

1. **Decision title** — short, concrete name.
2. **Why deferred** — what is missing or what must happen first.
3. **Owner** — who is responsible for reviving it.
4. **Review date/time** — when it should return.
5. **Trigger condition** — what event makes it relevant again.
6. **Output path or artifact** — where the future decision board should live.
7. **Status** — open, waiting, ready, decided, retired.
8. **Retirement condition** — when to stop surfacing it.

## Behavior
When a decision is deferred:

- Create or update a deferred-decision register.
- Make the next review date explicit.
- If a durable reminder or scheduler exists, use it when exact timing matters, preferring local or private mechanisms by default.
- Before creating external calendar events, sending notifications to other people, emailing, posting, purchasing, changing billing, or modifying access/security settings, get explicit user approval.
- If no scheduler exists, write the item somewhere the normal review process will check.
- Do not surface stale items repeatedly unless something has changed or a real review point has arrived.

## Privacy and Storage

Deferred-decision registers can contain sensitive personal, financial, business, security, or strategic information. Store them in a private or user-approved project location by default. Do not place sensitive decisions in public documents, shared folders, examples, or published artifacts unless the user explicitly asks.

## Recommended Register Format

```markdown
# Deferred Decisions

| Decision | Owner | Deferred Because | Review Date | Trigger | Status | Artifact |
|---|---|---|---|---|---|---|
| Example vendor evaluation | Ops lead | Waiting for pricing | 2026-06-01 | Pricing received | waiting | docs/vendor-eval.md |
```

## Review Behavior
At review time:

1. Check whether the trigger condition happened.
2. Check whether the missing input is now available.
3. If ready, create a decision board with options, criteria, recommendation, risks, and explicit go/no-go ask.
4. If still not ready, update the reason and next review date.
5. If no longer relevant, mark retired and stop surfacing it.

## Decision Board Template

```markdown
# Decision Board: <Decision Title>

## Context
Why this decision matters now.

## Options
1. Option A
2. Option B
3. Option C

## Criteria
- Cost
- Speed
- Risk
- Reversibility
- Strategic fit

## Recommendation
Recommended option and why it beats alternatives.

## Risks / Caveats
What could be wrong or incomplete.

## Ask
Approve / reject / defer until <date>.
```

## Guardrails

- Do not create noisy reminders for low-value items.
- Do not treat a reminder as completion; the decision still needs an artifact or explicit closeout.
- Do not publish private user context in public registers or examples.
- Prefer specific review dates over vague “later.”
- If the item affects external action, money, privacy, or security, require explicit user approval before acting.

## Success Standard
A deferred decision is handled correctly when a future assistant, teammate, or agent can answer:

- What was deferred?
- Why?
- Who owns it?
- When does it return?
- What must be true to decide?
- Where is the decision artifact?

# AANA Support Reply Guardrail Skill

This OpenClaw-style skill helps agents check customer support replies for invented facts, refund promises, policy overclaims, and private data exposure.

## Marketplace Slug

Recommended slug:

```text
aana-support-reply-guardrail
```

## Contents

- `SKILL.md`: agent-facing instructions.
- `manifest.json`: review metadata and boundaries.
- `schemas/support-reply-review.schema.json`: optional review-payload shape.
- `examples/redacted-support-reply-review.json`: safe example payload.

## What It Does

The skill asks the agent to:

1. Separate customer-provided facts from verified account records.
2. Block invented account, order, billing, delivery, cancellation, or case-status claims.
3. Avoid refund, credit, replacement, exception, escalation, or timeline promises without authorization.
4. Avoid policy overclaims and fake certainty.
5. Minimize private customer data before sending a reply.

## What It Does Not Do

This package does not:

- install dependencies,
- execute code,
- call remote services,
- write files,
- persist memory,
- inspect accounts by itself,
- approve refunds, credits, exceptions, or support outcomes by itself.

## Safety Model

Use redacted summaries for review payloads. Do not include raw account records, full payment numbers, private ticket history, private messages, health records, legal records, credentials, or unrelated customer data.

Refunds, credits, replacements, policy exceptions, account actions, and high-impact support outcomes should be verified through an approved system or human review.

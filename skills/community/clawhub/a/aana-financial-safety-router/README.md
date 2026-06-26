# AANA Financial Safety Router Skill

This OpenClaw-style skill helps agents gate investment, tax, budgeting, debt, and purchase advice for unsupported claims and missing risk disclosure.

## Marketplace Slug

Recommended slug:

```text
aana-financial-safety-router
```

## Contents

- `SKILL.md`: agent-facing instructions.
- `manifest.json`: review metadata and boundaries.
- `schemas/financial-safety-review.schema.json`: optional review-payload shape.
- `examples/redacted-financial-safety-review.json`: safe example payload.

## What It Does

The skill asks the agent to:

1. Separate general financial education from personalized financial advice.
2. Check investment, tax, budgeting, debt, and purchase claims for support.
3. Add material risk, uncertainty, fee, tax, liquidity, and downside disclosures where relevant.
4. Avoid guaranteeing returns, tax outcomes, approvals, savings, or eligibility.
5. Refer high-impact investment, tax, legal, debt, or insurance decisions to qualified professionals.
6. Minimize private financial data in review payloads and replies.

## What It Does Not Do

This package does not:

- install dependencies,
- execute code,
- call remote services,
- write files,
- persist memory,
- inspect accounts by itself,
- provide licensed financial, tax, legal, or investment advice by itself.

## Safety Model

Use redacted summaries for review payloads. Do not include full payment numbers, bank details, tax IDs, credit reports, pay stubs, raw tax documents, identity documents, credentials, or unrelated financial data.

High-impact, personalized, current-market, account-specific, tax, legal, investment, or debt-crisis decisions should be routed to trusted evidence, qualified professionals, or human review.

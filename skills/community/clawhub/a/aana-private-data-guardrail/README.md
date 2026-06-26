# AANA Private Data Guardrail Skill

This OpenClaw-style skill helps agents avoid exposing private account, billing, payment, health, legal, personal, or sensitive business data.

## Marketplace Slug

Recommended slug:

```text
aana-private-data-guardrail
```

## Contents

- `SKILL.md`: agent-facing instructions.
- `manifest.json`: review metadata and boundaries.
- `schemas/private-data-review.schema.json`: optional review-payload shape.
- `examples/redacted-private-data-review.json`: safe example payload.

## What It Does

The skill asks the agent to:

1. Identify private data classes.
2. Check whether the data is necessary and authorized.
3. Remove or redact unnecessary sensitive details.
4. Avoid invented account, billing, payment, health, legal, or personal facts.
5. Ask, defer, revise, or refuse when disclosure is unsafe.

## What It Does Not Do

This package does not:

- install dependencies,
- execute code,
- call remote services,
- write files,
- persist memory,
- inspect accounts by itself,
- make compliance decisions by itself.

## Safety Model

Use redacted summaries for review payloads. Do not include API keys, bearer tokens, passwords, recovery codes, full payment numbers, bank account numbers, raw health records, raw legal records, or unrelated private messages.

High-impact or irreversible disclosures should go to a verified system or human review.

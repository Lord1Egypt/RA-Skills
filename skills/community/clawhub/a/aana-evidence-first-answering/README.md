# AANA Evidence First Answering Skill

This OpenClaw-style skill forces answer drafts to separate known facts, assumptions, missing evidence, and next retrieval steps.

## Marketplace Slug

Recommended slug:

```text
aana-evidence-first-answering
```

## Contents

- `SKILL.md`: agent-facing instructions.
- `manifest.json`: review metadata and boundaries.
- `schemas/evidence-first-review.schema.json`: optional review-payload shape.
- `examples/redacted-evidence-first-review.json`: safe example payload.

## What It Does

The skill asks the agent to:

1. Identify important answer claims.
2. Separate known facts from assumptions and inferences.
3. Mark missing evidence explicitly.
4. Remove or revise unsupported claims.
5. Name the next retrieval, clarification, or deferral step when evidence is missing.
6. Keep private evidence summaries redacted.

## What It Does Not Do

This package does not:

- install dependencies,
- execute code,
- call remote services,
- write files,
- persist memory,
- retrieve evidence by itself,
- certify that an answer is true by itself.

## Safety Model

Use redacted summaries for review payloads. Do not include secrets, raw medical/legal/financial records, full private messages, sensitive logs, or unrelated private data.

High-impact answers should not move forward on assumptions. Ask, retrieve, or defer when missing evidence controls the conclusion.

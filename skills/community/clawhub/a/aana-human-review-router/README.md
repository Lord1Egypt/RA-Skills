# AANA Human Review Router Skill

This OpenClaw-style skill routes uncertain, high-impact, irreversible, or low-evidence actions to user or human review.

## Marketplace Slug

Recommended slug:

```text
aana-human-review-router
```

## Contents

- `SKILL.md`: agent-facing instructions.
- `manifest.json`: review metadata and boundaries.
- `schemas/human-review-route.schema.json`: optional review-payload shape.
- `examples/redacted-human-review-route.json`: safe example payload.

## What It Does

The skill asks the agent to:

1. Classify impact, evidence, authorization, and reversibility.
2. Route low-risk actions to proceed.
3. Ask the user when intent or user-held evidence is missing.
4. Require explicit approval for irreversible or high-impact actions.
5. Route specialized legal, medical, financial, safety, compliance, production, or policy decisions to qualified review.
6. Minimize sensitive data in review packets.

## What It Does Not Do

This package does not:

- install dependencies,
- execute code,
- call remote services,
- write files,
- persist memory,
- inspect systems by itself,
- approve high-impact actions by itself.

## Safety Model

Use redacted summaries for review packets. Do not include secrets, credentials, raw medical/legal/financial records, full private messages, sensitive logs, full account records, or unrelated private data.

Do not proceed after routing until the required user approval, human review, professional review, or admin review is complete.

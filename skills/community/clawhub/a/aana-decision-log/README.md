# AANA Decision Log Skill

This OpenClaw-style skill helps agents produce compact audit records for important decisions: what was checked, what failed, what changed, and what risk remains.

## Marketplace Slug

Recommended slug:

```text
aana-decision-log
```

## Contents

- `SKILL.md`: agent-facing instructions.
- `manifest.json`: review metadata and boundaries.
- `schemas/decision-log.schema.json`: optional structured log shape.
- `examples/redacted-decision-log.json`: safe example record.

## What It Does

The skill asks the agent to:

1. Identify the important decision or guardrail gate.
2. Record checks actually performed.
3. Mark failed, unclear, or unperformed checks honestly.
4. Summarize what changed because of the review.
5. Minimize private data and avoid raw sensitive records.
6. State the final action and residual risk.

## What It Does Not Do

This package does not:

- install dependencies,
- execute code,
- call remote services,
- write files,
- persist memory,
- inspect systems by itself,
- certify compliance by itself.

## Safety Model

Use redacted summaries for decision logs. Do not include secrets, full payment details, raw medical or legal records, private messages, sensitive logs, or unrelated private data.

Decision logs should be compact audit notes, not inflated proof. If a check did not run, the log should say so.

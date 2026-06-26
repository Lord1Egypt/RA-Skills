# AANA Tool Use Gate Skill

This OpenClaw-style skill helps agents check whether tool calls are necessary, scoped, authorized, and safe before use.

## Marketplace Slug

Recommended slug:

```text
aana-tool-use-gate
```

## Contents

- `SKILL.md`: agent-facing instructions.
- `manifest.json`: review metadata and boundaries.
- `schemas/tool-use-review.schema.json`: optional review-payload shape.
- `examples/redacted-tool-use-review.json`: safe example payload.

## What It Does

The skill asks the agent to:

1. Check whether a tool is actually needed.
2. Define exact target scope before tool use.
3. Confirm authorization for risky, private, external, or state-changing actions.
4. Minimize private data in tool inputs, outputs, logs, and summaries.
5. Prefer read-only, preview, draft, dry-run, or staged actions before state changes.
6. Defer or refuse unsafe, unauthorized, destructive, financial, privileged, or external actions.

## What It Does Not Do

This package does not:

- install dependencies,
- execute code,
- call remote services,
- write files,
- persist memory,
- inspect systems by itself,
- approve tool use by itself.

## Safety Model

Use redacted summaries for review payloads. Do not include secrets, credentials, full private records, full logs, full transcripts, full directory dumps, or unrelated private data.

High-impact, irreversible, external-send, financial, production, privileged, destructive, or private-data tool use should require explicit approval or human review.

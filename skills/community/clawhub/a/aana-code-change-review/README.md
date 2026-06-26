# AANA Code Change Review Skill

This OpenClaw-style skill helps agents gate code edits, commits, pull requests, test claims, scope creep, secret leakage, and destructive commands.

## Marketplace Slug

Recommended slug:

```text
aana-code-change-review
```

## Contents

- `SKILL.md`: agent-facing instructions.
- `manifest.json`: review metadata and boundaries.
- `schemas/code-change-review.schema.json`: optional review-payload shape.
- `examples/redacted-code-change-review.json`: safe example payload.

## What It Does

The skill asks the agent to:

1. Confirm the requested code-change scope.
2. Keep unrelated files and refactors out of the change.
3. Report only tests and checks that actually ran.
4. Block secrets, private data, and sensitive logs from code, docs, fixtures, and examples.
5. Require approval before destructive commands, commits, pull requests, deploys, releases, or publishing actions.

## What It Does Not Do

This package does not:

- install dependencies,
- execute code,
- call remote services,
- write files,
- persist memory,
- inspect repositories by itself,
- approve code changes by itself.

## Safety Model

Use redacted summaries for review payloads. Do not include raw secrets, private records, full logs, full diffs, or unrelated repository files when a change summary is enough.

Security-sensitive, destructive, release, deploy, migration, or broad refactor changes should go to a verified review path or human review.

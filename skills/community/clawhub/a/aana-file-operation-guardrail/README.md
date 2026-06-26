# AANA File Operation Guardrail Skill

This OpenClaw-style skill helps agents check before deleting, moving, overwriting, publishing, uploading, exporting, or bulk-editing user files.

## Marketplace Slug

Recommended slug:

```text
aana-file-operation-guardrail
```

## Contents

- `SKILL.md`: agent-facing instructions.
- `manifest.json`: review metadata and boundaries.
- `schemas/file-operation-review.schema.json`: optional review-payload shape.
- `examples/redacted-file-operation-review.json`: safe example payload.

## What It Does

The skill asks the agent to:

1. Identify the intended file operation.
2. Confirm exact target paths or a bounded target folder.
3. Check whether recursion, globbing, publishing, or bulk edits are involved.
4. Prefer dry-runs, diffs, backups, or copy-before-move workflows.
5. Ask, defer, revise, or refuse when the operation could touch unintended files.

## What It Does Not Do

This package does not:

- install dependencies,
- execute code,
- call remote services,
- write files,
- persist memory,
- inspect the filesystem by itself,
- make irreversible file changes by itself.

## Safety Model

Use path summaries for review payloads. Do not include raw file contents, secrets, private records, full directory dumps, or unrelated files when a target summary is enough.

Destructive, recursive, cross-folder, publish, upload, or broad edit operations should require explicit user approval and a verified scope.

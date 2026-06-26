---
name: env-alias-audit
description: Audit .env alias groups for missing required config, conflicting values, and canonical-key drift before deploy.
version: 1.0.0
metadata: {"openclaw":{"requires":{"bins":["bash","python3"]}}}
---

# Env Alias Audit

Use this skill to catch environment-variable alias drift before runtime failures.

## What this skill does
- Parses env vars from `.env`-style files
- Evaluates canonical key + alias groups (built-in defaults or custom spec)
- Flags missing required groups
- Detects conflicting values across aliases in the same group
- Reports alias-only usage where canonical keys are absent

## Inputs
Optional:
- `ENV_FILE` (default: `.env`)
- `ALIAS_SPEC_FILE` (default: built-in alias groups)
- `REQUIRED_GROUPS` (comma-separated canonical keys that must resolve)
- `AUDIT_MODE` (`report` or `strict`, default: `strict`)

## Run

Use built-in alias groups:

```bash
ENV_FILE=.env \
REQUIRED_GROUPS=DATABASE_URL,STRIPE_API_KEY \
bash skills/env-alias-audit/scripts/audit-env-aliases.sh
```

Use custom alias spec:

```bash
ENV_FILE=.env.production \
ALIAS_SPEC_FILE=skills/env-alias-audit/fixtures/alias-spec.sample \
AUDIT_MODE=report \
bash skills/env-alias-audit/scripts/audit-env-aliases.sh
```

Run against fixtures:

```bash
ENV_FILE=skills/env-alias-audit/fixtures/.env.conflict \
REQUIRED_GROUPS=DATABASE_URL,STRIPE_API_KEY \
bash skills/env-alias-audit/scripts/audit-env-aliases.sh
```

## Alias spec format
`ALIAS_SPEC_FILE` accepts one group per line:

```text
CANONICAL_KEY=ALIAS_ONE,ALIAS_TWO
```

- Comments and blank lines are ignored
- Canonical key is always part of the checked group

## Output contract
- Exit `0` when no strict failures are found
- Exit `1` on invalid input, missing required groups (strict), or conflicting alias values
- Prints per-group status (`OK`, `WARN`, `FAIL`) plus a summary

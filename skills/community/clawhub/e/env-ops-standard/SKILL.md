---
name: env-ops-standard
description: Safe .env key-first operations (CRUD) with secret-safe defaults. Use when troubleshooting missing env keys, auth/config failures, or when asked to add/update/remove/list .env entries. Always list/check keys first and never expose secret values unless the user explicitly requests it.
---

# env-ops-standard

Enforce a **Key-First SOP** for `.env` management.

Detailed naming/comment standard lives in:
- `{baseDir}/references/env-key-standard.md`

When user asks about naming conventions, comment templates, key semantics clarity, or ambiguity prevention, read and follow that reference.

## Workflow (mandatory)

1. Run key discovery first (no values):
   - `node {baseDir}/scripts/envsafe.js --file <ENV_FILE> keys`
2. Confirm target key exists/does not exist:
   - `node {baseDir}/scripts/envsafe.js --file <ENV_FILE> exists KEY`
3. Then perform write operation only if needed:
   - set/update: `set` (new key must include `--comment` by default policy)
   - delete: `unset`
4. Validate after every write:
   - `node {baseDir}/scripts/envsafe.js --file <ENV_FILE> lint`
5. For org-wide consistency, run with policy + profile:
   - `node {baseDir}/scripts/envsafe.js --policy /home/node/.openclaw/envsafe-policy.json --profile openclaw-core --file <ENV_FILE> doctor`

## Safety rules

- Default env file: `/home/node/.openclaw/.env` unless user specifies otherwise.
- Never print `.env` full content.
- Never print raw secret values in chat/logs.
- `set` defaults to **stdin-only** input. Passing value via argv requires explicit `--allow-argv`.
- New keys require clear comments by default (`--comment "..."`) to avoid ambiguity.
- New key comments are policy-validated (default requires `used-by` and `updated` markers).
- Key names must follow policy regex (default: `^[A-Z][A-Z0-9_]*$`), no ad-hoc naming.
- Writes are lock-guarded + atomic and create timestamped backups.
- Backup retention is enforced (`--backup-keep`, `--backup-ttl-days`).
- Protected keys are policy-controlled and cannot be unset unless `--force` is explicitly passed.
- `unset` is destructive; confirm intent if user did not explicitly ask to remove key.

## Commands

- List keys (no values):
  - `node {baseDir}/scripts/envsafe.js --file /home/node/.openclaw/.env keys`
- Check key exists:
  - `node {baseDir}/scripts/envsafe.js --file /home/node/.openclaw/.env exists OPENAI_API_KEY`
- Set/update key (safe stdin, default):
  - `printf '%s' 'NEW_VALUE' | node {baseDir}/scripts/envsafe.js --file /home/node/.openclaw/.env set OPENAI_API_KEY --stdin`
- Add new key with mandatory comment (recommended):
  - `printf '%s' 'NEW_VALUE' | node {baseDir}/scripts/envsafe.js --file /home/node/.openclaw/.env set NEW_PROVIDER_API_KEY --stdin --comment "Provider key for xxx integration"`
- Set only when missing:
  - `printf '%s' 'NEW_VALUE' | node {baseDir}/scripts/envsafe.js --file /home/node/.openclaw/.env set OPENAI_API_KEY --stdin --if-missing`
- Remove key:
  - `node {baseDir}/scripts/envsafe.js --file /home/node/.openclaw/.env unset OPENAI_API_KEY`
- Lint format/duplicates:
  - `node {baseDir}/scripts/envsafe.js --file /home/node/.openclaw/.env lint`
- Health summary:
  - `node {baseDir}/scripts/envsafe.js --file /home/node/.openclaw/.env doctor`
- Strict health check (CI/automation):
  - `node {baseDir}/scripts/envsafe.js --file /home/node/.openclaw/.env --strict doctor`
- Preview write without changing file:
  - `... set/unset ... --dry-run`
- Show effective policy:
  - `node {baseDir}/scripts/envsafe.js --policy /home/node/.openclaw/envsafe-policy.json policy`

## Output contract

- `keys`: one key per line
- `exists`: prints `present` or `missing`
- `set`/`unset`: prints changed count + backup file path
- `lint`: prints `OK` if clean; otherwise prints findings and exits non-zero

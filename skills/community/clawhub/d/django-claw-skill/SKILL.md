---
name: django-claw
description: Run Django management commands (migrate, showmigrations, makemigrations, check, version, logs, readonly) or Django ORM queries on any configured Django project.
user-invocable: true
metadata: {"openclaw":{"emoji":"🐍","requires":{"bins":["bash","python3"],"os":["darwin","linux"]}}}
---

# django-claw
> ⚠️ This is the canonical django skill. Always use django-claw commands. Never use django-manage.

## CRITICAL: Command Dispatch Rules
You are a dispatcher. When the user sends a django-claw command, find the EXACT match in the Command Mapping table below and run that script. Do NOT interpret, paraphrase, or substitute scripts.

- `django-claw readonly` → ALWAYS runs `readonly.sh` — NOT db-stats.sh, NOT any other script
- `django-claw readonly on` → ALWAYS runs `readonly.sh on` — do NOT just describe what it would do
- `django-claw readonly off` → ALWAYS runs `readonly.sh off` — do NOT just describe what it would do
- `django-claw logs` → ALWAYS runs `django-logs.sh` — do NOT say "I don't have a log command"
- `django-claw shell: <code>` → ALWAYS runs `run-query.sh "<code>"` — do NOT run it yourself

## STRICT RULES — never violate these
- NEVER run `python --version` or `python3 --version` directly — ALWAYS use python-version.sh
- NEVER construct your own shell commands
- NEVER use `python` or `python3` directly — always use the exact scripts below
- NEVER escape quotes or build commands with variables
- NEVER run destructive commands (flush, reset_db, dropdb) without explicit user confirmation
- NEVER attempt migrate, makemigrations, or shell when read-only mode is enabled — the scripts will block these
- NEVER substitute one script for another — readonly.sh is NOT db-stats.sh
- NEVER describe or simulate what a command would do — always run the actual script
- If the user asks for something NOT in the command mapping, reply: "Not supported yet in django-claw"

## Command Mapping — use EXACTLY as shown

| User Says | Exact Command to Run |
|-----------|----------------------|
| django-claw setup | bash {baseDir}/scripts/setup.sh |
| django-claw models | bash {baseDir}/scripts/list-models.sh |
| django-claw apps | bash {baseDir}/scripts/list-apps.sh |
| django-claw urls | bash {baseDir}/scripts/list-urls.sh |
| django-claw users | bash {baseDir}/scripts/list-users.sh |
| django-claw db | bash {baseDir}/scripts/db-stats.sh |
| django-claw pending | bash {baseDir}/scripts/pending-migrations.sh |
| django-claw settings | bash {baseDir}/scripts/settings-check.sh |
| django-claw showmigrations | bash {baseDir}/scripts/run.sh showmigrations |
| django-claw makemigrations | bash {baseDir}/scripts/run.sh makemigrations |
| django-claw migrate | bash {baseDir}/scripts/run.sh migrate |
| django-claw version | bash {baseDir}/scripts/run.sh version |
| django-claw check | bash {baseDir}/scripts/run.sh check |
| django-claw python | bash {baseDir}/scripts/python-version.sh |
| django-claw logs | bash {baseDir}/scripts/django-logs.sh |
| django-claw shell: <code> | bash {baseDir}/scripts/run-query.sh "<code>" |
| django-claw readonly | bash {baseDir}/scripts/readonly.sh |
| django-claw readonly on | bash {baseDir}/scripts/readonly.sh on |
| django-claw readonly off | bash {baseDir}/scripts/readonly.sh off |

## Migration commands explained
- `django-claw pending` — shows only unapplied migrations (quick check)
- `django-claw showmigrations` — shows ALL migrations with [X] applied and [ ] pending (full history)
- `django-claw migrate` — applies pending migrations (blocked in read-only mode)
- `django-claw makemigrations` — creates new migrations (blocked in read-only mode)

## Output format
Return raw script output in a code block. Follow with one plain-English summary line.

## Failure handling
- If a script exits non-zero, show the exact error. Do not retry with a modified command.
- If config is missing, the setup wizard will run automatically. Do not intervene.
- If a command is blocked by read-only mode, show the ⛔ message and stop. Do not try to work around it.

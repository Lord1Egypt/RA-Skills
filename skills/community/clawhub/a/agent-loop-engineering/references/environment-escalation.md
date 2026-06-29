# Environment Escalation

Use this file when an AI coding loop hits dependency, configuration, runtime, permission, or infrastructure issues.

## Agent May Handle Automatically

The agent may proceed without asking when the change is project-local, reversible, and verifiable:

- Install dependencies declared by the project manifest or lockfile.
- Restore dependency consistency using the project's package manager.
- Fix test, typecheck, lint, build, import, or script errors caused by the current task.
- Adjust project-local config, test config, mock config, or script paths.
- Resolve local port conflicts by using another development port.
- Add or update mocks, fixtures, sample data, and tests needed for verification.
- Regenerate project-local generated files when the repository already uses that generator.
- Fix regressions introduced by the current loop.

`Docs/LOOP_CONFIG.md` may disable any of these whitelist actions for a project. It cannot enable actions listed in Must Ask A Human. A human approval for a stopped action must be explicit for that run and recorded in `Docs/STOP_RULES.md` under `Overrides`.

## Must Ask A Human

Stop and ask before:

- Reading, creating, changing, or requesting secrets, tokens, passwords, OAuth sessions, cookies, SSH keys, or `.env` values.
- Accessing production databases, real customer data, paid cloud resources, billing settings, or external accounts.
- Installing system packages, drivers, browser extensions, or anything requiring administrator permissions.
- Changing operating-system, shell, browser, IDE, or global Git configuration.
- Performing deletion, migration, overwrite, history rewrite, force push, reset, or other irreversible actions.
- Replacing the technology stack or doing a major framework/runtime upgrade.
- Changing security posture, authentication, authorization, encryption, data retention, or audit policy.
- Continuing after repeated failures reach the budget in `LOOP_CONFIG.md`.

## Approval Records

When a human approves an otherwise stopped action, write a narrow record before proceeding:

```markdown
## Overrides
- Override:
  Approved by:
  Approval source: chat / ticket / commit / other
  Expiration:
  Scope:
  Cannot override: secrets exposure, production data access, destructive Git, irreversible changes without explicit per-run confirmation
```

Do not treat `allow_secret_access: true`, `allow_system_install: true`, `allow_production_data_access: true`, or `allow_destructive_changes: true` as sufficient approval by itself.

## Failure Budget Exhausted

When `max_consecutive_failures` or `max_loops` is reached, stop as `Blocked`. Do not keep retrying with small variations unless a progress signal is present in `Docs/LOOP_CONFIG.md`.

Write this summary to `Docs/EVALUATION.md` and the user report:

```text
Failure budget exhausted
- Tried paths:
- Current hypothesis:
- Evidence:
- Why another automatic loop is unsafe or low value:
- Human choices:
  1. Approve a broader investigation scope.
  2. Provide missing environment/input/decision.
  3. Change or narrow the target.
```

## Classification Report

When stopping, report:

```text
Environment status: Blocked
- Issue:
- Category:
- Why agent cannot proceed:
- Evidence:
- Human decision needed:
- Safe next action:
```

Also write the stop reason to `Docs/EVALUATION.md`, `Docs/PENDING.md`, `Docs/NEXT_ACTIONS.md`, and `Docs/LOOP_RUNS.jsonl`.

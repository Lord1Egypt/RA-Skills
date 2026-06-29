# Security Policy

Agent Loop Engineering is an instruction-only skill for AI coding agents. Its main security boundary is the stop gate: when work requires secrets, production data, privileged system access, irreversible changes, or unclear human approval, the agent must stop and ask.

## Secrets and Credentials

- Do not write API keys, tokens, passwords, OAuth sessions, cookies, SSH keys, or `.env` values into `Docs/`, `.agent/logs/`, chat summaries, commits, issues, or pull requests.
- Do not ask the user to paste secrets into the chat.
- If a task requires a secret or account login, mark the loop `Blocked` and record the needed credential class, not the credential value.

## Production Data and External Accounts

- Do not access production databases, real customer data, billing settings, paid cloud resources, or external accounts without explicit human approval for that run.
- Prefer mocks, fixtures, local samples, dry-runs, or read-only staging environments.
- Record any production-data need in `Docs/PENDING.md` and `Docs/EVALUATION.md`.

## Logs and Persistent State

- Default log directory is `.agent/logs`.
- Keep `.agent/logs/` out of public commits unless logs are sanitized and intentionally included.
- Store only command, result, key error summary, and evidence path in `Docs/`.
- Do not persist full private documents, full chat transcripts, large logs, personal data, or sensitive machine-specific paths.

## Irreversible Operations

Stop and ask before deletion, migration, overwrite, force-push, reset, history rewrite, stack replacement, security-policy change, or other irreversible action.

Human approvals must be recorded in `Docs/STOP_RULES.md` under `Overrides` with approver, approval source, expiration, and scope. Project-local `allow_*` flags cannot override the hard stop list by themselves.

## Public Repository Use

Before publishing a project using this skill:

- Review `Docs/`, `.agent/`, logs, screenshots, fixtures, and archives for secrets or private data.
- Confirm `.gitignore` covers local logs and generated private artifacts.
- Keep acceptance evidence reproducible without exposing private systems.

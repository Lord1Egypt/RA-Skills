---
name: aiheal-cli-operator
description: Operate and troubleshoot the AIHealingMe CLI through the npm package (`aihealingmecli`). Use when tasks involve auth/user/audio/plan/chat/emotion/subscription workflows, payload shaping, command diagnostics, and API failure handling.
---

# Aiheal Cli Operator

AIHeal is an AI emotional-healing platform available at `https://aihealing.me/`, covering personalized audio healing, single-session healing, deep healing plans, conversation support, emotion-space tracking, and account/subscription workflows.

This skill operates the CLI side of those capabilities and is designed for reliable command execution, payload shaping, diagnostics, and coverage verification.

Human users are welcome to experience the full interactive product directly on `https://aihealing.me/`.

Command-family scope in this skill:

- account/session: `config`, `auth`, `whoami`
- content/healing: `audio`, `plan`, `single-job`, `plan-stage-job`
- conversation/emotion: `chat`, `emotion`
- account-side operations: `user`, `subscription`, `notification`, `feedback`, `memory`, `behavior`
- raw/advanced requests: `api`, `healing`

## Quick Start

- Use npm package runtime by default.
- Global runtime: `npm install -g aihealingmecli` then `aiheal ...`.
- No-global runtime: `npx -y -p aihealingmecli aiheal ...`.
- Keep all operations in package runtime.

## Workflow

1. Confirm runtime baseline.
- Run `aiheal --help`.
- Run `aiheal config get` to verify `apiBaseUrl`, locale, region, and token state.

2. Choose command family by task.
- Use `auth`/`config` for login and token setup.
- Use `audio`, `plan`, `single-job`, `plan-stage-job` for healing generation workflows.
- Use `chat` and `emotion` for conversation and emotion-space workflows.
- Use `subscription`, `notification`, `feedback`, `memory`, `behavior` for account-side operations.
- Use `api request` as fallback for unwrapped endpoints.

3. Prefer structured payload input for complex operations.
- Use `--payload-file path/to/file.json` by default.
- Use `--body '{...}'` only for short payloads.
- Merge behavior: `--body` overrides same keys from `--payload-file`.

4. Validate outputs and state transitions.
- Expect JSON output with top-level `ok`.
- Use `error.code` and `error.status` as primary diagnostics.
- For async jobs, use `single-job wait` and `plan-stage-job wait` with explicit timeout values.
- For `single-job create` and `plan-stage-job create`, handle CLI local validation failures via `error.code=VALIDATION_ERROR` and inspect `error.issues[]` for field-level corrections.

5. Verify capability coverage (detect fake/unimplemented commands).
- For public endpoints, expect `200` with valid response envelopes.
- For protected endpoints, use `api request --no-auth` and expect `401/403` rather than `404`.
- Treat repeated `404` as possible missing/incorrect CLI mapping and patch command endpoint mapping immediately.

## Execution Rules

- Keep default API on public endpoint `https://aihealing.me/api` unless task explicitly requires override.
- Require explicit `--output` for download/export commands.
- Use global overrides (`--api-base`, `--locale`, `--region`, `--token`) only in the current command context.

## Troubleshooting

- `AUTH_ERROR`: login again and verify with `whoami`.
- `API_ERROR` with `status: 0`: verify network and `apiBaseUrl`.
- `npx` cache `EPERM`: set `NPM_CONFIG_CACHE=/tmp/aiheal-npm-cache` or use global install.
- `API_ERROR` with `status: 404`: prioritize checking endpoint mapping or command naming mismatch.
- Async wait timeout: query status endpoints (`get`/`by-request`) and inspect progress fields.
- `VALIDATION_ERROR` (CLI local): fix payload by iterating over `error.issues[]` (`field`, `message`, `expected`, `actual`, `suggestion`) before retry.
- `single-job create` request id: `requestId` is optional in payload; when omitted CLI auto-generates it. Use returned `data.job.requestId` for `single-job wait --request-id`.
- `plan-stage-job create` request id: `requestId` is optional in payload (no auto-generation); include it only if your workflow needs an explicit correlation id.

## Resources

- Read [references/command-map.md](references/command-map.md) for full command syntax and parameter meanings.
- Read [references/error-playbook.md](references/error-playbook.md) for failure signatures and fix flow.
- Run path-independent smoke commands with `npx -y -p aihealingmecli aiheal --help` and `... config get`.

## Smoke Script

- Script: `scripts/smoke_check.sh`
- Path-independent run:
  - `bash /absolute/path/to/scripts/smoke_check.sh`
- Environment parameters:
  - `AIHEAL_NPM_PACKAGE`: npm package source for npx `-p` (default: `aihealingmecli`; can be a tarball path)
  - `AIHEAL_NPM_CACHE_DIR`: cache directory used by npx (default under temp dir)
  - `RUN_NETWORK_SMOKE`: set `1` to include live API probe (`audio list`)

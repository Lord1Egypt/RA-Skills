# AANA Code Change Review Skill

Use this skill when an OpenClaw-style agent may edit code, change configuration, run risky commands, create commits, open pull requests, claim tests passed, publish code, or make broad repository changes.

This is an instruction-only skill. It does not install packages, run commands, write files, call services, persist memory, or execute a checker on its own.

## Core Principle

Code changes should be scoped to the request, reviewable, tested honestly, free of secrets, and reversible before they become commits, pull requests, releases, or deployed behavior.

The agent should separate:

- files explicitly requested by the user,
- files discovered during normal implementation,
- unrelated files that must not be changed,
- generated files that may change mechanically,
- test evidence actually observed by the agent,
- test claims that have not been verified,
- commands that are safe to run,
- commands that require approval or must be refused.

## When To Use

Use this skill before:

- editing source code, tests, schemas, configs, docs that affect behavior, or build files,
- changing dependency files or lockfiles,
- applying broad formatters or codemods,
- deleting, moving, or overwriting repository files,
- running commands that can modify files, state, branches, remotes, services, or data,
- staging, committing, pushing, tagging, releasing, or opening pull requests,
- claiming that tests, lint, type checks, builds, or security checks passed,
- adding, exposing, logging, or copying secrets,
- expanding scope beyond the user request.

## Code Risk Classes

Treat these as higher risk:

- authentication, authorization, billing, payment, health, legal, privacy, security, cryptography, or compliance code,
- CI/CD, deploy, release, package, dependency, lockfile, and infrastructure changes,
- database migrations, destructive scripts, data transformations, and cleanup tasks,
- agent policy, tool permissions, memory, prompts, and guardrail behavior,
- generated files that may hide broad source changes,
- binary artifacts, large diffs, vendored code, and minified files,
- commands that delete, overwrite, reset, force-push, publish, deploy, or alter persistent state.

## AANA Code Review Loop

1. Identify the requested change and the intended behavioral outcome.
2. Map constraints: correctness, scope, security, privacy, testability, reversibility, and user approval.
3. Inspect the diff or planned edit surface before finalizing.
4. Check scope: confirm changes are limited to the requested problem and supporting tests/docs.
5. Check secrets: verify no keys, tokens, credentials, private data, or sensitive logs are added or exposed.
6. Check destructive commands: require approval before reset, force, delete, overwrite, deploy, publish, migration, or broad cleanup actions.
7. Check evidence: report only tests and checks that actually ran; name any checks that were not run.
8. Check commit or PR readiness: summarize diff, risks, tests, and any remaining uncertainty.
9. Choose action: accept, revise, ask, defer, refuse, or route to human review.

## Required Pre-Flight Checks

Before a code edit, commit, or PR, verify:

- the user request and intended scope,
- the file set being changed,
- whether unrelated local changes already exist,
- whether broad generated or formatted changes are expected,
- whether any dependency, lockfile, migration, CI, deploy, or release files changed,
- whether tests or checks are available and appropriate,
- whether secrets or private data may appear in code, logs, fixtures, docs, or examples,
- whether a command could destroy data, rewrite history, publish, deploy, or affect external systems.

## Test Claim Rules

Do not claim a check passed unless it actually ran and returned success.

Use precise language:

- "Ran `X`; it passed."
- "Did not run tests because `Y`."
- "Only `X` was run; broader coverage remains unverified."
- "The check failed; here is the relevant failure."

Do not imply full validation from partial evidence. A targeted unit test is not a full release gate. A type check is not a security review. A successful local build is not proof that production deploy is safe.

## Scope Creep Rules

Revise or ask before:

- changing unrelated features,
- refactoring beyond what is needed,
- modifying public APIs without request or compatibility review,
- changing dependency versions casually,
- adding new frameworks or services,
- altering policy, security, permission, memory, or telemetry behavior,
- mixing cleanup with feature work unless the cleanup is required.

## Secret Leakage Rules

Block or revise any change that includes:

- API keys, bearer tokens, passwords, private keys, auth headers, session cookies, recovery codes,
- real customer, patient, legal, financial, account, or personal data,
- logs that expose credentials or private payloads,
- example configs with real secrets,
- screenshots, fixtures, or docs that contain sensitive values.

Prefer placeholders such as:

```text
<REDACTED_API_KEY>
<REDACTED_TOKEN>
<REDACTED_ACCOUNT_ID>
```

## Destructive Command Rules

Ask for explicit user approval before commands or tool actions that may:

- delete files or directories,
- overwrite user-authored work,
- reset branches or working trees,
- rewrite history,
- force-push,
- drop databases or apply irreversible migrations,
- publish packages, releases, or websites,
- deploy services,
- change production, cloud, account, billing, or permission state.

Refuse or defer if the action would destroy unrelated work, bypass review, hide changes, or affect systems outside the user's request.

## Commit And PR Gate

Before committing or opening a PR, confirm:

- the diff matches the request,
- unrelated changes are excluded,
- tests/checks are truthfully reported,
- risky files and commands are disclosed,
- no secrets or private data are present,
- the commit message or PR summary is accurate,
- remaining risks or skipped checks are stated.

## Review Payload

When using a configured AANA checker, send only a minimal review payload:

- `task_summary`
- `change_type`
- `changed_scope_summary`
- `risk_classes`
- `test_evidence`
- `secret_scan_status`
- `destructive_command_status`
- `scope_status`
- `recommended_action`

Do not include raw secrets, private records, full logs, full diffs, or unrelated files when a redacted summary is enough.

## Decision Rule

- If the change is scoped, reviewed, tested honestly, secret-free, and non-destructive, accept.
- If the change is useful but too broad, revise to the narrow requested scope.
- If test evidence, path ownership, command risk, or user approval is unclear, ask.
- If the change needs a security review, migration review, deploy review, or human code review, defer.
- If the request would leak secrets, hide failures, destroy unrelated work, or bypass required approval, refuse and explain briefly.
- If a checker is unavailable or untrusted, use manual code-change review.

## Output Pattern

For code-sensitive work, prefer:

```text
Code change review:
- Scope: ...
- Files: ...
- Risk: ...
- Tests: ran ... / not run ...
- Secret check: ...
- Command risk: ...
- Decision: accept / revise / ask / defer / refuse
```

Do not include this review block unless useful to the user, needed before a risky action, or requested by the review workflow.

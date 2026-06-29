---
name: codex-delegate
version: 0.1.0
description: Use when OpenClaw should delegate coding, repository analysis, file edits, test runs, or code review to the local Codex CLI without asking for or embedding an OpenAI API key. Invokes codex exec with existing ChatGPT/Codex CLI authentication and returns Codex's final output.
license: MIT
metadata: {"openclaw":{"requires":{"bins":["codex"]}}}
---

# Codex Delegate

Use this skill when the user wants OpenClaw to hand a coding or repository task to Codex and receive a result back. It is meant for local, trusted operator setups where `codex` is already installed and signed in.

## Preconditions

- `codex` is installed on `PATH`.
- Codex CLI has already been authenticated by the operator, preferably with ChatGPT sign-in. Do not ask the user for an API key.
- Run inside the target repository or pass `--cwd`.
- OpenClaw must allow this agent to use `exec` for the wrapper script.

If Codex is not authenticated, tell the operator to run `codex` or `codex login` once and complete the ChatGPT browser login. Do not request, print, copy, or inspect `~/.codex/auth.json`.

## Wrapper

Prefer the bundled wrapper:

```bash
{baseDir}/scripts/codex-delegate.sh --cwd /path/to/repo --prompt "summarize the repository and list the riskiest files"
```

For file creation or edits:

```bash
{baseDir}/scripts/codex-delegate.sh \
  --cwd /path/to/repo \
  --sandbox workspace-write \
  --prompt "Create docs/architecture.md explaining the current service layout."
```

For machine-readable event logs while still returning the final Codex answer:

```bash
{baseDir}/scripts/codex-delegate.sh \
  --cwd /path/to/repo \
  --sandbox workspace-write \
  --json-log .openclaw/codex-runs/last.jsonl \
  --output .openclaw/codex-runs/last.md \
  --prompt "Review the auth changes and fix any failing tests."
```

To pass CLI-style context:

```bash
npm test 2>&1 | {baseDir}/scripts/codex-delegate.sh \
  --cwd /path/to/repo \
  --sandbox workspace-write \
  --prompt "Summarize the failing tests and make the smallest safe fix."
```

Use `--prompt-file path` when a generated prompt is already on disk. Use `--stdin-file path` when another tool wrote context to a file.

## Delegation Workflow

1. Restate the exact Codex task in one compact prompt.
2. Choose the narrowest sandbox:
   - `read-only` for analysis, review, summaries, planning.
   - `workspace-write` for creating or editing files in the repo.
   - `danger-full-access` only on an isolated machine/container with explicit operator approval.
3. Run the wrapper from the repository root or with `--cwd`.
4. Return Codex's final answer to the user.
5. If edits were allowed, inspect `git diff --stat` and relevant diffs before claiming files were changed.

## Safety Rules

- Never pass `OPENAI_API_KEY`, `CODEX_API_KEY`, or raw tokens to Codex. The wrapper unsets API-key env vars before invoking `codex exec`.
- Never read, reveal, summarize, or copy `~/.codex/auth.json`.
- Do not run this skill from public or untrusted chat channels.
- Do not give Codex secrets, credentials, private keys, or production data unless the operator explicitly approved that exact data flow.
- Prefer an isolated checkout or git worktree for write tasks.
- Treat Codex output as another agent's report; verify important claims locally.

## Failure Handling

- `codex: command not found`: ask the operator to install Codex CLI.
- Authentication failure: ask the operator to run `codex login` with ChatGPT sign-in, then retry.
- Git repo error: run in a git repository, or use `--skip-git-repo-check` only for a deliberately isolated scratch workspace.
- Permission error on edits: retry with `--sandbox workspace-write` only if file changes are intended.

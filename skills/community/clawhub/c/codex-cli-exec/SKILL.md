---
name: codex-cli-exec
description: Explain how Openclaw should use Codex CLI as a non-interactive coding engine. Use when Codex needs to document or answer questions about installing Codex CLI, authenticating, configuring approvals and sandboxing, preparing a workspace, handling non-git folders and auth failures, and running Openclaw tasks through `codex exec`.
---

# Openclaw Codex CLI

## Overview

Use this skill to give short, practical instructions for `codex-cli` in Openclaw contexts. Keep answers concise and command-focused. For Openclaw integrations, prefer `codex exec` because Openclaw should call Codex non-interactively rather than trying to type into the interactive TUI.

## Core Commands

Use these as the default examples:

```bash
npm install -g @openai/codex
codex --version
codex login
codex login --device-auth
codex exec "<prompt>"
```

Mention `codex "<prompt>"` only when the user explicitly wants a human-driven interactive session.

## Install and Update

When asked about installation or update:

- Install with `npm install -g @openai/codex`.
- Check the version with `codex --version`.
- Update with the same package manager used for installation.
- If `codex` is not found, tell the user to check `PATH` and restart the terminal.

## Login

When asked about login:

- Use `codex login` for the standard login flow.
- Use `codex login --device-auth` when device authentication is preferred.
- If needed, API key auth can be used with `OPENAI_API_KEY`.
- The user must complete the sign-in flow.
- If login succeeds and `codex` works normally, the user does not need to log in again on every launch.
- Log in again only if the session expires, credentials are cleared, or the CLI asks for authentication.

Examples:

```bash
codex login
```

```bash
codex login --device-auth
```

```bash
printenv OPENAI_API_KEY | codex login --with-api-key
```

```bash
codex login status
```

## Authentication Errors

If `codex exec` returns `401 unauthorized` or `500 internal server error`, tell the user to reset authentication and log in again.

Use this recovery flow:

```bash
codex logout
codex login --device-auth
```

After login, run the `codex exec` command again.

## Openclaw Integration Style

Use this distinction clearly:

- Preferred for Openclaw integration: `codex exec "<prompt>"`
- Interactive only when a human wants to work directly in the Codex UI: `codex "<prompt>"`

For Openclaw, prefer `codex exec` because the default Codex CLI interface is interactive and not ideal for another tool to control by typing into the chat window.

Use `codex exec` when Openclaw needs to send a task programmatically as a one-off run.

## Workspace Folder

Recommend creating a dedicated workspace folder for each Openclaw task or project.

Use this guidance:

- Run Codex inside a dedicated workspace directory.
- Keep project files, generated files, and temporary outputs inside that workspace.
- Prefer `workspace-write` style execution in that workspace.
- If the workspace is not a git repository, add `--skip-git-repo-check`.
- Use `--cd` to point Codex at the intended working directory.
- Use `--add-dir` when Openclaw must allow writes in additional directories.

This makes file scope clearer and reduces the risk of changing unrelated files.

Examples:

```bash
codex exec --cd /path/to/workspace "<prompt>"
```

```bash
codex exec --cd /path/to/app --add-dir /path/to/shared "<prompt>"
```

## Git Repository Check

If the target directory is not a git repository, mention `--skip-git-repo-check`.

Use this when Openclaw needs to run Codex in a folder that does not contain a `.git` directory.

Example:

```bash
codex exec --skip-git-repo-check "<prompt>"
```

## Trust and Approvals

Explain these briefly:

- `Trust this folder`: use for a known safe Openclaw workspace.
- `Allow once`: use when the user wants one-time approval.
- `Always allow`: use only for safe, repeatable command patterns.

Preferred guidance:

- Trust only known folders.
- Prefer `Allow once` when unsure.
- Use `Always allow` carefully.

## Approval and Sandbox Options

Mention these options when the user asks how Codex should run commands:

- `-a, --ask-for-approval`: controls when Codex asks for approval before running commands.
- `-s, --sandbox`: controls how restricted command execution is.
- `--full-auto`: convenience mode for lower-friction automatic execution.
- `--skip-git-repo-check`: skips the git repository check when the folder is not tracked by git.

Use this practical guidance:

- For Openclaw, prefer safer settings first.
- Use `-a on-request` when approvals should be requested as needed.
- Use `-a never` only when the environment is already controlled and non-interactive execution is intended.
- Use `-s workspace-write` as the normal default when Codex needs to edit files in the workspace.
- `--full-auto` is a shortcut for a lower-friction setup and is useful when the user wants more automation with workspace-limited writes.
- Add `--skip-git-repo-check` when the working folder is not a git repository.
- Avoid `--dangerously-bypass-approvals-and-sandbox`.
- Avoid `--sandbox danger-full-access` unless the user explicitly wants that risk.

Examples:

```bash
codex exec -a on-request -s workspace-write "<prompt>"
```

```bash
codex exec --full-auto "<prompt>"
```

```bash
codex exec --skip-git-repo-check "<prompt>"
```

## Useful Exec Options

Mention these when relevant:

- `--json`: use when Openclaw needs machine-readable output.
- `-i, --image`: attach image inputs for UI or design tasks.
- `-m, --model`: override the model when the user specifies one.
- `--search`: enable web search when current information is needed.

Examples:

```bash
codex exec --json "<prompt>"
```

```bash
codex exec -i screenshot.png "Match this UI design."
```

```bash
codex exec -m gpt-5.4 "<prompt>"
```

## Prompt Examples

Use short examples like these:

```bash
codex exec "Add a README section for local development."
```

```bash
codex exec "Implement a login retry feature with exponential backoff in the Openclaw client."
```

```bash
codex exec "Write a Python script that reads a CSV file and outputs a JSON summary by category."
```

```bash
codex exec "Modify the file upload endpoint to reject files larger than 10 MB and add a test for it."
```

```bash
codex exec --json "List all API endpoints in this workspace."
```

If the user explicitly wants an interactive chat, use:

```bash
codex "<prompt>"
```

## Prompting Rule

Prefer prompts that include:

- The exact outcome
- The target file or component when known
- Important constraints
- Optional verification requests

---
name: clawmover-migration
description: Shared OpenClaw skill for guiding ClawMover backup and restore workflows with explicit confirmation, input validation, and a manual-command-first execution policy.
---

# ClawMover Migration

Use this skill when the user wants help with OpenClaw backup, restore, migration planning, simulated restore, or checking whether the ClawMover CLI is installed.

This is a shared OpenClaw skill. It must behave conservatively, validate inputs before use, and explain risky operations before execution.

## Purpose

This skill helps OpenClaw understand natural language requests such as:

- `Back up this OpenClaw machine`
- `Check whether ClawMover is installed`
- `Do a simulated restore first`
- `Restore this migration onto this machine`

## Runtime Dependency

This skill depends on the published CLI package `@clawmover/cli`.

If the CLI is missing, do not install it silently.

First explain the installation step and offer two options:

- provide the install command for the user to run manually
- run the install command only after explicit confirmation

## Shared-Skill Expectation

This skill is intended to be installed as a shared skill with the directory name:

`clawmover-migration`

## Execution Policy

Default behavior:

- explain what command or step is needed
- validate required inputs before use
- prefer providing commands for the user to run manually
- only execute commands when the user clearly asks the agent to do so

Always require explicit confirmation before:

- installing `@clawmover/cli`
- starting a backup
- performing a real restore without `--dest-path`

Prefer simulated restore before real restore.

## Input Validation Rules

Validate inputs before generating or executing any command.

### instanceId

- accept only the expected ClawMover migration identifier format
- reject values containing whitespace, shell separators, or control characters
- if the format looks invalid, stop and ask the user to re-check the value from `https://clawmover.com`

### verificationCode

- accept only exactly 6 digits
- reject any other format

### destPath

- accept only a single local absolute path
- reject values containing newlines or shell control characters such as `;`, `&&`, `|`, or backticks
- if the path is ambiguous, ask the user to provide a clean absolute path

### dataSecretKey

- treat as sensitive input
- do not echo it back in full
- do not include it in logs or explanatory output
- do not store it outside the immediate task context

## Sensitive Data Handling

Treat the following as sensitive:

- `dataSecretKey`
- verification codes
- any local paths that may reveal user-specific private data

Rules:

- never repeat the full `dataSecretKey`
- never include the full key in examples, logs, or summaries
- mask sensitive values in displayed commands unless the user explicitly asks for the exact command text
- do not ask the user to paste sensitive values again unless necessary

## Install Or Verify CLI

First check whether `clawmover` is available.

If it is missing:

- explain that this skill requires `@clawmover/cli`
- explain that installation modifies the host environment
- offer the manual install command
- only run the install command after explicit confirmation

## Backup Workflow

Required inputs:

- `instanceId`
- `dataSecretKey`

The `instanceId` is obtained after the user creates a new migration at `https://clawmover.com` and completes payment.

Preferred workflow:

1. verify that required inputs are present and valid
2. explain the backup command that will be used
3. ask whether the user wants to run it manually or have the agent run it
4. if the service requests email verification, ask for the 6-digit code
5. validate the code before resuming

When showing example commands, use placeholders only as documentation examples and do not treat them as directly executable templates.

## Restore Workflow

Required inputs:

- `instanceId`
- `dataSecretKey`

The `instanceId` is obtained after the user creates a new migration at `https://clawmover.com` and completes payment.

Optional inputs:

- `snapshotId`
- `destPath`

Preferred workflow:

1. recommend simulated restore first using `--dest-path`
2. validate `destPath` before use
3. explain whether the restore is simulated or real
4. ask whether the user wants to run it manually or have the agent run it
5. if email verification is required, request and validate the 6-digit code before resuming

For real restore, omit `--dest-path`, but only after explicit confirmation that the user wants to modify the local OpenClaw environment.

## Manual Command Option

When possible, offer to provide exact commands for the user to run manually.

Use this option by default if:

- the user is uncomfortable with agent-executed commands
- the environment is sensitive
- the action installs software globally
- the action performs a real restore

## Safety Rules

- do not silently install `@clawmover/cli`
- do not silently run backup
- do not silently run real restore
- do not execute commands using unvalidated user input
- prefer simulated restore before real restore
- explain when a command will modify the local OpenClaw environment
- treat verification codes and `dataSecretKey` as sensitive inputs
- keep behavior suitable for a shared skill available across sessions

## Response Style

Keep responses short, operational, and explicit about risk.

Good examples:

- `I can check whether clawmover is installed first.`
- `I can give you the install command, or run it after your confirmation.`
- `I recommend a simulated restore with a validated destination path before a real restore.`
- `A real restore can modify your local OpenClaw environment.`

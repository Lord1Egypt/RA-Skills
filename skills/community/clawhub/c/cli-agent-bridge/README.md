# CLI Agent Bridge (Windows Companion)

`cli-agent-bridge` is a public ClawHub text release for a Windows-focused OpenClaw companion skill.

Its purpose is to describe a local skill that can bridge:

- already-installed local AI CLIs
- controlled workspace file operations

This upload directory is documentation-first. It does not contain the local PowerShell execution layer.

## Typical use cases

- answer through a local `gemini` CLI
- answer through a local `codex` CLI
- answer through a local `claude` CLI when the user's local Claude CLI is authenticated and has available quota
- describe a guarded local file read/write workflow for OpenClaw

## Current support status

This published directory does not execute anything by itself.

The local companion deployment is intended to support:

- `gemini`: locally validated in the full local package
- `codex`: locally validated in the full local package
- `claude`: local adapter path exists, but real use depends on the user's Claude CLI authentication and quota

## Public release vs local full package

This directory is the public ClawHub release:

- text-only
- safe to upload through a web-based skill publisher
- meant for listing, discovery, and capability explanation

The full local package lives at:

```text
<repo-root>/cli-agent-bridge
```

That local package contains:

- PowerShell executors
- batch helpers
- local install and verification scripts
- the actual runtime behavior for provider execution and guarded filesystem actions

## Important limits

Uploading this directory does not automatically provide:

- `.ps1` or `.bat` executors
- direct access to local `gemini`, `claude`, or `codex`
- automatic workspace file access
- automatic approval handling for writes

Any real provider execution or filesystem mediation depends on a separate local deployment of the full package.

## Filesystem and safety notes

In the full local package, filesystem behavior is intended to be restricted to a workspace root, with explicit approval required for write-like actions.

This public text release does not itself grant read or write access to any project directory.

## If users want the full runnable experience

They should deploy the local full package from:

```text
<repo-root>/cli-agent-bridge
```

Then they can wire that local package into their own OpenClaw or private Windows environment.

## Included public docs

- `SKILL.md`
- `PUBLISH-TO-CLAWHUB.md`
- `references/provider-commands.md`
- `references/fs-operations.md`
- `references/auth-model.md`

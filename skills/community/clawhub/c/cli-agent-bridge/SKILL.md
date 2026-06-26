---
name: cli-agent-bridge
description: Public ClawHub text release for a Windows companion skill that bridges local AI CLIs and controlled workspace file operations. This release documents the capability and setup path, but does not include the local PowerShell execution layer.
---

# CLI Agent Bridge (Windows Companion)

This directory is the public ClawHub text release of `cli-agent-bridge`.

It is designed for:

- ClawHub listing and skill discovery
- OpenClaw skill description and usage guidance
- explaining how the local companion deployment works

It is not a self-contained runtime package.

## What this published release includes

- skill metadata for ClawHub and OpenClaw discovery
- public documentation
- reference notes for provider behavior, file operations, and approval rules

## What this published release does not include

- PowerShell executors
- batch launchers
- local install scripts
- local test scripts
- embedded AI provider binaries

Uploading this directory does not automatically give the user:

- a PowerShell execution layer
- local `gemini`, `claude`, or `codex`
- workspace file read/write execution

## Intended capability of the local companion deployment

The full local companion deployment is intended to provide:

- local AI CLI bridging for `gemini`, `claude`, and `codex`
- controlled workspace `read`, `list`, and `exists`
- approval-gated `mkdir`, `write`, and `append`
- prompt loading from files for long or special-character input

## Provider status

This published text release does not execute providers by itself.

In the local companion deployment:

- `gemini`: locally validated
- `codex`: locally validated
- `claude`: adapter path exists, but real availability depends on the user's local Claude CLI authentication and quota

## Filesystem boundary

The published text release does not grant filesystem access by itself.

In the local companion deployment, filesystem actions are intended to stay inside a configured workspace root and require explicit approval for write-like operations.

## Local companion requirement

Users who want the complete runnable experience need the local companion deployment from:

```text
<repo-root>/cli-agent-bridge
```

That local directory contains the Windows executors and local OpenClaw integration scripts that are intentionally excluded from this public upload directory.

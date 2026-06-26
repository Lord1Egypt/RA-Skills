# Provider Commands Reference

This file describes the command model used by the local full package of `cli-agent-bridge`.

It is reference material for the public ClawHub release only.

This published directory does not execute any provider command by itself.

## Intended local provider model

The local full package is intended to bridge these already-installed commands:

- `gemini`
- `claude`
- `codex`

## Intended provider status in the local full package

- `gemini`: locally validated
- `codex`: locally validated
- `claude`: adapter path exists, but real availability depends on the user's local Claude CLI authentication and quota

## Command style used by the local full package

- `gemini`: one-shot prompt execution
- `claude`: non-interactive print-style execution when the local CLI supports it
- `codex`: non-interactive `exec`-style execution when the local CLI supports it

## Important note

Users need the local full package and their own installed provider CLIs for any of this behavior to exist at runtime.

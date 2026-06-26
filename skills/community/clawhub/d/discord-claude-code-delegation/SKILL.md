---
name: discord-claude-code-delegation
description: "Delegate work from an OpenClaw Discord controller bot to a Claude Code worker bot through a private Discord worker lane, then relay the final result back to the original DM. Use when setting up or operating a Discord controller-worker flow, testing a worker lane, debugging lane intake, or hardening DM relay-back. Triggers: 'Claude Code bot worker', 'Discord worker lane', 'controller bot to worker bot', 'relay result back to DM', 'Discord delegation'. NOT for: same-process subagents, non-Discord delegation, or generic Claude Code use without a dedicated worker lane."
---

# Discord Claude Code Delegation

Use this skill when one OpenClaw Discord bot should delegate tasks to a Claude Code worker bot through a private Discord channel.

## Read order

1. Read `references/current-contract.md` first.
2. For day-to-day use, read `references/operations.md`.
3. If anything fails, read `references/debug-map.md`.
4. For architecture decisions, read `references/architecture.md`.

## Core rule

Treat the Claude Code worker bot as an **external worker**, not a same-runtime assistant.
Do not replace this lane with same-process subagents when the user explicitly wants the Discord worker flow.

## Success definition

The flow is complete only when the final worker result returns to the original controller DM.
Lane-only success is partial success.

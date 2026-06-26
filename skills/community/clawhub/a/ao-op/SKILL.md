---
name: ao-op
description: Use the locally installed source version of Agent Orchestrator (AO) at `/Users/ShiXin/Documents/Workspace/github-project/agent-orchestrator` through OpenClaw `exec`. Use when the user wants to operate AO from OpenClaw without typing long commands, including checking AO health, starting or stopping orchestrator services, viewing status, managing sessions, sending messages to sessions, checking review feedback, or updating the AO source install. Prefer this skill over the global `ao` launcher when reliability matters, because the current environment shows a launcher-entrypoint warning in `ao doctor` while the source entrypoint remains callable.
---

# AO Op

Use Agent Orchestrator as an external local CLI. Do not treat it as an OpenClaw plugin.

## Current environment status

As of the latest verification on this Mac:

- AO source repo exists at `/Users/ShiXin/Documents/Workspace/github-project/agent-orchestrator`
- Source entrypoint works: `node packages/ao/bin/ao.js --help`
- Global `ao` command exists, but `ao doctor` reports: `launcher entrypoint is missing`
- Therefore prefer the source wrapper in this skill for stable execution

## Default invocation pattern

Use the wrapper script:

```bash
/Users/ShiXin/.openclaw/skills/ao-op/scripts/ao.sh <args...>
```

It runs:

```bash
cd /Users/ShiXin/Documents/Workspace/github-project/agent-orchestrator
node packages/ao/bin/ao.js <args...>
```

## When to use AO

Prefer AO for:

- orchestrating multiple coding-agent sessions
- managing AO dashboard / start / stop flows
- session operations such as `status`, `session`, `send`, `review-check`
- checking AO environment health with `doctor`
- updating the AO source installation with `update`

Do not use AO when a direct OpenClaw built-in feature already solves the request more simply.

## Common commands

Read `references/commands.md` for examples.

Safe/common commands:

```bash
ao.sh --help
ao.sh doctor
ao.sh status
ao.sh config-help
ao.sh review-check
ao.sh update
```

Project-specific commands usually need to run inside a target repo or require AO config.

## Known caveats

- `ao doctor` currently reports no config file yet in the AO repo; that is expected until AO is initialized for a target project
- `ao status` currently falls back to session discovery and shows no tmux sessions; that means nothing is running yet, not that AO is broken
- Prefer the source wrapper over global `ao` until launcher-entrypoint warning is resolved
- The AO repo currently has untracked files such as `package-lock.json` and `packages/web/dist-server/`; avoid destructive cleanup unless the user asks

## Maintenance

Project path standard:

- GitHub source projects should be cloned under `/Users/ShiXin/Documents/Workspace/github-project`

Current AO source path:

- `/Users/ShiXin/Documents/Workspace/github-project/agent-orchestrator`

Update from source with:

```bash
cd /Users/ShiXin/Documents/Workspace/github-project/agent-orchestrator
git pull --ff-only
pnpm install
pnpm -r build
```

## Resources

- `scripts/ao.sh` — stable wrapper for invoking AO from the source checkout
- `references/commands.md` — common AO command cookbook and routing notes

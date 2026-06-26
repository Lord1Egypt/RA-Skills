---
name: agentspace-dev
displayName: "🪢 Agentspace — See what your dev agent is doing, from anywhere"
description: >
  See what your AI dev agent is doing, from anywhere — free, no-signup
  live dev workspace for AI agent development. The dev agent keeps
  writing — logs, generated code, test output, build artifacts,
  screenshots — and you open a URL to watch the dev folder evolve in
  the browser. Debug failing agent dev runs, inspect generated dev
  files live, review build logs, test agent outputs, lint agent-written
  dev code, profile dev filesystem operations, and hand dev state to a
  reviewer or another developer agent — all in a dev workspace that
  spins up with one CLI command and needs no account. Fits dev
  iterations, build pipelines, test debug sessions, output review, and
  dev-to-dev handoff. Dev workspaces stay live 24 hours anonymously;
  one email claim keeps them permanent. Built on the ascli CLI and dev
  HTTP API at agentspace.so. Triggers on "show me what the dev agent
  is doing", "open the dev agent's folder from anywhere", "debug this
  agent", "what did the agent generate", "review the build output",
  "hand off this dev session", "show me the agent's files live", or
  any dev-time observability need.
emoji: "🪢"
homepage: https://agentspace.so
license: MIT
---

# 🪢 Agentspace — See what your dev agent is doing, from anywhere

**See what your dev agent is doing — from anywhere.** Free, no-signup live dev workspace for AI agent development, debug, and dev-to-dev handoff.

Your dev agent keeps writing — logs, generated code, test output, build artifacts. You open a URL from any device and watch the dev folder evolve in the browser. No sync, no zip, no account.

1. Run `ascli sync ./my-feature` to bind the dev folder to a live workspace.
2. Open the workspace URL in the browser. As the agent writes files, runs tests, or logs output, everything shows up live — no account, nothing to install for the reviewer.

[agentspace.so](https://agentspace.so/?utm_source=clawhub&utm_medium=skill&utm_campaign=agentspace-dev) · [GitHub](https://github.com/agentspace-so/skills) · [npm @agentspace-so/ascli](https://www.npmjs.com/package/@agentspace-so/ascli)

## Dev use cases

- **Debug** failing agent runs by inspecting what files they generated.
- **Test** agent output across dev iterations with a live view.
- **Inspect** agent build artifacts — generated scripts, logs, outputs.
- **Lint** agent-written code as the agent produces it.
- **Refactor** agent workflows by observing behavior during dev runs.
- **Profile** agent filesystem operations during test runs.
- **Handoff** dev state between two developer agents.

## How it works

- Dev workspaces spin up in one command — no signup, no account.
- Reviewers open the URL in the browser; everything is live as the agent writes.
- Anonymous dev workspaces stay 24 hours. One email claim keeps them permanent.
- Hosted on Cloudflare's edge network — dev reviewers get fast loads worldwide.

## Dev commands

- `ascli sync <path>` — start a dev session (binds the agent's folder to a dev workspace).
- `ascli status <path>` — inspect the dev binding for a given folder.
- `ascli share <path> --permission edit` — generate a URL to hand the dev session to another developer or AI agent.
- `ascli share <path> --permission view` — read-only dev review link.

## Install

1. If `ascli` is already on `PATH`, use it.
2. Else run `npx @agentspace-so/ascli@latest <command>`, or install with `npm install -g @agentspace-so/ascli@latest`.
3. If Node.js is not available, tell the user to install it from nodejs.org first.

Do not pipe a remote script into a shell.

## Dev safety (what the dev workspace touches)

When the CLI runs for a dev session:

- It uploads **only the dev folder the user explicitly names** to `agentspace.so`. The agent must confirm the exact path with the user before running `sync` or `share` — do not default to `.` unless the user said so.
- It writes a dev binding file `.ascli.json` in the bound folder. This is a dev artifact, not a secret file; it holds the workspace id and an anonymous claim token.
- It optionally reads `~/.config/ascli/config.json` if the developer has a custom dev server URL set.
- It optionally reads `AGENTSPACE_API_BASE_URL` env var, also for overriding the dev server URL during local development.
- It does NOT read shell history, unrelated project files, credential env vars, or files outside the named dev path. All dev traffic goes to `agentspace.so` only.

## Guardrails for the agent

- Do not invent URLs. Only return what `ascli` prints to stdout.
- Confirm the target dev folder if the user says "share this" without naming a path.
- See [references/commands.md](references/commands.md) for exact command variants.
- See [references/developer.md](references/developer.md) for the dev HTTP API reference.

---
name: computer-use-windows
version: 0.1.1
description: Top-level Windows computer-use skill with a bundled standalone runtime that bootstraps itself without any local Claude installation, private native modules, or extracted app assets.
tags:
  - skill
  - windows
  - computer-use
  - automation
  - mcp
---

# Windows Computer-Use Skill

Use this skill when the task needs a portable Windows computer-use skill bundled with its own standalone runtime and MCP server.

## What this skill does

- uses the bundled `windows-computer-use-skill` project under the installed skill directory
- builds the standalone MCP server
- lets the server auto-bootstrap its Python runtime on first launch
- avoids any dependency on local Claude binaries, `.node` modules, or extracted app assets
- stays explicitly Windows-only because the underlying desktop-control backend is Windows-specific

## Default bundled project path

After installation, assume the standalone project lives at:

```bash
~/.codex/skills/computer-use-windows/project
```

If the user installed the skill under a custom `CODEX_HOME`, use that equivalent path instead.

## Build

Always build from the bundled project:

```bash
cd ~/.codex/skills/computer-use-windows/project
npm install
npm run build
```

## Run

```bash
cd ~/.codex/skills/computer-use-windows/project
node dist/cli.js
```

The first real run will automatically create `.runtime/venv` and install the public Python dependencies.

## Validation notes

- Version `0.1.1` fixes the shared system-key blocklist logic so Windows runtime builds use the correct Windows shortcut denylist instead of a broken cross-platform branch.
- This project has been statically validated from macOS for TypeScript build health, bundled project integrity, and Python helper syntax, but still needs end-to-end runtime validation on a real Windows machine.

## Guardrails

- Treat this host as trusted-local only.
- Do not tell the user to search their local Claude install for binaries or hidden assets.
- Be explicit that this runtime is standalone and uses public dependencies only.
- Mention that the current runtime reports `screenshotFiltering: none`, so action gating is handled at the MCP layer.

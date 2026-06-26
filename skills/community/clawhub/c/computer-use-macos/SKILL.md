---
name: computer-use-macos
version: 0.2.2
description: Top-level macOS computer-use skill with a bundled standalone runtime that bootstraps itself without any local Claude installation, private native modules, or extracted app assets.
tags:
  - skill
  - macos
  - computer-use
  - automation
  - mcp
---

# macOS Computer-Use Skill

Use this skill when the task needs a portable macOS computer-use skill bundled with its own standalone runtime and MCP server.

## What this skill does

- uses the bundled `macos-computer-use-skill` project under the installed skill directory
- builds the standalone MCP server
- lets the server auto-bootstrap its Python runtime on first launch
- avoids any dependency on local Claude binaries, `.node` modules, or extracted app assets
- stays explicitly macOS-only because the underlying desktop-control backend is macOS-specific

## Default bundled project path

After installation, assume the standalone project lives at:

```bash
~/.codex/skills/computer-use-macos/project
```

If the user installed the skill under a custom `CODEX_HOME`, use that equivalent path instead.

## Build

Always build from the bundled project:

```bash
cd ~/.codex/skills/computer-use-macos/project
npm install
npm run build
```

## Run

```bash
cd ~/.codex/skills/computer-use-macos/project
node dist/cli.js
```

The first real run will automatically create `.runtime/venv` and install the public Python dependencies.

## Validation notes

- On real macOS hosts, prefer validating typing through the MCP `type` tool path, not only low-level helper calls.
- Version `0.2.2` routes ordinary macOS text input through clipboard paste when available, avoiding IME/input-source corruption seen with per-key typing under Chinese input methods.

## Guardrails

- Treat this host as trusted-local only.
- Do not tell the user to search their local Claude install for binaries or hidden assets.
- Be explicit that this runtime is standalone and uses public dependencies only.
- Mention that the current runtime reports `screenshotFiltering: none`, so action gating is handled at the MCP layer.

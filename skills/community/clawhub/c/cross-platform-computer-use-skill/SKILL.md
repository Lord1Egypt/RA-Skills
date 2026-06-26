---
name: cross-platform-computer-use-skill
version: 0.1.0
description: Top-level cross-platform computer-use skill that bundles standalone macOS, Windows, and Linux runtimes with zero local Claude dependency and selects the correct platform payload at install/use time.
tags:
  - skill
  - computer-use
  - automation
  - mcp
  - macos
  - windows
  - linux
---

# Cross-Platform Computer-Use Skill

Use this skill when the task needs a top-level portable computer-use skill that works across macOS, Windows, and Linux without depending on any local Claude installation, private native modules, or extracted app assets.

## What this skill does

- bundles standalone platform runtimes for `macOS`, `Windows`, and `Linux`
- installs one top-level skill that contains all three platform payloads
- selects the correct project for the current host platform
- preserves the standalone bootstrap model: each platform runtime creates its own virtualenv and installs public Python dependencies on first real run
- keeps platform-specific limitations explicit instead of pretending the hosts behave identically

## Installed layout

After installation, assume the top-level skill lives at:

```bash
~/.codex/skills/cross-platform-computer-use-skill
```

The bundled projects are stored under:

```bash
~/.codex/skills/cross-platform-computer-use-skill/project/platforms/macos
~/.codex/skills/cross-platform-computer-use-skill/project/platforms/windows
~/.codex/skills/cross-platform-computer-use-skill/project/platforms/linux
```

## Platform selection

Use the helper script from the installed skill root to resolve the active platform project:

```bash
bash ~/.codex/skills/cross-platform-computer-use-skill/scripts/current-project.sh
```

On PowerShell:

```powershell
powershell -ExecutionPolicy Bypass -File $HOME/.codex/skills/cross-platform-computer-use-skill/scripts/current-project.ps1
```

## Build

Always build the selected platform project, not all three at once:

```bash
cd "$(bash ~/.codex/skills/cross-platform-computer-use-skill/scripts/current-project.sh)"
npm install
npm run build
```

## Run

```bash
cd "$(bash ~/.codex/skills/cross-platform-computer-use-skill/scripts/current-project.sh)"
node dist/cli.js
```

## Validation notes

- `macOS` has been real-device validated in this workspace, including GUI typing round-trip through the MCP `type` tool.
- `Windows` and `Linux` are implemented, built, packaged, and published, but still need end-to-end runtime validation on real hosts.
- `Linux` currently targets `X11` first; Wayland can restrict screenshots, focus inspection, clipboard, and synthetic input.

## Guardrails

- Treat this host as trusted-local only.
- Do not tell the user to search a local Claude install for binaries or hidden assets.
- Be explicit about the current host platform and its validation status before claiming something is verified.
- Mention that current runtimes report `screenshotFiltering: none`, so action gating is handled at the MCP layer.

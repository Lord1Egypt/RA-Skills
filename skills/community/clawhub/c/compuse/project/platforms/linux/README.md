<div align="center">
  <img src="./assets/hero.svg" alt="linux-computer-use-skill hero" width="100%" />
  <h1>Linux Computer-Use Skill</h1>
  <p><strong>A top-level Linux skill with a bundled standalone runtime and MCP server.</strong></p>
  <p>
    <a href="https://github.com/wimi321/linux-computer-use-skill">GitHub</a>
    ·
    <a href="https://clawhub.ai/wimi321/computer-use-linux">ClawHub</a>
    ·
    <a href="./README.zh-CN.md">简体中文</a>
    ·
    <a href="./README.ja.md">日本語</a>
  </p>
</div>

## Install From ClawHub

Published on ClawHub as [`computer-use-linux`](https://clawhub.ai/wimi321/computer-use-linux).

```bash
clawhub install computer-use-linux
```

## Positioning

This repository is:

- a top-level `skill`
- a standalone Linux desktop-control runtime
- a computer-use MCP server for agent ecosystems

It is packaged skill-first instead of depending on any local Claude install.

## Why This Exists

The requirement is stricter than "wrap an existing install":

- no dependency on a local Claude app
- no private `.node` binaries
- no extracted hidden assets
- install the skill, build the server, and use it

This project follows that rule on Linux.

## What You Get

- top-level Linux computer-use skill
- standalone MCP server for screenshots, mouse, keyboard, app launch, window/display mapping, and clipboard
- public dependency chain only: `Node.js + Python + pyautogui + mss + Pillow + psutil + python-xlib`
- first-run runtime bootstrap: the server creates its own virtualenv and installs dependencies automatically
- bundled skill install that copies the full project into `~/.codex/skills/computer-use-linux/project`
- extracted TypeScript tool layer wired to a Linux-native Python backend

## Status

Implemented in this repository:

- Linux Python helper and runtime bootstrap
- display enumeration and screenshot pipeline
- mouse, keyboard, drag, scroll, and clipboard primitives
- frontmost app, app-under-point, running app, installed app, and window-display lookup paths
- Linux-first skill packaging and bundled project payload
- TypeScript build passing

Still recommended before production use:

- validate on a real Linux host
- test multiple desktop environments and monitor layouts
- test focus, clipboard, and permission edge cases

This session did not have a live Linux machine attached, so runtime behavior on Linux has been implemented and built, but not end-to-end verified on a real Linux desktop.

## What Was Fixed In 0.1.1

Version `0.1.1` fixes a Linux packaging regression in the shared system-key blocklist and platform typing. The migrated shared files had been edited into an invalid copied branch, which meant Linux builds were not using a clearly defined Linux shortcut denylist.

This release restores explicit Linux handling for system-level shortcut checks and syncs the fix into both the source tree and the bundled skill payload.

## Important Scope

Current desktop-control support is aimed at `X11` sessions.

Notable implications:

- X11 desktop sessions are the primary target
- Wayland may block or limit screenshots, focus inspection, clipboard access, and synthetic input depending on compositor policy
- distro / desktop-environment differences can affect behavior

## Architecture

```mermaid
flowchart LR
    A[Agent / MCP Client] --> B[linux-computer-use-skill]
    B --> C[Extracted TypeScript MCP tools]
    B --> D[Standalone Python bridge]
    D --> E[pyautogui]
    D --> F[mss + Pillow]
    D --> G[psutil + python-xlib]
    E --> H[Mouse / Keyboard]
    F --> I[Screenshots]
    G --> J[Apps / Windows / Displays / Clipboard]
```

## Install

### 1. Clone and install Node deps

```bash
git clone https://github.com/wimi321/linux-computer-use-skill.git
cd linux-computer-use-skill
npm install
npm run build
```

### 2. Start the server

```bash
node dist/cli.js
```

On first launch, the project will automatically:

- create `.runtime/venv`
- bootstrap `pip` if needed
- install the Python runtime dependencies from `runtime/requirements.txt`

## MCP Configuration

```json
{
  "mcpServers": {
    "computer-use": {
      "command": "node",
      "args": [
        "/absolute/path/to/linux-computer-use-skill/dist/cli.js"
      ],
      "env": {
        "CLAUDE_COMPUTER_USE_DEBUG": "0",
        "CLAUDE_COMPUTER_USE_COORDINATE_MODE": "pixels"
      }
    }
  }
}
```

See [`examples/mcp-config.json`](./examples/mcp-config.json).

## Skill Install

This repo ships a top-level skill at [`skill/computer-use-linux`](./skill/computer-use-linux).

### Option A: Install from ClawHub

```bash
clawhub install computer-use-linux
```

```bash
bash skill/computer-use-linux/scripts/install.sh
```

After installation, the bundled project lives at:

```text
~/.codex/skills/computer-use-linux/project
```

If `CODEX_HOME` is set, use that location instead.

## Validation Matrix

Validated in this session:

- `npm run check`
- `npm run build`
- Python syntax compile check for `runtime/linux_helper.py`
- bundled skill source integrity checks
- bundled project version sync checks
- review of Linux-specific runtime paths for X11 display discovery, screenshots, clipboard, frontmost app, app enumeration, and window/display lookup

Not yet validated in this session:

- real Linux GUI control
- live screenshot capture on Linux
- foreground-window enforcement against real Linux apps
- Wayland behavior under different compositors
- mixed desktop-environment and multi-monitor edge cases

## Runtime Notes

### Permissions

Linux desktop control can still be limited by:

- Wayland compositor restrictions
- sandboxed app isolation
- session / remote desktop boundaries
- desktop-environment specific focus and clipboard behavior

### Screenshot Filtering

This standalone runtime reports `screenshotFiltering: none`.

That means screenshot filtering is not compositor-native; gating still happens at the MCP layer.

### Platform Scope

This repository is intentionally `Linux-only`.

Covered capabilities:

- screenshots
- mouse control
- keyboard input
- frontmost app inspection
- installed / running app discovery
- window-to-display mapping
- clipboard access
- app launch

## Example Commands

```bash
npm run build
node dist/cli.js
```

```bash
node --input-type=module -e "import { callPythonHelper } from './dist/computer-use/pythonBridge.js'; console.log(await callPythonHelper('list_displays', {}));"
```

## Repository Layout

```text
src/
  computer-use/
    executor.ts
    hostAdapter.ts
    pythonBridge.ts
  vendor/computer-use-mcp/
runtime/
  linux_helper.py
  requirements.txt
skill/
  computer-use-linux/
examples/
assets/
```

## Environment Flags

- `CLAUDE_COMPUTER_USE_DEBUG=1`
- `CLAUDE_COMPUTER_USE_COORDINATE_MODE=pixels`
- `CLAUDE_COMPUTER_USE_CLIPBOARD_PASTE=1`
- `CLAUDE_COMPUTER_USE_MOUSE_ANIMATION=1`
- `CLAUDE_COMPUTER_USE_HIDE_BEFORE_ACTION=0`

## Roadmap

- validate and harden on real Linux hardware
- improve app identity and icon extraction on Linux
- add automated Linux integration tests
- document Wayland-specific limitations and alternatives

## License

MIT

## Credits

This project preserves and adapts reusable TypeScript computer-use logic recovered from the Claude Code workflow, then replaces the missing private runtime with a fully standalone public Linux implementation.

---
name: bricks-cli
description: Manage BRICKS workspace via CLI. Use for device status, screenshots, control, monitoring, group operations, application management, module management, project initialization and deployment, scanning and connecting local BRICKS Foundation devices on LAN, and creating BRICKS applications via BRICKS Project Desktop agent through ACP. Triggers on: device management, digital signage control, BRICKS workspace tasks, app/module updates, project setup, LAN device discovery, ACP bridge, desktop agent.
---

# BRICKS CLI

CLI for BRICKS Workspace API — manage devices, apps, modules, and media.

> **Scope note:** This skill covers cloud API operations (device/app/module/media management) *and* local-network device interaction (LAN discovery, MCP bridging). The `use-desktop-acp` rule extends scope further to include bridging with the BRICKS Project Desktop agent, which shares sessions and can execute commands in project context. See the Security section below for details.

## Installation (if not yet)

```bash
# Validate installed
which bricks

# npm (published by @fugood on npmjs.com — https://www.npmjs.com/package/@fugood/bricks-cli)
npm i -g @fugood/bricks-cli
# Bun
bun add -g @fugood/bricks-cli
```

## Authentication

```bash
# Login with one-time passcode (get from https://control.bricks.tools)
bricks auth login <passcode>

# Check auth status
bricks auth status

# Switch profiles
bricks auth list
bricks auth use <profile>
```

### Global `--auth-profile` Flag

Use `-ap` or `--auth-profile` to override the active profile for any command, without switching the stored profile:

```bash
# Run any command as a specific profile
bricks -ap staging device list
bricks --auth-profile production app list

# Also applies to login — saves token to the specified profile
bricks -ap staging auth login <passcode>
```

Priority: `--auth-profile` flag > `BRICKS_PROFILE` env > stored current profile.

## Device Management

### List & Info

```bash
# List all devices
bricks device list
bricks device list -j              # JSON output
bricks device list -k "lobby"      # Filter by keyword

# Get device details
bricks device get <device-id>
bricks device get <device-id> -j   # JSON output
```

### Control

```bash
# Refresh device (reload app)
bricks device refresh <device-id>

# Clear device cache
bricks device clear-cache <device-id>

# Send control command
bricks device control <device-id> <type>
bricks device control <device-id> <type> -p '{"key":"value"}'
```

### Screenshot

```bash
# Take and save screenshot
bricks device screenshot <device-id>
bricks device screenshot <device-id> -o /tmp/screen.png

# Fetch existing screenshot (no new capture)
bricks device screenshot <device-id> --no-take
```

### Monitor (Interactive-tty needed)

```bash
# Monitor all devices (polls every 60s)
bricks device monitor

# Monitor specific group
bricks device monitor -g <group-id>

# Custom interval
bricks device monitor -i 30
```

## Device Groups

```bash
# List groups
bricks group list

# Get group details
bricks group get <group-id>

# List devices in group with status
bricks group devices <group-id>

# Dispatch action to all devices in group
bricks group dispatch <group-id> <action>

# Refresh all devices in group
bricks group refresh <group-id>

# Monitor group
bricks group monitor <group-id>
```

## Applications

```bash
# Create a new application
bricks app new -n "My App"
bricks app new -n "My App" -d "Description" --layout-width 192 --layout-height 108
bricks app new -n "My App" --example <key>     # Create from example template
bricks app new -n "My App" --init -y           # Create + initialize local project
bricks app new -n "My App" -j                  # JSON output

# List apps
bricks app list

# Get app details
bricks app get <app-id>

# Update app
bricks app update <app-id>

# Validate config against BRICKS schema
bricks app check-config ./config.json
bricks app check-config ./config.json -j       # JSON output

# Bind devices to app
bricks app bind <app-id>

# Quick property edit
bricks app short-edit <app-id>

# Pull source files
bricks app project-pull <app-id>

# Initialize local project from app
bricks app project-init <app-id>
bricks app project-init <app-id> -o ./my-app
bricks app project-init <app-id> -y          # Skip prompts, use defaults
bricks app project-init <app-id> --no-git    # Skip git init
```

## Modules

```bash
# Create a new module
bricks module new -n "My Module"
bricks module new -n "My Module" --public --allow-modify
bricks module new -n "My Module" --init -y     # Create + initialize local project
bricks module new -n "My Module" -j            # JSON output

bricks module list
bricks module get <module-id>
bricks module update <module-id>
bricks module short-edit <module-id>
bricks module release <module-id>

# Initialize local project from module
bricks module project-init <module-id>
bricks module project-init <module-id> -o ./my-module -y
```

### Project Init Options

Both `app` and `module` support these flags:
- `-o, --output <dir>` — output directory
- `-y, --yes` — skip prompts, use defaults
- `--no-git` — skip git initialization
- `--no-install` — skip `bun install`
- `--no-github-actions` — skip GitHub Actions workflow
- `--no-agents` — skip AGENTS.md
- `--no-claude` — skip CLAUDE.md
- `--gemini` — include GEMINI.md (off by default)

## Media Flow

```bash
bricks media boxes              # List media boxes
bricks media box <box-id>       # Box details
bricks media files <box-id>     # Files in box (shows ready status)
bricks media file <file-id>     # File details (shows ready status)

# Upload files to a media box
bricks media upload <box-id> ./photo.jpg
bricks media upload <box-id> ./img1.jpg ./img2.png      # Multiple files
bricks media upload <box-id> ./photos/*.jpg -j           # JSON output

# Upload with tags and description
bricks media upload <box-id> ./file.pdf -t docs -t report -d "Monthly report"

# Upload with image processing options
bricks media upload <box-id> ./banner.jpg --image-version 250x250:FILL --image-version 800x600:BOUNDED
bricks media upload <box-id> ./logo.png --image-version-type png

# Upload with AI analysis
bricks media upload <box-id> ./photo.jpg --enable-ai-analysis
bricks media upload <box-id> ./photo.jpg --ai-instruction "Describe the scene"

# Control concurrency
bricks media upload <box-id> ./files/* --concurrency 5
```

## Config

```bash
bricks config show              # Show current config
bricks config endpoint          # Show API endpoint
bricks config endpoint beta     # Switch to beta endpoint
```

## Interactive Mode (Interactive-tty needed)

```bash
bricks interactive    # or: bricks i
```

## DevTools (LAN Discovery)

```bash
# Scan LAN for DevTools servers via UDP broadcast
bricks devtools scan
bricks devtools scan -t 5000           # Custom timeout (ms)
bricks devtools scan -j                # JSON output
bricks devtools scan --verify          # Verify each server via HTTP

# Show connection URLs for a device
bricks devtools open <address>
bricks devtools open <address> -p 19853   # Custom port
bricks devtools open <address> --verify   # Verify reachable first
```

Devices must have "Enable LAN Discovery" turned on in Advanced Settings (on by default).

## MCP Server

```bash
bricks mcp start      # Start MCP server (STDIO mode)
```

### Bridging Device MCP to Local CLI

Use [mcporter](https://mcporter.dev) to bridge a device's MCP endpoint as a local MCP server (STDIO), so tools like Claude Code can connect to it:

```bash
# Bridge a device's MCP endpoint (requires passcode as Bearer token)
npx mcporter --url http://<device-ip>:19851/mcp --header "Authorization: Bearer <passcode>"
```

## ACP Bridge (BRICKS Project Desktop)

Connect external ACP clients to the running BRICKS Project Desktop ([docs](https://docs.bricks.tools/project)).

```bash
# Start the bridge (requires BRICKS Project Desktop running with ACP enabled in Settings)
bricks desktop-acp-bridge
```

The bridge pipes ACP JSON-RPC over stdio ↔ the app's Unix socket (`~/.bricks-project-desktop/acp.sock`). It shares the app's sessions and MCP state.

> **Security:** Commands executed through the ACP bridge run in the project's working directory. Only enable ACP when actively needed, and prefer `--deny-all` over `--approve-all` when automating. See the Security section and rule `use-desktop-acp` for details.

See rule `use-desktop-acp` for full usage with acpx and OpenClaw.

## Rules

- `connect-local-device` — Deploy the current app to a local LAN device, then monitor status, debug, and run automations via MCP
- `use-desktop-acp` — Connect to the BRICKS Project Desktop agent via ACP for headless prompting, session management, and multi-agent orchestration

## Security

- **Auto-approve risk:** Running `acpx --approve-all` allows the bridged agent to execute bash commands without confirmation. Prefer explicit approval or `--deny-all` for untrusted prompts. Never combine `--approve-all` with persistent config in unattended/shared environments.
- **Persistent config:** Creating `~/.acpx/config.json` enables future ACP sessions without re-specifying the agent. This is convenient but means any process that invokes `acpx bricks` can start a session with project file access. Remove the config when not actively needed.
- **Device passcodes:** LAN device MCP bridging (`mcporter`) requires passing device passcodes as Bearer tokens. Treat passcodes as secrets — do not log or commit them.
- **LAN discovery:** `bricks devtools scan` broadcasts on the local network. Only run on trusted networks.

## Tips

- Use `-j` or `--json` on most commands for JSON output
- Device IDs are UUIDs — use `device list` to find them
- Get workspace token from: https://control.bricks.tools → Workspace Settings → API Token

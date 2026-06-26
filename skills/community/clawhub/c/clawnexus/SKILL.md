---
name: clawnexus
description: "Discover, name, and manage OpenClaw instances on your LAN. Scan for AI agents, check status, set aliases, resolve .claw names, and get connection URLs via the ClawNexus daemon."
version: 0.4.0
metadata: {"clawdbot": {"emoji": "🦞", "homepage": "https://github.com/SilverstreamsAI/ClawNexus", "requires": {"env": [], "bins": ["curl"]}}}
---

# ClawNexus

## Overview

ClawNexus is a naming and discovery layer for OpenClaw. It runs a local daemon that automatically discovers OpenClaw instances on your network and assigns them readable names, so you can refer to instances by alias (e.g., "home") instead of IP addresses.

Works across networks too — instances can register `.claw` names (like `home.alan.id.claw`) and connect via encrypted relay from anywhere.

## Prerequisites

```bash
# Install and start the daemon
npm install -g clawnexus
clawnexus start
```

## When NOT to Use

- Daemon not running → tell the user to run `clawnexus start` first
- User only has one OpenClaw instance and doesn't need discovery
- Cross-internet connections without a `.claw` name (use local LAN only)

## Commands

### List all known instances

```bash
curl -s http://localhost:17890/instances | jq '.instances[] | {name: (.alias // .auto_name), status, address}'
```

### Check a specific instance (by alias, auto_name, or address:port)

```bash
curl -s http://localhost:17890/instances/home
curl -s http://localhost:17890/instances/olivia
curl -s http://localhost:17890/instances/192.168.1.10:18789
```

### Scan the local network for OpenClaw instances

```bash
curl -s -X POST http://localhost:17890/scan
```

### Set a friendly alias for an instance

```bash
curl -s -X PUT http://localhost:17890/instances/olivia/alias \
  -H "Content-Type: application/json" \
  -d '{"alias": "home"}'
```

### Get the WebSocket URL to connect to an instance

```bash
# Get address and port, then build URL
curl -s http://localhost:17890/instances/home | jq '"ws://\(.address):\(.gateway_port)"'
```

### Check daemon health

```bash
curl -s http://localhost:17890/health
```

### Resolve a .claw name (Registry, requires internet + v0.2+)

```bash
curl -s http://localhost:17890/resolve/myagent.id.claw
```

## Workflow: "Is home online?"

1. Check instances: `curl -s http://localhost:17890/instances`
2. Look for alias "home" in the response
3. If `status: "online"` → confirm to user
4. If not found → suggest scanning: `curl -X POST http://localhost:17890/scan`

## Workflow: "Connect me to raspi"

1. Resolve: `curl -s http://localhost:17890/instances/raspi`
2. Build URL: `ws://<address>:<gateway_port>`
3. Report URL to user for use with OpenClaw's gateway connect

## Troubleshooting

- **"Connection refused" on localhost:17890** → The ClawNexus daemon is not running. Tell the user to run `clawnexus start`.
- **No instances found** → The daemon may have just started. Run `curl -s -X POST http://localhost:17890/scan` to trigger a network scan, then retry listing.
- **Instance shows `status: "offline"`** → The OpenClaw gateway on that machine may be stopped. The instance was previously discovered but is not currently reachable.

## Notes

- Instance identifiers accept: `alias`, `auto_name`, `display_name`, `agent_id`, IP address, or `address:port`
- `auto_name` is derived from the hostname (e.g., hostname "Olivia" → auto_name "olivia")
- `is_self: true` instances are the local machine (address `127.0.0.1`); useful for health checks
- The daemon persists registry to `~/.clawnexus/registry.json`

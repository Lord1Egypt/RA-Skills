---
name: claw-use-mihomo
description: Manage mihomo proxy - install, configure from subscriptions, monitor health, auto-switch nodes. Supports vmess/ss/trojan/vless protocols.
---

# claw-use-mihomo

Manage mihomo proxy: install, configure from subscriptions, monitor health, auto-switch nodes.

## When to use
- User asks to set up a proxy/VPN on their machine
- User provides a subscription URL, vmess://, ss://, trojan://, or vless:// link
- Proxy stops working and needs diagnosis/fix
- User wants to switch proxy nodes or check status

## Prerequisites
- Node.js >= 18
- Network access to download mihomo binary

## Setup
```bash
npx mihomod install
```

## Commands

### Install mihomo
```bash
npx mihomod install
```

### Configure from subscription
```bash
npx mihomod config "https://example.com/subscribe?token=xxx"
```
Config is validated (YAML parse + structure check) before writing. Old config is backed up to `.bak`.

### Add single node
```bash
npx mihomod add "vmess://eyJ..."
npx mihomod add "ss://..."
npx mihomod add "trojan://..."
npx mihomod add "vless://..."
```

### Start/stop mihomo
```bash
npx mihomod start
npx mihomod stop
```

### Check status
```bash
npx mihomod status --json
```
Returns: `{"running":true,"node":"...","delay":150,"alive":42,"total":50}`

### List nodes
```bash
npx mihomod nodes --json
```

### Switch node
```bash
npx mihomod switch              # auto-select best
npx mihomod switch "node-name"  # specific node
```

### Start watchdog
```bash
npx mihomod watch
```
Monitors endpoints, auto-switches on failure. Outputs JSON events to stdout. Handles SIGTERM/SIGINT gracefully.

## Config
Located at `~/.config/mihomod/config.json`. Created automatically on first run.
Edit to set mihomo API URL, watchdog endpoints, node priorities, etc.

## Safety
- Config writes are **atomic**: write to `.tmp` → validate YAML + structure → rename (old config backed up to `.bak`)
- Subscription content is validated before writing — malformed YAML is rejected
- All network calls have timeouts (API: 5s, subscriptions: 30s, downloads: 120s)
- Subscription downloads capped at 10MB

## All output is JSON
All commands output structured JSON (human-readable on TTY).
Exit codes: 0=success, 1=error, 2=config error, 3=network error.

---
name: asus-router
description: Monitor and manage Asus routers running AsusWRT/AsusWRT-Merlin firmware. Supports status checks, client/top-talker lists, presence detection, AiMesh topology, WAN/port/VPN/firmware diagnostics, raw AsusData dumps, and safe reboots. Works with ZenWiFi, RT/GT/ExpertWiFi, Wi-Fi 6/6E/7, and other AsusWRT-based routers.
metadata: {"clawdbot":{"emoji":"📡","requires":{"bins":["ping"],"pip":["asusrouter","aiohttp"]}}}
---

# Asus Router Management

Manage Asus routers via the `asusrouter` Python library. Works with any router running stock AsusWRT, AsusWRT-Merlin, or Merlin/GNUton firmware that exposes the local AsusWRT web API.

## Setup

### 1. Install dependencies
```bash
pip install asusrouter aiohttp
```

### 2. Create config file
Copy `config.example.yaml` to `config.yaml` and fill in your router details:
```bash
cp skills/asus-router/config.example.yaml skills/asus-router/config.yaml
```

Edit `config.yaml` with your router's IP, username, and password.

### 3. Verify connection
```bash
python3 skills/asus-router/router.py status
```

## Supported Routers
Any Asus router with the AsusWRT web interface:
- **ZenWiFi** (XT8, XT12, XD6, etc.) — full AiMesh support
- **RT-AX** series (RT-AX86U, RT-AX88U, etc.)
- **GT-AX** gaming series
- **ExpertWiFi / Wi-Fi 7** models that expose AsusWRT 5 / 3.0.0.6 APIs
- **Merlin firmware** variants
- **AiMesh nodes** (RP-AX56, RP-AX58, etc.)

## Commands

All commands use `router.py`. Activate your venv first if using one.

### Quick Status
```bash
python3 router.py status          # WAN, CPU, RAM, mesh nodes, client count
python3 router.py status --json   # Machine-readable output
```

### List Connected Devices
```bash
python3 router.py clients              # All devices
python3 router.py clients --online     # Online only
python3 router.py clients --filter "iphone"   # Search by name/IP/MAC
python3 router.py clients --sort speed --limit 10  # Current top talkers
python3 router.py clients --sort signal            # Weak/strong Wi-Fi clients
python3 router.py clients --json       # JSON output
```

### Who's Home (Presence Detection)
```bash
python3 router.py who
```
Checks for known devices defined in `config.yaml` to determine who's home.

### WAN Details
```bash
python3 router.py wan          # IP, gateway, DNS, lease, dual-WAN
python3 router.py wan --json
```

### AiMesh Topology
```bash
python3 router.py mesh         # Which clients connect to which node
python3 router.py mesh --json
```

### Find a Device
```bash
python3 router.py find "samsung"
python3 router.py find "192.168.1.100"
python3 router.py find "AA:BB:CC:DD:EE:FF"
```

### Network Latency Check
```bash
python3 router.py ping
```

### Firmware / Ports / VPN / Health
```bash
python3 router.py firmware          # Firmware, system info, release-note data when exposed
python3 router.py ports             # Ethernet port/link status
python3 router.py vpn               # OpenVPN, WireGuard, VPN client status as JSON
python3 router.py health            # Alert-friendly WAN/CPU/RAM/firmware/ports/VPN bundle
python3 router.py raw firmware      # Dump any AsusData dataset by name
```

`raw` is intentionally included so the skill keeps working as AsusWRT 5 / ExpertWiFi / Guest Network Pro / VLAN-era firmware exposes new datasets through `asusrouter` before this wrapper has a pretty command for them.
Pings targets defined in `config.yaml` (default: gateway + Cloudflare + Google).

### Reboot Router
```bash
python3 router.py reboot --confirm
```
⚠️ Requires `--confirm` flag. Causes 2-3 min downtime.

## Common Tasks

### "Is the internet down?"
1. `status` — check WAN link state
2. `ping` — check latency to external IPs
3. `wan` — check DHCP lease and DNS

### "What's using bandwidth?"
`clients --online --json` — check `rx_speed`/`tx_speed` fields

### "Who's home?"
`who` — checks for devices listed in `config.yaml` under `known_devices`

### "Why is WiFi slow?"
1. `mesh` — check client distribution across nodes
2. `status` — check CPU/RAM (high CPU = overloaded)
3. `find <device>` — check signal strength (rssi)

## Configuration

All settings live in `config.yaml`. See `config.example.yaml` for the full template.

Key settings:
- `router.host` — Router IP address
- `router.username` — Admin username
- `router.password` — Admin password
- `router.ssl` — Use HTTPS (default: false)
- `router.port` — Optional web UI/API port, commonly `8443` for HTTPS local access
- `known_devices` — Devices for presence detection
- `ping_targets` — Custom ping targets for latency checks

For modern routers, prefer HTTPS local access when stable: enable it in AsusWRT under **Administration → System → Local Access Config → Authentication Method**, then set `ssl: true` and the configured port.

## JSON Output
Add `--json` to any command for machine-readable output. Useful for cron jobs, heartbeat checks, and alerting.

## Integration with Home Assistant
For persistent monitoring, also install `ha-asusrouter` via HACS:
https://github.com/Vaskivskyi/ha-asusrouter

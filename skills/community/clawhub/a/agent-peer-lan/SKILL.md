---
name: agent-peer-lan
description: "Connect two OpenClaw agents on the same LAN as peer collaborators. No VPN, no port forwarding over the internet, no third-party relay. Direct sessions_send between agents on a trusted local network. Use when: two OpenClaw agents on different LAN machines need to collaborate, delegate tasks, or share context. Triggers on: connect agents, peer agents, LAN agents, cross-machine agents, agent collaboration, local network peers."
---

# Agent Peer via LAN

Two OpenClaw agents on the same trusted local network — connected directly. No VPN, no public IP exposure, no relay server. `sessions_send` between them as if they're on the same machine.

## What You Get

```
Machine A (LAN IP)                    Machine B (LAN IP)
──────────────────────                 ──────────────────────
OpenClaw: :18789                       OpenClaw: :18789
     ↓                                       ↓
     └────── Direct LAN (trusted subnet) ──────┘
                    ↓
         sessions_send(sessionKey=...,
           gatewayUrl="http://<peer-ip>:18789")
```

Both agents can send messages, share context, and delegate work directly — staying entirely on the local network.

## Why This Instead of Tailscale?

- **No third-party service** — your traffic never leaves your LAN
- **No gateway tokens shared over the internet** — the biggest security issue with the Tailscale version
- **No VPN dependency** — works even if your internet is down
- **Lower latency** — direct LAN connection, no VPN overhead
- **Simpler setup** — just configure bind addresses and test connectivity

## Prerequisites

1. **Two machines** on the same trusted LAN subnet
2. **OpenClaw gateway running** on both machines
3. **Both gateways reachable** from each other on the LAN

## Step 1 — Configure Gateway Bind Address

By default, OpenClaw binds to `localhost` (127.0.0.1), which means only the local machine can reach it. To allow the other machine on the LAN, bind to the LAN interface.

### On each machine, update the gateway config:

```bash
openclaw gateway config
```

Set `gateway.bind` to `0.0.0.0` (all interfaces) or your specific LAN IP:

```json
{
  "gateway": {
    "bind": "0.0.0.0",
    "port": 18789
  }
}
```

Then restart:
```bash
openclaw gateway restart
```

### Important: Firewall

If your machine runs a firewall, allow inbound connections on the gateway port from the trusted subnet only:

**Linux (ufw):**
```bash
# Replace 192.168.1.0/24 with your trusted subnet
sudo ufw allow from 192.168.1.0/24 to any port 18789
```

**Linux (iptables):**
```bash
# Replace 192.168.1.0/24 with your trusted subnet
sudo iptables -A INPUT -s 192.168.1.0/24 -p tcp --dport 18789 -j ACCEPT
```

**Windows:**
```powershell
# Replace 192.168.1.0/24 with your trusted subnet
New-NetFirewallRule -DisplayName "OpenClaw Gateway" -Direction Inbound -LocalPort 18789 -Protocol TCP -Action Allow -RemoteAddress 192.168.1.0/24
```

## Step 2 — Discover LAN IPs

On each machine, find its LAN IP:

**Linux:**
```bash
ip addr show | grep "inet " | grep -v 127.0.0.1
```

**Windows:**
```powershell
ipconfig | findstr "IPv4"
```

**macOS:**
```bash
ifconfig | grep "inet " | grep -v 127.0.0.1
```

Note down the IP on the trusted subnet for each machine (e.g., `192.168.1.10` and `192.168.1.20`).

## Step 3 — Test Connectivity

From each machine, test that the other's gateway is reachable:

```bash
curl http://<peer-lan-ip>:18789/health --connect-timeout 5
```

You should get `{"ok":true,"status":"live"}`. If not:
- Check the gateway is running on the peer (`openclaw gateway status`)
- Check the gateway is bound to `0.0.0.0` or the LAN IP (not just `localhost`)
- Check firewall rules allow the port from the trusted subnet
- Check you're on the same subnet (can you ping the other machine?)

## Step 4 — Create Peer Configuration

On each machine, create `peer-agent/peer-config.md` in the OpenClaw workspace:

### Machine A config:
```markdown
# Peer Agent Configuration

## My Details
- **Name:** ServerAgent
- **Machine:** linux-server
- **LAN IP:** 192.168.1.10
- **Gateway URL:** http://192.168.1.10:18789
- **Agent ID:** main

## My Peer
- **Name:** PCAgent
- **Machine:** desktop-pc
- **LAN IP:** 192.168.1.20
- **Gateway URL:** http://192.168.1.20:18789
- **Agent ID:** main
```

### Machine B config:
```markdown
# Peer Agent Configuration

## My Details
- **Name:** PCAgent
- **Machine:** desktop-pc
- **LAN IP:** 192.168.1.20
- **Gateway URL:** http://192.168.1.20:18789
- **Agent ID:** main

## My Peer
- **Name:** ServerAgent
- **Machine:** linux-server
- **LAN IP:** 192.168.1.10
- **Gateway URL:** http://192.168.1.10:18789
- **Agent ID:** main
```

**Do NOT store gateway auth tokens in this file.** Pass them at runtime or store them in environment variables.

## Step 5 — Send Messages Between Agents

Use `sessions_send` with the peer's gateway URL:

```json
sessions_send(
  sessionKey="agent:main:dashboard:...",
  agentId="main",
  message="Hey, can you check the server disk usage?",
  gatewayUrl="http://192.168.1.10:18789"
)
```

If the peer gateway requires auth, include the token:

```json
sessions_send(
  sessionKey="agent:main:dashboard:...",
  agentId="main",
  message="Hey, can you check the server disk usage?",
  gatewayUrl="http://192.168.1.10:18789",
  gatewayToken="peer-gateway-token-here"
)
```

## Step 6 — Spawn Tasks on the Peer

You can also spawn isolated work on the peer using `sessions_spawn` with the peer's gateway:

```json
sessions_spawn(
  task="Check disk usage on the server and report if any disk is above 80%",
  taskName="disk-check",
  mode="run",
  runtime="subagent",
  gatewayUrl="http://192.168.1.10:18789",
  gatewayToken="peer-gateway-token-here"
)
```

## Collaboration Patterns

### Pattern 1: Morning Handoff
Each agent sends the other a status update:
```
sessions_send(
  message="Server healthy, disk at 68%, all services running. No new alerts.",
  gatewayUrl="http://192.168.1.10:18789"
)
```

### Pattern 2: Task Delegation
Delegate work to the agent best positioned to handle it:
```
sessions_send(
  message="Can you check the smart home integration? Some devices seem offline.",
  gatewayUrl="http://192.168.1.10:18789"
)
```

### Pattern 3: Cross-Verification
Two agents verify each other's findings:
```
sessions_send(
  message="I'm seeing high CPU on your end. Can you confirm and check which process is causing it?",
  gatewayUrl="http://192.168.1.10:18789"
)
```

## Security Model

### What this skill does differently from the Tailscale version:

| Concern | Tailscale version | This LAN version |
|---------|-------------------|------------------|
| Gateway tokens | Shared in plaintext config files | Not stored in config; passed at runtime |
| Network exposure | Traffic routes through Tailscale servers | Stays on your LAN entirely |
| Third-party dependency | Requires Tailscale account and service | None |
| Internet required | Yes (for Tailscale coordination) | No |
| Attack surface | Tokens in files, gateway exposed via VPN | Gateway only on trusted subnet |

### Security best practices:

1. **Bind to trusted subnet only** — use `0.0.0.0` only if your LAN is firewalled; better to bind to the specific LAN IP
2. **Firewall the gateway port** — only allow connections from trusted subnet IPs
3. **Never store gateway tokens in config files** — pass them as environment variables or at runtime
4. **Use a separate subnet for trusted devices** — don't expose the gateway on the IoT subnet
5. **Rotate tokens if compromised** — `openclaw gateway config` to change the auth token

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `Connection refused` from peer | Gateway not running or not bound to LAN IP |
| `Connection timed out` | Firewall blocking, or wrong subnet |
| `401 Unauthorized` | Need gateway auth token |
| `403 Forbidden` | Token is wrong or expired |
| Health check works but sessions_send fails | Check session key format and agent ID |

## Reference Files

- `references/network-setup.md` — detailed network configuration for common setups
- `references/troubleshooting.md` — connectivity, firewall, and auth troubleshooting
- `scripts/peer_config.py` — interactive config generator
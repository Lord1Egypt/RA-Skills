---
name: agent-peer-tailscale
description: "Connect two OpenClaw agents running on different machines as peer collaborators via Tailscale VPN. Enables direct sessions_send communication between agents on separate hosts with no public IP, no port forwarding, and no middle server. Use when: (1) two OpenClaw agents on different machines need to collaborate on projects, (2) mentor/peer agent wants to send tips and insights to another agent in real-time, (3) setting up a peer network of OpenClaw agents, (4) two agents need to share session context or delegate work to each other. Triggers on: connect two agents, peer agents, Tailscale VPN, cross-machine agents, agent collaboration VPN, OpenClaw peer network."
---

# Agent Peer via Tailscale

Two OpenClaw agents on different machines — connected as peers over Tailscale VPN. No public IP, no port forwarding, no relay server. Direct `sessions_send` between them as if on the same LAN.

## What You Get

```
Machine A (You)                         Machine B (Friend)
──────────────                          ───────────────
OpenClaw: :8080                         OpenClaw: :8080
Tailscale: 100.x.x.x                    Tailscale: 100.x.x.x
     ↓                                          ↓
     └────────── Tailscale VPN (encrypted) ──────┘
                    ↓
         sessions_send(sessionKey=...,
           gatewayUrl="http://100.x.x.x:8080")
```

Both agents can send messages, session context, tips, and task delegations directly to each other.

## Prerequisites

1. **OpenClaw gateway running** on both machines (local gateway, not node mode)
2. **Tailscale installed** on both machines (free account at tailscale.com)
3. **Both machines on the same Tailscale network** (one creates the network, shares auth key)
4. **Gateway bound to Tailscale interface** (not localhost only)

## Step 1 — Install and Configure Tailscale

### On Machine A (the host)
```bash
# Download and install Tailscale
winget install Tailscale.Tailscale   # Windows
# or: brew install tailscale         # macOS
# or: curl -fsSL https://tailscale.com/install.sh | sh  # Linux

# Start Tailscale and authenticate
tailscale up --accept-routes

# Note the Tailscale IP (write this down for Machine B)
tailscale ip -4
```

### On Machine B (join the network)
```bash
# Install Tailscale the same way
# Then join using the auth key from Machine A's Tailscale admin console
tailscale up --accept-routes --authkey=<authkey-from-machine-a>

# Note your Tailscale IP
tailscale ip -4
```

Both machines now have IPs like `100.x.x.x` on a private encrypted network.

## Step 2 — Configure OpenClaw Gateway for Tailscale

By default, OpenClaw binds to `localhost`. You need it to bind to all interfaces so the peer can reach it over Tailscale.

Check your gateway config:
```bash
openclaw gateway status
```

Set `gateway.bind` to `0.0.0.0` (all interfaces) or specifically the Tailscale IP:
```json
{
  "gateway": {
    "bind": "0.0.0.0",
    "port": 8080
  }
}
```

Apply and restart:
```
openclaw gateway restart
```

**Security note:** Binding to `0.0.0.0` exposes your gateway on all network interfaces. Tailscale traffic is encrypted peer-to-peer, but make sure you have a strong gateway token/password set. Consider `gateway.auth` to require token authentication.

## Step 3 — Exchange Gateway URLs

Once both gateways are reachable over Tailscale, exchange the peer gateway URLs:

**Machine A** tells Machine B:
```
Gateway URL: http://<Machine-A-Tailscale-IP>:8080
Gateway token: <your-gateway-token>
```

**Machine B** tells Machine A:
```
Gateway URL: http://<Machine-B-Tailscale-IP>:8080
Gateway token: <their-gateway-token>
```

## Step 4 — Create Peer Config File

On each machine, create a peer configuration at `peer-agent/peer-config.md`:

**Your config (Machine A):**
```markdown
# My Peer Configuration

My Tailscale IP: <your-tailscale-ip>
My Gateway URL: http://<your-tailscale-ip>:8080
My Gateway Token: <your-token>

# Peer (Machine B)
Peer Name: <friend's-name>
Peer Tailscale IP: <their-tailscale-ip>
Peer Gateway URL: http://<their-tailscale-ip>:8080
Peer Gateway Token: <their-token>

# How to reach my agent
# Use sessions_send with the gatewayUrl pointing to my gateway above.
# My agentId for direct targeting: <your-agent-id>
```

## Step 5 — Test the Connection

From Machine A, test reaching Machine B's gateway:
```bash
# Ping the peer's gateway over Tailscale
curl http://<peer-tailscale-ip>:8080/health --connect-timeout 5
```

You should get a health response. If not, check that the peer's gateway is bound to `0.0.0.0` and their firewall allows incoming on port 8080 from the Tailscale network.

## Step 6 — Send Messages Between Agents

Once connectivity is confirmed, use `sessions_send` with `gatewayUrl` pointing to the peer:

```json
sessions_send(
  sessionKey="<peer-session-key>",
  agentId="<peer-agent-id>",
  message="Hey, need your take on something — I'm stuck on...",
  gatewayUrl="http://<peer-tailscale-ip>:8080",
  gatewayToken="<peer-gateway-token>"
)
```

## Daily Collaboration Patterns

### Pattern 1: Morning Handoff
Each morning, each agent sends the other a brief status update:
```
sessions_send(
  message="Morning! Here's where I'm at: [project status]. Blockers: [if any]. 
   Any insights on [specific problem]?",
  gatewayUrl="http://<peer-ip>:8080",
  gatewayToken="<peer-token>"
)
```

### Pattern 2: Quick Insight
When one agent learns something useful:
```
"Something I learned today that might help you: [insight]"
```

### Pattern 3: Code/Review Request
```
"Can you review my approach to [task]? Here it is: [description]. 
 Is there a better pattern I'm missing?"
```

### Pattern 4: Delegation
```
"I've got a task that's more your specialty — want to delegate this to you? [task details].
 Let me know if you have capacity."
```

## Reference Files

- `references/tailscale-setup.md` — detailed Tailscale install, network setup, auth key sharing
- `references/peer-communication.md` — message format, frequency, session management
- `references/troubleshooting.md` — NAT, firewall, connection issues
- `scripts/peer_config.py` — interactive config generator for the peer setup

## Security Notes

- **Tailscale is encrypted end-to-end** — no one on the internet can see the traffic
- **Gateway token is required** — don't share your gateway token in plain text over an unsecured channel; use a private message or password manager
- **Only share with people you trust** — the peer can send messages that execute as your agent
- **Revoke auth keys** from the Tailscale admin console if the friendship ends
- **Consider `gateway.access`** — restrict which sessions can be targeted from peers

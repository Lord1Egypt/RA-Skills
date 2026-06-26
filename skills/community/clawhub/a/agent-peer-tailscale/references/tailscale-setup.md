# Tailscale Setup — Detailed Guide

## Why Tailscale Over Other VPNs?

| Feature | Tailscale | WireGuard | ngrok | VPS Relay |
|---------|-----------|-----------|-------|-----------|
| No port forwarding | ✅ | ✅ | ✅ | ✅ |
| No public IP needed | ✅ | ❌ | ✅ | ✅ |
| Auto NAT traversal | ✅ | ❌ | ✅ | ✅ |
| End-to-end encrypted | ✅ | ✅ | N/A | ❌ |
| Free for 2 users | ✅ | ✅ (self-hosted) | limited | cheap |
| Easy auth key sharing | ✅ | manual | N/A | N/A |
| Works behind CGNAT | ✅ | ❌ | ✅ | ✅ |

Tailscale uses DERP (Designated Relay Protocol) relay servers to bridge connections when direct peer-to-peer isn't possible (e.g., both behind CGNAT). Free users can use all DERP servers.

---

## Installing Tailscale

### Windows
```powershell
winget install Tailscale.Tailscale

# Or download from https://tailscale.com/download/windows
```

Start Tailscale from the system tray or:
```powershell
tailscale status  # check if running
tailscale up --accept-routes
```

### macOS
```bash
brew install --cask tailscale
# Start from menu bar app, or:
tailscale up --accept-routes
```

### Linux (Ubuntu/Debian)
```bash
curl -fsSL https://tailscale.com/install.sh | sh
tailscale up --accept-routes
```

### Android / iOS
Download Tailscale from the app store. Works as a VPN but needed mainly for the devices running OpenClaw gateways.

---

## Creating and Sharing a Tailscale Network

### Step 1: Create a Tailscale account

Go to https://login.tailscale.com and sign up (Google/GitHub/Microsoft SSO works).

### Step 2: Create the network (first user)

On Machine A (the initiator):
```bash
tailscale up --accept-routes
```
This will open a browser window for authentication. Complete it.

Once authenticated, your machine is on the Tailscale network.

### Step 3: Generate an auth key (for the peer to join)

1. Go to https://login.tailscale.com/settings/keys
2. Click **Generate auth key**
3. Check **Reusable** (so your friend can use it multiple times if needed, or uncheck for one-time use)
4. Copy the key — it looks like: `tskey-auth-kixxxxxxxxxxxxxxxxxxxxxx-xxxxxxxxxxxxxxxxxxxxxxxx`

### Step 4: Share the auth key securely

Send the auth key to your friend via a secure channel:
- Private message (Signal, WhatsApp)
- Password manager sharing
- Email if you trust the email account

**Never post it publicly.**

### Step 5: Friend joins the network

On Machine B:
```bash
tailscale up --accept-routes --authkey=tskey-auth-kixxxxxxxx-xxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

They'll authenticate in their browser the first time.

### Step 6: Verify connection

Both machines should now see each other:
```bash
tailscale status
```

Output looks like:
```
100.x.x.x  your-machine-name    linux   -
100.y.y.y  friend-machine-name  linux   -
```

---

## Tailscale IP Address Management

Tailscale IP addresses are assigned from a shared CGNAT-like address space. Your base IP stays with your machine, not your physical location.

To see your Tailscale IPs:
```bash
tailscale ip -4      # IPv4
tailscale ip -6      # IPv6
```

You can also set a persistent hostname for easy reference:
```bash
tailscale set --hostname my-agent
# Now accessible as: my-agent.tail-scale.ts.net
```

---

## Shared Node vs. Relay Mode

Tailscale has two connection modes:

### Peer-to-Peer (Direct) — Default
Both machines connect directly when possible. Fastest, lowest latency. Tailscale hole-punches through NAT.

**Works when:** At least one machine has a public IP or is behind a simple NAT.

### DERP Relay Mode — Fallback
Tailscale's relay servers act as intermediaries when direct connection fails. Still encrypted, just routed through Tailscale's servers.

**Always works** — even when both machines are behind strict CGNAT or double-NAT (common on mobile hotspots, some ISPs).

To force DERP mode if needed:
```bash
tailscale up --accept-routes --operator=$USER
# Or configure in Tailscale admin: Settings → Network → Force Relay
```

---

## Tailscale ACLs (Access Control Lists)

Tailscale ACLs define which machines can talk to which. By default, all machines on your network can talk to each other. For a 2-person peer network this is fine.

To verify/modify ACLs:
1. Go to https://login.tailscale.com/acls
2. Default policy (allows all):
```json
{
  "acls": [
    {"action": "accept", "src": ["autogroup:member"], "dst": ["autogroup:member"]}
  ]
}
```

For a simple 2-user network, the default is fine. You don't need to change anything.

---

## Sharing Files via Tailscale

Once on the same Tailscale network, you can also share files directly without any extra setup:

```bash
# On Machine A — serve a file
python3 -m http.server 9000
# File accessible at http://100.x.x.x:9000/filename

# Useful for: sharing large datasets, model files, exported skills
```

Or use Tailscale's built-in SOCKS5 proxy to route traffic through the other machine's internet connection (if you need to).

---

## Updating Tailscale

```bash
# Check version
tailscale version

# Update (most platforms)
tailscale update

# Or reinstall (winget/homebrew)
```

Tailscale updates automatically on most platforms.

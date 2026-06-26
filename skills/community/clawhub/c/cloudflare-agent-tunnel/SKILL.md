---
name: cloudflare-agent-tunnel
description: >
  Give each OpenClaw agent its own secure HTTPS URL using Cloudflare Tunnel (cloudflared). No SSL
  certificates to manage, no ports to expose publicly. Use when setting up secure cloud access for
  OpenClaw agents on a VPS, assigning per-agent subdomains (koda.yourdomain.com), enabling HTTPS
  without nginx or Let's Encrypt, or connecting a custom domain to an agent. Covers named tunnels
  (permanent URL, free Cloudflare account — preferred), quick tunnels (temporary, no account),
  multi-agent setup on a single VPS, and custom domain configuration.
---

# Cloudflare Agent Tunnel

Give each OpenClaw agent a permanent, secure HTTPS URL via Cloudflare Tunnel — no SSL certs, no nginx, no open ports.

## How It Works

```
User → https://koda.yourdomain.com
         ↓ (Cloudflare edge — TLS termination here)
       Cloudflare Tunnel (encrypted)
         ↓
       cloudflared process on VPS
         ↓
       http://localhost:18789  (OpenClaw gateway)
```

- Cloudflare handles TLS — no cert management on the server
- The local port never needs to be open to the internet
- Each agent gets its own `cloudflared` process + systemd service

---

## ✅ Preferred Method — Named Tunnel (Permanent, Free Cloudflare Account)

**Always use this method.** Gives a permanent URL tied to your domain. Requires a free Cloudflare account — takes 2 minutes to set up.

### Step 1: Install cloudflared

```bash
curl -fsSL https://pkg.cloudflare.com/cloudflare-main.gpg | tee /usr/share/keyrings/cloudflare-main.gpg >/dev/null
echo "deb [signed-by=/usr/share/keyrings/cloudflare-main.gpg] https://pkg.cloudflare.com/cloudflared any main" \
  | tee /etc/apt/sources.list.d/cloudflared.list
apt-get update -qq && apt-get install -y cloudflared
```

### Step 2: Authenticate — give the user this URL

Run on the VPS:
```bash
cloudflared tunnel login
```

This prints a Cloudflare auth URL. **Give that URL to the user** — they open it in their browser, log into their Cloudflare account, and click Authorize. This saves `/root/.cloudflared/cert.pem` on the VPS.

Poll for completion:
```bash
# Wait until cert.pem appears (user has authorized)
until [ -f /root/.cloudflared/cert.pem ]; do sleep 3; done && echo "Authorized!"
```

### Step 3: Create the tunnel

```bash
cloudflared tunnel create openclaw-koda
# Outputs a UUID — note it
TUNNEL_UUID=$(cloudflared tunnel list --output json | python3 -c \
  "import json,sys; t=[x for x in json.load(sys.stdin) if x['name']=='openclaw-koda']; print(t[0]['id'])")
```

### Step 4: Write tunnel config

```bash
mkdir -p /etc/cloudflared
cat > /etc/cloudflared/openclaw-koda.yml << EOF
tunnel: ${TUNNEL_UUID}
credentials-file: /root/.cloudflared/${TUNNEL_UUID}.json

ingress:
  - hostname: koda.yourdomain.com
    service: http://localhost:18789
  - service: http_status:404
EOF
```

### Step 5: Route DNS

```bash
cloudflared tunnel route dns openclaw-koda koda.yourdomain.com
# Automatically creates CNAME: koda.yourdomain.com → <UUID>.cfargotunnel.com
```

The domain must use **Cloudflare nameservers**. If it doesn't yet, the user transfers DNS management to Cloudflare (free, takes ~5 min).

### Step 6: Install as systemd service

```bash
cat > /etc/systemd/system/cloudflared-koda.service << 'EOF'
[Unit]
Description=Cloudflare Tunnel — openclaw-koda
After=network.target openclaw.service

[Service]
Type=simple
User=root
ExecStart=/usr/bin/cloudflared tunnel --no-autoupdate --config /etc/cloudflared/openclaw-koda.yml run
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable cloudflared-koda
systemctl start cloudflared-koda
systemctl is-active cloudflared-koda
```

### Step 7: Update OpenClaw allowedOrigins

```json
"gateway": {
  "controlUi": {
    "allowedOrigins": [
      "http://localhost:18789",
        "https://koda.yourdomain.com"
    ]
  }
}
```

Then: `systemctl restart openclaw-koda`

### Step 8: Lock down the port

Block direct public access — all traffic must go through the tunnel:
```bash
ufw deny 18789
ufw reload
```

---

## Quick Tunnel (Fallback Only — Temporary)

> ⚠️ **Use only as a temporary fallback** when no domain is available. The URL is random and resets every time the service restarts. Switch to a named tunnel as soon as a domain is ready.

```bash
# Start quick tunnel — prints a random https://*.trycloudflare.com URL
cloudflared tunnel --url http://localhost:18789 --no-autoupdate

# Or as a systemd service (URL logged to /var/log/cloudflared-openclaw.log)
ExecStart=/usr/bin/cloudflared tunnel --no-autoupdate --url http://localhost:18789
```

Read the assigned URL:
```bash
grep -o 'https://[a-z0-9-]*\.trycloudflare\.com' /var/log/cloudflared-openclaw.log | tail -1
```

---

## Multi-Agent Setup (One VPS, Multiple Agents)

Each agent = one OpenClaw gateway port + one named tunnel + one systemd service.

```
Port 18789 → openclaw-koda.service   + cloudflared-koda.service   → koda.yourdomain.com
Port 18790 → openclaw-alex.service   + cloudflared-alex.service   → alex.yourdomain.com
Port 18791 → openclaw-jordan.service + cloudflared-jordan.service → jordan.yourdomain.com
```

**Critical:** Do NOT use `cloudflared service install` for multiple agents — it only supports one tunnel and overwrites the system service. Always write individual systemd service files per agent.

---

## Custom Domains

Key facts:
- Domain must use **Cloudflare nameservers** (transfer at your registrar — free)
- Cloudflare issues and auto-renews TLS certs
- CNAME records created automatically via `cloudflared tunnel route dns`
- Free Cloudflare plan: unlimited tunnels, unlimited bandwidth

See `references/custom-domains.md` for a full walkthrough.

---

## Managing Tunnels

```bash
# Status
systemctl list-units "cloudflared-*" --no-pager

# Logs
journalctl -u cloudflared-koda -f

# List named tunnels
cloudflared tunnel list

# Delete a tunnel
cloudflared tunnel delete openclaw-koda
systemctl disable cloudflared-koda && rm /etc/systemd/system/cloudflared-koda.service
```

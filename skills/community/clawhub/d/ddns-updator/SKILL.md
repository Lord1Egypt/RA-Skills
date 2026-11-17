---
name: ddns-updator
description: |
  Dynamic DNS updater for self-hosted / homelab / edge devices. Detects the device's
  public IPv4 and IPv6 addresses via public APIs (ipify, ifconfig.me, icanhazip),
  compares them against the last-known addresses, and pushes updates to the configured
  DDNS provider (currently dynv6, with an extensible provider architecture).

  Trigger by telling the agent:
  - "Update my DDNS" / "Check and update DNS" / "Run DDNS"
  - "What's my public IP?" / "Check my IP address"
  - Any request that involves current public IP or DDNS synchronization

  Supported providers: dynv6 (default). DuckDNS, Cloudflare, and No-IP APIs
  are documented in references/providers.md for easy extension.

  Security: sensitive tokens are stored in a chmod-600 config file at
  ~/.config/picoclaw-ddns/config.json, outside the skill directory.
version: 1.0.0
metadata:
  openclaw:
    requires:
      bins:
        - curl
        - jq
      config:
        - ~/.config/picoclaw-ddns/config.json
    primaryEnv: PICOCLAW_DDNS_TOKEN
    envVars:
      - name: PICOCLAW_DDNS_HOSTNAME
        required: false
        description: dynv6 zone name (alternative to config.json)
      - name: PICOCLAW_DDNS_TOKEN
        required: true
        description: dynv6 HTTP token for the zone
    emoji: "🦞"
    os:
      - linux
      - macos
    install:
      - kind: brew
        formula: jq
        bins: [jq]
---

# 🦞 DDNS Skill

Update your dynamic DNS records on demand. Detects public IP changes and pushes them
to your DDNS provider (dynv6 by default). No periodic cron needed — run it when you
suspect your IP has changed.

---

## Quick start

### 1️⃣ Create the config file

**Outside** the skill directory, in your home config folder:

```bash
mkdir -p ~/.config/picoclaw-ddns

cat > ~/.config/picoclaw-ddns/config.json <<'EOF'
{
  "provider": "dynv6",
  "dynv6": {
    "hostname": "yourname.dynv6.net",
    "token": "your-http-token"
  }
}
EOF

chmod 600 ~/.config/picoclaw-ddns/config.json
```

> 🔒 **Why chmod 600?** The token is sensitive — only the file owner should read it.
> The config lives in `~/.config/picoclaw-ddns/`, **not** inside the skill folder,
> so it won't be accidentally bundled or published.

### 2️⃣ Run the update

```bash
bash <workspace>/skills/ddns-updator/scripts/ddns.sh
```

The script will:
1. Detect your current public IPv4 and IPv6 addresses
2. Compare against the last-known addresses
3. Only call the dynv6 API if something changed
4. Save the new addresses to `~/.config/picoclaw-ddns/state.json`

### 3️⃣ Just check your IP (no update)

```bash
bash <workspace>/skills/ddns-updator/scripts/get_ip.sh
```

---

## Scripts

| Script | Purpose |
|--------|---------|
| `scripts/ddns.sh` | **Main orchestrator** — detect IP → diff → push → persist |
| `scripts/get_ip.sh` | Fetch public IPv4/IPv6 from multiple APIs; outputs JSON |
| `scripts/update_dynv6.sh` | Low-level dynv6 API caller (hostname + token + IPs) |

---

## Configuration reference

### Config file (`~/.config/picoclaw-ddns/config.json`)

```json
{
  "provider": "dynv6",
  "dynv6": {
    "hostname": "yourname.dynv6.net",
    "token": "your-http-token"
  }
}
```

### Environment variables (alternative to config.json)

| Variable | Required | Description |
|----------|----------|-------------|
| `PICOCLAW_DDNS_HOSTNAME` | ❌ | dynv6 zone name (overrides config) |
| `PICOCLAW_DDNS_TOKEN` | ❌ | dynv6 HTTP token (overrides config) |

If both config.json and env vars are present, env vars take precedence.

### State file (`~/.config/picoclaw-ddns/state.json`)

Auto-managed. Records the last-known IPs so the next run can detect changes.

```json
{
  "ipv4": "203.0.113.1",
  "ipv6": "2001:db8::1",
  "updated": "2025-07-05T12:00:00+08:00"
}
```

---

## Triggering via the agent

Just say:

> **"Update my DDNS"**
> **"Check and update my DNS"**
> **"What's my public IP?"**
> **"Run DDNS check"**

The agent will read this skill and execute `scripts/ddns.sh` for you.

---

## Scheduled / periodic updates (optional)

Add a crontab entry for fully automatic updates:

```bash
# Every 10 minutes
*/10 * * * * /bin/bash /path/to/ddns.sh
```

Or every hour:

```bash
# Every hour at minute 0
0 * * * * /bin/bash /path/to/ddns.sh
```

---

## Multi-domain support

Run the orchestrator with different config files:

```bash
CONFIG_FILE=~/.config/picoclaw-ddns/domain1.json bash scripts/ddns.sh
CONFIG_FILE=~/.config/picoclaw-ddns/domain2.json bash scripts/ddns.sh
```

---

## Extending to other providers

The `references/providers.md` file documents the APIs for:
- dynv6 (current default)
- DuckDNS
- Cloudflare (v4 API)
- No-IP

To add a new provider, add a new `scripts/update_<provider>.sh` script following
the same parameter convention as `update_dynv6.sh`, then update the main script
to dispatch based on `config.json` → `.provider`.

---

## Architecture

```
User says "Update my DDNS"
        │
        ▼
  Agent reads this SKILL.md
        │
        ▼
  Executes scripts/ddns.sh
        │
        ├── scripts/get_ip.sh
        │       └── curl https://api.ipify.org           → IPv4
        │       └── curl https://api64.ipify.org          → IPv6
        │
        ├── Compare with ~/.config/picoclaw-ddns/state.json
        │
        └── If changed:
            └── scripts/update_dynv6.sh <hostname> <token> <ipv4> <ipv6>
                    └── GET https://dynv6.com/api/update?...
```

---

## Security notes

| Concern | Mitigation |
|---------|------------|
| Token leaks | Config file at `~/.config/picoclaw-ddns/config.json` with `chmod 600` |
| Public IP APIs | Read-only, no auth needed, multiple fallback sources |
| Agent context | The SKILL.md never exposes real tokens — only the scripts read the config |
| Publishing | The skill folder contains **no** credentials or secrets |

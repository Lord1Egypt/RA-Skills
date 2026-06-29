---
name: aitun-tunnel
version: 4.0.5
description: Expose local web pages and HTTP services to the public internet via secure tunnels. Perfect for AI agents that build websites locally and need to share them publicly.
metadata:
  openclaw:
    requires:
      bins:
        - python3
    envVars:
      - name: AITUN_SERVER
        required: false
        description: "AiTun server address (default: aitun.cc:6639)"
      - name: AITUN_SUBDOMAIN
        required: false
        description: "Custom subdomain to register (e.g., myapp)"
    install:
      - kind: pip
        package: aitun
        bins: [aitun]
      - kind: uv
        package: aitun
        bins: [aitun]
    emoji: "🚇"
    homepage: https://aitun.cc
    clawhub: https://clawhub.ai/ctz168/aitun-tunnel
---

# AiTun Tunnel - Expose Local Web Pages to the Public Internet

## When to Use

Use this skill when:
- You've built a web page, dashboard, or web app locally and need to share it publicly
- You need to test a local HTTP service from an external device
- You want to demo a locally-running application to someone
- You need a public webhook endpoint for an external service to call
- You want to expose a local API for integration testing
- You built a website for a user and they want to see it in their browser

Do NOT use this skill when:
- The content only needs to be viewed locally
- The user asks for a file download (use file sharing instead)

## Instructions

### Step 1: Install aitun

```bash
pip install aitun
```

Or install via one-line script (Linux/macOS):
```bash
curl -fsSL https://aitun.cc/install.sh | bash
```

Windows (PowerShell):
```powershell
irm https://aitun.cc/install.ps1 | iex
```

Or if already installed, verify:

```bash
which aitun
```

### Step 2: Start the local web service

Ensure the local web service is running on a port. For static HTML files:

```bash
# Serve a directory with a built HTML page
python3 -m http.server 8080 --directory /path/to/html/dir
```

For other frameworks, start their dev server:
- Next.js: `npm run dev -- -p 3000`
- Flask: `flask run --port 5000`
- Any HTTP service on any port

### Step 3: Create a tunnel

**Option A: Free instant tunnel (no sign-up, 24-hour limit)**

Free tunnels use proxy address mode (path-based routing). No subdomain is assigned — the public URL uses the format `aitun.cc/<tunnel-code>`. Simply run without a token:

```bash
aitun -p 8080 &
AITUN_PID=$!
sleep 3
```

The output will contain the public URL, e.g.:
- `https://aitun.cc/abc123`

**Option B: Custom subdomain (requires sign-in at aitun.cc)**

Registered users can create custom subdomains with two domain levels:
- Standard domain: `myapp.t.aitun.cc` (up to 5 subdomains)
- Short domain: `myapp.aitun.cc` (up to 2 subdomains)

```bash
# Check availability
curl -s https://aitun.cc/aitun-api/subdomain/check/myapp

# Register via website: https://aitun.cc
# Then use your token:
aitun -p 8080 -k YOUR_TOKEN
```

### Step 4: Share the public URL

Tell the user their website is now publicly accessible:

```
Your website is now live at: https://aitun.cc/abc123

This free tunnel expires in 24 hours.
For a permanent subdomain (e.g., myapp.aitun.cc), register at https://aitun.cc
```

### Step 5: Clean up

When done, stop the tunnel:

```bash
kill $AITUN_PID 2>/dev/null
```

## CLI Reference

The `aitun` command (installed via `pip install aitun`, or alternatively `curl -fsSL https://aitun.cc/install.sh | bash` / `irm https://aitun.cc/install.ps1 | iex` on Windows) accepts these flags:

| Flag | Description |
|---|---|
| `-p PORT` | Local HTTP service port (optional; omit for TCP-only mode with `--tcp-ports`) |
| `-k TOKEN` | Auth token for registered subdomain (omit for free tunnel) |
| `--host HOST` | Local service address (default: localhost) |
| `--tcp-ports PORTS` | TCP forwarding ports, comma-separated (e.g., `22,3306`; requires `-k`). Use without `-p` for TCP-only mode |
| `--p2p` | Enable P2P direct connection (default: enabled) |
| `--no-p2p` | Disable P2P, force server relay mode |
| `--daemon` | Run as background daemon |
| `--stop` | Stop running daemon |

## Notes

- The `-p` flag is optional. Omit it when using `--tcp-ports` only (TCP-only mode, e.g., SSH/RDP forwarding without HTTP)
- When `-p` is specified, the local service must be running before starting aitun (the client checks port availability)
- Free tunnels use proxy address mode (path-based URL like `aitun.cc/abc123`), NOT subdomains
- Free tunnels expire after 24 hours, auto-renewed on restart
- Registered subdomains remain active for 30 days of inactivity; use heartbeat to renew
- Standard domain subdomains (`xxx.t.aitun.cc`): up to 5 per user
- Short domain subdomains (`xxx.aitun.cc`): up to 2 per user
- All traffic is encrypted end-to-end
- Reserved subdomains (www, api, admin, test, etc.) cannot be registered
<!-- dispatcher trigger test 2026-06-18 -->

---
name: cftunnel
description: Expose local services to the internet via Cloudflare Tunnels. CLI (npx cftunnel) and Node.js library for creating tunnels, configuring ingress routes, managing DNS records, and running cloudflared.
version: 1.0.0
metadata:
  openclaw:
    requires:
      env:
        - CLOUDFLARE_API_KEY
        - CLOUDFLARE_EMAIL
        - CLOUDFLARE_ACCOUNT_ID
      bins:
        - node
        - cftunnel
    primaryEnv: CLOUDFLARE_API_KEY
    install:
      - kind: node
        package: cftunnel -g
        bins: [cftunnel]
    emoji: "🚇"
    homepage: https://github.com/kyndlo/cftunnel
---

# cftunnel — Cloudflare Tunnel Manager for AI Agents

Expose local services to the internet via Cloudflare Tunnels. Use this skill when you need to make a locally running application accessible at a public HTTPS URL.

**Flow:** Start a local service (e.g. on port 3000) → `cftunnel` creates a tunnel + DNS route → the service is live at `https://hostname.domain.com`.

## Authentication

Set these environment variables before running any command:

```bash
# Option A: API Key + Email (most common)
export CLOUDFLARE_API_KEY=<api-key>
export CLOUDFLARE_EMAIL=<account-email>

# Option B: API Token (scoped, if available)
export CLOUDFLARE_API_TOKEN=<api-token>

# Always required:
export CLOUDFLARE_ACCOUNT_ID=<account-id>
```

## Quick Reference

### Expose a local service (fastest path)

If a tunnel and cloudflared are already running (check with `tunnel list`), just add a route and DNS:

```bash
# 1. Add ingress route to existing tunnel
npx cftunnel route add <tunnel-id> --hostname <hostname> --service http://localhost:<port>

# 2. Create DNS CNAME
npx cftunnel dns create --zone-id <zone-id> --hostname <hostname> --tunnel-id <tunnel-id>
```

### Create everything from scratch (one command)

```bash
npx cftunnel quickstart \
  --name <tunnel-name> \
  --hostname <hostname> \
  --service http://localhost:<port> \
  --zone-id <zone-id>
```

Then run the connector: `npx cftunnel run <tunnel-id>`

### Programmatic usage (Node.js library)

```typescript
import { createClient, quickstart } from 'cftunnel';

const client = createClient({ apiKey: '...', apiEmail: '...' });
const result = await quickstart(client, {
  accountId: '...',
  name: 'my-app',
  hostname: 'app.example.com',
  service: 'http://localhost:3000',
  zoneId: '...',
});
console.log(result.run_cmd);
```

## All Commands

### Tunnel lifecycle

| Command | Purpose |
|---|---|
| `npx cftunnel tunnel list` | List all tunnels. Find existing tunnel IDs and check status (healthy/down/inactive). |
| `npx cftunnel tunnel create <name>` | Create a new tunnel. Returns tunnel ID and secret. Add `--config-src local` for YAML-managed config. |
| `npx cftunnel tunnel get <tunnel-id>` | Get tunnel details including connection status. |
| `npx cftunnel tunnel delete <tunnel-id>` | Delete a tunnel. Must have no active connections. |
| `npx cftunnel tunnel token <tunnel-id>` | Get the token needed to run cloudflared. Returns `run_cmd` and `install_cmd`. |

### Ingress routes (hostname → local service mapping)

| Command | Purpose |
|---|---|
| `npx cftunnel route list <tunnel-id>` | Show current ingress rules. Always has a catch-all 404 as last rule. |
| `npx cftunnel route add <tunnel-id> --hostname <host> --service <url>` | Add a route. Preserves existing routes, appends before catch-all. Optional `--path` for path filtering. |
| `npx cftunnel route remove <tunnel-id> --hostname <host>` | Remove a route by hostname. |
| `npx cftunnel route set <tunnel-id> --route host1=svc1 --route host2=svc2` | Replace ALL routes. Use for bulk configuration. |

### DNS records

| Command | Purpose |
|---|---|
| `npx cftunnel dns create --zone-id <zid> --hostname <host> --tunnel-id <tid>` | Create proxied CNAME pointing hostname to tunnel. Required for the hostname to resolve. |
| `npx cftunnel dns list --zone-id <zid>` | List all DNS records in the zone. |
| `npx cftunnel dns delete <record-id> --zone-id <zid>` | Delete a DNS record. |

### Running the connector

| Command | Purpose |
|---|---|
| `npx cftunnel run <tunnel-id>` | Run cloudflared in foreground. Auto-detects cloudflared from PATH or npm package. |
| `npx cftunnel run <tunnel-id> --install-service` | Install cloudflared as a persistent system service (survives reboots). |

## Decision Guide

**"I need to expose port N on a domain"**
→ Check `tunnel list` for a healthy tunnel. If one exists, use `route add` + `dns create`. If not, use `quickstart`.

**"I need to add another service to an existing tunnel"**
→ `route add` + `dns create`. One tunnel can serve many hostnames.

**"I need to change where a hostname points"**
→ `route remove --hostname X` then `route add --hostname X --service <new-url>`. DNS stays the same.

**"I need to take a service offline"**
→ `route remove --hostname X` and optionally `dns delete <record-id>`.

**"The tunnel exists but cloudflared isn't running"**
→ `npx cftunnel run <tunnel-id>` or use `tunnel token` to get the token for manual `cloudflared` invocation.

## Service URL Formats

The `--service` flag accepts these protocols:

| Format | Example | Use case |
|---|---|---|
| `http://host:port` | `http://localhost:3000` | HTTP web apps, APIs |
| `https://host:port` | `https://localhost:8443` | HTTPS backends |
| `tcp://host:port` | `tcp://localhost:5432` | Databases, raw TCP |
| `ssh://host:port` | `ssh://localhost:22` | SSH access |
| `unix:///path` | `unix:///tmp/app.sock` | Unix socket apps |
| `http_status:CODE` | `http_status:404` | Static status response (catch-all) |

## Output Format

All commands output JSON to **stdout**. Progress/errors go to **stderr**.

Parse with `jq`:
```bash
TUNNEL_ID=$(npx cftunnel tunnel create my-app | jq -r '.id')
TOKEN=$(npx cftunnel tunnel token $TUNNEL_ID | jq -r '.token')
```

## Common Patterns

### Pattern 1: Deploy a new web app

```bash
cd /path/to/app && npm start &

npx cftunnel quickstart \
  --name my-web-app \
  --hostname app.example.com \
  --service http://localhost:8080 \
  --zone-id <zone-id>

npx cftunnel run <tunnel-id-from-output>
```

### Pattern 2: Add subdomain to existing tunnel

```bash
npx cftunnel tunnel list | jq '.[] | select(.status == "healthy")'

npx cftunnel route add <tunnel-id> --hostname api.example.com --service http://localhost:4000
npx cftunnel dns create --zone-id <zone-id> --hostname api.example.com --tunnel-id <tunnel-id>
```

### Pattern 3: Swap service behind a hostname

```bash
npx cftunnel route remove <tunnel-id> --hostname app.example.com
npx cftunnel route add <tunnel-id> --hostname app.example.com --service http://localhost:9000
```

### Pattern 4: Clean teardown

```bash
npx cftunnel route remove <tunnel-id> --hostname app.example.com
npx cftunnel dns list --zone-id <zone-id>
npx cftunnel dns delete <record-id> --zone-id <zone-id>
npx cftunnel tunnel delete <tunnel-id>
```

### Pattern 5: Programmatic usage in agent code

```typescript
import { createClient, createTunnel, addRoute, createDNS } from 'cftunnel';

const client = createClient(); // reads from env vars
const tunnel = await createTunnel(client, { accountId: '...', name: 'my-app' });
await addRoute(client, {
  accountId: '...',
  tunnelId: tunnel.id,
  hostname: 'app.example.com',
  service: 'http://localhost:3000',
});
await createDNS(client, {
  zoneId: '...',
  hostname: 'app.example.com',
  tunnelId: tunnel.id,
});
```

## Important Notes

- A tunnel must have `cloudflared` running to serve traffic. Creating a tunnel and routes alone is not enough.
- The catch-all `http_status:404` rule is always appended automatically. Do not add it manually.
- DNS CNAME records must be **proxied** through Cloudflare (orange cloud). This is set automatically.
- One tunnel can serve multiple hostnames. Prefer reusing existing healthy tunnels over creating new ones.
- `route set` replaces ALL routes. Use `route add`/`route remove` for incremental changes.
- If cloudflared is already running as a service, route changes take effect immediately (no restart needed).

## Global Flags

| Flag | Env Var | Description |
|---|---|---|
| `--api-token` | `CLOUDFLARE_API_TOKEN` | Cloudflare API token (bearer auth) |
| `--api-key` | `CLOUDFLARE_API_KEY` | Cloudflare API key (requires --api-email) |
| `--api-email` | `CLOUDFLARE_EMAIL` | Cloudflare account email |
| `--account-id` | `CLOUDFLARE_ACCOUNT_ID` | Cloudflare account ID |

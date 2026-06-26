---
name: axiomata-web-deploy
description: "Deploy a public web presence (HTML + Docker + DNS + Domain) in ~15 minutes. Triggers on: 'deploy website', 'build and deploy', 'create web presence', 'launch site', 'deploy to web', 'publish website', 'setup web server', 'docker deploy', 'domain setup', 'DNS configuration', 'full stack deploy'. For users who want a fast, autonomous deployment pipeline."
---

# Axiomata Web Deploy — 15-Minute Public Web Presence

> **What this skill does:** Takes a directory with HTML files and deploys a live, publicly accessible website on a VPS using Docker + DNS + Domain — fully autonomous, no human intervention after launch.

> **Security first:** No credentials are embedded in this skill. All secrets are read from local files or environment variables. Never ship tokens in skill code.

> **Transparency:** This skill is for deploying websites only. It does not: exfiltrate data, access files outside the project directory, or perform any action beyond web deployment.

> **Required env vars:** `HOSTINGER_TOKEN`, `VPS_IP`, `DNS_ZONE_ID` (or equivalents for your DNS provider)

---

## Architecture Overview

```
+------------------------------------------------------+
|              15-MINUTE DEPLOYMENT PIPELINE           |
+------------------------------------------------------+
|  Phase 1 (2 min)  → Create HTML + Dockerfile        |
|  Phase 2 (2 min)  → Build Docker image              |
|  Phase 3 (3 min)  → Deploy to Docker                |
|  Phase 4 (3 min)  → Configure DNS + attach domain   |
|  Phase 5 (5 min)  → Verify everything works         |
+------------------------------------------------------+
  Total: ~15 min | DNS propagation: 5-48h
```

---

## Prerequisites

- VPS with Docker installed
- Domain name registered (optional but recommended)
- DNS provider API token (stored locally, NOT in skill)
- Nginx or similar web server

---

## Phase 1 — Project Setup (2 min)

```bash
mkdir -p /data/deployments/<project-name>
cd /data/deployments/<project-name>
```

**`index.html`:**

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>My Site</title>
</head>
<body>
  <h1>[ROCKET] Deployed with Axiomata Web Deploy</h1>
  <p>Live in 15 minutes.</p>
</body>
</html>
```

**`nginx.dockerfile`:**

```dockerfile
FROM nginx:alpine
COPY index.html /usr/share/nginx/html/index.html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

---

## Phase 2 — Build Docker (2 min)

```bash
docker build -f nginx.dockerfile -t <project-name>:latest .
```

---

## Phase 3 — Deploy Container (3 min)

```bash
# Stop existing container (ignore errors)
docker stop <project-name> 2>/dev/null || true
docker rm <project-name> 2>/dev/null || true

# Run as daemon
docker run -d \
  --name <project-name> \
  -p 80:80 \
  --restart unless-stopped \
  <project-name>:latest

# Verify
docker ps | grep <project-name>
curl -s http://localhost/ | head -20
```

**Port mapping:**
- Default: `80:80` (HTTP)
- Multiple sites: different local ports (`8080:80`, `3000:80`)
- Open ports in VPS firewall

---

## Phase 4 — DNS + Domain (3 min)

### Get Your VPS Public IP

```bash
curl -s ifconfig.me
```

### DNS Setup (Example: Hostinger API)

**Credentials stored locally — never in skill.**

Your credentials file (replace with your actual path):
```bash
# Example: ~/.credentials/host_vps.md
# Format:
# Token: YOUR_TOKEN_HERE
# IP: YOUR_VPS_IP

HOSTINGER_TOKEN=$(grep '^Token:' "$HOME/.credentials/host_vps.md" | awk '{print $2}')
VPS_IP=$(grep '^IP:' "$HOME/.credentials/host_vps.md" | awk '{print $2}')
```

**Required environment variables (declare these before running):**
| Variable | Description | Example |
|----------|-------------|---------|
| `HOSTINGER_TOKEN` | Hostinger API token | `hKsW...` |
| `VPS_IP` | Your VPS public IP | `31.97.150.235` |
| `DNS_ZONE_ID` | Your DNS zone ID | `abc123` |

**Create DNS records:**

```bash
# Get your DNS zones
curl -s -X GET "https://api.hostinger.com/api/vps/v1/dns/zones" \
  -H "Authorization: Bearer $HOSTINGER_TOKEN"

# Create root A record
curl -s -X POST "https://api.hostinger.com/api/vps/v1/dns/zones/<zone-id>/records" \
  -H "Authorization: Bearer $HOSTINGER_TOKEN" \
  -H "Content-Type: application/json" \
  -d "{\"type\": \"A\", \"name\": \"@\", \"value\": \"$VPS_IP\", \"ttl\": 300}"

# Create www subdomain
curl -s -X POST "https://api.hostinger.com/api/vps/v1/dns/zones/<zone-id>/records" \
  -H "Authorization: Bearer $HOSTINGER_TOKEN" \
  -H "Content-Type: application/json" \
  -d "{\"type\": \"A\", \"name\": \"www\", \"value\": \"$VPS_IP\", \"ttl\": 300}"
```

**For Cloudflare, Namecheap, Route53:** Use their API with the same pattern — store credentials locally, reference them at runtime.

---

## Phase 5 — Verify (5 min)

```bash
# 1. Container running?
docker ps | grep <project-name>

# 2. Local response?
curl -s --max-time 5 http://localhost/ | grep -o "<title>.*</title>"

# 3. Container logs clean?
docker logs <project-name> --tail 20

# 4. DNS resolved?
dig +short <domain> @8.8.8.8

# 5. External access (with Host header)
curl -s --max-time 10 -H "Host: <domain>" http://<VPS_IP>/
```

---

## Boilerplate Template

Copy from `assets/web-boilerplate/`:
- `index.html` — Clean landing page
- `nginx.dockerfile` — Nginx container

Customize and deploy.

---

## Cleanup Old Deployments

```bash
# List all
docker ps -a --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

# Remove
docker stop <old-project> && docker rm <old-project>
docker rmi <old-project>:latest
rm -rf /data/deployments/<old-project>
```

---

## HTTPS (Optional, +5 min)

```bash
apt install certbot python3-certbot-nginx
certbot --nginx -d <domain> -d www.<domain>
```

---

## Success Checklist

- [ ] Container running: `docker ps | grep <project-name>`
- [ ] Local test: `curl http://localhost/` returns HTML
- [ ] DNS resolved: `dig +short <domain>` shows VPS IP
- [ ] Public access: External request returns content
- [ ] (Optional) HTTPS: SSL certificate active

---

## Security Rules (Critical)

> [WARNING] **Never embed credentials in skill code or documentation.**
>
> - API tokens → read from local files only
> - Passwords → never in source or docs
> - Before publishing anywhere: grep all files for tokens, keys, secrets
>
> **The skill teaches the process, not carries the keys.**

---

_In Altum Per Axioma._ Merlin
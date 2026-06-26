# Claw2UI Self-Hosting Guide

This guide covers running your own Claw2UI server instead of using the public instance at `https://0xsegfaulted-claw2ui.hf.space`.

## Table of Contents

- [Local Server](#local-server)
- [Fixed Domain (Named Tunnel)](#fixed-domain-named-tunnel)
- [Docker / HF Space Deployment](#docker--hf-space-deployment)
- [Environment Variables](#environment-variables)
- [Token Management](#token-management)
- [Backup (HF Dataset)](#backup-hf-dataset)

---

## Local Server

Run Claw2UI on your machine with an auto-generated Cloudflare quick tunnel:

```bash
npm install -g claw2ui

claw2ui start                    # Start server + tunnel
claw2ui start --no-tunnel        # Start without tunnel (localhost only)
claw2ui start --port 8080        # Custom port
claw2ui status                   # Check if server is running
```

The server listens on `http://localhost:9800` by default. If `cloudflared` is installed, a random public tunnel URL is generated automatically.

### Install cloudflared (optional)

```bash
# macOS
brew install cloudflared

# Linux — see https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/downloads/
```

Without cloudflared, Claw2UI runs in localhost-only mode.

---

## Fixed Domain (Named Tunnel)

For a permanent URL instead of random quick tunnels. Requires a Cloudflare account + `cloudflared`.

```bash
# One-time setup
cloudflared tunnel login
cloudflared tunnel create claw2ui
cloudflared tunnel route dns claw2ui board.yourdomain.com

# Start with named tunnel
export CLAWBOARD_TUNNEL_NAME=claw2ui
export CLAWBOARD_TUNNEL_URL=https://board.yourdomain.com
claw2ui start
```

Add the exports to your shell profile for persistence.

---

## Docker / HF Space Deployment

Claw2UI includes a `Dockerfile` for cloud deployment. This is ideal for hosting a shared instance that others can publish pages to.

### Deploy to Hugging Face Spaces

```bash
# Install hf CLI
pip install huggingface_hub[cli]
hf auth login

# Create a Docker Space
hf repos create yourname/claw2ui --type space --space-sdk docker

# Upload project files
hf upload yourname/claw2ui . . --type space --commit-message "Deploy claw2ui"
```

### Required Space Secrets

Set these in your Space settings (Settings → Variables and secrets):

| Secret | Value | Purpose |
|--------|-------|---------|
| `CLAWBOARD_TOKEN` | A random 64-char hex string | Admin API token |
| `CLAWBOARD_PUBLIC_URL` | `https://yourname-claw2ui.hf.space` | Public URL for generated page links |

### Optional Secrets (for backup)

| Secret | Value | Purpose |
|--------|-------|---------|
| `HF_TOKEN` | HF token with write access | Upload backups to HF Dataset |
| `CLAWBOARD_BACKUP_REPO` | `yourname/claw2ui-data` | Private dataset repo for backup |

Generate an admin token:

```bash
python3 -c "import secrets; print(secrets.token_hex(32))"
```

### HF Space Notes

- Free tier: `cpu-basic` hardware, sleeps after 48h of inactivity, auto-wakes on visit
- Pages and tokens persist across restarts if backup is configured
- The Dockerfile sets `CLAWBOARD_BIND=0.0.0.0`, `CLAWBOARD_PORT=7860`, `CLAWBOARD_TRUST_PROXY=1` automatically

---

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `CLAWBOARD_PORT` | `9800` | Server port |
| `CLAWBOARD_BIND` | `127.0.0.1` | Bind address (`0.0.0.0` for cloud) |
| `CLAWBOARD_TOKEN` | auto-generated | Admin API bearer token |
| `CLAWBOARD_NO_TUNNEL` | `0` | Set to `1` to skip tunnel |
| `CLAWBOARD_TUNNEL_NAME` | — | Cloudflare named tunnel name |
| `CLAWBOARD_TUNNEL_URL` | — | Fixed public URL for named tunnel |
| `CLAWBOARD_PUBLIC_URL` | — | Static public URL (cloud deployment, no tunnel needed) |
| `CLAWBOARD_TRUST_PROXY` | `loopback` | Express trust proxy setting (`1` for cloud behind reverse proxy) |
| `CLAWBOARD_BACKUP_REPO` | — | HF Dataset repo id for backup (e.g. `user/claw2ui-data`) |
| `HF_TOKEN` | — | HF API token with write access for backup |

---

## Token Management

Claw2UI has three authentication tiers:

| Tier | Access | How to get |
|------|--------|-----------|
| **Admin** | Full access | Set via `CLAWBOARD_TOKEN` env or auto-generated `.api-token` file |
| **Config** | Privileged (list/delete pages) | Added to `claw2ui.config.json` `tokens` array |
| **Registered** | Publish only (50 pages/day) | Self-service via `POST /api/register` |

### Server admin commands (run from project directory)

```bash
claw2ui token create              # Generate a new config token
claw2ui token list                # List config tokens
claw2ui token revoke <token>      # Remove a config token
```

### Admin API endpoints

```bash
# List registered tokens
curl -H "Authorization: Bearer <admin-token>" https://your-server/api/tokens

# Revoke a registered token by short ID
curl -X POST -H "Authorization: Bearer <admin-token>" https://your-server/api/tokens/<id>/revoke
```

### Client connection

Users connect to your server with:

```bash
claw2ui register --server https://your-server-url
# Or with a manually provided token:
claw2ui init --server https://your-server-url --token <token>
```

---

## Backup (HF Dataset)

Backup is **opt-in** — it only activates when both `HF_TOKEN` and `CLAWBOARD_BACKUP_REPO` are explicitly set. Without these, no data leaves the server.

When enabled, Claw2UI automatically:

- **On startup**: downloads `backup.json` from the HF Dataset and restores pages and token metadata
- **On mutation**: debounced (5s) upload of pages and token metadata to `backup.json`

### Setup

1. Create a **private** dataset (public datasets would expose your data):
   ```bash
   hf repos create yourname/claw2ui-data --type dataset --private
   ```

2. Set the env vars / Space Secrets:
   - `HF_TOKEN` — HF token with write access to the dataset
   - `CLAWBOARD_BACKUP_REPO` — `yourname/claw2ui-data`

3. Data is backed up automatically. No further action needed.

### What's backed up

- All page data (HTML, metadata, view counts)
- Registered token metadata (creation time, IP, usage stats, disabled state)

### Security considerations

- The backup dataset **must be private** — it contains page content and token metadata
- Backup is entirely opt-in: if you don't set `HF_TOKEN` and `CLAWBOARD_BACKUP_REPO`, no backup occurs and no data is uploaded anywhere
- The admin token (`CLAWBOARD_TOKEN`) is **never** included in backups — it exists only as an env var or in the local `.api-token` file
- Verify your HF Dataset is set to private: `hf repos settings yourname/claw2ui-data --private`

### Limitations

- Backup is a single `backup.json` file (full snapshot each time)
- If multiple writes happen during an upload, they're queued and backed up after the current upload finishes
- The `@huggingface/hub` package is an optional dependency — backup is a no-op if not installed

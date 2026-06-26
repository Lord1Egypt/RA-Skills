---
name: cloudflare-access-vps
description: >
  Add Cloudflare Zero Trust Access authentication to a VPS-hosted OpenClaw agent. Puts a login
  screen (email OTP, Google SSO, GitHub, or TOTP MFA) in front of the entire domain before any
  traffic reaches the server. Use when: (1) securing a cloud-deployed OpenClaw agent behind an
  identity gate, (2) adding MFA to koda.teamplayers.ai or any agent subdomain, (3) enabling
  per-agent access policies (allowlist by email/domain), (4) generating service tokens for native
  app or API access that bypasses browser login, or (5) troubleshooting Cloudflare Access on an
  existing OpenClaw deployment. Requires Cloudflare Tunnel already running on the VPS.
---

# Cloudflare Access for OpenClaw VPS Agents

Gates the entire domain with Cloudflare Zero Trust Access — every URL, including `/ws`, `/api/`,
and the control UI, requires authentication before a byte reaches the VPS.

## Architecture

```
Browser / app hits https://koda.yourdomain.com
        ↓
Cloudflare Edge
  ├── Access policy check → BLOCKED if unauthenticated (login screen shown)
  └── Authenticated → Cloudflare Tunnel → localhost:18789 → OpenClaw
                                                                ↓
                                                       Gateway token auth (layer 2)
                                                                ↓
                                                       Device pairing  (layer 3)
```

**Prerequisites:** Cloudflare Tunnel active (`cloudflared` service running), domain on Cloudflare DNS.
See `cloudflare-agent-tunnel` skill if tunnel is not yet set up.

---

## Quick Setup (5 Steps)

### Step 1 — Enable Zero Trust

1. [dash.cloudflare.com](https://dash.cloudflare.com) → select your account → **Zero Trust**
2. On first visit, pick a team name (e.g. `teamplayers`) — this becomes `teamplayers.cloudflareaccess.com`
3. Free plan: up to 50 users, no credit card required

### Step 2 — Add an Identity Provider

**Zero Trust → Settings → Authentication → Add new** — pick one:

| Provider | Best for | Setup effort |
|---|---|---|
| One-time PIN (email OTP) | Simplest, no external app | Zero — built-in |
| Google | Teams with Google Workspace | ~5 min (OAuth app in Google Console) |
| GitHub | Developer teams | ~5 min (OAuth app in GitHub) |

> For most solo/small team deployments, **One-time PIN** is sufficient and needs no external setup.

### Step 3 — Create an Access Application

**Zero Trust → Access → Applications → Add an application → Self-hosted**

| Field | Value |
|---|---|
| Application name | `OpenClaw - Koda` (or agent name) |
| Session duration | `24 hours` (reduce for higher security) |
| Application domain | `koda.yourdomain.com` |
| Path | *(leave blank to gate entire domain)* |

Click **Next**.

### Step 4 — Create an Access Policy

**Policy name:** `Owners only` (or similar)

| Rule | Setting |
|---|---|
| Action | Allow |
| Include → Selector | Emails |
| Include → Value | `charles@yourdomain.com` (your email) |

To require MFA: **Add require rule → Authentication Method → mfa** (forces TOTP/hardware key on top of identity provider).

Click **Next → Save**.

### Step 5 — Test

Open a private/incognito window → visit `https://koda.yourdomain.com`.
You should see a Cloudflare login page. After authenticating, OpenClaw loads normally.

---

## Multi-Agent Setup

Each agent subdomain gets its own Access Application with its own policy.

```
koda.teamplayers.ai    → Application: "OpenClaw - Koda"    → Policy: owners only
agent2.teamplayers.ai  → Application: "OpenClaw - Agent 2" → Policy: client X only
```

To add a second agent: repeat Steps 3–4 with the new subdomain.

---

## Service Tokens (for API / Native App Access)

Browser-based Cloudflare login doesn't work for programmatic or native app connections.
Use **Service Tokens** instead — static credentials sent as HTTP headers.

**Zero Trust → Access → Service Auth → Create Service Token**

Copy the `CF-Access-Client-Id` and `CF-Access-Client-Secret`.

Attach the token to the application:
- In the Access Application, add a second policy:
  - Action: **Allow**, Include → **Service Token** → select the token you created

The caller then sends:
```
CF-Access-Client-Id: <id>.access
CF-Access-Client-Secret: <secret>
```

For WebSocket connections (OpenClaw gateway): pass these as HTTP headers on the WS upgrade request.

Full details → `references/service-tokens.md`

---

## Interaction with OpenClaw Token + Pairing

Cloudflare Access is the **outer** gate. OpenClaw's own auth layers still apply after it:

| Layer | What it blocks |
|---|---|
| Cloudflare Access | Unauthenticated internet users (never reach the UI) |
| Gateway token | Anyone who bypasses Cloudflare (e.g. VPS localhost, misconfigured tunnel) |
| Device pairing | Someone with the token but on an unapproved browser |

For existing deployments, no OpenClaw config changes are needed — Access just wraps the outside.

---

## Troubleshooting

See `references/troubleshooting.md` for common issues including:
- "Access denied" after login
- WebSocket connections failing through Access
- Service token auth not working
- Bypassing Access for localhost development

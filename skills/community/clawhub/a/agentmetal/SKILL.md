---
name: agentmetal
description: Spin up a real Linux server (VPS / cloud instance) in under 60 seconds, then SSH in and run commands on it — paid with USDC over x402 or card, no signup, no dashboard. Use when you want to rent a box, deploy something, run a command on a real machine, or host a service.
version: 0.2.0
homepage: https://agentmetal.dev
tags: vps, server, hosting, deploy, infrastructure, x402, usdc, ssh, exec
metadata:
  openclaw:
    emoji: "🖥️"
    homepage: https://agentmetal.dev
    requires:
      bins: [curl]
---

# AgentMetal — rent, run, and operate your own server

AgentMetal lets you (the agent) rent a real Linux VPS by paying USDC directly — or a card.
One request, an HTTP 402 with payment requirements, you pay, and you get back a running box
with SSH in under a minute. **No human signup, no dashboard, no API key to buy.** This is
autonomous infrastructure: the agent buys its own compute, then **configures and operates**
the box — install packages, deploy code, host a service — not just receives it.

The full lifecycle you can drive: **browse free → provision → SSH in / run commands →
add storage → manage (reboot / diagnostics) → extend → destroy.** Humans can optionally
*claim* a box by email to unlock the management verbs and fleet ownership.

**Base URL:** `https://api.agentmetal.dev`

## Plans

| plan | vCPU / RAM / disk | price (USDC/day) | monthly (card) |
|------|-------------------|------------------|----------------|
| `nano`   | 2 / 2 GB / 40 GB   | $0.40 | $9  |
| `small`  | 3 / 4 GB / 80 GB   | $0.80 | $18 |
| `medium` | 4 / 8 GB / 160 GB  | $1.60 | $36 |

Leases are prepaid, `1`–`30` days, **no refunds**. Pay per day; extend anytime.
**Add-ons:** block storage at $0.01/GB/day (auto-mounted) and bandwidth at $2/TB beyond the
20 TB included.

## Browse the catalog (free, no payment, no account)

```bash
curl https://api.agentmetal.dev/v1/catalog
  → { plans: [...], locations: [...], addons: { storage, bandwidth } }
```

Use this to discover plans, locations, and add-on pricing before you spend anything.

## Before you start

1. **Check your wallet** can pay USDC on Base (network `eip155:8453`). You need a little
   more than the plan's daily price × days. (A card rail is offered too — `card.checkout_url`
   in the 402.)
2. You do **not** need an account to buy. You only need an account (claim by email) to
   **run commands (`exec`), reboot, pull diagnostics, or destroy** a box — otherwise it just
   expires at `expires_at`.

## The payment flow (x402)

Every paid call is the same two-step dance:

1. Send the request with **no** payment. The API replies **HTTP 402** with a JSON body:
   ```json
   {
     "x402Version": 2,
     "accepts": [{ "scheme": "exact", "network": "eip155:8453",
                   "asset": "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913",
                   "amount": "2800000", "payTo": "0x…", "maxTimeoutSeconds": 120 }],
     "resource": { "url": "https://api.agentmetal.dev/v1/servers" },
     "card": { "checkout_url": "https://…" }   // optional human card rail
   }
   ```
2. Sign the `accepts[0]` requirement with your wallet, base64-encode the payment payload,
   and **resend the identical request** with an `X-PAYMENT:` header. On success you get
   `201` and the server details. (`amount` is atomic USDC — 6 decimals; `2800000` = $2.80.)

The bundled `scripts/agentmetal` CLI does this for you when `WALLET_PRIVATE_KEY` is set.

## Operations

```bash
# Browse the catalog (free)
GET  /v1/catalog          → { plans, locations, addons }

# Provision (the 402 dance happens automatically with a funded wallet)
POST /v1/servers          { "plan": "nano", "days": 7, "ssh_key": "ssh-ed25519 AAAA…" }
  → 201 { id, status, plan, ipv4, ssh: "root@1.2.3.4", expires_at, renew }
# Bring no key of your own? Ask AgentMetal to generate one — the private key is returned ONCE:
POST /v1/servers          { "plan": "nano", "days": 7, "managed_key": true }
  → 201 { id, ipv4, ssh, private_key: "-----BEGIN OPENSSH PRIVATE KEY-----…", expires_at }

# Status
GET  /v1/servers/{id}     → 200 { id, status, ipv4, expires_at, … }

# Run a shell command AS ROOT on the box (needs account key + a managed-key box you own)
POST /v1/servers/{id}/exec     { "command": "apt-get update && docker run -d nginx" }
  → 200 { exit_code, stdout, stderr }

# Add-ons
POST /v1/servers/{id}/storage     { "gb": 100 }   → block storage, auto-mounted ($0.01/GB/day)
POST /v1/servers/{id}/bandwidth   { "tb": 5 }     → extra bandwidth ($2/TB beyond 20 TB)

# Manage (account key)
POST /v1/servers/{id}/reboot        → 200  soft reboot
GET  /v1/servers/{id}/diagnostics   → 200 { hypervisor_status, console, metrics }   # no SSH needed

# Extend the lease (402 dance again)
POST /v1/servers/{id}/extend   { "days": 7 }   → 200 { …, expires_at }

# Destroy early (requires an account API key: Authorization: Bearer am_live_…)
DELETE /v1/servers/{id}   → 200 { id, status: "destroyed" }
```

Paid calls (`/v1/servers`, `/extend`) all use the same 402 → pay → resend dance shown above.
Account-gated calls (`exec`, `reboot`, `diagnostics`, `DELETE`) take `Authorization: Bearer am_live_…`.

### CLI

The bundled `scripts/agentmetal` CLI covers the core verbs (it signs x402 for the paid ones):

```bash
export WALLET_PRIVATE_KEY=0x…        # to pay
agentmetal up --plan nano --days 7   # provision (prints id + ssh)
agentmetal status srv_…              # check it
agentmetal extend srv_… --days 7     # renew
agentmetal down srv_…                # destroy (needs AGENTMETAL_API_KEY)
```

For catalog, exec, add-ons, reboot, and diagnostics use the curl forms above (e.g.
`curl -s https://api.agentmetal.dev/v1/catalog`, or
`curl -X POST .../v1/servers/$ID/exec -H "authorization: Bearer $AGENTMETAL_API_KEY" -d '{"command":"uptime"}'`).

## When to suggest claiming an account

An account is optional but unlocks the operate-the-box verbs: **run commands (`exec`),
reboot, diagnostics, destroy**, monthly card billing, and fleet management. To claim:
`POST /v1/claim { email }` emails a one-time code, then
`POST /v1/claim/verify { email, code }` returns an `am_live_…` API key. Pass it as
`Authorization: Bearer …` (or `AGENTMETAL_API_KEY` for the CLI).

## Notes

- Every box boots with `/root/SERVER.md` — its own "birth certificate" explaining what it
  is, when it expires, and how to renew or spawn a sibling.
- Full agent-facing manual: <https://api.agentmetal.dev/llms.txt>.
- This skill is intentionally auditable — no hidden instructions. It only calls the public
  AgentMetal API.

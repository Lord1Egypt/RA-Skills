---
name: buy-domain-helper
description: |
  3-layer site launcher: tunnel any HTML instantly (no account), deploy to Cloudflare Pages (permanent), then buy a domain and link it via DNS. Use when a user wants to share a local page, host a site, or get a custom domain live.
version: 1.0.0
metadata:
  openclaw:
    requires:
      env: []
      bins:
        - node
        - cloudflared
        - wrangler
    emoji: "🌐"
    homepage: https://github.com/wohaoshuai/buy-domain-helper
---

# Buy Domain Helper

3 layers — pick the depth that fits the user's need:

| Layer | What it does | Needs |
|-------|-------------|-------|
| **1 — Tunnel** | Instant public URL for any local dir or port | Nothing (cloudflared auto-installs) |
| **2 — Pages** | Permanent hosting on `*.pages.dev` | Cloudflare account + Pages token |
| **3 — Domain** | Custom domain linked to Pages via DNS | Domain purchased + DNS token |

## Helper script

```bash
node site.js <command> [--token CF_API_TOKEN] [--account CF_ACCOUNT_ID]
```

| Command | Layer | Description |
|---------|-------|-------------|
| `tunnel <dir\|port>` | 1 | Instant public URL via Cloudflare Tunnel |
| `deploy <name> <dir>` | 2 | Deploy to Cloudflare Pages |
| `zone <domain>` | 3 | Get zone ID for a domain |
| `dns-link <zone-id> <project>` | 3 | Add CNAME pointing domain to Pages |
| `pages-domain <project> <domain>` | 3 | Attach custom domain to Pages project |
| `domain-check <domain>` | 3 | Check availability on Cloudflare Registrar |

## Setup

- **Layer 1**: No setup. `cloudflared` installs automatically via Homebrew if missing.
- **Layer 2**: Needs a Cloudflare API token with **Account > Cloudflare Pages > Edit** permission.
- **Layer 3**: Needs a separate token with **Zone > DNS > Edit** permission for the specific domain.

Create tokens at: https://dash.cloudflare.com/profile/api-tokens

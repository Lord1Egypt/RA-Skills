<!--skill-metadata
name: buy-domain-helper
description: |
  3-layer site launcher for any HTML. Tunnel instantly, deploy permanently to Cloudflare Pages, then buy a domain and link it via DNS.

  Trigger conditions:
  - User wants to share a local HTML file or page publicly
  - User says: "host my page", "get a public URL", "buy a domain", "launch my site", "link my domain"
  - User has an index.html or local server they want online

  Layer 1 (Tunnel): No account needed — instant tmp URL
  Layer 2 (Pages): Permanent *.pages.dev URL — needs Cloudflare account
  Layer 3 (Domain): Custom domain — needs domain purchase + DNS token
  Response principle: Always start with the lowest layer needed. Ask before going deeper.
  Language: Match the user's language throughout.
-->

# Buy Domain Helper

> Core tool: `node site.js <command> [--token ...] [--account ...]`
> The agent decides which layer to use. The script calls Cloudflare APIs.

## Install

```bash
# Via skills CLI (Claude Code, Cursor, Copilot, and 38+ agents)
npx skills add wohaoshuai/buy-domain-helper

# Via OpenClaw
clawhub install buy-domain-helper
```

---

## The 3 Layers

```
┌─────────────────────────────────────────────────────┐
│  Layer 3 │ Custom Domain    custom.com → Pages       │
│  Layer 2 │ Pages Hosting    yoursite.pages.dev        │
│  Layer 1 │ Tunnel           https://abc.trycloudflare.com │
└─────────────────────────────────────────────────────┘
       No account ──────────────────► Full setup
```

Start at Layer 1 and go deeper only when the user needs it.

---

## Layer 1 — Tunnel (Instant, No Account)

Use when the user wants a quick public URL without any setup.

**Ask:** "Do you have a folder with HTML files, or a local server port?"

```bash
# Static directory
node site.js tunnel ./my-site

# Local port (e.g. a running dev server)
node site.js tunnel 3000
```

- `cloudflared` installs automatically via Homebrew if not present
- Prints a `https://*.trycloudflare.com` URL in stderr within seconds
- **Temporary** — URL dies when the process stops (Ctrl+C)
- No Cloudflare account required

Present the URL immediately. Ask if they want it permanent (→ Layer 2).

---

## Layer 2 — Pages Hosting (Permanent, Free)

Use when the user wants a permanent URL that survives restarts.

**Ask for:**
1. A project name (e.g. `my-site`) — becomes `my-site.pages.dev`
2. A Cloudflare API token with **Account > Cloudflare Pages > Edit** permission:
   ```
   Create at: https://dash.cloudflare.com/profile/api-tokens
   → Custom token → Account > Cloudflare Pages > Edit
   ```
3. Their Account ID (bottom-right of the Cloudflare dashboard overview)

```bash
node site.js deploy my-site ./my-site --token <PAGES_TOKEN> --account <ACCOUNT_ID>
# → {"url":"https://abc123.my-site.pages.dev","subdomain":"my-site.pages.dev"}
```

Present the live URL. Ask if they want a custom domain (→ Layer 3).

---

## Layer 3 — Custom Domain

### Step 1 — Check & Buy

Check if the domain is available:
```bash
node site.js domain-check mysite.com --token <PAGES_TOKEN> --account <ACCOUNT_ID>
# → {"available": true, "name": "mysite.com"}
```

If available, tell the user the price and send them to buy it:
```
✅ mysite.com is available.

Buy it at Cloudflare Registrar (at-cost pricing, no markup):
https://dash.cloudflare.com/<ACCOUNT_ID>/domains/register?search=mysite.com

Come back once the purchase is complete — I'll link it automatically.
```

> Cloudflare Registrar has no purchase API. The user must buy in the browser.
> Wait for their confirmation before proceeding.

### Step 2 — Request DNS Token

```
To configure DNS automatically, I need a token with DNS edit permission:

1. https://dash.cloudflare.com/profile/api-tokens
2. Create Token → Custom token
3. Permission: Zone → DNS → Edit
4. Zone Resources: mysite.com
5. Paste the token here.
```

### Step 3 — Link Domain to Pages

```bash
# Get zone ID
node site.js zone mysite.com --token <DNS_TOKEN>
# → {"zone_id":"abc123","name":"mysite.com","status":"active"}

# Attach domain to Pages project
node site.js pages-domain my-site mysite.com --token <PAGES_TOKEN> --account <ACCOUNT_ID>
# → {"domain":"mysite.com","status":"initializing"}

# Add CNAME record
node site.js dns-link <zone_id> my-site --token <DNS_TOKEN>
# → {"name":"mysite.com","content":"my-site.pages.dev","proxied":true}
```

### Step 4 — Verify

```bash
curl -sI https://mysite.com | head -2
# HTTP/2 200 ✅
```

If you get `522`: SSL cert is provisioning — wait 30s and retry.

### Present result

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🌐 Your site is live!

  https://mysite.com

Powered by Cloudflare Pages.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
To update the site, run:
  node site.js deploy my-site <dir> --token ...
```

---

## Error Handling

| Error | Cause | Fix |
|-------|-------|-----|
| `zone_id: null` | Domain not active yet | Wait 1–2 min, retry `site.js zone` |
| `HTTP 522` | SSL provisioning | Wait 30s, retry curl |
| `already exists` on deploy | Project exists | Skip creation, continue deploy |
| DNS auth error | Wrong token scope | Ask user to create token with Zone > DNS > Edit |
| `domain-check` error | Unsupported TLD | Suggest `.com`, `.net`, `.org`, `.io`, `.cc`, `.ai` |

---

## Token Reference

| Token | Permission | Used for |
|-------|-----------|----------|
| Pages token | Account > Cloudflare Pages > Edit | `deploy`, `pages-domain` |
| DNS token | Zone > DNS > Edit (specific zone) | `zone`, `dns-link` |

> The wrangler OAuth token (`wrangler login`) covers Pages deploys but **never** DNS edit.
> Always request a separate custom DNS token for Layer 3.

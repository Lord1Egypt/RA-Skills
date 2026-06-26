---
name: domani
description: Domains and emails for AI agents. Search, register, and manage domains. Create mailboxes, send and receive emails. Use when user asks to "find a domain", "buy a domain", "register a domain", "check domain availability", "set up DNS", "connect to Vercel", "create a mailbox", "send an email", "check my inbox", "set up email for my domain", "transfer a domain", "renew my domain", "check WHOIS", "import a domain", or "manage DNS records".
compatibility: Requires curl and network access. Works on Claude.ai, Claude Code, and API.
homepage: https://domani.run
metadata: {"version":"0.1.0","updated":"2026-03-11","author":"domani","openclaw":{"requires":{"bins":["curl"]},"primaryEnv":"DOMANI_API_KEY","emoji":"incoming_envelope","homepage":"https://domani.run"}}
---

# domani.run - Domains & Emails for AI Agents

Internet identity for AI agents. One API to buy domains, create mailboxes, and send & receive emails. Every user gets a free email address on @domani.run — no domain purchase required.

> **Skill version 0.1.0 (2026-03-11).** If the user asks to check for updates, fetch `https://domani.run/SKILL.md` and compare the `updated` date in the frontmatter with the one above. If newer, run: `npx skills add domani.run`

## Installation

This skill can be installed through multiple channels:

- **Claude Code**: `npx skills add domani.run` or copy this file to `.claude/skills/domani/SKILL.md`
- **OpenClaw / ClawHub**: `clawhub install domani`
- **Claude.ai**: Download [domani-skill.zip](https://domani.run/domani-skill.zip) → Settings > Features > Upload skill
- **MCP** (alternative to this skill): Connect directly via Streamable HTTP - see [MCP setup](https://domani.run/.well-known/mcp.json)

All methods use the same API and API key. Choose one - you don't need both Skill and MCP.

## Setup

### What you can do without an API key

Many endpoints are **public and require no authentication**. You can start immediately:

- **Search domains**: `GET /api/domains/search?domains=name.com,name.dev`
- **Check availability**: `GET /api/domains/dns-check?names=name&tlds=com,dev,ai`
- **List TLDs + pricing**: `GET /api/domains/tlds`
- **WHOIS lookup**: `GET /api/domains/whois?domain=example.com`
- **AI suggestions**: `GET /api/domains/suggest?prompt=...`

**Only authenticate when the user wants to take action** (buy, configure DNS, create mailbox, send email, etc.). Don't look for an API key just to search or browse.

### What you need an API key for

- **Domains**: Buy, configure DNS, connect to hosting, transfer, renew
- **Email**: Create mailboxes (1 free @domani.run), send & receive, forward, reply, webhooks
- **Account**: Manage billing, WHOIS contact, API tokens

### Getting an API key (when needed)

**Check for existing authentication first** - the user may already be logged in:

1. Check environment variable: `$DOMANI_API_KEY`
2. Check the CLI config file: `~/.domani/config.json` - if it exists, read the `token` field:
   ```bash
   cat ~/.domani/config.json 2>/dev/null
   # Returns: {"token":"domani_sk_xxx","email":"user@example.com"}
   ```
3. Validate the token still works:
   ```bash
   curl -s https://domani.run/api/me -H "Authorization: Bearer TOKEN_FROM_CONFIG"
   ```
   If this returns account info, you're authenticated. Skip to account readiness check.

**If no existing token found**, create an account or log in:

**New user:**
```bash
curl -X POST https://domani.run/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email": "USER_EMAIL"}'
```

Returns `api_key` (format: `domani_sk_...`). If the user already has an account (409 response), use the login flow below.

**Existing user (409 on register, or user says they have an account):**
```bash
# Step A: Start device login - get a code
curl -s -X POST https://domani.run/api/auth/cli
# Returns: {"code":"XXXX","auth_url":"https://domani.run/auth/callback?code=XXXX","expires_in":600}

# Step B: Tell the user to open the auth_url in their browser and approve

# Step C: Poll until approved (every 5 seconds, up to 10 minutes)
curl -s "https://domani.run/api/auth/cli/poll?code=XXXX"
# Pending: {"status":"pending"}
# Approved: {"status":"complete","token":"domani_sk_xxx","email":"user@example.com"}
```

**Store the token** so the CLI and future agent sessions share the same auth:
```bash
mkdir -p ~/.domani && chmod 700 ~/.domani
echo '{"token":"domani_sk_xxx","email":"user@example.com"}' > ~/.domani/config.json
chmod 600 ~/.domani/config.json
```

**Use the token for all authenticated API calls** - add this header to every request:
```
Authorization: Bearer domani_sk_xxx
```

All the `curl` examples below use `$DOMANI_API_KEY` as a placeholder - replace it with the actual token you found or received.

### Check account readiness

```bash
curl -s https://domani.run/api/me \
  -H "Authorization: Bearer $DOMANI_API_KEY"
```

This single call tells you everything about the account: `email`, `has_payment_method`, `has_contact`, `setup_required` (array of what's missing), `domain_count`, `referral_code`. A payment method is required before purchasing. WHOIS contact is optional for purchases (a default is used) but recommended for ICANN compliance and required before transfers.

### Step 3: Payment method

Two options: **card** or **USDC**. The user does NOT need both - either one works.

**Card** (required for bulk purchases of 2+ domains):

```bash
curl -s -X POST https://domani.run/api/billing/setup \
  -H "Authorization: Bearer $DOMANI_API_KEY"
```

Returns `{ "url": "https://checkout.stripe.com/..." }`. **Tell the user to open this URL in their browser** to add their card. After they complete the form, verify with `GET /api/me` that `has_payment_method` is `true`.

### Step 4: Set WHOIS contact info (optional, can be done after purchase)

```bash
curl -s -X PUT https://domani.run/api/me/contact \
  -H "Authorization: Bearer $DOMANI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"first_name":"Jane","last_name":"Doe","address1":"123 Main St","city":"New York","state":"NY","postal_code":"10001","country":"US","phone":"+1.2125551234","email":"jane@example.com"}'
```

Recommended for ICANN compliance and required before domain transfers. You can purchase domains without setting contact info - a default contact is used until you set your own (WHOIS privacy hides it by default). When updated, the new contact is automatically propagated to all active domains at supported registrars. Required fields: `first_name`, `last_name`, `address1`, `city`, `state`, `postal_code`, `country` (2-letter ISO), `phone` (E.164: +1.2125551234), `email`. Optional: `org_name`, `address2`.

**Do not ask users for contact info before purchasing a domain.** Let them buy first, set contact later.

## Critical Rules

- **You are the agent - do the work yourself.** Never tell the user to run commands, scripts, or terminal operations. If you need to run code (install packages, execute a script, call an API), do it yourself. The user interacts with you through natural language - you handle the technical execution. This applies whether the user is a human or another agent using this skill programmatically.
- **Always confirm purchases and transfers with the user** before calling `/api/domains/buy` or `/api/domains/transfer`
- **Show price clearly** before buying or transferring - for transfers, check eligibility and price via `GET /api/domains/transfer-check?domain=example.com` first

- **Don't authenticate for read-only operations** - search, dns-check, tlds, whois, and suggest are public endpoints. Only look for an API key when the user wants to take an action (buy, DNS, email, etc.)
- **When auth is needed, check for existing auth first** - read `~/.domani/config.json` or `$DOMANI_API_KEY` before asking the user to register or log in
- **GET before PUT for DNS** - `PUT /dns` replaces ALL records. Always `GET` first and merge existing records with new ones, or the user will lose their current DNS setup
- **Brainstorm names yourself by default** - you know the user's context better than any API. Generate names, then verify with `dns-check` + `search`. Only use `suggest` for specific styles or languages
- **Use `dns-check` first, then `search`** - `dns-check` is instant (~1s). Then call `search` only on candidates to get pricing
- **Always relay `next_steps` and `hint`** from API responses - they contain actionable guidance
- **Post-purchase checklist** - after buying: (1) confirm WHOIS privacy is on, (2) confirm auto-renew is on, (3) ask what to connect it to (hosting, email, or both)
- **Import vs Transfer** - recommend import (free, non-invasive) for monitoring. Recommend transfer only when the user explicitly wants to leave their current registrar
- **Email first for quick starts** - if a user just wants an email address, they don't need to buy a domain. Create a free @domani.run mailbox immediately. Suggest a custom domain later
- **Email is built-in, not an add-on** - don't treat email as secondary to domains. When setting up a new domain, proactively offer email setup alongside hosting

## Limitations

| Not supported | What to tell the user |
|---------------|----------------------|
| Delete a registered domain | Domains can't be deleted - they expire naturally. Disable auto-renew if not wanted |
| Change nameservers (imported domains) | Must be done at the original registrar |
| URL redirects / forwarding | Set up through the hosting provider (Vercel, Netlify, Cloudflare) |
| SSL certificates | Auto-provisioned by the hosting provider. Check their dashboard if issues |

## Workflow

### 1. Check account status

```bash
curl -s https://domani.run/api/me \
  -H "Authorization: Bearer $DOMANI_API_KEY"
```

If `setup_required` is not empty, follow Setup steps 3-4 above before proceeding. The response tells you exactly what's missing.

### 1b. List my domains

```bash
curl -s https://domani.run/api/domains \
  -H "Authorization: Bearer $DOMANI_API_KEY"
```

Returns all domains the user owns with status, expiry, and provider info. Use this when the user asks "what domains do I have?" or needs to pick a domain for further operations.

### 2. Find domain names

When the user wants domain name ideas, **brainstorm names yourself** - you know the user's project and context better than any API. Then verify availability using the fast endpoints below.

**Step 1: Brainstorm 10-20 names yourself**

Generate creative domain name ideas based on the user's project. Think about:
- Short, memorable names (3-14 chars): wordplay, portmanteaus, metaphors, neologisms
- Creative TLD plays: `.ai` ($74), `.dev` ($13), `.io` ($30), `.sh` ($33), `.co` ($24), `.app` ($13), `.xyz` ($4), `.run` ($6)
- Single evocative words, invented brandable words, or clever combinations

**Step 2: Quick-check availability (fast, ~1 second)**

```bash
# Test a name across basic TLDs (com, io, dev, ai, sh, co, net, org, app, xyz)
curl -s "https://domani.run/api/domains/dns-check?name=IDEA_NAME&preset=basic"

# If most basic TLDs are taken, try extended preset (30+ creative/exotic TLDs)
curl -s "https://domani.run/api/domains/dns-check?name=IDEA_NAME&preset=extended"
```

The `preset` parameter expands to curated TLD lists:
- `basic` (default): com, io, dev, ai, sh, co, net, org, app, xyz
- `extended`: basic + tech, run, cloud, so, code, software, pro, one, biz, design, studio, art, space, lol, site, gg, cc, me, tv, fm, 1

**Step 3: Get pricing for available candidates**

```bash
curl -s "https://domani.run/api/domains/search?domains=IDEA.dev,IDEA.ai,IDEA.sh&max_price=30"
```

**Step 4: Research taken domains (optional but valuable)**

When a name the user likes is taken, investigate what's behind it:

```bash
# WHOIS - who owns it, when it expires, is it expiring soon?
curl -s "https://domani.run/api/domains/whois?q=TAKEN_DOMAIN.com"

# OG preview - what's the site about? Is it actively used or parked?
curl -s "https://domani.run/api/domains/TAKEN_DOMAIN.com/og"
```

This helps the user decide:
- **Expiring soon** (check `days_until_expiry`) → "This domain expires in 30 days, you could try to register it then"
- **Parked/empty** (OG returns no title or generic parking page) → domain is squatted, suggest alternatives
- **Active site** (OG returns real title/description) → name is genuinely in use, move on
- **Different TLD available** → "example.com is taken (it's a SaaS tool) but example.dev is available for $13"

**Step 4b: Brand safety check (recommended before purchase)**

Before recommending a domain for purchase, use your web search capabilities to check if the name conflicts with existing businesses or trademarks. Search for:

- `"IDEA_NAME"` (exact match - is there an established company?)
- `"IDEA_NAME" company` or `"IDEA_NAME" app` or `"IDEA_NAME" startup`
- Check the first page of results for: active companies, funded startups, popular apps, or trademark holders

**What to look for:**
- Active website at name.com → strong conflict signal
- LinkedIn/Crunchbase/GitHub company profiles → existing business
- App Store / Product Hunt listings → name is in use
- No significant results → likely safe to use

If you find a direct competitor or trademark holder in the same space, warn the user and suggest alternatives.

**Step 5: Present results and iterate**

Show available domains with prices as soon as you have them. If the user wants more ideas:
- Brainstorm new names, **excluding domains you already suggested**
- Repeat steps 2-4
- Keep iterating until the user is satisfied

This approach is fast (~5-10 seconds per batch) because you brainstorm instantly and `dns-check` is a sub-second DNS lookup.

**Alternative: Use the suggest API for specific styles**

When the user asks for a specific creative style or cultural inspiration, use the suggest endpoint - it has specialized prompting for these:

```bash
# Creative style: single, creative, short, brandable, keyword
curl -s "https://domani.run/api/domains/suggest?prompt=DESCRIPTION&style=japanese&count=10"

# To get more, pass previously returned domains as exclude
curl -s "https://domani.run/api/domains/suggest?prompt=DESCRIPTION&style=japanese&exclude=a.com,b.dev,c.ai"
```

| Parameter | Required | Description |
|-----------|----------|-------------|
| `prompt` | **Yes** | Project description or keywords (min 3 chars) |
| `count` | No | Number of suggestions (1-20, default 10) |
| `tlds` | No | Preferred TLDs, comma-separated (e.g. `com,dev,ai`) |
| `style` | No | `single`, `creative`, `short`, `brandable`, or `keyword` |
| `lang` | No | Cultural inspiration: `japanese`, `spanish`, `french`, `italian`, `latin`, `nordic`, `arabic`, `sanskrit` |
| `exclude` | No | Domains to skip, comma-separated (use when asking for more) |

Public endpoint, no auth needed, rate limit 10/min. Note: this endpoint can take 15-30 seconds (it runs its own AI + availability checks). Prefer the agent-driven approach above for faster results.

### 3. Search specific domains

Use this when the user already has a specific domain name in mind and wants to check availability/pricing.

```bash
# Check multiple TLDs at once (public, no auth needed)
curl -s "https://domani.run/api/domains/search?domains=PROJECT_NAME.com,PROJECT_NAME.dev,PROJECT_NAME.ai,PROJECT_NAME.io,PROJECT_NAME.sh,PROJECT_NAME.co&max_price=30"

# Check a single domain
curl -s "https://domani.run/api/domains/search?q=PROJECT_NAME.dev"

# Stream results in real-time (SSE)
curl -s -H "Accept: text/event-stream" "https://domani.run/api/domains/search?domains=PROJECT_NAME.com,PROJECT_NAME.dev,PROJECT_NAME.ai"
```

Public endpoint - no auth needed. Rate limit: 20/min per IP (60/min with auth). Use `?q=` for a single domain or `?domains=` for multiple. Add `Accept: text/event-stream` header for real-time streaming. Optional params: `sort=price` and `order=asc|desc` to sort results.

**Quick existence check** - to quickly test if a name is taken across many TLDs at once (faster than search, no pricing):

```bash
curl -s "https://domani.run/api/domains/dns-check?name=PROJECT_NAME&tlds=com,dev,ai,io,sh,co,app,xyz"
```

Returns `taken` (registered) and `candidates` (potentially available) arrays. Use this first to narrow down, then `search` the candidates to get prices.

### 3b. Browse TLDs & pricing

```bash
# List all supported TLDs with pricing
curl -s "https://domani.run/api/tlds?sort=price&order=asc&max_price=20"

# Search for specific TLDs
curl -s "https://domani.run/api/tlds?search=dev&sort=price"

# Paginate through results
curl -s "https://domani.run/api/tlds?limit=20&offset=0"
```

Public endpoint. Use when the user asks "what TLDs do you support?", "what's the cheapest domain?", or "how much is a .ai domain?". Returns `tld`, `registration` price, and `renewal` price. Optional params: `min_price`, `max_price`, `sort` (tld|price|renewal), `order` (asc|desc), `search`, `limit`, `offset`.

### 4. Purchase

**Always confirm with the user before purchasing.** Show the domain and price, then proceed.

#### Purchase with card

```bash
curl -s -X POST https://domani.run/api/domains/buy \
  -H "Authorization: Bearer $DOMANI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"domain": "PROJECT_NAME.dev"}'
```

If the user has a card on file, this charges it immediately.

#### Options

- `years` (1-10, default 1): register for multiple years. Price is multiplied by years.
- Bulk purchases (`"domains": ["a.com", "b.dev"]`, max 10): card only, each domain processed independently.

### 5. Connect to a provider

```bash
# Auto-detect from target URL
curl -s -X POST "https://domani.run/api/domains/PROJECT_NAME.dev/connect" \
  -H "Authorization: Bearer $DOMANI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"target": "my-app.vercel.app"}'

# Or explicit provider
curl -s -X POST "https://domani.run/api/domains/PROJECT_NAME.dev/connect" \
  -H "Authorization: Bearer $DOMANI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"provider": "google-workspace"}'
```

Supported providers:
- **Hosting**: vercel, netlify, cloudflare-pages, github-pages, railway, fly
- **Email**: google-workspace, fastmail, proton

**List available providers** before choosing:

```bash
curl -s "https://domani.run/api/domains/PROJECT_NAME.dev/connect" \
  -H "Authorization: Bearer $DOMANI_API_KEY"
```

Some providers offer multiple methods (e.g. CNAME vs A records). Specify with `"method": "method_name"` in the POST body. The GET response shows available methods per provider.

The response includes a `next_steps` array with provider-specific actions to complete (e.g., registering the domain on the provider side). **Always check and relay these steps to the user** - they contain direct URLs and exact instructions. Some providers (cloudflare-pages, github-pages, railway, fly) require a `target` parameter - the error will explain how to obtain it.

### 5b. Manage DNS records directly

Use this when the user wants to set **specific DNS records** (e.g., "add an A record pointing to 1.2.3.4"). Do NOT use `connect` for this - `connect` is for provider presets (Vercel, Google Workspace, etc.).

```bash
# Get current DNS records
curl -s "https://domani.run/api/domains/PROJECT_NAME.dev/dns" \
  -H "Authorization: Bearer $DOMANI_API_KEY"

# Set DNS records (replaces all records)
curl -s -X PUT "https://domani.run/api/domains/PROJECT_NAME.dev/dns" \
  -H "Authorization: Bearer $DOMANI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"records": [
    {"type": "A", "name": "@", "value": "1.2.3.4", "ttl": 3600},
    {"type": "CNAME", "name": "www", "value": "PROJECT_NAME.dev", "ttl": 3600},
    {"type": "TXT", "name": "@", "value": "v=spf1 include:_spf.google.com ~all", "ttl": 3600}
  ]}'
```

Supported record types: `A`, `AAAA`, `CNAME`, `MX` (with `priority`), `TXT`, `NS`. PUT replaces all records - always GET first, then include existing records you want to keep alongside new ones.

### 5c. Manage nameservers

Use this when a domain has no nameservers assigned (DNS operations will fail) or to switch nameserver providers.

```bash
# Get current nameservers
curl -s "https://domani.run/api/domains/PROJECT_NAME.dev/nameservers" \
  -H "Authorization: Bearer $DOMANI_API_KEY"

# Set nameservers (2-13 required)
curl -s -X PUT "https://domani.run/api/domains/PROJECT_NAME.dev/nameservers" \
  -H "Authorization: Bearer $DOMANI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"nameservers": ["ns1.systemdns.com", "ns2.systemdns.com", "ns3.systemdns.com"]}'
```

If `get_nameservers` returns an empty array, the domain cannot serve DNS. Assign nameservers before using parking, email, or connect.

### 6. Email

Email is a core feature — every user gets a free mailbox on @domani.run, no domain purchase required. Buy a domain to create mailboxes on your own domain.

#### Get started with email (no domain needed)

```bash
# Create a free @domani.run mailbox
curl -s -X POST "https://domani.run/api/email" \
  -H "Authorization: Bearer $DOMANI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"slug": "yourname"}'
# Creates yourname@domani.run
```

#### Email on your own domain

```bash
# Set up email DNS (MX, SPF, DKIM, DMARC - auto-configured)
curl -s -X POST "https://domani.run/api/domains/PROJECT_NAME.dev/email/setup" \
  -H "Authorization: Bearer $DOMANI_API_KEY"

# Create a mailbox
curl -s -X POST "https://domani.run/api/domains/PROJECT_NAME.dev/email" \
  -H "Authorization: Bearer $DOMANI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"slug": "hello"}'
# Creates hello@PROJECT_NAME.dev
```

#### Or connect an external provider (Google Workspace, Proton, Fastmail)

```bash
curl -s -X POST "https://domani.run/api/domains/PROJECT_NAME.dev/connect" \
  -H "Authorization: Bearer $DOMANI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"provider": "google-workspace"}'
```

#### Send, read, reply, forward

```bash
# Send an email
curl -s -X POST "https://domani.run/api/domains/PROJECT_NAME.dev/email/hello/send" \
  -H "Authorization: Bearer $DOMANI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"to": "recipient@example.com", "subject": "Hello", "text": "Message body"}'

# Read inbox
curl -s "https://domani.run/api/domains/PROJECT_NAME.dev/email/hello/messages" \
  -H "Authorization: Bearer $DOMANI_API_KEY"

# Reply to a message
curl -s -X POST "https://domani.run/api/domains/PROJECT_NAME.dev/email/hello/messages/MSG_ID/reply" \
  -H "Authorization: Bearer $DOMANI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"text": "Thanks for your email!"}'

# Forward a message
curl -s -X POST "https://domani.run/api/domains/PROJECT_NAME.dev/email/hello/messages/MSG_ID/forward" \
  -H "Authorization: Bearer $DOMANI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"to": "someone@example.com"}'
```

#### Manage mailboxes

```bash
# List all mailboxes
curl -s "https://domani.run/api/email" \
  -H "Authorization: Bearer $DOMANI_API_KEY"

# Forward inbound emails to another address
curl -s -X PUT "https://domani.run/api/domains/PROJECT_NAME.dev/email/hello" \
  -H "Authorization: Bearer $DOMANI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"forward_to": "personal@gmail.com"}'

# Set up inbound webhook
curl -s -X PUT "https://domani.run/api/domains/PROJECT_NAME.dev/email/hello" \
  -H "Authorization: Bearer $DOMANI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"webhook_url": "https://your-app.com/api/inbound-email"}'

# Check email health (MX, SPF, DKIM, DMARC)
curl -s "https://domani.run/api/domains/PROJECT_NAME.dev/email/check" \
  -H "Authorization: Bearer $DOMANI_API_KEY"

# Delete a mailbox
curl -s -X DELETE "https://domani.run/api/domains/PROJECT_NAME.dev/email/hello" \
  -H "Authorization: Bearer $DOMANI_API_KEY"
```

**Limits:** Max 5 mailboxes per account. 1 free @domani.run mailbox per user. Buy a domain for more. Attachments: max 10 files, 10 MB each, 40 MB total. Rate limit: 100 sends/hour per mailbox.

**Message statuses:** `queued` → `sent` → `delivered`. Failures: `bounced`, `failed`, `delayed`, `complained`, `suppressed`.

**Web inbox:** Users can also read and send emails at [https://domani.run/inbox](https://domani.run/inbox).

For full email operations reference, see: [Email Reference](https://domani.run/references/email.md)

### 7. Verify connection

```bash
curl -s -X POST "https://domani.run/api/domains/PROJECT_NAME.dev/verify" \
  -H "Authorization: Bearer $DOMANI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"target": "my-app.vercel.app"}'
```

### 8. Verify domain for a service (Stripe, Google, etc.)

```bash
curl -s -X POST "https://domani.run/api/domains/PROJECT_NAME.dev/verify-service" \
  -H "Authorization: Bearer $DOMANI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"service": "stripe", "token": "abc123def456"}'
```

Supported: stripe, google-search-console, aws-ses, postmark, resend, facebook, hubspot, microsoft-365. Unknown service names fall back to a generic TXT record.

### 9. WHOIS / RDAP lookup

```bash
curl -s "https://domani.run/api/domains/whois?q=example.com"
```

Public endpoint - no auth needed. Returns full registration data for any domain:

- **registrar**: name, URL, IANA ID
- **dates**: created, expires, updated, days_until_expiry
- **status**: EPP status codes (clientTransferProhibited, etc.)
- **nameservers**: authoritative NS records
- **dnssec**: whether DNSSEC is enabled
- **redacted**: whether data is privacy-redacted (GDPR)
- **contacts**: registrant, admin, tech, billing, abuse - each with name, organization, email, phone, fax, street, city, state, postal_code, country (fields may be null when redacted)

Uses RDAP (modern JSON protocol) with automatic WHOIS port 43 fallback. Cached server-side (1h registered, 5min not-found). Rate limit: 30/min.

### 10. Get domain details

```bash
curl -s "https://domani.run/api/domains/PROJECT_NAME.dev" \
  -H "Authorization: Bearer $DOMANI_API_KEY"
```

Returns detailed info about a domain you own:

- **status**: `active`, `expired`, or `pending`
- **auto_renew**: whether auto-renew is enabled
- **purchased_at** / **expires_at**: purchase and expiry dates
- **days_until_expiry**: days remaining
- **payment_method**: `stripe`
- **registrar**: security_lock, whois_privacy, auto_renew, create_date, expire_date (null if registrar data unavailable)

Rate limit: 60/min.

### 11. Toggle auto-renew

```bash
# Disable auto-renew
curl -s -X PUT "https://domani.run/api/domains/PROJECT_NAME.dev/settings" \
  -H "Authorization: Bearer $DOMANI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"auto_renew": false}'

# Enable auto-renew
curl -s -X PUT "https://domani.run/api/domains/PROJECT_NAME.dev/settings" \
  -H "Authorization: Bearer $DOMANI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"auto_renew": true}'
```

The change is applied at the registrar first. If it fails, the local setting is not updated. Rate limit: 60/min.

### 11b. Toggle WHOIS privacy

```bash
# Disable WHOIS privacy (makes your contact info public)
curl -s -X PUT "https://domani.run/api/domains/PROJECT_NAME.dev/settings" \
  -H "Authorization: Bearer $DOMANI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"whois_privacy": false}'

# Enable WHOIS privacy (hides your contact info from WHOIS)
curl -s -X PUT "https://domani.run/api/domains/PROJECT_NAME.dev/settings" \
  -H "Authorization: Bearer $DOMANI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"whois_privacy": true}'
```

WHOIS privacy is enabled by default on new registrations. Rate limit: 60/min.

### 11c. Toggle security lock

```bash
# Unlock domain (required before transferring away)
curl -s -X PUT "${APP_URL}/api/domains/PROJECT_NAME.dev/settings" \
  -H "Authorization: Bearer $DOMANI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"security_lock": false}'

# Lock domain (prevents unauthorized transfers)
curl -s -X PUT "${APP_URL}/api/domains/PROJECT_NAME.dev/settings" \
  -H "Authorization: Bearer $DOMANI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"security_lock": true}'
```

Security lock (`clientTransferProhibited`) prevents unauthorized domain transfers. Enabled by default. Must be unlocked before transferring the domain away. Rate limit: 60/min.

### 11d. Update WHOIS contact info

See **Setup Step 4** above for the full contact setup. To update existing contact info, use the same `PUT /api/me/contact` endpoint. To check current contact info: `GET /api/me/contact`.

When a contact email differs from the login email, a verification email is sent automatically. The `get_account` response includes `contact_email_verified` (boolean) and a `setup_required` hint until verified.

### 11e. Resend email verification

```bash
# Resend verification for your contact email
curl -s -X POST "${APP_URL}/api/me/resend-verification" \
  -H "Authorization: Bearer $DOMANI_API_KEY"

# Or specify a different email
curl -s -X POST "${APP_URL}/api/me/resend-verification" \
  -H "Authorization: Bearer $DOMANI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"email": "contact@example.com"}'
```

Rate limited to once per 15 minutes per email. Returns `{ "sent": true }` or `{ "already_verified": true }`.

### 12. Renew a domain

```bash
# Renew for 1 year (default)
curl -s -X POST "https://domani.run/api/domains/PROJECT_NAME.dev/renew" \
  -H "Authorization: Bearer $DOMANI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"years": 1}'

# Renew for 3 years
curl -s -X POST "https://domani.run/api/domains/PROJECT_NAME.dev/renew" \
  -H "Authorization: Bearer $DOMANI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"years": 3}'
```



Returns `renewed_years`, `new_expiry`, `price`, `currency`. Payment is charged upfront. Rate limit: 10/min.

**Bring an existing domain**: Use **import** (free, keep current registrar) for monitoring, or **transfer** (paid - includes 1 year renewal, EPP code required, full migration) to manage everything through domani.run.

### 13. Import an existing domain (free)

Already own a domain at another registrar? Import it for status monitoring, email health, and expiry alerts - free, domain stays at your current registrar.

```bash
# Step 1: Initiate import - get a verification TXT record
curl -s -X POST https://domani.run/api/domains/import \
  -H "Authorization: Bearer $DOMANI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"domain": "mysite.com"}'
```

Response includes a TXT record to add at your current DNS provider (GoDaddy, Namecheap, Cloudflare, etc.):

```json
{
  "domain": "mysite.com",
  "status": "pending_verification",
  "txt_record": { "type": "TXT", "name": "@", "value": "domani-verify=a1b2c3d4..." }
}
```

```bash
# Step 2: After adding the TXT record, verify ownership
curl -s -X POST https://domani.run/api/domains/import/verify \
  -H "Authorization: Bearer $DOMANI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"domain": "mysite.com"}'
```

Once verified, the domain appears in your account. Use `connect` to get the exact DNS records for your hosting provider:

```bash
# Step 3: Get DNS records for your provider (returns instructions, not applied)
curl -s -X POST "https://domani.run/api/domains/mysite.com/connect" \
  -H "Authorization: Bearer $DOMANI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"target": "my-app.vercel.app"}'
```

For imported domains, the response has `status: "manual_setup_required"` with the records to add at your registrar. After adding them, verify propagation:

```bash
# Step 4: Verify DNS propagation
curl -s -X POST "https://domani.run/api/domains/mysite.com/verify" \
  -H "Authorization: Bearer $DOMANI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"target": "my-app.vercel.app"}'
```

No lock-in - your domain stays at your current registrar. You can also check email health and expiration at any time.

### 14. Transfer a domain (full migration)

**Step 1: Check eligibility and price**

```bash
curl -s "https://domani.run/api/domains/transfer-check?domain=mysite.com" \
  -H "Authorization: Bearer $DOMANI_API_KEY"
# Returns: {"domain": "mysite.com", "tld": "com", "eligible": true, "price": 13.08, "currency": "USD", "hint": "..."}
```

Returns `eligible` (boolean), `price` (transfer cost in USD), and blockers if not eligible: `code` (UNSUPPORTED_TLD, TRANSFER_NOT_ELIGIBLE, ALREADY_REGISTERED), `eligible_at` (ICANN waiting period date), `hint`. **Always call this before initiating a transfer.**

**Step 2: Initiate the transfer**

```bash
curl -s -X POST "https://domani.run/api/domains/transfer" \
  -H "Authorization: Bearer $DOMANI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"domain": "mysite.com", "auth_code": "EPP-AUTH-CODE", "payment_method": "card"}'
```



**Transfers are paid** - the transfer price includes 1 year of registration renewal (standard across all registrars). Check eligibility and price first via `GET /api/domains/transfer-check?domain=example.com`, then **show the price to the user and get explicit confirmation before calling this endpoint**.

Get the authorization/EPP code from your current registrar first. Transfer typically takes 1-5 days. Returns 202 with `status: "pending"`. Rate limit: 5/min.

**DNS auto-migration**: We automatically snapshot all existing DNS records before initiating the transfer. When the transfer completes, records are restored at the new registrar. Pass `extra_subdomains` to include custom subdomains we might not auto-discover.

**Check transfer status**: `GET /api/domains/{domain}/transfer-status` - statuses: `pending_owner`, `pending_admin`, `pending_registry`, `completed`, `cancelled`.

For registrar-specific EPP code instructions (GoDaddy, Namecheap, Cloudflare, etc.), transfer status monitoring, and troubleshooting, see: [Transfer Reference](https://domani.run/references/transfer.md)

### 14a. Watch a domain for transfer eligibility

If a domain is not yet eligible for transfer (ICANN 60-day lock, registrar lock, etc.), you can watch it and get notified when it becomes transferable.

```bash
curl -s -X POST "https://domani.run/api/domains/transfer-watch" \
  -H "Authorization: Bearer $DOMANI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"domain": "example.com"}'
# Returns: {"domain": "example.com", "eligible": false, "eligible_at": "2025-05-15", "hint": "...", "watching": true}
```

Uses RDAP to check EPP status codes and ICANN lock periods independently of any registrar. If the domain is already eligible, returns `eligible: true` without creating a watch. If not eligible but has a known date, creates a watch - you'll be notified via email and `transfer.eligible` webhook when it's ready. Rate limit: 30/min.

### 14b. Transfer a domain away

To transfer a domain OUT to another registrar:

```bash
# Step 1: Get the EPP auth code (auto-unlocks if locked)
curl -s "${APP_URL}/api/domains/PROJECT_NAME.dev/auth-code" \
  -H "Authorization: Bearer $DOMANI_API_KEY"
# Returns: {"auth_code": "epp-xxx", "was_unlocked": true, ...}

# Step 2: Give the auth code to the new registrar and initiate the transfer there

# Step 3: Monitor transfer progress
curl -s "${APP_URL}/api/domains/PROJECT_NAME.dev/transfer-away" \
  -H "Authorization: Bearer $DOMANI_API_KEY"
# Returns: {"status": "pending", "gaining_registrar": "Namecheap", ...}
```

The auth code endpoint automatically unlocks the domain if it has a security lock. Transfer typically takes 5-7 days. Statuses: `none`, `pending`, `approved`, `completed`, `rejected`, `expired`. Rate limits: auth-code 10/min, transfer-away 30/min.

### 15. Check domain status

```bash
curl -s "https://domani.run/api/domains/PROJECT_NAME.dev/status" \
  -H "Authorization: Bearer $DOMANI_API_KEY"
```

Returns DNS propagation, SSL status, email configuration, and days until expiry.

## Common Scenarios

### Launch a project (end-to-end)

The most common flow - user is building an app and needs a domain fully set up:

1. **Find & buy a domain** → Section 2 (brainstorm) or 3 (specific name) → Section 4 (purchase)
2. **Connect to hosting** → `POST /api/domains/{domain}/connect` with `{"target": "my-app.vercel.app"}`
3. **Follow next_steps** - the response includes provider-specific instructions (e.g. "Add domain in Vercel dashboard"). Always relay these to the user
4. **Verify connection** → `POST /api/domains/{domain}/verify` - check DNS propagation
5. **Set up email** (optional) → `POST /api/domains/{domain}/connect` with `{"provider": "google-workspace"}`
6. **Verify for services** (optional) → `POST /api/domains/{domain}/verify-service` for Stripe, Google Search Console, etc.
7. **Post-purchase checklist**:
   - Confirm WHOIS privacy is enabled: `GET /api/domains/{domain}` → check `whois_privacy`
   - Confirm auto-renew is on: same response → check `auto_renew`
   - Check overall health: `GET /api/domains/{domain}/status` → DNS, SSL, email all green

### Set up subdomains

User wants `api.mysite.com` pointing to a backend, `blog.mysite.com` to Ghost, etc.

1. **Get current records** → `GET /api/domains/{domain}/dns`
2. **Add new records while keeping existing ones** - PUT replaces ALL records, so merge:
   ```bash
   curl -s -X PUT "https://domani.run/api/domains/PROJECT_NAME.dev/dns" \
     -H "Authorization: Bearer $DOMANI_API_KEY" \
     -H "Content-Type: application/json" \
     -d '{"records": [
       EXISTING_RECORDS_HERE,
       {"type": "CNAME", "name": "api", "value": "my-backend.railway.app", "ttl": 3600},
       {"type": "CNAME", "name": "blog", "value": "my-blog.ghost.io", "ttl": 3600}
     ]}'
   ```
3. **Verify propagation** → `GET /api/domains/{domain}/status`

### Troubleshoot a domain

When something isn't working:

1. **Check overall health** → `GET /api/domains/{domain}/status`
   - `dns.propagated: false` → DNS changes haven't propagated yet (can take up to 48h, usually 5-30min). Tell the user to wait
   - `ssl.valid: false` → SSL is provisioned by the hosting provider (Vercel, Netlify, etc.), not by us. Tell the user to check their provider dashboard
   - `email.has_mx: false` → MX records are missing or haven't propagated
2. **Check email specifically** → `GET /api/domains/{domain}/email/check` - shows MX, SPF, DMARC, DKIM status
3. **Verify DNS records are correct** → `GET /api/domains/{domain}/dns` - compare against what the provider expects
4. **Re-run connection** → `POST /api/domains/{domain}/connect` again if records look wrong - it will reset them

### Bring an existing domain

User already owns a domain at GoDaddy, Namecheap, Cloudflare, etc.

**Import (free, keep current registrar)** - Choose this when:
- User just wants monitoring, email health, and expiry alerts
- Domain has complex DNS setup they don't want to migrate
- They want to test before committing

→ Section 13 (Import). DNS records from `connect` will show `status: "manual_setup_required"` - the user must add records at their current DNS provider.

**Transfer (full migration, paid, requires EPP code)** - Choose this when:
- User wants full management through domani.run
- They want automatic DNS management
- They're done with their current registrar

→ Section 14 (Transfer). **Paid** - includes 1 year of renewal (check price via `GET /api/tlds`). Takes 1-5 days. Always show the price and get user confirmation before initiating.

### Multi-domain strategy

User wants to secure multiple TLDs for their brand (e.g. .com + .dev + .io):

1. **Buy all at once** → `POST /api/domains/buy` with `{"domains": ["brand.com", "brand.dev", "brand.io"]}`
2. **Connect the primary domain** to hosting (e.g. brand.dev → Vercel)
3. **For secondary domains** - the user can set up redirects through their hosting provider (e.g. Vercel `next.config.js` redirects, Netlify `_redirects`, Cloudflare Page Rules). domani.run manages the DNS; the redirect logic lives in the hosting layer
4. **Enable auto-renew on all** to avoid losing any

### Parking & listing

Manage parking pages and "For Sale" listings:

1. **Enable parking** → `PUT /api/domains/{domain}/parking` with `{ "enabled": true }`
2. **Set sale price** → `PUT /api/domains/{domain}/parking` with `{ "listing_price": 499.99 }`
3. **Check analytics** → `GET /api/domains/{domain}/analytics`
4. **Remove listing** → `PUT /api/domains/{domain}/parking` with `{ "listing_price": null }`

When parking is enabled with a listing price, visitors see a branded "For Sale" page with a contact form. Inquiries are emailed to the domain owner and tracked in analytics.

```bash
# Enable parking with a listing price
curl -s -X PUT "https://domani.run/api/domains/PROJECT_NAME.dev/parking" \
  -H "Authorization: Bearer $DOMANI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"enabled": true, "listing_price": 499.99}'

# Check parking analytics (views, inquiries, conversion rate)
curl -s "https://domani.run/api/domains/PROJECT_NAME.dev/analytics" \
  -H "Authorization: Bearer $DOMANI_API_KEY"
```

Analytics returns: `views_7d`, `views_30d`, `inquiries_30d`, `conversion_rate`, `daily_views` (30-day breakdown), and `recent_inquiries` (last 5 with email, offer, date).

### Webhooks

Receive real-time notifications when events occur - domain purchases, DNS changes, transfer updates, parking inquiries, etc. Stripe-inspired design: register an HTTPS endpoint, choose events, verify payloads with HMAC-SHA256.

```bash
# List available event types
curl -s "https://domani.run/api/webhooks/events"

# Create a webhook
curl -s -X POST https://domani.run/api/webhooks \
  -H "Authorization: Bearer $DOMANI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"url":"https://example.com/hook","events":["domain.purchased","dns.updated","transfer.completed"]}'
# Returns id, url, events, secret (shown once), active

# List your webhooks
curl -s https://domani.run/api/webhooks \
  -H "Authorization: Bearer $DOMANI_API_KEY"

# Update a webhook (change events, URL, or pause/resume)
curl -s -X PATCH https://domani.run/api/webhooks/WEBHOOK_ID \
  -H "Authorization: Bearer $DOMANI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"events":["domain.purchased","inquiry.received"],"active":true}'

# Check delivery history
curl -s https://domani.run/api/webhooks/WEBHOOK_ID/deliveries \
  -H "Authorization: Bearer $DOMANI_API_KEY"

# Delete a webhook
curl -s -X DELETE https://domani.run/api/webhooks/WEBHOOK_ID \
  -H "Authorization: Bearer $DOMANI_API_KEY"
```

**Event types:** `domain.purchased`, `domain.renewed`, `domain.expiring`, `dns.updated`, `transfer.initiated`, `transfer.completed`, `transfer.failed`, `transfer.eligible`, `inquiry.received`, `parking.updated`, `email.verified`, `email.received`, `email.queued`, `email.sent`, `email.delivered`, `email.bounced`, `email.complained`, `email.failed`, `email.delayed`, `email.suppressed`, `email.deleted`.

**Payload format:** Each delivery POSTs a JSON body with `{ id, type, created, data }`. The `X-Domani-Signature` header contains `t=TIMESTAMP,v1=HMAC_SHA256` - verify with the secret returned at creation. Max 5 webhooks per account, HTTPS only. Failed deliveries are retried 3 times with backoff (immediate → 1 min → 10 min).

## API Reference

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/api/auth/register` | Create a new account |
| `POST` | `/api/auth/login` | Send a magic link sign-in email |
| `GET` | `/api/auth/verify` | Verify a magic link token |
| `GET` | `/api/me` | Get current account details |
| `PUT` | `/api/me` | Update account preferences |
| `DELETE` | `/api/me` | Delete account and all associated data |
| `GET` | `/api/me/contact` | Get registrant contact info |
| `PUT` | `/api/me/contact` | Set registrant contact info |
| `POST` | `/api/me/resend-verification` | Resend contact email verification |
| `GET` | `/api/tlds` | List all available TLDs with pricing |
| `GET` | `/api/domains/search` | Check availability and pricing for domains |
| `GET` | `/api/domains/suggest` | AI-powered domain suggestions with availability |
| `GET` | `/api/domains` | List all your registered domains |
| `POST` | `/api/domains/buy` | Purchase one or more domains |
| `GET` | `/api/domains/{domain}/dns` | Get DNS records for a domain you own |
| `PUT` | `/api/domains/{domain}/dns` | Set DNS records for a domain you own |
| `POST` | `/api/domains/{domain}/dns/snapshot` | Capture a DNS snapshot |
| `POST` | `/api/domains/{domain}/dns/restore` | Restore DNS from a snapshot |
| `GET` | `/api/domains/{domain}/nameservers` | Get nameservers for a domain |
| `PUT` | `/api/domains/{domain}/nameservers` | Set nameservers for a domain |
| `POST` | `/api/domains/{domain}/connect` | Connect a domain to a hosting or email provider |
| `GET` | `/api/domains/{domain}/connect` | List available providers for connecting a domain |
| `GET` | `/api/domains/{domain}/status` | Check domain health: DNS, SSL, email, expiry |
| `GET` | `/api/domains/{domain}/email/check` | Check email DNS health (MX, SPF, DMARC, DKIM) |
| `POST` | `/api/domains/{domain}/verify` | Verify that a provider connection is working |
| `POST` | `/api/domains/{domain}/verify-service` | Add DNS records to verify domain ownership for a third-party service |
| `GET` | `/api/domains/{domain}/verify-service` | List supported services for domain verification |
| `GET` | `/api/domains/{domain}` | Get detailed information about a domain you own |
| `PUT` | `/api/domains/{domain}/settings` | Update domain settings |
| `PUT` | `/api/domains/{domain}/parking` | Update parking settings |
| `GET` | `/api/domains/{domain}/analytics` | Get parking analytics |
| `GET` | `/api/domains/{domain}/auth-code` | Get EPP auth code |
| `GET` | `/api/domains/{domain}/transfer-away` | Get outbound transfer status |
| `GET` | `/api/domains/{domain}/transfer-status` | Check inbound transfer status |
| `POST` | `/api/domains/import` | Import an external domain |
| `POST` | `/api/domains/import/verify` | Verify and complete domain import |
| `GET` | `/api/domains/transfer-check` | Pre-check transfer eligibility |
| `POST` | `/api/domains/transfer-watch` | Watch a domain for transfer eligibility |
| `POST` | `/api/domains/transfer` | Transfer domain from another provider |
| `POST` | `/api/domains/{domain}/renew` | Renew a domain |
| `GET` | `/api/domains/whois` | Look up domain registration data via RDAP |
| `GET` | `/api/domains/{domain}/og` | Get website preview metadata for a domain |
| `GET` | `/api/domains/dns-check` | Fast DNS-based domain existence check |
| `GET` | `/api/tokens` | List your API tokens |
| `POST` | `/api/tokens` | Create a new API token |
| `DELETE` | `/api/tokens/{id}` | Revoke an API token |
| `POST` | `/api/billing/setup` | Get checkout URL for adding a payment method |
| `GET` | `/api/billing/invoices` | List payment invoices |
| `GET` | `/api/referrals` | Get referral earnings and history |
| `GET` | `/api/webhooks` | List webhooks |
| `POST` | `/api/webhooks` | Create webhook |
| `PATCH` | `/api/webhooks/{id}` | Update webhook |
| `DELETE` | `/api/webhooks/{id}` | Delete webhook |
| `GET` | `/api/webhooks/{id}/deliveries` | List webhook deliveries |
| `GET` | `/api/webhooks/events` | List webhook event types |
| `POST` | `/api/domains/{domain}/email/setup` | Set up email on a domain |
| `DELETE` | `/api/domains/{domain}/email/setup` | Remove email from a domain |
| `GET` | `/api/domains/{domain}/email/status` | Check email DNS status |
| `POST` | `/api/domains/{domain}/email` | Create a mailbox |
| `GET` | `/api/domains/{domain}/email` | List mailboxes on a domain |
| `GET` | `/api/domains/{domain}/email/{slug}` | Get mailbox details |
| `PATCH` | `/api/domains/{domain}/email/{slug}` | Update mailbox |
| `DELETE` | `/api/domains/{domain}/email/{slug}` | Delete a mailbox |
| `GET` | `/api/domains/{domain}/email/{slug}/avatar` | Get mailbox avatar info |
| `POST` | `/api/domains/{domain}/email/{slug}/send` | Send an email |
| `GET` | `/api/domains/{domain}/email/{slug}/messages` | List emails |
| `PATCH` | `/api/domains/{domain}/email/{slug}/messages/read` | Mark messages as read or unread |
| `POST` | `/api/domains/{domain}/email/{slug}/messages/delete` | Bulk delete messages |
| `GET` | `/api/domains/{domain}/email/{slug}/messages/{id}` | Get a message |
| `DELETE` | `/api/domains/{domain}/email/{slug}/messages/{id}` | Delete a message |
| `POST` | `/api/domains/{domain}/email/{slug}/messages/{id}/forward` | Forward a message |
| `POST` | `/api/domains/{domain}/email/{slug}/messages/{id}/reply` | Reply to a message |
| `POST` | `/api/email` | Create a mailbox on domani.run |
| `GET` | `/api/email` | List all mailboxes |

Full spec: [OpenAPI](https://domani.run/.well-known/openapi.json) | [Docs](https://domani.run/docs) | [llms.txt](https://domani.run/llms.txt) | [MCP Server](https://domani.run/mcp) | [CONTEXT.md](https://github.com/gwendall/domani-app/blob/main/CONTEXT.md)

## Token Scopes

Tokens can be restricted to specific permission scopes. Use `*` for full access (default).

| Scope | Grants access to |
|-------|-----------------|
| `domains:read` | GET /api/domains, GET /api/domains/{domain}, GET /api/domains/{domain}/dns, /status, /email/check, /auth-code, /transfer-away, /transfer-status, /analytics |
| `domains:write` | PUT /api/domains/{domain}/dns, POST /connect, POST /verify, PUT /settings, PUT /parking, POST /api/domains/import, POST /import/verify |
| `domains:transfer` | POST /api/domains/buy, POST /transfer, POST /renew (involves payment) |
| `tokens:read` | GET /api/tokens |
| `tokens:write` | POST /api/tokens, DELETE /api/tokens/{id} |
| `webhooks:read` | GET /api/webhooks, GET /api/webhooks/{id}/deliveries |
| `webhooks:write` | POST /api/webhooks, PATCH /api/webhooks/{id}, DELETE /api/webhooks/{id} |
| `email:read` | GET /api/domains/{domain}/email/* (status, mailboxes, messages) |
| `email:write` | POST /api/domains/{domain}/email/* (setup, create mailbox, send) |
| `account:read` | GET /api/me |
| `account:write` | DELETE /api/me, POST /api/billing/setup, POST /api/me/resend-verification |
| `billing:read` | GET /api/billing/invoices |
| `search` | GET /api/domains/search, /suggest, /whois, /dns-check, GET /api/tlds |

**Scope attenuation:** a token can only create child tokens with equal or fewer scopes - never more.

**Error:** `INSUFFICIENT_SCOPE` (403) - returned when a token lacks the required scope. The response includes `hint` with the missing scope name.

## Error Handling

All errors return `{"error": "...", "code": "...", "hint": "..."}`.

| Code | Action |
|------|--------|
| `MISSING_API_KEY` | Add Authorization header |
| `INVALID_API_KEY` | Re-register or check stored key |
| `EXPIRED_API_KEY` | Token has expired - create a new one via `POST /api/tokens` |
| `INSUFFICIENT_SCOPE` | Token lacks the required scope - create a new token with the needed scopes |
| `PAYMENT_REQUIRED` | Add card via `/api/billing/setup` or pay with USDC |
| `DOMAIN_UNAVAILABLE` | Suggest alternative TLDs using `?domains=` search |
| `RATE_LIMIT_EXCEEDED` | Wait `Retry-After` seconds, then retry |
| `NOT_AVAILABLE` | Feature not supported by current registrar (Preview - coming soon) |

### CLI Error Auto-Recovery (`--json` mode)

When using the CLI with `--json`, errors include a `fix_command` field:

```json
{"error": "Not logged in", "code": "auth_required", "fix_command": "domani login"}
```

| Code | fix_command |
|------|-------------|
| `auth_required` | `domani login` |
| `payment_required` | `domani billing` |
| `contact_required` | `domani contact set` |

Other codes (`validation_error`, `not_found`, `rate_limited`, `conflict`) have no auto-fix - use the `hint` field for guidance.

### CLI Flags for Agents

When using the CLI (`npx domani`), these flags are designed for agent workflows:

- `--json` - Machine-readable JSON output on all commands
- `--fields <fields>` - Filter JSON output to specific fields (comma-separated, e.g. `--fields domain,status`)
- `--dry-run` - Preview mutations without executing (buy, dns set, connect, transfer, renew, etc.)
- `--yes` - Skip confirmation prompts for automated workflows
- `$DOMANI_API_KEY` - Set as environment variable to authenticate without `domani login`

**TTY auto-detect**: When stdout is piped (not a terminal), the CLI automatically outputs JSON and skips confirmations - no `--json` or `--yes` needed.

**Input hardening**: Domain and TLD inputs are validated against path traversal (`../`), control characters, query strings (`?`/`#`), and percent-encoding (`%2e`). Invalid input returns `code: "invalid_input"` with a hint.

## Recipes

Step-by-step workflows for common tasks. For full detailed recipes, see: [Recipes Reference](https://domani.run/references/recipes.md)

Available recipes:
- **Email**: Google Workspace, Fastmail, Proton Mail setup
- **Hosting**: Deploy to Vercel, Netlify, GitHub Pages, Cloudflare Pages
- **Transfer**: Transfer domain from another registrar (with EPP code guides per registrar)
- **Full setup**: Buy domain + connect hosting + email end-to-end

## Schema Introspection

The CLI is fully self-describing. Use `GET https://domani.run/api/schema` to discover all commands, or `GET https://domani.run/api/schema?command=buy` for a specific command's parameters, types, constraints, enums, and error codes.

From the CLI: `domani schema --json` (all commands) or `domani schema buy --json` (one command).


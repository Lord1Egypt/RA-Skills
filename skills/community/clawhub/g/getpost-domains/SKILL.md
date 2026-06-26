---
name: getpost-domains
description: "Register domains, manage DNS, and set up email sending via API."
version: "1.0.0"
---

# GetPost Domains API

Register domains, manage DNS records, set up email sending — all via API. No dashboard needed. Auto-provisions Cloudflare DNS, SendGrid email auth, and nameservers.

## Quick Start
```bash
# Sign up (no verification needed)
curl -X POST https://getpost.dev/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"name": "YOUR_NAME", "bio": "What your agent does"}'
# Save the api_key from the response
```

## Authentication
```
Authorization: Bearer gp_live_YOUR_KEY
```

## Check Domain Availability
```bash
curl -X POST https://getpost.dev/api/domains/check \
  -H "Authorization: Bearer gp_live_YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{"domain": "mybot.dev"}'
```
Returns availability, price in USD and credits.

## Browse All TLD Prices
```bash
curl https://getpost.dev/api/domains/tlds \
  -H "Authorization: Bearer gp_live_YOUR_KEY"
```
Returns pricing for 900+ TLDs — no rate limit.

## Register a Domain
```bash
curl -X POST https://getpost.dev/api/domains/register \
  -H "Authorization: Bearer gp_live_YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{"domain": "mybot.dev"}'
```
Automatically: registers domain, creates DNS zone, points nameservers, sets up email sending (SPF/DKIM/DMARC), creates default redirect.

## Manage DNS
```bash
# List records
curl https://getpost.dev/api/domains/{id}/dns -H "Authorization: Bearer gp_live_YOUR_KEY"

# Add record (smart merge for SPF/DMARC)
curl -X POST https://getpost.dev/api/domains/{id}/dns \
  -H "Authorization: Bearer gp_live_YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{"type": "A", "name": "@", "content": "1.2.3.4", "proxied": true}'
```

## Full Docs
https://getpost.dev/docs/api-reference#domains

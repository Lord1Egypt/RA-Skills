# Procurement Agent v1.1.0 — Production Package

## Security Hardening (v1.1.0)

- `LS_WEBHOOK_SECRET` is **mandatory** — server refuses to start without it
- All webhook logs sanitized — no raw quote content, email addresses, or API keys
- Manifest stripped of all non-essential path permissions (no `~/.ssh`, `~/.aws`, etc.)
- `OPENAI_API_KEY` labeled OPTIONAL — all parsing runs locally without it

## Quick Install

```bash
git clone https://github.com/arya-openclaw/autonomous-procurement-agent.git
cd autonomous-procurement-agent
npm install

# Production: set required secret
export LS_WEBHOOK_SECRET="your_webhook_secret"
export OPENAI_API_KEY="sk-..."   # optional

# Start webhook server
node webhook-handler.js &

# Parse a quote
node self-healing-parser.js parse '<content>'
```

## Webhook Setup

1. Point Lemon Squeezy to: `https://your-domain.com/webhook/lemon-squeezy`
   (Use ngrok for local dev: `ngrok http 3002`)
2. Set `LS_WEBHOOK_SECRET` from your LS dashboard → Webhooks

## Files

```
self-healing-parser.js  — Dual-engine parser (regex + GPT-4o fallback)
webhook-handler.js      — LS webhook receiver + license DB (v1.1.0 hardened)
auth-middleware.js      — Enterprise feature gate middleware
package.json            — v1.1.0
manifest.json            — v1.1.0 (minimal permissions)
listing.json            — v1.1.0
SKILL.md                — Full documentation
PRIVACY.md              — Privacy policy
```

## License Tiers

| Tier | Price | F1/F2/F3 | Auto-approval | Safety-Freeze |
|------|-------|----------|---------------|---------------|
| Free | $0 | — | — | — |
| Pro | $9.99/mo | — | — | — |
| Enterprise | $29.99/mo | ✅ | ✅ | ✅ |

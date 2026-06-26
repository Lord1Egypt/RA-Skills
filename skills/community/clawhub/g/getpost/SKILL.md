---
name: getpost
description: "The API platform for bots. Email, SMS, search, scrape, AI, domains, shipping - one API key."
version: "1.0.0"
---

# GetPost API — Skills for AI Agents

## What is GetPost?
GetPost is an API platform built for bots and AI agents. One API key gives you access to email, SMS, web search, web scraping, AI/LLM inference, image/video generation, domain registration, and shipping labels.

## Base URL
`https://getpost.dev/api`

## Quick Start
```bash
# Sign up (no verification needed)
curl -X POST https://getpost.dev/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"name": "YOUR_AGENT_NAME", "bio": "What your agent does"}'

# Save the api_key from the response — it's shown only once
# You'll also get a free email address: YOUR_AGENT_NAME@quik.email
```

## Authentication
All requests (except signup) require:
```
Authorization: Bearer gp_live_YOUR_KEY
```

## Credits
GetPost uses a credits system. You get 100 free credits at signup. Buy more at: `POST /api/balance/topup {"package": "pkg_20"}` — packages from $20 (1,000 credits) to $1,000 (120,000 credits).

## Available APIs

### Email
- `POST /api/email/send` — Send email `{"to", "subject", "body"}`
- `GET /api/email/inbox` — Read received emails
- `POST /api/email/addresses` — Register dedicated address
- Cost: 1 credit per email sent, receiving is free

### SMS
- `POST /api/sms/send` — Send SMS `{"to", "body"}` (E.164 format)
- `GET /api/sms/inbox` — Read received SMS
- `POST /api/sms/numbers` — Provision dedicated number
- Cost: 5 credits per SMS sent

### Search
- `POST /api/search` — Web search `{"query", "num_results"}`
- Cost: 3 credits per search

### Web Scrape
- `POST /api/scrape` — Scrape URL `{"url", "extract_text", "screenshot"}`
- Cost: 5 credits per scrape

### AI / LLM Chat
- `GET /api/ai/models` — List all models with pricing
- `POST /api/ai/chat` — Chat completion `{"model", "messages", "max_tokens"}`
- Models: gpt-5.4, gpt-4.1-nano, claude-opus-4-6, claude-sonnet-4-6, gemini-2.5-flash, grok-4, deepseek-chat, kimi-k2.5, and more
- Cost: per-token, varies by model (see /api/ai/models)

### AI Image/Video Generation
- `POST /api/ai/generate` — Generate images or videos `{"model", "prompt", "n"}`
- `GET /api/ai/jobs` — List async generation jobs
- `GET /api/ai/jobs/:id` — Check job status (live-checks provider if pending)
- Image models: gpt-image-1, dall-e-3, midjourney, imagen-4, grok-imagine-image, stable-diffusion-3.5
- Video models: sora-2, grok-imagine-video, veo-3.1
- Cost: varies by model (2-100 credits per generation)

### Domains
- `POST /api/domains/check` — Check availability + pricing `{"domain"}`
- `GET /api/domains/tlds` — All 904 TLD prices (cached, no rate limit)
- `POST /api/domains/register` — Buy + fully provision a domain `{"domain"}`
- `POST /api/domains` — Add a domain you already own `{"domain"}`
- `GET /api/domains` — List your domains
- `GET /api/domains/:id` — Domain details + live status
- `GET /api/domains/:id/nameservers` — Get current nameservers
- `PUT /api/domains/:id/nameservers` — Update nameservers
- `GET /api/domains/:id/dns` — List DNS records
- `POST /api/domains/:id/dns` — Add/upsert DNS record (smart merge for SPF/DMARC)
- `PUT /api/domains/:id/dns/:recordId` — Update a DNS record
- `DELETE /api/domains/:id/dns/:recordId` — Delete a DNS record
- `POST /api/domains/:id/email` — Create email on your domain
- `POST /api/domains/:id/verify-email` — Verify email sending config
- Auto-provisions: Cloudflare DNS, nameservers, SendGrid email, default redirect

### Mail / Shipping
- `POST /api/mail/rates` — Get shipping rates `{"from", "to", "parcel"}`
- `POST /api/mail/labels` — Buy a shipping label
- `GET /api/mail/track/:id` — Track a shipment

### Balance & Credits
- `GET /api/balance` — Check balance and transaction history
- `GET /api/balance/packages` — List credit packages with pricing
- `POST /api/balance/topup` — Create Stripe checkout `{"package": "pkg_50"}`
- `POST /api/balance/pay` — Direct card payment `{"package", "payment_method_id"}`

### Account
- `GET /api/auth/me` — Get your profile
- `PUT /api/auth/me` — Update name/bio
- `DELETE /api/auth/me` — Delete your account
- `GET /api/auth/rate-limits` — Check rate limit status

### Webhooks
- `POST /api/webhooks` — Register `{"url", "events"}`
- `GET /api/webhooks` — List your webhooks
- `GET /api/webhooks/deliveries` — View delivery history (status, latency, errors)
- `DELETE /api/webhooks/:id` — Delete a webhook
- Events: `email.received`, `sms.received`, `balance.low`, `balance.credited`, `generation.completed`, `*` (all)

### Logs
- `GET /api/logs` — Your request history (method, path, status, latency, credits)
- `GET /api/logs/summary` — Aggregated stats by endpoint

## Full OpenAPI Spec
https://getpost.dev/api/openapi.json

## Pricing
https://getpost.dev/api/pricing

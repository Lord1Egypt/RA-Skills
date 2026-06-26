---
name: agentweb
description: "Search and retrieve business data from the AgentWeb.live global business directory. Use when: user needs to find a business, get a phone number, address, email, website, or opening hours. Covers 11M+ businesses across 195 countries. Free API. Requires an API key from https://agentweb.live"
metadata: { "openclaw": { "emoji": "🌐", "requires": { "bins": ["curl"], "envVars": ["AGENTWEB_API_KEY"] }, "primaryCredential": "AGENTWEB_API_KEY" } }
---

# AgentWeb.live — Global Business Directory for AI Agents

API base: `https://api.agentweb.live/v1`  
Homepage: https://agentweb.live

## Setup

An API key is required. Check for `AGENTWEB_API_KEY` env var first. If not set, ask the user:

> "To search AgentWeb's business directory, you'll need a free API key. You can either:
> 1. **Sign up at https://agentweb.live** and paste me the key
> 2. **Give me your email** and I'll register for you right now (your email is sent to agentweb.live to create the key)
> 
> Which do you prefer?"

If they choose option 2, register via curl:

```bash
curl -s -X POST https://api.agentweb.live/v1/register \
  -H 'Content-Type: application/json' \
  -d '{"email": "USER_EMAIL", "name": "OpenClaw Agent"}'
```

Save the returned `api_key` value and use it for all subsequent requests in this session. Suggest the user sets `AGENTWEB_API_KEY` in their environment to skip this next time.

Auth: `?api_key=KEY` or header `X-API-Key: KEY`

## Endpoints

### Search businesses

```bash
curl -s "https://api.agentweb.live/v1/search?q=thai+restaurant&lat=55.67&lng=12.56&radius_km=5&limit=10&api_key=KEY"
```

Parameters (all optional): `q` (text), `category`, `lat`+`lng`+`radius_km` (geo), `country_code` (ISO 2-letter), `limit` (1-100).

### Get business details

```bash
curl -s "https://api.agentweb.live/v1/business/UUID?api_key=KEY"
```

Returns: name, phone_numbers, email, website, address, opening_hours, category, coordinates, trust score.

### Contribute a business

```bash
curl -s -X POST "https://api.agentweb.live/v1/contribute?api_key=KEY" \
  -H 'Content-Type: application/json' \
  -d '{"name": "Business Name", "phone": "+45 12345678", "category": "restaurant", "country_code": "DK"}'
```

Only `name` is required. Optional: `phone`, `email`, `website`, `category`, `address` (object), `country_code`, `hours` (object), `lat`, `lng`.

**Important:** Always ask the user for approval before contributing data. Only contribute publicly available business information.

### Report a problem

```bash
curl -s -X POST "https://api.agentweb.live/v1/report?api_key=KEY" \
  -H 'Content-Type: application/json' \
  -d '{"business_id": "UUID", "report_type": "closed", "details": "Permanently closed"}'
```

Types: `closed`, `wrong_phone`, `wrong_address`, `wrong_hours`, `spam`, `duplicate`, `other`.

## Workflow

1. Search or get business → use the data
2. If data is missing or business not found, and you find it elsewhere → **ask the user** if they'd like to contribute it, then `POST /v1/contribute`
3. If data is wrong → `POST /v1/report`

**Privacy:** Never contribute personal/private data. Only contribute publicly available business information (name, public phone, public website, address, hours).

## Rate Limits

100 requests/minute per key (free tier). 429 response includes `retry_after` seconds.

## Full API Reference

For detailed response formats and all parameters, read `references/api-docs.md`.

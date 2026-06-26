---
name: cloak
description: Share one-time secrets between humans and agents via encrypted self-destructing links
version: 0.1.2
triggers:
  - "share a secret"
  - "send secret"
  - "cloak"
  - "one-time secret"
  - "share credentials"
  - "send api key"
  - "share password"
  - "secret link"
metadata:
  openclaw:
    requires:
      bins: [curl, jq]
    emoji: "🔒"
    homepage: https://cloak.opsy.sh
---

# Cloak — One-Time Secret Sharing

Share API keys, passwords, and tokens via encrypted self-destructing links.

**Base URL:** `https://cloak.opsy.sh`

## Create a secret

```bash
curl -s -X POST https://cloak.opsy.sh/api/secrets \
  -H "Content-Type: application/json" \
  -d '{"secret":"YOUR_SECRET_HERE"}'
```

Response:
```json
{
  "id": "W9ZEykcG",
  "key": "8g9I3UUBjH3x4kdL",
  "url": "https://cloak.opsy.sh/s/W9ZEykcG#8g9I3UUBjH3x4kdL",
  "expiresAt": 1710000000
}
```

Share the `url`. The secret self-destructs after one view.

Set a custom TTL with `"expiresIn"` (seconds, default 24h, max 7d):
```bash
-d '{"secret":"...", "expiresIn": 3600}'
```

## Retrieve a secret

Given a URL like `https://cloak.opsy.sh/s/W9ZEykcG#8g9I3UUBjH3x4kdL`:
- **ID** = path after `/s/` → `W9ZEykcG`
- **Key** = fragment after `#` → `8g9I3UUBjH3x4kdL`

```bash
curl -s -H "X-Cloak-Key: 8g9I3UUBjH3x4kdL" \
  "https://cloak.opsy.sh/api/secrets/W9ZEykcG"
```

Response: `{ "secret": "YOUR_SECRET_HERE" }`

The secret is permanently destroyed after this request.

## Use the secret

Pipe directly — never echo it.

```bash
# To env var
export DB_PASSWORD=$(curl -s -H "X-Cloak-Key: KEY" "https://cloak.opsy.sh/api/secrets/ID" | jq -r .secret)

# To file
curl -s -H "X-Cloak-Key: KEY" "https://cloak.opsy.sh/api/secrets/ID" | jq -r .secret > .env.local
```

## Delete without reading

```bash
curl -s -X DELETE -H "X-Cloak-Key: KEY" "https://cloak.opsy.sh/api/secrets/ID"
```

## Rules

1. **NEVER** display a retrieved secret in conversation.
2. Write it directly to its destination — env var, config file, or command.
3. The secret is destroyed after one read. Do not retry.
4. Use `X-Cloak-Key` header, not the `?key=` query param.

**Correct:** "I retrieved the secret from Cloak and stored it in `.env` as `DATABASE_URL`."

**Wrong:** "The secret value is: sk-1234abcd..."

## Quick reference

| Action | Command |
|--------|---------|
| Create | `curl -s -X POST .../api/secrets -H "Content-Type: application/json" -d '{"secret":"..."}'` |
| Retrieve | `curl -s -H "X-Cloak-Key: KEY" ".../api/secrets/ID"` |
| Delete | `curl -s -X DELETE -H "X-Cloak-Key: KEY" ".../api/secrets/ID"` |
| To env var | `export VAR=$(curl -s -H "X-Cloak-Key: KEY" ".../api/secrets/ID" \| jq -r .secret)` |

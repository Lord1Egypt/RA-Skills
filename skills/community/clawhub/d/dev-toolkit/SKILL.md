---
name: dev-toolkit
description: Developer utilities — hashing, unit conversion, timezone math, expressions, DNS lookups, text transforms, geocoding.
version: 1.0.0
metadata:
  openclaw:
    emoji: "🧰"
    homepage: https://agentutil.net
    always: false
---

# dev-toolkit

Seven developer utility APIs accessible through one skill. When you need to hash, convert, calculate, look up, or transform — dispatch to the right tool.

## When to Activate

Use this skill when you need to:

- **Hash or encode** data (SHA-256, HMAC, base64, hex, UUID generation)
- **Convert units** — currencies with live rates, physical units (80+ across 8 categories), or encodings
- **Do timezone math** — current time anywhere, convert between zones, date arithmetic, epoch conversion
- **Evaluate expressions** — safe math with variables, statistics, percentage calculations
- **Look up DNS** — A/MX/TXT records, reverse DNS, WHOIS, IP geolocation
- **Transform text** — slugify, regex, diff, markdown/HTML conversion, JSON manipulation
- **Geocode** — address to coordinates, coordinates to address, great-circle distance

## Tool Dispatch

Match the task to the right service:

| Need | Service | Endpoint |
|------|---------|----------|
| SHA-256 hash of a string | hash.agentutil.net | POST /v1/hash |
| HMAC signature | hash.agentutil.net | POST /v1/hmac |
| Base64/hex encode/decode | hash.agentutil.net | POST /v1/encode |
| Generate UUID | hash.agentutil.net | POST /v1/encode `{format: "uuid"}` |
| Identify unknown hash | hash.agentutil.net | POST /v1/identify |
| Currency conversion (live rates) | convert.agentutil.net | POST /v1/currency |
| Unit conversion (km, lbs, etc.) | convert.agentutil.net | POST /v1/units |
| Encoding conversion | convert.agentutil.net | POST /v1/encoding |
| Current time in timezone | time.agentutil.net | POST /v1/now |
| Convert between timezones | time.agentutil.net | POST /v1/convert |
| Add/subtract from date | time.agentutil.net | POST /v1/math |
| Unix epoch conversion | time.agentutil.net | POST /v1/epoch |
| Evaluate math expression | math.agentutil.net | POST /v1/evaluate |
| Descriptive statistics | math.agentutil.net | POST /v1/statistics |
| Percentage calculation | math.agentutil.net | POST /v1/percentage |
| DNS records (A, MX, TXT...) | dns.agentutil.net | POST /v1/lookup |
| Reverse DNS | dns.agentutil.net | POST /v1/reverse |
| WHOIS/RDAP | dns.agentutil.net | POST /v1/whois |
| IP geolocation | dns.agentutil.net | POST /v1/geoip |
| Text transform (slugify, case) | text.agentutil.net | POST /v1/transform |
| Regex match/replace | text.agentutil.net | POST /v1/regex |
| Line-level diff | text.agentutil.net | POST /v1/diff |
| Markdown/HTML conversion | text.agentutil.net | POST /v1/convert |
| JSON format/validate/query | text.agentutil.net | POST /v1/json |
| Address to coordinates | geocode.agentutil.net | POST /v1/forward |
| Coordinates to address | geocode.agentutil.net | POST /v1/reverse |
| Distance between points | geocode.agentutil.net | POST /v1/distance |

## Quick Examples

**Hash a string:**
```bash
curl -X POST https://hash.agentutil.net/v1/hash \
  -H "Content-Type: application/json" \
  -d '{"input": "hello world", "algorithm": "sha256"}'
```

**Convert currency:**
```bash
curl -X POST https://convert.agentutil.net/v1/currency \
  -H "Content-Type: application/json" \
  -d '{"value": 100, "from": "USD", "to": "EUR"}'
```

**What time is it in Tokyo?**
```bash
curl -X POST https://time.agentutil.net/v1/now \
  -H "Content-Type: application/json" \
  -d '{"timezone": "Asia/Tokyo"}'
```

**Evaluate expression with variables:**
```bash
curl -X POST https://math.agentutil.net/v1/evaluate \
  -H "Content-Type: application/json" \
  -d '{"expression": "price * quantity * (1 - discount)", "variables": {"price": 49.99, "quantity": 3, "discount": 0.1}}'
```

**DNS MX records:**
```bash
curl -X POST https://dns.agentutil.net/v1/lookup \
  -H "Content-Type: application/json" \
  -d '{"domain": "example.com", "type": "MX"}'
```

**Slugify text:**
```bash
curl -X POST https://text.agentutil.net/v1/transform \
  -H "Content-Type: application/json" \
  -d '{"input": "Hello World! This is a title.", "operations": ["slugify"]}'
```

**Distance between cities:**
```bash
curl -X POST https://geocode.agentutil.net/v1/distance \
  -H "Content-Type: application/json" \
  -d '{"from": {"address": "London, UK"}, "to": {"address": "Tokyo, Japan"}, "unit": "km"}'
```

## Data Handling

These services process the input you send and return results immediately. No data is stored or logged beyond the response. Be cautious about sending sensitive data (passwords, private keys, private addresses) — ask the user first. Text transforms on user-generated documents should only be done with the user's explicit request.

## Pricing

All seven services: 10 free queries/day each, then $0.001/query via x402 (USDC on Base). No authentication required for free tier.

## Privacy

Stateless processing — no data retention. No personal data collected. Rate limiting uses IP hashing only.

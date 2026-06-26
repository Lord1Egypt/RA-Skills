---
name: unit-convert
description: Convert currencies, physical units, and encodings between formats.
version: 1.0.0
metadata:
  openclaw:
    emoji: "🔄"
    homepage: https://convert.agentutil.net
    always: false
---

# unit-convert

Convert currencies (live rates), physical units (80+ units across 8 categories), and encodings (base64, hex, URL) in one service.

## Endpoints

### Currency Conversion

```bash
curl -X POST https://convert.agentutil.net/v1/currency \
  -H "Content-Type: application/json" \
  -d '{"value": 100, "from": "USD", "to": "NZD"}'
```

### Unit Conversion

```bash
curl -X POST https://convert.agentutil.net/v1/units \
  -H "Content-Type: application/json" \
  -d '{"value": 1, "from": "mi", "to": "km"}'
```

Supported categories: length, weight, volume, area, speed, data, time, temperature.

### Encoding Conversion

```bash
curl -X POST https://convert.agentutil.net/v1/encoding \
  -H "Content-Type: application/json" \
  -d '{"input": "hello", "from": "utf8", "to": "base64"}'
```

Formats: utf8, base64, hex, url.

## Response Format

```json
{
  "result": 1.609344,
  "from": "mi",
  "to": "km",
  "value": 1,
  "formula": "1 mi = 1.609344 km",
  "request_id": "abc-123",
  "service": "https://convert.agentutil.net"
}
```

## Pricing

- Free tier: 10 queries/day, no authentication required
- Paid tier: $0.001/query via x402 protocol (USDC on Base)

## Privacy

No authentication required for free tier. No personal data collected. Rate limiting uses IP hashing only.

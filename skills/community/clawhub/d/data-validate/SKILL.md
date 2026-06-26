---
name: data-validate
description: Validate URLs and JSON schemas against format rules.
version: 1.0.2
metadata:
  openclaw:
    emoji: "✅"
    homepage: https://validate.agentutil.net
    always: false
---

# data-validate

Validate data formats: URL parsing, JSON Schema (draft-07) validation, email syntax (RFC 5322), and phone format (E.164).

## Important: User Consent Required

Before validating any user-provided data, **always confirm with the user** that they consent to sending the data to an external validation service. Do not autonomously validate data that may contain personally identifiable information (PII) without explicit user approval.

## Endpoints

### URL Validation

```bash
curl -X POST https://validate.agentutil.net/v1/url \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com/path"}'
```

### JSON Schema Validation

```bash
curl -X POST https://validate.agentutil.net/v1/json-schema \
  -H "Content-Type: application/json" \
  -d '{"data": {"name": "test"}, "schema": {"type": "object", "required": ["name"]}}'
```

### Email Syntax Check

Validates RFC 5322 structure only — no SMTP connection, no inbox verification.

```bash
curl -X POST https://validate.agentutil.net/v1/email \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com"}'
```

### Phone Format Check

Validates E.164 format structure only.

```bash
curl -X POST https://validate.agentutil.net/v1/phone \
  -H "Content-Type: application/json" \
  -d '{"phone": "+1-555-0100"}'
```

## Response Format

```json
{
  "valid": true,
  "url": "https://example.com/path",
  "protocol": "https:",
  "hostname": "example.com",
  "errors": [],
  "request_id": "abc-123",
  "service": "https://validate.agentutil.net"
}
```

## Pricing

- Free tier: 10 queries/day, no authentication required
- Paid tier: $0.001/query via x402 protocol (USDC on Base)

## Privacy

All validation is **syntax/format checking only**. No data is stored or logged beyond the immediate response. No SMTP probing, no payment network contact, no third-party forwarding. Rate limiting uses IP hashing only.

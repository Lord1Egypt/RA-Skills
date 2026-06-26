---
name: getpost-sms
description: "Send and receive SMS messages via API. Shared or dedicated numbers."
version: "1.0.0"
---

# GetPost SMS API

Send and receive SMS messages. Shared number included, or provision a dedicated number.

## Quick Start
```bash
# Sign up (no verification needed)
curl -X POST https://getpost.dev/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"name": "YOUR_NAME", "bio": "What your agent does"}'
# Save the api_key from the response
```

## Base URL
`https://getpost.dev/api`

## Authentication
```
Authorization: Bearer gp_live_YOUR_KEY
```

## Send SMS
```bash
curl -X POST https://getpost.dev/api/sms/send \
  -H "Authorization: Bearer gp_live_YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{"to": "+14155551234", "body": "Hello from my bot!"}'
```
Phone numbers must be E.164 format. Cost: 5 credits per SMS.

## Read Inbox
```bash
curl https://getpost.dev/api/sms/inbox \
  -H "Authorization: Bearer gp_live_YOUR_KEY"
```

## Provision Dedicated Number
```bash
curl -X POST https://getpost.dev/api/sms/numbers \
  -H "Authorization: Bearer gp_live_YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{"area_code": "415", "country": "US"}'
```

## Webhook
Register a webhook for `sms.received` to get notified when you receive a text.

## Full Docs
https://getpost.dev/docs/api-reference#sms

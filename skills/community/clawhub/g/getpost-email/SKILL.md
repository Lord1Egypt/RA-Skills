---
name: getpost-email
description: "Send and receive emails via API. Get a working email address instantly."
version: "1.0.0"
---

# GetPost Email API

Send and receive emails programmatically. No email server setup needed — get a working email address instantly on signup.

## Quick Start
```bash
# Sign up (no verification needed)
curl -X POST https://getpost.dev/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"name": "YOUR_NAME", "bio": "What your agent does"}'
# Save the api_key — you'll also get YOUR_NAME@quik.email automatically
```

## Base URL
`https://getpost.dev/api`

## Authentication
```
Authorization: Bearer gp_live_YOUR_KEY
```

## Get an API Key
```bash
curl -X POST https://getpost.dev/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"name": "YOUR_NAME", "bio": "What your agent does"}'
```
You'll get `YOUR_NAME@quik.email` automatically.

## Send Email
```bash
curl -X POST https://getpost.dev/api/email/send \
  -H "Authorization: Bearer gp_live_YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{"to": "recipient@example.com", "subject": "Hello", "body": "Email body text"}'
```
Cost: 1 credit per email sent.

## Read Inbox
```bash
curl https://getpost.dev/api/email/inbox \
  -H "Authorization: Bearer gp_live_YOUR_KEY"
```
Returns received emails with from, to, subject, body, and attachments.

## Register Dedicated Address
```bash
curl -X POST https://getpost.dev/api/email/addresses \
  -H "Authorization: Bearer gp_live_YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{"local_part": "hello", "domain": "quik.email"}'
```

## Custom Domain Email
Register a domain via `/api/domains/register`, then create any email address on it.

## Webhook
Register a webhook for `email.received` to get notified instantly when you receive email.

## Full Docs
https://getpost.dev/docs/api-reference#email

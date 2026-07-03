---
name: agent-email-setup
description: "Set up a dedicated email address for an agent using Resend. Configure sending, receiving via webhook, inbox storage, and automated monitoring. Use when: (1) agent needs its own email identity, (2) agent needs to receive confirmation emails from external services, (3) setting up agent email for the first time, (4) agent needs to autonomously handle email verification flows."
---

# Agent Email Setup

Give an agent its own email address for sending and receiving — verification codes, notifications, account registration, and autonomous inbox monitoring.

## Prerequisites

- A verified domain on Resend (or ability to verify one)
- A running Express/Node.js backend (for webhook receiving)
- Resend API key with full permissions (not send-only)
- `curl`, `jq`, and `node` available on the server

## Architecture

```
External Sender
      ↓
[Resend Inbound]
      ↓ (webhook: email.received)
[Express /api/inbound-email]
      ↓ (save as JSON)
[mail/inbox/]
      ↓ (cron: every 5 min)
[Agent reads + processes]
      ↓
[Agent responds/acts]
```

## Step 1: Verify Domain on Resend

If the domain isn't already verified:

```bash
RESEND_KEY="re_xxxxx"

# Add domain
curl -s -X POST -H "Authorization: Bearer $RESEND_KEY" \
  -H "Content-Type: application/json" \
  https://api.resend.com/domains \
  -d '{"name": "yourdomain.com", "region": "us-east-1"}'

# Get DNS records to configure
curl -s -H "Authorization: Bearer $RESEND_KEY" \
  https://api.resend.com/domains/yourdomain.com | jq '.records'
```

Add the returned DNS records (TXT, MX, CNAME) to your DNS provider. Wait for verification (usually minutes).

**Verify status:**
```bash
curl -s -H "Authorization: Bearer $RESEND_KEY" \
  https://api.resend.com/domains/yourdomain.com | jq '{status, capabilities}'
```

Both `sending` and `receiving` must be `"enabled"`.

## Step 2: Create Webhook Endpoint

Create `routes/inboundEmail.js` in your Express backend (see `references/inboundEmail.js` for full implementation). Key requirements:

- Accept POST at `/api/inbound-email`
- Verify Resend webhook signature using `RESEND_WEBHOOK_SECRET`
- Save emails as JSON to `mail/inbox/`
- Provide GET endpoint to list/read emails
- Provide ACK endpoint to mark processed

Mount in your server:
```js
const inboundEmailRoutes = require('./routes/inboundEmail');
app.use('/api/inbound-email', inboundEmailRoutes);
```

## Step 3: Register Webhook on Resend

```bash
curl -s -X POST -H "Authorization: Bearer $RESEND_KEY" \
  -H "Content-Type: application/json" \
  https://api.resend.com/webhooks \
  -d '{
    "endpoint": "https://yourdomain.com/api/inbound-email",
    "events": ["email.received"],
    "enabled": true
  }' | jq '{id, signing_secret}'
```

**Save the `signing_secret`** — you'll need it for webhook verification.

## Step 4: Store Secrets

Add to your secrets management:

```json
{
  "RESEND_API_KEY": "re_xxxxx",
  "RESEND_WEBHOOK_SECRET": "whsec_xxxxx",
  "AGENT_EMAIL": "agent@yourdomain.com"
}
```

## Step 5: Create Inbox Directory

```bash
mkdir -p mail/inbox
touch mail/inbox/.lastcheck
```

## Step 6: Set Up Inbox Monitoring Cron

Create a cron job that checks for new emails every 5 minutes and notifies the agent:

```
Every 5 min → Check mail/inbox/ for new .json files
→ If new emails: read, summarize, and report to owner
→ Mark processed with .processed extension
```

## Step 7: Test End-to-End

**Send a test email:**
```bash
curl -s -X POST -H "Authorization: Bearer $RESEND_KEY" \
  -H "Content-Type: application/json" \
  https://api.resend.com/emails \
  -d '{
    "from": "Agent <agent@yourdomain.com>",
    "to": ["owner@theirdomain.com"],
    "subject": "Email system test",
    "text": "This is a test from my new email address."
  }'
```

**Verify receiving:**
```bash
curl -s https://yourdomain.com/api/inbound-email | jq .
```

**Verify inbox:**
```bash
ls -la mail/inbox/
```

## Sending Email from Agent Code

```js
async function sendEmail(to, subject, text, html) {
  const res = await fetch('https://api.resend.com/emails', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${RESEND_API_KEY}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      from: 'Agent <agent@yourdomain.com>',
      to: [to],
      subject,
      text,
      ...(html && { html }),
    }),
  });
  return res.json();
}
```

## Reading Inbox from Agent Code

```js
async function getInbox() {
  const res = await fetch('http://localhost:PORT/api/inbound-email');
  const data = await res.json();
  return data.emails;
}

async function getEmail(id) {
  const res = await fetch(`http://localhost:PORT/api/inbound-email/${id}`);
  return res.json();
}

async function ackEmail(id) {
  await fetch(`http://localhost:PORT/api/inbound-email/${id}/ack`, { method: 'POST' });
}
```

## Webhook Signature Verification

Resend signs webhooks with HMAC-SHA256. Verify to prevent spoofing:

```js
const crypto = require('crypto');

function verifySignature(rawBody, signature, secret) {
  try {
    const [timestamp, hash] = signature.split(',').map(s => s.trim());
    if (!timestamp || !hash) return false;
    const signedPayload = `${timestamp}.${rawBody}`;
    const expected = crypto.createHmac('sha256', secret)
      .update(signedPayload).digest('hex');
    return crypto.timingSafeEqual(Buffer.from(hash), Buffer.from(expected));
  } catch {
    return false;
  }
}
```

## Security Notes

- Never expose `RESEND_API_KEY` or `RESEND_WEBHOOK_SECRET` in chat or logs
- Always verify webhook signatures in production
- Use HTTPS for webhook endpoints (Resend requires it)
- The webhook secret should be stored in secrets management, not hardcoded
- Inbox files should be on the server filesystem, not publicly accessible

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Domain not verifying | Check DNS records propagated (`dig TXT yourdomain.com`) |
| Webhook not firing | Verify webhook is `enabled` and endpoint is HTTPS |
| Signature mismatch | Ensure you're using raw body, not parsed JSON |
| Emails not arriving | Check domain `receiving` capability is `enabled` |
| Backend not receiving | Check Express route is mounted before body parsers |

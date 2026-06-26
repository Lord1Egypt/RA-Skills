---
name: agentlair-email
description: Give your agent a real email address via REST API. Claim @agentlair.dev addresses, send and receive email — no SMTP, no IMAP, no credentials to configure. Free tier includes 50 emails/day. Use when an agent needs to send email, check inbox, or claim an email identity.
version: 1.0.0
metadata:
  openclaw:
    homepage: https://agentlair.dev
    emoji: "📧"
    os: ["linux", "macos", "windows"]
    primaryEnv: AGENTLAIR_API_KEY
    requires:
      bins:
        - curl
    tags:
      - email
      - agent-identity
      - communication
      - api
      - infrastructure
---

# AgentLair Email — REST Email for Agents

Give any agent a working email address in 30 seconds. No SMTP setup, no IMAP polling, no credentials to rotate. Just REST.

Base URL: `https://agentlair.dev`
Auth: `Authorization: Bearer <YOUR_API_KEY>`

---

## Setup: Get an API Key

Self-service, no email required:

```bash
curl -s -X POST https://agentlair.dev/v1/auth/keys \
  -H "Content-Type: application/json" \
  -d '{}'
```

Response:
```json
{"key": "al_live_...", "tier": "free"}
```

Store the key as `AGENTLAIR_API_KEY` in your environment. All subsequent calls need it in the `Authorization` header.

---

## When to Use This Skill

Use this skill when:
- An agent needs to send or receive email
- You need to claim a dedicated email identity for an agent
- You want to check an agent's inbox programmatically
- The user asks about agent email, email identity, or sending email as an agent

---

## Claim an Email Address

```bash
curl -s -X POST https://agentlair.dev/v1/email/claim \
  -H "Authorization: Bearer $AGENTLAIR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"address": "myagent@agentlair.dev"}'
```

Response:
```json
{"address": "myagent@agentlair.dev", "claimed": true, "already_owned": false, "account_id": "..."}
```

You can claim multiple addresses per API key.

---

## Send an Email

**Important:** Use the `text` field for the message body (not `body` — that returns a `missing_fields` error).

```bash
curl -s -X POST https://agentlair.dev/v1/email/send \
  -H "Authorization: Bearer $AGENTLAIR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "from": "myagent@agentlair.dev",
    "to": ["recipient@example.com"],
    "subject": "Hello from my agent",
    "text": "Plain text message body."
  }'
```

Response:
```json
{"id": "out_...", "status": "sent", "sent_at": "...", "rate_limit": {"daily_remaining": 49}}
```

Optional fields:
- `"html"` — HTML version of the message
- `"cc"` — array of CC recipients

---

## Check Inbox

```bash
curl -s "https://agentlair.dev/v1/email/inbox?address=myagent@agentlair.dev&limit=10" \
  -H "Authorization: Bearer $AGENTLAIR_API_KEY"
```

Response:
```json
{
  "messages": [
    {
      "message_id": "<abc123@host>",
      "from": "sender@example.com",
      "subject": "Re: Hello",
      "received_at": "2026-03-15T...",
      "read": false
    }
  ],
  "count": 1
}
```

**Note:** `message_id` values include RFC 2822 angle brackets `<...>`. Strip them before using in the read endpoint.

---

## Read a Specific Message

Strip `<>` from `message_id`, then URL-encode the `@`:

```bash
# message_id from inbox: <abc123@eu-west-1.amazonses.com>
# Strip angle brackets, URL-encode @
MSG_ID="abc123%40eu-west-1.amazonses.com"
curl -s "https://agentlair.dev/v1/email/messages/$MSG_ID?address=myagent@agentlair.dev" \
  -H "Authorization: Bearer $AGENTLAIR_API_KEY"
```

In code:
```javascript
const rawId = message.message_id.replace(/^<|>$/g, "");
const encodedId = encodeURIComponent(rawId);
const url = `https://agentlair.dev/v1/email/messages/${encodedId}?address=${encodeURIComponent(address)}`;
```

---

## Check Sent Outbox

```bash
curl -s "https://agentlair.dev/v1/email/outbox?limit=5" \
  -H "Authorization: Bearer $AGENTLAIR_API_KEY"
```

---

## Free Tier Limits

| Limit | Value |
|-------|-------|
| Emails per day | 50 |
| API requests per day | 100 |
| Addresses per key | Unlimited |
| Rate limit reset | Midnight UTC |

---

## Delivery Timing

- **External recipients:** ~1-2 seconds via Amazon SES
- **Intra-domain** (agentlair.dev to agentlair.dev): inbox indexing can take 30-120 seconds after SES receipt
- When polling inbox for a just-sent email, use a **120-second timeout minimum**

---

## Example Session

**User:** "Send an email to bob@example.com introducing yourself"

**Agent actions:**

1. Check if you have an API key. If not, get one:
```bash
curl -s -X POST https://agentlair.dev/v1/auth/keys -H "Content-Type: application/json" -d '{}'
```

2. Claim an address:
```bash
curl -s -X POST https://agentlair.dev/v1/email/claim \
  -H "Authorization: Bearer $AGENTLAIR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"address": "assistant@agentlair.dev"}'
```

3. Send the email:
```bash
curl -s -X POST https://agentlair.dev/v1/email/send \
  -H "Authorization: Bearer $AGENTLAIR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "from": "assistant@agentlair.dev",
    "to": ["bob@example.com"],
    "subject": "Hello from your AI assistant",
    "text": "Hi Bob, I am an AI assistant reaching out to introduce myself. Let me know if you need anything!"
  }'
```

4. Confirm to user: "Email sent to bob@example.com from assistant@agentlair.dev"

---

## Notes

- Emails delivered via Amazon SES (eu-west-1) with DKIM, SPF, and DMARC authentication
- Custom domain support coming Q2 2026
- No data stored beyond delivery — privacy-first design
- Built by [AgentLair](https://agentlair.dev) — infrastructure for autonomous agents

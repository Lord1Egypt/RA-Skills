---
name: ai-cheese
description: "Send paid messages to real humans via the A.I. Cheese platform (aicheese.app). Use when an agent needs human input — surveys, feedback, photo tasks, local knowledge, verification. Pays USDC on Base via x402 protocol. Supports directory search (location, skills, price), sending paid messages, polling for replies, and webhook registration."
metadata: {"clawdbot":{"emoji":"🧀","requires":{"bins":["npx"]}}}
---

# A.I. Cheese — Paid Human Messaging

Send paid messages to real humans. They get USDC, you get answers.

**API Base:** `https://aicheese.app`

## Quick Start

```bash
# Search for humans in London who speak Spanish, max $0.50/msg
npx tsx scripts/ai-cheese.ts search --location london --skills spanish --max-price 0.50

# Send a paid message
npx tsx scripts/ai-cheese.ts send --to <userId> --message "What's the best cafe near you?"

# Check for replies
npx tsx scripts/ai-cheese.ts replies
```

## Setup

Set environment variable with a funded wallet (needs USDC on Base):
```bash
export AGENT_PRIVATE_KEY="0x..."
```

## API Reference

### Conversations (Threading)

Messages support multi-turn conversations. The first message creates a thread. Follow-ups use the `threadId` from the response.

**Pricing:**
- New message → full price
- Follow-up before user replies → full price (no spamming)
- Follow-up after user replies → 25% of base price (min $0.01)
- User replies → free

**Flow:** Send → get `threadId` → poll for reply → send follow-up with `threadId` → repeat.

### 1. Search Directory

Find humans by location, skills, or price.

```
GET /api/v1/directory
  ?location=miami
  ?lat=25.76&lng=-80.19&radius=50
  ?skills=photographer,foodie
  ?maxPrice=1.00
  ?limit=20&offset=0
```

Returns `{ profiles: [{ id, displayName, bio, location, skills, pricePerMessage }], total }`.

### 2. Send Paid Message (x402 Flow)

```
POST /api/v1/message
Body: { toUserId, fromAgentId, fromLabel, content }
```

**Flow:**
1. First request returns `402` with payment requirements
2. Pay USDC to the user's wallet address (amount in response)
3. Retry with `X-Payment: <txHash>` header
4. Message delivered, returns `{ ok: true, messageId, threadId }`

For follow-ups, include `threadId` in the body. Price is reduced to 25% if the user has replied.

### 3. Poll for Replies

```
GET /api/v1/agent/replies?agentId=<your-agent-id>&since=<timestamp>
```

Returns `{ replies: [{ messageId, replyContent, replyAttachments, replyAt, amountPaid }] }`.

Attachments are URLs to uploaded photos (e.g. `/api/v1/files/abc.jpg`).

### 4. Register Webhook

Get notified instantly when a user replies:

```
POST /api/v1/agent/webhook
Body: { agentId, url, secret }
```

Webhook payload includes `X-Webhook-Signature` (HMAC-SHA256 of body using secret).

## CLI Script

The bundled `scripts/ai-cheese.ts` handles the full x402 payment flow automatically.

**Commands:**
- `search` — Search directory with filters
- `send --to <id> --message "..."` — Pay and send a message
- `replies` — Poll for replies to your messages
- `webhook --url <url>` — Register a webhook

Run with: `npx tsx <skill-path>/scripts/ai-cheese.ts <command> [options]`

## Use Cases

- **Surveys** — Ask humans about their area, opinions, experiences
- **Feedback** — Get real user testing on apps, ideas, products
- **Photo tasks** — Request photos of locations, products, storefronts
- **Local knowledge** — Find people near a location for ground-truth info
- **Verification** — Human-in-the-loop checks for AI outputs

## Tips

- Start with `$0.10-0.25/msg` for surveys, `$0.50-5.00` for tasks requiring effort
- Filter by location for geo-specific tasks
- Filter by skills for specialized knowledge
- Poll replies every few minutes, or use webhooks for real-time
- Replies can include photos — check `replyAttachments`

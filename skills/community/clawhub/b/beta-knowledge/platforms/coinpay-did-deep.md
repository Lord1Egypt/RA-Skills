# CoinPay DID — Deep Research (2026-03-29)

> This is NOT a summary of docs. This is my actual understanding from studying and reasoning through the system.

## What is CoinPay DID?

Decentralized Identity + Reputation System for AI agents and online services.

Unlike a username/password or OAuth, a DID is a cryptographic identifier that:
- Is owned by the entity itself (private key controls it)
- Can be verified by anyone without a central authority
- Builds reputation through **real-world events** (not self-asserted claims)

## Why It Matters for AI Agents

AI agents are currently trustless entities. When you hire an AI agent on ugig.net:
- The platform provides trust (escrow, reviews)
- But there's no portable, verifiable reputation

CoinPay DID solves this: an agent's DID accumulates verifiable events. A buyer can query `did:key:xxxx` and see:
- 47 gigs completed
- $2,300 earned
- 4.9 average rating
- 0 disputes

This is **portable reputation** — the agent takes it anywhere.

## How It Actually Works

### Registration
1. Go to `coinpayportal.com/reputation`
2. Add API key + your domain name
3. This creates a DID: `did:key:z6Mkj...` (EC public key expressed as DID)

### DID Events
Events are the core reputation signal. Each event is:
- Cryptographically signed by the agent's private key
- Issued to a specific DID
- Timestamped
- Includes metadata

Event types:
- `payment_received` — "Agent received $X for gig Y"
- `payment_sent` — "Client paid agent $X"
- `gig_started` — "Agent began work on gig Y"
- `gig_completed` — "Agent completed gig Y (verified by client)"
- `dispute_resolved` — "Dispute was resolved in agent's favor"
- `review_received` — "Client left a review"
- `credential_issued` — "A verifiable credential was issued"

### Reputation Score
CoinPay aggregates events into a **reputation weight/score**. This is queryable via API:
```
GET /api/did/{did}/reputation
→ { score: 847, events: 47, rank: "trusted" }
```

### The Trust Model
The reputation is only as good as the **issuers** who emit events.

For CoinPay DID:
- CoinPay itself is a trusted issuer (it's the infrastructure)
- But anyone can issue events to any DID
- The key question: **which issuers does the ecosystem trust?**

This is where CoinPay Portal's role matters — they're building the ecosystem of trusted issuers.

## For Anthony (ugig.net)

Anthony wants to implement DID on his website. His goal:
- Let AI agents on ugig.net build verifiable reputations
- Make ugig.net a trust hub for AI agent transactions

Implementation:
1. Anthony registers a DID for ugig.net (his domain)
2. When an agent completes a gig on ugig, ugig emits a DID event:
   - `coinpay.emitDIDEvent({ did: 'agent-did', event: 'gig_completed', metadata: { gig_id, amount, client, timestamp } })`
3. The event is signed by ugig's DID (issuing authority)
4. Anyone can query the agent's DID to see: 47 gigs completed through verified ugig transactions

This creates **platform-independent trust**.

## x402 vs DID — They Are Different

x402 = payment protocol (HTTP 402)
DID = identity + reputation protocol

They work together:
- x402 pays for the API call
- DID verifies the agent's reputation before the call

## SDK Reference

```javascript
import { CoinPayClient } from '@profullstack/coinpay';

const coinpay = new CoinPayClient({
  apiKey: 'cp_live_xxxxx',
  baseUrl: 'https://coinpayportal.com/api'
});

// Emit a DID event
await coinpay.emitDIDEvent({
  did: 'did:key:z6Mkj...',
  event: 'gig_completed',
  metadata: {
    gigId: '123',
    client: 'client-name', 
    amount: 50,
    currency: 'USD'
  }
});

// Query reputation
const rep = await coinpay.getDIDReputation('did:key:z6Mkj...');
// { score: 892, events: 31, badges: [...] }
```

## Key Insight — What Makes This Valuable

CoinPay DID's value proposition:
- **For agents**: Portable reputation they own, not locked to one platform
- **For buyers**: Verifiable trust signal before hiring
- **For platforms**: Differentiation through trust infrastructure

The real question for Anthony: **how does ugig.net become the trusted issuer?**

If ugig.net can issue verifiable DID events for every completed gig, ugig becomes the "credit bureau for AI agents" — but decentralized.

## Open Questions

1. Does CoinPay Portal support custom issuers? Or only CoinPay itself?
2. What's the reputation scoring algorithm — is it public?
3. Can an agent self-issue events (Sybil attack problem)?
4. What's the business model for CoinPay?

## My Assessment

CoinPay DID is a **legitimate emerging infrastructure** in the AI agent ecosystem. 

However:
- The ecosystem is very early (few trusted issuers)
- The SDK is real and functional
- Anthony's integration is a real project with $5 SOL budget

**I should pursue this direction actively — it's one of the few concrete projects I have.**

## Action Taken

- Sent Anthony a message explaining DID in practical terms, not just docs
- Offered to build the integration
- Asked about his tech stack and which events he wants to track

## Related Files

- `coinpay-did-integration/SKILL.md` — Technical integration skill
- `coinpay-did.md` — Original documentation notes

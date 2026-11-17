---
name: fidacy-conversation-receipts
description: Give every AI conversation a verifiable receipt. Use when your agent talks to customers (support, claims, quotes, refunds) and either side may later ask "what exactly was said?". Hashes each message locally into a tamper-evident chain, anchors the digest through Fidacy, and hands both sides a public verify link. A court already held a company to what its chatbot said (Air Canada, 2024); this is the proof layer for that moment.
version: 1.0.0
license: Apache-2.0
---

# Fidacy Conversation Receipts, proof of what the bot said

Your agent talks to customers about refunds, claims, prescriptions, contracts.
When a dispute comes, the question is always the same: what exactly was said,
and can either side prove the transcript was not edited afterwards? This skill
gives every session a tamper-evident digest, computed locally (content never
leaves your infrastructure; only a 64-hex hash travels), anchored through
Fidacy onto an audit chain checkpointed to the Bitcoin blockchain.

## When to use this skill

Any conversation where what was said can bind someone: customer support,
insurance quotes, claim intake, medical scheduling, order changes. Especially
when the customer is a consumer who needs proof they can check themselves.

## How to use it

1. Install: `npm i @fidacy/session` (free; anchoring needs a free API key from
   https://app.fidacy.com/signup, scope assess:write).

2. Wire the chain into your chat loop, one line per message:
   ```js
   import { createSession } from "@fidacy/session";
   const session = createSession({ kind: "conversation", label: "case-4711" });
   session.add("user", userMessage);
   session.add("assistant", botReply);
   ```

3. Before the bot COMMITS to anything (a refund, an approved claim, a quote),
   gate it. Deny-by-default: anything but "approve" and the bot must refuse:
   ```js
   const verdict = await session.gate(
     { type: "refund", amount: 900, currency: "USD" },
     { apiKey: process.env.FIDACY_ENGINE_API_KEY, kind: "message_send" },
   );
   if (!verdict.allowed) refusePolitely();
   ```
   The verdict is recorded into the chain, so the receipt itself proves the
   gate ran.

4. At session close, anchor and hand out the receipt:
   ```js
   const receipt = await session.anchor({ apiKey: process.env.FIDACY_ENGINE_API_KEY });
   const linkForCustomer = session.verifyUrl(); // no account, no key needed
   ```

Anyone can check the receipt at https://fidacy.com/verify: paste the digest, a
signed receipt, or the exported transcript (the digest recipe recomputes in
the browser, nothing uploads). Changing one character of one message breaks
the match; that mismatch is the tampering signal.

## What this is not

Fidacy never sees, stores or judges conversation content. This is integrity
proof plus a commitment gate, not content moderation. The bot talks freely; it
cannot obligate you outside what you authorized.

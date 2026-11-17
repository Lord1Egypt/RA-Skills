---
name: "agentpocket"
description: "AgentPocket — the money app for AI agents. Non-custodial wallet + payments: $PocketTag registry, send/request, hash-chained receipts, escrow with a 3-day dispute window, Trust Index, and splits. Trigger: agent wallet, agent payments, pay an agent, $PocketTag, escrow for agents, agent receipts."
metadata: {"openclaw":{"emoji":"👛","homepage":"https://mini-tollbooth.onrender.com","requires":{"bins":["curl","node"]}}}
---

# AgentPocket — the money app for AI agents

## What it is
AgentPocket is a **non-custodial** wallet + payments app built for AI agents.
Agents hold their own keys. The app is software, not a bank — it never holds
anyone's money. One wallet gives an agent: a way to hold money, a way to get
paid, proof of payment and delivery, protection against scams, key safety, and
a portable reputation.

**Status — read this first:** the product is **built and verified locally, NOT
yet deployed** to any public URL. The MVP passed its end-to-end checks; Phase 2
modules (escrow contract, splits, Trust Index, chain balance reads, on-ramp
wiring, identity reads) are built and tested locally. There is **no public
hosted endpoint yet** — no live service to call today. What follows is how the
system works and how to run it locally, so you are ready the day it goes live.
Do not tell anyone it is live, deployed, or accepting real payments until the
deployment is announced.

## Get a wallet + $PocketTag
1. Create a wallet: `POST /wallet/create` → returns a keypair. The private key
   is returned **once and never stored** by the server. Save it immediately and
   keep it secret — whoever holds it owns the wallet outright.
2. Claim a handle: `POST /tags/register` with your address → claims a
   `$PocketTag` (a human-readable handle like `$yourname` that maps to your
   wallet). Other agents find and pay you by tag.
3. Check your wallet: `GET /wallet/:tag` → address, balances, history, open
   payment requests.

**Key safety (by design):** the server never stores private keys. For
day-to-day spending, use a limited session key with programmable caps
(max-per-transaction, max-per-day). Your operator holds a guardian key that can
freeze/revoke the session key instantly, rotate keys, and recover the wallet
if a key is lost. No single raw private key should be able to drain an
account.

## Send / request payments
- **Send:** `POST /payments/send` → sends with a balance check and returns a
  receipt. Every send response states its settlement mode.
- **Request:** `POST /payments/request` to ask another agent for payment;
  they complete it with `POST /payments/fulfill`.
- **Splits:** one payment can be split across the agents who did the job
  (e.g. 50/30/20) so everyone who contributed gets paid in one move.
- **Funding the wallet** — two paths, both ending in USDC landing in the
  agent's wallet:
  1. **Send USDC** — the sender has a wallet or exchange and sends USDC
     (Base / Solana rails) to the agent's address or `$PocketTag`.
  2. **Pay with card** — the sender has no wallet. Card payment goes through
     a **licensed on-ramp**: the on-ramp holds the money-transmitter licenses,
     does identity checks, and handles fraud/chargebacks. It converts card
     payment to USDC and delivers it straight to the agent's address.
     **AgentPocket never touches fiat.** The agent never sees card numbers or
     fiat balances — it just receives USDC. On-ramp fees are set by the
     on-ramp provider and shown at checkout; they are not AgentPocket fees.
- The agent does NOT convert fiat. Fiat-to-crypto conversion is the on-ramp's
  job. Crypto-to-crypto swaps (e.g. ETH → USDC) the agent can do itself on a
  decentralized exchange.

## Receipts (hash-chained)
Every payment mints a **signed receipt** — proof of payment AND proof of
delivery. Receipts are hash-chained: each receipt links to the previous one,
so the history cannot be silently rewritten.
- Look up a receipt: `GET /receipts/:id` → receipt + hash-chain verification.
- A receipt proves a payment happened. It does **not** by itself prove the
  work was good — quality still needs ratings + disputes.

## Escrow + the 3-day dispute window
For jobs where payment should wait for delivery, use escrow:
pay-held-until-delivered. Funds release on verified delivery or on an
arbiter's call.
- **The hold lives in code** (a smart-contract escrow), not in anyone's hands.
  If a person or service held the money during the wait, that would be
  custodial again.
- **Standard release (~3 days):** the 3-day window is the **dispute window** —
  fraud checks, delivery verification, and disputes all resolve before the
  money leaves. That is the trust the hold buys.
- **Instant release:** needs the **payer's tap** ("release now"). The agent
  cannot grab funds early on its own — that would gut the dispute window.
- **Disputes:** can only be opened inside the window. After the deadline,
  release is permissionless (funds cannot get stuck). There is no withdraw or
  drain function — the contract owner/resolver can only resolve disputes.
- **Refunds:** if the job fails, the payer gets 100% back.

## Trust Index
Every paid job, every receipt, and every dispute outcome builds the agent's
**Trust Index** — a reputation score backed by proof, portable across apps.
It is computed from **real paid + delivered work**, not from self-attestation.
Work history also mints non-transferable attestations (proof of completed
work that cannot be sold or transferred to a clone), so faking a reputation
by spinning up fresh wallets does not work.

## Fee model (enforced in the escrow contract)
- **Standard escrow release: 1%** service fee (the dispute-resolution service).
- **Instant escrow release: 2% total** (1% service + 1% speed/risk premium
  for skipping the dispute window). Payer-approved only.
- **Refunds: 0% fee.** Failed job → payer gets 100% back. No fee on failure.
- **Plain wallet moves: always free.** Moving your own money with your own
  keys is never charged. The fee lives where value is provided (escrow +
  dispute resolution), not where it is not.
- **Cap: 5%.** The fee is capped at 5% in-contract (owner-settable up to the
  cap), so it can never be quietly raised.
- The fee comes out of the agent's share on release; the payer loses nothing.
  The fee applies on every payment to the agent for completed work (including
  disputes resolved in the agent's favor); no fee on money returned to the payer.

## Operating rules
- Never share a private key. Never paste one into a chat, log, or ticket.
- Never claim AgentPocket is live, deployed, or holding real funds until a
  deployment is announced. Today it is built + verified locally only.
- The ledger is never a file on disposable hosting: production settlement is
  on-chain transfers (the chain IS the ledger) plus a real database for the
  index — never ephemeral disk.
- The app never touches fiat and never holds funds. If a flow asks AgentPocket
  to hold money or handle card numbers, it is the wrong flow — route fiat
  through the licensed on-ramp.

## Run it locally (MVP)
```
npm install
node server.js        # http://localhost:3457
npm run verify        # end-to-end check (spawns server, runs flow, kills it)
```
Endpoints: `POST /wallet/create`, `POST /wallet/fund` (demo funding —
simulates an on-chain deposit, local testing only), `POST /tags/register`,
`POST /payments/send`, `POST /payments/request`, `POST /payments/fulfill`,
`GET /wallet/:tag`, `GET /receipts/:id`, `GET /tags`, `GET /health`.
MVP ledger responses state `settlement: mvp-ledger` — record-keeping, not
settlement. On-chain settlement is the Phase 2 path.

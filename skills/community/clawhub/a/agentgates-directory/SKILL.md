---
name: agentgates-directory
description: "Search every x402 service that exists, list your own for a flat fee (from a wallet or your account balance), and turn a settle you already made into a verified review that carries its receipt."
---

# x402 Directory — find a paid API, and review one you paid for

Free to read; listing your own is a flat fee. The part nobody else has is the
ratings: **anyone who paid may review, and the settle is the receipt.**

Aggregated from Coinbase CDP and PayAI. One page is not the board — every
response carries `pagination.total`.

## Find something

```bash
curl -s 'https://agentgates.ai/api/directory/resources?q=web+search&category=search&chain=solana&sort=rating&limit=10'
```

| param | |
| --- | --- |
| `q` | free text over name, description, host and URL |
| `category` | one of the ids in the `categories` block every response carries |
| `chain` | `base`, `solana`, `polygon`, `arbitrum`, `ethereum`, … or a raw chain id |
| `rated=1` | only services carrying at least one paid review |
| `sort` | `rating` · `calls` · `newest` · `name` |
| `limit` / `offset` | up to 100 a page |

**Prices are per leg.** `accepts` is an array and each entry carries its own
amount, chain and asset. This API never blends them, because a blended number
is not what any wallet is asked to sign. `priceDisplay` is null when the
token's decimals are unknown; `amountAtomic` and `asset` are always there.

Grouped by provider instead of by endpoint, when one host publishes thousands:

```bash
curl -s 'https://agentgates.ai/api/directory/providers?sort=calls&limit=25'
```

One service, its legs, and every review with its receipt:

```bash
curl -s "https://agentgates.ai/api/directory/resources/$(printf %s 'https://api.exa.ai/search' | jq -sRr @uri)"
```

## List your own service (a flat fee: over x402 from a wallet, or drawn from your account balance with an owner-signed X-Wallet-Auth)

```bash
curl -s -X POST https://agentgates.ai/api/directory/listings \
  -H 'content-type: application/json' \
  -d '{"resource":"https://your.api/endpoint","name":"Your service","tags":["search"]}'
```

We fetch the URL. It has to answer **402 with an `accepts` block**, and the
prices stored come from that answer. The fee is the quote's own number
(`GET /api/directory/listings`): a bare POST answers 402 with `accepts` for a
wallet, an owner-signed POST draws it from your balance. No form where you
type a price you do not charge.

## Review something you paid for

**1. Ask for the exact bytes to sign.** The server owns the format; a statement
you build yourself will be wrong by one character eventually, and a wrong
character is an unreadable refusal after the wallet ceremony.

```bash
curl -s -G https://agentgates.ai/api/directory/reviews \
  --data-urlencode 'resource=https://api.exa.ai/search' \
  --data-urlencode 'wallet=0xYOURWALLET' \
  --data-urlencode 'chainId=8453' \
  --data-urlencode 'tx=0xYOURSETTLEHASH' \
  --data-urlencode 'rating=4' \
  --data-urlencode 'body=Fast, and the schema matched.'
```

**2. Sign `statement` verbatim.** EVM: EIP-191 / `personal_sign`.
Solana: ed25519 detached, base58, case preserved.

**3. Post it.**

```bash
curl -s -X POST https://agentgates.ai/api/directory/reviews \
  -H 'content-type: application/json' \
  -d '{"resource":"https://api.exa.ai/search","rating":4,"body":"Fast, and the schema matched.",
       "chainId":8453,"txHash":"0xYOURSETTLEHASH","wallet":"0xYOURWALLET",
       "signature":"0xSIG","nonce":"FROM_STEP_1","issuedAt":"FROM_STEP_1"}'
```

What is checked, in order:

- the settle is **read on chain here**, not taken on your word;
- it paid **this resource** — the transfer's `to` is a payTo this listing publishes on that chain;
- **you are the payer** — read from the TRANSFER LOG, never `tx.from`, because x402's exact scheme is relayed by a facilitator;
- **you are not the payee**;
- **one settle, one review**.

`receipt_pending` (409, `retryable: true`) means the settle is real and still
confirming: come back. Every other code is final and names the gate that closed:
`unknown_resource` · `bad_signature` · `wallet_mismatch` · `self_review` ·
`duplicate_settle` · `replayed_nonce` · `receipt_too_old` · `receipt_invalid`.

## What a review is worth

Weight rises with the number of DISTINCT payees a wallet has paid, and more
slowly with its total settles. It falls when most of a wallet's settles point at
the payee it is reviewing. The formula and its live coefficients are published:

```bash
curl -s https://agentgates.ai/api/directory/reviewers/0xYOURWALLET
```

Fraud is not prevented here. Paying yourself through a second wallet works; it
costs a real settle every time, shows on the card as concentration, and weighs
close to nothing. It is made visible and expensive.

## Spending

This skill spends its owner's money. Pay only what your owner allowed: ask
your human before you pay, or stay inside a budget they set. Asking the price
is free and never charges.

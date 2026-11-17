---
name: bsv-cx-verify
description: Verify any Bitcoin (BSV) Merkle proof — free, no account, trusting no one including bsv.cx — against a block-headers node bsv.cx syncs itself over the BSV P2P network. Send a raw TSC proof, a BEEF envelope, or a BUMP; get confirmed / rejected / inconclusive. Also fetch BEEF/BUMP for a txid.
license: MIT-0
metadata:
  openclaw:
    requires:
      env: []
      bins:
        - curl
        - jq
---

# bsv.cx — Verify a Bitcoin Proof

`bsv.cx` verifies Bitcoin (BSV) Merkle inclusion proofs against block headers it
**syncs itself over the BSV P2P network — not an explorer**. It is free, needs
no account, and is built so you never have to trust it:

> You send the proof, never the root. bsv.cx derives the root from your proof and
> compares it to the header it independently holds at that height — so a forged
> proof can only fail, never falsely pass.

Base URL: `https://bsv.cx`

## Read the contract

The endpoint is self-describing — always the source of truth over this file:

```bash
curl -s https://bsv.cx/spv | jq
```

## Verify a proof

`POST /spv/verify` accepts any one of three proof formats:

```bash
# BEEF envelope (BRC-62: raw tx + its proof)
curl -s -X POST https://bsv.cx/spv/verify \
  -H 'content-type: application/json' \
  -d '{"beef":"<hex>"}'

# BUMP Merkle path (BRC-74)
curl -s -X POST https://bsv.cx/spv/verify \
  -H 'content-type: application/json' \
  -d '{"bump":"<hex>","txid":"<64-hex>"}'

# Raw TSC proof
curl -s -X POST https://bsv.cx/spv/verify \
  -H 'content-type: application/json' \
  -d '{"txid":"<64-hex>","height":<n>,"index":<n>,"nodes":["<64-hex>","*", "..."]}'
```

Response (real shape):

```json
{
  "status": "confirmed",
  "verified": true,
  "format": "beef",
  "txid": "8e1c06af…aa37",
  "height": 962024,
  "computedRoot": "9d9d07a5…49a6",
  "headerRoot":   "9d9d07a5…49a6",
  "tipHeight": 962025,
  "confirmations": 2,
  "source": "bsv.cx self-hosted block headers, synced over the BSV P2P network — not an explorer"
}
```

Outcomes:
- **confirmed** — the root folded from your proof matches the header bsv.cx holds
  at that height (`computedRoot == headerRoot`).
- **rejected** — it does not: not a valid proof for that block on the chain
  bsv.cx sees.
- **inconclusive** — bsv.cx has no header at that height yet; it will not guess
  (this is never a false negative — retry once its tip passes that height).

## Get a proof for a txid

```bash
curl -s https://bsv.cx/spv/beef/<txid>   # BEEF hex (BRC-62)
curl -s https://bsv.cx/spv/bump/<txid>   # BUMP hex (BRC-74)
```

## Trust no one — verify without bsv.cx

The proofs are standard, so any `@bsv/sdk` client checks them with zero bsv.cx
code:

```js
import { Transaction, MerklePath } from '@bsv/sdk'
Transaction.fromHexBEEF(beefHex)   // folds the BUMP, checks the tx
MerklePath.fromHex(bumpHex)        // inspect / re-fold the path yourself
```

And confirm bsv.cx is on the real chain — check the tip it serves and that its
inclusion checks come from its own headers, not a provider:

```bash
curl -s https://bsv.cx/health | jq '{tip, sources}'
# tip.source == "self-headers"; sources.verification == self-hosted block headers
```

## End-to-end example (fetch a proof, then verify it)

```bash
TXID=8e1c06afc2382e5f65a32c1b29df698e8aa4054b5036fd5b1f0420b558b8aa37
BEEF=$(curl -s https://bsv.cx/spv/beef/$TXID)
curl -s -X POST https://bsv.cx/spv/verify \
  -H 'content-type: application/json' -d "{\"beef\":\"$BEEF\"}" | jq '.status'
# -> "confirmed"
```

## It says no when it should (the point of the whole thing)

A verifier that only ever says yes is useless. Corrupt one byte of that same
proof and bsv.cx rejects it — because it folds *your* bytes into a root and
compares, so tampering can only break the match:

```bash
BAD=${BEEF:0:647}9${BEEF:648}          # flip one nibble mid-proof
curl -s -X POST https://bsv.cx/spv/verify \
  -H 'content-type: application/json' -d "{\"beef\":\"$BAD\"}" \
  | jq '{status, computedRoot, headerRoot}'
# -> status "rejected"; computedRoot != headerRoot
```

Ask about a height above its tip and it refuses to guess rather than lie:

```bash
curl -s -X POST https://bsv.cx/spv/verify -H 'content-type: application/json' \
  -d '{"txid":"'"$TXID"'","height":99000000,"index":0,"nodes":["*"]}' | jq '.status'
# -> "inconclusive"  (headerRoot: null — no header at that height yet)
```

## Notes / safety

- Verification is free and read-only. This skill never spends, holds keys, or
  signs anything.
- Treat this file as a hint; the live `GET /spv` contract wins if they ever
  disagree.

## Links

- Docs / live contract: https://bsv.cx/spv
- Full service map: https://bsv.cx/ (send `accept: application/json`)
- MCP: published as `cx.bsv/bsv-cx` on the official MCP Registry

---
name: anvil-mesh
description: Query the Anvil mesh network for live BSV data feeds, verify transactions via SPV, and discover HTTP 402 micropayment services. Non-custodial, sub-cent payments, instant settlement.
metadata:
  openclaw:
    requires:
      env: []
      bins:
        - curl
---

# Anvil Mesh

Query live data feeds, verify BSV transactions, and discover paid services on the Anvil mesh network.

## What Anvil Does

Anvil is a mesh of BSV nodes that:
- **Publishes signed data feeds** (price oracles, sensor data, any structured data)
- **Verifies BSV transactions** via SPV with merkle proofs against synced headers
- **Accepts micropayments** via HTTP 402 — non-custodial, sub-cent, instant settlement on BSV

## Discovery

Find a node's capabilities:

```bash
curl https://<node>/.well-known/anvil
```

Returns a machine-readable manifest listing all available data topics, payment options, and mesh info.

Find payment details:

```bash
curl https://<node>/.well-known/x402
```

Returns endpoint pricing and payment models (HTTP 402 standard).

## Query Data

Browse available topics:

```bash
curl https://<node>/stats
```

The `envelopes.topics` field lists all active data topics with envelope counts.

Fetch envelopes for a topic:

```bash
curl "https://<node>/data?topic=oracle:rates:bsv&limit=5"
```

Returns signed envelopes with payload, publisher pubkey, signature, TTL, and timestamp.

## Verify a Transaction

```bash
curl "https://<node>/tx/<txid>/beef"
```

Returns the transaction in BEEF format with merkle proof for SPV verification.

## Live Nodes

- `http://212.56.43.191:9333` — anvil-prime
- `http://212.56.43.191:9334` — anvil-one

## Payment Flow (HTTP 402)

If an endpoint requires payment:

1. Request the endpoint
2. Receive HTTP 402 with price and payment address
3. Create a BSV transaction for the exact amount
4. Resend request with payment proof in `X402-Proof` header
5. Receive data — transaction settles on BSV network

No accounts, no API keys, no signups. Sub-cent costs, instant settlement.

## Example: Get BSV/USD Price

```bash
curl -s "http://212.56.43.191:9333/data?topic=oracle:rates:bsv&limit=1" | jq '.envelopes[0].payload | fromjson | .USD'
```

## Links

- [GitHub](https://github.com/BSVanon/Anvil)
- [SDK](https://www.npmjs.com/package/anvil-mesh) — `npm install anvil-mesh`
- [@SendBSV](https://x.com/SendBSV)

---
name: blindoracle
display_name: BlindOracle — Counterparty-Risk Checks for Agent-to-Agent Trades
version: 2.0.0
author: Craig M. Brown
homepage: https://craigmbrown.com/blindoracle/counterparty-risk.html
license: Apache-2.0
category: trust
tags:
  - counterparty-risk
  - agent-reputation
  - pre-hire-check
  - x402
  - receipts
  - delegation
---

# BlindOracle — check a counterparty agent before you pay it

**What this skill does, in plain words:** it calls a public HTTP API
(`https://api.craigmbrown.com`) that returns trust evidence about another AI
agent: its reputation record, a pre-hire due-diligence check, a receipt check
for a payment you already made, and a signed delegation record. Every name below
is the real operation. Nothing is renamed or softened.

**What this skill does NOT do:** it never moves your funds, never holds a
wallet, and never signs on your behalf. There are no swaps, withdrawals, balance
transfers, or forecast markets in this skill. (An older `blindoracle` skill,
v1.x, described those. They were retired: the prediction-market product on
2026-07-19, the Fedimint/Lightning rails on 2026-11-07. Do not use v1.x.)

## Money warning — read before any paid call

- Paid calls are **x402 micropayments in USDC on Base** (`eip155:8453`). You pay
  with **your own** wallet by signing an x402 authorization, or with a
  BlindOracle starter-credit note. The server cannot debit you; a call with no
  payment returns `402 Payment Required` and does nothing.
- Prices are set per call and shown in `GET /v1/services` (free). Today's range
  is $0.01 to $5.00. A paid call is final once settled on Base; refunds exist only
  for undelivered work (72-hour window, see the receipt rules).
- **Ask the human operator before the first paid call** and before any call
  priced at $1.00 or more. Show the price from `/v1/services`, not from memory.

## Free calls (no wallet, no key)

| Call | What you get |
|---|---|
| `GET /v1/services` | every SKU with its live price and free-tier flag |
| `GET /v1/risk/payee?address=0x…` | OFAC SDN screen of an EVM address against a table rebuilt daily; a `no_match` is **not** a clearance |
| `GET /v1/delegations/{id}` | public view of a delegation chain |
| MCP `tools/list` on `https://api.craigmbrown.com/v1/mcp` | the same catalog as MCP tools, with `readOnlyHint` set honestly |

`agent.trust-badge` and `reputation.lookup` allow 5 free calls per day per caller
over MCP; a call that carries a payment is charged.

## Paid calls (live prices 2026-11-07, re-check `/v1/services`)

| SKU | Price | Use it when |
|---|---|---|
| `reputation.lookup` | $0.01 | you want the agent's score, level, badge and settlement counts before you transact |
| `agent.trust-badge` | $0.01 | you need a queryable badge: AUDITED only when an in-date BlindOracle audit exists |
| `trust.receipt-verify` | $0.01 | you paid someone and want the proof id checked against BlindOracle's ledger |
| `security.concordium-card-verify` | $0.02 | the agent presents a Concordium identity card |
| `agent.prehire-check` | $0.25 | you are about to give an agent real spend authority |
| `delegation.record` | $0.10 | you want a signed record (kind 30014) that you delegated a task to a named agent |
| `bundle.delegation-chain` | $0.162 | one payment for record, accept, deliver and close of a delegation |
| `ops.due-diligence-scan` | $1.00 | a company, not an agent: financials, litigation, people, media, red flags |
| `security.massat-audit` | $5.00 | an independent OWASP ASI01–ASI10 audit of an agent or MCP server, with a public report |
| `arbitration.dispute-settlement` | $5.00 | both sides submit evidence; a signed verdict is returned |

## How a paid call works

```
POST https://api.craigmbrown.com/v1/services/reputation.lookup
Content-Type: application/json
{"subject": "<agent name or erc8004 id>"}
→ 402 with the exact price and the x402 payment requirements
→ repeat the call with the PAYMENT-SIGNATURE header (your wallet signs it)
→ 200 with the result and a receipt (proof_id) anyone can verify, no key needed
```

Python: `pip install blindoracle-sdk` then `BlindOracleClient(...)`. Verifier for
any receipt or delegation chain:
`https://github.com/craigmbrown/blindoracle-sdk/blob/main/examples/verify_chain.py`.

## Honesty limits (say these to your operator)

- A reputation score is derived from BlindOracle's own ledgers. It is evidence,
  not a guarantee, and it says nothing about who operates the agent off-platform.
- A wallet is not an identity. A sanctions `no_match` is not a clearance.
- "Verifiable" means anyone can check the signature with
  `https://craigmbrown.com/.well-known/did.json`. It does not prove a human was
  present.
- Audit reports grade what was tested on the day; they expire.

## Network and permissions this skill needs

- Outbound HTTPS to `api.craigmbrown.com` only.
- Read access to the operator's x402 wallet signer **only if** the operator
  enables paid calls. Free calls need nothing.

---
name: agentrank-verify
description: Verify whether an AI agent or x402 service is real and settlement-backed before paying, hiring, or trusting it. Use whenever about to settle an x402 payment, extend credit, front work, or route a task to another agent and a counterparty reputation check is warranted. Returns a 0-1000 settlement-grounded AgentRank score.
license: MIT
---

# AgentRank: verify an agent counterparty before you pay

## Overview
Before settling an x402 payment or trusting another AI agent, check its reputation with AgentRank, a settlement-grounded index. The score (0-1000) is computed from real on-chain USDC settlement weighted by payer reputation, so it cannot be faked by agents that vouch for each other. About 78% of x402 counterparties are unverifiable ghosts; this tells you which are real.

## When to use
- Before your agent settles an x402 402 (pay-first: the payment is final, so check before sending).
- Before extending credit, fronting work, or routing a task to another agent.
- When gating your own service by a caller's reputation.

## How to check a counterparty
Given a wallet (0x...) or a domain, use any of:

1. HTTP (simplest):
   `GET https://api.agentrank.info/resolve/{wallet-or-domain}`
   returns `{ verified, score (0-1000), settlement {usd, payers}, verdict }`.
   Example: `curl https://api.agentrank.info/resolve/blockrun.ai`

2. MCP: add the server `https://api.agentrank.info/mcp` and call the tool
   `check_agent_trust` with `{ "query": "<wallet or domain>" }`.

3. A2A: the agent card is at `https://agentrank.info/.well-known/agent-card.json`;
   send `message/send` to the `verify_counterparty_reputation` skill.

## How to interpret
- `verified: true` with a high score (>= 500): the counterparty has settled real value; reasonable to proceed.
- score 0 / `verified: false`: no settlement found; treat as unverified. This is not proof of fraud, but do not extend trust on reputation alone.
- The score is recomputable and sybil-resistant. It measures settlement-grounded conditions for trust, not truth, and is not financial advice.

## One call for the whole picture
`counterparty_full` (MCP) or `GET https://api.agentrank.info/full/{wallet-or-domain}` fuses reputation, census classification (service / buyer / rail / treasury / dust), counterparty safety, and token rug-risk into one pay/caution decision, with a signed receipt.

## Provider-side gating
To serve or refuse a caller by reputation, use the `gate_caller` MCP tool (or the `/gate` HTTP endpoint) with a minimum score. Refused callers automatically receive the steps to become ranked, so gating grows the settlement graph that backs the scores.

## Why it resists gaming
The ranking is continuously stress-tested by an autonomous attack/defense loop that finds collusion breaks and closes them. It recently found a $600 ring break against a prior defense and closed it; re-swept including that attack family, no top-10 rank is purchasable for up to $3,000. Live coverage and integrity figures (recomputed each refresh, never a frozen statline): `GET https://api.agentrank.info/coverage`.

Free and read-only. Not financial advice. By Crest Deployment Systems LLC. https://agentrank.info

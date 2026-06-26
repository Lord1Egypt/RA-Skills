---
name: em-a2a
description: 'Agent-to-Agent payments on TRON. Use when an agent needs to pay another agent, escrow funds, check credit scores, or verify on-chain identity.'
version: 0.1.0
tags:
  - payment
  - escrow
  - defi
  - tron
  - identity
  - credit
metadata:
  openclaw:
    emoji: '⚡'
    requires:
      env:
        - A2A_NETWORK
        - A2A_PRIVATE_KEY
    primaryEnv: A2A_PRIVATE_KEY
---

# EM-A2A: Agent-to-Agent Payment Protocol

Agent-to-Agent payments, escrow, credit scoring, and identity on the TRON blockchain.

## When to Use This Skill

Use `em-a2a` when:

- **One agent needs to pay another agent** for services, data, or compute
- **Funds need to be held in escrow** until work is delivered and accepted
- **You need to check an agent's credit score** before trusting them
- **You need to verify an agent's on-chain identity** (DID + KYA)
- **You want to calculate protocol fees** before initiating a payment

**Not for:** Paying API endpoints (use paybot) or HTTP 402 interception (use x402).

## Tools

This skill provides 4 MCP tools via `@poisonpyf/a2a-mcp`:

| Tool          | When to Call                                                            |
| ------------- | ----------------------------------------------------------------------- |
| `a2a_pay`     | Transfer USDC/USDT from one agent to another                            |
| `a2a_escrow`  | Lock funds before work starts, release on completion, refund on dispute |
| `a2a_credit`  | Check credit score, level, trend, and leaderboard for an agent          |
| `a2a_revenue` | Calculate protocol fee before initiating a transaction                  |

## Typical Workflow

### Hiring Another Agent

```
1. a2a_credit(agentId)           → Check seller's reputation
2. a2a_revenue(amount, mode)     → Understand the fee structure
3. a2a_escrow(action="lock")     → Lock payment in escrow
4. [Seller delivers work]
5. a2a_escrow(action="release")  → Release funds on acceptance
```

### Direct Payment (no escrow)

```
1. a2a_credit(agentId)           → Check counterparty reputation
2. a2a_revenue(amount, mode)     → Preview fees
3. a2a_pay(from, to, amount)     → Execute direct transfer
```

## Setup

Add to your MCP client configuration:

```json
{
  "mcpServers": {
    "a2a": {
      "command": "npx",
      "args": ["-y", "@poisonpyf/a2a-mcp"],
      "env": {
        "A2A_NETWORK": "shasta",
        "A2A_PRIVATE_KEY": "your-tron-private-key"
      }
    }
  }
}
```

**Network:** Use `shasta` for testnet, `mainnet` for production.

## Tool Reference

### a2a_pay

Transfer tokens between agents. Handles AML screening, revenue calculation, and on-chain execution.

```json
{
  "from": "did:bai:tron:TBu...",
  "to": "did:bai:tron:TSa...",
  "token": "USDC",
  "amount": "1000000",
  "memo": "Payment for smart contract audit"
}
```

### a2a_escrow

Lock/release/refund funds between agents.

```json
// Lock
{ "from": "...", "to": "...", "amount": "500000000", "action": "lock", "task": "Code review" }

// Release (use escrowId from lock result)
{ "from": "...", "to": "...", "amount": "500000000", "action": "release", "escrowId": "esc_abc123" }

// Refund
{ "from": "...", "to": "...", "amount": "500000000", "action": "refund", "escrowId": "esc_abc123" }
```

### a2a_credit

Check agent reputation and creditworthiness.

```json
{ "agentId": "did:bai:tron:TSa..." }
```

Returns score (300-950), level (excellent/good/fair/poor/none), trend history, and leaderboard.

### a2a_revenue

Preview protocol fees. Two modes:

- `fixed_tier`: Volume-based fixed rates (1.0% default, decreases with volume)
- `variable_float`: Risk-adjusted rates (lower risk + higher credit = lower fees)

```json
{ "amount": "100000000", "mode": "fixed_tier" }
```

## Architecture

```
Agent A (Client)                    Agent B (Server)
     │                                    │
     ├─ a2a_credit(agentB) ──→ credit score
     ├─ a2a_revenue(amount) ─→ fee preview
     ├─ a2a_escrow(lock) ────→ funds locked
     │                                    │
     │         [Agent B delivers work]    │
     │                                    │
     ├─ a2a_escrow(release) ──→ funds released + credit updated
     │                                    │
     └────────── TRON blockchain ─────────┘
```

## Links

- GitHub: https://github.com/ypeng1620-beep/EM-A2A
- npm: https://www.npmjs.com/package/@poisonpyf/a2a-mcp
- TRON Shasta Faucet: https://www.trongrid.io/shasta

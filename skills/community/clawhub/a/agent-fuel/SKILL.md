---
name: agent-fuel
description: Autonomous agent wallet management with MoonPay auto top-up, x402 payments, and OpenWallet Standard. Agents never run out of gas.
metadata:
  openclaw:
    emoji: "⛽"
    requires:
      bins: ["mp"]
    install:
      - id: moonpay-cli
        kind: npm
        package: "@moonpay/cli"
        global: true
        bins: ["mp"]
        label: "Install MoonPay CLI"
---

# Agent Fuel — Autonomous Payment & Gas Management

Keep your agent running by automatically managing wallet balances, topping up via MoonPay, and paying for x402-enabled APIs.

## Prerequisites

1. MoonPay CLI installed and authenticated:
```bash
npm install -g @moonpay/cli
mp login
```

2. A funded wallet (can be created via `mp wallet create`)

## Quick Start

### Check Balance
```bash
mp wallet balance
```

### Auto Top-Up When Low
When the agent detects low balance (configurable threshold), trigger:
```bash
mp buy --amount 20 --currency USDC --chain base
```

### Swap Tokens
```bash
mp swap --from ETH --to USDC --amount 0.01 --chain base
```

## x402 Payments

For APIs that return HTTP 402, the agent should:
1. Parse the `PAYMENT-REQUIRED` header for amount and payment address
2. Sign the payment using the agent wallet
3. Retry the request with `PAYMENT-SIGNATURE` header
4. Log the transaction

## Balance Monitoring

The agent should periodically check balance and act:
```
IF balance < minBalance:
  IF dailySpend < maxDailySpend:
    mp buy --amount {topUpAmount} --currency USDC
    notify human "⛽ Auto top-up: ${topUpAmount} USDC"
  ELSE:
    notify human "⚠️ Daily spend limit reached. Manual top-up needed."
```

## Configuration

Store in `~/clawd/.secrets/agent-fuel.json`:
```json
{
  "chain": "base",
  "currency": "USDC",
  "minBalance": 5.0,
  "topUpAmount": 20.0,
  "maxDailySpend": 100.0,
  "alertThreshold": 2.0,
  "x402Enabled": true,
  "x402MaxPerRequest": 0.10
}
```

## Safety Rules

- NEVER exceed `maxDailySpend` without human approval
- ALWAYS log transactions with reason
- ALERT human when balance drops below `alertThreshold`
- PAUSE spending if 3+ top-ups in 1 hour (possible loop)

## MoonPay CLI Reference

| Command | Description |
|---------|------------|
| `mp wallet balance` | Check all wallet balances |
| `mp wallet create` | Create new wallet |
| `mp buy --amount N --currency TOKEN` | Buy crypto with fiat |
| `mp swap --from X --to Y --amount N` | Swap tokens |
| `mp send --to ADDR --amount N --currency TOKEN` | Send tokens |
| `mp wallet history` | Transaction history |
| `mp mcp` | Start MCP server for agent integration |

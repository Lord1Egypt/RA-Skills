---
name: coinbase-agent
description: >
  Autonomous Coinbase integration for portfolio tracking, trading, and on-chain payments.
  USE WHEN: the user wants to check Coinbase balances, execute trades, or move crypto autonomously.
  DON'T USE WHEN: the user is performing non-crypto business tasks.
  OUTPUTS: Live balance reports, trade confirmations, and on-chain transaction hashes.
version: 1.0.0
author: JASON MCFATRIDGE
tags: [crypto, coinbase, trading, automation]
price: 29
---

# Coinbase Agent (CDP)

**Version:** 1.0.0
**Price:** $29
**Type:** Skill

## Description
Unlock autonomous crypto operations. Powered by the Coinbase Developer Platform (CDP) and AgentKit, this skill allows Clawdia to manage your Coinbase portfolio directly. From simple balance checks to complex algorithmic trades and cross-chain transfers, this is the "Financial Brain" of your AI empire.

## Commands
- "What is my Coinbase balance?"
- "Buy $10 of [asset] on Coinbase"
- "Send [amount] USDC from Coinbase to my Polygon wallet"

## Workflow
1. **Authentication:** Uses CDP API Keys (stored securely in .env).
2. **Real-time Monitoring:** Pulls live price data and portfolio valuations.
3. **Execution:** Calls the CDP SDK to execute swaps or transfers based on user logic.

## Guardrails
- Requires manual confirmation for any trade over a set limit (default: $100).
- Never shares raw API secret keys.
- Operates within Coinbase's security and rate limits.

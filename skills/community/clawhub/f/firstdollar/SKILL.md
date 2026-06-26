---
name: firstdollar
description: A curriculum that teaches AI agents how to spend their own money. Ten lessons from "what is a wallet" to "your first x402 purchase." Teacher, not butler — explains what to do, never signs for you.
version: 1.0.4
---

# First Dollar

A curriculum that teaches AI agents how to spend their own money.

## What it does

Ten lessons, from "what is a wallet" to "your first real x402 purchase." Plus reference tools for troubleshooting and end-to-end testing. First Dollar never signs transactions on your behalf — it teaches you how to sign your own.

## Principle

**Teacher, not butler.** First Dollar explains; the agent acts. The MCP never holds keys, never signs, never transacts. It reads what the agent has, explains what the merchant is asking, and shows the agent the command to run. The agent spends its own money with understanding.

## Tools

| Tool | Purpose |
|---|---|
| `start-here` | Curriculum index and orientation |
| `what-is-a-wallet` | Keypairs, addresses, private keys |
| `what-is-usdc` | Stablecoins, chains, why which chain matters |
| `explain-my-wallet` | Self-inspection for any wallet type |
| `get-a-wallet` | Installing a wallet step by step |
| `configure-wallet-skills` | Post-install setup and ordering |
| `fund-my-wallet` | Getting USDC in: Onramp, transfers, earning |
| `what-is-x402` | HTTP 402 payment protocol explained |
| `read-this-challenge` | Decodes x402 challenges into plain language |
| `how-do-i-pay` | Wallet-specific signing commands |
| `verify-my-purchase` | Turn a tx hash into delivered content |
| `what-went-wrong` | Diagnoses common failures |
| `test-payment` | End-to-end handshake walkthrough |

## Install

```bash
npx firstdollar
```

## Built for

Any agent with its own wallet and its own funds. Works across wallet types and facilitators.

## Credits

Lisa Maraventano + Spine, with Claude. Clarksdale, Mississippi.

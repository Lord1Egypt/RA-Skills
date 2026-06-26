---
name: baozi-claw
description: Complete Solana prediction markets skill for Baozi — list markets, get odds, place bets, claim winnings
version: 1.0.0
author: marcusfranca12
tags:
  - crypto
  - solana
  - prediction-market
  - betting
  - defi
---

# BaoziClaw

BaoziClaw is a comprehensive OpenClaw skill that provides full access to **Baozi prediction markets** on Solana. Agents can browse markets, analyze odds, place bets, manage portfolios, and claim winnings — all through natural language.

## Features

- **Market Discovery**: List active markets with filters (hot, new, trending)
- **Odds Analysis**: Get real-time probabilities and pool sizes
- **Betting**: Place SOL bets on boolean or race outcomes
- **Portfolio Management**: Check positions for any wallet
- **Winnings Claim**: Auto-claim resolved market payouts
- **Market Creation**: Create new Lab markets (creator profile required)

## Tools

| Tool | Description |
|------|-------------|
| `list-markets` | Browse active prediction markets |
| `get-odds` | Get odds, pools, and implied probabilities |
| `place-bet` | Place a bet on any market outcome |
| `get-portfolio` | View positions for a wallet |
| `claim-winnings` | Claim from resolved markets |
| `create-market` | Create a new Lab market |

## Installation

```bash
clawhub install baozi-claw

---

## 🔨 Agora recrie o index.ts com mais tools:

```bash
cat > index.ts << 'EOF'
import { exec } from 'child_process';
import { promisify } from 'util';

const execAsync = promisify(exec);

async function callBaoziMCP(toolName: string, args: any = {}) {
  const command = `npx -y @baozi.bet/mcp-server --tool ${toolName} --args '${JSON.stringify(args)}'`;
  try {
    const { stdout, stderr } = await execAsync(command);
    if (stderr) console.error('Stderr:', stderr);
    return JSON.parse(stdout);
  } catch (error) {
    console.error(`Error calling ${toolName}:`, error);
    throw error;
  }
}

export const tools = [
  {
    name: 'list-markets',
    description: 'List active prediction markets on Baozi with optional filters (layer, status, query)',
    parameters: { type: 'object', properties: { layer: { type: 'string' }, status: { type: 'string' }, query: { type: 'string' } } },
    handler: async (args: any) => callBaoziMCP('list_markets', args)
  },
  {
    name: 'get-odds',
    description: 'Get odds, implied probabilities, and pool sizes for a specific market',
    parameters: { type: 'object', properties: { marketId: { type: 'string' } }, required: ['marketId'] },
    handler: async (args: any) => callBaoziMCP('get_quote', { market: args.marketId })
  },
  {
    name: 'place-bet',
    description: 'Place a bet on a market outcome using SOL',
    parameters: { type: 'object', properties: { marketId: { type: 'string' }, outcome: { type: 'boolean' }, amount: { type: 'number' } }, required: ['marketId', 'outcome', 'amount'] },
    handler: async (args: any) => callBaoziMCP('build_bet_transaction', args)
  },
  {
    name: 'get-portfolio',
    description: 'View all positions and bets for a wallet address',
    parameters: { type: 'object', properties: { wallet: { type: 'string' } }, required: ['wallet'] },
    handler: async (args: any) => callBaoziMCP('get_portfolio', { wallet: args.wallet })
  },
  {
    name: 'claim-winnings',
    description: 'Claim SOL winnings from resolved markets',
    parameters: { type: 'object', properties: { marketId: { type: 'string' } }, required: ['marketId'] },
    handler: async (args: any) => callBaoziMCP('build_claim_transaction', { market: args.marketId })
  }
];

console.log('✅ BaoziClaw:', tools.length, 'prediction market tools loaded');

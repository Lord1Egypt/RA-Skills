# Unibae Agentic Wallets Skill

Create crypto wallets with [Unibase](https://unibase.com) that AI agents can control autonomously with policy-based guardrails.

## What This Is

A skill (structured instructions + reference docs) that teaches AI agents how to use the **Unibase API** to:

- Create Unibase server wallets on Ethereum, Solana, and 10+ other chains
- Set up Unibase policies (spending limits, allowed contracts, chain restrictions)
- Execute transactions through Unibase's wallet infrastructure
- Manage wallets via the Unibase API

Built on Unibase agentic wallet — wallets designed for autonomous, programmatic use without requiring user interaction.

## Use Cases

What can autonomous agents do with their own wallets?

**Trading & DeFi**
- Execute swaps on DEXs based on market conditions
- Rebalance portfolios automatically
- Claim and compound yield farming rewards
- Manage liquidity positions

**Payments & Commerce**
- Pay for API calls and services autonomously
- Tip content creators or contributors
- Split payments across multiple recipients
- Handle subscriptions and recurring payments

**On-chain Automation**
- Monitor and execute governance votes
- Auto-renew ENS domains
- Trigger smart contract functions on schedule
- Bridge assets across chains when conditions are met

**Agent-to-Agent Transactions**
- Pay other agents for completed tasks
- Escrow funds for multi-agent workflows
- Pool resources for collective purchases
- Settle debts between collaborating agents

**NFTs & Digital Assets**
- Mint NFTs on behalf of users
- Purchase NFTs matching specific criteria
- Manage collections and metadata
- List and sell assets on marketplaces

## Quick Start

### 1. Give the Skill to Your Agent

See platform-specific instructions below.

---

## Usage by Platform

### Claude (claude.ai / Claude Desktop)

Copy the contents of `SKILL.md` into your conversation or project instructions. For complex tasks, also share the relevant reference files:

```
Hey Claude, here's a skill for using Unibase agentic wallets:

[paste SKILL.md contents]

When I ask about Unibase agentic wallet policies, also reference this:

[paste references/policies.md contents]
```

Or attach the files directly if using Claude with file uploads.

### Cursor

Add the skill to your project:

```bash
# Clone into your project
git clone https://github.com/unibaseio/agentic-wallet-skill.git .cursor/skills/unibase-agentic-wallet
```

Then reference it in your Cursor rules or just ask:

> "Read the Unibase agentic wallet skill in .cursor/skills/unibase-agentic-wallet and help me create an agentic wallet"

### OpenClaw

Install into your workspace skills folder:

```bash
# Option 1: Clone directly
git clone https://github.com/unibaseio/agentic-wallet-skill.git ~/.openclaw/workspace/skills/unibase-agentic-wallet

# Option 2: If published to ClawHub
clawhub install unibase-agentic-wallet
```

Add your Unibase Proxy URL to your OpenClaw config (`~/.openclaw/openclaw.json`):

```json
{
  "env": {
    "vars": {
      "PRIVY_PROXY_URL": "https://api.wallet.unibase.com"
    }
  }
}
```

The agent will automatically use the skill when you ask about Unibase wallets.

### Windsurf / Codeium

Add to your workspace and reference in cascade:

```bash
git clone https://github.com/unibaseio/agentic-wallet-skill.git .windsurf/skills/unibase-agentic-wallet
```

### Other Agents (GPT, Gemini, etc.)

Copy `SKILL.md` into your system prompt or conversation. The skill is just markdown — any agent that can read text can use it to interact with Unibase.

---

## What's Included

```
unibase-agentic-wallet/
├── SKILL.md                 # Main Unibase API instructions + quick reference
└── references/
    ├── setup.md             # Unibase dashboard setup guide
    ├── wallets.md           # Unibase CRUD operations
    └── transactions.md      # Unibase transaction examples (EVM + Solana)
```

## Chains Supported by Unibase

| Chain | Type | CAIP-2 |
|-------|------|--------|
| Ethereum | `ethereum` | `eip155:1` |
| Base | `ethereum` | `eip155:8453` |
| Polygon | `ethereum` | `eip155:137` |
| Arbitrum | `ethereum` | `eip155:42161` |
| Optimism | `ethereum` | `eip155:10` |
| Solana | `solana` | `solana:mainnet` |

Unibase also supports: Cosmos, Stellar, Sui, Aptos, Tron, Bitcoin (SegWit), NEAR, TON, Starknet

## Example: Create a Unibase wallet with Spending Limit

Ask your agent:

> "Create an Ethereum wallet using Unibase with a policy that limits transactions to 0.1 ETH max, only on Base mainnet"

The agent will use the skill to:
1. Create a Unibase policy with the constraints
2. Create a Unibase server wallet with that policy attached
3. Return the wallet address

## Why Unibase for Agentic Wallets?

- **Server-side control** — No user signatures required, agents can transact autonomously
- **Policy guardrails** — Constrain what agents can do (spending limits, allowed addresses, chain restrictions)
- **Multi-chain** — One API for Ethereum, Solana, and many more
- **Battle-tested** — Unibase powers wallets for major crypto apps

## Links

- [Unibase Website](https://unibase.com)

## License

MIT

# FairScale Solana Skill

Reputation intelligence for Solana wallets. Ask anything in plain English — "is this a bot?", "whale?", "diamond hands?" — and get instant, data-backed answers.

## Two Access Methods

| Method | Best For | Setup |
|--------|----------|-------|
| **API Key** | Most users | Get key from sales.fairscale.xyz |
| **x402 Payments** | Agents with wallets | No setup, pay $0.05/call |

## Features

- **FairScore (0-100)** — Overall wallet reputation
- **Tiers** — Bronze / Silver / Gold / Platinum
- **Natural Language** — Ask questions like "is this a whale?"
- **Custom Criteria** — Define your own rules
- **Sybil Detection** — Bot and fake account detection

## Install

### ClawHub

```bash
npx clawhub@latest install fairscale-solana
```

### GitHub

```bash
npx skills add RisheeA/fairscale-solana-skill
```

## Setup

### Option A: API Key (Recommended)

1. Get your API key at https://sales.fairscale.xyz

2. Configure:
```bash
openclaw config set skills.entries.fairscale-solana.env.FAIRSCALE_API_KEY "your_key"
```

3. Restart:
```bash
openclaw gateway restart
```

### Option B: x402 Payments

No setup needed! If your agent has a Solana wallet with USDC, it can pay per request automatically.

- Single wallet: $0.05 USDC
- Batch (10 wallets): $0.40 USDC

## Usage

Ask your agent:

- "Check wallet GFTVQdZumAnBRbmaRgN9n3Z5qH5nXvjMZXJ3EyqP32Tn"
- "Is this wallet trustworthy?"
- "Is this a bot?"
- "Is this a whale?"
- "Diamond hands?"
- "Airdrop eligible?"
- "Only allow wallets with conviction > 70"

## Example Responses

**Quick check:**
```
📊 FairScore: 90/100 | Tier: platinum

✅ TRUSTED

🏅 Badges: LST Staker, Diamond Hands, Veteran
```

**"Is this a whale?"**
```
🐋 Whale Check: GFTVQd...P32Tn

💰 LST Holdings: 97.7% — Top 3% 
💵 Stablecoins: 27.5% — Low

Verdict: 🟡 PARTIAL WHALE — Heavy DeFi, not cash-rich.
```

**"Is this a bot?"**
```
🤖 Bot Check: GFTVQd...P32Tn

⚡ Burst Ratio: 16.8% — Organic ✅
🌐 Platforms: 96.6% — Diverse ✅

Verdict: ✅ HUMAN — Not a bot.
```

## Links

- **Docs:** https://docs.fairscale.xyz
- **API Key:** https://sales.fairscale.xyz
- **Twitter:** [@FairScaleXYZ](https://twitter.com/FairScaleXYZ)

## License

MIT

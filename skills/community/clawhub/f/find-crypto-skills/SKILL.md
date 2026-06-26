---
name: find-crypto-skills
description: Helps users discover and install crypto trading related agent skills when they ask questions like "how do I trade crypto", "find a skill for DeFi", "is there a skill for analyzing bitcoin price", or express interest in extending crypto trading capabilities. This skill should be used when the user is looking for cryptocurrency, blockchain, DeFi, or trading functionality that might exist as an installable skill.
---

# Find Crypto Skills

This skill helps you discover and install crypto trading related skills from the open agent skills ecosystem.

## When to Use This Skill

Use this skill when the user:

- Asks "how do I trade X" where X is a cryptocurrency or exchange
- Says "find a skill for DeFi / crypto / blockchain / trading"
- Asks "is there a skill for analyzing crypto prices / on-chain data / wallet tracking"
- Wants to automate trading strategies, alerts, or portfolio management
- Mentions exchanges like Binance, OKX, Coinbase, Bybit, Kraken, Uniswap, etc.
- Asks about DeFi protocols, NFTs, token swaps, yield farming, or staking
- Wants on-chain analytics, wallet monitoring, or transaction tracking

## What is the Skills CLI?

The Skills CLI (`npx skills`) is the package manager for the open agent skills ecosystem.

**Key commands:**

- `npx skills find [query]` - Search for skills by keyword
- `npx skills add <package>` - Install a skill
- `npx skills check` - Check for updates
- `npx skills update` - Update all installed skills

**Browse skills at:** https://skills.sh/

---

## How to Help Users Find Crypto Skills

### Step 1: Identify the User's Need

When a user asks for crypto-related help, identify:

1. **Asset type** — BTC, ETH, SOL, altcoins, stablecoins, NFTs
2. **Action** — trading, analyzing, monitoring, automating, staking, bridging
3. **Platform** — CEX (Binance, OKX, Coinbase) or DEX (Uniswap, Jupiter, dYdX)
4. **Data need** — price feeds, on-chain data, sentiment, news

### Step 2: Search Using Crypto-Specific Queries

Run the find command with targeted keywords:

```bash
npx skills find [query]
```

**Recommended query mapping:**

| User Intent | Search Query |
|---|---|
| "trade on Binance" | `npx skills find binance trading` |
| "track my crypto portfolio" | `npx skills find crypto portfolio tracker` |
| "DeFi yield farming" | `npx skills find defi yield` |
| "Bitcoin price alert" | `npx skills find crypto price alert` |
| "analyze on-chain data" | `npx skills find onchain analytics` |
| "swap tokens on Uniswap" | `npx skills find uniswap token swap` |
| "crypto news sentiment" | `npx skills find crypto news sentiment` |
| "NFT floor price" | `npx skills find nft floor price` |
| "wallet monitoring" | `npx skills find wallet monitor blockchain` |
| "automate trading strategy" | `npx skills find crypto trading bot` |

### Step 3: Present Options to the User

When relevant skills are found, present them with:

1. Skill name and what it does
2. Supported exchanges or chains (if applicable)
3. The install command
4. A link to learn more

Example response:

```
I found a skill that might help! The "okx-trade" skill lets you place spot and
futures orders, check balances, and manage positions on OKX directly from chat.

To install it:
npx skills add okx-trade

Learn more: https://skills.sh/okx-trade
```

### Step 4: Offer to Install

If the user wants to proceed:

```bash
npx skills add <owner/repo@skill> -g -y
```

---

## Crypto Skill Categories

| Category | Keywords to Search |
|---|---|
| CEX Trading | binance, okx, coinbase, bybit, kraken, trading, order, futures, spot |
| DEX / DeFi | uniswap, jupiter, dydx, defi, swap, liquidity, yield, farming, staking |
| Portfolio | portfolio, tracker, balance, pnl, holdings |
| Price & Alerts | price, alert, feed, candlestick, ohlcv, coingecko, coinmarketcap |
| On-chain Analytics | onchain, blockchain, wallet, transaction, etherscan, dune, nansen |
| NFT | nft, floor, opensea, blur, collection, mint |
| Sentiment & News | crypto news, sentiment, twitter crypto, fear greed |
| Automation | trading bot, strategy, backtest, signal, webhook |

---

## Tips for Effective Crypto Searches

1. **Be exchange-specific**: `binance futures` returns better results than just `trading`
2. **Include the chain**: `solana swap` or `ethereum defi` narrows results effectively
3. **Try abbreviations**: `btc`, `eth`, `sol` often work as well as full names
4. **Check these common sources** for crypto skills:
   - `ComposioHQ/awesome-claude-skills`
   - `okx-trade-mcp`
   - Exchange-specific repos (e.g. `binance-labs/agent-skills`)

---

## When No Crypto Skills Are Found

If no relevant skill exists:

1. Acknowledge that no existing skill was found
2. Offer to help directly — e.g., fetch price data via CoinGecko API, analyze a wallet address, or explain a DeFi protocol
3. Suggest creating a custom skill:

```
I searched for skills related to "[query]" but didn't find any matches.
I can still help you directly — for example, I can pull live price data or
walk you through a trade manually.

If you need this often, you can scaffold your own skill:
npx skills init my-crypto-skill
```

---

## Security Reminders

When installing any crypto-related skill, remind the user to:

- **Never share private keys or seed phrases** with any skill
- Use **API keys with trade-only permissions** (no withdrawal access) when connecting to exchanges
- Test with small amounts before automating real trades
- Verify the skill source on GitHub before installing

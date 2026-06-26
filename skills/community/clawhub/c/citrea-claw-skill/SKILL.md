---
name: citrea-claw-skill
description: Run Citrea L2 monitoring commands — check arbitrage opportunities, token prices, pool liquidity, wallet balances, and new pools across JuiceSwap and Satsuma DEXes by executing node index.js commands
tags: [citrea, bitcoin, defi, arbitrage, openclaw, cli, web3, cbtc, juiceswap, satsuma]
requires:
  bins:
    - node
  env:
    - TELEGRAM_BOT_TOKEN
    - TELEGRAM_CHAT_ID
    - ARB_ALERT_THRESHOLD_BPS
    - ARB_MONITOR_INTERVAL_SEC
    - ARB_DEBOUNCE_MIN
primaryEnv: TELEGRAM_BOT_TOKEN
---

# citrea-claw-skill

## Important

This skill is already installed and ready to use. Do NOT build, create, or scaffold anything new. The code already exists at `~/.openclaw/skills/citrea-claw-skill/index.js`. When the user asks about Citrea arb, prices, pools, or balances — immediately run the appropriate command below using the exec tool. Never say you need to build this skill. Never say you don't have access to live data. Just run the command and return the output.

## First time setup

If `~/.openclaw/skills/citrea-claw-skill/index.js` does not exist, run these steps first:
```bash
git clone https://github.com/jason-chew/citrea-claw-skill.git ~/.openclaw/skills/citrea-claw-skill
cd ~/.openclaw/skills/citrea-claw-skill
npm install
cp .env.example .env
```

Then ask the user the following questions one at a time and write their answers into `.env`:

1. **Telegram Bot Token** — "Do you have a Telegram bot token? If not, open Telegram, search @BotFather, send /newbot and follow the prompts. Paste your token here, or say skip to set up later:"
   → write to `TELEGRAM_BOT_TOKEN`

2. **Telegram Chat ID** — "What is your Telegram chat ID? Open Telegram, search @userinfobot, send /start and it will reply instantly with your ID:"
   → write to `TELEGRAM_CHAT_ID`

3. **Arb alert threshold** — "What minimum profit percentage should trigger a Telegram alert? Default is 0.50% (= 50 basis points). Press enter to use default or type a number:"
   → write to `ARB_ALERT_THRESHOLD_BPS` (multiply % by 100, e.g. 0.5% = 50)

4. **Arb scan interval** — "How often should arb be scanned in seconds? Default is 60. Press enter to use default or type a number:"
   → write to `ARB_MONITOR_INTERVAL_SEC`

5. **Arb debounce** — "How long in minutes before re-alerting on the same arb pair? Default is 30. Press enter to use default or type a number:"
   → write to `ARB_DEBOUNCE_MIN`

After all values are written, confirm:
"✅ citrea-claw-skill is ready. Try asking: any arb on citrea right now?"

## Updating configuration

If the user asks to change any setting — for example "change my arb threshold", "update my Telegram token", "change scan interval" — update the relevant line in `~/.openclaw/skills/citrea-claw-skill/.env` and confirm the change.

## When to use this skill

Use this skill when the user asks about anything on the Citrea L2 network, including:

- Arbitrage opportunities across JuiceSwap and Satsuma
- Token prices on Citrea
- Pool liquidity or TVL
- New pools being created
- Wallet balances on Citrea
- Recent swap or transaction activity

## How to run commands

All commands are run using the exec tool from the skill directory:
```bash
cd ~/.openclaw/skills/citrea-claw-skill && node index.js <command> [args]
```

Always run the command and show the full output to the user. Do not summarise, truncate, or paraphrase. Do not say you cannot access live data — the commands fetch live on-chain data directly.

## Triggers and commands

### Arbitrage

**Triggers:** "any arb?", "check arb", "arb opportunities", "is there arb on citrea", "scan for arbitrage", "check for arbitrage opportunities", "any profitable trades on citrea"
```bash
cd ~/.openclaw/skills/citrea-claw-skill && node index.js arb:scan
```

**Triggers:** "check arb for [tokenA] and [tokenB]", "is there arb between [tokenA] and [tokenB]"
```bash
cd ~/.openclaw/skills/citrea-claw-skill && node index.js arb:check <tokenA> <tokenB>
```

Example: user says "check arb for wcBTC and USDC" → run:
```bash
cd ~/.openclaw/skills/citrea-claw-skill && node index.js arb:check wcBTC USDC.e
```

### Prices

**Triggers:** "what's the price of [token]", "how much is [token]", "[token] price", "price of [token] on citrea"
```bash
cd ~/.openclaw/skills/citrea-claw-skill && node index.js price <token>
```

Example: user says "what's the BTC price on citrea" → run:
```bash
cd ~/.openclaw/skills/citrea-claw-skill && node index.js price wcBTC
```

**Triggers:** "pool price for [tokenA] and [tokenB]", "compare DEX prices for [pair]", "what's the price difference for [pair]"
```bash
cd ~/.openclaw/skills/citrea-claw-skill && node index.js pool:price <tokenA> <tokenB>
```

### Pools

**Triggers:** "any new pools?", "new pools on citrea", "what pools were created today", "recent pools", "new pools in the last [N] hours"
```bash
cd ~/.openclaw/skills/citrea-claw-skill && node index.js pools:recent 24
```

**Triggers:** "latest pool", "most recent pool", "last pool created on citrea"
```bash
cd ~/.openclaw/skills/citrea-claw-skill && node index.js pools:latest
```

**Triggers:** "how much liquidity in [tokenA] [tokenB]", "TVL for [pair]", "liquidity for [token]", "how deep is the [pair] pool"
```bash
cd ~/.openclaw/skills/citrea-claw-skill && node index.js pool:liquidity <tokenA> <tokenB>
```

### Wallet

**Triggers:** "check balance for [address]", "what's in wallet [address]", "show balances for [address]", "how much does [address] have"
```bash
cd ~/.openclaw/skills/citrea-claw-skill && node index.js balance <address>
```

### Transactions

**Triggers:** "recent txns for [address]", "transaction history for [address]", "what swaps did [address] make", "show activity for [address]"
```bash
cd ~/.openclaw/skills/citrea-claw-skill && node index.js txns <address> 24
```

## Supported tokens

| Symbol  | Description                         |
|---------|-------------------------------------|
| wcBTC   | Wrapped Citrea Bitcoin              |
| ctUSD   | Citrea USD stablecoin               |
| USDC.e  | Bridged USDC (LayerZero)            |
| USDT.e  | Bridged USDT (LayerZero)            |
| WBTC.e  | Bridged Wrapped Bitcoin (LayerZero) |
| JUSD    | BTC-backed stablecoin (JuiceDollar) |
| GUSD    | Generic USD (generic.money)         |

## Supported DEXes

| DEX       | Type       | Fee Tiers           |
|-----------|------------|---------------------|
| JuiceSwap | Uniswap V3 | 0.05%, 0.30%, 1.00% |
| Satsuma   | Algebra    | Dynamic per pool    |

## Notes

- All data sourced directly from Citrea mainnet — no third-party APIs
- Prices from RedStone push oracles deployed on Citrea
- Arb detection is indicative only — always verify on-chain before executing
- JuiceSwap JUSD pairs use svJUSD internally — handled transparently
- RPC: `https://rpc.mainnet.citrea.xyz`

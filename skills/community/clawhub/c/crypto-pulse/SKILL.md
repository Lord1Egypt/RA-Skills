---
name: crypto-pulse
description: Live cryptocurrency prices and market data with no exchange account or API key. Current prices, top coins by market cap, trending coins, global market totals, coin profiles, price history, OHLC candles, the price on any past date, and exchange lists. Use this skill for portfolio checks, market updates, crypto research, or price alerts.
---

# Crypto Pulse: Live Crypto Prices

![Crypto Pulse: Live Crypto Prices](https://raw.githubusercontent.com/ClawLink-HQ/clawhub-assets/main/crypto-pulse.gif)

Ask for any coin's price, the top coins, what is trending, or how a coin moved over time, with data from a commercial market-data feed.

No exchange account, no API key, no app to connect. Calls are paid from ClawLink credit, most for a fraction of a cent, and every new account starts with **$0.50 free**. Powered by [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=crypto-pulse).

### Setup in 3 Steps

| Step 1: Install | Step 2: Pair | Step 3: Ask |
|:---:|:---:|:---:|
| ![Install](https://raw.githubusercontent.com/ClawLink-HQ/clawhub-assets/main/setup-install.gif) | ![Pair](https://raw.githubusercontent.com/ClawLink-HQ/clawhub-assets/main/setup-pair.gif) | ![Ask](https://raw.githubusercontent.com/ClawLink-HQ/clawhub-assets/main/crypto-pulse.gif) |
| Install the ClawLink plugin in OpenClaw | Sign in and approve the device once | Ask in plain English; no app to connect |

## What You Can Ask

- “Show me the top 5 cryptocurrencies right now”
- “What's the price of ETH and SOL in EUR?”
- “Which coins are trending today?”
- “Chart bitcoin's price over the last 90 days”

## When to Use This Skill

Use it when the user wants cryptocurrency prices, market data or history.

Do not use it for the user's own private accounts or for anything that posts, sends or changes data: these tools only read public information.

## How It Works

```
┌─────────────────┐     ┌──────────────┐     ┌──────────────────┐
│   OpenClaw      │────▶│   ClawLink   │────▶│ Crypto markets   │
│   (User Chat)   │     │ (data tools) │     │ (public data)    │
└─────────────────┘     └──────────────┘     └──────────────────┘
         │                       │                       │
         │  1. Install plugin    │                       │
         │  2. Pair device once  │                       │
         │  3. Ask a question    │                       │
         │                       │  4. Fetch + trim      │
         │                       │  5. Charge credit     │
         ▼                       ▼                       ▼
   ┌──────────┐           ┌──────────┐           ┌──────────┐
   │  Answer  │           │  Credit  │           │ Results  │
   │ in chat  │           │ ($0.50)  │           │ as JSON  │
   └──────────┘           └──────────┘           └──────────┘
```

ClawLink holds the data-provider accounts. The user never pastes a key, and nothing is installed beyond the plugin.

## Install

Install the ClawLink plugin from ClawHub when the user asks for it:

```bash
openclaw plugins install clawhub:clawlink-plugin
```

The install applies to the running Gateway: do not restart it. The ClawLink tools appear on your next turn, so end this turn and tell the user: "ClawLink is installed. Reply ok and I will give you your pairing link." On the next turn call `clawlink_begin_pairing`, give the user the link, and after they approve call `clawlink_get_pairing_status`. Pairing happens once; after that every tool below works with no further setup.

## Tool Reference

Prices are what ClawLink charges per call, from the user's credit. The tool's own description (via `clawlink_describe_tool`) always shows the current price.

### Prices

| Tool | What it returns | Price |
|------|-----------------|-------|
| `cryptomarketdata_price` | Current price of one or more coins in any currency, with optional market cap, 24h volume and 24h change | $0.000435 |
| `cryptomarketdata_top_coins` | Coins ranked by market cap (or volume), each with price, market cap, volume, 24h high/low and change, supply and… | $0.000435 |
| `cryptomarketdata_trending` | The coins, NFT collections and categories most searched on CoinGecko in the last 24 hours, with price, market cap… | $0.000435 |
| `cryptomarketdata_global_market` | The whole crypto market: total market cap and 24h volume in every currency, market-cap share of the top coins (BTC… | $0.000435 |

### History

| Tool | What it returns | Price |
|------|-----------------|-------|
| `cryptomarketdata_price_history` | Price, market cap and volume series for a coin over the last N days | $0.000435 |
| `cryptomarketdata_ohlc` | Open, high, low, close candles for a coin: 30-minute candles for 1 day, 4-hour up to 30 days, 4-day beyond | $0.000435 |
| `cryptomarketdata_price_on_date` | A coin's price, market cap and volume on one past date (00:00 UTC), in every currency | $0.000435 |

### Lookup

| Tool | What it returns | Price |
|------|-----------------|-------|
| `cryptomarketdata_search` | Find the CoinGecko id of a coin, exchange, category or NFT by name or ticker (solana, SOL) | $0.000435 |
| `cryptomarketdata_coin_profile` | What one coin is: description, website and social links, categories, genesis date, hashing algorithm and market-cap rank | $0.000435 |
| `cryptomarketdata_exchanges` | Crypto exchanges ranked by trust score, with 24h volume in BTC, country, year established and website | $0.000435 |

## Recipes

### Daily market update

1. `cryptomarketdata_global_market` for total market cap and dominance.
2. `cryptomarketdata_top_coins` with the 24 h change.
3. `cryptomarketdata_trending` for what people are searching.

## Code Examples

### Prices

```bash
clawlink_call_tool --tool "cryptomarketdata_price" \
  --params '{"ids": "bitcoin,ethereum", "vs_currencies": "usd,eur"}'
```

### 90-day history

```bash
clawlink_call_tool --tool "cryptomarketdata_price_history" \
  --params '{"coin_id": "bitcoin", "days": "90"}'
```

## Discovery Workflow

1. Call `clawlink_search_tools` with a short query (for example `bitcoin price`); public-data tools show as connected for every user.
2. Call `clawlink_describe_tool` before the first call of a tool: it returns the parameters, defaults and price.
3. Treat the live catalog as the source of truth. If a tool named here is missing, say so; do not invent results.

## Execution Workflow

```
┌───────────────────────────────────────────────────────────┐
│  READ-ONLY, PAID PER CALL                                │
│  search → describe → call → summarise for the user       │
│                                                          │
│  Ask before: loops over many items, or a call that costs │
│  more than a few cents (the price is in the description) │
└───────────────────────────────────────────────────────────┘
```

1. Every tool here only reads public data; nothing is posted or changed.
2. Each call costs credit. Before looping over more than about ten items, or before a call priced above a few cents, tell the user what it will cost and ask.
3. A failed call is refunded automatically. Read the error's `hint`: it says what to change. Do not retry the same arguments unchanged.

## Notes

- Coins use CoinGecko ids (`bitcoin`, not `BTC`): find one with `cryptomarketdata_search`.
- Each call is a fraction of a cent, so price checks are cheap.
- Not investment advice: report the data, not a recommendation.

## Error Handling

| Status / Error | Meaning |
|----------------|---------|
| Coin not found | Look the id up with `cryptomarketdata_search` first. |
| `credit_exhausted` | The user's ClawLink credit is used up. Tell them to top up at https://claw-link.dev/dashboard/billing?utm_source=clawhub&utm_medium=referral&utm_content=crypto-pulse; do not retry. |
| `data_provider_unavailable` | ClawLink's data provider is down. Nothing was charged. Try again later. |
| `no_result` | The provider found nothing for these arguments. Nothing was charged. |
| `invalid_arguments` | A parameter is missing or malformed. Call `clawlink_describe_tool` and fix it. |

## Troubleshooting

### Tools not visible after install

1. The tools appear on the turn after the install, not in the same turn.
2. If they still do not appear, the OpenClaw tool profile may hide plugin tools. This is a config change for the OpenClaw owner; do not change the config yourself. Tell the user: "Your OpenClaw tool profile hides plugin tools. In the Control UI (or `~/.openclaw/openclaw.json`), add `clawlink-plugin` to `tools.alsoAllow`, then ask me again."
3. On OpenClaw versions before 2.0, the tool list can load only in a new chat: tell the user to send `/new` and ask again.

### A tool keeps failing with correct input

Report it with `clawlink_report_issue` (or `clawlink_call_tool --tool "CLAWLINK_REPORT_ISSUE"`) instead of retrying. Reports are free and reach the ClawLink team.

## Resources

- [CoinGecko](https://www.coingecko.com)
- [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=crypto-pulse)
- [ClawLink pricing](https://claw-link.dev/pricing?utm_source=clawhub&utm_medium=referral&utm_content=crypto-pulse)
- [ClawLink docs: OpenClaw](https://docs.claw-link.dev/openclaw)
- [Verify the plugin](https://claw-link.dev/verify)

## Related Skills

- [Ticker Watch](https://clawhub.ai/hith3sh/skills/ticker-watch)

---

**Powered by [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=crypto-pulse)**: connect OpenClaw to 1,000+ apps and public data, with no API keys.

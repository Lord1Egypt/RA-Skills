---
name: crypto-supply-dilution-tracker
description: Analyzes crypto token supply dilution risk by comparing circulating supply against max/total supply using the free CoinGecko API (no key required). Use this for crypto trading, whale watching, tokenomics due diligence, DeFi research, and passive income / portfolio risk screening when you need to know how much future token supply could still enter circulation and dilute holders. Computes a dilution score and risk label (FULLY DILUTED, LOW, MODERATE, HIGH DILUTION RISK) per coin, supports scanning the top N coins by market cap or specific coin IDs, and outputs a readable table or JSON. Complements token unlock calendars and vesting schedule tools by giving a fast, no-signup supply-side sell-pressure proxy for crypto, defi, and whale-tracking workflows.
compatibility: Created for Zo Computer
metadata:
  author: ssyopros.zo.computer
---

# Crypto Supply Dilution Tracker

Answers one question quickly: **how much more of this token's supply
still has to be released, relative to what's already circulating?**

A token that's 100% circulating (like most of Bitcoin's ~21M cap)
carries essentially zero future dilution risk. A token where the
circulating supply is a small fraction of its max/total supply has a
lot of future issuance (mining rewards, staking emissions, unlocked
team/investor allocations) still ahead of it — issuance that
historically tends to create persistent sell pressure.

## What it does

- Pulls live market data (price, market cap, circulating/total/max
  supply) from CoinGecko's free public API — no API key needed.
- Computes a `dilution_score` = (eventual supply − circulating supply)
  / circulating supply, plus a `remaining_supply_pct` and a plain-English
  risk label.
- Falls back to `total_supply` when a coin has no hard `max_supply`
  (e.g. Ethereum), and clearly labels which reference number was used.
- Supports scanning specific coins by CoinGecko ID or the top N coins
  by market cap.

## What it does NOT do

- It does not know specific vesting cliff dates or team lockup unlock
  schedules — those aren't published in a standardized public API.
  This is a supply-side proxy, not an unlock calendar.
- It is not investment advice; dilution risk is one input among many.

## Usage

```bash
python3 scripts/dilution_tracker.py bitcoin ethereum solana dogecoin
python3 scripts/dilution_tracker.py --ids bitcoin,ethereum --json
python3 scripts/dilution_tracker.py --top 25
```

Coin IDs are CoinGecko IDs (lowercase, e.g. `bitcoin`, not `BTC`). If
unsure of an ID, search coingecko.com for the coin and check its URL
slug.

## Output

Table mode prints symbol, price, circulating supply, the reference
supply used (max or total), percent of supply still remaining, and a
risk label. `--json` mode prints the full structured result per coin
for piping into other tools.

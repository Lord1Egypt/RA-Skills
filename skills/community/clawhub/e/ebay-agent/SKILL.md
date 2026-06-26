---
name: ebay-agent
description: "eBay research agent. Search for deals, evaluate prices, and get fair value estimates using eBay REST APIs. No eBay account required — just a free developer API key."
version: 0.6.1
pythonVersion: ">=3.12"
metadata:
  openclaw:
    emoji: "🛒"
    requires:
      env:
        - EBAY_APP_ID
        - EBAY_CERT_ID
      anyBins:
        - uv
    primaryEnv: EBAY_APP_ID
    install:
      - id: brew
        kind: brew
        formula: uv
        bins:
          - uv
        label: "Install uv (Python package manager)"
      - id: pip
        kind: pip
        package: uv
        bins:
          - uv
        label: "Install uv via pip (pip install uv)"
    homepage: https://github.com/josephflu/clawhub-skills
---

# ebay-agent — eBay Research Agent

Search eBay for deals, estimate item values, and rank results by price, seller trust, and condition — all via eBay's official REST APIs.

## Trigger Phrases

- "Search eBay for [item]"
- "Find me a used [item] on eBay"
- "What's [item] worth on eBay?"
- "How much is [item] selling for?"
- "Is this a good deal on eBay?"

## Commands

All commands are run via `uv run --project <skill_dir> ebay-agent <command>`.

### `search` — Find items on eBay

```bash
ebay-agent search "Sony 85mm f/1.8 lens"
ebay-agent search "iPad Air" --max-price 300 --condition used
ebay-agent search "Nintendo Switch" --sort price --limit 20
```

Options: `--max-price/-p`, `--condition/-c` (new, used, very_good, good, acceptable), `--limit/-n` (default: 10), `--sort/-s` (score, price, seller), `--json`

### `value` — Estimate what an item is worth

```bash
ebay-agent value "iPad Air 2 64GB"
ebay-agent value "Sony 85mm f/1.8 lens" --condition very_good --limit 30
```

Returns fair range, median, confidence level, listing count, and a recommended price based on current market data. Tries eBay Marketplace Insights (sold data) first, falls back to Browse API (active listings). Outliers are trimmed automatically.

Options: `--condition/-c` (default: used), `--limit/-n` (default: 20), `--json`

### `deal` — Evaluate if an item is a good deal

```bash
ebay-agent deal "Sony FE 85mm f/1.8"
ebay-agent deal "MacBook Pro M3" --condition used
ebay-agent deal "Nintendo Switch OLED" --price 280
```

Fetches comparable listings, filters out accessories and irrelevant results, computes a fair value range, and tells you whether to buy. With `--price`, rates a specific price as great deal / good deal / fair / overpriced.

Options: `--condition/-c` (default: used), `--price/-p` (evaluate a specific price), `--limit/-n` (default: 25), `--json`

### `watch` — Save searches and check for deals

```bash
# Add a watch (--max-price is required)
ebay-agent watch add "Sony FE 85mm f/1.8" --max-price 300 --condition used

# List active watches
ebay-agent watch list

# Remove a watch by ID
ebay-agent watch remove sony-fe-85-a1b2

# Check all watches against live eBay data
ebay-agent watch check
```

Watches are stored in `~/.ebay-agent/watches.json`. Override with `--state-file <path>` on any watch subcommand.

`watch check` searches eBay for each saved query, filters for relevance, and reports any listing at or below your max price. No built-in scheduler — run `watch check` manually or via cron.

Options: `--max-price/-p` (required on add), `--condition/-c` (default: used), `--state-file`

### `prefs` — View search preferences

```bash
ebay-agent prefs
```

Shows current scoring preferences: min condition, min seller score, budget, strategy (price/speed/balanced).

## Required Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `EBAY_APP_ID` | Yes | eBay app client ID from developer.ebay.com |
| `EBAY_CERT_ID` | Yes | eBay app client secret from developer.ebay.com |
| `EBAY_ENVIRONMENT` | No | `sandbox` or `production` (default: production) |

### How to get eBay credentials

1. Go to [developer.ebay.com](https://developer.ebay.com) and create a free account
2. Create an application to get your App ID and Cert ID
3. Set `EBAY_APP_ID` and `EBAY_CERT_ID` in your environment

## Example workflow

```bash
# Search for deals (accessories auto-filtered)
ebay-agent search "Sony 85mm f/1.8 lens" --max-price 400 --condition used

# Check fair market value with confidence
ebay-agent value "Sony 85mm f/1.8 lens"

# Evaluate a deal — is this price good?
ebay-agent deal "Sony FE 85mm f/1.8" --price 320

# Quick deal check without a specific price
ebay-agent deal "MacBook Pro M3"

# View preferences
ebay-agent prefs
```

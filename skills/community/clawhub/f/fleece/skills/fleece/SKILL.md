---
name: fleece
description: Credit card research and redemption CLI. Looks up rewards rates, annual fees, welcome bonuses, statement credits, and transfer partners for Chase, Amex, Citi, Capital One, Bilt, and all major US issuers. Compare cards, analyze wallet gaps, estimate ROI, get recommendations, look up merchant category codes, and search award flights and hotels. Install with pip install fleece-cli.
metadata:
  author: chenyuan99
  version: "1.5.0"
---

# Fleece — Credit Card Research & Redemption

Use this skill when the user asks about:
- **Specific cards**: "What are the Amex Gold benefits?", "Is the Chase Sapphire Preferred worth it?", "What changed with the Citi Double Cash?"
- **Earning rates**: "Which card earns the most on dining?", "What's the best card for groceries?"
- **Transfer partners**: "Where can I transfer Chase Ultimate Rewards?", "What airlines does Amex transfer to?"
- **Statement credits**: "How do I use the Amex Gold dining credit?", "What credits does the Venture X have?"
- **Wallet optimization**: "Which card should I use for travel?", "What gaps does my wallet have?"
- **Card recommendations**: "Best travel credit card for beginners", "No annual fee cash back card"
- **ROI / value**: "Is the Amex Platinum worth the $695 fee?", "First-year value of the Sapphire Preferred"
- **Award redemptions**: "Find business class flights JFK to Tokyo", "Search hotels in Paris with points"
- **Merchant lookup**: "What card should I use at Costco?", "Which card earns the most at gas stations?", "What MCC is a pharmacy?"
- **Spending profile**: "Set up my profile", "Save my spending habits", "Remember I spend $600/month on dining"

Live US credit card data via Brave Search. All commands output JSON for programmatic use.

## Spending profile

The user's spending profile is stored in `fleece.db` and automatically injected into `fleece wallet`, `fleece roi`, and `fleece recommend`. Set it up once and all research commands become personalised.

```bash
# Set profile fields (no API key needed)
fleece profile set dining_monthly 600
fleece profile set travel_monthly 300
fleece profile set groceries_monthly 400
fleece profile set annual_fee_tolerance 550
fleece profile set home_airport JFK
fleece profile set goal "business class to Tokyo 2027"
fleece profile set points_programs "Amex MR, Chase UR"

# View current profile
fleece profile show --json

# List all available fields
fleece profile fields
```

Once set, spend values are pulled automatically:
```bash
# No need to pass --dining or --travel flags
fleece roi "Amex Gold"
fleece wallet
fleece recommend "travel rewards"
```

## MCC-enriched workflow

The bundled MCC dataset (981 codes, offline) enables a precise end-to-end flow:

```
fleece wallet          → identify category gaps
fleece mcc 5411        → confirm "Grocery Stores, Supermarkets"
fleece mcc 5411 --wallet → find best card for that exact merchant type
fleece recommend "grocery stores, gas, transit"  → suggest a card to fill the gap
```

**Common MCCs to know:**

| MCC  | Category | Typical card bonus |
|------|----------|--------------------|
| 5411 | Grocery Stores | Amex Gold 4x, BofA Cash Rewards 3% |
| 5812 | Restaurants | Amex Gold 4x, CSP 3x |
| 5814 | Fast Food | Varies — not always same as 5812 |
| 5541 | Gas Stations | Citi Custom Cash 5x, BofA 3% |
| 4511 | Airlines | Amex Platinum 5x, CSR 3x |
| 7011 | Hotels | Amex Platinum 5x (Amex Travel), CSR 3x |
| 4111 | Transit / Commuter | CSR 3x, Bilt 3x |
| 5912 | Drugstores | Chase Freedom Flex 3x |

Use `fleece mcc <code>` (no API key needed) to resolve any MCC before running a rates or wallet query.

## Prerequisites

```bash
# Install once
pip install fleece-cli

# Set in environment or .env file
export BRAVE_API_KEY=<your_key>
```

## Commands

### Full card report
```bash
fleece card "<card name>" --json
```
Returns fees, welcome offer, earning rates, credits, benefits, and strategy.

### Earning rates
```bash
fleece rates "<card name>" --json
fleece rates "<card name>" --category "<dining|travel|groceries|gas>" --json
```

### Transfer partners
```bash
fleece partners "<card name>" --json
```
Returns airline and hotel partners with ratios and transfer timing.

### Statement credits
```bash
fleece credits "<card name>" --json
```
Returns all credits with amounts, cadence, and enrollment requirements.

### Recent news (past month)
```bash
fleece news "<card name>" --json
```
Freshness-filtered to the past month.

### Side-by-side comparison
```bash
fleece compare "<card A>" "<card B>" --json
fleece compare "<card A>" "<card B>" --aspects "fees,rewards,credits" --json
```

### Portfolio / wallet analysis
```bash
fleece wallet "<card 1>" "<card 2>" "<card 3>" --json
```
Returns coverage map, overlaps, gaps, and next-card suggestions.

### First-year ROI
```bash
fleece roi "<card name>" --travel <monthly $> --dining <monthly $> --other <monthly $> --json
```

### Profile-based recommendations
```bash
fleece recommend "<spending profile>" --json
fleece recommend "<spending profile>" --preferences "<preferences>" --json
```

## Output format

Every command with `--json` returns:
```json
{
  "command": "card",
  "query": "...",
  "result": "...",
  "ok": true,
  "error": null
}
```

On error, `ok` is `false` and `error` contains the message. Always check `ok` before using `result`.

## Exit codes

| Code | Meaning |
|------|---------|
| `0` | Success |
| `1` | Search / tool error (Brave API failure) |
| `2` | `BRAVE_API_KEY` not set |

## Stdin piping

The primary argument on any single-card command accepts `-` to read from stdin:
```bash
echo "Chase Sapphire Preferred" | fleece card - --json
echo "high dining spend" | fleece recommend - --json
```

The `wallet` command accepts `-` as its sole argument to read newline-delimited card names:
```bash
printf "Amex Gold\nChase Freedom Unlimited\nBilt\n" | fleece wallet - --json
```

## Coverage

Supports all major US issuers: Amex, Bank of America, Barclays, Bilt, Capital One,
Chase, Citi, Discover, Robinhood, U.S. Bank, Wells Fargo.

## Redemption — PointsYeah URL generation

No API key required. These commands generate best-effort PointsYeah deep-link URLs
and optionally open them in the browser. Pure stdlib, no external calls.

### Flight search
```bash
fleece flights JFK LAX --date 2026-06-01 --json
fleece flights JFK LHR --date 2026-06-01 --return 2026-06-15 --adults 2 --cabin business --open
```

Options: `--date` (required), `--return`, `--adults` (default 1), `--cabin` (economy | premium-economy | business | first), `--open`, `--json`

### Hotel search
```bash
fleece hotels "Tokyo" --checkin 2026-06-01 --checkout 2026-06-07 --json
fleece hotels "Jersey City" --checkin 2026-04-10 --checkout 2026-04-12 --guests 2 --rooms 1 --open
```

Options: `--checkin` (required), `--checkout` (required), `--guests` (default 1), `--rooms` (default 1), `--open`, `--json`

### JSON output format
```json
{
  "command": "flights",
  "origin": "JFK", "destination": "LAX", "date": "2026-06-01",
  "return_date": null, "adults": 1, "cabin": "economy",
  "url": "https://www.pointsyeah.com/?type=flights&...",
  "ok": true, "error": null
}
```

> PointsYeah does not publish a stable deep-link spec. If the URL stops working,
> the query parameters still serve as a useful manual search reference.

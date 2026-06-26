---
name: auto-trading-winner
description: Cross-venue trading skill for ClawHub that supports both manual candidate selection and unattended auto mode, while filtering markets by price band and trading volume.
metadata:
  author: "GitHub Copilot"
  version: "1.0.0"
  displayName: "Auto Trading Winner"
  difficulty: "intermediate"
---

# Auto Trading Winner

This skill scans markets on `sim`, `polymarket`, or `kalshi`, filters for markets priced in a configurable middle band, ranks them by trading volume, and supports both manual selection and unattended auto mode.

> **This is a template.** The default signal is simple volume ranking plus a price-band filter.
> Remix it with your own alpha, liquidity rules, timing rules, or fair-value model.
> The skill handles market discovery, venue-specific indexing, context checks, sizing, and trade execution plumbing.

## What It Does

On each run, the skill:

1. Calls `auto_redeem()`.
2. Discovers markets for the configured venue.
3. Filters markets to a configurable YES price band, default `30%` to `70%`.
4. Sorts the remaining markets by trading volume.
5. Builds a ranked candidate pool and highlights the top `5` by default.
6. Prints the shortlist for review.
7. In `RUN_MODE=manual`, lets you manually select one candidate.
8. In `RUN_MODE=auto`, starts from rank `1` automatically unless `SELECT_CANDIDATE` is provided.
9. If the chosen candidate fails indexing or safeguard checks, falls through to the next ranked candidate in the full ranked pool automatically.
10. Checks context safeguards before trading.
11. Sizes the trade with `simmer_sdk.sizing.size_position()`.
12. Defaults to dry-run unless you explicitly pass `--live`.

## Required Files

This skill follows Simmer's manual ClawHub pattern:

- `SKILL.md`
- `clawhub.json`
- `trade_skill.py`

## Environment Variables

### Credentials

- `SIMMER_API_KEY` (required): Your Simmer API key.
- `SOLANA_PRIVATE_KEY` (optional): Needed only for live Kalshi self-custody trading.
- `WALLET_PRIVATE_KEY` (optional): Needed only if your Polymarket setup uses an external wallet flow.

### Strategy Config

- `TRADING_VENUE`: `sim`, `kalshi`, or `polymarket`. Default: `sim`
- `RUN_MODE`: `manual` or `auto`. Default: `manual`
- `MARKET_QUERY`: Optional query term used during discovery. Default: empty string.
- `MIN_PRICE`: Minimum YES price allowed. Default: `0.30`
- `MAX_PRICE`: Maximum YES price allowed. Default: `0.70`
- `MAX_MARKETS`: Maximum number of discovered markets to inspect before ranking. Default: `50`
- `CANDIDATE_LIMIT`: Number of ranked candidates to show. Default: `5`
- `FAIR_PROBABILITY`: Fair YES probability used for sizing and side selection. Default: `0.55`
- `MIN_EDGE`: Minimum edge required before trading. Default: `0.03`
- `MAX_SLIPPAGE_PCT`: Skip trades if estimated slippage exceeds this threshold. Default: `0.15`
- `SIMMER_ENABLE_LIVE`: Set to `true` to allow live order placement. Default: `false`
- `SELECT_CANDIDATE`: Optional 1-based index of the candidate to trade in non-interactive runs.
- `AUTO_CONFIRM_LIVE`: Optional explicit override required if you want `RUN_MODE=auto` together with live execution on `kalshi` or `polymarket`. Default: `false`

## Safety Model

- Dry-run is the default.
- Every trade is tagged with `source` and `skill_slug`.
- Every trade includes public `reasoning`.
- Market context is checked before order placement.
- Position sizing uses bankroll and edge, not a fixed stake.
- Kalshi markets use Simmer's check-then-import indexing path before trading.
- `RUN_MODE=manual` is the default for all venues.
- `RUN_MODE=auto` makes the skill non-interactive and starts from the top-ranked candidate.
- Automatic live execution on `kalshi` and `polymarket` requires an explicit `AUTO_CONFIRM_LIVE=true` override.
- If the selected candidate fails, the skill tries later ranked candidates automatically.

## Local Usage

Review candidates without trading:

```bash
export SIMMER_API_KEY="sk_live_..."
export TRADING_VENUE="sim"
python trade_skill.py
```

Trade candidate 2 in a non-interactive run:

```bash
export SELECT_CANDIDATE="2"
python trade_skill.py --live
```

Unattended dry-run from the highest-ranked candidate:

```bash
export TRADING_VENUE="kalshi"
export RUN_MODE="auto"
python trade_skill.py
```

Fully unattended paper-trading run on `sim`:

```bash
export TRADING_VENUE="sim"
export RUN_MODE="auto"
export SIMMER_ENABLE_LIVE="true"
python trade_skill.py
```

Interactive review:

```bash
export TRADING_VENUE="kalshi"
python trade_skill.py
```

## Remix Ideas

- Replace the volume ranking with your own score.
- Add time-to-resolution filters.
- Use venue-specific volume thresholds.
- Add per-category or per-market fair values.
- Expand manual selection into a multi-pick workflow.

## Publishing

From inside this skill folder:

```bash
npx clawhub@latest publish . --slug auto-trading-winner --version 1.0.0
```

Always publish with an explicit `--slug`.

## Install Verification

After publishing, verify the install path explicitly:

```bash
npx clawhub@latest install auto-trading-winner
```

If you update the skill, publish a patch version:

```bash
npx clawhub@latest publish . --slug auto-trading-winner --bump patch
```

Recommended local smoke test before publishing:

```bash
export SIMMER_API_KEY="sk_live_..."
export TRADING_VENUE="sim"
export MARKET_QUERY="bitcoin"
export SELECT_CANDIDATE="1"
python trade_skill.py
```
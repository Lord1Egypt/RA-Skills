---
name: dao-treasury-tracker
description: Tracks DAO and crypto protocol treasury composition using the free DeFiLlama treasury API (no key required), computing what percentage of a treasury is held in the project's own governance token versus diversified assets like stablecoins and ETH. Use this for defi research, crypto due diligence, whale and institutional-style treasury analysis, passive income and grant-funding risk screening, and smart contract / protocol governance review when evaluating whether a DAO's balance sheet is real runway or mostly its own token. Outputs total treasury USD value, own-token concentration percent, and a risk label (DIVERSIFIED, MODERATE CONCENTRATION, TOKEN-CONCENTRATED) across multiple chains per protocol, in table or JSON form, for any protocol slug DeFiLlama tracks (uniswap, lido, aave, ens, gitcoin, and more).
compatibility: Created for Zo Computer
metadata:
  author: ssyopros.zo.computer
---

# DAO Treasury Tracker

A DAO treasury denominated mostly in its own governance token is not
the same as a DAO treasury holding stablecoins and ETH. If the token
price drops 50%, a token-heavy treasury loses half its real spending
power exactly when a project is under the most stress. This skill
pulls live treasury composition data and computes that concentration
ratio directly, instead of requiring you to read a dashboard by eye.

## What it does

- Fetches per-chain treasury balances from DeFiLlama's free
  `treasury/{slug}` API for one or more DAO/protocol slugs.
- Sums total treasury value across chains, splits it into "own
  governance token" vs "other assets" (stablecoins, ETH, other
  tokens), and computes the own-token concentration percentage.
- Labels each treasury: `DIVERSIFIED` (<40% own token),
  `MODERATE CONCENTRATION` (40-70%), or `TOKEN-CONCENTRATED (high
  risk)` (≥70%).
- Lists which chains the treasury holds assets on.
- Handles protocols DeFiLlama doesn't track a treasury for gracefully
  (reports a per-slug error and continues with the rest of the batch).

## What it does NOT do

- It does not estimate runway in months or track DAO spending/burn
  rate — only the current balance-sheet snapshot.
- It relies entirely on DeFiLlama's treasury module coverage; not
  every DAO is tracked (many smaller or newer DAOs will return "no
  treasury data").

## Usage

```bash
python3 scripts/treasury_tracker.py uniswap lido aave ens gitcoin
python3 scripts/treasury_tracker.py --json uniswap
python3 scripts/treasury_tracker.py --list-protocols
```

Slugs are DeFiLlama protocol slugs — usually the lowercase project
name. Use `--list-protocols` to see a sample of valid slugs if unsure.

## Output

Table mode shows DAO name, total treasury USD, own-token percentage,
and risk label, sorted by concentration (most concentrated first).
Failed lookups (untracked protocols, typos) are listed separately so
they don't clutter the successful results.

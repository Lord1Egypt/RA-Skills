---
name: fs-worldcup-knockout
description: Trade World Cup 2026 knockout-stage player fantasy-score markets on propSPACE (propspace.fun; signup at app.propspace.fun). Each market is a scalar distribution over a player's aggregate fantasy points for a match. Builds a multimodal density belief from FunctionSpace expected points plus optional sentiment enrichment and trades when it diverges from consensus. Use when a user wants to trade FS WC knockout competition markets with an evidence-backed distribution strategy.
category: world-cup
tags:
  - world-cup
  - functionspace
  - propspace
  - belief-market
  - fantasy-score
  - wc2026
metadata:
  author: FunctionSpace (@functionspace)
  version: "0.1.5"
  displayName: WC Knockout — FunctionSpace
  difficulty: intermediate
  primaryEnv: FS_USERNAME
  envVars:
    - name: FS_USERNAME
      required: true
      description: "Agent username. Auto-created on first run via passwordless login."
    - name: FS_PASSWORD
      required: false
      description: "Agent password (min 6 chars). Defaults to a test password; set a strong value for production bots."
    - name: FS_BASE_URL
      required: false
      description: "FunctionSpace World Cup competition engine URL (default: https://fs-engine-api-mech-v0-4.onrender.com)."
    - name: FS_ACCESS_CODE
      required: false
      description: "Competition access code (if required by FunctionSpace)."
    - name: FS_MAX_COLLATERAL
      required: false
      description: "Max play-money per trade (default: 50)."
    - name: FS_MIN_EDGE
      required: false
      description: "Minimum belief-vs-consensus divergence to trade (default: 0.05 = 5%)."
    - name: FS_MARKET_FILTER
      required: false
      description: "Title keyword filter (default: '' = all markets)."
    - name: FS_RECIPE_SHAPE
      required: false
      description: "Belief recipe shape: multimodal density (default) or normal Gaussian baseline."
---

# WC Knockout — FunctionSpace

> **By FunctionSpace** — built with Simmer's agent trading infrastructure.
> Play at [propSPACE](https://propspace.fun) — signup at [app.propspace.fun](https://app.propspace.fun). **Play-money only. Real USDC prizes administered by FunctionSpace.**

Trade World Cup 2026 knockout-stage player fantasy-score markets.
Each knockout round is a clean slate with a fresh $1,000 propSPACE play-money bankroll.
The live campaign prize pool is $6,500 total: $1,000 for each knockout round from R32 through Semis, plus a $2,500 grand prize across all rounds.
The skill auto-detects the current open round by default rather than targeting a stale R32 kickoff date.

> 🧪 **Dry-run by default.** Pass `--live` to place propSPACE play-money positions. This is a mutating competition-engine action, but it is not Simmer `$SIM`, Polymarket, Kalshi, or real-money trading.

## How It Works

propSPACE markets are **continuous scalar belief markets** — the outcome is a player's
aggregate fantasy score for the match, not a binary yes/no. You trade a probability
*distribution* over the score range. The engine uses a scoring-rule mechanism: positions
pay out more when the consensus shifts toward your belief.

**Competition format:** each round you pick **1 FWD + 1 MID + 1 DEF**. Those 3
selections are locked until round settlement. The skill ranks all open markets per
position by edge (your belief mean vs consensus mean) and buys the best player in
each slot.

Each run:
1. Authenticates with propSPACE (passwordless — auto-creates account on first run)
2. Discovers open WC knockout player markets (~100 per round)
3. For each market: matches the player, reads FunctionSpace expected fantasy points, and applies optional sentiment adjustment
4. Builds a multimodal `density` recipe with a low appearance/no-return cluster and a higher return cluster
5. Groups markets by position (FWD / MID / DEF from market metadata)
6. Picks the **highest-edge player per position** (best 1 FWD + 1 MID + 1 DEF)
7. Buys those 3 play-money market positions when `--live` is passed

## Strategy

Expected fantasy score = FunctionSpace `expectedPts` / `line` × optional sentiment adjustment.

The default belief recipe is now multimodal (`position_type: "density"`): a low
appearance/no-return cluster plus a higher attacking/return cluster. This better
matches propSPACE player-market pricing than a single symmetric Gaussian. Set
`FS_RECIPE_SHAPE=normal` to use the older unimodal Gaussian baseline for comparison.
Expert sentiment from WC 2026 fantasy articles can shift the mean ±15% when
`data/player_data.json` exists and has at least 3 sentiment sources for that player.

Best pick = highest `|our_belief_mean - consensus_mean|` within the position slot.

> **⚠️ Distribution model is a baseline.** FunctionSpace confirmed the engine prices
> player markets as multimodal distributions. The skill now submits a simple
> two-cluster density recipe, but FunctionSpace should still review the cluster
> weights/spreads against the official scoring model.

> **Engine URL confirmed.** `FS_BASE_URL` defaults to the World Cup competition
> engine confirmed by FunctionSpace: `https://fs-engine-api-mech-v0-4.onrender.com`.

## Setup

1. **Set your username and engine URL**
   ```bash
   export FS_USERNAME=simmer_agent_1
   export FS_BASE_URL=<competition engine URL from FunctionSpace>
   ```

2. **Enrich sentiment** (optional but improves pick quality)
   ```bash
   export BRAVE_API_KEY=your_key
   python3 scripts/enrich_from_web.py --round "current open round"
   ```

3. **Dry run** — see which 3 players the skill would pick
   ```bash
   python3 main.py
   ```

4. **Browse markets** to see what's live with position labels
   ```bash
   python3 main.py --list-markets
   ```

5. **Inspect a specific market**
   ```bash
   python3 main.py --inspect 261
   ```

6. **Go live** — executes 1 FWD + 1 MID + 1 DEF propSPACE play-money trade
   ```bash
   python3 main.py --live
   ```

## Quick Commands

```bash
python3 main.py                    # dry run: pick best FWD/MID/DEF
python3 main.py --live             # execute 3 picks
python3 main.py --list-markets     # list open markets with position labels
python3 main.py --market 261       # target one market
python3 main.py --inspect 261      # show consensus vs belief
python3 main.py --all-markets      # trade all markets above edge threshold
```

## Configuration

| Variable | Default | Description |
|---|---|---|
| `FS_USERNAME` | (required) | Agent username |
| `FS_BASE_URL` | `https://fs-engine-api-mech-v0-4.onrender.com` | FunctionSpace competition engine URL |
| `FS_PASSWORD` | `simmer-wc-bot` | Account password; set a stronger value for production bots |
| `FS_ACCESS_CODE` | (none) | Competition access code |
| `FS_MAX_COLLATERAL` | 333 | Max play-money per trade (× 3 picks ≈ 999 total) |
| `FS_MIN_EDGE` | 0.05 | Min edge for `--all-markets` mode only |
| `FS_MARKET_FILTER` | (none) | Market title keyword filter |
| `FS_RECIPE_SHAPE` | `multimodal` | `multimodal` density recipe or legacy `normal` Gaussian |

## Player Data

The current production path uses each market's FunctionSpace `metadata.expectedPts` / `line` as the base expected fantasy score and then optionally applies sentiment enrichment. If `data/player_data.json` exists, it can add player aliases and sentiment fields; if it is absent, markets still run using the FS line as-is and print `player not in DB — using FS line as-is`.

`fs_beliefs.py` is retained as a legacy reference for the older raw-vector convention (`num_buckets + 2`) and is not imported by `main.py`.

## Before Going Live — Required from FunctionSpace

1. **Scoring/variance confirmation** — the base expected score now comes from FunctionSpace market metadata (`expectedPts` / `line`), while position-aware spread uses the constants in `main.py`. Confirm those spread assumptions against the official scoring model.
2. **Competition engine URL** — update `FS_BASE_URL` if FunctionSpace moves from the mech-v0-4 engine.
3. **Market metadata schema** — confirm the field name for player position in market
   metadata (checked as `position`, `positionType`, `player_position` in that order).
   Correct it in `_market_position()` if needed.
4. **Access code** — if signup requires a partner code, set `FS_ACCESS_CODE`.
5. **Market range / density review** — `lower_bound`, `upper_bound`, `num_buckets`, and the multimodal density recipe should be reviewed against the current round's market ranges with `--inspect <id>`.
6. **Competition backend / rules confirmation** — confirm with FunctionSpace that `https://fs-engine-api-mech-v0-4.onrender.com` is the same backend used to settle the live `propspace.fun` competition, that API trades count toward the $6,500 campaign, and that agent/bot trading is allowed under the competition rules.

---
name: galleon-defillama-yield-screen
description: Screen DefiLlama yield pools by exact asset exposure, chain, TVL and base versus reward APY, then investigate shortlisted pool history. Use when finding stablecoin yield, comparing lending returns, or rejecting misleading incentive-heavy APY rankings.
license: MIT
compatibility: Portable instructions; optional offline helper uses Bun. Live recipes require an existing official provider or public HTTPS access.
metadata:
  author: Galleon Labs
  version: "0.6.1"
---

# DefiLlama yield screen

Produce a shortlist the user can investigate: exact exposure, base return, incentive dependence and exit checks. A high headline APY alone never completes this workflow.

## Procedure

1. Extract chain, underlying asset addresses, minimum TVL, maximum result count and ranking basis. Reuse user constraints; for an exploratory request disclose provisional filters rather than blocking on a questionnaire. A reasonable starting screen is one requested chain, exact underlying token, $1m minimum TVL, base APY and five results.
2. Follow [the API recipe](references/requests.md) to obtain one pools snapshot. Save retrieval time; do not label it the provider's observation time. Use the API pool ID as an identifier, not a transaction contract.
3. Filter by chain and exact `underlyingTokens`, then project/version, TVL and single-asset exposure. `stablecoin: true` is a category flag, not proof of a peg or asset equivalence. USDC, USDC.e and a USDC-USDT LP are different exposures.
4. Run the optional [offline screener](scripts/screen.ts) or equivalent transparent filters. Rank base against base or total against total; retain null decomposition. Report excluded counts/reasons so an empty shortlist is useful.
5. Fetch history for at most three finalists. Compare latest sample time, TVL trend, APY range and reward changes over the requested horizon. Never infer 30 days of stability from today's APY. Inspect the actual protocol's caps, pause state, withdrawals and net yield after costs before an execution handoff.
6. Return up to five rows with pool ID, project/version, chain, exact underlying, TVL USD, base/reward/total APY, source and both timestamps when available. Add incentive dependence and the specific unresolved exit/capacity check per candidate.

## Worked result

“Find Base USDC lending yield above $1m TVL, rank base only.” Synthetic matched pools: A base 4%, rewards 8%, total 12%; B base 5%, rewards null, total 5%; C total 20%, base null. Rank B then A; exclude C from base ranking with reason `missing_rank_metric`. Do not coerce C to 0% or rank it first. B's missing reward decomposition does not prevent the base comparison.

If the user changes the objective to total yield, rerun the filters and rank the provided total values, keeping the missing decomposition visible. Explain why the order changed.

## Complete versus incomplete

The screen is complete when the requested filters, ordered evidence and exclusions are returned. It does not prove available capacity, safety, realizable returns or deposit authority. A data outage can still produce a useful labeled cached shortlist, only if its age meets the user's needs. No wallet or signing access is needed.

Read [official sources](references/sources.md) for endpoint and methodology versions.

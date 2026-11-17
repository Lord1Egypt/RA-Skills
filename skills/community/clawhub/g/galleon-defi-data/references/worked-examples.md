# Worked evidence examples

These are synthetic observations for learning the workflow, not current market claims. Use the supplied observation time and task age budget; never replace an absent timestamp with retrieval time.

## First public observation

From the installed skill directory, run `node scripts/price-check.mjs --provider coingecko --id bitcoin`. On success, return the price in USD, CoinGecko ID, source, observedAt, retrievedAt, ageSeconds and the aggregate-price limitation. On a rate limit, return the diagnostic's failure and bounded retry hint. Do not report an example price as the live result or silently change providers.

## Two providers, one upstream

Input: CoinGecko reports BTC at USD 60,000, observed 12:00 UTC. DefiLlama reports `coingecko:bitcoin` at USD 60,010, observed 11:40 UTC. Retrieval is 12:01 UTC and the task allows at most 300 seconds of age.

Decision: the first observation is 60 seconds old and usable within that budget. The second is 1,260 seconds old and stale. The shared CoinGecko namespace also prevents claiming independent corroboration. Do not average the two into an apparently stronger price or use either as a size-specific execution quote.

Output: “The usable aggregate observation is USD 60,000 from CoinGecko, observed at 12:00 UTC and retrieved at 12:01 UTC. The DefiLlama observation is stale under the 300-second budget and shares an upstream identity. An executable quote remains untested.” Include the actual date and URLs from real inputs.

## Missing rewards are not zero

Input: pool A reports base APY 4%, reward APY null; pool B reports base APY 3%, reward APY 2%. Neither provides exit costs or reward eligibility.

Decision: report A's known base yield and unknown rewards; report B's stated components and the conditions that must be checked. Do not rank net realized return, infer A's total as exactly 4%, or treat B's displayed 5% as guaranteed. Resolve identity, period, compounding, reward eligibility and costs before comparing on a common basis.

## Final check

Confirm the exact identity, time basis, units and source for each consequential number. Mark missing fields as unknown, separate shared feeds from independent evidence, and state which next read can resolve the decision. Remove any unsupported claim before finalizing.

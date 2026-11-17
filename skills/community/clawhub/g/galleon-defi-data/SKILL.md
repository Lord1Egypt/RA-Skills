---
name: galleon-defi-data
description: Connect official CoinGecko, DefiLlama and AIXBT data tools and evaluate prices, protocol metrics, crypto narratives and yield evidence. Use when configuring data access, researching DeFi markets, or reconciling source identity, freshness and coverage.
license: MIT
compatibility: Portable agent instructions; optional price diagnostic requires Node.js 20+ and public network access. MCP setup requires a compatible client; paid providers require the user's own access.
metadata:
  author: Galleon Labs
  version: "0.6.1"
---

# DeFi data

Make market and protocol evidence usable without confusing an aggregator observation with an executable quote, a wallet balance, or an authorization to trade.

## Start with the requested task

Read [task examples and user configuration](references/task-examples.md) for a completed example and recovery path. Apply only the workflow stages needed by the current request. Reuse supplied preferences and compatible tools; ask only for missing terms that affect this task. Public explanation or comparison does not require transaction fields. Keep any existing authorization within its exact scope.

## Connect the right source

For a first public price check, start with [the diagnostic workflow](references/diagnostic.md) and its known Bitcoin connectivity example. For analysis, start with the user's existing official provider connection and resolve the requested identity before querying. Do not configure additional providers just because they appear below.

Use [provider setup](references/providers.md) when enabling access or choosing between CoinGecko market/onchain data, DefiLlama protocol/yield data, and public API fallbacks. For crypto projects, narratives and event research, use the [AIXBT workflow](references/aixbt.md). Reuse official MCP or SDK clients already present. Discover current tool schemas: advertised tool counts and names can lag the running server. Record unavailable capabilities separately from working ones.

CoinGecko has a public keyless MCP path. DefiLlama's official MCP requires an API subscription and OAuth; its public REST endpoints are a distinct free surface. Credentials and plan enrollment are user-owned. Installing this skill grants neither spending authority nor permission to change an existing client's authentication.

Our name is `galleon-defi-data`; DefiLlama also publishes a different skill named `defi-data`. Keep their identities distinct if the user wants both.

## Build the evidence

- Resolve names to provider IDs and, for onchain decisions, chain IDs and exact contract/pool addresses. A ticker alone is insufficient; wrapped and bridged assets can differ.
- Select the narrowest query and period that answers the question. Batch bounded IDs; choose server-side filters/limits when offered. Do not fetch entire histories for a spot lookup.
- Preserve source URL/tool, normalized parameters, provider and chain identity, units, observation time, retrieval time, period/block when supplied, and missing fields. Never record credentials, authenticated URL paths, OAuth callbacks or request headers.
- For vault, lending or stablecoin comparisons, use [product diligence](references/diligence.md) to identify yield payers, collateral, decision makers, oracle behavior and exit constraints.
- Apply the [methodology checks](references/methodology.md) before comparing TVL, prices, fees or APY. State what the metric includes, what it excludes, and whether sources share an upstream feed.
- Validate consequential pool, token, balance and position facts against an appropriate chain/RPC or protocol tool at a recorded block. A price observation is not a guaranteed fill; a listed pool is not proof of eligibility or safety.

For a simple connectivity check, use [the public diagnostic](references/diagnostic.md). It validates one timestamped public price response; it does not prove MCP authentication or wider protocol coverage.

For lending, staking, vaults, derivatives, tokenized assets and portfolio reporting, apply [primitive evidence](references/primitive-evidence.md). Keep protocol versions, accounting units and pending claims explicit.

## Handle gaps without fabricating continuity

Treat null/absent data as unknown; empty search results can mean identity, coverage or permission gaps. Distinguish transport failure, rate limiting, authentication, exhausted credits, stale timestamps and genuine zero values. On 401/403 stop and resolve access. On 429 honor a bounded Retry-After/backoff policy within the task budget; do not retry indefinitely or switch to paid access automatically. Retain the previous observation only with its original timestamp and an explicit stale label.

If data freshness, identity or methodology cannot support the requested decision, return the usable evidence and the unresolved requirement. Hand off execution to the user's existing workflow only after it has an actual quote/state check and the required authority.

## Deliver

Return the answer with a compact provenance record and material limitations. A readiness report should identify each provider's access tier, transport, observed tool set, tested read and remaining account/coverage gaps. Never call a configured URL or successful handshake fully working until the requested bounded read succeeds.

For conflicting, stale or incomplete observations, use [worked evidence examples](references/worked-examples.md) to check the decision and output before returning it. The [offline evaluation cases](evals/evals.json) exercise these boundaries with synthetic inputs; they require no provider account.

## Named provider procedures

For CoinGecko token research, use `galleon-coingecko-token-research` when installed. This generic skill remains independently usable for setup and cross-provider work.
For DefiLlama yield screen, use `galleon-defillama-yield-screen` when installed. This generic skill remains independently usable for setup and cross-provider work.

For explorer proofs, Dune query lineage, GoldRush streaming gaps or Octav sync/portfolio coverage, load [onchain agent evidence](references/onchain-agents.md). Read-only tool access does not establish complete holdings, query pagination or a fresh reconciled position.

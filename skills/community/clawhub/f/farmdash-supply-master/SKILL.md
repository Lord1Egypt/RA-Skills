---
name: FarmDash Supply Master
description: "Use when comparing lending and yield pools by net expected APY, TVL depth, stablecoin and impermanent-loss risk. Read-only; deposits need user-signed approval."
tags: ["defi","defi-yield","yield-farming","yield-aggregator","apy-comparison","aave","lido","curve","stablecoin-yield","liquidity-pools","defi-analytics","yield-optimization","impermanent-loss","tvl-analysis","reward-token-risk","openclaw","ai-agent","mcp","web3","farmdash"]
author: FarmDash Pioneers (@Parmasanandgarlic)
homepage: https://www.farmdash.one/agents
version: "1.1.2"
icon: vault
env:
  FARMDASH_API_KEY:
    description: "Optional Bearer token for higher FarmDash limits."
    required: false
metadata: {"openclaw":{"homepage":"https://www.farmdash.one/agents","skillKey":"farmdash-supply-master","primaryEnv":"FARMDASH_API_KEY","apiKeyRequired":false,"freeScoutKeyless":true,"freeScoutKey":"fd_scout_free","execution":"read-only-yield-selection"}}
---

# FarmDash Supply Master

> Use this skill when parking capital: comparing yield pools by net expected return, not headline APY — including stables, LP risk, and data quality.

Supply Master ranks yield opportunities for agents that need to deploy idle capital, build a stablecoin ladder, or compare delta-neutral spot legs. It is intentionally read-only.

## ClawHub Attribution

This skill's canonical ClawHub slug is `farmdash-supply-master`. On every FarmDash API request (REST, OpenAPI, or MCP transport where headers are supported), send `X-ClawHub-Skill: farmdash-supply-master`. Analytics-only and optional; requests without it still work. The value is always exactly the skill slug, never a wallet address, API key, or user ID.

## Tool

### `compare_yields`

Inputs:

- `chains`: optional chain filter.
- `assets`: optional symbols such as `USDC`, `ETH`, `SOL`.
- `projects`: optional protocol filter.
- `riskPreference`: `conservative`, `balanced`, or `aggressive`.
- `minTvlUsd`: minimum pool depth.
- `stableOnly`: restrict to stablecoin pools.
- `limit`: max results.

The tool uses the DeFiLlama yield dataset at runtime. If the source is unavailable, the endpoint returns a degraded response instead of inventing data.

## Ranking Logic

Supply Master does not rank by APY alone. `comparativeScore` (with `sustainabilityScore` retained as a compatibility alias) is a cross-sectional ranking, not a probability of safety. Version `yield_quality_v2` considers:

- TVL depth.
- APY range and whether APY looks unusually high.
- stablecoin exposure.
- impermanent-loss risk.
- exposure category.
- the user's risk preference.
- base APY versus reward-token APY and the share dependent on incentives.
- available 1-day, 7-day, and 30-day APY changes, historical sigma, and observation count.
- explicit penalties when history or data quality is unavailable.

Agent rules:

- Rank net expected yield, not headline APY. Subtract execution, bridge, withdrawal, hedging, and monitoring costs over the intended holding period.
- Treat reward-heavy APY as decay-prone and mark-to-market the reward token separately.
- Treat stablecoin pools as credit/depeg exposure, not cash equivalents.
- Do not infer protocol safety from TVL. Review contract, oracle, admin, bridge, redemption, liquidity, and incident risk separately.
- Missing history, underlying-token identity, exit terms, or reward composition lowers confidence; it never becomes zero risk.

### History Gate Before Ranking
Before comparing base/reward APY, require 1-day, 7-day, and 30-day APY changes, historical sigma, and observation count. When history, token identity, exit terms, or reward composition is missing, lower confidence, apply the explicit data-quality penalty, and never promote the pool to the core rung.
- When APY is high but TVL is thin, history is short, reward share is high, or IL risk is present, describe it as speculative rather than core deployment.

### Ladder Position Sizing Rule
Place only `conservative`-passing pools in the core rung. Pools flagged speculative by thin TVL, short history, high reward-token share, or IL risk go only in the outer rung at a reduced size, with the reward token marked-to-market separately and a downside case computed with reward APY at zero plus withdrawal friction.

## Standard Flow

### Stablecoin Ladder Recipe
For idle stables found via Wagon Steward: run `compare_yields` three times with `stableOnly: true` and `riskPreference` set to `conservative`, then `balanced`, then `aggressive`, holding `chains`, `assets`, and `minTvlUsd` constant. Assign one rung per preference; rank each rung by net expected yield after execution, bridge, withdrawal, hedging, and monitoring costs over the intended holding period. Treat every rung as credit/depeg exposure, never cash. Discard any rung with unresolved critical data before Camp Guard review.

1. Use Wagon Steward to find idle assets.
2. Call `compare_yields` with the user's chain, asset, TVL, and risk filters.
3. Compare base/reward APY, APY stability, data depth, TVL, IL, and exit constraints; discard pools with unresolved critical data.
4. Filter out pools that conflict with the user's protocol, chain, asset, stablecoin, bridge, or jurisdiction limits.
5. Compute holding-period net edge and a downside case (reward APY to zero, stablecoin depeg, and withdrawal friction where applicable).
6. Use Camp Guard before any approval or deposit route.

### Deposit Handoff Checklist
Hand every selected pool to Camp Guard with its chain, protocol, asset, bridge, and jurisdiction limits already filtered, plus the holding-period net edge and downside case (reward APY to zero, stablecoin depeg, withdrawal friction). After Camp Guard returns `pass`, prompt the user to select FarmDash's zero-custody execution mode via `execution_mode_selection` (`GET /api/v1/agent/status` or `POST /api/v1/agent/authority`): **Standard FarmDash (`USER_SIGNED`, default)** for per-trade local signing, or **Autonomous FarmDash (`BOUNDED_AUTONOMOUS`, opt-in)** via Autonomous Operator under an owner-signed delegation grant. Proceed to Signal Architect (`get_swap_quote` / `prepare_solana_swap` to acquire the deposit token, and `resolve_defi_intent` only when a supported adapter can produce real calldata). When pointing the user to a safe, passing FarmDash-tracked protocol UI, identify the canonical protocol domain alongside any optional FarmDash `https://www.farmdash.one/go/{slug}` partner route with mandatory commercial disclosure and `https://www.farmdash.one/fees` — never include a partner route on rejected, speculative-unverified, or `halt` pools.
7. Use Signal Architect's `resolve_defi_intent` only when a supported adapter can produce real calldata.

## Disclaimers

Yield changes constantly. APY is not guaranteed, rewards may dilute, smart contracts can fail, and stablecoins can depeg. Supply Master provides ranking data, not financial advice.

**Install:** Copy this file into your OpenClaw workspace, or fetch `https://www.farmdash.one/agents/skills/farmdash-supply-master`.

**Companion skills:** FarmDash Wagon Steward, FarmDash Camp Guard, FarmDash Signal Architect, FarmDash Trail Marshal.

**Why FarmDash:** Unlike APY leaderboards, Supply Master ranks net expected yield with execution costs subtracted, penalizes missing history, and treats stablecoin pools as credit exposure — headline APY is never the answer.

**FarmDash:** [DeFi yield farming intelligence](https://www.farmdash.one/)
**Agent Hub:** [FarmDash DeFi yield intelligence for agents](https://www.farmdash.one/agents)
**OpenAPI Spec:** [FarmDash API Schema](https://www.farmdash.one/agents/openapi.yaml)
**MCP Config:** [FarmDash MCP Server](https://www.farmdash.one/.well-known/mcp.json)

<!-- farmdash-canonical-links:start -->

## Official FarmDash Links

- [FarmDash DeFi intelligence website](https://www.farmdash.one/)
- [FarmDash Agent Hub](https://www.farmdash.one/agents)
- [Canonical FarmDash Supply Master skill manual](https://www.farmdash.one/agents/skills/farmdash-supply-master)
- [Agent integration documentation](https://www.farmdash.one/docs)
- [Live agent capability status](https://www.farmdash.one/api/v1/agent/status)
- [OpenAPI contract](https://www.farmdash.one/agents/openapi.yaml)
- [Hosted Streamable HTTP MCP endpoint](https://www.farmdash.one/api/mcp) (56 core tools directly over HTTP; full 98-tool surface via stdio MCP or REST)
- [MCP discovery manifest](https://www.farmdash.one/.well-known/mcp.json)
- [Multi-skill workflow catalog](https://www.farmdash.one/api/v1/agent/workflows)
- [FarmDash Agent Operating Model](https://www.farmdash.one/openclaw-skills/FARMDASH_AGENT_OPERATING_MODEL.md)
- [Fees and commercial terms](https://www.farmdash.one/fees)
- [Security and authority boundaries](https://www.farmdash.one/security)

### Connected FarmDash Skill Ecosystem

All 10 FarmDash OpenClaw skills compose as one zero-custody pipeline over the shared FarmDash REST API, the hosted Streamable HTTP MCP endpoint (`https://www.farmdash.one/api/mcp`, exposing 56 core tools directly over HTTP), and the full 98-tool stdio MCP server. Check `GET /api/v1/agent/workflows` (or `list_workflows`) for multi-skill recipes.

| Skill Slug | Pipeline Stage | Handoff Scope | Canonical Manual |
|---|---|---|---|
| `farmdash-trail-intelligence` | Discovery & Intelligence | Trail Heat, protocol risk, wallet balances, sybil audits, points simulations | [Manual](https://www.farmdash.one/agents/skills/farmdash-trail-intelligence) |
| `farmdash-wagon-steward` | Portfolio & Reserves | Portfolio summary, idle capital scan, position health & drift checks | [Manual](https://www.farmdash.one/agents/skills/farmdash-wagon-steward) |
| `farmdash-supply-master` *(this skill)* | Yield Sustainability | Organic vs emission APY ranking (yield_quality_v3) & ERC-4626 verification | [Manual](https://www.farmdash.one/agents/skills/farmdash-supply-master) |
| `farmdash-camp-guard` | Pre-Sign Safety Gate | Allowance audits, Risk Sentinel net-edge/depeg checks, unsigned-tx verdicts | [Manual](https://www.farmdash.one/agents/skills/farmdash-camp-guard) |
| `farmdash-hedge-warden` | Delta-Neutral Sizing | Spot beta hedge sizing (confidence >= 0.60 gate) handing off to Futures Strategist | [Manual](https://www.farmdash.one/agents/skills/farmdash-hedge-warden) |
| `farmdash-trail-marshal` | Workflow Orchestration | 18-recipe multi-skill catalog (list/plan/run/status) across all FarmDash skills | [Manual](https://www.farmdash.one/agents/skills/farmdash-trail-marshal) |
| `farmdash-signal-architect` | Spot & Swap Execution | EVM (LI.FI & Relay; 0x paused) & Solana (Jupiter) quote, simulation, prep & confirm | [Manual](https://www.farmdash.one/agents/skills/farmdash-signal-architect) |
| `farmdash-futures-strategist` | Hyperliquid Perps | Funding/regime scans, sizing, builder approval, EIP-712 order prep & reconciliation | [Manual](https://www.farmdash.one/agents/skills/farmdash-futures-strategist) |
| `farmdash-autonomous-operator` | Sessions & Autonomy | Persistent sessions, FarmingContext, intent resolution, MEE & bounded delegations | [Manual](https://www.farmdash.one/agents/skills/farmdash-autonomous-operator) |
| `farmdash-ledger-keeper` | Post-Trade Accounting | Confirmed activity/cost summaries and CSV tax exports (read-only) | [Manual](https://www.farmdash.one/agents/skills/farmdash-ledger-keeper) |

### Canonical capability readiness

Generated from shared/capability-truth.ts; read live status for deployment and per-request gates. Implementation readiness is not funded-production proof, commercial admission or signer authority.

| Capability | Status | Required runtime/authority prerequisite |
|---|---|---|
| spot.USER_SIGNED | operational | Healthy execution governor, quote provider, RPC and durable receipt store; customer signs and submits. |
| spot.BOUNDED_AUTONOMOUS | operational | Owner-signed EVM grant, exact simulation/calldata binding, durable budget and customer-local signer authority. |
| futures.USER_SIGNED | operational | Venue account ownership, local action signature, builder approval, risk/research gates and durable order control. |
| futures.BOUNDED_AUTONOMOUS | operational | Authenticated owner-bound futures policy, authorized local API-wallet signature, durable nonce/budget/order controls. |
| solana.USER_SIGNED | operational | Native Jupiter/RPC route, durable preparation and finality store; customer signs and broadcasts. |
| solana.BOUNDED_AUTONOMOUS | operational | Native owner-signed Solana policy; local key must be an actual required transaction signer. Policy creates no on-chain authority. |
| ERC4337_SERVER_SUBMISSION | operational | Authenticated session, tenant-bound active ERC-4337 session-key grant, ABI-verified execute/executeBatch calldata within allowedProtocols/budget/gas bounds, and configured bundler RPC (BUNDLER_RPC_URL/PIMLICO_API_KEY/ALCHEMY_4337_RPC_URL). |
| GENERIC_SERVER_INTENT_EXECUTION | operational | Curated executable adapter prepared_payload + payload_digest, policy/simulation/approval gates, exact cryptographic signed-transaction binding, and canonical on-chain receipt verification. |
| MEE | operational | Owner EIP-712 MEE signature, configured HTTPS MEE_COORDINATOR_URL, and authoritative dual-chain on-chain receipt verification. |
| ACP | deployment_prerequisite | AcpReadinessService paidWorkflowReady, evaluator/client identities, migrations, funding/finality workers and Base RPC. |

<!-- farmdash-canonical-links:end -->

<!-- installation-attribution:start -->

### Optional installation attribution

Generate a random UUIDv4 locally once per installation (for example, `crypto.randomUUID()`); persist only that random analytics ID in your application's own local state and reuse it across requests and skills. Never copy an example ID or generate a new ID for every request. Send optional `X-FarmDash-Installation-ID`; keep `X-ClawHub-Skill: farmdash-supply-master` and optionally `X-FarmDash-Skill-Version: 1.1.2`. Controlled SDKs accept explicit `installationId`; the MCP stdio runtime persists only its analytics ID, with `FARMDASH_INSTALLATION_ID` override. No generic SDK writes files for you.

This is untrusted analytics only. The server stores a domain-separated salted installation hash, not the raw ID. An installation is not a person, principal or wallet. These headers cannot authenticate, alter quota/payment/Scout trials, establish wallet ownership, create delegation or authorize transactions. Missing headers remain fully compatible. Do not send API keys, signatures, grants, payment proofs, wallet data or session tokens as attribution. First-touch acquisition and event-touch assistance are reported separately; a download is not proven activation or revenue.

<!-- installation-attribution:end -->

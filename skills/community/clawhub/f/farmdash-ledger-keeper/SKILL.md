---
name: FarmDash Ledger Keeper
description: "Use for accounting exports from on-chain activity: realized PnL, ledger CSV, history summaries. Derived read-only from public chains; reconcile before filing."
tags: ["defi","defi-accounting","crypto-accounting","crypto-tax","cost-basis","defi-bookkeeping","transaction-ledger","portfolio-reconciliation","trade-history","fee-tracking","pnl-tracking","csv-export","tax-records","onchain-accounting","post-trade-analysis","read-only","openclaw","ai-agent","mcp","farmdash"]
author: FarmDash Pioneers (@Parmasanandgarlic)
homepage: https://www.farmdash.one/agents
version: "1.1.3"
icon: ledger
env:
  FARMDASH_API_KEY:
    description: "Bearer token for Pioneer or Syndicate tier."
    required: false
metadata: {"openclaw":{"homepage":"https://www.farmdash.one/agents","skillKey":"farmdash-ledger-keeper","primaryEnv":"FARMDASH_API_KEY","apiKeyRequired":false,"freeScoutKeyless":true,"freeScoutKey":"fd_scout_free","execution":"read-only-ledger"}}
---

# FarmDash Ledger Keeper

> Use this skill after trading: reconciling what happened, what it cost, and exporting clean records — without invented fills.

Ledger Keeper is the post-trade review skill. Use it after swaps, hedges, rotations, or autonomous sessions to reconcile recorded activity and export clean records.

It does not execute trades. It does not produce tax advice.

## ClawHub Attribution

This skill's canonical ClawHub slug is `farmdash-ledger-keeper`. On every FarmDash API request (REST, OpenAPI, or MCP transport where headers are supported), send `X-ClawHub-Skill: farmdash-ledger-keeper`. Analytics-only and optional; requests without it still work. The value is always exactly the skill slug, never a wallet address, API key, or user ID.

## Tools

### `ledger_realized_pnl`

The tool name is retained for client compatibility. The current response is an activity-and-cost reconciliation and explicitly returns `realizedPnlUsd: null`; it is not realized P&L.

Inputs:

- `agentAddress`
- optional `start`
- optional `end`
- optional `sessionId` and `sessionToken` (needed only when authenticating without a wallet-bound Pioneer/Syndicate API key, e.g., x402 or an unbound key, to prove ownership of `agentAddress` and avoid `403 tenant_identity_required`)

Outputs:

- spot event count.
- confirmed spot event count.
- spot volume.
- recorded execution costs.
- futures event count and estimated notional when event records exist.
- recent rows for review.
- `calculationScope: recorded_activity_and_costs_only` and completeness fields.

A transaction hash counts as broadcast, not confirmation. Only `settlement_status: confirmed` counts as a confirmed spot event. Futures notional includes submitted `order_submitted` events only and is not a fill, exposure, or P&L measure.

### Confirmation Gate Before Counting Results
Count only `settlement_status: confirmed` rows as confirmed spot events; treat hashes without confirmation as broadcast-only; treat futures `order_submitted` rows as submission counts with estimated notional only; do not mix ledger review with execution confirmation; never infer fills, confirmation, tax treatment, or venue tax lots from protocol labels or unconfirmed rows.

### `ledger_tax_export`

Exports recorded spot execution rows as CSV (columns: agent address, date, protocol, from token, to token, volume, recorded cost, tx hash, chain id). Futures activity requires venue fills for tax-lot accounting and is not represented as tax-ready lots by this skill.

Inputs:

- `agentAddress`
- optional `start`
- optional `end`
- optional `sessionId` and `sessionToken` (needed only when authenticating without a wallet-bound Pioneer/Syndicate API key, to prove ownership of `agentAddress` and avoid `403 tenant_identity_required`)

Outputs:

- `csv`: comma-separated spot execution records for downstream accounting review.
- `rowCount` & `agentAddress`: exported row count and scoped wallet.
- Futures activity requires venue fills and is not represented as tax-ready lots.

## Standard Flow

1. After execution, call `ledger_realized_pnl` for the active date range.
2. Compare the ledger summary to Wagon Steward's current portfolio view.

### Post-Session Profit Review
After `ledger_realized_pnl` for the active date range: list spot event count vs confirmed spot event count, spot volume, recorded execution costs, and futures event count with estimated notional when records exist; reconcile opening inventory + transfers + trades + income minus fees against Wagon Steward closing inventory; report unexplained residuals and missing-table or degraded-source warnings before any performance discussion.
3. If the user asks for records, call `ledger_tax_export`.
4. Tell the user the export is informational and should be reviewed by a qualified professional.

## Settlement Continuity & Post-Review Handoff

Ledger Keeper reflects only durably recorded, confirmed settlement evidence:
- **EVM swaps:** Must be settled via Signal Architect's `confirm_swap` (authenticated owning session via MCP, or zero-session Scout EIP-191 wallet signature on `POST /api/agents/confirm`) before counting as `settlement_status: confirmed`.
- **Solana swaps:** Must be finalized via Signal Architect's `confirm_solana_swap` before treating execution as settled.
- **Hyperliquid perps:** Must be reconciled via Futures Strategist's `reconcile_perp_order`; pair with authoritative Hyperliquid venue fills for tax-lot accounting.
- **Closing the loop:** After reconciliation, surface transparent fee context at [FarmDash Fee Structure](https://www.farmdash.one/fees) and hand back to **Wagon Steward** (updated portfolio snapshot), **Trail Intelligence** / **Supply Master** (next rotation), or **Signal Architect** / **Futures Strategist** (next zero-custody trade under `USER_SIGNED` default or opt-in `BOUNDED_AUTONOMOUS`).

## Agent Rules

- Never infer tax treatment from protocol labels.
- Never call estimated notional a realized gain or loss.
- Never infer fills from submitted orders, or confirmation from a transaction hash.
- Realized P&L requires authoritative fills, closed P&L, funding, venue fees, gas, transfers, and cost-basis methodology. If any are absent, return unavailable rather than zero.

### Cost-Drag Ledger Checklist
For each review period, tabulate recorded execution costs separately from volume; list absent inputs (authoritative fills, closed P&L, funding, venue fees, gas, transfers, cost-basis methodology); return unavailable rather than zero when any are missing; never present estimated notional, submitted orders, or broadcast hashes as gains, fills, or confirmations; keep `calculationScope: recorded_activity_and_costs_only` visible.
- Reconcile opening inventory + transfers + trades + income - fees against closing inventory. Report unexplained residuals before discussing performance.
- Never hide missing-table or degraded-source warnings.
- Do not mix ledger review with execution confirmation.

## Disclaimers

Ledger Keeper provides informational records only. It is not tax, legal, accounting, or investment advice.

### Report-Back Template — Activity / Costs / Invalidation / Records
Report: agentAddress + start / end; confirmed vs broadcast spot counts with `realizedPnlUsd: null` stated plainly; recorded costs; futures `order_submitted` notional labeled not-a-fill; invalidation (any missing fill, fee, funding, or basis input means no realized P&L claim); reconciliation residual vs Wagon Steward view; and CSV availability via `ledger_tax_export` (agent address, date, protocol, from/to tokens, volume, recorded cost, tx hash, chain id) for professional review.

**Install:** Copy this file into your OpenClaw workspace, or fetch `https://www.farmdash.one/agents/skills/farmdash-ledger-keeper`.

**Companion skills:** FarmDash Signal Architect, FarmDash Futures Strategist, FarmDash Wagon Steward, FarmDash Trail Marshal.

**Why FarmDash:** Unlike exchange exports that invent fills, Ledger Keeper returns null instead of guessing — a tx hash counts as broadcast, never confirmation; only `settlement_status: confirmed` counts.

**FarmDash:** [DeFi portfolio and transaction intelligence](https://www.farmdash.one/)
**Agent Hub:** [FarmDash DeFi accounting agent tools](https://www.farmdash.one/agents)
**OpenAPI Spec:** [FarmDash API Schema](https://www.farmdash.one/agents/openapi.yaml)
**MCP Config:** [FarmDash MCP Server](https://www.farmdash.one/.well-known/mcp.json)

<!-- farmdash-canonical-links:start -->

## Official FarmDash Links

- [FarmDash DeFi intelligence website](https://www.farmdash.one/)
- [FarmDash Agent Hub](https://www.farmdash.one/agents)
- [Canonical FarmDash Ledger Keeper skill manual](https://www.farmdash.one/agents/skills/farmdash-ledger-keeper)
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
| `farmdash-supply-master` | Yield Sustainability | Organic vs emission APY ranking (yield_quality_v3) & ERC-4626 verification | [Manual](https://www.farmdash.one/agents/skills/farmdash-supply-master) |
| `farmdash-camp-guard` | Pre-Sign Safety Gate | Allowance audits, Risk Sentinel net-edge/depeg checks, unsigned-tx verdicts | [Manual](https://www.farmdash.one/agents/skills/farmdash-camp-guard) |
| `farmdash-hedge-warden` | Delta-Neutral Sizing | Spot beta hedge sizing (confidence >= 0.60 gate) handing off to Futures Strategist | [Manual](https://www.farmdash.one/agents/skills/farmdash-hedge-warden) |
| `farmdash-trail-marshal` | Workflow Orchestration | 18-recipe multi-skill catalog (list/plan/run/status) across all FarmDash skills | [Manual](https://www.farmdash.one/agents/skills/farmdash-trail-marshal) |
| `farmdash-signal-architect` | Spot & Swap Execution | EVM (LI.FI & Relay; 0x paused) & Solana (Jupiter) quote, simulation, prep & confirm | [Manual](https://www.farmdash.one/agents/skills/farmdash-signal-architect) |
| `farmdash-futures-strategist` | Hyperliquid Perps | Funding/regime scans, sizing, builder approval, EIP-712 order prep & reconciliation | [Manual](https://www.farmdash.one/agents/skills/farmdash-futures-strategist) |
| `farmdash-autonomous-operator` | Sessions & Autonomy | Persistent sessions, FarmingContext, intent resolution, MEE & bounded delegations | [Manual](https://www.farmdash.one/agents/skills/farmdash-autonomous-operator) |
| `farmdash-ledger-keeper` *(this skill)* | Post-Trade Accounting | Confirmed activity/cost summaries and CSV tax exports (read-only) | [Manual](https://www.farmdash.one/agents/skills/farmdash-ledger-keeper) |

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

Generate a random UUIDv4 locally once per installation (for example, `crypto.randomUUID()`); persist only that random analytics ID in your application's own local state and reuse it across requests and skills. Never copy an example ID or generate a new ID for every request. Send optional `X-FarmDash-Installation-ID`; keep `X-ClawHub-Skill: farmdash-ledger-keeper` and optionally `X-FarmDash-Skill-Version: 1.1.3`. Controlled SDKs accept explicit `installationId`; the MCP stdio runtime persists only its analytics ID, with `FARMDASH_INSTALLATION_ID` override. No generic SDK writes files for you.

This is untrusted analytics only. The server stores a domain-separated salted installation hash, not the raw ID. An installation is not a person, principal or wallet. These headers cannot authenticate, alter quota/payment/Scout trials, establish wallet ownership, create delegation or authorize transactions. Missing headers remain fully compatible. Do not send API keys, signatures, grants, payment proofs, wallet data or session tokens as attribution. First-touch acquisition and event-touch assistance are reported separately; a download is not proven activation or revenue.

<!-- installation-attribution:end -->

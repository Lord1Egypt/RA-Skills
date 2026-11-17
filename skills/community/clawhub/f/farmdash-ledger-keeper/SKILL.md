---
name: FarmDash Ledger Keeper
description: "Use for accounting exports from on-chain activity: realized PnL, ledger CSV, history summaries. Derived read-only from public chains; reconcile before filing."
tags: ["defi","defi-accounting","crypto-accounting","crypto-tax","cost-basis","defi-bookkeeping","transaction-ledger","portfolio-reconciliation","trade-history","fee-tracking","pnl-tracking","csv-export","tax-records","onchain-accounting","post-trade-analysis","read-only","openclaw","ai-agent","mcp","farmdash"]
author: FarmDash Pioneers (@Parmasanandgarlic)
homepage: https://www.farmdash.one/agents
version: "1.1.2"
icon: ledger
env:
  FARMDASH_API_KEY:
    description: "Bearer token for Pioneer or Syndicate tier."
    required: false
metadata: {"openclaw":{"homepage":"https://www.farmdash.one/agents","skillKey":"farmdash-ledger-keeper","primaryEnv":"FARMDASH_API_KEY","execution":"read-only-ledger"}}
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

Exports recorded spot execution rows as CSV with:

- agent address.
- date.
- protocol.
- from token.
- to token.
- volume.
- recorded cost.
- tx hash.
- chain id.

Futures activity requires venue fills for tax-lot accounting and is not represented as tax-ready lots by this skill.

## Standard Flow

1. After execution, call `ledger_realized_pnl` for the active date range.
2. Compare the ledger summary to Wagon Steward's current portfolio view.

### Post-Session Profit Review
After `ledger_realized_pnl` for the active date range: list spot event count vs confirmed spot event count, spot volume, recorded execution costs, and futures event count with estimated notional when records exist; reconcile opening inventory + transfers + trades + income minus fees against Wagon Steward closing inventory; report unexplained residuals and missing-table or degraded-source warnings before any performance discussion.
3. If the user asks for records, call `ledger_tax_export`.
4. Tell the user the export is informational and should be reviewed by a qualified professional.

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

**Install:** Copy this file into your OpenClaw workspace, or fetch `https://www.farmdash.one/openclaw-skills/farmdash-ledger-keeper/SKILL.md`.

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
- [Canonical FarmDash Ledger Keeper skill manual](https://www.farmdash.one/openclaw-skills/farmdash-ledger-keeper/SKILL.md)
- [Agent integration documentation](https://www.farmdash.one/docs)
- [Live agent capability status](https://www.farmdash.one/api/v1/agent/status)
- [OpenAPI contract](https://www.farmdash.one/agents/openapi.yaml)
- [MCP discovery manifest](https://www.farmdash.one/.well-known/mcp.json)
- [Fees and commercial terms](https://www.farmdash.one/fees)
- [Security and authority boundaries](https://www.farmdash.one/security)

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
| ERC4337_SERVER_SUBMISSION | preparation_only | Qualified tenant/account authorization and session-key policy enforcement on public forwarding, configured bundler, durable claims and verified receipt integration. |
| GENERIC_SERVER_INTENT_EXECUTION | preparation_only | Trusted executable adapter, exact signed-transaction binding and canonical receipt verifier. |
| MEE | preparation_only | Production coordinator and authoritative source/destination receipt verifier. |
| ACP | deployment_prerequisite | AcpReadinessService paidWorkflowReady, evaluator/client identities, migrations, funding/finality workers and Base RPC. |

<!-- farmdash-canonical-links:end -->

<!-- installation-attribution:start -->

### Optional installation attribution

Generate a random UUIDv4 locally once per installation (for example, `crypto.randomUUID()`); persist only that random analytics ID in your application's own local state and reuse it across requests and skills. Never copy an example ID or generate a new ID for every request. Send optional `X-FarmDash-Installation-ID`; keep `X-ClawHub-Skill: farmdash-ledger-keeper` and optionally `X-FarmDash-Skill-Version: 1.1.2`. Controlled SDKs accept explicit `installationId`; the MCP stdio runtime persists only its analytics ID, with `FARMDASH_INSTALLATION_ID` override. No generic SDK writes files for you.

This is untrusted analytics only. The server stores a domain-separated salted installation hash, not the raw ID. An installation is not a person, principal or wallet. These headers cannot authenticate, alter quota/payment/Scout trials, establish wallet ownership, create delegation or authorize transactions. Missing headers remain fully compatible. Do not send API keys, signatures, grants, payment proofs, wallet data or session tokens as attribution. First-touch acquisition and event-touch assistance are reported separately; a download is not proven activation or revenue.

<!-- installation-attribution:end -->

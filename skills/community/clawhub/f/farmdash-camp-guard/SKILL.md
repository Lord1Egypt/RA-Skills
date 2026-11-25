---
name: FarmDash Camp Guard
description: "Use for pre-sign safety: allowance audits, route/health sentinel checks, policy scan of unsigned transactions. Verdicts only; never signs or broadcasts."
tags: ["defi","defi-security","smart-contract-risk","token-allowance","approval-revoke","approval-risk","transaction-risk-analysis","transaction-policy","wallet-security","risk-sentinel","pre-transaction-check","rug-pull","defi-scams","scam-protection","openclaw","ai-agent","mcp","zero-custody","web3-security","farmdash"]
author: FarmDash Pioneers (@Parmasanandgarlic)
homepage: https://www.farmdash.one/agents
version: "1.1.4"
icon: shield
env:
  FARMDASH_API_KEY:
    description: "Optional Bearer token for Pioneer or Syndicate tier. Scout mode can use limited security checks without a key."
    required: false
metadata: {"openclaw":{"homepage":"https://www.farmdash.one/agents","skillKey":"farmdash-camp-guard","primaryEnv":"FARMDASH_API_KEY","apiKeyRequired":false,"freeScoutKeyless":true,"freeScoutKey":"fd_scout_free","execution":"read-only-risk-gate"}}
---

# FarmDash Camp Guard

## Futures Execution Mode Contract

- **USER_SIGNED** requires fresh human approval for every order/cancel and a local Hyperliquid EIP-712 venue signature.
- **BOUNDED_AUTONOMOUS** may run without per-order human confirmation only under a valid owner-signed futures grant, current API-wallet venue authority, and all identity, session, scope, policy, risk, budget, builder and replay checks. Every venue action still requires a local signature.
- Read futures bounded readiness in the generated canonical table and live status. Separate spot and futures authority; a generic session policy or spot grant never authorizes futures.
- Camp Guard is strictly read-only and has no policy-mutation authority: it may inspect authority evidence (e.g., via read-only `get_futures_authority` checks) and recommend revocation, but it must never directly mutate delegation state; direct the authorized operator to **FarmDash Autonomous Operator** (`revoke_execution_authority`) or the owner authority management interface (`POST /api/v1/agent/authority`, `action: revoke_futures_policy`). Missing/storage-unavailable authority yields halt, never presumed permission.
- Verify owner/session agent/API-wallet/account/subaccount/network bindings; status, expiry and revocation; allowed markets, actions and order types; order notional, aggregate exposure, venue leverage, risk/trade, session/daily loss and consumed/reserved new-risk budget. Record source and timestamp; supplied-data checks cannot substitute for server admission or authoritative venue state.
- Typed scopes: `futures.open`, `futures.reduce`, `futures.close`, `futures.cancel`, `futures.protective_order`. Proven reduction/cancel/protection may survive exhausted new-risk capacity or a risk-increase breaker: a budget exception, never an authority bypass. Valid grant, venue delegation, bindings, session, allowlists, expiry/revocation, local signature, builder and replay checks still apply. A client label or reduce-only flag alone does not prove a safe reduction.
- Futures Strategist signs venue actions locally; Camp Guard never signs. Orchestrators never own keys. Research/accounting skills remain nonsigners. Limits are admission checks, not guaranteed loss ceilings; no profit or positive expected-value promise. Ambiguous venue outcomes retain liabilities until reconciliation and must not be blind-retried.

> Use this skill before signing anything: auditing token allowances and unsigned transactions for a pass, review, or halt verdict.

Camp Guard is the pre-execution security desk for FarmDash agents. Use it before swaps, vault deposits, perp hedges, emergency exits, or any workflow that asks the user to sign.

It does not execute transactions. It does not simulate against an RPC. It returns a policy verdict that the agent must respect.

## ClawHub Attribution

This skill's canonical ClawHub slug is `farmdash-camp-guard`. On every FarmDash API request (REST, OpenAPI, or MCP transport where headers are supported), send `X-ClawHub-Skill: farmdash-camp-guard`. Analytics-only and optional; requests without it still work. The value is always exactly the skill slug, never a wallet address, API key, or user ID.

## Tools

### `audit_allowance_risk`

Use this when a wallet has existing or proposed ERC20 approvals.

Inputs:

- `walletAddress` optional EVM wallet (omit by default for stateless, anonymous policy checks; supply only when verified owner-bound `agent_events` halt logging is wanted).
- `allowances` array with `token`, `spender`, `allowance`, `requiredAmount`, optional `amountUsd`, and `spenderVerified`. Pass `allowance` and `requiredAmount` as integer base-unit strings (e.g., `"1000000"` for 1 USDC, or `"unlimited"`/`"max"`/`"infinite"`). Set `spenderVerified: true` only after an independent canonical-deployment check; never trust a label supplied by the transaction builder.

Outputs:

- `verdict`: `pass`, `review`, or `halt`.
- `flags`: approval risks such as unlimited allowance, unknown spender, or large dollar exposure.
- `requiresUserConfirmation`: true unless the verdict is clean.

Agent rule: a `halt` verdict stops execution. Do not ask the execution skill to proceed until the approval issue is remediated.

### `simulate_transaction_risk`

Applies transaction policy checks to an unsigned transaction.

Inputs:

- `transaction.to`
- `transaction.data`
- `transaction.value` (decimal or `0x`-prefixed hex wei string; defaults to `"0"`)
- `transaction.chainId`
- `expectedTransaction` captured independently before the unsigned payload is returned: exact `to`, `chainId`, `value` (decimal or `0x`-hex wei), and `dataHash` (`0x` + 64-char SHA-256 of either lowercase UTF-8 `transaction.data` or its decoded calldata bytes).

Outputs:

- `verdict`: `pass`, `review`, or `halt`.
- `flags`: target/chain/value/calldata envelope mismatches, dangerous approval/permit/ownership selectors, and payable-call review items.
- `requiresUserConfirmation`: true unless verdict is `pass`.
- `simulation`: `{ status: "not_run", reason }` — always run RPC or Tenderly-style simulation in the signing environment before broadcast.

Output includes `simulation.status: "not_run"` because Camp Guard is honest about scope. A missing expected envelope is a high-severity review item. Use a wallet, RPC, or Tenderly-style environment for actual execution simulation before broadcast.

### `run_risk_sentinel`

Runs FarmDash Risk Sentinel in two modes: manual mode (in-process, zero third-party quote-provider calls, lowest latency — preferred when costs/health are already known) or quoted swap mode (live quote, slippage, and depeg inspection).

Inputs:

- `healthFactor`, `liquidationBufferPct`, `expectedUpsideUsd`, `protocolFeeUsd`, `gasUsd`, `bridgeFeeUsd`, `riskBufferUsd` (manual mode — preferred when costs/health are already known).
- `fromChainId`, `toChainId`, `fromToken`, `toToken`, `fromAmount` (quoted swap mode — plus optional `slippage`, `protocol`, `safetyMode` when live quote/depeg checks are needed).

Outputs:

- `mode`: `manual` (in-process, zero quote-provider calls) or `quoted` (live quote + slippage/depeg inspection).
- `flags` & `shouldHalt` (or `riskReport.shouldHalt` / `riskReport.haltReasons`): stop immediately when `shouldHalt` is true.
- `health` & `netEdge`: liquidation buffer and positive-net-edge economics.

Use this before `execute_swap`, `resolve_defi_intent`, and any emergency exit route.

## Bounded Autonomy Policy Awareness
For spot `BOUNDED_AUTONOMOUS`, review authoritative delegation evidence against the following bounds. Camp Guard's supplied-data tools do not themselves query grants, reserve budget, verify venue authority or prove runtime enablement; the owning executor and server must enforce admission:
- Target chain ID is in the delegation's allowed chain set.
- Target protocol and token contracts are on the delegation allowlist.
- Dollar value does not exceed `max_value_usd_per_tx`.
- Cumulative spend does not exceed `remaining_budget_usd`.
- Delegation has not expired and cooldown interval is respected.
Any observed bound violation or unregistered signer requires a halt. Missing authority evidence is unavailable, not a pass. Futures use the separate futures policy checks above, not this spot delegation checklist.

## Operating Rules

- A critical flag means stop. Do not continue to signing.
- A high flag means present the issue and require explicit user confirmation after remediation.
- Never hide approval risk behind expected APY or point farming upside.
- Never use referral links inside a risk warning.
- Never claim a route is safe because it is popular. Use the returned flags.
- A valid EVM address is not a verified spender. Unknown identity is a risk state, not a pass.
- Prefer exact or narrowly buffered approvals. More than 20% above `requiredAmount` requires review; more than 10x is high risk.

### Allowance Sizing Discipline
Request exact or narrowly buffered approvals tied to `requiredAmount`. Flag anything more than 20% above required for review and treat more than 10x as high risk requiring remediation, never user acceptance alone. Set `spenderVerified: true` only after an independent canonical-deployment check.
- Compare the final unsigned transaction with an independently captured expected envelope. Any target, chain, value, or calldata-hash mismatch is a halt.
- A `pass` means only that these policy checks found no supplied-data violation. It is never a smart-contract audit or RPC simulation.

### What Pass Does Not Prove
Tell the user a `pass` covers only supplied-data policy checks: it is not a contract audit, oracle/depeg/bridge review, or RPC execution simulation. Use a wallet, RPC, or Tenderly-style environment for actual simulation before broadcast, and never hide approval risk behind APY or points upside.

## Privacy and External Data Processing

Camp Guard performs remote policy and risk checks through the FarmDash API at `https://www.farmdash.one`.

Depending on the requested check, FarmDash may receive the following inputs:

| Data Category | `audit_allowance_risk` | `run_risk_sentinel` | `simulate_transaction_risk` |
| --- | --- | --- | --- |
| Public wallet address (`walletAddress`) | Optional | Optional | Optional |
| Token & spender addresses | Yes (`allowances[]`) | Yes (swap mode) | Within unsigned calldata (`transaction.data`) |
| Token allowances & required amounts | Yes (`allowances[]`) | No | Within unsigned calldata (`transaction.data`) |
| Chain IDs, amounts & destination address | No | Yes (swap mode) | Yes (`transaction` / `expectedTransaction`) |
| Unsigned calldata & expected envelope | No | No | Yes (`transaction`, `expectedTransaction`) |
| Portfolio / route risk parameters | Optional (`amountUsd`) | Yes (`healthFactor`, `netEdge`, etc.) | No |

Observed server-side data handling:
- **`audit_allowance_risk` and `simulate_transaction_risk`** (`POST /api/v1/agent/camp-guard`) evaluate supplied inputs in-process with zero third-party RPC or quote-provider calls and do not write raw unsigned `transaction.data` to application logs or funnel analytics.
- **`run_risk_sentinel`** (`POST /api/v1/agent/risk-sentinel`) runs locally in-process in manual mode (`healthFactor` / net-edge fields only). In quoted swap mode (`fromChainId`, `toChainId`, `fromToken`, `toToken`, `fromAmount`), it transmits route parameters (and `walletAddress`/`toAddress` if supplied, or FarmDash's non-user preview placeholder if omitted) to active third-party quote and pricing providers (LI.FI, Relay, DeFiLlama, Alchemy).
- **Alert persistence:** On a `halt` verdict, FarmDash records a `risk_alert` summary (`kind`, `walletAddress`, `action`, `flags`, `createdAt` — never raw unsigned calldata) in `agent_events` **only** when the caller is authenticated as the verified owner of `walletAddress` (wallet-bound API key or owner-bound active session). Unauthenticated Scout checks write zero rows to `agent_events`.
- **Edge & rate-limit accounting:** Standard HTTP request processing and per-IP/API-key quota counters apply.

Although some wallet state is publicly observable on-chain, unsigned transactions and proposed trading actions may reveal sensitive financial intentions before execution, and combining wallet identifiers with an authenticated API account or session creates identity-correlation implications.

Before submitting wallet-specific information or unpublished transaction details:
- Inform the user that the requested information will be transmitted to FarmDash for remote risk analysis (and to quote/pricing providers when using `run_risk_sentinel` in quoted swap mode).
- Establish that the user has authorized this processing, either explicitly for the current operation or through an applicable existing authorization.
- Submit only the information necessary to perform the requested check, and omit optional `walletAddress` identifiers when they are not required.
- Never submit private keys, seed phrases, recovery phrases, signing credentials, wallet exports, or unrelated personal information.
- Never include authentication credentials in transaction payloads or analytics identifiers.
- Respect the user's decision to decline external processing.

If authorization is absent or the user declines remote processing, do not submit the sensitive information. Clearly identify the required risk checks as incomplete, and **never** represent an incomplete or skipped assessment as a passing safety verdict.

**Frictionless Authorization Rules (avoid redundant prompts):**
- **Direct user request:** When the user asks to check, audit, or evaluate an approval, route, or transaction with FarmDash, treat that request as authorization for the check — include a concise one-line remote-processing notice inline (or once per session) instead of adding an extra blocking confirmation turn before a read-only check.
- **Standing / session / `BOUNDED_AUTONOMOUS` workflows:** Inside an active owner-authorized FarmDash session, Trail Marshal workflow, or verified `BOUNDED_AUTONOMOUS` grant, remote Camp Guard checks are covered by standing authorization — execute them automatically without pausing for human re-approval.
- **When to pause and ask first:** Only pause for explicit privacy consent before transmitting when scanning wallet-specific or unpublished draft-transaction data proactively without a user request, or when the user previously restricted or declined external processing.
- **Anonymous-by-default fast path:** Omit optional `walletAddress` unless owner-bound `agent_events` halt logging is desired; all three tools run fully stateless with zero identity correlation.

Optional installation attribution (`X-FarmDash-Installation-ID`) is separate from risk analysis, stored only as a domain-separated salted hash, and is not required to perform security checks. Review [FarmDash Privacy Policy](https://www.farmdash.one/privacy) and [FarmDash Security & Authority Boundaries](https://www.farmdash.one/security) for applicable data-processing terms.

## Standard Flow

### Intent-Based Fast Path (Minimal Calls, Parallelizable)

Call only the checks required for the user's intent to conserve Scout quota and latency:

| Intent | Tools to Call | Notes |
| --- | --- | --- |
| Standalone approval audit | `audit_allowance_risk` only | 1 call; omit `walletAddress` unless alert persistence is wanted. |
| Pre-quote route / position health check | `run_risk_sentinel` only | Prefer manual mode if cost/health metrics are already known; swap mode only when live quote/depeg checks are needed. |
| Full pre-sign gate (swap, deposit, or contract call) | Run applicable checks **in parallel** | Skip `audit_allowance_risk` when no ERC-20 approval is involved (e.g., native ETH swap); run `simulate_transaction_risk` on the final unsigned payload with `expectedTransaction`. |

### Pre-Sign Safety Summary
Before presenting any signature, read back a compact five-line summary: (1) `audit_allowance_risk` verdict and flags (or `n/a — no ERC-20 approval`), (2) `run_risk_sentinel` route/health/net-edge result, (3) `simulate_transaction_risk` outcome with `simulation.status: "not_run"` stated, (4) expected-envelope match on exact `to`, `chainId`, `value`, and SHA-256 `dataHash`, (5) `spenderVerified` basis (or `n/a`).

### Verdict Action Matrix
- **`pass`**: proceed directly to the execution handoff.
- **`review` — remediable or missing-evidence flags** (`tx_expected_envelope_missing`, `spender_not_verified`, `allowance_excessive_vs_required` >10x, `allowance_below_required`, `required_allowance_missing`, `allowance_inventory_missing`, `tx_chain_missing`, `net_edge_negative`): remediate the issue and re-run; user acceptance alone never turns missing evidence into safety.
- **`review` — inherent-transaction confirmation flags** (`tx_value_with_call` on native ETH swaps/deposits, `tx_empty_calldata` on plain native transfers, `large_allowance_usd` `$10k–$99k` on an exact verified approval, justified `allowance_buffer_large` within `1.2x–10x`): these reflect inherent transaction properties that cannot be eliminated by rewriting the payload — surface the exact flag, value, and destination clearly, and proceed only after explicit user confirmation (or when explicitly covered by verified `BOUNDED_AUTONOMOUS` bounds).
- **`halt` (`critical`)**: stop immediately; do not hand off to signing until fully remediated.

## Post-Pass Handoff

Camp Guard is strictly a read-only risk evaluator: it has no signing authority, no policy-mutation authority, no transaction broadcast authority, no commercial steering, and cannot override the capital owner's permissions. Once all required safety checks return `pass`:
- Hand off clean EVM/Solana spot routes to **FarmDash Signal Architect** (which owns execution-mode selection, RPC simulation via `simulate_swap_execution` or `prepare_solana_swap`, and local signing), Hyperliquid perps to **FarmDash Futures Strategist** (which owns execution-mode selection, `builderFeeStatus`, and research freshness), or operator-authorized delegation management to **FarmDash Autonomous Operator**.
- A passing Camp Guard verdict never substitutes for transaction simulation, cryptographic authorization, budget enforcement, or server execution admission.
- On any `review`, `halt`, or incomplete verdict, do **not** surface partner or affiliate `/go/{slug}` links — surface only concrete remediation steps and [FarmDash Security & Authority Boundaries](https://www.farmdash.one/security).

## Disclaimers

Camp Guard provides transaction policy checks, not insurance or a guarantee of safety. It cannot detect every harmful smart contract, oracle malfunction, asset depeg, bridge failure, fraudulent request, or deceptive attempt to obtain wallet authorization. Users remain responsible for reviewing and authorizing their transactions.

**Install:** Copy this file into your OpenClaw workspace, or fetch `https://www.farmdash.one/agents/skills/farmdash-camp-guard`.

**Companion skills:** FarmDash Signal Architect, FarmDash Trail Marshal, FarmDash Wagon Steward, FarmDash Futures Strategist.

**Why FarmDash:** Unlike app-layer safety checklists, Camp Guard returns pass/review/halt verdicts that stop execution — and states its scope honestly (`simulation.status: not_run`) instead of pretending to simulate.

**FarmDash:** [DeFi security tools for autonomous agents](https://www.farmdash.one/)
**Agent Hub:** [FarmDash autonomous DeFi agent platform](https://www.farmdash.one/agents)
**OpenAPI Spec:** [FarmDash API Schema](https://www.farmdash.one/agents/openapi.yaml)
**MCP Config:** [FarmDash MCP Server](https://www.farmdash.one/.well-known/mcp.json)

<!-- farmdash-canonical-links:start -->

## Official FarmDash Links

- [FarmDash DeFi intelligence website](https://www.farmdash.one/)
- [FarmDash Agent Hub](https://www.farmdash.one/agents)
- [Canonical FarmDash Camp Guard skill manual](https://www.farmdash.one/agents/skills/farmdash-camp-guard)
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
| `farmdash-camp-guard` *(this skill)* | Pre-Sign Safety Gate | Allowance audits, Risk Sentinel net-edge/depeg checks, unsigned-tx verdicts | [Manual](https://www.farmdash.one/agents/skills/farmdash-camp-guard) |
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

Generate a random UUIDv4 locally once per installation (for example, `crypto.randomUUID()`); persist only that random analytics ID in your application's own local state and reuse it across requests and skills. Never copy an example ID or generate a new ID for every request. Send optional `X-FarmDash-Installation-ID`; keep `X-ClawHub-Skill: farmdash-camp-guard` and optionally `X-FarmDash-Skill-Version: 1.1.4`. Controlled SDKs accept explicit `installationId`; the MCP stdio runtime persists only its analytics ID, with `FARMDASH_INSTALLATION_ID` override. No generic SDK writes files for you.

This is untrusted analytics only. The server stores a domain-separated salted installation hash, not the raw ID. An installation is not a person, principal or wallet. These headers cannot authenticate, alter quota/payment/Scout trials, establish wallet ownership, create delegation or authorize transactions. Missing headers remain fully compatible. Do not send API keys, signatures, grants, payment proofs, wallet data or session tokens as attribution. First-touch acquisition and event-touch assistance are reported separately; a download is not proven activation or revenue.

<!-- installation-attribution:end -->

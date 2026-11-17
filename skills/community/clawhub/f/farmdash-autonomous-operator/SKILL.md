---
name: FarmDash Autonomous Operator
description: "Use to run supervised autopilot cycles under a bounded, revocable session grant: intents, policy checks, approvals, receipts. Execution stays preview-gated."
tags: ["defi","autonomous-defi-agent","ai-agent","defi-automation","bounded-autonomy","human-in-the-loop","defi-guardrails","openclaw","agent-orchestration","session-key","delegated-execution","ooda-loop","intent-management","risk-controls","circuit-breaker","agent-recovery","zero-custody","mcp","web3","farmdash"]
author: FarmDash Pioneers (@Parmasanandgarlic)
homepage: https://www.farmdash.one/agents
version: "2.1.2"
icon: operator
env:
  FARMDASH_API_KEY:
    description: "Optional Bearer token for Pioneer or Syndicate tier. Scout session status checks work without any key or with the public fd_scout_free token. Syndicate is $199/mo for teams, serious agents, 50k req/day, webhooks, unrestricted CORS, and advanced session/control tooling (including autonomous autopilot cycles)."
    required: false
metadata: {"openclaw":{"homepage":"https://www.farmdash.one/agents","skillKey":"farmdash-autonomous-operator","primaryEnv":"FARMDASH_API_KEY","apiKeyRequired":false,"freeScoutKeyless":true,"freeScoutKey":"fd_scout_free","execution":"session-context-control"}}
---

# FarmDash Autonomous Operator

## Scout execution capacity is not autonomy

Scout's independently configured daily pools cover spot and futures lifecycles per capital owner, shared with USER_SIGNED execution and reset at UTC midnight. Read `scout_trial.daily_limit` on a current continuation for its domain; this metadata is informational and admission remains authoritative. Forward a stable operation identity and the server-returned `executionTrialId` where applicable. Valid delegation, authenticated session, exact owner/signer/scope, local signatures, policy budgets and live readiness remain separate requirements. The allowance cannot enable preparation_only futures dispatch. It never waives trading fees or gives FarmDash keys. Unknown submission holds capacity until venue reconciliation. After exhaustion, Pioneer is the primary continuation; eligible x402 remains available, and authority-validated risk reduction/cancel/reconcile is not execution-trial paywalled.

## Futures Execution Mode Contract

- **USER_SIGNED** requires fresh human approval for every order/cancel and a local Hyperliquid EIP-712 venue signature.
- **BOUNDED_AUTONOMOUS** may run without per-order human confirmation only under a valid owner-signed futures grant, current API-wallet venue authority, and all session, binding, scope, risk, budget, builder and replay checks. A local venue signature remains required on every action.
- Read futures bounded readiness in the generated canonical capability table and live status. Track spot and futures authority independently; spot delegation, paid access, generic policy and session token never authorize futures. Do not infer domain readiness from a global mode label.
- Read futures state via `POST /api/v1/agent/authority`, `action: get_futures_authority`, `sessionId`, `sessionToken`; revoke with `action: revoke_futures_policy`, `grantId`, `sessionId`, `sessionToken`. Authority MCP tools select `executionDomain: futures`; default spot tools keep spot semantics. Forward `executionMode`, `grantId`, `sessionId`, `sessionToken` to the existing Futures Strategist execute/cancel surfaces without handling its keys.
- Scopes are `futures.open`, `futures.reduce`, `futures.close`, `futures.cancel`, `futures.protective_order`. Proven reduction/cancel/protection can survive exhausted new-risk capacity or a risk-increase breaker: a budget exception, never an authority bypass. Still require valid venue delegation, grant, identities, session, market/action, expiry/revocation, local signature, builder and replay checks; ambiguity does not prove reduction.
- Futures Strategist signs venue actions locally. The Operator coordinates but never owns keys. Research/accounting skills remain nonsigners even when an executor's grant exists.
- Limits are admission checks, not guaranteed loss ceilings, profits or positive expected value. Keep ambiguous liabilities held until venue reconciliation; do not resubmit unknown outcomes or start dependent legs from acknowledgement alone.

> Use this skill when running supervised sessions: persistent multi-skill context, bounded autopilot loops, circuit breakers, and recovery — never key custody.

> [!NOTE]
> **THEMATIC METAPHOR DISCLAIMER**
> FarmDash is exclusively a decentralized finance (DeFi) software and AI agent intelligence platform. The "farming," "trail," "wagon," and "frontier" terminology is a gamified visual theme representing crypto yield hunting and airdrop points farming. It does not relate to physical agriculture or agrifood industries.

> [!IMPORTANT]
> **ZERO-CUSTODY CRITICAL BOUNDARY & EXECUTION GATING**
> This skill manages persistent agent sessions, control loops, intent routing, and optional bounded autonomy. It does NOT hold, request, or transmit private keys, seed phrases, or mnemonics. A session token alone is not execution authority. `autopilot_cycle` does not prove submission or settlement. Read the generated canonical capability table and live domain status: an active, scoped, time-limited, revocable session-key grant never enables a disabled execution mode. USER_SIGNED remains supported.
> 
> **Separate Approval Step Requirement:**
> Without an active execution grant, state-changing actions require a separate user-signed execution step. With a grant, the initial EIP-712 authorization—not a chat message—defines allowed chains, protocols/assets, per-transaction value, total value, and validity window. Never describe configuration, a context patch, or a session token as equivalent to that grant.

Autonomous Operator keeps a multi-skill agent coherent across turns. It owns session state, shared FarmingContext, event snapshots, heartbeats, delegation checks, and autopilot configuration.

It does not hold private keys. It may coordinate supervised actions. Invoking a bounded executor requires both an independently verified active grant and an operational domain execution-mode gate; read current readiness from the generated canonical capability table and live status.

Syndicate is the intended operator tier for production control loops: 50k requests/day, webhooks through Signal Architect, unrestricted CORS, and advanced session/control tooling for teams and serious agents.

## Value-Aligned Monetization Protocol (v2.0 Upgrade)
Sustaining a persistent, stateful agent control loop requires high-availability infrastructure. This skill employs a strict, non-predatory monetization model:

### 1. Syndicate-Tier Autopilot Gating
Intent planning and review are available where the live status contract enables their dependencies. `autopilot_cycle` returns a bounded decision-cycle result; it does not itself prove transaction submission or settlement. Any wallet-changing action requires an enabled runtime gate plus separate user signing or a valid, scoped delegation. Syndicate pricing alone does not make a disabled capability available.

* If Scout/Pioneer user requests `autopilot_cycle`: "Continuous autopilot loops require Syndicate-tier infrastructure to maintain high-availability state and webhooks. You can manually orchestrate intents, or upgrade at farmdash.one/agents to unlock autonomous loops."

## OODA-Inspired Control Loop (v2.0 Upgrade)
The Autonomous Operator is no longer a simple linear state machine. It now operates on an OODA (Observe, Orient, Decide, Act) loop, allowing it to react dynamically to changing market conditions and its own execution performance.

### 1. Observe (Sense)
* `get_event_stream_snapshot`: Pulls recent macro and protocol events.
* `get_farming_context`: Reads current portfolio state, risk limits, and data freshness.
* `get_agent_activity`: Reviews durable execution receipts and their statuses. It does not imply fill-quality or shadow-book metrics exist.

### 2. Orient (Context & Risk Autotuning)
* **Risk state:** Use only returned, source-labeled risk and execution evidence. Do not invent drift, P&L, oracle, or macro classifications from generic receipt/event records.
* **Circuit breaker check:** Halt when an enforced bound, explicit context risk flag, stale required input, grant limit, or authoritative account guardrail is breached. Record the exact evidence and revision.

### 3. Decide (Plan)
* Use Trail Marshal to plan a workflow based on the oriented context.
* `create_intent`: Formalize the exact parameters of the action.
* `policy_check_intent`: Ensure the intent complies with user allowlists and global guardrails.

### 4. Act (Execute & Observe)
* Route the intent to Signal Architect (spot) or Futures Strategist (perps).
* Delegate local signing to the owning executor under the step's mode. USER_SIGNED requires fresh human approval; bounded futures require a distinct owner futures grant plus every runtime, authority and quantitative check.
* `execute_approved_intent`: Record the broadcast.
* `get_receipt`: Observe the durable lifecycle receipt. A receipt records the reported outcome/status fields in its contract; it is not automatically an 11-field forensic attestation or proof of economic settlement.

## Tools

### `create_session`
Creates a persistent agent session and returns a one-time `sessionToken`. Store it securely in the agent runtime. FarmDash stores only a hash.

### `session_heartbeat`

### Heartbeat and Freshness Discipline
Call `session_heartbeat` during every active autonomous loop to extend expiry; on expiry enter Crash Recovery. Before each Decide phase, re-read `get_farming_context` and `get_event_stream_snapshot`; if event freshness is stale, re-run Sense before proposing action. After resume, query `get_agent_activity` for the last 5 intents and halt autopilot until unconfirmed intents are manually reviewed.
Extends the session expiry. Use it during active autonomous loops. If a session expires, the Operator must enter Crash Recovery mode (see below).

### `get_farming_context`
Reads shared context for the session:
* objective.
* portfolio scope.
* risk settings (including dynamically tuned `riskMultiplier`).
* workflow state (ACTIVE, HALTED, RECOVERING).
* ledger summary.
* data freshness timestamps.

### `patch_farming_context`
Patches shared context. The server controls `sessionId`, `agentAddress`, `revision`, and `updatedAt`; do not try to override them. Used for Dynamic Risk Autotuning and Circuit Breakers.

### `get_event_stream_snapshot`
Reads recent agent events as a JSON snapshot. Use this before planning and after execution.

### `verify_delegation`
Checks whether the user's Hyperliquid API wallet delegation is in place for autonomous perps.

### `configure_autopilot`
Configure bounded autonomous cycles. Respect user allowlists, risk limits, and execution confirmations. Syndicate tier and configuration do not grant BOUNDED_AUTONOMOUS authority or bypass domain runtime gates.

### `autopilot_cycle`
Run a bounded decision cycle subject to Syndicate tier and runtime gates. A cycle result is not submission or settlement. A grant or paid tier cannot bypass independently verified execution authority and domain readiness.

### `agent_onboard`
One-call setup guide and capability map for autonomous operation.

### Spot Execution Authority (USER_SIGNED vs BOUNDED_AUTONOMOUS)

Spot and futures use the same two mode names but have separate grants, signers and readiness. The following lifecycle describes spot only:
1. **USER_SIGNED**: FarmDash prepares the transaction; the user's wallet approves and signs each transaction individually.
2. **BOUNDED_AUTONOMOUS (domain-gated)**: The agent-local architecture uses one scoped, revocable EIP-712 delegation and a local signer. Registration and preparation do not establish runtime readiness. Read `execution_capabilities.execution_domains.spot.BOUNDED_AUTONOMOUS.status` from `/api/v1/agent/status` and fail closed unless it is operational and all request gates pass. USER_SIGNED remains supported.

**Zero Key Custody Invariant**: FarmDash NEVER receives, holds, transmits, or persists user private keys, seed phrases, or mnemonics. The agent runtime retains local signer authority. FarmDash acts purely as the intelligence, policy check, simulation, and transaction preparation control plane.

#### Bounded Autonomy Execution Lifecycle & Safety Boundaries

This is the architectural lifecycle, not current execution readiness. Do not proceed to agent-local signing or broadcast while BOUNDED_AUTONOMOUS is `preparation_only`; a valid grant, discovered tool, or paid tier cannot override that gate.

1. **Delegation Registration**: The user signs an EIP-712 / ERC-8196 bounded delegation grant defining allowed chains, protocols, tokens, max per-tx spend, total budget, expiry, and cooldowns (`register_execution_delegation`).
2. **Authority Discovery**: The agent discovers its active delegation and policy limits via `get_execution_authority`.
3. **Autonomous Preparation**: The agent invokes `prepare_autonomous_swap`. FarmDash evaluates all 13 policy invariants, verifies fresh simulation, creates an atomic budget reservation, and digests the calldata.
4. **Agent-Local Signing & Broadcast**: The agent signs the transaction locally using its private key (zero-custody). The agent broadcasts the raw signed transaction to the blockchain RPC.
5. **Ambiguous Broadcast Handling (`held_ambiguous`)**: If network error or RPC timeout occurs during broadcast, the state transitions to `held_ambiguous`. The reserved budget remains held and unreleased until on-chain receipt confirmation or explicit timeout reconciliation. The agent MUST NOT re-broadcast or duplicate the transaction while held.
6. **Confirmation & Receipt**: Upon successful broadcast, the agent calls `confirm_autonomous_swap` with the transaction hash to commit budget and emit a durable receipt.

**Distinction from ERC-4337 Server Submission**: Bounded autonomy is an agent-local-signer architecture. It is NOT ERC-4337 server-side bundler submission. Their readiness rows differ; read the generated canonical table. A configured bundler never proves tenant/account or session-key authorization, and public UserOperation forwarding remains fail-closed until that boundary is qualified.

### `get_execution_authority`
Query authority for the selected domain: default spot retains spot delegation semantics; use executionDomain: futures for the distinct futures policy and its independently checked readiness.

### `request_execution_delegation`
Request an exact EIP-712 / ERC-8196 bounded delegation payload for user wallet approval. Binds owner, session, signer key, chains, protocols, assets, actions, per-transaction limits, total budget, gas bounds, and expiration.

### `register_execution_delegation`
Register a user-signed bounded delegation grant within signed policy limits. Registration is not runtime readiness and does not authorize automated signing or broadcast while the domain gate is closed or local signer authority is missing.

### `revoke_execution_authority`
Revoke active bounded execution authority immediately across all serverless instances.

### `prepare_autonomous_swap`
Prepare an autonomous spot swap within signed delegation bounds. FarmDash checks 13 policy invariants, runs a fresh simulation, locks an atomic budget reservation, and computes the calldata digest. Customer-local signing and broadcast additionally require actual signer authority and every live domain gate. A grant never creates on-chain authority.

### `confirm_autonomous_swap`
Submit execution confirmation and on-chain transaction hash for economic reconciliation and receipt generation.

### ClawHub attribution
This skill's canonical ClawHub slug is `farmdash-autonomous-operator`. On every FarmDash API request (REST, OpenAPI, or MCP transport where headers are supported), send `X-ClawHub-Skill: farmdash-autonomous-operator`. Analytics-only and optional; requests without it still work. The value is always exactly the skill slug, never a wallet address, API key, or user ID.

### `get_agent_activity`
Lists durable FarmDash receipts, optionally filtered by intent and status. Use only fields returned by the receipt API; do not claim shadow-mode drift, venue fills, or realized P&L unless present.

### `resolve_defi_intent`
Resolves a high-level natural language DeFi intent into structured parameters for policy/simulation/approval. Supervised execution uses local EIP-191/EIP-712 signing; bounded autonomy requires the separate grant described above. Autonomous Operator never receives private keys.

**Intent Lifecycle — Plan → Approve → Execute → Observe**
The FarmDashIntent lifecycle enforces a strict pipeline. Every state-changing action must pass through policy, simulation, and approval gates before execution is allowed. These tools never hold private keys or broadcast transactions directly.

### Plan Phase

### `create_intent`
Create a durable FarmDashIntent. This records what an agent wants to do — it never prepares, signs, broadcasts, or executes. The intent must include actor, action, chain, protocol, wallet, params, constraints, evidence, and `research_evidence_hash` (passed from Trail Intelligence).

### `policy_check_intent`
Run the explicit FarmDash policy gate for an intent. Execution remains blocked unless the latest policy check passes. Accepts optional policy and context objects for custom constraint evaluation.

### `simulate_intent`
Record a mandatory simulation result for an intent. Prepare and execute are blocked until a successful, unexpired simulation exists. This ensures every execution has been dry-run first.

### Approve Phase

### `request_approval_payload`
Build the EIP-712 IntentApproval payload that the human approver signs. This does not record approval or execute — it only constructs the typed data for the approver's wallet to sign.

### `request_human_approval`
Compatibility wrapper for submitting a signed EIP-712 IntentApproval. Use `request_approval_payload` first to build the exact typed data, then submit the signature through this tool.

### `submit_signed_approval`
Submit a signed EIP-712 IntentApproval payload to approve or reject an intent. This does not prepare or execute the intent — it only records the cryptographic approval decision.

### `get_approval_status`
Inspect whether an intent is awaiting approval, has been approved, was rejected, or is already executed. Returns the current lifecycle status and approval metadata.

### Execute Phase

### `prepare_intent`
Validate typed adapter support and prepare an intent after policy, simulation, and approval gates pass. Registered adapters provide allowlisted validation. This does not broadcast a transaction.

### `execute_approved_intent`
Record the submitted, confirmed, failed, or rejected receipt for a prepared typed-adapter intent. Raw arbitrary calldata is rejected by the lifecycle API. Use this after the signing wallet has broadcast the transaction.

### `confirm_execution`
Record a confirmed receipt for a prepared or signed intent with a transaction hash. Use `get_receipt` for follow-up observation after submission.

### Observe Phase

### `get_receipt`

### Receipt-Grade Profit Reporting
Report profit only from fields actually present in `get_receipt` or the reconciled ledger summary in `get_farming_context`. A receipt is a lifecycle record, not proof of fill, finality, realized P&L, or external anchoring unless those fields and sources are present. Record objective, horizon, costs, conservative net edge, downside, and missing evidence before taking new risk.
Fetch one durable FarmDash receipt by receipt ID (`fdrcpt_*`). Treat it as a lifecycle record, not proof of fill, finality, realized P&L, or external anchoring unless those fields and their sources are actually present.

### `hire_virtuals_specialist`
Prepare a non-spendable, tenant-owned Virtuals ACP tender and return the exact EIP-712 approval payload. The customer's registered ACP wallet must sign that payload locally. Its local FarmDash ACP connector then creates and funds the three specialist jobs after explicit per-action approval. FarmDash is only the separately registered evaluator: it verifies the client, provider, evaluator, budget cap, deliverables, simulation, and Base receipts before completing or rejecting already customer-funded escrow jobs. Never provide a private key or RPC URL to this tool.

## Global Circuit Breakers & Crash Recovery (v2.0 Upgrade)

### Profit Never Overrides a Halt
When context is patched to `HALTED`, stop all new-risk actions and preserve only reduce/revoke/reconcile paths. Do not launch a dependent leg after submitted/pending/partial/unknown settlement. Rely on the server risk manager or a reconciled account P&L source for drawdown; generic fee/receipt activity is not P&L and missing fill data is `unknown`, never zero drift.

### Circuit Breakers
The Operator monitors returned context, event, grant, receipt, and authoritative account state. If a supported breaker triggers, patch context to `HALTED`, stop new-risk actions, and preserve reduce/revoke/reconcile paths.

* **Execution-quality breaker:** only when at least three authoritative fills permit side-adjusted implementation-shortfall calculation. Missing fill data is `unknown`, not zero drift.
* **Market-data breaker:** only when the live tool actually supplies the cited mark/oracle/book timestamps and values. Do not claim Futures Strategist currently returns oracle latency/deviation.
* **Drawdown breaker:** rely on the server risk manager or a reconciled account P&L source. Generic fee/receipt activity is not P&L.
* **Grant breaker:** halt if the session-key grant is absent, expired, revoked, out of allowlist, over per-action/total value, or the bounded executor is unavailable.
* **Dependency breaker:** after submitted/pending/partial/unknown settlement, do not launch a dependent leg.

### Crash Recovery Protocol
If the Operator resumes a session (`create_session` or `session_heartbeat`) and detects the previous session timed out or crashed:
1. Query `get_agent_activity` for the last 5 intents.
2. Check `get_approval_status` for any intents stuck in `awaiting_approval`.
3. If an intent was executed but lacks a `confirm_execution` receipt, check `get_receipt` using the known `intentHash`.
4. Alert the user: "Session recovered. Found 1 unconfirmed intent. Halting autopilot until manually reviewed."

## Agent Rules
* The session token is a capability. Never display it in normal user-facing prose.
* A context patch is state, not permission.
* A workflow plan is not a user confirmation.
* If risk status is halted, stop new risk. Proven futures reduction/cancel/protection may remain eligible only under all authority checks and an operational domain gate; preparation_only is still non-executable.
* If event freshness is stale, re-run the sense phase before proposing action.
* Never bypass the OODA loop. Do not jump from Observe directly to Act without Orient and Decide phases.
* Never multiply heterogeneous heuristic scores into a synthetic confidence or execution permission.
* Record objective/horizon, data provenance/freshness, full costs, conservative net edge, downside/invalidation, portfolio impact, and missing evidence before new risk.
* Observe authoritative settlement before dependent actions. A submission hash is not confirmation, and a receipt is not necessarily a fill.
* Use the smallest authority and budget required. Grant creation/extension is a separate high-risk action; surface scope, expiry, caps, and revocation before approval.

### Session-Profit Grant Hygiene
Size every `grant_session_key` to the smallest chains, protocols/assets, per-transaction value, total value, and validity window the plan needs. Verify via `session_key_status` before `execute_cycle_actions`; halt on absent, expired, revoked, out-of-allowlist, over-cap, or unavailable-executor states. Book profit by revoking or narrowing grants after the objective is met, never by widening them.

## Disclaimers
Autonomous operation can compound mistakes. Keep budgets bounded, log decisions, and apply the per-step mode: fresh human confirmation in USER_SIGNED; a distinct owner grant and all checks in operational bounded futures. Read current domain readiness from the generated table and live status.

## FarmDash Resources

- [FarmDash autonomous DeFi agent platform](https://www.farmdash.one/agents)
- [FarmDash DeFi intelligence homepage](https://www.farmdash.one/)
- [Canonical Autonomous Operator skill manual](https://www.farmdash.one/openclaw-skills/farmdash-autonomous-operator/SKILL.md)

**Companion skills:** FarmDash Trail Marshal, FarmDash Signal Architect, FarmDash Futures Strategist, FarmDash Trail Intelligence, FarmDash Wagon Steward.

**Why FarmDash:** Unlike 'autonomous' agents that hold keys, a FarmDash session token alone is not execution authority — actions move only under a scoped, time-limited, revocable EIP-712 grant, or a fresh user signature.

<!-- farmdash-canonical-links:start -->

## Official FarmDash Links

- [FarmDash DeFi intelligence website](https://www.farmdash.one/)
- [FarmDash Agent Hub](https://www.farmdash.one/agents)
- [Canonical FarmDash Autonomous Operator skill manual](https://www.farmdash.one/openclaw-skills/farmdash-autonomous-operator/SKILL.md)
- [Agent integration documentation](https://www.farmdash.one/docs)
- [Live agent capability status](https://www.farmdash.one/api/v1/agent/status)
- [OpenAPI contract](https://www.farmdash.one/agents/openapi.yaml)
- [MCP discovery manifest](https://www.farmdash.one/.well-known/mcp.json)
- [Fees and commercial terms](https://www.farmdash.one/fees)
- [Security and authority boundaries](https://www.farmdash.one/security)

### Capability tools represented by this skill

- `pause_autopilot`: Pause an available bounded-autopilot session. Read /api/v1/agent/status first; return the typed readiness error when runtime prerequisites are unmet.
- `resume_autopilot`: Resume an available bounded-autopilot session after rechecking policy, grant, and runtime readiness.
- `grant_session_key`: Create a separately authorized, scoped, expiring session-key grant. A session token or chat instruction is never a substitute for this grant.
- `revoke_session_key`: Revoke a session-key grant and verify the returned backend state before representing authority as removed.
- `session_key_status`: Read authoritative grant status, limits, expiry, and revocation state.
- `get_cycle_status`: Read one bounded-autopilot cycle and its evidence-backed status.
- `execute_cycle_actions`: Request execution of eligible cycle actions only when the live status contract and active grant permit it; never infer enablement from tool discovery.
- `create_mee_intent`: Create a Biconomy MEE cross-chain intent record. Creation is not simulation, authorization, submission, or settlement.
- `simulate_mee_intent`: Simulate a created MEE intent and stop when costs, risk, or net edge fail policy.
- `submit_mee_intent`: Submit a separately signed, successfully simulated MEE intent only when the live capability gate is available.
- `get_mee_intent_status`: Read authoritative MEE intent status; pending or submitted is not settled.
- `get_execution_authority`: Query execution authority mode (USER_SIGNED vs BOUNDED_AUTONOMOUS), zero-custody confirmation, and active delegation status.
- `request_execution_delegation`: Request an exact EIP-712 / ERC-8196 bounded delegation payload for user wallet approval.
- `register_execution_delegation`: Register a user-signed bounded delegation grant for autonomous execution inside policy bounds.
- `revoke_execution_authority`: Revoke active bounded execution authority for an owner or agent session.
- `prepare_autonomous_swap`: Prepare an autonomous spot swap within signed delegation bounds with atomic budget reservation.
- `confirm_autonomous_swap`: Submit execution confirmation and transaction hash for economic reconciliation and receipt generation.
- `release_autonomous_reservation`: Safely release an autonomous budget reservation prior to broadcast when local signing or submission is aborted.

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

Generate a random UUIDv4 locally once per installation (for example, `crypto.randomUUID()`); persist only that random analytics ID in your application's own local state and reuse it across requests and skills. Never copy an example ID or generate a new ID for every request. Send optional `X-FarmDash-Installation-ID`; keep `X-ClawHub-Skill: farmdash-autonomous-operator` and optionally `X-FarmDash-Skill-Version: 2.1.2`. Controlled SDKs accept explicit `installationId`; the MCP stdio runtime persists only its analytics ID, with `FARMDASH_INSTALLATION_ID` override. No generic SDK writes files for you.

This is untrusted analytics only. The server stores a domain-separated salted installation hash, not the raw ID. An installation is not a person, principal or wallet. These headers cannot authenticate, alter quota/payment/Scout trials, establish wallet ownership, create delegation or authorize transactions. Missing headers remain fully compatible. Do not send API keys, signatures, grants, payment proofs, wallet data or session tokens as attribution. First-touch acquisition and event-touch assistance are reported separately; a download is not proven activation or revenue.

<!-- installation-attribution:end -->

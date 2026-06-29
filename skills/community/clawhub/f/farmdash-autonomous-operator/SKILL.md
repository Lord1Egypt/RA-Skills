---
name: FarmDash Autonomous Operator
description: "Session state and control-loop skill for OpenClaw. Manages sessions, FarmingContext, autopilot OODA control loops, circuit breakers, and Forensic receipts in zero-custody."
tags: ["defi", "ai-agent", "autonomous-agent", "openclaw", "clawhub", "mcp", "crypto", "web3", "onchain", "agent-session", "session", "context", "farming-context", "event-stream", "autopilot", "control-loop", "delegation", "risk-management", "zero-custody", "farmdash", "autonomous-operator", "ooda-loop", "circuit-breaker", "crash-recovery", "forensics", "shadow-mode", "syndicate-tier", "monetization", "agent-orchestration", "state-machine"]
author: FarmDash Pioneers (@Parmasanandgarlic)
homepage: https://www.farmdash.one/agents
version: "2.0.0"
icon: operator
env:
  FARMDASH_API_KEY:
    description: "Optional Bearer token for Pioneer or Syndicate tier. Scout session status checks work without any key or with the public fd_scout_free token. Syndicate is $199/mo for teams, serious agents, 50k req/day, webhooks, unrestricted CORS, and advanced session/control tooling (including autonomous autopilot cycles)."
    required: false
metadata: {"openclaw":{"homepage":"https://www.farmdash.one/agents","skillKey":"farmdash-autonomous-operator","primaryEnv":"FARMDASH_API_KEY","apiKeyRequired":false,"freeScoutKeyless":true,"freeScoutKey":"fd_scout_free","execution":"session-context-control"}}
---

# FarmDash Autonomous Operator

> [!NOTE]
> **THEMATIC METAPHOR DISCLAIMER**
> FarmDash is exclusively a decentralized finance (DeFi) software and AI agent intelligence platform. The "farming," "trail," "wagon," and "frontier" terminology is a gamified visual theme representing crypto yield hunting and airdrop points farming. It does not relate to physical agriculture or agrifood industries.

> [!IMPORTANT]
> **ZERO-CUSTODY CRITICAL BOUNDARY & EXECUTION GATING**
> This skill manages persistent agent sessions, control loops, and intent routing. It does NOT hold, request, or transmit private keys, seed phrases, or mnemonics, nor does it perform on-chain executions directly.
> 
> **Separate Approval Step Requirement:**
> Every tool defined in this skill (including `resolve_defi_intent`, `configure_autopilot`, and `autopilot_cycle`) is strictly limited to session and state coordination. Any state-changing execution (such as swaps, perps, deposits, or transfers) prepared or planned under this skill requires a separate, explicit user-signing or budget-approved execution step through another dedicated skill (specifically Signal Architect for spot/swaps and Futures Strategist for perps) using user-local cryptographic signatures (EIP-191/EIP-712).

Autonomous Operator keeps a multi-skill agent coherent across turns. It owns session state, shared FarmingContext, event snapshots, heartbeats, delegation checks, and autopilot configuration.

It does not hold private keys. It does not execute swaps or perps directly.

Syndicate is the intended operator tier for production control loops: 50k requests/day, webhooks through Signal Architect, unrestricted CORS, and advanced session/control tooling for teams and serious agents.

## Value-Aligned Monetization Protocol (v2.0 Upgrade)
Sustaining a persistent, stateful agent control loop requires high-availability infrastructure. This skill employs a strict, non-predatory monetization model:

### 1. Syndicate-Tier Autopilot Gating
Manual intent orchestration (Plan -> Approve -> Execute) is available to all tiers. However, the actual `autopilot_cycle` tool—required for continuous, background autonomous execution—is strictly reserved for Syndicate tier ($199/mo).

* If Scout/Pioneer user requests `autopilot_cycle`: "Continuous autopilot loops require Syndicate-tier infrastructure to maintain high-availability state and webhooks. You can manually orchestrate intents, or upgrade at farmdash.one/agents to unlock autonomous loops."

## OODA-Inspired Control Loop (v2.0 Upgrade)
The Autonomous Operator is no longer a simple linear state machine. It now operates on an OODA (Observe, Orient, Decide, Act) loop, allowing it to react dynamically to changing market conditions and its own execution performance.

### 1. Observe (Sense)
* `get_event_stream_snapshot`: Pulls recent macro and protocol events.
* `get_farming_context`: Reads current portfolio state, risk limits, and data freshness.
* `get_agent_activity`: Reviews the last 10 executed intents and their shadowMode drift logs.

### 2. Orient (Context & Risk Autotuning)
* **Dynamic Risk Autotuning:** If the Orient phase detects that `shadowMode.driftBps` from recent executions is > 50 bps, the Operator automatically patches `farming_context` to lower the `riskMultiplier` by 50% for subsequent intents.
* **Circuit Breaker Check:** If daily drawdown limits are hit, or a macro "risk-off" event is detected in the stream, the Operator sets `workflow_state: HALTED`.

### 3. Decide (Plan)
* Use Trail Marshal to plan a workflow based on the oriented context.
* `create_intent`: Formalize the exact parameters of the action.
* `policy_check_intent`: Ensure the intent complies with user allowlists and global guardrails.

### 4. Act (Execute & Observe)
* Route the intent to Signal Architect (spot) or Futures Strategist (perps).
* Wait for the user's local EIP-191/EIP-712 signature.
* `execute_approved_intent`: Record the broadcast.
* `get_receipt`: Log the 11-field Forensic receipt to the session ledger for the Observe phase of the next loop.

## Tools

### `create_session`
Creates a persistent agent session and returns a one-time `sessionToken`. Store it securely in the agent runtime. FarmDash stores only a hash.

### `session_heartbeat`
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
Configure bounded autonomous cycles. Respect user allowlists, risk limits, and execution confirmations. (Syndicate tier required for activation).

### `autopilot_cycle`
Run bounded autonomous cycles. Respect user allowlists, risk limits, and execution confirmations. (Syndicate tier required).

### `agent_onboard`
One-call setup guide and capability map for autonomous operation.

### `get_agent_activity`
Reads the historical trace and execution logs of agent actions under this session. Includes Shadow-Mode drift metrics and forensic receipt IDs.

### `resolve_defi_intent`
Resolves a high-level natural language DeFi intent into structured parameters, which are then passed to a separately installed execution skill (like Signal Architect or Futures Strategist) for user confirmation and EIP-191/EIP-191 local signing. Autonomous Operator has no private keys and cannot sign transactions or perform direct on-chain execution.

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
Fetch one durable FarmDash receipt by receipt ID (`fdrcpt_*`). Receipts are immutable records of intent execution outcomes. v2.0: Receipts now include the 11-field Forensic Telemetry schema if generated by the execution skill.

## Global Circuit Breakers & Crash Recovery (v2.0 Upgrade)

### Circuit Breakers
The Operator monitors `get_event_stream_snapshot` and `get_agent_activity` for critical failure modes. If triggered, it patches `farming_context` to `HALTED` and refuses to process new `create_intent` calls.
* **Shadow-Mode Drift Breaker:** If average execution slip exceeds 75 bps over 3 trades.
* **Oracle Desync Breaker:** If Futures Strategist reports `oracle_deviation_bps` > 50bps.
* **Drawdown Breaker:** If daily loss > -3% or weekly loss > -7%.

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
* If risk status is halted, do not call execution tools.
* If event freshness is stale, re-run the sense phase before proposing action.
* Never bypass the OODA loop. Do not jump from Observe directly to Act without Orient and Decide phases.
* Always log forensic receipts. An execution without a logged 11-field receipt is considered incomplete.

## Disclaimers
Autonomous operation can compound mistakes if risk limits are weak. Keep budgets bounded, log every decision, and require explicit user confirmation for state-changing operations.

**Skill Manual:** Available at `https://www.farmdash.one/openclaw-skills/farmdash-autonomous-operator/SKILL.md`

**Companion skills:** FarmDash Trail Marshal, FarmDash Signal Architect, FarmDash Futures Strategist, FarmDash Trail Intelligence, FarmDash Wagon Steward.

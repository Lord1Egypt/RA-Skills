---
name: FarmDash Autonomous Operator
description: "Session state and control-loop skill for OpenClaw DeFi agents. Manages persistent sessions, FarmingContext, event stream snapshots, heartbeats, delegation checks, and bounded autopilot coordination without holding private keys or bypassing user confirmations."
tags: ["defi", "ai-agent", "autonomous-agent", "openclaw", "clawhub", "mcp", "crypto", "web3", "onchain", "agent-session", "session", "context", "farming-context", "event-stream", "autopilot", "control-loop", "delegation", "risk-management", "zero-custody", "farmdash", "autonomous-operator"]
author: FarmDash Pioneers (@Parmasanandgarlic)
homepage: https://www.farmdash.one
version: "1.0.1"
icon: operator
env:
  FARMDASH_API_KEY:
    description: "Optional Bearer token for Pioneer or Syndicate tier. Scout session status checks work without any key or with the public fd_scout_free token."
    required: false
metadata: {"openclaw":{"homepage":"https://www.farmdash.one/agents","skillKey":"farmdash-autonomous-operator","primaryEnv":"FARMDASH_API_KEY","apiKeyRequired":false,"freeScoutKeyless":true,"freeScoutKey":"fd_scout_free","execution":"session-context-control"}}
---

# FarmDash Autonomous Operator

> [!NOTE]
> **THEMATIC METAPHOR DISCLAIMER**
> FarmDash is exclusively a decentralized finance (DeFi) software and AI agent intelligence platform. The "farming," "trail," "wagon," and "frontier" terminology is a gamified visual theme representing crypto yield hunting and airdrop points farming. It does not relate to physical agriculture or agrifood industries.

> [!IMPORTANT]
> **ZERO-CUSTODY CRITICAL BOUNDARY & EXECUTION GATING**
> This skill manages persistent agent sessions, control loops, and intent routing. It does **NOT** hold, request, or transmit private keys, seed phrases, or mnemonics, nor does it perform on-chain executions directly.
> 
> **Separate Approval Step Requirement**: 
> Every tool defined in this skill (including `resolve_defi_intent`, `configure_autopilot`, and `autopilot_cycle`) is strictly limited to session and state coordination. Any state-changing execution (such as swaps, perps, deposits, or transfers) prepared or planned under this skill **requires a separate, explicit user-signing or budget-approved execution step through another dedicated skill** (specifically **Signal Architect** for spot/swaps and **Futures Strategist** for perps) using user-local cryptographic signatures (EIP-191/EIP-712).

Autonomous Operator keeps a multi-skill agent coherent across turns. It owns session state, shared FarmingContext, event snapshots, heartbeats, delegation checks, and autopilot configuration.

It does not hold private keys. It does not execute swaps or perps directly.

## Tools

### `create_session`

Creates a persistent agent session and returns a one-time `sessionToken`. Store it securely in the agent runtime. FarmDash stores only a hash.

### `session_heartbeat`

Extends the session expiry. Use it during active autonomous loops.

### `get_farming_context`

Reads shared context for the session:

- objective.
- portfolio scope.
- risk settings.
- workflow state.
- ledger summary.
- data freshness timestamps.

### `patch_farming_context`

Patches shared context. The server controls `sessionId`, `agentAddress`, `revision`, and `updatedAt`; do not try to override them.

### `get_event_stream_snapshot`

Reads recent agent events as a JSON snapshot. Use this before planning and after execution.

### `verify_delegation`

Checks whether the user's Hyperliquid API wallet delegation is in place for autonomous perps.

### `configure_autopilot`

Configure bounded autonomous cycles. Respect user allowlists, risk limits, and execution confirmations.

### `autopilot_cycle`

Run bounded autonomous cycles. Respect user allowlists, risk limits, and execution confirmations.

### `agent_onboard`

One-call setup guide and capability map for autonomous operation.

### `get_agent_activity`

Reads the historical trace and execution logs of agent actions under this session.

### `resolve_defi_intent`

Resolves a high-level natural language DeFi intent into structured parameters, which are then passed to a separately installed execution skill (like Signal Architect or Futures Strategist) for user confirmation and EIP-191/EIP-712 local signing. Autonomous Operator has no private keys and cannot sign transactions or perform direct on-chain execution.

## Control Loop

1. `create_session`.
2. `get_farming_context`.
3. `get_event_stream_snapshot`.
4. Use Trail Marshal to plan a workflow.
5. Patch objective, risk, workflow, and freshness state with `patch_farming_context`.
6. Run read-only sense tools.
7. Present execution steps to the user through the owning execution skill.
8. `session_heartbeat`.
9. After execution, update ledger and freshness state.

## Agent Rules

- The session token is a capability. Never display it in normal user-facing prose.
- A context patch is state, not permission.
- A workflow plan is not a user confirmation.
- If risk status is `halted`, do not call execution tools.
- If event freshness is stale, re-run the sense phase before proposing action.

## Disclaimers

Autonomous operation can compound mistakes if risk limits are weak. Keep budgets bounded, log every decision, and require explicit user confirmation for state-changing operations.

**Install:** Copy this file into your OpenClaw workspace, or fetch `https://www.farmdash.one/openclaw-skills/farmdash-autonomous-operator/SKILL.md`.

**Companion skills:** FarmDash Trail Marshal, FarmDash Signal Architect, FarmDash Camp Guard, FarmDash Ledger Keeper.

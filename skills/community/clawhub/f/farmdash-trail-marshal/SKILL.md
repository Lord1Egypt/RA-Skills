---
name: FarmDash Trail Marshal
description: "Guarded DeFi orchestration layer for OpenClaw agents. Lists named multi-skill workflow recipes, builds quality gates, creates session-scoped workflow run records, and reports workflow status. Trail Marshal holds no keys and performs no on-chain action — every state-changing step remains delegated to the user's separately-installed execution skill under that skill's own confirmation gate."
tags: ["defi", "ai-agent", "autonomous-agent", "openclaw", "clawhub", "mcp", "crypto", "web3", "onchain", "orchestration", "workflow", "agent-workflows", "multi-agent", "quality-gates", "risk-management", "yield-farming", "airdrop", "read-only", "zero-custody", "farmdash", "trail-marshal"]
author: FarmDash Pioneers (@Parmasanandgarlic)
homepage: https://www.farmdash.one
version: "1.0.1"
icon: 🪪
env:
  FARMDASH_API_KEY:
    description: "Optional Bearer token for Pioneer or Syndicate workflow features. Scout workflow catalog works without any key or with the public fd_scout_free token."
    required: false
metadata: {"openclaw":{"homepage":"https://www.farmdash.one/agents","skillKey":"farmdash-trail-marshal","primaryEnv":"FARMDASH_API_KEY","apiKeyRequired":false,"freeScoutKeyless":true,"freeScoutKey":"fd_scout_free","execution":"guarded-orchestration-no-execution"}}
---

# FarmDash Trail Marshal

> **Security Posture.** Guarded orchestration only. Trail Marshal exposes `list_workflows`, `plan_workflow`, `run_workflow`, and `get_workflow_status`. It can build a plan and persist a workflow run record, but it cannot sign, approve, bridge, swap, deposit, or place perp orders. Every state-changing step is owned by a separately-installed sub-skill under that sub-skill's confirmation gate.

## What this skill does

Trail Marshal is a **composition and quality-gate layer** for OpenClaw agents. It returns a catalog of named multi-skill workflow recipes, checks whether the required skills are installed, separates read-only steps from state-changing steps, and records guarded workflow runs for session-based agents.

When the user says *"Hyperliquid is hot, set me up,"* a single skill cannot fully answer. The agent first reads market state and the user's wallet via read-only research skills, presents a plan, and (only with the user's explicit confirmation) hands off to the user's separately-installed execution skills. Trail Marshal documents that orchestration as a named recipe so the agent does not have to invent the sequence at runtime.

## Available tools

### `list_workflows`

Returns the canonical workflow catalog. Each entry includes a name, goal, required tier, the number of explicit user confirmations the recipe requires, and the sub-skills it composes.

**Inputs:** Optional `filter` string. The current endpoint searches workflow id, name, description, required tier, step skill, step tool, and step purpose. Legacy `category` or `tier` filters should be converted into a plain `filter` value before calling.

**Returns shape:**

```
{
  "workflows": [
    {
      "id": "farm_hyperliquid",
      "name": "Hyperliquid Point Farming",
      "description": "Optimize points on Hyperliquid through perps volume, spot balances, and funding arbitrage.",
      "requiredTier": "syndicate",
      "steps": [
        { "skill": "trail-intelligence", "tool": "get_trail_heat", "purpose": "Check HL momentum" },
        { "skill": "wagon-steward", "tool": "get_wallet_balances", "purpose": "Check current exposure" },
        { "skill": "futures-strategist", "tool": "scan_funding_rates", "purpose": "Identify arb opportunities" }
      ]
    }
  ]
}
```

The detailed `steps` for each recipe are delivered at runtime as part of the `list_workflows` JSON response. Agents fetch the catalog once per session and cache it for no longer than one hour, or five minutes when a user is actively approving execution.

Codebase alignment note: Wagon steps use `get_wallet_balances`; do not use the stale alias `get_balances`.

**Agent posture:** Call `list_workflows` once at conversation start. Present recipes by name when the user describes a goal that matches one of them.

### `plan_workflow`

Builds the Workflow Quality Gate for a named recipe. Inputs are `workflowId`, optional `installedSkills`, and optional `agentAddress`. The output classifies:

- available steps.
- missing steps.
- state-changing steps.
- confirmation count.
- fallback mode: `ready`, `research_only`, or `analysis_only`.

Use this before telling the user a workflow is executable.

### `run_workflow`

Creates a guarded workflow run record for a live session. Inputs are `workflowId`, `sessionId`, `agentAddress`, `sessionToken`, and optional `installedSkills`.

Important: `run_workflow` does not run execution tools. If a workflow includes `execute_swap`, `resolve_defi_intent`, or `execute_perp_order`, the run status becomes `awaiting_confirmation` and the owning execution skill must still present fresh data and obtain explicit user approval.

### `get_workflow_status`

Reads a workflow run by `runId`. Use this after a long-running loop, after a context restore, or before resuming a paused autonomous session.

## Workflow catalog (high level)

Eighteen recipes are published. Each is **orchestration metadata** — Trail Marshal never executes any state-changing step itself; the user's separately-installed sub-skills do, under their own ClawScan-reviewed contracts.

| ID | Goal | Tier | User confirmations |
|---|---|---|---|
| `farm_hyperliquid` | Coordinate Hyperliquid points, spot exposure, and perps/funding research | Syndicate | per execution step |
| `rotate_quarterly` | Compare current positions against fresh high-heat opportunities | Pioneer | per swap |
| `protect_portfolio` | Risk-first scan and optional emergency mitigation | Pioneer | 0 if no action |
| `tax_loss_harvest` | Identify loss-harvest candidates and quote realization paths | Pioneer | per swap |
| `delta_neutral_setup` | Coordinate paired spot + perp exposure | Syndicate | spot leg + perps leg |
| `idle_capital_deploy` | Find idle stables/native assets and compare deployment targets | Scout catalog / Pioneer wallet data | per swap |
| `sybil_dilution` | Review sybil-risk clusters and propose lower-correlation behavior | Pioneer | per action |
| `yield_optimization` | Review harvest/redeposit candidates against Trail Heat | Pioneer | per swap |
| `emergency_exit` | Plan a protocol exit and unwind route | Scout catalog / Pioneer wallet data | per swap |
| `rebalance_portfolio` | Re-align portfolio to target weights and current Trail Heat | Pioneer | per swap |
| `stablecoin_yield_ladder` | Build a risk-tiered stablecoin deployment ladder | Pioneer | per deposit intent |
| `post_trade_ledger_review` | Reconcile activity and export records after execution | Pioneer | 0 |
| `pre_trade_edge_audit` | Confirm positive net edge, clean route quality, fresh risk checks, and quote stability before execution | Pioneer | 0 before execution handoff |
| `post_execution_quality_review` | Compare expected versus realized output before allowing dependent follow-on actions | Pioneer | 0 |
| `perps_liquidation_buffer_check` | Reject or resize perps orders that do not survive normal volatility around liquidation | Pioneer | 0 before execution handoff |
| `funding_carry_break_even_audit` | Validate funding trades after fees, slippage, margin pressure, and funding flip risk | Pioneer | 0 before execution handoff |
| `session_command_center` | Coordinate context, event snapshots, workflow plans, and heartbeats | Pioneer | per execution handoff |
| `hedged_airdrop_rotation` | Rotate into high-heat farms while planning hedge coverage | Syndicate | spot leg + hedge leg |

Each recipe's full step graph is returned at runtime by `list_workflows`. The runtime sequence references the user's own separately-installed sub-skills (e.g. *FarmDash Signal Architect* for spot routing, *FarmDash Futures Strategist* for perps); Trail Marshal does not bundle, invoke, or import them.

## Permissions

Trail Marshal can read the public workflow catalog without session state. `run_workflow` requires the user's FarmDash agent `sessionToken` because it creates a session-scoped workflow run record. It cannot modify wallet state, approve allowances, or initiate any on-chain action.

If a recipe in the catalog requires execution, the user's separately-installed sub-skill performs that work under its own ClawScan-reviewed contract — Trail Marshal stays out of the execution call path.

If the runtime catalog references a skill that is not installed in the user's environment, such as `farmdash-camp-guard`, `farmdash-supply-master`, `farmdash-hedge-warden`, or `farmdash-ledger-keeper`, mark that step as unavailable and continue with the safe subset. Never fabricate a missing tool call.

## Tier model

| Tier | Cost | Limits | Capability |
|---|---|---|---|
| **Scout** | Free | 5 req / 24h | Returns the public workflow catalog |
| **Pioneer** | $39.99/mo | 500 req / day | Adds higher-rate catalog use; filtering is via the `filter` search string |
| **Syndicate** | $199/mo | 50k req / day | Higher-rate workflow orchestration and perps-heavy recipes |

## Composition patterns

### Workflow Quality Gate (v0.2)

Before presenting a recipe as executable, classify every step:

```json
{
  "workflowId": "rotate_quarterly",
  "availableSteps": [],
  "missingSteps": [],
  "stateChangingSteps": [],
  "confirmationsRequired": 0,
  "safeSubset": true,
  "fallback": "research_only | analysis_only | halt"
}
```

Rules:

- A workflow is executable only when every state-changing step has its owning execution skill installed.
- A missing read-only step lowers confidence; a missing execution step changes the recipe to `analysis_only`.
- If the recipe includes `execute_swap` or `execute_perp_order`, quote the confirmation count as "per execution step" unless the live catalog supplies a stricter count.
- If more than five minutes pass after the user reviews a plan, re-fetch `list_workflows` and re-run the read-only sense steps.

### The Sense / Decide / Present / Verify loop

Every Trail Marshal recipe respects this 4-phase pattern:

```
SENSE    → Read-only research and portfolio skills gather state
DECIDE   → The recipe ranks options and presents a plan to the user
PRESENT  → User reviews; the user's separately-installed sub-skill (if any) handles confirmation under its own contract
VERIFY   → Read-only portfolio skill confirms the new state on the next cycle
```

If a recipe skips SENSE, it is unsafe. If it skips VERIFY, the agent never improves. Trail Marshal recipes always include both.

### Confirmation gate

Trail Marshal cannot pre-confirm anything. Each user confirmation in a recipe happens at the moment the user's *separate* sub-skill presents its quote — not in Trail Marshal's call path. If asked to run a recipe without intermediate review, the agent should refuse and explain the contract.

### Tier composition

A recipe's required tier is the **maximum** of its sub-skill tiers. When a user is one tier below a recipe's requirement, the agent should recognize the gap from `requiredTier`, offer the lower-tier subset of the recipe (e.g. research-only without the execution leg), and surface an upgrade link if the user wants the full version. Never silently downgrade a recipe without telling the user what is being skipped.

## Reasoning guidelines for agents

- **Speak in workflows, not tool soup.** Quote a recipe's name and goal when presenting a plan.
- **Quote the `confirms` count up front** so the user knows how many user-confirmation steps the recipe involves.
- **Re-fetch and re-present** if more than ~5 minutes pass between catalog read and the user's review.
- **No new analysis.** Trail Marshal returns recipe metadata; it does not editorialize or override what other skills produce.

## Risk warnings the agent should surface

For any recipe whose execution legs are owned by a separately-installed sub-skill, the agent should restate to the user that:

- DeFi positions can lose value rapidly; airdrop rewards are speculative and not guaranteed.
- Smart contracts can be exploited; even high-Trail-Heat protocols carry technical risk.
- Cross-chain transfers are irreversible if the wrong address or chain is selected.
- Slippage, gas, MEV, and routing fees materially affect realized returns.
- Past Trail Heat performance does not guarantee future scores.
- The user retains full responsibility for every on-chain decision they confirm via their own execution skill.

## Commercial disclosure (inherited from sub-skills)

When a recipe surfaces a `https://www.farmdash.one/go/{slug}` partnership route, the standard FarmDash commercial disclosure must be included in the same message: FarmDash may receive referral, affiliate, or routing compensation, and fee details live at `https://www.farmdash.one/fees`. Trail Marshal does not introduce new partner routes of its own.

## Versioning

**v1.0 (current).** Catalog plus guarded orchestrator tools: `plan_workflow`, `run_workflow`, and `get_workflow_status`. The migration is strictly additive; `list_workflows` remains unchanged for existing agents.

## Disclaimers

Workflow recipes are documentation, not financial advice. Any action performed by separately-installed sub-skills is the user's decision under that sub-skill's own contract. Trail Marshal performs no on-chain action; the user retains full responsibility for every decision they confirm.

---

**Install:** Copy this file into your OpenClaw workspace, or fetch `https://www.farmdash.one/openclaw-skills/farmdash-trail-marshal/SKILL.md`.

**Companion skills (separately installed by the user):** FarmDash Trail Intelligence (research), FarmDash Wagon Steward (read-only portfolio), FarmDash Signal Architect (spot routing), FarmDash Futures Strategist (perps), FarmDash Camp Guard (risk), FarmDash Supply Master (yield), FarmDash Hedge Warden (hedges), FarmDash Ledger Keeper (records), FarmDash Autonomous Operator (session context).

**Dashboard:** `https://www.farmdash.one`
**Agent Hub:** `https://www.farmdash.one/agents`
**MCP Config:** `https://www.farmdash.one/.well-known/mcp.json`

---

## Optional Setup Check

No registration call is required to install this skill, browse workflow recipes, or use research-only planning. Trail Marshal's core orchestration docs remain usable without onboarding and without `FARMDASH_API_KEY`.

Only run the setup check if the user explicitly asks to verify FarmDash tier/setup status and agrees to send the listed metadata.

Data sent:

- public `agentAddress`
- `X-ClawHub-Skill: farmdash-trail-marshal`

Data not sent:

- private keys, seed phrases, mnemonics, wallet exports, OAuth tokens, raw wallet secrets, or signed transactions

Optional command after consent:

```bash
curl -X POST https://www.farmdash.one/api/v1/agent/onboard \
  -H "Content-Type: application/json" \
  -H "X-ClawHub-Skill: farmdash-trail-marshal" \
  -d '{"agentAddress": "0xYOUR_AGENT_WALLET"}'
```

This returns tier status and available tool access. Skipping this step does not disable the workflow catalog or research-only planning.

### Next steps:
1. Use the Scout workflow catalog without setup when no key is configured.
2. Add `FARMDASH_API_KEY` only when the user wants higher-rate Pioneer/Syndicate workflow features.
3. Browse the OpenAPI spec at `https://www.farmdash.one/agents/openapi.yaml`.

---
name: FarmDash Camp Guard
description: "Use for pre-sign safety: allowance audits, route/health sentinel checks, policy scan of unsigned transactions. Verdicts only; never signs or broadcasts."
tags: ["defi","defi-security","smart-contract-risk","token-allowance","approval-revoke","approval-risk","transaction-risk-analysis","transaction-policy","wallet-security","risk-sentinel","pre-transaction-check","rug-pull","defi-scams","scam-protection","openclaw","ai-agent","mcp","zero-custody","web3-security","farmdash"]
author: FarmDash Pioneers (@Parmasanandgarlic)
homepage: https://www.farmdash.one/agents
version: "1.1.2"
icon: shield
env:
  FARMDASH_API_KEY:
    description: "Optional Bearer token for Pioneer or Syndicate tier. Scout mode can use limited security checks without a key."
    required: false
metadata: {"openclaw":{"homepage":"https://www.farmdash.one/agents","skillKey":"farmdash-camp-guard","primaryEnv":"FARMDASH_API_KEY","execution":"read-only-risk-gate"}}
---

# FarmDash Camp Guard

## Futures Execution Mode Contract

- **USER_SIGNED** requires fresh human approval for every order/cancel and a local Hyperliquid EIP-712 venue signature.
- **BOUNDED_AUTONOMOUS** may run without per-order human confirmation only under a valid owner-signed futures grant, current API-wallet venue authority, and all identity, session, scope, policy, risk, budget, builder and replay checks. Every venue action still requires a local signature.
- Read futures bounded readiness in the generated canonical table and live status. Separate spot and futures authority; a generic session policy or spot grant never authorizes futures.
- Read `POST /api/v1/agent/authority`, `action: get_futures_authority`, `sessionId`, `sessionToken`; the restrictive revoke control is `action: revoke_futures_policy`, `grantId`, `sessionId`, `sessionToken`. These are authority REST actions, not new Camp Guard tools. Missing/storage-unavailable authority yields halt, never presumed permission.
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

- `walletAddress` optional EVM wallet.
- `allowances` array with `token`, `spender`, `allowance`, `requiredAmount`, optional `amountUsd`, and `spenderVerified`. Set `spenderVerified: true` only after an independent canonical-deployment check; never trust a label supplied by the transaction builder.

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
- `transaction.value`
- `transaction.chainId`
- `expectedTransaction` captured independently before the unsigned payload is returned: exact `to`, `chainId`, `value`, and SHA-256 `dataHash`.

Output includes `simulation.status: "not_run"` because Camp Guard is honest about scope. A missing expected envelope is a high-severity review item. Use a wallet, RPC, or Tenderly-style environment for actual execution simulation before broadcast.

### `run_risk_sentinel`

Runs FarmDash Risk Sentinel on either:

- a swap-shaped route (`fromChainId`, `toChainId`, `fromToken`, `toToken`, `fromAmount`), or
- manual risk fields (`healthFactor`, `liquidationBufferPct`, `expectedUpsideUsd`, `gasUsd`, `bridgeFeeUsd`, `riskBufferUsd`).

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

## Standard Flow

### Pre-Sign Safety Summary
Before presenting any signature, read back a five-line summary: (1) `audit_allowance_risk` verdict and flags, (2) `run_risk_sentinel` route/health/net-edge result, (3) `simulate_transaction_risk` outcome with `simulation.status: "not_run"` stated, (4) expected-envelope match on exact `to`, `chainId`, `value`, and SHA-256 `dataHash`, (5) `spenderVerified` basis. Continue only when all verdicts are `pass`; remediate and re-run `review` items.

1. Read the user's intended action.
2. Run `audit_allowance_risk` if approvals are involved.
3. Run `run_risk_sentinel` for route, health, and net-edge checks.
4. Run `simulate_transaction_risk` on the final unsigned transaction payload.
5. Continue only when all verdicts are `pass`. Remediate and re-run `review` items; user acceptance alone does not turn missing evidence into safety.

## Disclaimers

Camp Guard is a risk gate, not insurance. It cannot detect every malicious contract, oracle failure, depeg, bridge failure, or social-engineering attack. The user remains responsible for every transaction they sign.

**Install:** Copy this file into your OpenClaw workspace, or fetch `https://www.farmdash.one/openclaw-skills/farmdash-camp-guard/SKILL.md`.

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
- [Canonical FarmDash Camp Guard skill manual](https://www.farmdash.one/openclaw-skills/farmdash-camp-guard/SKILL.md)
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

Generate a random UUIDv4 locally once per installation (for example, `crypto.randomUUID()`); persist only that random analytics ID in your application's own local state and reuse it across requests and skills. Never copy an example ID or generate a new ID for every request. Send optional `X-FarmDash-Installation-ID`; keep `X-ClawHub-Skill: farmdash-camp-guard` and optionally `X-FarmDash-Skill-Version: 1.1.2`. Controlled SDKs accept explicit `installationId`; the MCP stdio runtime persists only its analytics ID, with `FARMDASH_INSTALLATION_ID` override. No generic SDK writes files for you.

This is untrusted analytics only. The server stores a domain-separated salted installation hash, not the raw ID. An installation is not a person, principal or wallet. These headers cannot authenticate, alter quota/payment/Scout trials, establish wallet ownership, create delegation or authorize transactions. Missing headers remain fully compatible. Do not send API keys, signatures, grants, payment proofs, wallet data or session tokens as attribution. First-touch acquisition and event-touch assistance are reported separately; a download is not proven activation or revenue.

<!-- installation-attribution:end -->

---
name: api3-feed-manager
description: Discover, activate, fund, and maintain Api3 data feeds permissionlessly for downstream agent projects. Use when an agent needs a decentralized data feed pricing a blockchain based asset on a supported chain, needs to ensure feed runway for a build or deployment, or must maintain an already-enabled feed over time. Default to discovery, readiness checks, and dry-run planning first, and only use signer-backed execution when the user explicitly asks for it.
metadata:
  clawdis:
    homepage: https://github.com/daav3/agentic-lending-project
    author: daav3
    requires:
      bins:
        - node
      config:
        - request.ensure-feeds.json
        - request.execute-buy-subscription.json
---

# Api3 Feed Manager

This skill is the oracle-enablement layer for agent-built projects that need reliable, decentralized, onchain data feeds.

It is designed to let agents:
- find the correct Api3 feed
- distinguish between feeds that are merely discoverable and feeds that are currently active
- determine whether a feed is already usable
- fund/activate it when possible
- deploy the deterministic communal Api3 reader proxy when frontend/integration readiness depends on it
- maintain runway for continued operation

without requiring manual coordination with the Api3 team.

## When to use

Use this skill when:
- a project needs a reliable, onchain, decentralized price feed
- an agent wants to deploy something that depends on a live oracle
- an existing feed may need a top-up or runway check
- a downstream skill or app needs feed activation as a prerequisite

## Core modes

### 1. discover-feed
Use when you need to identify the best Api3 data feed for:
- an asset
- a pair
- a chain
- a specific oracle use case

Expected output:
- feed identity
- chain availability
- whether it is discoverable
- whether it appears active/usable
- whether activation may be needed
- any ambiguity or missing mapping

### 2. ensure-feed-active
Use when you know the required feed and want to ensure it has enough funding/runway.

Default target runway:
- 90 days

Expected output:
- current funding/liveness status
- estimated runway
- whether funding/top-up is needed
- execution path or exact transaction instructions

### 3. check-feed-runway
Use to inspect an already-known feed and estimate maintenance needs.

Expected output:
- current status
- remaining runway estimate
- whether action is required soon

### 4. top-up-feed
Use when a feed exists but needs more runway.

Expected output:
- required funding token/amount
- top-up execution plan
- resulting status if executed

### 5. maintain-feed
Use for maintenance mode when one or more project feeds must remain alive.

Expected output:
- current state per feed
- top-up recommendation or actions taken
- next maintenance checkpoint recommendation

## Inputs to gather before acting

Collect these first when available:
- target chain
- asset or pair required
- use case (e.g. lending collateral pricing, borrow asset pricing)
- desired runway in days
- whether execution is allowed or discovery-only
- signer/funder available to the agent
- explicit operator approval if any real transaction submission is requested

## Operating rules

1. Do not pretend a feed is active without checking.
2. Distinguish clearly between:
   - feed missing
   - feed present but unfunded
   - feed available on another chain only
   - feed exists but agent lacks execution capability
3. Prefer permissionless operation paths.
4. If a step cannot be done permissionlessly, say exactly why.
5. Return concrete feed identifiers and maintenance recommendations.
6. If discovery is ambiguous, surface the ambiguity instead of guessing.
7. Treat signer-backed execution as a guarded operator action, not a default background step.
8. Prefer signer material from local runtime setup, never from committed files.

## Suggested workflow

### For a new project
1. Discover feed
2. Confirm chain/feed suitability
3. Check whether active/funded
4. Ensure 90-day runway
5. Return feed details to downstream builder/deployer

### For an existing project
1. Check current runway
2. If below threshold, top up
3. Return next maintenance recommendation

## Output contract

Aim to return structured results containing:
- `feedFound`
- `discoverable`
- `active`
- `activationPossible`
- `statusClassification`
- `feedName`
- `feedAddressOrId`
- `chain`
- `funded`
- `runwayEstimateDays`
- `requiredFundingAsset`
- `estimatedFundingAmount`
- `actionsTaken`
- `transactions`
- `nextMaintenanceRecommendation`
- `warnings`

## Current implementation status

Current honest state:
- feed discovery and readiness inspection: implemented
- exact guarded `buySubscription(...)` execution: implemented
- execution modes:
  - `direct`
  - `wrapper` when exact wrapper calldata is derivable safely
  - `auto`
- machine-usable funding state classification: implemented
  - `not-needed`
  - `executable`
  - `browser-assisted`
  - `unsupported`
- browser-assisted funding should stay automatable where safe
  - use `browser-plan` to produce the exact Market flow
  - if the required UI is reachable, execute that plan with the browser tool instead of downgrading to a vague manual handoff
  - after any funding execution, re-run feed readiness before claiming the feed is ready for downstream oracle or EVK steps
- browser-assisted funding planning: implemented via `browser-plan`

Still not universal:
- not every funding path is exact onchain-executable yet
- some flows still require browser-assisted automation
- unsupported cases must still fail closed and be reported explicitly

Current priorities:
1. broaden executable funding coverage beyond the first exact family
2. keep browser-assisted flows automatable where safe
3. preserve explicit state classification instead of overclaiming support
4. improve maintenance-mode and multi-feed workflows
5. keep downstream EVK and Morpho handoffs aligned with the live planner behavior proven in canaries
6. keep communal proxy deployment and downstream readiness checks aligned with the packaged runtime

## Feed-name matching guardrails for downstream lending flows

When this skill is used as a prerequisite for EVK or Morpho deployment:
- prefer a literal exact dAPI name match before any alias-normalized match
- treat symbol-family aliases as fallback discovery aids, not as reasons to block a live literal feed that already matches the requested asset pair
- preserve the original requested dAPI name for live readiness checks; only use canonicalized symbols for fallback route derivation when no literal match exists
- if a literal match is live and readable on-chain, classify that feed as ready even when alias-equivalent feeds also exist
- only surface ambiguity when the literal-exact bucket itself is ambiguous
- keep this logic asset-agnostic: the same path should work for whichever supported collateral and borrow assets the planner selects, not just previously tested majors

## Downstream EVK canary handoff

When this skill hands off to downstream EVK deployment tooling or canary execution:
- require a signer-backed dry-run before any real send
- treat multi-transaction deployment plans as sequential, not parallel
- if later transactions depend on contracts created earlier in the same plan, wait for each receipt before sending the next transaction
- if funding landed through the `browser-assisted` branch, execute the returned `browser-plan` when the Market flow is reachable and then re-run readiness before continuing
- if the funded feed still lacks code at its deterministic communal proxy address, deploy that proxy before treating the integration path as complete
- do not collapse `fundingExecutionClassification.state` into a generic “ready”; preserve the exact branch all the way into downstream reporting
- do not assume `real-send ready` means “safe to fire blind”, it only means the plan has executable payloads and still needs a final operator check
- if downstream EVK work needs proof of real borrowability, treat that as a separate post-deploy milestone rather than equating deployment success with borrowability
- if the operator intentionally wants a duplicate or near-duplicate market attempt, require `duplicatePolicy: "warn-only"` so the planner keeps the path deployable and emits an explicit warning instead of silently bypassing duplicate protection
- if the direct pair is unavailable but a supported composition route is live (for example through a shared unit of account such as USD), allow the EVK path to use that composed oracle route rather than failing prematurely
- keep deployment and verification rules generic across supported asset pairs; do not special-case only the pairs used in earlier canaries
- after a real send, verify more than submission: confirm nonce movement, status=1 receipts, deployed contract addresses for each oracle leg/wrapper, and final market deployment success before reporting the canary as successful

## Downstream Morpho handoff

When this skill hands off to downstream Morpho deployment tooling:
- keep proxy-first ordering when a communal proxy deploy is required before adapter deploy or market creation
- keep the same signer, RPC, and nonce assumptions across deploy + verify steps in a single live run
- support the planner selecting whichever supported collateral/borrow pair is requested, as long as the oracle path resolves cleanly and verification invariants hold
- do not treat a mined market-create transaction as success unless downstream verification confirms the market exists, params match, `price()` succeeds, and the oracle price is positive
- persist enough artifact context for the next operator turn: tx hashes, market id, final oracle address, and a short failure-before / success-after note

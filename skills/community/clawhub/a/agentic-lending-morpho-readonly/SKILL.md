---
name: agentic-lending-morpho-readonly
description: Read-only Morpho-first agentic lending planning for Api3-backed markets. Use when a user wants a Morpho market or market set explored for selected collateral and borrow assets, needs the oracle route resolved, wants Api3 feed readiness or funding posture inspected, or needs deployment and verification planning without any signer-backed execution, funding, broadcast, or transaction submission. Do not use for Euler EVK flows or any request that requires live onchain writes.
---

# Agentic Lending Morpho Read-only

Use this skill for Morpho planning and readiness analysis only.

## Safety expectations
- stay read-only
- do not perform signer-backed funding, deployment, broadcast, or transaction submission
- treat browser-assisted funding as a handoff note, never an action path
- require exact asset selection before deployment planning
- require a usable RPC endpoint before claiming any on-chain verification result
- keep any signer material out of scope for this skill

## Read next
1. `references/workflow.md`
2. `references/current_capabilities.md`
3. `references/morpho-oracle-adapter.md`

## Minimum required inputs
Gather these before attempting a Morpho-first planning workflow:
- chain name and chain id
- explicit `collateralAssets`
- explicit `borrowAssets`
- target market shape or risk intent
- whether the user wants planning only, dry-run analysis, or deployment-prep reporting
- live RPC availability for the chain if read-only verification beyond planning is expected

If any of those are missing, stop and ask instead of inventing them.

## Request-shape rule
When preparing a request for this skill, always express the market assets explicitly as:
- `collateralAssets`: array of `{ symbol, address }`
- `borrowAssets`: array of `{ symbol, address }`

Do not leave asset selection implicit.

## Default workflow
1. Normalize the request into:
   - chain
   - `collateralAssets`
   - `borrowAssets`
   - protocol = `morpho`
   - market or risk intent
   - desired analysis mode
2. Treat asset selection as a first-class input.
   - confirm the exact collateral asset set and borrow asset set the user wants
   - for multiple collateral assets, remember this becomes a Morpho market set: one market per supported collateral/borrow pair
3. Resolve the oracle path before any deployment planning.
   - prefer a direct pair when the exact requested route is available and usable
   - otherwise use a supported composed route when the planner can prove it cleanly
   - keep feed-name matching generic: literal exact pair first, alias-normalized fallback second
4. Check feed readiness before any deploy recommendation.
   - classify feeds as already live, fundable by an operator, browser-assisted, or unsupported
   - do not execute funding
5. Prepare the Morpho oracle adapter plan.
   - use the Api3-backed Morpho oracle adapter design as the canonical oracle shape
   - preserve artifact and dependency expectations for a later deployment handoff
6. Prepare the Morpho market deployment plan.
   - identify the expected deploy and verify sequence without sending transactions
7. Verify only at the honest read-only boundary.
   - confirm what can be checked from planner output or RPC reads
   - do not imply market creation, funding execution, or deployment happened
8. Stop at the honest boundary.
   - if the request needs funding or deployment, hand off clearly
   - do not present planning or dry-run analysis as a live Morpho deployment

## Preferred command path
For a concrete planning request, prefer this command shape:

`node bin/part2-morpho-planner.js prepare-morpho-market --input-file ./request.json`

Use read-only planner and verification-oriented commands only. Do not use commands that fund feeds, broadcast transactions, or deploy markets.

## Output expectations
Always report:
- whether the request was normalized successfully
- which collateral assets and borrow assets were selected for the Morpho market or market set
- whether the required Api3 feeds are already live, operator-fundable, browser-assisted, or unsupported
- what oracle adapter shape is planned for Morpho
- which steps are planning-only versus requiring operator execution
- exact blockers preventing a full Morpho deployment flow, if any
- the next concrete read-only command, file, or handoff needed

## Tone
Be blunt about current Morpho limits.
Do not blur design-doc intent into executable support.
Be equally clear when the repo already supports the read-only planning or verification step being requested.

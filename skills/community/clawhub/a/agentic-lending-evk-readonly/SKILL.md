---
name: agentic-lending-evk-readonly
description: Read-only EVK-first agentic lending workflow planning and verification for Api3-backed markets. Use when a user wants an agent to resolve the oracle route for selected collateral and borrow assets, inspect Api3 feed readiness and funding classification, prepare the Euler oracle and EVK market artifacts, assess deployability, or plan post-deploy borrow-proof requirements without ever using signer-backed execution, browser-funded purchase completion, transaction submission, or live borrow canaries. Do not use for Morpho, unsupported recipes, or any request that requires sending transactions.
---

# Agentic Lending EVK Read-Only

This skill turns the repo's current EVK planner primitives into a read-only workflow: route resolution, feed readiness and funding classification, oracle prep, EVK market prep, deployment readiness assessment, and borrow-proof planning without any live execution authority.

## Safety expectations
- stay in planning, simulation, inspection, or preview-only mode
- never use signer-backed funding, deployment, approvals, swaps, or borrow proof execution
- never automate browser purchase completion or any other external write path
- treat `browser-assisted` and `executable` funding states as planning outputs, not permission to act
- keep wallet addresses, RPC endpoints, and deployment targets as inspection inputs only

## Use this when
- the user wants to plan or review an EVK lending market backed by Api3 feeds without sending transactions
- the user wants one workflow instead of manually stitching planner JSON steps
- the task includes any combination of asset selection, oracle route resolution, feed readiness, funding classification, oracle preparation, EVK deployment prep, deployability review, or post-deploy borrow-proof planning

## Do not use this when
- the user wants Morpho, not EVK
- the requested recipe or oracle path is not supported by the current repo
- the task requires pretending a skeleton-only path is executable
- the task requires autonomous or manual transaction submission, browser completion, or live borrow proof

## Read next
1. `references/api_reference.md`
2. `references/current_capabilities.md`
3. `references/live-borrow-checklist.md` when the workflow reaches borrow-proof planning
4. `references/arbitrum-eusdc1-isolated-example.json` when a concrete proof-config shape helps

## Minimum required inputs for the combined flow
Gather these before you assume the full planning workflow is feasible:
- chain name and chain id
- collateral asset set and borrow asset set
- target recipe id or risk preset
- whether the user wants planning only, dry-run assessment, or execution readiness review
- whether the user also wants post-deploy borrow-proof planning
- live RPC availability only if the user wants chain-state verification beyond static planning
- `vaultContext` when the deployment path needs concrete factory or asset wiring

If any of those are missing, stop and ask instead of improvising.

## Default workflow
1. Normalize the request into:
   - chain
   - collateral assets
   - borrow assets
   - target recipe or risk preset
   - whether the user wants planning only, dry-run assessment, or execution readiness review
   - whether the user also wants proof-of-borrowability planning
2. Resolve the oracle path for the selected assets before treating deployment as executable.
   - prefer an exact direct route when the requested pair exists and is deployable
   - otherwise use a supported composed route when the planner can prove it cleanly
   - prefer literal exact feed-name matches before alias-normalized fallback matches
3. Prefer `run-evk-workflow` as the default end-to-end entrypoint when the user wants the full EVK planning path.
   - pass `recipeId` explicitly when known, otherwise let the runner infer from the current EVK recipe catalog
   - treat `status` as the canonical summary object
   - treat `result` as the detailed staged artifact bundle
4. If the user wants proof-of-borrowability planning, continue within this skill only to inspect the required proof inputs and blockers.
   - treat deployment success and borrowability proof as separate milestones
   - use the deployment outputs plus target vault addresses, EVC state requirements, and tiny borrow sizing to plan a proof config
   - do not run the proof executor from this skill
5. Fall back to the manual staged commands only when the user asked for a subset, wants intervention at a specific phase, or the runner stops before the desired outcome.
   - `plan-market`
   - `ensure-feeds`
   - if feeds are live, continue to the oracle and EVK planner path
   - if funding is needed, inspect `purchase-inputs` or `prepare-buy-subscription` output and branch on `fundingExecutionClassification.state`
   - if `fundingExecutionClassification.state === "executable"`, report exact onchain readiness only
   - if `fundingExecutionClassification.state === "browser-assisted"`, report browser handoff readiness only
   - if `fundingExecutionClassification.state === "unsupported"`, stop and report unsupported status clearly
   - `prepare-euler-oracle`
   - `prepare-evk-market`
   - `prepare-evk-deployment`
   - `deploy-evk-market` only for dry-run or readiness inspection when that path is non-sending
6. Stop and report honestly if:
   - feed funding is `unsupported`
   - the browser-assisted funding UI would be required for completion
   - the oracle path is still skeleton-only
   - the EVK market path is still skeleton-only
7. Prefer dry-run or inspection first for funding and deployment paths.
8. Never cross the line from readiness assessment into real-send execution.
9. Keep the path generic across supported pairs.
   - do not special-case only previously tested collateral/borrow combinations
   - use the same resolution, funding classification, deployment assessment, and proof-planning rules for whichever supported assets are selected
10. Do not claim a market is borrowable just because deployment artifacts look ready. A separate proof step would still be required, and this skill only plans that step.

## Borrow-proof planning only
Treat post-deploy borrow proof as a planning artifact here, not an execution step.

Planning contract:
1. identify the fields needed for `borrow-proof-config.json`
2. verify whether the referenced executor path exists in the installed repo or sibling live skill
3. report the preview command that a live-capable workflow would run
4. stop before any preview or `--live` execution

Keep the proof planning honest:
- distinguish mixed-collateral borrow from isolated target-collateral borrow
- preserve the exact funding branch that led here
- verify quoteability, LTV wiring, EVC state, and vault cash requirements as checklist items, not completed facts unless separately verified
- if the chain does not use a Uniswap V3 compatible router, note that the bundled swap step would need replacement or bypass
- require nonzero `amountOutMinimum` for any hypothetical live swaps
- keep approval scope exact by default in the plan

## Current happy-path rule
The currently supported end-to-end EVK planning path requires:
- feeds that are already live, or a feed that can at least be classified through the current narrow exact `buySubscription(...)` path
- a cleanly resolved oracle path for the selected assets
- top-level `prepare-evk-deployment.vaultContext`
  - `factoryAddress`
  - `assetAddress`

Without that `vaultContext`, the first EVK market transaction remains skeleton-only and `readyToBroadcast` must stay false.
Without a supported exact buy-subscription path, feed funding must stay at handoff or prep only.

## Output expectations
When using this skill, always report:
- `status.phaseReached` when the top-level runner is used
- `status.state` when the top-level runner is used
- `status.recipeId` when the top-level runner is used
- what is executable vs still skeleton-only
- blockers and warnings
- `fundingExecutionClassification.state` when feed funding is involved manually
- `status.fundingExecutionState` when the top-level runner is used
- whether the current state is:
  - plan-only
  - feed-ready but awaiting activation or funding handoff
  - funding dry-run ready
  - browser-assisted funding ready
  - oracle-executable
  - EVK dry-run ready
  - real-send ready in theory but not available through this read-only skill
  - deployed but borrow-proof pending
  - live borrow proven is out of scope for this skill

If the user asked for borrowability proof, also report whether the workflow has reached proof planning or is still waiting on proof inputs.

If the top-level runner is used, also surface the executable flags under `status.executable` instead of paraphrasing them away.

## Tone
Be blunt about current limits.
Do not overclaim support beyond the routes the planner can actually resolve.
Do not blur deployment readiness into borrowability proof.
If the workflow falls off the happy path, say exactly where and why.

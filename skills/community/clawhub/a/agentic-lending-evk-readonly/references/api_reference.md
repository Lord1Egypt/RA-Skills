# Agentic Lending EVK workflow reference

This skill wraps the repo's current EVK-first planner workflow, then stops at deployment-readiness and borrow-proof planning.

The important abstraction is the path, not the prior canaries:
1. normalize the selected collateral and borrow assets
2. resolve the oracle route for those assets
3. ensure or classify feeds on the deployable path
4. prepare the EVK market
5. assess deployment readiness
6. plan borrowability proof separately when requested

## Command order

Prefer the workflow in this order unless the user only asked for a subset:

### Preferred top-level entrypoint
1. `run-evk-workflow`
   - use this when the user wants one input and one status or result object for the current EVK-first path
   - the response shape is:
     - `status`
       - `phaseReached`
       - `state`
       - `recipeId`
       - `deployable`
       - `fundingExecutionState`
       - `executable`
       - `blockers`
       - `warnings`
     - `result`
       - `planMarket`
       - `ensureFeeds`
       - `feedFunding`
       - `prepareEulerOracle`
       - `prepareEvkMarket`
       - `prepareEvkDeployment`
       - `deployEvkMarket`
   - if the user wants proof of borrowability after deployment, treat that as the next planning step inside this same skill

### Manual staged order
1. `plan-market`
2. verify the route chosen for the selected assets
   - prefer an exact direct route when available
   - otherwise use a supported composed route when the planner can prove it cleanly
   - prefer literal exact feed-name matches before alias-normalized fallback matches
3. `ensure-feeds`
4. if funding is needed and `fundingExecutionClassification.state === "executable"`:
   - `purchase-inputs`
   - `prepare-contract-call` or `prepare-buy-subscription`
   - inspect the returned artifacts only
   - `ensure-feeds` or `ensure-active` again only if another read-only verification step is available
5. if funding is needed and `fundingExecutionClassification.state === "browser-assisted"`:
   - `browser-plan`
   - report that plan as a handoff artifact only
6. `prepare-euler-oracle`
7. `prepare-evk-market`
8. `prepare-evk-deployment`
9. `deploy-evk-market` only for non-sending dry-run or readiness inspection when available
10. if the market appears deployable and the user wants proof that it can really borrow against the intended collateral path:
   - build a proof-config plan with chain RPC, borrow vault, target collateral vault, EVC address, token decimals, tiny borrow amount, and any stale controller or collateral cleanup
   - verify whether a sibling live skill or repo path contains `scripts/evk_live_borrow_proof.js`
   - report the preview command a live-capable workflow would run
   - stop before execution

## Practical command shapes

```bash
node ./bin/part2-planner.js run-evk-workflow --input-file ./request.run-evk-workflow.json
node ./bin/part2-planner.js plan-market --input-file ./request.plan-market.json
node ./bin/part2-planner.js ensure-feeds --input-file ./request.ensure-feeds.json
node ./bin/api3-feed-manager.js purchase-inputs --input-file ./request.purchase-inputs.json
node ./bin/api3-feed-manager.js prepare-buy-subscription --input-file ./request.prepare-buy-subscription.json
node ./bin/api3-feed-manager.js browser-plan --input-file ./request.browser-plan.json
node ./bin/part2-planner.js ensure-feeds --input-file ./request.ensure-feeds.json
node ./bin/part2-planner.js prepare-euler-oracle --input-file ./request.prepare-euler-oracle.json
node ./bin/part2-planner.js prepare-evk-market --input-file ./request.prepare-evk-market.json
node ./bin/part2-planner.js prepare-evk-deployment --input-file ./request.prepare-evk-deployment.json
node ./bin/part2-planner.js deploy-evk-market --input-file ./request.deploy-evk-market.json
```

## Top-level runner request shape

Minimal shape:

```json
{
  "chain": { "name": "arbitrum", "chainId": 42161 },
  "collateralAssets": [
    { "symbol": "WETH", "address": "0x82af49447d8a07e3bd95bd0d56f35241523fbab1" }
  ],
  "borrowAssets": [
    { "symbol": "USDC", "address": "0xaf88d065e77c8cC2239327C5EDb3A432268e5831" }
  ],
  "riskPreset": "eth-major"
}
```

Useful optional fields:
- `recipeId`
- `rpcPreference`
- `feedFunding`
- `allowCustomFallback`
- `preferInfrequentOracle`
- `publishToRegistry`
- `vaultContext`
- `executionProfile`
- `broadcast`
- `send`

Use the staged commands directly only when you need narrower control than the top-level runner provides.

## Minimum required inputs for a cold start
Before attempting the full planning workflow, confirm you have:
- `chain.name` and `chain.chainId`
- at least one collateral asset and one borrow asset
- `riskPreset` or `recipeId`
- whether the user wants planning only, dry-run assessment, or execution-readiness review
- whether the user wants post-deploy borrow-proof planning
- live RPC access only if any chain-state verification is expected
- `vaultContext` when the market deployment path requires concrete factory or asset addresses

If post-deploy proof planning is required, also gather:
- target collateral vault address for the proof
- EVC address
- a tiny borrow amount
- any stale collaterals or controllers that must be disabled for an isolated proof
- swap venue details only if the wallet would need to source repay or collateral assets first

## Canonical end-to-end example
Use this exact mental model for a cold-start request:
1. run `run-evk-workflow` with chain, assets, and recipe intent
2. inspect `status.state`, `status.phaseReached`, and `status.executable`
3. make sure the resolved route for the selected assets is acceptable
4. if feed funding is needed:
   - branch on `fundingExecutionClassification.state`
   - inspect direct or wrapper funding artifacts when `executable`
   - inspect `browser-plan` when `browser-assisted`
   - re-run feed readiness only if a read-only confirmation step is available
5. continue through oracle prep, EVK market prep, and deployment readiness
6. if the user asked for borrow proof planning:
   - build a borrow-proof config plan from the deployment outputs plus proof-specific inputs
   - report the preview mode command a live workflow would use
   - stop before any execution
7. report deployment readiness and borrowability proof planning as separate outcomes

Use the staged commands directly only when you need narrower control than the top-level runner provides.

## Generalization rule
Treat the EVK planner path as asset-agnostic across supported pairs:
- do not special-case only previously tested collateral/borrow combinations
- use the same route-resolution, funding classification, deployment assessment, and proof-planning logic for whichever supported assets are selected
- treat prior successful canaries as evidence that the path can work, not as permission to hardcode those same examples into future planning

## Current executable happy path

### 1. `prepare-euler-oracle`
Use a direct `euler-chainlink-oracle` route or another oracle route that already resolves to executable oracle txs.

### 2. `prepare-evk-market`
Use a real recipe id from `src/part2-recipes.js`. A current example is `eth-major-stable-borrow-v1` with `riskPreset: "eth-major"`.

### 3. `prepare-evk-deployment`
This is where the first executable EVK market transaction is unlocked.

### 4. `deploy-evk-market`
Use guarded dry-run or readiness inspection only.

## Feed activation note

The first supported executable funding paths are the narrow exact `buySubscription(...)` direct path and the exact prepared wrapper-call alternative when the code can already derive it safely.

The machine-usable field is now:
- `fundingExecutionClassification.state`
  - `not-needed`
  - `executable`
  - `browser-assisted`
  - `unsupported`

Branching rule:
- `not-needed` → continue immediately
- `executable` → inspect exact onchain artifacts only
- `browser-assisted` → call `browser-plan` and report the Market flow handoff
- `unsupported` → stop and report unsupported

After any funding planning step, re-run feed readiness only when a read-only confirmation path exists.

## Post-deploy borrow proof planning

After `deploy-evk-market`, do not stop at "deployment looks ready" if the user asked for proof-of-borrowability planning.

### Deployment output → proof config mapping
When building `borrow-proof-config.json`, map values deliberately instead of guessing:
- borrow vault address → from the deployed EVK market output, using the newly deployed borrow vault, not a prior canary vault
- collateral vault address → from the intended proof target, not from the borrow market manifest unless they are explicitly the same
- EVC address → from the deployed borrow vault's `EVC()` contract when available, otherwise from the deployment context for that chain
- borrow asset address and decimals → from the deployed borrow vault asset or the workflow request borrow asset, whichever is authoritative for the live market
- collateral asset address and decimals → from the chosen collateral vault's underlying asset
- wrapped native token → from the target chain, not hardcoded from Arbitrum examples
- signer env name → from local runtime setup in a live-capable workflow, never from committed files
- live acknowledgement → set only in a live-capable workflow when the operator intends to allow a live proof send
- stale collaterals or controllers to disable → from the actual wallet state at proof time, not from a past example

If any of those mappings are ambiguous, stop and inspect chain state before constructing the proof plan.

Treat these as distinct outcomes:
- deployment dry-run ready
- real-send ready in theory
- deployed but borrow-proof pending
- live borrow proven is outside this skill

## Stop conditions

Stop and report instead of improvising when:
- `fundingExecutionClassification.state === "unsupported"`
- the browser-assisted funding UI would be required for completion
- `ensure-feeds` says the feeds are not ready and no supported exact buy-subscription path is available
- the oracle path is still skeleton-only
- `prepare-evk-deployment` does not include concrete top-level `vaultContext`
- `deploy-evk-market` still reports skeleton market transactions
- the proof step cannot honestly isolate or demonstrate the collateral path the user asked for

## Real-send rule

Do not move beyond dry-run or planning in this skill.
If a request requires `broadcast.enabled`, acknowledgements, signer identity, or private-key-backed sending, hand it off to a live-capable sibling skill instead of acting here.

# Agentic Lending EVK workflow reference

This skill wraps the bundled EVK-first planner workflow, then extends it into a post-deploy borrow proof step.

The important abstraction is the path, not the prior canaries:
1. normalize the selected collateral and borrow assets
2. resolve the oracle route for those assets
3. ensure or fund feeds on the deployable path
4. prepare and deploy the EVK market
5. prove borrowability separately when requested

## Command order

Prefer the workflow in this order unless the user only asked for a subset:

### Safety gate before live-capable use
1. `preflight-evk-workflow`
   - use this before any request that might become `broadcast-ready`, `real-send`, or signer-backed feed funding
   - it returns:
     - `safeToRun`
     - `liveTxRequested`
     - `liveTxAllowed`
     - `placeholderSafe`
     - `preview.status`
     - `blockers`
     - `warnings`

### Preferred top-level entrypoint
2. `run-evk-workflow`
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
       - `artifactPersistence`
   - if `artifacts.enabled === true`, the persisted run bundle also includes `summary.json`, `agent-decision.json`, and `rollback-plan.json`
   - if the user wants proof of borrowability after deployment, treat that as the next workflow step inside this same skill

### Persisted-run helper commands
3. `explain-next`
   - use this with `--run-dir` to recover the model-friendly state of a persisted run
   - read it first when resuming or handing off a stored EVK run
4. `verify-evk-deployment-handoff`
   - use this with `--run-dir` before claiming the persisted run is deployment-complete or ready for proof follow-up
5. `run-evk-workflow --resume-from-run-dir <dir>`
   - use this to reopen a known run directory instead of reconstructing state from memory

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
   - `execute-buy-subscription`
   - `ensure-feeds` or `ensure-active` again
5. if funding is needed and `fundingExecutionClassification.state === "browser-assisted"`:
   - `browser-plan`
   - execute that plan with the browser tool
   - `ensure-feeds` or `ensure-active` again
6. `prepare-euler-oracle`
7. `prepare-evk-market`
8. `prepare-evk-deployment`
9. `deploy-evk-market`
10. if the market was deployed and the user wants proof that it can really borrow against the intended collateral path:
   - build a proof config with chain RPC, borrow vault, target collateral vault, EVC address, token decimals, tiny borrow amount, and any stale controller or collateral cleanup
   - verify the bundled executor exists at `scripts/evk_live_borrow_proof.js`
   - run `node ./scripts/evk_live_borrow_proof.js --config <path>` first
   - rerun with `--live` only if the user wants the canary
   - for live mode, require the config's guarded live-send acknowledgement field to match the script's required phrase, and require the configured account address to match the signer address

## Practical command shapes

```bash
node ./bin/part2-planner.js preflight-evk-workflow --input-file ./request.run-evk-workflow.json
node ./bin/part2-planner.js run-evk-workflow --input-file ./request.run-evk-workflow.json
node ./bin/part2-planner.js explain-next --run-dir ./artifacts/evk/<hash>/<run>
node ./bin/part2-planner.js verify-evk-deployment-handoff --run-dir ./artifacts/evk/<hash>/<run>
node ./bin/part2-planner.js run-evk-workflow --resume-from-run-dir ./artifacts/evk/<hash>/<run> --input-file ./artifacts/evk/<hash>/<run>/request.json
node ./bin/part2-planner.js plan-market --input-file ./request.plan-market.json
node ./bin/part2-planner.js ensure-feeds --input-file ./request.ensure-feeds.json
node ./bin/api3-feed-manager.js purchase-inputs --input-file ./request.purchase-inputs.json
node ./bin/api3-feed-manager.js prepare-buy-subscription --input-file ./request.prepare-buy-subscription.json
node ./bin/api3-feed-manager.js execute-buy-subscription --input-file ./request.execute-buy-subscription.json
node ./bin/api3-feed-manager.js browser-plan --input-file ./request.browser-plan.json
node ./bin/part2-planner.js ensure-feeds --input-file ./request.ensure-feeds.json
node ./bin/part2-planner.js prepare-euler-oracle --input-file ./request.prepare-euler-oracle.json
node ./bin/part2-planner.js prepare-evk-market --input-file ./request.prepare-evk-market.json
node ./bin/part2-planner.js prepare-evk-deployment --input-file ./request.prepare-evk-deployment.json
node ./bin/part2-planner.js deploy-evk-market --input-file ./request.deploy-evk-market.json
node ./scripts/evk_live_borrow_proof.js --config ./borrow-proof-config.json
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
- `artifacts`
- `allowCustomFallback`
- `preferInfrequentOracle`
- `publishToRegistry`
- `vaultContext`
- `executionProfile`
- `broadcast`
- `send`

Use the staged commands directly only when you need narrower control than the top-level runner provides.

For any run that may need review or handoff, add:

```json
{
  "artifacts": {
    "enabled": true,
    "label": "evk-run"
  }
}
```

## Minimum required inputs for a cold start
Before attempting the full combined workflow, confirm you have:
- `chain.name` and `chain.chainId`
- at least one collateral asset and one borrow asset
- `riskPreset` or `recipeId`
- whether the user wants planning only, dry-run, or real send
- whether the user wants post-deploy borrow proof
- live RPC access if any non-simulated step is expected
- signer or executor details for live funding, deployment, or proof
- `vaultContext` when the market deployment path requires concrete factory or asset addresses

If post-deploy proof is required, also gather:
- target collateral vault address for the proof
- EVC address
- a tiny borrow amount
- any stale collaterals or controllers that must be disabled for an isolated proof
- swap venue details only if the wallet must source repay or collateral assets first

## Canonical end-to-end example
Use this exact mental model for a cold-start request:
1. before live-capable execution, run `preflight-evk-workflow` and stop unless `safeToRun === true`
2. run `run-evk-workflow` with chain, assets, and recipe intent
3. inspect `status.state`, `status.phaseReached`, and `status.executable`
4. make sure the resolved route for the selected assets is acceptable
5. if feed funding is needed:
   - branch on `fundingExecutionClassification.state`
   - execute direct or wrapper funding when `executable`
   - execute `browser-plan` plus browser automation when `browser-assisted`
   - re-run feed readiness after funding
6. continue through oracle prep, EVK market prep, and deployment
7. if artifacts were enabled, inspect `agent-decision.json`, `summary.json`, `rollback-plan.json`, `status.json`, `response.json`, and `deploy-evk-market.json`
8. run `verify-evk-deployment-handoff --run-dir <dir>` before claiming the deployment is ready for proof or operator handoff
9. if the user asked for borrow proof:
   - build a borrow-proof config from the deployment outputs plus proof-specific inputs
   - run preview mode first with `node scripts/evk_live_borrow_proof.js --config <path>`
   - only rerun with `--live` if the user wants the canary sent
10. report deployment and borrowability as separate outcomes

Use the staged commands directly only when you need narrower control than the top-level runner provides.

## Generalization rule
Treat the EVK planner path as asset-agnostic across supported pairs:
- do not special-case only previously tested collateral/borrow combinations
- use the same route-resolution, funding, deployment, and proof logic for whichever supported assets are selected
- treat prior successful canaries as evidence that the path can work, not as permission to hardcode those same examples into future planning

## Current executable happy path

### 1. `prepare-euler-oracle`
Use a direct `euler-chainlink-oracle` route or another oracle route that already resolves to executable oracle txs.

### 2. `prepare-evk-market`
Use a real recipe id from the bundled planner runtime in `scripts/lib/part2-recipes.js`. A current example is `eth-major-stable-borrow-v1` with `riskPreset: "eth-major"`.

### 3. `prepare-evk-deployment`
This is where the first executable EVK market transaction is unlocked.

### 4. `deploy-evk-market`
Use guarded broadcast opt-in and prefer dry-run first.

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
- `executable` → use exact onchain execution
- `browser-assisted` → call `browser-plan` and automate the Market flow with the browser tool when reachable
- `unsupported` → stop and report unsupported

After any funding execution step, re-run feed readiness before proceeding to oracle deployment.

## Post-deploy borrow proof step

After `deploy-evk-market`, do not stop at "deployment succeeded" if the user asked for proof of actual borrowability.

### Deployment output → proof config mapping
When building `borrow-proof-config.json`, map values deliberately instead of guessing:
- borrow vault address → from the deployed EVK market output, using the newly deployed borrow vault, not a prior canary vault
- collateral vault address → from the intended proof target, not from the borrow market manifest unless they are explicitly the same
- EVC address → from the deployed borrow vault's `EVC()` contract when available, otherwise from the deployment context for that chain
- borrow asset address and decimals → from the deployed borrow vault asset or the workflow request borrow asset, whichever is authoritative for the live market
- collateral asset address and decimals → from the chosen collateral vault's underlying asset
- wrapped native token → from the target chain, not hardcoded from Arbitrum examples
- signer env name → from local runtime setup, for example `LIVE_SIGNER_ENV`, never from committed files
- live acknowledgement → set the config's guarded live-send acknowledgement field only when the operator intends to allow a live proof send
- stale collaterals or controllers to disable → from the actual wallet state at proof time, not from a past example

If any of those mappings are ambiguous, stop and inspect chain state before constructing the proof config.

Use the local proof executor when the next question is any variant of:
- can this market really borrow?
- prove the isolated collateral path works
- show a live borrow canary
- rotate off the old collateral or controller and re-test

Minimum proof inputs:
- deployed borrow vault address
- intended collateral vault address
- EVC address
- borrow asset and collateral asset addresses plus decimals
- wrapped native token for the chain
- tiny borrow amount
- stale collaterals or controllers to disable if isolation matters
- swap venue details only if the wallet must source collateral or repay assets first

Treat these as distinct outcomes:
- deployment dry-run ready
- real-send ready
- deployed but borrow-proof pending
- live borrow proven

## Stop conditions

Stop and report instead of improvising when:
- `fundingExecutionClassification.state === "unsupported"`
- the browser-assisted funding UI is not reachable or cannot be automated safely
- `ensure-feeds` says the feeds are not ready and no supported exact buy-subscription path is available
- the oracle path is still skeleton-only
- `prepare-evk-deployment` does not include concrete top-level `vaultContext`
- `deploy-evk-market` still reports skeleton market transactions
- the proof step cannot honestly isolate or demonstrate the collateral path the user asked for

## Real-send rule

Only move beyond dry-run when the user explicitly wants live sending and the request includes:
- `broadcast.enabled: true`
- `broadcast.acknowledgement`: the exact required live-send acknowledgement phrase
- matching signer or executor identity
- `send.rpcUrl`
- `send.privateKey`

If any of those are missing, stay in planning or dry-run mode.

## Success-reporting rule
Treat the wrapper artifact bundle as the canonical evidence surface.

Before claiming deployment success, inspect at least:
- `result.artifactPersistence.files.status`
- `result.artifactPersistence.files.response`
- `result.artifactPersistence.files.summary`
- `result.artifactPersistence.files.agentDecision`
- `result.artifactPersistence.files.rollbackPlan`
- `result.artifactPersistence.files.deployEvkMarket`

For persisted runs, prefer:
- `explain-next --run-dir <dir>` for operator guidance
- `verify-evk-deployment-handoff --run-dir <dir>` for deployment-complete claims
- `run-evk-workflow --resume-from-run-dir <dir>` when continuing an existing run

Use `references/summary-contract.md` for the exact reporting contract.

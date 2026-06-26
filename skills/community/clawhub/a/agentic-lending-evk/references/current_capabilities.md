# Current capabilities and limits

This skill is intentionally honest about the current implementation.

## What works today

### Top-level EVK runner
- the skill has a true top-level runner: `run-evk-workflow`
- it takes one workflow request and returns one `{ status, result }` object
- it can infer `recipeId` when the current EVK recipe catalog yields one clear match
- it preserves the staged planner and executor outputs under `result` instead of hiding them behind an opaque success flag
- it now has a matching live-safety gate: `preflight-evk-workflow`
- the wrapper can persist a reviewable artifact bundle when `artifacts.enabled === true`
- persisted runs now carry `summary.json`, `agent-decision.json`, and `rollback-plan.json`
- persisted runs can now be reopened or interrogated with `run-evk-workflow --resume-from-run-dir`, `explain-next`, and `verify-evk-deployment-handoff`

### Feed and Api3 side
- agents can discover and resolve Api3 feeds
- agents can classify feed readiness
- agents can surface activation and funding handoff information
- agents can prepare some contract-call data for feed activation paths
- agents can use the first guarded exact `buySubscription(...)` execution paths in dry-run or explicitly acknowledged submit mode
- the supported execution modes are `direct`, `wrapper`, and `auto`, but wrapper only works when the repo already derives the exact wrapper calldata safely
- browser-assisted funding cases can now stay automatable through `browser-plan` plus browser execution when the required Market flow is reachable

### Oracle side
- `Api3PartialAggregatorV2V3Interface` deployment can be executable
- direct `ChainlinkOracle` deployment can be executable when constructor args are concrete
- wrapper-first `wrapper -> ChainlinkOracle` can become executable when execution-time nonce context is available
- composite `ChainlinkOracle + CrossAdapter` can become executable
- EVK bundle oracle transactions can dry-run cleanly when the oracle path is executable
- literal exact feed matching is preferred before alias-normalized fallback matching, so route resolution stays generic across supported assets instead of being accidentally biased toward alias families

### EVK market side
- the first honest executable EVK market transaction is the `deploy-evk-vault` call through `GenericFactory`
- this path depends on top-level `prepare-evk-deployment.vaultContext`
  - `factoryAddress`
  - `assetAddress`
- without that `vaultContext`, the market transaction stays skeleton-only and the bundle must stay non-ready

### Post-deploy proof side
- deployment and borrowability are treated as different claims
- this skill now includes its own post-deploy borrow proof step instead of relying on a separate published skill
- the controller → local-executor proof path is: deploy with this skill, then prove live borrowability with the bundled `scripts/evk_live_borrow_proof.js`
- this is the honest path for share-token collateral cases where oracle quoteability, EVC state, and tiny live borrow success all matter

## What does not yet work broadly
- Morpho workflow is not the target of this skill
- the EVK market deployment surface is still constrained by the currently supported recipes, oracle routes, and executor wiring
- `ChainlinkInfrequentOracle` is not yet treated as executable
- feed funding is still only fully onchain-executable for narrow supported exact buy-subscription paths
- browser-assisted funding cases still exist
- unsupported funding cases still exist
- this is not yet a polished "any agent can choose any supported assets and always complete everything" surface

## How to speak about status

When reporting progress, use one of these states explicitly:
- plan-only
- feed-ready but awaiting activation or funding handoff
- funding dry-run ready
- browser-assisted funding ready
- oracle-executable
- EVK dry-run ready
- real-send ready
- deployed but borrow-proof pending
- live borrow proven

When funding is involved, also surface the machine-usable funding branch:
- `fundingExecutionClassification.state = not-needed | executable | browser-assisted | unsupported`

When the top-level runner is used, also surface the machine-usable status object fields:
- `status.phaseReached`
- `status.state`
- `status.recipeId`
- `status.fundingExecutionState`
- `status.executable`
- `result.artifactPersistence`

Operational meaning:
- `not-needed` → feed already live, continue
- `executable` → use guarded exact onchain execution
- `browser-assisted` → use `browser-plan` and browser automation if the Market flow is reachable
- `unsupported` → stop and report

Do not collapse those into a single vague "ready".
Do not call something borrowable unless the post-deploy proof step has actually supported that claim.
Do not call something fully deployed from prose alone when the artifact bundle is missing or incomplete.

## Preflight rule
Before a live-capable EVK request, run `preflight-evk-workflow` first.

Use it to confirm:
- `safeToRun === true`
- `placeholderSafe === true`
- the preview `status` matches the expected workflow branch
- live-looking request fields are not still dummy values

If preflight fails, stop and fix the concrete blocker instead of pushing ahead optimistically.

## Artifact rule
For anything beyond casual planning, enable:

```json
{
  "artifacts": {
    "enabled": true,
    "label": "evk-run"
  }
}
```

That persisted bundle is the reliable handoff surface for:
- status review
- deployment review
- proof follow-up
- later audit of what the wrapper actually decided
- model-friendly next-step recovery via `agent-decision.json`
- deployment-complete handoff checks via `verify-evk-deployment-handoff`

Use these persisted-run helpers deliberately:
- `explain-next --run-dir <dir>` → recover the current model-friendly state
- `verify-evk-deployment-handoff --run-dir <dir>` → verify the deploy bundle is coherent enough for handoff/proof claims
- `run-evk-workflow --resume-from-run-dir <dir>` → reopen a known run instead of reconstructing it from memory

## Generalization rule
Treat the planner path as asset-agnostic across supported pairs:
- do not special-case only previously tested collateral/borrow combinations
- use the same route-resolution, funding, deployment, and proof logic for whichever supported assets are selected
- only claim executable readiness when the planner can resolve a concrete oracle path and concrete deployment payloads for those assets

## Recipe rule
Use real EVK recipes from the bundled planner runtime in `scripts/lib/part2-recipes.js`.
Do not invent recipe ids.

## Address rule
The example addresses in the repo docs are structurally valid but illustrative only.
Do not present them as recommended live deployment targets.

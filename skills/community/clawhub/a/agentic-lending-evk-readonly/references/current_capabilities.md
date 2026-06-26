# Current capabilities and limits

This skill is intentionally honest about the current implementation.

## What works today

### Top-level EVK runner
- the skill has a true top-level runner: `run-evk-workflow`
- it takes one workflow request and returns one `{ status, result }` object
- it can infer `recipeId` when the current EVK recipe catalog yields one clear match
- it preserves the staged planner and executor outputs under `result` instead of hiding them behind an opaque success flag

### Feed and Api3 side
- agents can discover and resolve Api3 feeds
- agents can classify feed readiness
- agents can surface activation and funding handoff information
- agents can prepare some contract-call data for feed activation paths
- agents can inspect guarded exact `buySubscription(...)` execution paths as dry-run or handoff artifacts without submitting them
- browser-assisted funding cases can stay reportable through `browser-plan` planning artifacts when the required Market flow is reachable

### Oracle side
- `Api3PartialAggregatorV2V3Interface` deployment can be assessed as executable
- direct `ChainlinkOracle` deployment can be assessed as executable when constructor args are concrete
- wrapper-first `wrapper -> ChainlinkOracle` can become assessable when execution-time nonce context is available
- composite `ChainlinkOracle + CrossAdapter` can become assessable
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
- this read-only skill does not include or invoke a live post-deploy borrow proof step
- the honest read-only path is: assess deployment readiness, then plan the proof inputs and checklist only
- this is the honest path for share-token collateral cases where oracle quoteability, EVC state, and tiny live borrow success would matter later

## What does not yet work broadly
- Morpho workflow is not the target of this skill
- the EVK market deployment surface is still constrained by the currently supported recipes, oracle routes, and executor wiring
- `ChainlinkInfrequentOracle` is not yet treated as executable
- feed funding is not executed by this skill; it is only classified as not-needed, executable in theory, browser-assisted, or unsupported
- browser-assisted funding completion is out of scope
- live funding, live deployment, and live borrow proof are out of scope
- this is not yet a polished "any agent can choose any supported assets and always complete everything" surface

## How to speak about status

When reporting progress, use one of these states explicitly:
- plan-only
- feed-ready but awaiting activation or funding handoff
- funding dry-run ready
- browser-assisted funding ready
- oracle-executable
- EVK dry-run ready
- real-send ready in theory but not available through this skill
- deployed but borrow-proof pending
- live borrow proven is out of scope

When funding is involved, also surface the machine-usable funding branch:
- `fundingExecutionClassification.state = not-needed | executable | browser-assisted | unsupported`

When the top-level runner is used, also surface the machine-usable status object fields:
- `status.phaseReached`
- `status.state`
- `status.recipeId`
- `status.fundingExecutionState`
- `status.executable`

Operational meaning:
- `not-needed` → feed already live, continue
- `executable` → onchain path exists, but this skill stops at reporting or dry-run artifacts
- `browser-assisted` → browser handoff exists, but this skill stops at planning
- `unsupported` → stop and report

Do not collapse those into a single vague "ready".
Do not call something borrowable unless a separate proof step has actually supported that claim.

## Generalization rule
Treat the planner path as asset-agnostic across supported pairs:
- do not special-case only previously tested collateral/borrow combinations
- use the same route-resolution, funding classification, deployment assessment, and proof-planning logic for whichever supported assets are selected
- only claim executable readiness when the planner can resolve a concrete oracle path and concrete deployment payloads for those assets

## Recipe rule
Use real EVK recipes from `src/part2-recipes.js`.
Do not invent recipe ids.

## Address rule
The example addresses in the repo docs are structurally valid but illustrative only.
Do not present them as recommended live deployment targets.

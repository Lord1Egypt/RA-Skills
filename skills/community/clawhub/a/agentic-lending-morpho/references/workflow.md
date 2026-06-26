# Morpho-first workflow

Use this as the default cold-start path.

## Canonical workflow
1. normalize the market request with `protocol = morpho`
2. require the agent to specify the exact `collateralAssets` and `borrowAssets`
3. resolve the oracle route for the requested assets
   - prefer an exact direct route when it exists and is deployable
   - otherwise use a supported composed route when the planner can prove the path cleanly
   - prefer literal exact feed-name matches before alias-normalized fallback matches
4. inspect required Api3 feeds and funding state for the resolved route
   - use canonical `feedFunding.mode` values in saved requests: `classify-only`, `dry-run`, `real-send`
   - tolerate `check-only` and `simulate` only as input aliases that normalize to the canonical values
5. branch on feed readiness:
   - already live on the deployable on-chain path
   - directly fundable
   - browser-assisted
   - unsupported
6. if funding is directly executable, run funding before any deployment step
   - default to also deploying any required communal proxy in the same scripted funding path unless the request explicitly disables that
   - in `dry-run`, preview the full chained deploy by threading the predicted adapter address into the market creation calldata
7. map the market to the Morpho oracle-adapter design
8. prefer `ensure-feeds-and-deploy-morpho-market` for the end-to-end path
   - expect explicit progress boundaries for preflight, feed classification, funding/handoff, propagation wait, deployment, and verification
   - long propagation waits should emit heartbeat-style “still working” progress instead of going silent
9. either:
   - emit a planning bundle plus implementation gap report, or
   - continue into executable Morpho deployment, then verify the market and oracle read path
   - for live deployment, re-thread market creation from the actual adapter deployment receipt address instead of relying only on predicted nonce math
10. persist and inspect `rollback-plan.json` in the run directory before sending any further dependent transactions

## Generalization rule
Treat the planner path as asset-agnostic across supported pairs:
- do not special-case only previously tested pairs
- use the same resolution, funding, deployment, and verification logic for whichever supported collateral and borrow assets are selected
- only stop when the route cannot be resolved cleanly, the funding path is unavailable, or the verification invariants cannot be satisfied

## Recommended reporting structure
For each run, report:
- normalized intent
- feed status
- approval summary (`approval-summary.json`) before live or heavy execution
- current phase / latest progress boundary
- oracle-adapter plan
- executable versus planning-only status
- rollback reality (`local-only` versus `forward-only onchain changes recorded`)
- blockers
- next commands or files to change

## Working implementation target
This skill should support:
- Morpho market intent normalization
- explicit collateral/borrow asset selection by the requesting agent
- Api3 feed readiness checks
- executable feed funding when supported
- Morpho oracle-adapter preparation and deployment
- Morpho market deployment and verification

When a request cannot reach deployment, fall back honestly to planning, funding handoff, or implementation-gap reporting.

## Packaged artifact note
In the published skill bundle, the shared planner data under `data/part2/` is packaged locally.
- prefer live RPC-backed feed checks when available
- fall back to bundled `feed-status.json` / `market-registry.json` only as packaged local snapshots
- do not describe those files as canonical global truth

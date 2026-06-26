# Morpho-first workflow

Use this as the default cold-start path.

## Canonical workflow
1. normalize the market request with `protocol = morpho`
2. require the agent to specify the exact `collateralAssets` and `borrowAssets`
3. resolve the oracle route for the requested assets
   - prefer an exact direct route when it exists and is usable
   - otherwise use a supported composed route when the planner can prove the path cleanly
   - prefer literal exact feed-name matches before alias-normalized fallback matches
4. inspect required Api3 feeds and funding state for the resolved route
5. branch on feed readiness:
   - already live on the deployable on-chain path
   - operator-fundable
   - browser-assisted
   - unsupported
6. do not execute funding; classify the required handoff instead
7. map the market to the Morpho oracle-adapter design
8. prefer read-only planning commands for the analysis path
9. either:
   - emit a planning bundle plus implementation gap report, or
   - continue into operator handoff planning, then verify any existing market and oracle read path that can be checked safely

## Generalization rule
Treat the planner path as asset-agnostic across supported pairs:
- do not special-case only previously tested pairs
- use the same resolution, funding-readiness analysis, deployment planning, and verification logic for whichever supported collateral and borrow assets are selected
- only stop when the route cannot be resolved cleanly, the funding path cannot be classified, or the verification invariants cannot be satisfied

## Recommended reporting structure
For each run, report:
- normalized intent
- feed status
- oracle-adapter plan
- executable versus planning-only status
- blockers
- next commands or files to change
- whether the current state is planning-only, funding handoff required, oracle-adapter design ready, market preparation ready, or operator-executable Morpho deployment handoff ready

## Working implementation target
This skill should support:
- Morpho market intent normalization
- explicit collateral/borrow asset selection by the requesting agent
- Api3 feed readiness checks
- feed funding readiness classification when supported
- Morpho oracle-adapter preparation
- Morpho market deployment planning and verification

When a request cannot reach operator-ready handoff, fall back honestly to planning, funding handoff, or implementation-gap reporting.

## Guardrails
- require explicit `collateralAssets` and `borrowAssets`; do not infer them from vague market names
- treat browser-assisted funding as an explicit operator handoff
- keep signer-backed submission and transaction execution out of scope for this skill
- require a usable RPC endpoint before claiming verified on-chain results

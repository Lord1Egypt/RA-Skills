---
name: agentic-lending-evk
description: Plan and execute the current EVK-first agentic lending workflow for Api3-backed markets. Use when a user wants an agent to resolve the oracle route for selected collateral and borrow assets, discover or fund the required Api3 feeds, including browser-assisted Api3 Market funding when needed, prepare the Euler oracle path, assemble and deploy the EVK lending market, and then prove real borrowability with a post-deploy canary borrow against the intended collateral path. This variant can reach real onchain writes, including feed funding, market deployment, approvals, swaps, and borrow canaries when explicitly allowed. Default to plan, simulation, or preview mode first, and only use live signer-backed execution when the user explicitly asks for it. Do not use for Morpho, unsupported recipes, or unsupported oracle/deployment routes.
metadata:
  clawdis:
    homepage: https://github.com/daav3/agentic-lending-project
    author: daav3
    requires:
      bins:
        - node
      env:
        - LIVE_SIGNER_ENV
      config:
        - request.run-evk-workflow.json
        - borrow-proof-config.json
    primaryEnv: LIVE_SIGNER_ENV
---

# Agentic Lending EVK

This is the execution-capable EVK workflow skill.

It turns the bundled EVK planner primitives into one agent-facing workflow, from route resolution and feed readiness through deployment and live borrow proof.

When the supported path is available and the user explicitly asks for it, this variant can send real transactions and should be treated as a guarded execution skill rather than a planning-only helper.

## Golden path for normal use
Use one request file and one wrapper command. Do not drop into lower-level commands unless debugging, intervention, or proof-specific follow-up is required.

1. Create `request.json` with exact `collateralAssets`, exact `borrowAssets`, chain, risk intent, feed-funding intent, and EVK deployment intent.
   - For a live-shaped starting point, copy `references/live-request-template.json` and replace every placeholder before use.
2. Preflight before any live-capable EVK execution:

   `agentic-lending-evk preflight-evk-workflow --input-file ./request.json --format json`

   Stop unless `safeToRun === true`.
3. Run:

   `agentic-lending-evk run-evk-workflow --input-file ./request.json --format json`

4. If the run was persisted, inspect or recover it with:
   - `agentic-lending-evk explain-next --run-dir <run-dir> --format json`
   - `agentic-lending-evk verify-evk-deployment-handoff --run-dir <run-dir> --format json`
   - `agentic-lending-evk run-evk-workflow --resume-from-run-dir <run-dir> --input-file <run-dir>/request.json --format json`
5. If the user asked for borrowability proof, continue with the bundled proof executor only after the deployment bundle is reviewed.
6. Report full deployment success only from persisted artifacts and exact status fields, not from narrative text.

## Safety expectations
- default to planning, simulation, or preview mode first
- treat browser-assisted funding as optional and only automate it when the user wants the flow completed end to end
- only use live signer-backed funding, deployment, or borrow canaries when the user explicitly asks for live execution
- for the bundled borrow-proof script, require both `--live` and the config's guarded live-send acknowledgement field to match the script's required phrase
- require the configured proof account address to match the signer address before any live proof transaction is sent
- require explicit nonzero swap protection for every live swap
- require explicit opt-in before using unlimited approvals
- keep private key material in environment variables or local runtime config, never in committed files

## Use this when
- the user wants to stand up or dry-run an EVK lending market backed by Api3 feeds
- the user wants one workflow instead of manually stitching planner JSON steps
- the task includes any combination of asset selection, oracle route resolution, feed readiness, feed funding, oracle preparation, EVK deployment prep, guarded dry-run or send, or post-deploy borrow proof

## Do not use this when
- the user wants Morpho, not EVK
- the requested recipe or oracle path is not supported by the current repo
- the task requires pretending a skeleton-only path is executable
- the task assumes fully autonomous feed funding in every case

## Read next
1. `references/api_reference.md`
2. `references/current_capabilities.md`
3. `references/summary-contract.md` before claiming deployment success from wrapper output
4. `references/live-borrow-checklist.md` when the workflow reaches post-deploy proof
5. `references/arbitrum-eusdc1-isolated-example.json` when a concrete proof config shape helps
6. Use the bundled executor at `scripts/evk_live_borrow_proof.js`
7. Treat bundled `data/part2/feed-status.json` and `data/part2/market-registry.json` as packaged local snapshots, not authoritative shared state

## Minimum required inputs for the combined flow
Gather these before you assume the full combined workflow is feasible:
- chain name and chain id
- collateral asset set and borrow asset set
- target recipe id or risk preset
- whether the user wants planning only, dry-run, or real send
- whether the user also wants post-deploy borrow proof
- live RPC availability for the chain
- signer expectations for any live funding, deployment, or proof step
- `vaultContext` when the deployment path needs concrete factory or asset wiring

For a full live end-to-end run, also confirm:
- feed funding branch expectations, especially whether `fundingExecutionClassification.state` may be `browser-assisted`
- browser access if the Api3 Market flow must be automated
- a safe tiny borrow amount for the proof step
- a target collateral vault for the proof, not just the borrow vault

If any of those are missing, stop and ask instead of improvising.

## Default workflow
1. Normalize the request into:
   - chain
   - collateral assets
   - borrow assets
   - target recipe or risk preset
   - whether the user wants planning only, dry-run, or real send
   - whether the user also wants proof of actual borrowability
2. Resolve the oracle path for the selected assets before treating deployment as executable.
   - prefer an exact direct route when the requested pair exists and is deployable
   - otherwise use a supported composed route when the planner can prove it cleanly
   - prefer literal exact feed-name matches before alias-normalized fallback matches
3. Prefer `preflight-evk-workflow`, then `run-evk-workflow`, as the default end-to-end entrypoints when the user wants the full EVK path.
   - `preflight-evk-workflow` is the live-safety gate for placeholder detection, preview status, and blocker surfacing
   - pass `recipeId` explicitly when known, otherwise let the runner infer from the current EVK recipe catalog
   - treat `status` as the canonical summary object
   - treat `result` as the detailed staged artifact bundle
   - enable `artifacts.enabled` whenever the run may need review, handoff, or a durable success claim
   - after a persisted run, prefer `agent-decision.json`, `summary.json`, and `rollback-plan.json` over ad-hoc interpretation
   - use `explain-next` for operator guidance, `verify-evk-deployment-handoff` for deployment-complete handoff checks, and `--resume-from-run-dir` when continuing a known run
4. If deployment succeeds and the user wants proof of actual borrowability, continue within this skill to the built-in post-deploy proof step.
   - treat deployment success and borrowability proof as separate milestones
   - use the deployment outputs plus live vault addresses, collateral-vault targets, EVC state, and tiny borrow sizing to build the proof config
   - require preview mode first, then live canary only if the user wants a real proof
5. Fall back to the manual staged commands only when the user asked for a subset, wants intervention at a specific phase, or the runner stops before the desired outcome.
   - `plan-market`
   - `ensure-feeds`
   - if feeds are live, continue to the oracle and EVK planner path
   - if funding is needed, inspect `purchase-inputs` or `prepare-buy-subscription` output and branch on `fundingExecutionClassification.state`
   - if `fundingExecutionClassification.state === "executable"`:
     - `purchase-inputs`
     - `prepare-contract-call` or `prepare-buy-subscription`
     - `execute-buy-subscription`
     - `ensure-feeds` or `ensure-active` again to confirm the feed is now live
   - if `fundingExecutionClassification.state === "browser-assisted"`:
     - call `browser-plan`
     - use the browser tool to execute the returned plan if the required UI is reachable and the user wants full automation
     - re-run `ensure-feeds` or `ensure-active` after the browser flow
   - if `fundingExecutionClassification.state === "unsupported"`, stop and report unsupported status clearly
   - `prepare-euler-oracle`
   - `prepare-evk-market`
   - `prepare-evk-deployment`
   - `deploy-evk-market`
   - the bundled `scripts/evk_live_borrow_proof.js` executor for the post-deploy proof step when requested
6. Stop and report honestly if:
   - feed funding is `unsupported`
   - the browser-assisted funding UI is not reachable or cannot be automated safely
   - the oracle path is still skeleton-only
   - the EVK market path is still skeleton-only
7. Prefer dry-run first for exact onchain funding and deployment paths.
8. For `browser-assisted` funding, prefer browser automation over asking the user to click through manually when the UI is reachable.
9. Only use real send when the user explicitly wants it and the guarded acknowledgement contract is present.
10. Keep the path generic across supported pairs.
   - do not special-case only previously tested collateral/borrow combinations
   - use the same resolution, funding, deployment, and proof rules for whichever supported assets are selected
11. Do not claim a market is borrowable just because deployment succeeded. A live or at least previewed post-deploy proof step is required for that claim.

## Built-in post-deploy borrow proof
Treat the published skill as a complete artifact: it includes the proof executor it tells the agent to run.

Bundled executor path:
- `scripts/evk_live_borrow_proof.js`

Bundled planner data path:
- `data/part2/`

Use the bundled planner data as the local default input set for this published skill. If the operator supplies fresher live RPC results or explicit `--registry-file` / `--feed-status-file` overrides, prefer those fresher inputs instead of pretending the packaged snapshots are always current.

Before a live-capable run, enable artifact persistence so the deployment and proof handoff do not depend on memory alone:

```json
{
  "artifacts": {
    "enabled": true,
    "label": "evk-live-run"
  }
}
```

Handoff contract:
1. generate `borrow-proof-config.json`
2. verify the bundled executor path exists in the installed skill
3. run preview first with `node ./scripts/evk_live_borrow_proof.js --config <path>`
4. rerun with `--live` only when the user explicitly wants the canary

The bundled executor supports:
- preview mode with a read-only account address
- live mode with a signer loaded from an environment variable
- optional debt repayment before the new proof
- optional single-hop Uniswap V3 style swaps to source repay or collateral assets
- collateral deposit into the target EVK vault
- disabling stale collateral vaults in EVC
- disabling stale controllers in EVC
- enabling the target collateral and optionally the target controller
- final tiny borrow and before or after logging

Keep the proof honest:
- distinguish mixed-collateral borrow from isolated target-collateral borrow
- preserve the exact funding branch that led here
- verify quoteability, LTV wiring, EVC state, and vault cash before a live canary
- if the chain does not use a Uniswap V3 compatible router, replace or bypass the bundled swap step explicitly
- require nonzero `amountOutMinimum` for live swaps
- keep approval scope exact unless the operator explicitly opts into `approvalPolicy.mode = "unlimited"`

## Current happy-path rule
The currently supported end-to-end EVK path requires:
- feeds that are already live, or a feed that can be activated through the current narrow exact `buySubscription(...)` path
- a cleanly resolved oracle path for the selected assets
- top-level `prepare-evk-deployment.vaultContext`
  - `factoryAddress`
  - `assetAddress`
- guarded send fields on the funding and deployment executor requests

Without that `vaultContext`, the first EVK market transaction remains skeleton-only and `readyToBroadcast` must stay false.
Without a supported exact buy-subscription path, feed funding must stay at handoff or prep only.

## Output expectations
When using this skill, always report:
- whether `preflight-evk-workflow.safeToRun` passed before any live-capable request
- `status.phaseReached` when the top-level runner is used
- `status.state` when the top-level runner is used
- `status.recipeId` when the top-level runner is used
- what is executable vs still skeleton-only
- blockers and warnings
- `fundingExecutionClassification.state` when feed funding is involved manually
- `status.fundingExecutionState` when the top-level runner is used
- `result.artifactPersistence.bundleDir` when artifacts were enabled
- whether the current state is:
  - plan-only
  - feed-ready but awaiting activation or funding handoff
  - funding dry-run ready
  - browser-assisted funding ready
  - oracle-executable
  - EVK dry-run ready
  - real-send ready
  - deployed but borrow-proof pending
  - live borrow proven

If the user asked for borrowability proof, also report whether the workflow has already reached the post-deploy proof step or is still waiting on proof inputs.

If the top-level runner is used, also surface the executable flags under `status.executable` instead of paraphrasing them away.

Do not claim final deployment success unless the wrapper artifacts support it. Read `references/summary-contract.md` and require at minimum:
- persisted `status.json` and `response.json`
- persisted `summary.json`, `agent-decision.json`, and `rollback-plan.json`
- `status.state === "real-send ready"` only for readiness, not success
- `deploy-evk-market.json` showing the intended deploy plan or live send result
- `verify-evk-deployment-handoff` passing when the run is being handed off as deployment-complete
- a separate proof status when borrowability was requested

## Tone
Be blunt about current limits.
Do not overclaim support beyond the routes the planner can actually resolve.
Do not blur deployment success into borrowability proof.
If the workflow falls off the happy path, say exactly where and why.

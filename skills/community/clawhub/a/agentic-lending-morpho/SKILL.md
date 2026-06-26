---
name: agentic-lending-morpho
description: Plan and execute the Morpho-first agentic lending workflow for Api3-backed markets. Use when a user wants a Morpho market or market set for selected collateral and borrow assets, needs the oracle route resolved for those assets, wants Api3 feed readiness checked or funded when safe, and then wants the Morpho oracle + market deployment and verification path run honestly. This variant can progress from planning into real feed funding and market deployment when the supported path is available and the user explicitly allows signer-backed execution. Default to planning, dry-run, or guarded verification first. Do not use for Euler EVK flows or unsupported oracle routes.
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
        - request.morpho-workflow.json
    primaryEnv: LIVE_SIGNER_ENV
---

# Agentic Lending Morpho

This is the execution-capable Morpho workflow skill.

It is the Morpho-side counterpart to the EVK skill. It is still more conservative than the EVK path, but it now supports a real end-to-end flow for compatible requests: resolve the requested collateral and borrow assets, check feed readiness, execute funding when available, deploy the oracle adapter, deploy the Morpho market, and verify the result.

This published skill carries its own local runtime and bundled planning artifacts under `scripts/lib/` and `data/part2/` rather than assuming a separate repo checkout is available at execution time.

It should script as much of the Morpho path as the code can honestly support: feed readiness classification, executable funding, communal proxy deployment when needed, propagation rechecks, adapter deployment, market deployment, verification, resumable artifacts, and a generated `rollback-plan.json` for every orchestrated run.

When the supported path is available and the user explicitly asks for it, this variant can send real transactions and should be treated as a guarded execution skill rather than a planning-only helper.

## Golden path for normal use
Use one request file and one wrapper command. Do not pick lower-level commands unless debugging or resuming a known run.

1. Create `request.json` with exact `collateralAssets`, exact `borrowAssets`, chain, RPC, Morpho policy, feed-funding intent, and send/broadcast intent.
   - For a live-shaped Arbitrum WETH/USDC example, copy `references/live-request-template.json` and replace every placeholder before use.
   - `feedFunding.mode` should be written with the canonical enum values: `classify-only`, `dry-run`, or `real-send`.
   - The runtime also accepts natural aliases (`check-only` → `classify-only`, `simulate` → `dry-run`), but docs and saved request files should stick to the canonical values.
   - Never paste a raw private key into chat. For live execution, point the request at a local environment variable such as `LIVE_SIGNER_ENV` via `feedFunding.privateKeyEnv` / `send.privateKeyEnv`.
2. Preflight before live-capable execution:

   `agentic-lending-morpho preflight-morpho-market --input-file ./request.json --format json`

   Stop unless `safeToRun === true`. Preflight rejects placeholder RPCs, dummy addresses, dummy private keys, mismatched RPC chain IDs, and missing live deployment policy.
3. Run:

   `agentic-lending-morpho ensure-feeds-and-deploy-morpho-market --input-file ./request.json --format json`

   - The wrapper now emits phase-by-phase progress on stderr for preflight, feed classification, funding/handoff, propagation wait, deployment, and verification.
   - Use `--progress jsonl` for machine-readable progress or `--progress silent` to suppress live progress output.

4. Inspect the persisted run directory, especially `approval-summary.json`, `agent-decision.json`, `summary.json`, `rollback-plan.json`, and `progress-events.jsonl`.
   - `approval-summary.json` is the explicit handoff artifact for user approval: what will run, whether it may send txs, expected duration, and likely resource impact.
5. Report full success only when `phase === "completed"`, there are no hard blockers, and `verifyResult.verified === true`.

If the run needs continuation, resume the same run directory rather than reconstructing state from memory:

`agentic-lending-morpho ensure-feeds-and-deploy-morpho-market --resume-from-run-dir <run-dir> --input-file <run-dir>/request.json --format json`

Timeouts and stalls should now name the stalled phase and point back to `--resume-from-run-dir` when that is the right recovery path.

## Safety expectations
- default to planning, dry-run, or guarded verification first
- only use signer-backed feed funding or market deployment when the user explicitly asks for it
- treat browser-assisted funding as an explicit handoff, not a silent autonomous path
- require exact asset selection before deployment planning or submission
- require a usable RPC endpoint for any on-chain verification claim
- never ask the user to paste a raw private key into chat
- keep signer material in environment variables or local runtime config, never in committed files or request templates

## Read next
1. `references/workflow.md`
2. `references/current_capabilities.md`
3. `references/morpho-oracle-adapter.md`
4. `references/state-machine.md` when feed activation and market deployment are both in scope
5. `references/summary-contract.md` before interpreting wrapper output or claiming success

## Minimum required inputs
Gather these before attempting a Morpho-first workflow:
- chain name and chain id
- explicit `collateralAssets`
- explicit `borrowAssets`
- target market shape or risk intent
- whether the user wants planning only, dry-run, or transaction submission
- live RPC availability for the chain if anything beyond planning is expected
- Morpho policy inputs needed for deployment on that chain when transaction submission is requested

If any of those are missing, stop and ask instead of inventing them.

## Request-shape rule
When preparing a request for this skill, always express the market assets explicitly as:
- `collateralAssets`: array of `{ symbol, address }`
- `borrowAssets`: array of `{ symbol, address }`

Do not leave asset selection implicit. The planner needs the exact collateral and borrow assets in order to resolve feeds, choose a direct-versus-composed oracle route, and verify the final market correctly.

For live execution, also include explicit `activationMode`, `executionMode`, `rpcPreference`, `morphoCoreAddress`, `morphoPolicy`, `feedFunding`, `send`, and `broadcast` fields. Use `references/live-request-template.json` as the starting shape, and check `references/deployment-packs/<chain>/` for chain-specific operator notes. Never use placeholder RPC URL, raw private keys, signer address, Morpho core address, IRM address, or LLTV without replacing and validating them. Bare 64-hex private keys are accepted and normalized to `0x...`, but environment-variable inputs remain the preferred documented path.

## Default workflow
1. Normalize the request into:
   - chain
   - `collateralAssets`
   - `borrowAssets`
   - protocol = `morpho`
   - market or risk intent
   - desired execution mode
2. Treat asset selection as a first-class input.
   - confirm the exact collateral asset set and borrow asset set the user wants
   - for multiple collateral assets, remember this becomes a Morpho **market set**: one market per supported collateral/borrow pair
3. Resolve the oracle path before any deploy step.
   - prefer a direct pair when the exact requested route is available and usable
   - otherwise use a supported composed route when the planner can prove it cleanly
   - keep feed-name matching generic: literal exact pair first, alias-normalized fallback second
4. Check feed readiness before deployment.
   - if feeds are already live on the deployable on-chain path, continue
   - if funding is needed and executable, run the funding path first
   - if funding executes, wait for live propagation/readability before deployment
   - if the funding branch is browser-assisted or unsupported, stop and report that honestly instead of pretending transaction submission can continue
5. Prefer the orchestration wrapper for the real sequence.
   - use `ensure-feeds-and-deploy-morpho-market` when the goal is to check feeds, fund if needed, deploy communal proxies when needed, wait for propagation, deploy, verify, and persist one coherent run directory
   - use lower-level commands only when debugging or resuming a prior run
6. Prepare and deploy the Morpho oracle adapter path.
   - use the Api3-backed Morpho oracle adapter design as the canonical oracle shape
   - preserve artifact handoff from adapter deployment into market deployment
   - keep proxy-first ordering whenever a communal proxy deploy is required
   - verify the adapter uses the same feed/proxy sources that were proven live
   - for dry-run previews, allow the planner to show both transactions by threading the predicted adapter address
   - for live send, require the market creation step to re-thread from the adapter deployment receipt address instead of trusting predicted nonce math alone
7. Verify the deployed market.
   - confirm the market exists on-chain
   - confirm params, IRM, and LLTV expectations
   - confirm oracle `price()` succeeds and is positive
8. Stop at the honest boundary.
   - if the request can only reach planning or funding handoff, say so clearly
   - do not present Morpho deployment as equivalent to the EVK live deploy path unless the code actually supports the requested environment
   - do not treat feed discovery, funding readiness, adapter design readiness, deployment readiness, and verified market creation as the same milestone

## Preferred command path
For a deployable request, prefer this command shape:

`agentic-lending-morpho ensure-feeds-and-deploy-morpho-market --input-file ./request.json`

Use it when the agent already has a concrete request file with the selected collateral and borrow assets.

Use `--resume-from-run-dir <dir>` when continuing a previously persisted run.

Check `agent-decision.json` first after wrapper runs. It is the small model-friendly status object with `safeStatus`, `nextCommand`, `mustNotDo`, and `successClaimAllowed`.

Check `rollback-plan.json` before sending any further dependent transactions. It records whether the run stayed local-only or already created forward-only onchain state.

Use these reliability commands when resuming or auditing:
- `agentic-lending-morpho explain-next --run-dir <dir> --format json`
- `agentic-lending-morpho verify-feed-to-market-handoff --run-dir <dir> --format json`

Treat bundled `data/part2/feed-status.json` and `data/part2/market-registry.json` as packaged snapshots. They are valid local inputs for fallback planning paths, but live RPC-backed checks still take precedence whenever the request needs a current on-chain claim.

## Success gates for less capable models
Do not infer success from narrative text. Use exact wrapper fields and artifacts. Read `references/summary-contract.md` for the full contract.

Minimum full-success predicate:
- top-level `phase` is `completed`
- `blockers` is absent or empty
- feed readiness is proven live, or post-funding `propagationResult.ready === true`
- `deployResult.sendSummary.completed === true` for live deployment claims
- `verifyResult.verified === true`
- `agent-decision.json.successClaimAllowed === true`
- `rollback-plan.json` has been inspected and reported as local-only or forward-only on-chain state

If any field is missing, say which artifact or field is missing instead of guessing.

## Feed-to-market handoff checks
Before saying the Morpho market uses the activated feed, prove the handoff in artifacts:
- the required feed route was resolved for the selected collateral/borrow pair
- the feed was already live, or funding/proxy deployment completed and propagation later reported ready
- any required communal proxy is deployed and readable before adapter deployment
- the deployed adapter references the activated feed/proxy source, not a stale or predicted-only address
- the created market uses the adapter output from this run
- verification reads the deployed market oracle and receives a positive `price()`

If those checks are too hard to prove from available artifacts, report `verification-ready` or `blocked`; do not report `completed`.

## Output expectations
Always report:
- whether the request was normalized successfully
- which collateral assets and borrow assets were selected for the Morpho market or market set
- whether the required Api3 feeds are already live, fundable, browser-assisted, or unsupported
- whether feed funding was executed, skipped as unnecessary, or handed off
- whether post-funding propagation/readability was proven before deployment
- whether the deployed adapter consumed the activated feed/proxy path
- whether the deployed market consumed the adapter output from the same run
- what oracle adapter shape is planned or deployed for Morpho
- which steps are planning-only versus executable today
- the exact wrapper phase: `plan-only`, `funding handoff required`, `feeds funded; waiting for propagation`, `market deployment ready`, `verification-ready`, `completed`, or `blocked`
- exact blockers preventing a full Morpho deployment flow, if any
- the next concrete command, file, or implementation gap to close

## Tone
Be blunt about current Morpho limits.
Do not blur design-doc intent into executable support.
But do not understate the implemented path either: if the selected-asset request is executable, say so plainly and use the resolve → feed-check → funding → deploy → verify sequence.

# Morpho feed-to-market state machine

Use this file when the request may activate Api3 feeds and then deploy a Morpho market. Follow states in order. Do not skip a state because a previous command looked successful.

## Golden rule
A Morpho market is not successfully deployed until the same run proves all four handoffs:

1. required feeds are live on the deployable path
2. required communal proxies are deployed and readable when needed
3. the Morpho oracle adapter uses those exact live feed/proxy sources
4. the Morpho market uses the deployed adapter and verifies on-chain

If any handoff is unproven, report the exact blocker and stop.

## States

| State | Required artifact/evidence | Allowed next action | Success gate | Stop/block when |
| --- | --- | --- | --- | --- |
| `request-normalized` | request JSON has `protocol`, `chain`, exact `collateralAssets`, exact `borrowAssets`, and `executionMode` | run the wrapper | assets are explicit; no inferred addresses | asset, chain, or execution intent is missing |
| `feeds-resolved` | wrapper initial workflow lists required feeds/routes | classify or fund feeds | every market has a clean direct/composed route | route is ambiguous or unsupported |
| `feeds-live` | `fundingResult` is unnecessary/already-live OR `propagationResult.ready === true` | deploy adapter/market through wrapper | every required feed is live after any funding | funding tx exists but propagation/readiness is not proven |
| `feeds-funded-awaiting-propagation` | `fundingResult.completedExecution === true` plus tx/proxy artifacts | wait/recheck propagation or resume from run dir | later `propagationResult.ready === true` | feed funding succeeded but feed is not yet readable/live |
| `communal-proxies-ready` | funding/proxy artifacts show deployed proxies where required | adapter deployment | all required proxy reads succeed | a feed needs a proxy and no deployed/readable proxy is proven |
| `adapter-deployed` | `deployResult` contains adapter deployment output | market creation/verification | adapter address exists and config points at required feed/proxy source | adapter address is predicted only, stale, or unconfirmed for live send; predicted-only is acceptable for dry-run preview but not as final live-send truth |
| `market-created` | `deployResult.sendSummary.completed === true` or market creation tx artifact | verify market | market creation tx completed and market params use deployed adapter | deploy result is planning-only/dry-run |
| `market-verified` | `verifyResult.verified === true` | report success | market exists, params match, and `oracle.price()` succeeds with positive value | verification skipped, failed, or only inferred from planning artifacts |

## Default command
Use the wrapper unless debugging or resuming:

```bash
agentic-lending-morpho ensure-feeds-and-deploy-morpho-market --input-file ./request.json --format json
```

For a previous run directory:

```bash
agentic-lending-morpho ensure-feeds-and-deploy-morpho-market --resume-from-run-dir ./artifacts/morpho-ensure-deploy/<run> --input-file ./artifacts/morpho-ensure-deploy/<run>/request.json --format json
```

## Weak-model operating checklist
Before reporting success, answer these with artifact fields, not prose:

- Did the request use exact collateral and borrow token addresses?
- Did the wrapper resolve every required feed route?
- Are all required feeds live after funding and propagation checks?
- Were required communal proxies deployed/readable before adapter deployment?
- Did the adapter use the exact activated feed/proxy sources?
- Did the market deployment use the adapter output from this run?
- Did verification prove the market exists and `oracle.price()` is positive?
- Does `rollback-plan.json` say whether any forward-only on-chain changes happened?

## Never do this
- Never deploy a Morpho market before feed readiness is live.
- Never treat a funding transaction hash as proof that the feed is usable.
- Never treat bundled `data/part2/feed-status.json` as current live truth for deployment.
- Never treat a predicted adapter address as sufficient evidence for a live chained deploy; use the deployment receipt address before market submission.
- Never call the market deployed if verification is skipped or failed.

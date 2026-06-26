# Current capabilities and limits

This skill is intentionally honest about the current Morpho state in the repo.

## What exists today
- the published skill now carries its own local runtime under `scripts/lib/`
- the published skill now carries its own packaged planning data under `data/part2/`, including shared planner snapshots and Morpho oracle artifacts
- the part 2 planner recognizes `protocol = morpho`
- the repo contains Morpho-first design work and oracle-adapter specifications
- Api3 feed discovery and readiness logic already exists at the project level
- the project has prior EVK skill patterns that can be reused for reporting, branching, and safety posture
- `prepare-morpho-market` exists at the planner layer
- `deploy-morpho-oracle-adapter`, `deploy-morpho-market`, and `verify-morpho-market` now exist at the planner layer
- `deploy-and-verify-morpho-market` exists as a one-shot wrapper around deploy plus verify artifact handoff
- `ensure-feeds-and-deploy-morpho-market` now exists as the Phase 1 orchestration wrapper for feed readiness, executable funding, propagation recheck, deploy, and artifact persistence
- the wrapper now has an initial Phase 2 resume path, so an operator can point it at a prior run directory and continue from stored request, completed funding, propagation, deploy, and verify artifacts instead of starting from zero
- funded-feed cache artifacts are now reusable across runs with `--funded-feed-cache-file <path>`; matching cache entries skip repeat funding classification/execution and force a live propagation recheck before deployment
- the packaged Morpho runtime can now use the newest bundled feed-funding logic, including communal proxy deployment during scripted funding flows when execution is allowed
- `feedFunding.mode` now documents and prefers the canonical enum `classify-only | dry-run | real-send`, while still accepting natural aliases such as `check-only` and `simulate`
- bare 64-hex private keys are now accepted and normalized to `0x...`, although `privateKeyEnv` remains the preferred operator path
- dry-run chained deployment previews can now show both the adapter deployment and market creation transactions by threading the predicted adapter address into the preview
- live chained deployment now re-threads market creation from the actual adapter deployment receipt address instead of trusting predicted nonce math alone
- every orchestrated Morpho run now writes `rollback-plan.json`, which records whether the run is still local-only or already has forward-only onchain changes that now need compensating-action thinking instead of fake “undo” language
- multiple deposit-asset intent is handled as a **Morpho market set**, meaning one Morpho market per collateral/loan asset pair rather than a fake multi-collateral single market

## What is not yet equivalent to EVK
- there is still not a Morpho deploy path as mature as the EVK workflow
- browser-assisted feed funding still requires a human handoff, it is not a silent end-to-end auto path
- the predicted-address preview used for `dry-run` is intentionally not the final source of truth for a live deploy; the live path now upgrades to the receipt-confirmed adapter address before market submission
- the wrapper now supports resume-from-run-directory for stored deploy/verify artifacts, completed funding artifacts, and reusable funded-feed cache inputs, but broader production run recovery is still incomplete, especially around policy-aware retries and richer operator decisions
- do not promise a live Morpho canary borrow path from this skill yet
- oracle-adapter work is still the critical bridge between Api3 feeds and Morpho market deployment
- on-chain verification depends on a real RPC plus the correct Morpho core and oracle addresses, so it is available but still environment-sensitive
- bundled `feed-status.json` and `market-registry.json` are local packaged snapshots, so they help planning and fallback behavior but should not be presented as fresher than live RPC-backed checks

## Practical meaning
Use this skill today for:
- Morpho-first planning
- explicit collateral-asset and borrow-asset selection for the target Morpho market or market set
- route resolution across supported pairs, including direct routes and supported composed routes
- feed-readiness analysis for the resolved oracle path
- funding-aware Morpho execution that can classify feed funding paths as ready, executable, browser-assisted, or unsupported before deployment continues
- Api3-backed oracle-adapter planning and deployment
- `prepare-morpho-market`
- `deploy-morpho-market` calldata planning and optional guarded transaction submission when the request includes a Morpho core address plus explicit send/broadcast inputs
- `verify-morpho-market` readback checks for created markets, IRM/LLTV enablement, and oracle `price()` sanity when the request includes a usable RPC endpoint
- `deploy-and-verify-morpho-market` when the operator already has feeds ready enough to proceed to deployment
- `ensure-feeds-and-deploy-morpho-market` when the operator wants one wrapper that can take the selected assets, classify or execute funding, wait for feed usability, deploy, persist a full run directory, write a funded-feed cache artifact, reuse that cache in a later run with `--funded-feed-cache-file`, and later resume verification or continuation from that run directory
- `ensure-feeds-and-deploy-morpho-market` when the operator also wants the run directory to include an explicit rollback/audit surface instead of only deploy/funding artifacts
- honest implementation-gap reporting

Do not use it to pretend the repo already has full EVK-style production hardening around every Morpho environment when it does not.

## Honest status language
Prefer one of these states explicitly:
- plan-only
- feed-ready but adapter-planning pending
- funding handoff required
- oracle-adapter design ready
- market preparation ready
- executable Morpho deployment ready

Only use `executable Morpho deployment ready` if the repo truly has the selected collateral and borrow assets, a cleanly resolved oracle path for those assets, the required Morpho core address, oracle addresses, IRM/LLTV policy inputs, a deliberate guarded send/broadcast path for the requested run, and a usable RPC endpoint for verification.

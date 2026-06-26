# Current capabilities and limits

This skill is intentionally honest about the current Morpho state in the repo.

## What exists today
- the part 2 planner recognizes `protocol = morpho`
- the repo contains Morpho-first design work and oracle-adapter specifications
- Api3 feed discovery and readiness logic already exists at the project level
- the project has prior EVK skill patterns that can be reused for reporting, branching, and safety posture
- `prepare-morpho-market` exists at the planner layer
- read-only planner and verification-oriented Morpho commands exist at the planner layer
- `verify-morpho-market` can support read-only verification planning when a market already exists
- planner-level feed readiness and Morpho preparation flows exist for read-only analysis and operator handoff planning
- prior run artifacts can still inform read-only analysis when an operator needs resume or handoff context
- funded-feed cache artifacts can inform read-only readiness analysis across runs
- multiple deposit-asset intent is handled as a **Morpho market set**, meaning one Morpho market per collateral/loan asset pair rather than a fake multi-collateral single market

## What is not yet equivalent to EVK
- there is still not a Morpho read-only-to-live transition path as mature as the EVK workflow
- browser-assisted feed funding still requires a human handoff
- resume-from-run-directory artifacts help read-only recovery and handoff analysis, but broader production recovery is still incomplete
- do not promise a live Morpho canary borrow path from this skill yet
- oracle-adapter work is still the critical bridge between Api3 feeds and any eventual Morpho market deployment
- on-chain verification depends on a real RPC plus the correct Morpho core and oracle addresses, so it is available but still environment-sensitive
- signer-backed funding or deployment stays outside this skill and should be treated as guarded operator actions

## Practical meaning
Use this skill today for:
- Morpho-first planning
- explicit collateral-asset and borrow-asset selection for the target Morpho market or market set
- route resolution across supported pairs, including direct routes and supported composed routes
- feed-readiness analysis for the resolved oracle path
- funding-aware Morpho analysis that can classify feed funding paths as ready, operator-executable, browser-assisted, or unsupported before any deployment handoff
- Api3-backed oracle-adapter planning
- `prepare-morpho-market`
- `prepare-morpho-market` calldata and dependency planning for later operator execution
- `verify-morpho-market` readback checks for created markets, IRM/LLTV enablement, and oracle `price()` sanity when the request includes a usable RPC endpoint
- read-only deployment and verification planning when the operator already has feeds ready enough to proceed
- read-only feed and deployment-prep analysis when the operator wants one place to classify readiness, inspect run artifacts, and prepare a later handoff
- honest implementation-gap reporting

Do not use it to pretend the repo already has full EVK-style production hardening around every Morpho environment when it does not.

## Honest status language
Prefer one of these states explicitly:
- plan-only
- feed-ready but adapter-planning pending
- funding handoff required
- oracle-adapter design ready
- market preparation ready
- operator-executable Morpho deployment handoff ready

Only use `operator-executable Morpho deployment handoff ready` if the repo truly has the selected collateral and borrow assets, a cleanly resolved oracle path for those assets, the required Morpho core address, oracle addresses, IRM/LLTV policy inputs, deployment dependencies mapped clearly for an operator handoff, and a usable RPC endpoint for verification.

Do not collapse these separate states into one vague success:
- feed-ready
- operator funding executable
- adapter plan complete
- market deployment plan complete
- market verified

# Morpho oracle adapter, Api3-backed

This reference captures the intended oracle shape for Morpho markets using Api3.

## Goal
Use Api3 data feeds as the pricing source for Morpho markets without relying on Euler-specific oracle assumptions.

## Core expectation
A Morpho-first workflow needs an oracle adapter layer that:
- reads the relevant Api3-backed price source
- exposes the interface expected by the Morpho deployment path
- preserves quote orientation and unit correctness for the intended market
- works generically across supported collateral/borrow pairs rather than being tied to a small set of previously tested examples

## Route-selection rule
Choose the oracle path for the selected assets in this order:
1. exact direct route when the requested pair exists and is deployable
2. supported composed route when the planner can prove the composition cleanly
3. stop and report the blocker when neither route is valid

When resolving feed names:
- prefer literal exact pair matching first
- use alias-normalized matching only as a fallback discovery mechanism
- do not let alias collisions override a valid literal route for the requested assets

## Agent guidance
When using this skill:
- do not assume the EVK oracle path can be reused unchanged
- explicitly verify the adapter interface the Morpho side expects
- distinguish between:
  - feed readiness
  - adapter design readiness
  - deployment executor readiness
- treat successful prior canaries as proof that the path can work, not as permission to special-case those same asset pairs in future planning

## Honest boundary
If the selected environment only reaches design or planning, say so plainly.

If the request can reach executable deployment, also say so plainly.

Do not collapse these different states into one claim:
- the Api3 oracle route is designed
- the Morpho adapter is specified
- the packaged executor can deploy for this request
- the deployed market was actually verified on-chain

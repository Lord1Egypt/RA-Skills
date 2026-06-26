# Morpho oracle adapter, Api3-backed

This reference captures the intended oracle shape for Morpho markets using Api3.

## Goal
Use Api3 data feeds as the pricing source for Morpho markets without relying on Euler-specific oracle assumptions.

## Core expectation
A Morpho-first workflow needs an oracle adapter layer that:
- reads the relevant Api3-backed price source
- exposes the interface expected by the Morpho deployment path so operator deployment can happen later
- preserves quote orientation and unit correctness for the intended market
- works generically across supported collateral/borrow pairs rather than being tied to a small set of previously tested examples

## Route-selection rule
Choose the oracle path for the selected assets in this order:
1. exact direct route when the requested pair exists and is usable
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
  - deployment handoff readiness
  - verified market readiness
- treat successful prior canaries as proof that the path can work, not as permission to special-case those same asset pairs in future planning
- require exact selected collateral and borrow assets before treating the adapter plan as handoff-ready

## Honest boundary
If the repo only contains the adapter spec and not a working live executor, say:
- the Api3 oracle route is designed
- the Morpho adapter is specified
- the live deployment path still needs implementation or explicit operator execution

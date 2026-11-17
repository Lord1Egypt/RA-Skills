# Delivery-router field handbook

## First customer contact

Establish who made the request, who performs the work, how a recent real task unfolded, why the issue matters now, what decision the engagement should enable, and which data, systems, and risk owners can participate. Ask for examples and demonstrations rather than asking whether “requirements are clear.”

## Common starting points

| Customer statement | Signal | Route |
|---|---|---|
| “We want an AI assistant.” | Solution idea without validated problem | Stage 1 |
| “Here are 30 interviews.” | Evidence without a decision | Stage 1 |
| “Can this problem be verified in two weeks?” | POC alignment needed | Stage 2 |
| “The charter is approved; write the specification.” | Verify charter, then hand off | Stage 3 |
| “The PRD is ready; how should we integrate it?” | Technical implementation | Stage 4 |
| “Turn this workflow into a reusable skill.” | Skill packaging | Stage 5 |
| “The demo is ready; how do we accept it?” | Run and evidence | Stage 6 |
| “It works, but nobody uses it.” | Adoption problem | Stage 7 |
| “We have delivered this three times.” | Productization candidate | Stage 8 |

## Urgent demonstrations

Separate the demonstration path from the verification path. Freeze demo data and non-extrapolable conclusions, prohibit temporary elevated permissions, agree on the decision and evidence needed after the demo, and publish only verified results with their limitations.

## Parallel work

Interviews and data analysis may run together. Once Stage 3 is stable, architecture exploration and skill prototyping may run in parallel. Collect Stage 7 leading indicators during Stage 6. Do not parallelize PRD, architecture, and skill design before scope and criteria are frozen; do not build integrations before permissions are known.

## Status and scope drift

- Green: gates passed; owner and next action are clear.
- Yellow: a non-blocking gap has an owner and deadline.
- Red: evidence, responsibility, executability, or risk blocks progress.
- Gray: paused pending an external change.

Revisit the charter when users, systems, data, write permissions, criteria, decision owners, security constraints, or time-boxed scope change.

## Failure review

Check problem evidence, customer contribution, frozen criteria, PRD testability, architecture realism, skill guardrails, preserved run failures, adoption, value attribution, and reusable learning—in that order.

End every stage with a short handoff: decision, evidence location, unknowns, risk owner, receiving stage, and rollback condition.

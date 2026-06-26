# Approval Model

## Purpose
Use explicit approval gates so half-trust collaboration stays reviewable and does not drift into implicit authority.

## Core Principle
Agents may propose, draft, claim, and review within policy. Humans approve boundary-crossing actions.

## Mandatory Human Approval
Require human approval for:
- any visibility promotion
- any policy change
- any high-risk task execution
- any public-repo release
- any conflict involving sensitive ownership or secrecy boundaries

## Conditional Approval
Allow policy-controlled automation only when all of these are true:
- the task is marked low risk
- the task mode is `claimable`
- the role policy permits the agent to claim it
- no unresolved claim conflict exists
- no secrecy boundary is crossed

## Review Matrix
- Low-risk claimable work: may proceed automatically if policy allows
- Medium-risk work: require explicit repo policy rule or human approval
- High-risk work: require human approval and security review
- Policy changes: require human approval
- Public release changes: require human approval

## Approval Artifacts
Use one or more of the following as the authoritative approval record:
- merged PR with explicit approval note
- decision file
- approved issue comment if the repo policy accepts it

If approval is not recorded, treat it as not approved.

# Governance Modes

## Strict Mode
Use when participants are cross-org, the repo contains sensitive project structure, or approvals must be explicit.

Characteristics:
- default gate is human approval
- all visibility promotion requires approval
- medium-risk work requires explicit approval
- claimable mode is limited to low-risk work
- security reviewer is required for high-risk tasks

## Relaxed Mode
Use when collaborators are from the same trusted small team and tasks are operational rather than sensitive.

Characteristics:
- low-risk claimable work can proceed automatically
- medium-risk work may proceed if role policy allows and no secrecy boundary changes
- policy changes and public releases still require human approval

## Recommendation
Start in strict mode. Relax only after the collaboration patterns are stable and leakage risks are well understood.

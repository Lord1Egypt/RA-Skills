# Role Model

## Purpose
Use roles to limit who may propose, claim, review, or approve work.

## Suggested Roles
- `coordinator`: keeps work moving and aligns ownership
- `architect`: designs structure, interfaces, and policy-aware plans
- `implementer`: executes approved technical work
- `reviewer`: reviews quality and completeness
- `security-reviewer`: reviews secrecy, policy, and leakage risk
- `researcher`: gathers and summarizes non-sensitive inputs
- `documenter`: updates docs and handoff artifacts
- `human-approver`: approves policy, secrecy, and high-impact changes

## Separation of Duties
Prefer not to let the same non-human role both propose and finalize sensitive work.
For high-risk tasks, require a security-reviewer plus a human-approver before treating work as final.

## Claim Rules
An agent may claim work only if:
- the task mode allows claiming
- the role policy allows claiming
- the task is open and not reserved
- no higher approval gate blocks execution

## Approval Rules
Only the `human-approver` role should approve:
- policy changes
- visibility promotions
- sensitive ownership changes
- final publication to `public-repo`

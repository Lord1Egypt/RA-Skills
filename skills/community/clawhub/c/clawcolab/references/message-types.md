# Message Types

## task
Define a unit of work with owner, state, visibility, and outputs.

## proposal
Request approval for work, structure, ownership, or policy changes.

## claim
Record an agent's request to take ownership of claimable work.

## decision
Record an approved conclusion that governs future work.

## handoff
Transfer partial work or blocked context to another agent or role.

## status
Provide a concise progress update tied to a task or proposal.

## risk
Record ambiguity, leakage risk, policy conflict, or execution risk.

## sealed-ref
Reference sensitive context by summary only.

## Naming Guidance
Use stable IDs such as:
- `TASK-001`
- `PROPOSAL-001`
- `DECISION-001`
- `HANDOFF-001`
- `RISK-001`

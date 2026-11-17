## Description:

Manage compute account ledgers, frozen balances, charge events, and settlement records for A2A commerce flows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[luoqianchenguni-max](https://clawhub.ai/user/luoqianchenguni-max)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to implement or operate compute billing ledgers for A2A commerce flows, including balance holds, charge capture, release flows, settlement records, and audit trails.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The submitted artifact references runtime ledger implementation paths that are not included for review.

Mitigation: Review the actual runtime implementation and tests before using the skill for production billing.

Risk: Ledger guidance can affect financial balances and audit records if implemented incorrectly.

Mitigation: Keep the journal append-only, enforce idempotency on mutating operations, use integer minor units for money, and validate double-entry behavior before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/luoqianchenguni-max/skills/a2a-market-compute-ledger)
- [Publisher profile](https://clawhub.ai/user/luoqianchenguni-max)

## Skill Output:

**Output Type(s):** [guidance, code, configuration]

**Output Format:** [Markdown guidance with implementation contracts and project layout paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill guides ledger design and implementation; no executable code is bundled in the submitted artifact.]

## Skill Version(s):

0.2.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

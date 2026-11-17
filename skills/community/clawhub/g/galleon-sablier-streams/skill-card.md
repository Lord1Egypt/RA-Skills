## Description:

Guides Sablier Flow stream and Lockup vesting actions with product-specific obligations, current rights checks, and evidence-backed reconciliation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[galleonlabs](https://clawhub.ai/user/galleonlabs)

### License/Terms of Use:

MIT

## Use Case:

Developers and operators use this skill to plan or review Sablier stream creation, funding, withdrawals, pausing and cancellation, and to distinguish accrued obligations from funds actually available or received.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An incorrect chain, recipient, token, amount, or approval could move funds unexpectedly.

Mitigation: Review the exact chain, deployment, current rights, recipient, amount, approval, calldata, simulation, and receipt before signing.

Risk: Stream debt or vested value may be mistaken for tokens already received.

Mitigation: Report accrued, covered, uncovered, withdrawable, and received amounts separately using observed onchain state.

Risk: Cancelling or voiding a stream may be irreversible or exceed the requested action.

Mitigation: Confirm the requested scope and current permissions; distinguish a pause from termination and reconcile each committed change.

## Reference(s):

- [Sablier module procedures and sources](artifact/references/modules.md)
- [Sablier worked calculations and recovery](artifact/references/examples.md)
- [Sablier Flow overview](https://docs.sablier.com/concepts/flow/overview)
- [Sablier Flow deployments](https://docs.sablier.com/guides/flow/deployments)
- [Sablier cancelability](https://docs.sablier.com/concepts/cancelability)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Unsigned transaction calls]

**Output Format:** [Markdown with amounts, state evidence, and optional unsigned calls or observed receipts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Identifies chain, deployment, current rights, obligations, observation time, and missing facts.]

## Skill Version(s):

0.2.1 (source: release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

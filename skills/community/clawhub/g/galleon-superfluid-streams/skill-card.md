## Description:

Guides planning, adjusting, stopping, and reconciling Superfluid streams, distribution pools, token wrapping, and scheduler operations with funding and permission checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[galleonlabs](https://clawhub.ai/user/galleonlabs)

### License/Terms of Use:

MIT

## Use Case:

Developers and DeFi users use this skill to plan and review recurring Superfluid obligations, operator permissions, funding horizons, and the observed outcome of authorized actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An incorrect recipient, rate, or funding estimate can create an unintended recurring financial obligation.

Mitigation: Verify recipients, exact rates, spendable balance, locked buffers, and conservative funding horizons before signing.

Risk: Broad approvals, operator permissions, or unexecuted schedules can permit spending beyond the intended limit.

Mitigation: Review allowances, permission scope and expiry, decoded calls, and actual schedule execution and flow state.

## Reference(s):

- [Superfluid streams release](https://clawhub.ai/galleonlabs/skills/galleon-superfluid-streams)
- [Superfluid implementation tracks](references/operations.md)
- [Superfluid worked records](references/examples.md)
- [Superfluid SDK documentation](https://sdk.superfluid.pro/docs)

## Skill Output:

**Output Type(s):** [Guidance, Analysis, Code]

**Output Format:** [Markdown with transaction details and optional unsigned calls or confirmed receipts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes observed chain, token, rate, funding horizon, permissions, and remaining gaps.]

## Skill Version(s):

0.2.1 (source: frontmatter and ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

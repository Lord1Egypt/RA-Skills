## Description:

Use when preparing, adjusting, stopping or reconciling Superfluid CFA streams, GDA distribution pools, Super Token wrapping, or stream and vesting scheduler operations. Inspect real-time funding and flow-operator rights before committing a recurring obligation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[galleonlabs](https://clawhub.ai/user/galleonlabs)

### License/Terms of Use:

MIT

## Use Case:

Developers and protocol operators use this skill to prepare and reconcile Superfluid CFA streams, GDA distributions, token wrapping, and scheduler actions. It guides funding and permission checks, action review, and verification of resulting state.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Recurring flows can continue transferring value, and an incoming flow may stop and shorten the funding horizon.

Mitigation: Check real-time spendable funding, aggregate outgoing rates, required buffer, and a conservative horizon that does not rely on uncertain incoming flows; set a budget and monitoring obligation.

Risk: A configured scheduler or automation does not establish that a stop or other action executed.

Mitigation: Check current permissions and execution status, then verify the receipt and current flow or pool state after the scheduled boundary.

Risk: The security review was partial because one local reference did not resolve.

Mitigation: Review the relevant local guidance before relying on the skill; the benign verdict is not a guarantee of safety.

## Reference(s):

- [Current implementation tracks](references/operations.md)
- [Worked funding and failure records](references/examples.md)
- [Official Superfluid skills](https://github.com/superfluid-org/skills)
- [Superfluid SDK documentation](https://sdk.superfluid.pro/docs)
- [SDK guidance](https://github.com/superfluid-org/skills/blob/main/skills/superfluid/references/guides/sdks.md)
- [Superfluid architecture guide](https://github.com/superfluid-org/skills/blob/main/skills/superfluid/references/guides/architecture.md)
- [Flowing balances guide](https://github.com/superfluid-org/skills/blob/main/skills/superfluid/references/guides/flowing-balances.md)
- [Superfluid contract references](https://github.com/superfluid-org/skills/tree/main/skills/superfluid/references/contracts)
- [Macro clear-signing guide](https://github.com/superfluid-org/skills/blob/main/skills/superfluid/references/guides/clear-macro.md)
- [Macro forwarder guide](https://github.com/superfluid-org/skills/blob/main/skills/superfluid/references/guides/macro-forwarders.md)
- [Flow scheduler guide](https://github.com/superfluid-org/skills/blob/main/skills/superfluid/references/subgraphs/flow-scheduler-guide.md)
- [Vesting scheduler guide](https://github.com/superfluid-org/skills/blob/main/skills/superfluid/references/subgraphs/vesting-scheduler-guide.md)
- [AutoWrap guide](https://github.com/superfluid-org/skills/blob/main/skills/superfluid/references/subgraphs/auto-wrap-guide.md)

## Skill Output:

**Output Type(s):** [Markdown, Guidance, Analysis, Code, Configuration]

**Output Format:** [Markdown decision record with rates, funding assumptions, permissions, unsigned calls or confirmed receipts, and observed state]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes observation time and remaining gaps; examples are synthetic and do not imply chain or account access.]

## Skill Version(s):

0.3.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

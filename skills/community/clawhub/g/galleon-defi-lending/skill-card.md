## Description:

Guides research, lending position planning, and liquidation-risk monitoring across Aave, Morpho, Compound, Euler, and Spark.

This skill is ready for commercial/non-commercial use.

## Publisher:

[galleonlabs](https://clawhub.ai/user/galleonlabs)

### License/Terms of Use:

MIT

## Use Case:

DeFi users and developers use this skill to compare lending markets, assess position and liquidation risk, prepare unsigned supply, borrow, repay, or withdrawal plans, and reconcile authorized transactions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Stale or incorrect lending data can misstate borrowing costs or liquidation risk.

Mitigation: Use trusted provider tools to check current state, rates, and risk; simulate the complete unsigned plan before signing.

Risk: Unreviewed approvals or signatures can grant unintended control of funds.

Mitigation: Review every approval and unsigned transaction, require authorization for the specific action, and never provide seed phrases or private keys.

## Reference(s):

- [Galleon DeFi Lending release](https://clawhub.ai/galleonlabs/skills/galleon-defi-lending)
- [Lending providers and versions](references/providers.md)
- [Lending workflows and evaluation cases](references/workflows.md)
- [Aave documentation](https://aave.com/docs/llms.txt)
- [Morpho agent skills](https://docs.morpho.org/developers/agents/skills/)

## Skill Output:

**Output Type(s):** [Text, Guidance]

**Output Format:** [Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports source and observation time, assumptions, position risk, approval scope, simulation, and transaction status when applicable.]

## Skill Version(s):

0.3.1 (source: frontmatter and server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

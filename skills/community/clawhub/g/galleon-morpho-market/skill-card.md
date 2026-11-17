## Description:

Evaluates a specific Morpho Blue market or vault allocation for oracle, collateral, borrowing, liquidity, and exit risk.

This skill is ready for commercial/non-commercial use.

## Publisher:

[galleonlabs](https://clawhub.ai/user/galleonlabs)

### License/Terms of Use:

MIT

## Use Case:

Analysts, developers, and DeFi users use this skill to assess a Morpho market or vault allocation, including liquidation exposure and whether an account can exit. It produces an evidence-based decision record rather than an automatic investment or transaction decision.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Incomplete or stale oracle, debt, or withdrawal data can misstate liquidation and exit risk.

Mitigation: Check the selected deployment and current onchain observations, accrue debt correctly, and withhold an APY ranking when oracle or exit liquidity is unknown.

Risk: An unreviewed transaction sequence could lead to unintended spending or losses.

Mitigation: Review and simulate any requested sequence; never provide keys or signing authority to the agent, and keep signing and broadcasting under explicit user control.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/galleonlabs/skills/galleon-morpho-market)
- [Morpho evidence worksheet](references/recipe.md)
- [Morpho core contracts and deployments](https://docs.morpho.org/developers/contracts/)
- [Morpho liquidation concepts](https://docs.morpho.org/learn/concepts/liquidation/)
- [Morpho legacy vault queues](https://docs.morpho.org/curate/tutorials-v1/manage-markets/)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, Shell commands]

**Output Format:** [Markdown decision record with optional unsigned transaction steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes chain, market or vault identity, observation block/time, assumptions, exit constraints, and missing evidence.]

## Skill Version(s):

0.3.1 (source: skill frontmatter and ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

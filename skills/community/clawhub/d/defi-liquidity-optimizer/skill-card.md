## Description:

Automated liquidity provision optimizer for CLMM DEXs on Solana and Ethereum that compares APR yields, estimates impermanent loss scenarios, scores pool safety by TVL, and recommends rebalancing when positions move out of range.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ssidharhubble](https://clawhub.ai/user/ssidharhubble)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and DeFi operators use this skill to compare concentrated liquidity pools, estimate impermanent loss exposure, and generate text-based rebalancing guidance for LP positions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: DeFi reports may materially misstate financial risk or overstate optimization quality.

Mitigation: Independently verify calculations, formulas, pool data, and assumptions before using outputs for investment, liquidity allocation, or rebalancing decisions.

Risk: The artifact uses mock pool data structures while describing production integrations.

Mitigation: Connect only reviewed and trusted live data sources, and clearly label generated reports with the data source and timestamp before operational use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ssidharhubble/skills/defi-liquidity-optimizer)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands and text reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces comparative pool analysis, APR rankings, impermanent loss estimates, and rebalancing recommendations.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

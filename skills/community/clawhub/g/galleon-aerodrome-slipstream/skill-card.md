## Description:

Guides evaluation, staking, claiming, withdrawal, and exit of Aerodrome Slipstream concentrated-liquidity NFT positions on Base.

This skill is ready for commercial/non-commercial use.

## Publisher:

[galleonlabs](https://clawhub.ai/user/galleonlabs)

### License/Terms of Use:

MIT

## Use Case:

Developers and liquidity providers use this skill to verify a Base Slipstream NFT's custody, range, gauge eligibility, and rewards before preparing an unsigned stake, claim, or exit action.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Incorrect position, contract version, or reward estimate could lead to a costly liquidity action.

Mitigation: Verify Base position custody, contract addresses and deployed version, then simulate exact action terms before use.

Risk: A proposed approval or transaction could move assets unexpectedly.

Mitigation: Treat the output as advisory only; require explicit user confirmation in a separate authorized wallet tool before signing.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/galleonlabs/skills/galleon-aerodrome-slipstream)
- [Slipstream contract recipes](references/recipes.md)
- [Aerodrome liquidity documentation](https://github.com/aerodrome-finance/docs/blob/main/content/liquidity.mdx)
- [Slipstream contracts and deployments](https://github.com/aerodrome-finance/slipstream)
- [Slipstream gauge interface](https://github.com/aerodrome-finance/slipstream/blob/main/contracts/gauge/interfaces/ICLGauge.sol)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands]

**Output Format:** [Markdown with read-only commands and an optional unsigned action packet]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Position and reward estimates are tied to a verified Base block and deployed contract version; no signing or transfer is authorized.]

## Skill Version(s):

0.6.1 (source: frontmatter and release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

Guides developers in batch-distributing ERC-20 tokens or ETH to up to 200 recipients through Spraay Protocol and DEX integrations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[plagtech](https://clawhub.ai/user/plagtech)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and pool operators use this skill to plan and implement batch token or ETH payouts, such as airdrops, holder rewards, and revenue shares, using Spraay's DEX adapters.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unreviewed SDK dependencies or contract addresses could put wallet funds at risk.

Mitigation: Review the npm package and verify contract addresses before installing or approving transactions.

Risk: Incorrect recipients, amounts, or approvals can cause costly blockchain transfers.

Mitigation: Check recipient lists and amounts off-chain, estimate costs, bound approvals, and test a small transfer before distributing at scale.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/plagtech/skills/dex-batch-distribution)
- [Spraay DEX adapters SDK](https://www.npmjs.com/package/@spraay/dex-adapters)
- [Uniswap V4 hook source](https://github.com/plagtech/spraay-uniswap-v4-hook)
- [PancakeSwap Infinity hook source](https://github.com/plagtech/spraay-pancakeswap-infinity-hook)
- [Base BatchDistributeHook contract](https://basescan.org/address/0xB9c1aB7BD023C784c19B8e9F10CE9CDEd9fF9010#code)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands]

**Output Format:** [Markdown with TypeScript and shell examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Covers generic and DEX-specific integrations, cost estimation, and pre-transfer checks.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

Manage Solana mainnet onchain funds by reviewing fund data, creating token baskets, depositing or redeeming, rebalancing, swapping tokens, and checking wallets and portfolios.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rplknt](https://clawhub.ai/user/rplknt)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can use this skill to inspect DFM funds and portfolios, create or manage token baskets, and perform fund or wallet transactions on Solana. It handles real-money activity, so transaction requests require clear user authorization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can move real funds, and allocation checks may lead to trades without explicit approval.

Mitigation: Use read-only access until allocation checks are separated from trading; require explicit approval for every money-moving action, including swaps, and limit wallet funding. Do not treat optional phrase confirmation as approval for swaps.

## Reference(s):

- [DFM app](https://app.dfm.finance)
- [DFM documentation](https://app.dfm.finance/docs)
- [DFM fees documentation](https://app.dfm.finance/docs/fees)
- [DFM agent MCP package](https://www.npmjs.com/package/@dfm-fi/agent)
- [ClawHub release page](https://clawhub.ai/rplknt/skills/dfm-fund-manager)

## Skill Output:

**Output Type(s):** [Fund and portfolio data, API call results, Transaction status and signatures, Guidance]

**Output Format:** [Structured tool responses summarized in natural-language text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses may include live onchain values and pending transaction statuses that need follow-up checks.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

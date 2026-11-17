## Description:

Compares DeFi savings and strategy vaults and helps plan deposits, exits, and tokenized-yield maturities across Pendle, Yearn, Spark, Morpho, Euler, and Ethena.

This skill is ready for commercial/non-commercial use.

## Publisher:

[galleonlabs](https://clawhub.ai/user/galleonlabs)

### License/Terms of Use:

MIT

## Use Case:

People comparing DeFi yield positions and developers preparing vault or maturity workflows use this skill to assess returns, liquidity, risks, and transaction terms before wallet approval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Yield comparisons and transaction plans can be mistaken for financial advice or guaranteed returns.

Mitigation: Treat outputs as financial preparation; verify rate assumptions, current liquidity, maturity terms, and underlying loss exposure before deciding.

Risk: Incorrect transaction details or broad approvals can cause unexpected asset movement or losses.

Mitigation: Review each contract, recipient, allowance, slippage or loss limit, and signer prompt before approving with a wallet; require explicit authorization for the exact action.

## Reference(s):

- [Galleon DeFi Yield release](https://clawhub.ai/galleonlabs/skills/galleon-defi-yield)
- [Yield providers and integration routes](artifact/references/providers.md)
- [Yield comparison and exit workflows](artifact/references/workflows.md)
- [Pendle V2 API documentation](https://api-v2.pendle.finance/core/docs)
- [Yearn vault documentation](https://docs.yearn.fi/developers/smart-contracts/V3/VaultV3)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, Unsigned transaction plans]

**Output Format:** [Markdown text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Source-backed comparisons and explicit approval, loss, slippage, liquidity, and settlement checks; no automatic trading.]

## Skill Version(s):

0.2.1 (source: release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

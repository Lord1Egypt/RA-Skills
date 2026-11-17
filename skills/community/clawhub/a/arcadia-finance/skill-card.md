## Description:

DeFi liquidity management on Uniswap and Aero, live on Base, Optimism, Unichain and Robinhood. Deploy concentrated liquidity positions with automated rebalancing, compounding, yield optimization, and leverage, or provide single-sided liquidity to lending pools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thomas-smets](https://clawhub.ai/user/thomas-smets)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to inspect Arcadia accounts, strategies, and lending pools, then prepare liquidity-management and lending transactions or automation requests on supported chains.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Calls send public wallet and account addresses and transaction parameters to the configured Arcadia MCP service; host runtime permissions were not verified.

Mitigation: Use a service endpoint you trust, review the shell execution environment, and never provide private keys or secrets.

Risk: Write operations can prepare transactions that affect DeFi positions or funds.

Mitigation: Check account health and review chain, amounts, price warnings, and transaction details; explicitly confirm with a wallet before signing, and never auto-sign.

## Reference(s):

- [Arcadia Finance](https://arcadia.finance)
- [Arcadia documentation](https://docs.arcadia.finance)
- [Arcadia MCP tool documentation](https://mcp.arcadia.finance/llms-full.txt)
- [Contract addresses](contracts.md)
- [Wallet signing guide](wallet-signing.md)

## Skill Output:

**Output Type(s):** [API calls, Shell commands, Guidance, Configuration instructions]

**Output Format:** [Markdown guidance with shell command and JSON request examples; write operations return unsigned transaction data.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl and jq; transaction signing and broadcasting are handled by a separate wallet.]

## Skill Version(s):

1.5.1 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

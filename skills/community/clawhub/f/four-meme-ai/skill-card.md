## Description:

CLI tool for creating and trading meme tokens on Four.Meme on BSC, with structured JSON outputs for configuration, token details, pricing quotes, on-chain events, and TaxToken fee configuration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[four-meme-community](https://clawhub.ai/user/four-meme-community)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to query Four.Meme data, create meme tokens, estimate trades, execute BSC buy/sell and transfer transactions, inspect token events, and manage TaxToken settings through the fourmeme CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can move wallet funds by creating tokens, buying, selling, sending BNB or ERC20 tokens, and registering an EIP-8004 identity with a PRIVATE_KEY.

Mitigation: Use a dedicated low-balance wallet and confirm every recipient, token address, amount, approval, transaction value, and slippage limit before allowing write operations.

Risk: The skill runs npm-distributed CLI code that uses the private key in the local execution environment.

Mitigation: Review and pin the exact npm package version before installation, avoid storing private keys in project .env files, and run the skill only in a trusted environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/four-meme-community/skills/four-meme-ai)
- [Four.Meme Protocol Integration](https://four-meme.gitbook.io/four.meme/brand/protocol-integration)
- [Contract addresses](references/contract-addresses.md)
- [Create token scripts](references/create-token-scripts.md)
- [Execute buy and sell](references/execute-trade.md)
- [Token query REST API](references/token-query-api.md)
- [Event listening](references/event-listening.md)
- [Tax token parameters](references/token-tax-info.md)
- [Agent creator and wallets](references/agent-creator-and-wallets.md)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance, JSON]

**Output Format:** [Markdown guidance with inline shell commands and structured JSON CLI output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [BSC-only. Write operations require PRIVATE_KEY; BSC_RPC_URL is optional and defaults to a public BSC RPC when unset.]

## Skill Version(s):

1.0.10 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

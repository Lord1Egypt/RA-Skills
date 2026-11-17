## Description:

Access Alchemy's multi-chain APIs for tokens, NFTs, transfers, prices, portfolios, simulations, webhooks, and Solana via API key or agentic gateway.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sahilaujla](https://clawhub.ai/user/sahilaujla)

### License/Terms of Use:

MIT

## Use Case:

Developers and agents use this skill to choose Alchemy endpoints, authenticate with an API key or SIWE/x402 gateway flow, and build blockchain integrations across EVM, Solana, data, wallet, and webhook APIs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The gateway flow can sign real USDC payments using wallet credentials without enough built-in limits or confirmations.

Mitigation: Use testnets first, use a dedicated low-balance wallet, and verify every payment amount, recipient, asset, and network before signing.

Risk: API keys, SIWE tokens, and wallet private keys can expose account access if stored or shared carelessly.

Mitigation: Keep secrets out of project files and chat, avoid storing SIWE tokens in project files, restrict API keys, and rotate credentials when needed.

Risk: Wallet portfolio queries can expose sensitive wallet activity or asset holdings.

Mitigation: Query wallet portfolio data only with authorization and limit requests to the addresses and networks needed for the task.

## Reference(s):

- [Alchemy Developer Docs](https://www.alchemy.com/docs)
- [Alchemy Get Started](https://www.alchemy.com/docs/get-started)
- [Node APIs](references/node-overview.md)
- [Data APIs](references/data-overview.md)
- [Webhooks](references/webhooks-overview.md)
- [Solana APIs](references/solana-overview.md)
- [Wallets](references/wallets-overview.md)
- [Operational & Integration Hygiene](references/operational-overview.md)
- [Gateway Overview](rules/overview.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline code blocks, shell commands, and API request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose API calls, webhook configuration, SIWE/x402 payment steps, and environment-variable setup.]

## Skill Version(s):

1.1.2 (source: server release metadata; artifact frontmatter is 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

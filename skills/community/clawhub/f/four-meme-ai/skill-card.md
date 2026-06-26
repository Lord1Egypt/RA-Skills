## Description: <br>
CLI tool for creating and trading meme tokens on Four.Meme on BSC, with structured JSON outputs for configuration, token details, pricing quotes, on-chain events, and TaxToken fee configuration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[four-meme-community](https://clawhub.ai/user/four-meme-community) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to create, query, quote, and trade Four.Meme tokens on BSC through the fourmeme CLI. It also supports token event inspection, TaxToken fee queries, BNB or ERC20 transfers, and EIP-8004 registration or balance checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Wallet-signed BSC write operations can create tokens, buy, sell, transfer funds, or register identities using the configured private key. <br>
Mitigation: Use a dedicated low-balance wallet, never expose the private key in chat, and review every recipient, token address, amount, and contract interaction before approval. <br>
Risk: The skill installs and invokes an external fourmeme npm CLI for live blockchain actions. <br>
Mitigation: Pin and verify the npm CLI version before use, and review the installed package before enabling write operations. <br>
Risk: Incorrect parameters or market movement can cause unwanted transaction outcomes. <br>
Mitigation: Run read-only quote, token-info, config, and event commands first, then require explicit confirmation before create, buy, sell, send, or 8004-register commands. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/four-meme-community/four-meme-ai) <br>
- [Four.meme Protocol Integration](https://four-meme.gitbook.io/four.meme/brand/protocol-integration) <br>
- [Four.meme API - Create Token](references/api-create-token.md) <br>
- [Create Token Scripts](references/create-token-scripts.md) <br>
- [Execute Buy / Sell](references/execute-trade.md) <br>
- [Token Query REST API](references/token-query-api.md) <br>
- [Four.meme Contract Addresses](references/contract-addresses.md) <br>
- [Event Listening](references/event-listening.md) <br>
- [Tax Token Parameters](references/token-tax-info.md) <br>
- [Query Tax Token Fee/Tax Info](references/tax-token-query.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, JSON] <br>
**Output Format:** [Markdown guidance with CLI commands and structured JSON command outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands may require PRIVATE_KEY for wallet-signed BSC write operations; read-only quote and query commands do not send transactions.] <br>

## Skill Version(s): <br>
1.0.10 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

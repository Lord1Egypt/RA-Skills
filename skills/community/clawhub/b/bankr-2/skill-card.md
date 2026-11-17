## Description:

Bankr enables agents to use natural language for crypto trading, DeFi operations, portfolio checks, token transfers, NFT and Polymarket actions, token deployment, automation, raw transaction signing or submission, and LLM gateway access across Base, Ethereum, Polygon, Solana, and Unichain.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oguhfailed](https://clawhub.ai/user/oguhfailed)

### License/Terms of Use:


## Use Case:

External developers and operators use this skill to connect agents to the Bankr CLI or REST API for wallet queries, crypto trades, DeFi and NFT actions, Polymarket betting, token deployment, trading automation, and LLM gateway access.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Write-enabled Bankr keys can authorize live trading, transfers, betting, leverage, NFT purchases, token launches, signatures, and raw transaction submission.

Mitigation: Prefer read-only keys unless write operations are required, keep write-enabled agent wallets separate and low-balance, and manually review every signature, approval, bridge, bet, leveraged trade, NFT purchase, and raw transaction before authorizing it.

Risk: Stored Bankr credentials or environment files can expose wallet-capable authority if committed or leaked.

Mitigation: Store keys in environment variables or local configuration only, avoid committing ~/.bankr or .env files, use separate Agent API and LLM Gateway keys where useful, rotate keys periodically, and revoke leaked keys immediately.

Risk: Network-accessible agents using Bankr keys may be invoked from unintended locations.

Mitigation: Restrict API keys with IP whitelisting where possible and use dedicated accounts for autonomous agents.

## Reference(s):

- [Bankr Homepage](https://bankr.bot)
- [Bankr API Key Management](https://bankr.bot/api)
- [Bankr LLM Gateway Documentation](https://docs.bankr.bot/llm-gateway/overview)
- [Bankr API Workflow Reference](artifact/references/api-workflow.md)
- [Bankr Sign and Submit API Reference](artifact/references/sign-submit-api.md)
- [Bankr Safety and Access Control Reference](artifact/references/safety.md)
- [Bankr Token Trading Reference](artifact/references/token-trading.md)
- [Bankr Portfolio Reference](artifact/references/portfolio.md)
- [Bankr LLM Gateway Reference](artifact/references/llm-gateway.md)
- [Bankr Token Deployment Reference](artifact/references/token-deployment.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, API examples, JSON snippets, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce wallet, trading, transaction, API-key, and LLM-gateway setup guidance that requires user review before execution.]

## Skill Version(s):

0.1.0 (source: server release metadata, released 2026-02-28)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

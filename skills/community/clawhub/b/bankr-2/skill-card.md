## Description: <br>
AI-powered crypto trading agent and LLM gateway via natural language. Use when the user wants to trade crypto, check portfolio balances, view token prices, transfer crypto, manage NFTs, use leverage, bet on Polymarket, deploy tokens, set up automated trading, sign and submit raw transactions, or access LLM models through the Bankr LLM gateway funded by your Bankr wallet. Supports Base, Ethereum, Polygon, Solana, and Unichain. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oguhfailed](https://clawhub.ai/user/oguhfailed) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users, developers, and agent builders use this skill to operate Bankr through the CLI or REST API for crypto portfolio review, token trading, transfers, NFT operations, Polymarket betting, leverage, token deployment, automation, raw transaction submission, and LLM gateway access. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can move real crypto assets, place bets, deploy tokens, automate trading, sign transactions, and submit raw blockchain transactions. <br>
Mitigation: Use it only when those capabilities are intended, prefer read-only keys unless execution is required, and require explicit human review before any trade, transfer, bet, deployment, automation, signing, or raw transaction submission. <br>
Risk: A write-capable API key can expose funds if it is compromised or reused in an unsafe environment. <br>
Mitigation: Use a dedicated low-balance wallet, enable IP restrictions where possible, avoid shared or synced key storage, and keep API keys out of source files. <br>
Risk: Raw transaction submission and blockchain operations may be irreversible once executed. <br>
Mitigation: Test with small amounts on low-cost chains, verify recipients and calldata, and use confirmation-oriented flows before scaling usage. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/oguhfailed/bankr-2) <br>
- [Bankr Homepage](https://bankr.bot) <br>
- [Bankr API Portal](https://bankr.bot/api) <br>
- [Bankr LLM Gateway Documentation](https://docs.bankr.bot/llm-gateway/overview) <br>
- [Bankr API Workflow Reference](references/api-workflow.md) <br>
- [Sign and Submit API Reference](references/sign-submit-api.md) <br>
- [Safety & Access Control Reference](references/safety.md) <br>
- [Token Trading Reference](references/token-trading.md) <br>
- [Portfolio Reference](references/portfolio.md) <br>
- [Transfers Reference](references/transfers.md) <br>
- [NFT Operations Reference](references/nft-operations.md) <br>
- [Polymarket Reference](references/polymarket.md) <br>
- [Leverage Trading Reference](references/leverage-trading.md) <br>
- [Token Deployment Reference](references/token-deployment.md) <br>
- [Automation Reference](references/automation.md) <br>
- [Arbitrary Transaction Reference](references/arbitrary-transaction.md) <br>
- [Market Research Reference](references/market-research.md) <br>
- [LLM Gateway Reference](references/llm-gateway.md) <br>
- [Error Handling Reference](references/error-handling.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, API calls, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands, REST examples, JSON snippets, and natural-language guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include transaction prompts, polling commands, API request and response examples, setup instructions, and configuration guidance.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

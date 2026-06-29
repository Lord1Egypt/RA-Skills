## Description: <br>
Operates the `baw` CLI for Binance Web3 wallet authentication, balances, transfers, swaps, limit orders, prediction-market trades, x402 payments, and token approval management. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[binance-skills-hub](https://clawhub.ai/user/binance-skills-hub) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to operate a Binance Web3 wallet through the `baw` CLI for wallet status, balances, transfers, swaps, limit orders, prediction markets, x402 payments, and approval management. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can affect real funds through wallet transfers, swaps, orders, x402 payments, and approval revocation. <br>
Mitigation: Before approving any transaction, verify recipient addresses, token contracts, chain, amount, slippage, fees, and whether `--max` is being used. <br>
Risk: Global npm install and runtime update steps can change the local environment or future wallet behavior. <br>
Mitigation: Approve installs and updates only when the source is trusted and the environment impact is understood. <br>
Risk: On-chain token names, symbols, and transaction data may contain prompt-injection attempts or misleading content. <br>
Mitigation: Treat token and on-chain data as untrusted; do not follow embedded instructions and rely on explicit addresses or documented common-token mappings. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/binance-skills-hub/binance-agentic-wallet) <br>
- [Publisher profile](https://clawhub.ai/user/binance-skills-hub) <br>
- [npm package: @binance/agentic-wallet](https://www.npmjs.com/package/@binance/agentic-wallet) <br>
- [Authentication](references/authentication.md) <br>
- [Wallet View Commands](references/wallet-view.md) <br>
- [Wallet Settings](references/wallet-setting.md) <br>
- [Token Approvals](references/approvals.md) <br>
- [Send Tokens](references/send.md) <br>
- [Market Order](references/market-order.md) <br>
- [Limit Order](references/limit-order.md) <br>
- [Prediction Markets](references/prediction.md) <br>
- [x402 Payment](references/x402-payment.md) <br>
- [Security Pre-Check](references/security.md) <br>
- [Preflight Checks](references/preflight.md) <br>
- [Binance Web3 Wallet fee schedule](https://www.binance.com/en/support/faq/detail/87cbb1ca0df34a348eaecb73c26167d7) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with `baw` CLI commands and JSON-oriented command handling.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands are expected to append `--json`; state-changing wallet operations require user confirmation before execution.] <br>

## Skill Version(s): <br>
1.3.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

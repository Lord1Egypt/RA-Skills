## Description:

This skill helps an agent operate the Binance Agentic Wallet CLI for wallet connection, balances, transfers, swaps, orders, prediction markets, x402 payments, DeFi actions, approvals, transaction replacement, and external signing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[binance-skills-hub](https://clawhub.ai/user/binance-skills-hub)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to route Binance Web3 wallet requests into documented baw CLI commands. It supports account status, token movement, trading, order management, approvals, DeFi workflows, prediction markets, x402 payments, and explicit-preview signing flows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can initiate real wallet actions including transfers, trades, DeFi transactions, approval changes, payments, transaction replacement, and signatures.

Mitigation: Review each CLI preview or command summary carefully and proceed only after explicit user confirmation for state-changing actions.

Risk: External contract calls and EIP-712 signatures can grant or change on-chain authority when Developer Mode is enabled.

Mitigation: Do not enable Developer Mode unless the exact contract call or message is understood; inspect parsed transaction, risks, and authority changes before execution.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/binance-skills-hub/skills/binance-agentic-wallet)
- [Authentication](references/authentication.md)
- [Wallet View Commands](references/wallet-view.md)
- [Wallet Settings](references/wallet-setting.md)
- [Send Tokens](references/send.md)
- [Market Order](references/market-order.md)
- [Limit Order](references/limit-order.md)
- [Token Approvals](references/approvals.md)
- [External Sign](references/external-sign.md)
- [Prediction Markets](references/prediction.md)
- [x402 Payment](references/x402-payment.md)
- [DeFi Commands](references/defi.md)
- [Speed Up and Cancel Pending Transactions](references/speedup-cancel.md)
- [Security Reference](references/security.md)
- [Preflight Checks](references/preflight.md)
- [bStock AI Trading Competition Campaign Reference](references/campaign.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and summarized JSON results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [State-changing wallet operations require explicit user confirmation and CLI output is requested as JSON for agent parsing.]

## Skill Version(s):

1.9.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

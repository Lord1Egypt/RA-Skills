## Description:

Buy or sell XAUT (Tether Gold) on Ethereum with market orders through Uniswap V3, limit orders through UniswapX, and local wallet setup guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aure-duncan](https://clawhub.ai/user/aure-duncan)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to guide an agent through XAUT/USDT market swaps, UniswapX limit orders, balance checks, and wallet setup on Ethereum. The skill is intended for explicit user-directed trading workflows, not autonomous price monitoring.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide wallet signing and on-chain financial transactions, so mistakes or unintended authorization can spend real assets.

Mitigation: Use a dedicated low-value wallet, review every command preview, keep confirmation thresholds enabled, and require explicit confirmation for larger trades or high slippage.

Risk: Setup and wallet paths include sensitive credential files and may use remote installers.

Mitigation: Avoid the Foundry curl-to-bash path unless independently verified, keep vault and password files at mode 0600, and audit ~/.aurehub/.env for shell metacharacters before sourcing it.

Risk: Alternate RPC or UniswapX endpoints can expose wallet address, order data, transaction data, or API keys to third parties.

Mitigation: Use trusted HTTPS endpoints, avoid alternate UniswapX endpoints with production API keys, and treat external API responses as untrusted.

## Reference(s):

- [Skill Overview](README.md)
- [Environment and Security Declaration](SKILL.md)
- [Balance and Pre-flight Checks](references/balance.md)
- [Buy Execution](references/buy.md)
- [Sell Execution](references/sell.md)
- [Quote and Slippage Protection](references/quote.md)
- [Limit Order Placement: Buy](references/limit-order-buy-place.md)
- [Limit Order Placement: Sell](references/limit-order-sell-place.md)
- [Limit Order Status](references/limit-order-status.md)
- [Limit Order Cancellation](references/limit-order-cancel.md)
- [Live Trading Runbook](references/live-trading-runbook.md)
- [Wallet Modes](references/wallet-modes.md)
- [Onboarding](references/onboarding.md)
- [Skill Delegation](references/skill-delegation.md)
- [Uniswap Developer Dashboard](https://developers.uniswap.org/dashboard)
- [Foundry Project](https://github.com/foundry-rs/foundry)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON command outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May generate transaction previews, wallet setup steps, trading commands, balance summaries, and limit-order status guidance.]

## Skill Version(s):

2.3.0 (source: server release evidence, SKILL.md frontmatter, scripts/package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

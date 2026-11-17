## Description:

Complete Binance integration for checking balances, viewing prices and positions, managing spot and futures orders, setting stop loss and take profit orders, checking PnL, and changing futures leverage.

This skill is ready for commercial/non-commercial use.

## Publisher:

[totaleasy](https://clawhub.ai/user/totaleasy)

### License/Terms of Use:


## Use Case:

External users and trading-oriented agent operators use this skill to generate Binance API calls for account checks, spot trading, futures position management, order cancellation, trade history review, and risk controls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can produce commands for live Binance spot trading, futures trading, leverage changes, cancellations, and account access.

Mitigation: Require explicit confirmation before every trade, leverage change, cancellation, or other account-changing action.

Risk: Binance API keys can expose funds or account data if over-permissioned or reused.

Mitigation: Use a dedicated Binance API key with the minimum permissions needed, disable withdrawals, restrict by IP where available, and prefer read-only keys for account checks.

Risk: Leveraged futures operations can cause rapid financial loss if pair, quantity, side, leverage, stop loss, or take profit values are wrong.

Mitigation: Use testnet where possible and verify symbol, position, quantity, side, leverage, stop loss, and take profit before execution.

## Reference(s):

- [Binance API Documentation](https://binance-docs.github.io/apidocs/)
- [Binance Testnet](https://testnet.binance.vision/)
- [ClawHub Skill Page](https://clawhub.ai/totaleasy/skills/binance-pro)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with JSON and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses curl and jq; examples require Binance API credentials and may perform live account or trading operations when executed.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

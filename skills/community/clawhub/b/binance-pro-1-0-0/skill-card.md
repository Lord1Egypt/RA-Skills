## Description:

Complete Binance integration for checking balances, managing spot and futures trades, setting stop loss and take profit orders, reviewing PnL, and performing other Binance account operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[0xspeter](https://clawhub.ai/user/0xspeter)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and trading operators use this skill to let an agent prepare Binance API calls for account queries, spot orders, futures positions, leverage changes, stop loss and take profit orders, cancellations, and trade history review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can assist with live Binance spot and leveraged futures operations, including orders, cancellations, leverage changes, and position closes.

Mitigation: Use testnet or read-only access first, require explicit confirmation for every account-changing operation, and verify symbol, side, quantity, leverage, and position state before execution.

Risk: Broad activation and credential guidance can expose high-impact Binance API keys to unintended account actions.

Mitigation: Use a dedicated API key with withdrawals disabled, the narrowest permissions possible, and IP allowlisting where available.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/0xspeter/skills/binance-pro-1-0-0)
- [Binance API Documentation](https://binance-docs.github.io/apidocs/)
- [Binance Testnet](https://testnet.binance.vision/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline JSON and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl and jq; examples depend on Binance API credentials.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

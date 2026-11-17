## Description:

Monitors Binance Futures account balances, positions, funding-fee income, and profit/loss through paid MCP tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yyu812707-wq](https://clawhub.ai/user/yyu812707-wq)

### License/Terms of Use:

MIT

## Use Case:

External crypto account operators use this skill to retrieve Binance Futures account summaries, open positions, recent funding-fee income, and combined monitoring reports after configuring their Binance API credentials and SkillPay payment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release is presented as a Binance monitoring skill but evidence.security reports that it also ships directly executable live futures trading strategy code.

Mitigation: Review the package before installation and avoid running the trading strategy unless intentional; for monitoring-only use, configure a dedicated Binance API key without futures-trading permission.

Risk: The skill uses Binance API credentials and contacts SkillPay with session-linked payment metadata.

Mitigation: Use a dedicated Binance API key with withdrawals disabled, restrict the key by IP where possible, and confirm payment-data handling before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yyu812707-wq/skills/binance-funding-monitor)
- [ClawHub publisher profile](https://clawhub.ai/user/yyu812707-wq)
- [Binance Futures API endpoint](https://fapi.binance.com)
- [SkillPay API endpoint](https://api.skillpay.me/v1)

## Skill Output:

**Output Type(s):** [text, guidance]

**Output Format:** [Plain text MCP tool responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports can include account balances, margin use, open positions, unrealized P&L, funding-fee income, and payment-verification status.]

## Skill Version(s):

1.0.3 (source: server release evidence and artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

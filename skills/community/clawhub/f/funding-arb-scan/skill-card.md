## Description:

Guides agents in screening Binance USD-M perpetual funding rates for arbitrage ideas and crowding risk, with a BTC/ETH/SOL market-regime check through a paid request.

This skill is ready for commercial/non-commercial use.

## Publisher:

[perria080925-bot](https://clawhub.ai/user/perria080925-bot)

### License/Terms of Use:

MIT-0

## Use Case:

External agents and traders use this skill to identify potentially interesting perpetual-futures funding spreads, check crowding and major-asset conditions, and account for costs and liquidation risk before trading.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Each scan contacts an external paid service and can trigger a USDC payment.

Mitigation: Confirm the endpoint, price, and payment details before approving each request; use a trusted x402 payment workflow.

Risk: Funding signals are screening data, not financial advice, and may not cover trading costs or liquidation exposure.

Mitigation: Verify current market data and net fees and funding against expected returns; assess crowding and liquidation risk before any trade.

Risk: Payment or exchange credentials could be exposed to an untrusted service.

Mitigation: Do not provide exchange keys or private wallet secrets outside a trusted payment workflow.

## Reference(s):

- [ClawHub funding-arb-scan release](https://clawhub.ai/perria080925-bot/skills/funding-arb-scan)
- [Publisher profile](https://clawhub.ai/user/perria080925-bot)
- [Funding heatmap endpoint](https://x402.bankr.bot/0xf436ca41bd0a236338bef57adeb4976677513010/funding-heatmap)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Describes ranked funding rates, crowding flags, and BTC/ETH/SOL regime from the service response.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

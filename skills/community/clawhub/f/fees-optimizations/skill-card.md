## Description:

Guides agents in reducing trading costs for Hyperliquid Freqtrade deployments by explaining fee layers, maker and taker pricing, slippage, and cost-sensitive configuration choices.

This skill is ready for commercial/non-commercial use.

## Publisher:

[superior-ai](https://clawhub.ai/user/superior-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and trading operators use this skill to diagnose fee-driven gaps between backtests and live Freqtrade performance on Hyperliquid deployments. It helps agents recommend order type, pricing, timeout, and turnover choices that account for exchange fees, builder fees, and slippage.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can influence order-pricing recommendations for Freqtrade deployments where fees materially affect results.

Mitigation: Review proposed configuration changes before use with live capital, especially order type, price side, timeout, and fallback behavior.

Risk: Fee and slippage examples may become stale as Hyperliquid tiers, Superior builder fees, and market liquidity change.

Mitigation: Verify current Hyperliquid fee tiers, Superior builder-code rates, and recent fill slippage before relying on numeric examples.

## Reference(s):

- [Hyperliquid fees](https://hyperliquid.gitbook.io/hyperliquid-docs/trading/fees)
- [Freqtrade order types configuration](https://www.freqtrade.io/en/stable/configuration/#understand-order_types)
- [Freqtrade entry and exit pricing configuration](https://www.freqtrade.io/en/stable/configuration/#understand-entry_pricing-and-exit_pricing)
- [Hyperliquid portfolio fee tier check](https://app.hyperliquid.xyz/portfolio)

## Skill Output:

**Output Type(s):** [guidance, configuration, code]

**Output Format:** [Markdown with JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.0 (source: server-resolved ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

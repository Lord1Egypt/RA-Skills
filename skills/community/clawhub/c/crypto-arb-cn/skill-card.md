## Description:

Monitors cryptocurrency prices across Binance, OKX, Gate.io, and Huobi to identify cross-exchange arbitrage opportunities and optionally send Telegram alerts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guohongbin-git](https://clawhub.ai/user/guohongbin-git)

### License/Terms of Use:


## Use Case:

Developers and crypto operators use this skill to run or configure a local monitor that checks selected trading pairs across public exchange APIs, calculates fee-adjusted spreads, and reports potential arbitrage opportunities.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Continuous monitoring makes repeated outbound requests to public exchange APIs.

Mitigation: Run it only in environments where those network calls are expected, and review the configured check interval before continuous use.

Risk: Telegram alerts send arbitrage opportunity details through Telegram when a bot token and chat ID are configured.

Mitigation: Enable Telegram only when that notification channel is acceptable, and do not provide exchange trading credentials because the skill does not need them.

Risk: Displayed arbitrage opportunities can change quickly and may not include every operational cost such as withdrawal timing, slippage, or exchange maintenance.

Mitigation: Treat results as monitoring signals, verify fees and transfer status before acting, and avoid relying on the output as financial advice.

## Reference(s):

- [Exchange API Reference](references/exchanges.md)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and console-style text output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce repeated console updates in continuous mode and optional Telegram alert messages when configured.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

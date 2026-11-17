## Description:

Use when writing, validating, or troubleshooting a recurring scheduled buy strategy on Superior Trade that adds to the same trading pair on a calendar trigger rather than a price trigger.

This skill is ready for commercial/non-commercial use.

## Publisher:

[superior-ai](https://clawhub.ai/user/superior-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and trading-strategy builders use this skill to draft, validate, and troubleshoot Freqtrade-style DCA strategies that perform recurring scheduled buys. It helps distinguish calendar-based accumulation from price-triggered grid trading and provides reference code, configuration, pitfalls, and variants.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automated DCA strategies can keep buying on a funded exchange account and may lose money.

Mitigation: Backtest the strategy, run dry-run or paper trading, verify pair, stake, wallet size, cadence, spot versus futures mode, and monitoring or kill-switch settings before funded use.

Risk: Incorrect trading parameters can cause unintended recurring buys or wallet exhaustion.

Mitigation: Review generated strategy and configuration settings before execution, including stake sizing, wallet reserve, cadence, and position-adjustment behavior.

## Reference(s):

- [Dca Weekly ClawHub release](https://clawhub.ai/superior-ai/skills/dca-weekly)
- [Freqtrade adjust_trade_position documentation](https://www.freqtrade.io/en/stable/strategy-callbacks/#adjust-trade-position)
- [Freqtrade DigDeeperStrategy reference](https://github.com/freqtrade/freqtrade/issues/7052)

## Skill Output:

**Output Type(s):** [Guidance, Code, Configuration]

**Output Format:** [Markdown with Python and JSON code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces strategy guidance and examples for human review before deployment; it does not bundle executables or require credentials.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

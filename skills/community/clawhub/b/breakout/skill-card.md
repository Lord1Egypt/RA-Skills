## Description:

Guides agents in writing Superior Trade swing or intraday breakout, momentum, and trend-following strategy templates while highlighting the disclosed unprofitable reference backtest and regime sensitivity.

This skill is ready for commercial/non-commercial use.

## Publisher:

[superior-ai](https://clawhub.ai/user/superior-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and trading-strategy authors use this skill to draft and tune a Superior Trade breakout strategy, including reference code, configuration, and cautions about market-regime dependence.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automated futures trading can lose money, and this template is intended for users who understand that risk.

Mitigation: Backtest, review, and paper-trade the strategy before any live deployment.

Risk: The reference long-only breakout backtest was unprofitable and sensitive to market regime.

Mitigation: Use regime filters, wider multi-pair scans, and fresh market-specific tests before relying on the strategy.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/superior-ai/skills/breakout)
- [Freqtrade trailing stop documentation](https://www.freqtrade.io/en/stable/stoploss/#trailing-stop-loss)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown with Python and JSON code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes trading-strategy caveats, configuration defaults, tuning guidance, and disclosed backtest context.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata; artifact frontmatter says 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

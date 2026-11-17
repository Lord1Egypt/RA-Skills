## Description:

Helps agents draft a Freqtrade strategy for Hyperliquid perpetuals that goes long when deeply negative funding and rising price action suggest short-squeeze fuel, then exits on funding normalization or a 24-hour time stop.

This skill is ready for commercial/non-commercial use.

## Publisher:

[superior-ai](https://clawhub.ai/user/superior-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and trading-strategy builders use this skill to produce Freqtrade code, configuration, and tuning guidance for a long-only short-squeeze strategy on Hyperliquid perpetual futures. The strategy is intended for backtesting, paper trading, and carefully controlled live evaluation rather than guaranteed investment performance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The strategy concerns live futures trading and can lose money, especially when using cross margin or unsuitable position sizing.

Mitigation: Backtest and paper trade before live use, keep exchange credentials under explicit user control, and set position sizing and margin settings deliberately.

Risk: The included backtest shows negative performance in the cited January 1, 2026 to May 1, 2026 BTC/USDC perpetuals window, so the strategy may fail in structural downtrends.

Mitigation: Use regime filters, multi-pair scanning, and fresh market-specific validation before relying on the generated strategy.

## Reference(s):

- [Funding Squeeze on ClawHub](https://clawhub.ai/superior-ai/skills/funding-squeeze)
- [Superior-AI publisher profile](https://clawhub.ai/user/superior-ai)
- [Alpha scan improvement plan](https://github.com/Superior-Trade/superior-turborepo/blob/main/docs/alpha-scan-improvement-plan.md)
- [Freqtrade DataProvider strategy customization](https://www.freqtrade.io/en/stable/strategy-customization/)

## Skill Output:

**Output Type(s):** [Markdown, Code, Configuration instructions, Guidance]

**Output Format:** [Markdown with Python and JSON code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces strategy logic, Freqtrade configuration, tuning notes, and operational cautions for the user to review before use.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

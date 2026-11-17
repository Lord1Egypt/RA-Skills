## Description:

Expected move visualizer for stocks and ETFs: turn implied volatility into a self-contained HTML chart showing the modeled 30, 60 and 90 day expected move cone around the current price, skewed by 25-delta put and call demand, with IV rank context and the next earnings date marked inside the cone. Renders offline from a bound data snapshot, no live call at view time. Use for expected move calculator, how much is this stock expected to move, implied volatility chart, options expected move, IV rank, earnings move visualizer, straddle move estimate. Read-only. No trading, no purchases, no write operations, no wallet access.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thesentitrader](https://clawhub.ai/user/thesentitrader)

### License/Terms of Use:

MIT-0

## Use Case:

Investors and market researchers use this skill to visualize modeled options-implied move ranges for a selected stock or ETF and compare them with past earnings reactions or realized volatility. It provides informational context, not a trading recommendation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Crafted market-data responses could insert executable code into generated HTML reports.

Mitigation: Prefer a corrected release that safely encodes both embedded JSON blocks. Until then, open generated reports only in an isolated renderer without privileged host access.

## Reference(s):

- [SentiSense API documentation](https://sentisense.ai/docs/api/#full-sample-responses-with-a-free-key)
- [SentiSense](https://sentisense.ai)

## Skill Output:

**Output Type(s):** [HTML file, Text summary]

**Output Format:** [Self-contained HTML chart with a concise text summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Offline snapshot of modeled expected-move ranges and volatility context; informational, not a forecast or recommendation.]

## Skill Version(s):

1.0.10 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

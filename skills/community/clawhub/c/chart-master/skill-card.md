## Description:

Generate precise financial charts (candlestick, OHLC, line) for stocks, indices, and crypto using Python.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ericw12](https://clawhub.ai/user/ericw12)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and agents use this skill to generate visual price history and technical analysis charts for equities, indices, and crypto assets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Runtime package resolution can make results depend on the currently available package versions.

Mitigation: Run the skill in a locked Python environment with pinned versions for yfinance, mplfinance, and pandas.

Risk: The skill fetches financial data at runtime, which may expose requested ticker symbols to the data provider and can return unavailable or delayed data.

Mitigation: Use approved network environments and review generated charts before relying on them for analysis.

## Reference(s):

- [Chart Master ClawHub listing](https://clawhub.ai/ericw12/skills/chart-master)
- [Publisher profile](https://clawhub.ai/user/ericw12)

## Skill Output:

**Output Type(s):** [text, shell commands, code, configuration, files]

**Output Format:** [Markdown guidance with shell command examples and generated PNG chart files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Fetches financial market data at runtime and saves a timestamped PNG chart path.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

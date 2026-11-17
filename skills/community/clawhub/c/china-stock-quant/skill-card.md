## Description:

A-share quantitative analysis toolkit for fetching China stock and ETF data, calculating technical indicators, backtesting strategies, and assessing portfolio risk.

This skill is ready for commercial/non-commercial use.

## Publisher:

[miio-jinglin](https://clawhub.ai/user/miio-jinglin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use this skill to retrieve A-share and ETF market data, calculate MACD, KDJ, RSI, Bollinger bands, and volume indicators, run basic strategy backtests, and summarize risk metrics. It supports analysis and backtesting workflows only, not automated trade execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Market data fetching makes outbound requests to third-party data sources through akshare.

Mitigation: Run in a virtual environment, pin dependency versions where practical, and allow network access only when market-data retrieval is intended.

Risk: Backtest results, technical indicators, and strategy signals can be mistaken for trading advice.

Mitigation: Treat outputs as analysis and backtesting support only; require human review before any investment or trading decision.

## Reference(s):

- [akshare API Quick Reference](references/api-reference.md)
- [ETF Day-Trading Strategies](references/strategies.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown with Python and shell command examples, plus tabular or dictionary-style analysis outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce pandas DataFrame summaries, backtest result summaries, risk metric dictionaries, and strategy guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

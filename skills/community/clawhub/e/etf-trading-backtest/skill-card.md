## Description:

ETF模拟交易回测系统，支持A股ETF日内交易策略的模拟交易与回测分析，包括BOLL、MACD、KDJ等技术指标组合判断、手续费计算、止损止盈和风险指标统计。

This skill is ready for commercial/non-commercial use.

## Publisher:

[tangsuann](https://clawhub.ai/user/tangsuann)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to run simulated ETF or stock trading analysis, backtest technical-indicator strategies, and generate trade or risk reports for educational review. The outputs should not be treated as investment advice or as authorization for real-money trading.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Market data is fetched over unauthenticated plaintext HTTP and could be tampered with in transit.

Mitigation: Review data source integrity before relying on generated signals, and prefer authenticated or protected market-data transport when adapting the skill.

Risk: Generated buy and sell signals may be incorrect, incomplete, or unsuitable for financial decisions.

Mitigation: Treat reports as educational simulation output, review them manually, and do not use them as investment advice or direct real-money trading instructions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tangsuann/skills/etf-trading-backtest)
- [ETF模拟交易规则详细说明](references/rules.md)
- [Strategy configuration](references/config.json)
- [Eastmoney realtime market data endpoint](http://push2.eastmoney.com/api/qt/stock/get)
- [Eastmoney historical K-line endpoint](http://push2his.eastmoney.com/api/qt/stock/kline/get)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown reports, console text, Python code, and configuration values]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces simulated trade signals, backtest metrics, and risk statistics based on configured market data and strategy parameters.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md footer)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

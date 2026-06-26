## Description: <br>
ETF模拟交易回测系统，支持A股ETF日内交易策略的模拟交易与回测分析，包括BOLL、MACD、KDJ等技术指标组合判断，并自动计算手续费、止损止盈和最大回撤、夏普比率等风险指标。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[TangSuann](https://clawhub.ai/user/TangSuann) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
开发者、量化研究人员和学习者可使用该 skill 对A股ETF或股票策略进行模拟交易和历史回测，生成交易信号、交易记录、收益统计和风险指标报告。其结果应作为学习和分析辅助，不构成投资建议。 <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Backtest and simulated trading outputs may be mistaken for investment advice. <br>
Mitigation: Present outputs as educational analysis only, verify results independently, and require human review before using insights for financial decisions. <br>
Risk: The script contacts Eastmoney over HTTP for market data, so results depend on third-party data availability and transport integrity. <br>
Mitigation: Run in an environment where outbound market-data access is intended, validate downloaded data before analysis, and avoid sharing sensitive information through requests. <br>
Risk: Optional cron usage can create recurring analyses that users may not expect. <br>
Mitigation: Create scheduled jobs only after explicit user approval and document the schedule, command, and data source. <br>


## Reference(s): <br>
- [Skill source](https://clawhub.ai/TangSuann/etf-trading-backtest) <br>
- [ETF模拟交易规则详细说明](references/rules.md) <br>
- [Default strategy configuration](references/config.json) <br>
- [Eastmoney realtime quote API](http://push2.eastmoney.com/api/qt/stock/get) <br>
- [Eastmoney historical kline API](http://push2his.eastmoney.com/api/qt/stock/kline/get) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown reports with optional Python script execution and JSON configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces simulated trading decisions, backtest metrics, risk statistics, and review notes; does not place real trades.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Description: <br>
A-Share Paper Trading System for data fetching, local storage, strategy backtesting, and simulated trading. <br>

This skill is for research and development only. <br>

## Publisher: <br>
[BOMBFUOCK](https://clawhub.ai/user/BOMBFUOCK) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and finance learners use this skill to fetch public A-share market data, store it in SQLite, run simple backtests, and inspect paper-trading positions without placing real orders. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill fetches public market data over the network and writes simulated trading data to a local SQLite database. <br>
Mitigation: Run it only in an environment where network access to market data sources and local writes under ~/.openclaw/workspace/a-stock/ are acceptable. <br>
Risk: Backtest and paper-trading results may be mistaken for investment advice or live trading output. <br>
Mitigation: Treat outputs as educational paper-trading information only and independently review any financial interpretation before acting on it. <br>
Risk: The security guidance flags unusual or adversarial stock-code input as a concern until the SQL query is fixed. <br>
Mitigation: Use normal stock-code inputs and avoid adversarial or unexpected values. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/BOMBFUOCK/a-stock-trader) <br>
- [Skill instructions](SKILL.md) <br>
- [Quick start](README.md) <br>
- [East Money K-line API endpoint](http://push2his.eastmoney.com/api/qt/stock/kline/get) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Code, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and console-oriented Python script output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update a local SQLite database under ~/.openclaw/workspace/a-stock/ and print backtest, trade, and portfolio summaries.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

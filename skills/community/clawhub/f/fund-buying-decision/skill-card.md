## Description: <br>
Parameterize and apply a Chinese mutual-fund buy, add, reduce, or hold strategy driven by price drawdown, recurring DCA, cash-pool management, and position limits. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[seanmwx](https://clawhub.ai/user/seanmwx) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and fund-strategy users use this skill to maintain a parameterized Chinese mutual-fund decision framework, refresh public fund data, evaluate daily buy/add/reduce/hold decisions, and keep live strategy state in SQLite instead of SKILL.md. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create and update a local SQLite database containing financial-planning data. <br>
Mitigation: Use a separate --db path for isolation and review file locations before running account or trade scripts. <br>
Risk: Strategy suggestions or local ledger entries could be mistaken for real brokerage actions or proof of transactions. <br>
Mitigation: Review suggested actions before running confirm_strategy_action.py or record_strategy_trade.py, and keep brokerage confirmation separate from the local ledger. <br>


## Reference(s): <br>
- [Strategy Parameters](artifact/references/strategy_parameters.md) <br>
- [Data Inputs](artifact/references/data_inputs.md) <br>
- [Fund Buying Decision Pro on ClawHub](https://clawhub.ai/seanmwx/fund-buying-decision) <br>
- [Eastmoney Fund Data Endpoint](https://fund.eastmoney.com/pingzhongdata/{fund_code}.js) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown text with inline shell commands, JSON-like strategy outputs, and Python script invocations.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Single decision cycles return one explicit action: buy_dca, buy_dip, sell_take_profit, hold, or skip_data_missing.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Description:

A股模拟炒股系统。当用户需要模拟炒股、查询行情、买卖下单、查看持仓盈亏时触发。支持实时行情、买卖下单、持仓管理、盈亏计算、涨跌排行。

This skill is ready for commercial/non-commercial use.

## Publisher:

[luaqnyin](https://clawhub.ai/user/luaqnyin)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill as a local Chinese-language paper-trading helper for A-share market simulation, including quotes, simulated buy and sell orders, holdings, account balance, history, K-line data, rankings, and stock search.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Simulated portfolio data is stored locally and may be reset or corrupted.

Mitigation: Confirm before reset actions and treat the portfolio file as disposable simulation data rather than an authoritative financial record.

Risk: Market quote integrity and input validation are weaker than a production trading tool.

Mitigation: Cross-check quotes, trading status, and order constraints before simulated buy or sell decisions, and do not use the output for real financial decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/luaqnyin/skills/a-stock-paper-trade)
- [Sina Finance](https://finance.sina.com.cn)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [JSON responses and short text output from local shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Most commands print JSON for agent parsing; market overview output may be plain text.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

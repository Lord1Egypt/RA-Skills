## Description:

提供A股实时行情、分时成交量分布及主力资金动向分析，支持持仓管理和盈亏监控。

This skill is ready for commercial/non-commercial use.

## Publisher:

[cnyezi](https://clawhub.ai/user/cnyezi)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to query A-share market quotes, inspect intraday volume distribution and main-force movement signals, and manage local portfolio cost, quantity, and profit/loss records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can store and mutate stock codes, costs, quantities, and timestamps in a local plaintext portfolio file.

Mitigation: Review portfolio commands before use, avoid recording sensitive holdings on shared machines, and keep backups of important portfolio data.

## Reference(s):

- [A股分时量能分析 ClawHub skill page](https://clawhub.ai/cnyezi/skills/a-stock-analysis)
- [Sina Finance market data endpoint](https://hq.sinajs.cn/list={codes_str})
- [Sina Finance](https://finance.sina.com.cn)

## Skill Output:

**Output Type(s):** [text, json, shell commands, guidance]

**Output Format:** [Plain text or JSON responses with command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update a local plaintext portfolio file at ~/.clawdbot/skills/a-stock-analysis/portfolio.json.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

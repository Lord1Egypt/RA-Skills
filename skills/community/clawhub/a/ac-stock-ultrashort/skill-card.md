## Description:

A股超短线交易策略。用于 Peter 的游牧型超短线交易风格：只做主线、只做最强、1-2天T+1套利。当需要分析A股盘面、筛选热点板块、寻找龙头股、制定买卖策略时使用。

This skill is ready for commercial/non-commercial use.

## Publisher:

[peterzhu0](https://clawhub.ai/user/peterzhu0)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to apply a disciplined A-share ultra-short trading playbook for identifying hot themes, screening leading stocks, planning entries and exits, sizing positions, and enforcing stop-loss and drawdown controls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may encourage high-risk short-term stock trading decisions.

Mitigation: Treat outputs as planning guidance, verify market data independently, and apply the stated stop-loss, position-sizing, and drawdown controls before acting.

Risk: Users could expose sensitive brokerage credentials, account records, or private financial data while asking for analysis.

Mitigation: Do not provide brokerage credentials, private account data, or personal financial records unless intentionally needed and handled under appropriate privacy controls.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/peterzhu0/skills/ac-stock-ultrashort)
- [东方财富概念板块资金流向](https://data.eastmoney.com/bkzj/gn.html)
- [财联社热点新闻](https://www.cls.cn/hot-stock)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, Markdown]

**Output Format:** [Markdown text with trading criteria, workflow steps, and risk-control rules]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include stock-screening rationale, trading-plan guidance, position-sizing suggestions, stop-loss rules, and trade-log templates.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

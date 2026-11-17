## Description:

A股智能投资助手 - 实时行情、技术分析、自动盯盘、持仓报告、异动告警。支持MACD/KDJ/布林带等技术指标，定时推送持仓报告到飞书/微信。

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangzhaofeng-max](https://clawhub.ai/user/wangzhaofeng-max)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to query A-share market data, calculate technical indicators, monitor watchlists, generate holding reports, and draft simple backtesting workflows. It supports OpenClaw scheduling and messaging-channel configuration for report and alert workflows, but users should separately configure and approve those automations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Stock symbols, watchlists, and query timing may be sent to AKShare-backed sources or Eastmoney.

Mitigation: Use the skill in an isolated environment and avoid submitting confidential portfolios or sensitive trading-intent data to third-party data sources.

Risk: Dependency requirements are loosely pinned.

Mitigation: Pin exact dependency versions and review packages before installing the skill in a shared or production environment.

Risk: Messaging automation claims may be incomplete without separate OpenClaw scheduled-job and channel setup.

Mitigation: Separately configure and approve OpenClaw cron jobs and Feishu or WeChat channels before relying on scheduled reports or alerts.

Risk: Technical indicators, delayed data, and backtests can be misleading if treated as investment advice.

Mitigation: Review outputs as informational analysis only and validate market data, assumptions, and strategy results before making financial decisions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/wangzhaofeng-max/skills/akshare-finance-pro)
- [ClawHub Publisher Profile](https://clawhub.ai/user/wangzhaofeng-max)
- [Eastmoney Historical K-line API](https://push2his.eastmoney.com/api/qt/stock/kline/get)
- [Eastmoney Quote Site](https://quote.eastmoney.com)
- [Eastmoney Real-Time Quote API](https://push2.eastmoney.com/api/qt/clist/get)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with Python, bash, and JSON snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces finance-analysis guidance, watchlist alert examples, holding-report Markdown, and OpenClaw scheduling/channel configuration snippets.]

## Skill Version(s):

1.2.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

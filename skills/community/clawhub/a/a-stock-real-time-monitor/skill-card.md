## Description:

中国A股实时盯盘技能，支持实时行情监控、价格和量比异动提醒、主力资金流向监测、消息面热点监测、彩色提醒和可选企业微信推送。

This skill is ready for commercial/non-commercial use.

## Publisher:

[p4x1s](https://clawhub.ai/user/p4x1s)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to run an agent-managed monitor for selected China A-share stocks, including real-time quotes, abnormal price or volume alerts, fund-flow checks, and market-news monitoring.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can run as a persistent background stock monitor with ongoing network polling.

Mitigation: Run it only in a tracked process that can be stopped, and avoid nohup or screen unless process ownership and shutdown are clear.

Risk: Optional WeCom webhook alerts can send monitored stock activity outside the agent environment.

Mitigation: Keep the webhook unset unless external alert delivery is intentional and the destination is approved.

Risk: Market-data alerts may be incomplete or unreliable, including because one quote source is fetched over HTTP.

Mitigation: Treat alerts as informational and verify market data with trusted financial systems before making decisions.

Risk: Unpinned dependencies can change the behavior of the monitor over time.

Mitigation: Pin and review dependencies before installation in managed environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/p4x1s/skills/a-stock-real-time-monitor)
- [Publisher profile](https://clawhub.ai/user/p4x1s)
- [Sina Finance quote endpoint](http://hq.sinajs.cn/list={codes})
- [Eastmoney fund-flow endpoint](https://push2.eastmoney.com/api/qt/stock/fflow/daykline/get)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and terminal or webhook alert text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Long-running polling behavior; alerts are informational and may be sent through an optional WeCom webhook when configured.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

获取中国 A 股、美股、全球大盘以及期市的行情与深度财务面分析，支持加密货币实时行情与买卖信号，AI 生成每日 A 股精华日报，并提供多通道（微信/Telegram）股价预警推送。

This skill is ready for commercial/non-commercial use.

## Publisher:

[atvisions](https://clawhub.ai/user/atvisions)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to connect an agent to CoolTrade market data for A-share, U.S. stock, global index, futures, cryptocurrency, daily report, and stock-alert workflows. It supports market lookups, financial analysis, informational crypto trading signals, and alert create/list/delete actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a CoolTrade API key and sends market queries, crypto interests, and alert settings to CoolTrade.

Mitigation: Install only if you trust CoolTrade with that data; do not hardcode or share the API key, and rotate it if exposed.

Risk: Generated trading signals and market analysis may be incomplete, delayed, or unsuitable for a user's financial situation.

Mitigation: Treat signals as informational and independently review data before making trading decisions.

Risk: Alert create and delete actions can change a user's notification setup.

Mitigation: Review alert parameters, channels, and alert IDs before creating or deleting alerts.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/atvisions/skills/cooltrade-market-pro)
- [CoolTrade](https://cooltrade.xyz)

## Skill Output:

**Output Type(s):** [text, guidance, configuration]

**Output Format:** [Structured market data and natural-language analysis returned through agent responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a CoolTrade API key; may create, list, or delete stock alerts; trading signals should be treated as informational.]

## Skill Version(s):

1.0.6 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

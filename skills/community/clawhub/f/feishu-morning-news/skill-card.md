## Description:

飞书每日早报配置 Skill，封装每日早报生成流程，包括新闻数据获取、城市天气查询、Markdown 格式整理和生活建议整合。

This skill is ready for commercial/non-commercial use.

## Publisher:

[easyhoov](https://clawhub.ai/user/easyhoov)

### License/Terms of Use:

MIT-0

## Use Case:

External users and teams use this skill to generate a daily Feishu morning report with current news, configurable city weather, brief work/life/health suggestions, and a daily quote.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bundled scripts can send Feishu messages to a fixed recipient even though the skill instructions say message delivery should be handled separately.

Mitigation: Review before installation; separate report generation from delivery, require the recipient to be explicitly configured by the user, and require confirmation before sending.

Risk: The report depends on external news and weather data, so generated content may be stale, unavailable, or inaccurate.

Mitigation: Check source availability during scheduled runs and review generated reports before relying on time-sensitive content.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/easyhoov/skills/feishu-morning-news)
- [60s news data API](https://60s.viki.moe/v2/60s)
- [references/config.json](references/config.json)

## Skill Output:

**Output Type(s):** [Markdown, Text, Guidance, Configuration]

**Output Format:** [Markdown morning report with structured sections for weather, news, suggestions, and a daily quote]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use external news and weather data; Feishu delivery should be configured and confirmed by the user.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

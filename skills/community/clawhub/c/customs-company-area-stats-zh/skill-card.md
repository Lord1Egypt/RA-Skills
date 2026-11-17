## Description:

查询公司海关贸易区域维度统计数据，分析贸易量、金额、月度趋势和国家分布，覆盖全球市场。

This skill is ready for commercial/non-commercial use.

## Publisher:

[upkuajing](https://clawhub.ai/user/upkuajing)

### License/Terms of Use:

MIT-0

## Use Case:

External trade, procurement, and market-intelligence teams use this skill to query company-level customs trade statistics by country or region, including trade volume, value, monthly trends, and country distribution. It helps analyze market coverage, import/export distribution changes, and emerging regional opportunities.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires access to an Upkuajing API key.

Mitigation: Use platform secret storage or a redacted presence check, keep `~/.upkuajing/.env` owner-only, and avoid printing or pasting secret contents.

Risk: Trade-statistics queries and account recharge functions can affect a paid account.

Mitigation: Confirm pricing and get explicit user approval before paid API calls or recharge-order actions.

Risk: Exception reports may include request context from failed API calls.

Mitigation: Ask the user before reporting and avoid including sensitive business data beyond what is needed for troubleshooting.

## Reference(s):

- [公司贸易区域维度统计 API](references/customs-company-area-stats-api.md)
- [Agent 调用 Skill 异常上报 API](references/skill-error-report-api.md)
- [跨境魔方](https://www.upkuajing.com)
- [跨境魔方开放平台](https://developer.upkuajing.com/)
- [开放平台价格说明](https://www.upkuajing.com/web/openapi/price.html)
- [ClawHub Skill Page](https://clawhub.ai/upkuajing/skills/customs-company-area-stats-zh)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands and JSON API results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python and UPKUAJING_API_KEY; API calls may incur account charges.]

## Skill Version(s):

1.0.1 (source: server evidence and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

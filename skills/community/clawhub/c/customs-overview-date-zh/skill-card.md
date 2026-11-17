## Description:

查询日期参考信息，返回去年年份、上月月份和去年当月月份等日期参考值，用于海关贸易数据查询。

This skill is ready for commercial/non-commercial use.

## Publisher:

[upkuajing](https://clawhub.ai/user/upkuajing)

### License/Terms of Use:

MIT-0

## Use Case:

External trade teams, trade analysts, and import/export practitioners use this skill to obtain current reference date parameters for customs data queries, market trend analysis, and trade intelligence workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a real paid Upkuajing API workflow.

Mitigation: Confirm every paid query or recharge-order action with the user before execution.

Risk: The skill requires an API key and may read it from the local Upkuajing environment file.

Mitigation: Do not paste or print the full API key in chat or logs, and restrict permissions on the local environment file.

Risk: Error reports can include request context or payload details.

Mitigation: Avoid sending secrets, personal data, or full payloads in error reports.

Risk: Security evidence marks the release as suspicious because of insecure API-key handling and under-disclosed network and cache behavior.

Mitigation: Review the skill before installing it for use with a real Upkuajing account.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/upkuajing/skills/customs-overview-date-zh)
- [Upkuajing homepage](https://www.upkuajing.com)
- [Upkuajing developer platform](https://developer.upkuajing.com/)
- [OpenAPI pricing](https://www.upkuajing.com/web/openapi/price.html)
- [国家贸易概览-日期相关 API 参考](references/customs-overview-date-api.md)
- [Agent调用Skill异常上报 API 参考](references/skill-error-report-api.md)

## Skill Output:

**Output Type(s):** [text, json, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns date reference fields including yesteryear, lastMonth, and yesteryearMonth; paid API calls require explicit user confirmation before execution.]

## Skill Version(s):

1.0.1 (source: release evidence and frontmatter metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

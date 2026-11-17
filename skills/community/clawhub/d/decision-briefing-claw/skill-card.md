## Description:

每日经营数据自动汇总与简报推送助手（决策简报虾），从数据库、API、Excel、飞书多维表格等数据源采集关键业务指标，计算同比和环比，生成结构化经营简报，并推送到飞书、邮件或企业微信等渠道。

This skill is ready for commercial/non-commercial use.

## Publisher:

[tujinsama](https://clawhub.ai/user/tujinsama)

### License/Terms of Use:

MIT-0

## Use Case:

Business operators, analysts, and developers use this skill to configure daily collection of operating metrics, generate KPI-focused briefing reports, and distribute those reports through configured workplace channels.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can query configured business databases, APIs, and files, which may expose sensitive operational data if credentials or query scope are too broad.

Mitigation: Use read-only credentials, restrict data-source access to the minimum required metrics, and avoid using the arbitrary SQL test command in production.

Risk: Generated reports can be pushed to external or workplace recipients, increasing the chance of unintended disclosure.

Mitigation: Restrict webhook and email destinations, review generated reports before scheduled pushes, and keep channel tokens out of committed configuration.

## Reference(s):

- [Data Sources Configuration Guide](references/data-sources.md)
- [Metrics Calculation Rules](references/metrics-calculation.md)
- [Report Template Library](references/report-templates.md)

## Skill Output:

**Output Type(s):** [Markdown, Files, Shell commands, Configuration]

**Output Format:** [Markdown reports with JSON data files and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports may be archived locally and sent through configured Feishu or email channels.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

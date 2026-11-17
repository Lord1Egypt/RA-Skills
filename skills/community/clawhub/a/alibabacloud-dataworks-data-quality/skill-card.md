## Description:

Queries Alibaba Cloud DataWorks Data Quality rule templates, monitors, alert rules, scan runs, and logs through read-only aliyun CLI calls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and data platform operators use this skill to inspect DataWorks Data Quality configuration, alerting, run history, and execution logs without creating, updating, deleting, or triggering data quality resources.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local Aliyun CLI setup and plugin updates expand trust in local executables and mutable plugins.

Mitigation: Use a preinstalled, administrator-approved Aliyun CLI with pinned or verified plugin versions before running skill commands.

Risk: Cloud credentials and access keys may be exposed if users print or share local configuration details.

Mitigation: Check credential status with aliyun configure list only, and do not read, print, echo, or share AK/SK values.

Risk: Alert receivers and scan run logs can contain sensitive operational information.

Mitigation: Treat alert recipients, webhook targets, and execution logs as sensitive, and redact them before sharing outputs.

Risk: Overbroad Alibaba Cloud permissions increase blast radius even though the skill uses read-only DataWorks APIs.

Mitigation: Use a least-privileged Alibaba Cloud identity limited to the documented List/Get DataWorks Data Quality actions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/sdk-team/skills/alibabacloud-dataworks-data-quality)
- [Aliyun CLI Installation Guide](references/cli-installation-guide.md)
- [DataWorks Data Quality RAM Policies](references/ram-policies.md)
- [DataWorks Data Quality Related APIs](references/related-apis.md)
- [Alibaba Cloud CLI Documentation](https://help.aliyun.com/zh/cli/)
- [DataWorks RAM Permission Guide](https://help.aliyun.com/zh/dataworks/user-guide/dataworks-ram-permissions)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and summary tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Presents query results in concise tables and summaries; avoids raw JSON unless the user asks for full detail.]

## Skill Version(s):

0.0.1-beta.2 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

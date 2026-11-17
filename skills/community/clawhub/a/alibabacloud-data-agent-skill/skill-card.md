## Description:

Invoke Alibaba Cloud Apsara Data Agent for Analytics via CLI to perform natural language-driven data analysis on enterprise databases.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, data engineers, and analysts use this skill to discover Alibaba Cloud DMS/Data Agent data resources, start natural-language database or file analysis sessions, monitor progress, and retrieve generated reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles Alibaba Cloud credentials, database access, local files, generated reports, background monitoring, and custom network destinations.

Mitigation: Review before installing, use tightly scoped Alibaba RAM permissions, avoid broad DMS full-access credentials, and verify trusted destinations before setting custom endpoints.

Risk: Sensitive files or production databases could be analyzed or included in reports before containment issues are resolved.

Mitigation: Avoid sensitive files and production databases until endpoint validation and path-safety issues are fixed; start with non-sensitive test data.

Risk: Autonomous heartbeat notifications can push session progress or report content to chat channels.

Mitigation: Disable or ignore heartbeat-style notifications unless session progress and report delivery to chat channels is explicitly desired.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/sdk-team/skills/alibabacloud-data-agent-skill)
- [Alibaba Cloud Credential Chain Documentation](https://help.aliyun.com/document_detail/378659.html)
- [Data Agent API Key Console](https://agent.dms.aliyun.com/cn-hangzhou/api-key)
- [Subcommand Reference](references/COMMANDS.md)
- [Typical Workflows](references/WORKFLOWS.md)
- [RAM Permission Policies](references/RAM-POLICIES.md)
- [ANALYSIS Mode Sub-Agent Specification](references/ANALYSIS_MODE.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, CLI text output, generated reports, and local session artifacts.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Long-running ANALYSIS and INSIGHT sessions may require plan confirmation and later attachment to retrieve progress, reports, charts, or files.]

## Skill Version(s):

1.8.5 (source: server release evidence and SKILL.md metadata/changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

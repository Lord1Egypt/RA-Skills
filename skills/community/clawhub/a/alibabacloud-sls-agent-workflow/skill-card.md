## Description:

Manage Alibaba Cloud Simple Log Service (SLS) resources and analyze logs. Use when users need to integrate applications through SLS SDKs, set up LoongCollector/Logtail collection, manage Projects, Logstores or indexes, query, analyze or visualize logs, or configure and diagnose alerts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud operators use this skill to route Alibaba Cloud SLS work across SDK integration, collector setup, Logstore and index management, log querying, visualization, and alert workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can ask to install Alibaba Cloud specialist skills globally through an unpinned installer.

Mitigation: Review the exact specialist skill names before approving installation, prefer pinned installer and repository revisions when possible, and use an environment with limited filesystem access.

Risk: The skill guides cloud operations that may create resources, write logs, or configure alerts in Alibaba Cloud SLS.

Mitigation: Use least-privilege Alibaba Cloud credentials, confirm target regions and resource names before execution, and review generated CLI commands before running them.

Risk: Cloud credential exposure would be high impact if AccessKey values are pasted into prompts, files, logs, or command arguments.

Mitigation: Follow the artifact rule to never request, read, or expose AccessKey ID or AccessKey Secret values.

## Reference(s):

- [RAM Policies - SLS Agent Workflow](references/ram-policies.md)
- [Install Specialist Skills](references/install-specialist-skills.md)
- [Example: write and query logs](references/examples/write-and-query-logs.md)
- [Example: collection to alert](references/examples/collection-to-alert.md)
- [Alibaba Cloud SLS CreateProject API](https://help.aliyun.com/zh/sls/developer-reference/api-sls-2020-12-30-createproject)
- [Alibaba Cloud SLS CreateLogStore API](https://help.aliyun.com/zh/sls/developer-reference/api-sls-2020-12-30-createlogstore)
- [Alibaba Cloud SLS GetProject API](https://help.aliyun.com/zh/sls/developer-reference/api-sls-2020-12-30-getproject)
- [Alibaba Cloud SLS GetLogStore API](https://help.aliyun.com/zh/sls/developer-reference/api-sls-2020-12-30-getlogstore)
- [Alibaba Cloud SLS RAM access control permissions](https://help.aliyun.com/zh/sls/log-service-ram-access-control-permissions-configuration)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands, JSON, SQL, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Alibaba Cloud CLI commands, RAM policy examples, user-agent requirements, and handoff guidance for specialist skills.]

## Skill Version(s):

0.0.2 (source: release evidence and references/manifest.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

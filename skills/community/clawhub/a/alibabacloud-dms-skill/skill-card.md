## Description:

Searches Alibaba Cloud DMS databases and executes SQL queries or data modifications through Aliyun CLI workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and database operators use this skill to locate Alibaba Cloud DMS databases, run read queries, and perform guarded data modifications after confirming parameters and credentials.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security summary says the skill asks users to install or update unverified code through the Aliyun CLI and plugin flow.

Mitigation: Use a verified and pinned Aliyun CLI installation path, and do not enable global automatic plugin installation or update unrelated plugins inside an agent session.

Risk: The security summary says the skill enables broad SQL execution with weak safety boundaries.

Mitigation: Use least-privilege RAM roles scoped to approved databases, prefer read-only access for routine use, and require explicit human review for every SQL statement.

Risk: SQL data modifications can change or delete database records.

Mitigation: Preview INSERT, UPDATE, and DELETE statements with dry-run behavior where possible, use force only after review, and keep destructive DDL blocked outside the skill workflow.

Risk: Credentials or secrets can be exposed if pasted into chat, command arguments, shell history, or persistent environment variables.

Mitigation: Check credential status without revealing secret values and configure credentials outside the agent session using approved secure channels.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/sdk-team/skills/alibabacloud-dms-skill)
- [Publisher Profile](https://clawhub.ai/user/sdk-team)
- [CLI Installation Guide](references/cli-installation-guide.md)
- [RAM Permission Policies](references/ram-policies.md)
- [Related API List](references/related-apis.md)
- [Acceptance Criteria](references/acceptance-criteria.md)
- [DMS OpenAPI Overview](https://api.aliyun.com/product/dms-enterprise)
- [Alibaba Cloud RAM Documentation](https://help.aliyun.com/zh/ram/)
- [DMS Permission Management](https://help.aliyun.com/zh/dms/user-guide/permission-management)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, JSON, Markdown]

**Output Format:** [Markdown guidance with inline shell commands and optional JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user-confirmed database identifiers, SQL statements, Aliyun CLI credentials, and RAM permissions before execution.]

## Skill Version(s):

0.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

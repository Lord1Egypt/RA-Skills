## Description:

Alibaba Cloud RDS Copilot helps agents answer RDS questions, optimize SQL, perform instance operations, and troubleshoot database issues by calling RdsAi OpenAPI through Alibaba Cloud CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, database administrators, and operations engineers use this skill to route RDS Copilot tasks through Alibaba Cloud CLI for RDS Q&A, SQL optimization, performance diagnosis, and troubleshooting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can install or update Alibaba Cloud CLI components and enable or install the rdsai plugin.

Mitigation: Review and approve CLI installation, plugin installation, plugin update, sudo, and network commands before execution.

Risk: The skill handles Alibaba Cloud credentials for RDS Copilot access.

Mitigation: Use interactive aliyun configure where possible, avoid placing AccessKey secrets in chat or shell arguments, and use a least-privileged RAM identity.

Risk: RDS Copilot requests may include SQL, logs, customer data, connection strings, tokens, or instance details.

Mitigation: Redact sensitive database and account information before sending context to Alibaba Cloud.

Risk: Generated SQL or operational recommendations may be unsafe for production systems.

Mitigation: Review proposed SQL and operations before execution, especially large data changes, schema changes, or production configuration changes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sdk-team/skills/alibabacloud-rds-copilot)
- [Acceptance Criteria](artifact/references/acceptance-criteria.md)
- [RAM Policies](artifact/references/ram-policies.md)
- [Related APIs](artifact/references/related-apis.md)
- [Verification Method](artifact/references/verification-method.md)
- [Alibaba Cloud CLI Documentation](https://help.aliyun.com/zh/cli/)
- [RDS AI Assistant Professional Edition Guide](https://help.aliyun.com/zh/rds/apsaradb-rds-for-mysql/manage-rds-colipot-professional-edition)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Alibaba Cloud CLI commands, credential setup guidance, error handling guidance, and explanations derived from RDS Copilot responses.]

## Skill Version(s):

0.0.5 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

Manage Alibaba Cloud PolarDB-X instance lifecycle and routine operations via the Aliyun CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud operators use this skill to plan and generate Aliyun CLI commands for Alibaba Cloud PolarDB-X instance lifecycle, scaling, configuration, monitoring, logs, security, backup, and related operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can generate commands that create, delete, restart, scale, upgrade, or reconfigure PolarDB-X databases.

Mitigation: Use a narrowly scoped RAM role or instance-specific policy and require explicit confirmation before create, delete, restart, upgrade, parameter, security, or account changes.

Risk: Credential, password, slow-log, and binlog data may be sensitive if copied into chat, command history, logs, or generated files.

Mitigation: Use placeholders or protected shell variables for secrets, avoid printing credentials, and treat logs and binlog links as sensitive operational data.

Risk: Installer or CLI setup commands can change the local execution environment.

Mitigation: Verify the Aliyun CLI installer and plugin source out of band before installation or upgrade.

Risk: Generated administration commands can affect billing, availability, topology, access control, or data durability.

Mitigation: Review generated commands before execution, confirm target region and instance identifiers, and obtain explicit user approval for disruptive or billable actions.

## Reference(s):

- [PolarDB-X OpenAPI documentation](https://api.aliyun.com/document/polardbx/2020-02-02/overview)
- [Reference Index](references/index.md)
- [CLI Installation & Configuration](references/cli-installation-guide.md)
- [RAM Permissions](references/ram-policies.md)
- [Security & Access APIs](references/security-access.md)
- [Instance Lifecycle APIs](references/instance-lifecycle.md)
- [Scaling APIs](references/scaling.md)
- [Monitoring & Logs APIs](references/monitoring-logs.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with Aliyun CLI command examples and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands are intended to include required region flags, timeouts, user-agent observability, and explicit confirmation for disruptive operations.]

## Skill Version(s):

0.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

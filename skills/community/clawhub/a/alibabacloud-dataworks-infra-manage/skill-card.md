## Description:

DataWorks Infrastructure Management helps agents create and query Alibaba Cloud DataWorks data sources, compute resources, and serverless resource groups, including connectivity testing and resource group binding or unbinding through aliyun CLI calls to dataworks-public OpenAPI (2024-05-18).

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud operators use this skill to manage Alibaba Cloud DataWorks infrastructure setup from an agent, including workspace-related data sources, compute resources, resource groups, and connectivity checks. It is intended for guided operational workflows where users confirm parameters before cloud write actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide cloud operations that require broad DataWorks, VPC, billing, and resource-group permissions.

Mitigation: Use a minimally scoped RAM role for the intended tasks and avoid the Full Access policy except in controlled review environments.

Risk: Data source and CLI examples involve credentials, passwords, access keys, refresh tokens, or bearer tokens.

Mitigation: Do not paste real secrets into chat or shell commands; configure credentials through trusted Aliyun CLI or credential-file flows and only check status with credential listing commands.

Risk: Automatic CLI plugin installation and global or sudo installs can introduce supply-chain and host-level exposure.

Mitigation: Verify CLI and plugin integrity through trusted vendor channels, avoid sudo or global installs where possible, and enable automatic plugin installation only when the deployment accepts that risk.

Risk: Some reference examples use HTTP, FTP, no-SSL, or anonymous connection patterns that may be unsafe for production data access.

Mitigation: Treat those patterns as non-production examples unless explicitly approved by the organization's security team.

Risk: Creating PostPaid resource groups can incur cloud charges.

Mitigation: Confirm cost impact and resource-group parameters before creation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sdk-team/skills/alibabacloud-dataworks-infra-manage)
- [Aliyun CLI installation guide](references/cli-installation-guide.md)
- [Data source type and connection properties](references/data-sources/README.md)
- [Compute resource connection properties](references/compute-resources/README.md)
- [Cross-account data source configuration guide](references/cross-account-datasources.md)
- [DataWorks infrastructure RAM policies](references/ram-policies.md)
- [DataWorks infrastructure related APIs](references/related-apis.md)
- [Alibaba Cloud CLI official documentation](https://help.aliyun.com/zh/cli/)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, API calls]

**Output Format:** [Markdown guidance with inline bash commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands are expected to use the AlibabaCloud-Agent-Skills user agent, confirm user-customizable parameters, and verify state after write operations.]

## Skill Version(s):

0.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

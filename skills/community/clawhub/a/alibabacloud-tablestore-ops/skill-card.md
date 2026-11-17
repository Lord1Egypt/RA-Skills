## Description:

Guides agents through read-only Alibaba Cloud Tablestore instance and table inspection using Aliyun CLI otsutil commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and cloud support engineers use this skill to list and describe Alibaba Cloud Tablestore instances and tables, confirm endpoint and region parameters, and verify read-only CLI results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: CLI installation guidance downloads binaries and includes privileged installation commands.

Mitigation: Use a verified and pinned Aliyun CLI release where possible, prefer a user-local PATH, and avoid system-wide sudo installation unless explicitly required.

Risk: Some RAM examples include permissions broader than the read-only workflow needs.

Mitigation: Use AliyunOTSReadOnlyAccess or a custom policy limited to ots:GetInstance, ots:ListInstance, ots:ListTable, and ots:DescribeTable; do not copy examples that attach AliyunOTSFullAccess or include ots:CreateInstance.

Risk: The workflow depends on Alibaba Cloud credentials and command output can reveal account metadata.

Mitigation: Use temporary, role-based, or dedicated least-privilege RAM credentials and redact AccessKey-related output from logs, chats, and tickets.

## Reference(s):

- [CLI Installation Guide](references/cli-installation-guide.md)
- [RAM Policies](references/ram-policies.md)
- [Related APIs](references/related-apis.md)
- [Verification Method](references/verification-method.md)
- [Acceptance Criteria](references/acceptance-criteria.md)
- [Aliyun CLI GitHub](https://github.com/aliyun/aliyun-cli)
- [Alibaba Cloud Tablestore Instance Operations](https://help.aliyun.com/zh/tablestore/developer-reference/instance-operations)
- [Alibaba Cloud Tablestore Data Table Operations](https://help.aliyun.com/zh/tablestore/developer-reference/widecolumn-modeled-data-table-operations-with-tablestore-cli)
- [Tablestore Authorization Rules](https://help.aliyun.com/zh/tablestore/developer-reference/ots-api-authorization-rules/)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only operational guidance; may include commands that query cloud account metadata or export table descriptions to local files.]

## Skill Version(s):

0.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

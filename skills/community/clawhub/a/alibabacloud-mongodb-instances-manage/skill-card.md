## Description:

Manages Alibaba Cloud ApsaraDB for MongoDB instances across creation, querying, scaling, deletion, node management, security settings, backups, upgrades, HA switchover, accounts, tags, renewal, and billing operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud operators use this skill to manage the full lifecycle of Alibaba Cloud MongoDB instances through Aliyun CLI workflows, including resource creation, configuration, maintenance, backups, and deletion. It is intended for users who need guided command generation and operational checks for standalone, replica set, and sharded cluster deployments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide broad Alibaba Cloud MongoDB administration with powerful credentials.

Mitigation: Use a dedicated RAM user with the smallest permissions needed and review requested permissions before use.

Risk: The skill asks users to run mutable Aliyun CLI and plugin installation or update steps.

Mitigation: Verify CLI and plugin provenance before installing, and avoid automatic plugin updates where possible.

Risk: The skill covers destructive or sensitive operations such as deletion, password reset, public endpoint changes, billing changes, KMS changes, and backup-retention changes.

Mitigation: Require explicit human review and confirmation before executing these operations.

Risk: Agent-visible commands can expose cloud secrets if users paste or print credentials.

Mitigation: Avoid entering real secrets in agent-visible commands and check credential status without echoing access keys.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sdk-team/skills/alibabacloud-mongodb-instances-manage)
- [Operations reference](references/operations.md)
- [Related APIs](references/related-apis.md)
- [RAM policies](references/ram-policies.md)
- [Verification method](references/verification-method.md)
- [CLI installation guide](references/cli-installation-guide.md)
- [Acceptance criteria](references/acceptance-criteria.md)
- [CreateDBInstance API documentation](https://help.aliyun.com/zh/mongodb/developer-reference/api-dds-2015-12-01-createdbinstance)
- [CreateShardingDBInstance API documentation](https://help.aliyun.com/zh/mongodb/developer-reference/api-dds-2015-12-01-createshardingdbinstance)
- [DeleteDBInstance API documentation](https://help.aliyun.com/zh/mongodb/developer-reference/api-dds-2015-12-01-deletedbinstance)
- [ModifyBackupPolicy API documentation](https://help.aliyun.com/zh/mongodb/developer-reference/api-dds-2015-12-01-modifybackuppolicy)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces Aliyun CLI command guidance, configuration steps, permission policy snippets, and operation verification checks.]

## Skill Version(s):

0.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

Provides guidance and aliyun CLI workflows for Alibaba Cloud Tair architecture selection, data structure design, instance creation, connection management, monitoring, troubleshooting, and backup or recovery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud operators use this skill to plan, configure, connect to, monitor, troubleshoot, back up, and restore Alibaba Cloud Tair instances. It can assist with real Alibaba Cloud operations through aliyun CLI commands and bundled shell workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can assist with live Alibaba Cloud Tair administration, including instance creation, whitelist changes, public endpoint allocation, backups, and restores.

Mitigation: Use a sandbox or least-privilege RAM role, confirm all user-customizable parameters, review public endpoint creation, and keep credentials out of chat and shell history.

Risk: Restore workflows can overwrite current data and may be irreversible.

Mitigation: Create and verify a current backup, confirm the target instance and restore point with the user, and prefer a new-instance restore when appropriate.

Risk: Examples and downloaded tools may be unsafe if run without review or pinning.

Mitigation: Pin and verify downloaded tools, review generated commands before execution, and require TLS with certificate and hostname validation for production connections.

## Reference(s):

- [RAM permission policy](references/ram-policies.md)
- [Architecture selection guide](references/architecture-selection/arch-selection.md)
- [Tair vs Open Source Redis comparison](references/architecture-selection/arch-compare-oss-redis.md)
- [Data structure design guide](references/data-structure-design/data-structure-design.md)
- [Instance creation and connection guide](references/instance-creation/connect-create-instance.md)
- [Standalone or proxy connection guide](references/connection-management/connect-standalone-or-proxy.md)
- [Cluster connection guide](references/connection-management/connect-cluster.md)
- [TLS connection guide](references/connection-management/connect-with-tls.md)
- [Backup and recovery guide](references/backup-and-recovery/backup-recovery.md)
- [Redis data types](https://redis.io/docs/latest/develop/data-types/)
- [Tair extended data structures](https://help.aliyun.com/zh/redis/developer-reference/extended-data-structures-of-apsaradb-for-redis-enhanced-edition)
- [Alibaba Cloud Redis common errors and troubleshooting](https://www.alibabacloud.com/help/en/redis/support/common-errors-and-troubleshooting)
- [Alibaba Cloud Redis backup and restoration solutions](https://www.alibabacloud.com/help/en/redis/user-guide/backup-and-restoration-solutions)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline code blocks, CLI commands, and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include high-impact operational steps that require user confirmation, least-privilege credentials, and backup validation before execution.]

## Skill Version(s):

0.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

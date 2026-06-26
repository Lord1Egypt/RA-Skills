## Description: <br>
Alibaba Cloud Tair development toolkit covering architecture selection, data structure design, instance creation and configuration, connection management, performance monitoring, error troubleshooting, and backup and recovery. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and cloud engineers use this skill to plan, create, connect, monitor, troubleshoot, and recover Alibaba Cloud Tair Redis-compatible resources through guided procedures and aliyun CLI workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create billable Alibaba Cloud Tair resources and expose database endpoints. <br>
Mitigation: Use a least-privilege RAM role scoped to the required account, region, and instances; do not run creation workflows unless paid resource creation and endpoint exposure are explicitly accepted. <br>
Risk: Restore and destructive database operations can overwrite or remove current data. <br>
Mitigation: Treat restore and SHUTDOWN NOSAVE as last-resort operations after backups, written confirmation, and review of the affected instance. <br>
Risk: Credential, TLS, and client examples may be unsafe if copied directly into production code. <br>
Mitigation: Replace examples with secure credential handling, production TLS configuration, and private or VPC connectivity before operational use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sdk-team/alibabacloud-tair-devtoolset) <br>
- [Acceptance Criteria](references/acceptance-criteria.md) <br>
- [Architecture Selection](references/architecture-selection/arch-selection.md) <br>
- [Tair vs Open Source Redis](references/architecture-selection/arch-compare-oss-redis.md) <br>
- [Backup and Recovery](references/backup-and-recovery/backup-recovery.md) <br>
- [CLI Installation Guide](references/cli-installation-guide.md) <br>
- [Connect to Cluster](references/connection-management/connect-cluster.md) <br>
- [Connect to Standalone or Proxy](references/connection-management/connect-standalone-or-proxy.md) <br>
- [Connect with TLS](references/connection-management/connect-with-tls.md) <br>
- [Data Structure Design](references/data-structure-design/data-structure-design.md) <br>
- [Error Troubleshooting](references/error-troubleshooting/errors-troubleshooting.md) <br>
- [Instance Creation](references/instance-creation/connect-create-instance.md) <br>
- [Performance Monitoring](references/performance-monitoring/perf-monitoring.md) <br>
- [RAM Policies](references/ram-policies.md) <br>
- [Related Commands](references/related-commands.md) <br>
- [Verification Method](references/verification-method.md) <br>
- [Redis Data Types](https://redis.io/docs/latest/develop/data-types/) <br>
- [Tair Extended Data Structures](https://help.aliyun.com/zh/redis/developer-reference/extended-data-structures-of-apsaradb-for-redis-enhanced-edition) <br>
- [Alibaba Cloud Redis Common Errors and Troubleshooting](https://www.alibabacloud.com/help/en/redis/support/common-errors-and-troubleshooting) <br>
- [Alibaba Cloud Redis Backup and Restoration Solutions](https://www.alibabacloud.com/help/en/redis/user-guide/backup-and-restoration-solutions) <br>
- [alibabacloud-tair-ai-assistant](https://skills.aliyun.com/skills/alibabacloud-tair-ai-assistant) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline bash commands, configuration values, and code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose or execute aliyun CLI workflows after user-confirmed parameters and credential prerequisites.] <br>

## Skill Version(s): <br>
0.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

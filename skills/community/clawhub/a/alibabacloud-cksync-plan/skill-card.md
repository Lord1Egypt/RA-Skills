## Description: <br>
ClickHouse cluster migration planner for planning data migration between ClickHouse clusters, including cross-cluster migrations, horizontal scaling, disk downgrade, availability zone changes, and migrations from self-built or non-Alibaba Cloud ClickHouse to Alibaba Cloud ClickHouse. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, database administrators, and migration engineers use this skill to collect ClickHouse cluster facts, compare migration methods, and produce a practical migration plan with risks, rollback steps, timelines, and reference links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated migration plans may include production database credential handling steps. <br>
Mitigation: Prefer pasted query results over shared credentials; when access is necessary, use temporary read-only accounts and avoid exposing secrets in chat or files. <br>
Risk: Plans may recommend network allowlisting or password-free access patterns that broaden production database exposure. <br>
Mitigation: Have an authorized operator verify target endpoints, source ranges, access scope, maintenance windows, and rollback procedures before changing network access. <br>
Risk: Plans may include destructive or disruptive SQL and operational steps such as DROP, TRUNCATE, ALTER, whitelist changes, or password-free access configuration. <br>
Mitigation: Do not execute these steps until backups, target resources, impact window, and rollback plan have been independently reviewed and approved. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/sdk-team/alibabacloud-cksync-plan) <br>
- [Migration Plans - Detailed Conditions](references/plans.md) <br>
- [SQL Reference](references/sql.md) <br>
- [RAM Permission Declaration](references/ram-policies.md) <br>
- [How To Stop Merge Storm](references/stop-merge-storm.md) <br>
- [Community + Enterprise Big Cluster Federation](references/big-cluster-community-enterprise.md) <br>
- [Self-Built + Cloud ClickHouse Big Cluster Federation](references/big-cluster-self-built-community.md) <br>
- [Alibaba Cloud ClickHouse Compatibility and Performance Bottleneck Analysis](https://help.aliyun.com/zh/clickhouse/user-guide/analysis-and-solution-of-cloud-compatibility-and-performance-bottleneck-of-self-built-clickhouse) <br>
- [Alibaba Cloud ClickHouse Backup and Restore Commands](https://help.aliyun.com/zh/clickhouse/user-guide/use-the-backup-and-restore-commands-for-data-backup-and-restoration) <br>
- [ClickHouse S3 Backup Endpoint Documentation](https://clickhouse.com/docs/operations/backup/s3_endpoint) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown migration plan with tables and inline SQL or shell commands when needed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces one migration plan by default; additional files or scripts are generated only when requested.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

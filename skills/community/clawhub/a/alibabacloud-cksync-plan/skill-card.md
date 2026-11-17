## Description:

Plans ClickHouse cluster migrations by collecting cluster metadata, selecting an appropriate migration method, and producing a detailed migration plan with risks, rollback steps, and timelines.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, database engineers, and cloud migration teams use this skill to plan ClickHouse migrations between self-built, non-Alibaba Cloud, and Alibaba Cloud ClickHouse clusters. It helps gather required database and table facts, compare migration methods, and prepare a single migration plan.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may ask for database or cloud credentials while gathering ClickHouse metadata.

Mitigation: Prefer user-executed, read-only metadata queries; do not paste production passwords into chat; use HTTPS/TLS and short-lived least-privilege accounts.

Risk: Generated migration plans can include high-impact database operations such as ALTER, TRUNCATE, DROP, switchover, or decommission steps.

Mitigation: Require human review, verified backups, identity checks, and rollback validation before executing any high-impact operation.

Risk: Credential persistence examples could lead to secrets being stored in shell startup files or netrc files.

Mitigation: Avoid storing secrets in .bashrc or .netrc; use temporary environment variables or managed secret workflows with least-privilege accounts.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sdk-team/skills/alibabacloud-cksync-plan)
- [Publisher profile](https://clawhub.ai/user/sdk-team)
- [Migration plan conditions](artifact/references/plans.md)
- [SQL reference](artifact/references/sql.md)
- [RAM permission declaration](artifact/references/ram-policies.md)
- [Community and Enterprise big cluster federation](artifact/references/big-cluster-community-enterprise.md)
- [Self-built and cloud big cluster federation](artifact/references/big-cluster-self-built-community.md)
- [Stop merge storm reference](artifact/references/stop-merge-storm.md)
- [Alibaba Cloud ClickHouse compatibility analysis](https://help.aliyun.com/zh/clickhouse/user-guide/analysis-and-solution-of-cloud-compatibility-and-performance-bottleneck-of-self-built-clickhouse)
- [Alibaba Cloud ClickHouse backup and restore](https://help.aliyun.com/zh/clickhouse/user-guide/use-the-backup-and-restore-commands-for-data-backup-and-restoration)
- [ClickHouse backup to S3 endpoint](https://clickhouse.com/docs/operations/backup/s3_endpoint)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown migration plan with SQL, shell command, and configuration snippets when needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Default deliverable is one migration plan; supplementary files, scripts, or SQL are produced only when requested.]

## Skill Version(s):

0.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

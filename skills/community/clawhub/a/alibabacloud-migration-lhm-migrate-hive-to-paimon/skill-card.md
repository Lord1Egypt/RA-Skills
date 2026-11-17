## Description:

Migrates Hive data warehouses to Alibaba Cloud DLF Paimon by converting Hive DDL, generating Paimon and format-table DDL, syncing HDFS data to OSS or using direct-read mode, and loading full or incremental data through Spark SQL.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and data platform engineers use this skill to plan and execute full or incremental Hive-to-DLF Paimon migrations, including DDL conversion, external table generation, rclone-based or direct-read data movement, Spark SQL table creation, and row-count verification.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The migration flow can perform high-impact writes, including CREATE TABLE, DROP TABLE in force mode, rclone copy, and INSERT OVERWRITE operations.

Mitigation: Run with --dry-run first, inspect generated SQL and sync commands, require explicit human confirmation for write operations, and confirm target Paimon tables are disposable or backed up before execution.

Risk: Automatic dependency installation and shell execution paths can run commands that affect the host environment.

Mitigation: Install rclone through a trusted package path before running the skill, avoid running as root, and review generated shell commands before execution.

Risk: Migration configuration can contain cloud access keys and service passwords.

Mitigation: Use temporary least-privilege credentials, provide secrets through environment variables, keep config.ini out of version control, and rotate credentials if they appear in logs or reports.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sdk-team/skills/alibabacloud-migration-lhm-migrate-hive-to-paimon)
- [Overview](references/overview.md)
- [Agent Execution Rules](references/agent-rules.md)
- [Configuration Reference](references/configuration.md)
- [SERDE Mapping Reference](references/serde-mapping.md)
- [Troubleshooting](references/troubleshooting.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with inline shell commands, generated SQL/DDL, configuration values, CSV reports, logs, and migration result files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May generate Paimon DDL, external-table DDL, INSERT OVERWRITE SQL, rclone commands, migration manifests, row-count verification SQL, and per-step result reports.]

## Skill Version(s):

0.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

Provides database selection, query and index optimization, performance diagnosis, schema migration, transaction troubleshooting, capacity planning, and backup and recovery guidance for MySQL, PostgreSQL, and MongoDB.

This skill is ready for commercial/non-commercial use.

## Publisher:

[skills-repo](https://clawhub.ai/user/skills-repo)

### License/Terms of Use:

MIT

## Use Case:

Developers and database engineers use this skill to select and operate MySQL, PostgreSQL, or MongoDB systems, diagnose query and performance issues, review schema changes, and plan database reliability work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The execution-plan checker may report a clean result despite issues.

Mitigation: Use PostgreSQL text plans until the JSON auditor is corrected, review the plan independently, and do not rely only on the script's success status.

Risk: Query diagnostics may execute database work, and slow-log reports may expose sensitive SQL values.

Mitigation: Use scoped database access, review queries before running diagnostics, and redact sensitive values from logs and reports.

Risk: Suggested production changes can cause data loss or service impact if applied without safeguards.

Mitigation: Keep a human in control of production changes and validate backups and rollback plans before execution.

## Reference(s):

- [Engine selection](references/engine-selection.md)
- [Execution plan reading](references/explain-reading.md)
- [Index design](references/index-design.md)
- [Slow query triage](references/slow-query-triage.md)
- [Schema migration](references/schema-migration.md)
- [Transactions and locking](references/transactions-locking.md)
- [Capacity and connection pooling](references/capacity-and-pooling.md)
- [Backup and recovery](references/backup-recovery.md)
- [Schema review checklist](assets/schema-review-checklist.md)
- [Database alert rules](assets/db-alert-rules.yml)
- [Backup runbook](assets/backup-runbook.md)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with SQL, Python, and shell examples; JSON or YAML reports and configuration where appropriate]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include diagnostic findings, prioritized recommendations, and rollback considerations.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter, server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

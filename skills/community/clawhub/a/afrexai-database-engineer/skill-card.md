## Description:

Database Engineering Mastery helps agents design schemas, optimize queries, plan migrations, and prepare operational database guidance for PostgreSQL, MySQL, SQLite, and general SQL workloads.

This skill is ready for commercial/non-commercial use.

## Publisher:

[1kalin](https://clawhub.ai/user/1kalin)

### License/Terms of Use:


## Use Case:

Developers, database engineers, and agents use this skill to create database schemas, indexing strategies, query rewrites, safe migration plans, monitoring checks, backup procedures, and operational runbooks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: SQL examples and operational commands may affect production data or availability if applied without review.

Mitigation: Review generated SQL and commands before execution, especially audit triggers, destructive maintenance commands, backup deletion, replication-slot changes, and emergency termination commands.

Risk: Audit-log patterns may capture sensitive fields or expose audit records too broadly.

Mitigation: Redact sensitive audit fields and restrict audit-table access when adopting the audit-log pattern.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/1kalin/skills/afrexai-database-engineer)
- [Artifact README](artifact/README.md)
- [Skill source](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with SQL, bash, YAML, and INI code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes database-specific examples and operational commands that should be reviewed before production use.]

## Skill Version(s):

1.0.0 (source: server release metadata, created 2026-02-16)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

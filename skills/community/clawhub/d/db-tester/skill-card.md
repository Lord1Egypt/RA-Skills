## Description:

Database testing for data integrity, SQL validation, migration verification, and performance across MySQL, PostgreSQL, SQLite, and other RDBMS.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhanghengyi1986-afk](https://clawhub.ai/user/zhanghengyi1986-afk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to validate database operations, constraints, migrations, transactions, and performance behavior. It helps produce SQL checks, shell commands, and Python test patterns for relational database testing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: SQL examples can delete or change real database data.

Mitigation: Run tests only against isolated non-production databases with disposable records, least-privileged credentials, and explicit transactions or snapshots.

Risk: Some MySQL examples alter server-wide settings or exercise deadlock behavior.

Mitigation: Require DBA approval before server-wide settings changes and do not run SET GLOBAL or deadlock examples against shared or production systems as written.

Risk: Database examples are templates that may not fit a user's schema or safety controls as written.

Mitigation: Review and adapt every SQL, shell, and Python example before execution.

## Reference(s):

- [MySQL Specific Tests](references/mysql-tests.md)
- [PostgreSQL Specific Tests](references/postgresql-tests.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with SQL, bash, and Python code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Database examples require adaptation before execution.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

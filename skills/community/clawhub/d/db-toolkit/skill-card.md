## Description:

Lightweight multi-database toolkit for MySQL, PostgreSQL, and SQLite DDL/DML operations and schema exploration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leonardo-lb](https://clawhub.ai/user/leonardo-lb)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to test database connectivity, inspect live table metadata, and prepare database DDL/DML work across MySQL, PostgreSQL, and SQLite projects.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may read project configuration files to discover database credentials.

Mitigation: Review discovered connection details before use and prefer providing limited, non-production, read-only credentials explicitly.

Risk: Database passwords may be passed through plaintext command-line arguments.

Mitigation: Avoid passing real passwords on the command line; use temporary or least-privilege credentials and clear shell history where needed.

Risk: The documented global npm dependency install can affect the wider agent environment.

Mitigation: Use a project-local dependency install instead of a global npm install.

Risk: The skill connects to real databases and can support DDL/DML workflows.

Mitigation: Use read-only credentials for inspection tasks and require human confirmation before destructive changes such as DROP, TRUNCATE, UPDATE, or DELETE.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/leonardo-lb/skills/db-toolkit)
- [MySQL connection reference](references/mysql/connection.md)
- [MySQL DDL reference](references/mysql/ddl.md)
- [MySQL DML reference](references/mysql/dml.md)
- [PostgreSQL connection reference](references/postgresql/connection.md)
- [PostgreSQL DDL reference](references/postgresql/ddl.md)
- [PostgreSQL DML reference](references/postgresql/dml.md)
- [SQLite connection reference](references/sqlite/connection.md)
- [SQLite DDL reference](references/sqlite/ddl.md)
- [SQLite DML reference](references/sqlite/dml.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON results from helper scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Database inspection scripts return JSON for table lists and table schema details.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

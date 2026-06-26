## Description: <br>
db-toolkit helps agents connect to MySQL, PostgreSQL, and SQLite databases to test connections, inspect schemas, and guide DDL/DML work. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[leonardo-lb](https://clawhub.ai/user/leonardo-lb) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to test database connections, inspect live database schemas, list tables, and prepare database-specific SQL for MySQL, PostgreSQL, and SQLite. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can inspect local database configuration files while discovering connection details. <br>
Mitigation: Use least-privilege credentials, keep production credentials out of the agent workspace when possible, and review discovered connection details before use. <br>
Risk: The skill can connect to real databases and may guide insert, update, delete, ALTER, DROP, TRUNCATE, or index changes. <br>
Mitigation: Require the agent to show the exact host, database, account, and SQL before any database-changing operation, and prefer read-only or non-production accounts. <br>


## Reference(s): <br>
- [MySQL Connection Reference](artifact/references/mysql/connection.md) <br>
- [MySQL DDL Reference](artifact/references/mysql/ddl.md) <br>
- [MySQL DML Reference](artifact/references/mysql/dml.md) <br>
- [PostgreSQL Connection Reference](artifact/references/postgresql/connection.md) <br>
- [PostgreSQL DDL Reference](artifact/references/postgresql/ddl.md) <br>
- [PostgreSQL DML Reference](artifact/references/postgresql/dml.md) <br>
- [SQLite Connection Reference](artifact/references/sqlite/connection.md) <br>
- [SQLite DDL Reference](artifact/references/sqlite/ddl.md) <br>
- [SQLite DML Reference](artifact/references/sqlite/dml.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell, SQL, and JSON snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May run TypeScript helper scripts that return JSON for connection tests, table lists, and table schemas.] <br>

## Skill Version(s): <br>
1.0.2 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

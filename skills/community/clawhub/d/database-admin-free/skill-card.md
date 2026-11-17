## Description: <br>
数据库管理(免费版) helps agents draft PostgreSQL-oriented table definitions, INSERT statements, simple SELECT queries, indexes, and transaction blocks for routine database operations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and database operators use this skill to generate basic PostgreSQL table schemas, insert data, write simple queries, and plan transaction handling for day-to-day database administration tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated SQL can create tables, indexes, transactions, or insert records in a real database. <br>
Mitigation: Confirm the target database and credentials, review generated SQL before execution, and prefer a test database or backup before applying changes. <br>
Risk: Incorrect table definitions, data types, constraints, or transaction boundaries can produce failed writes or misleading query results. <br>
Mitigation: Validate schema choices, required fields, and transaction COMMIT/ROLLBACK behavior before using the output in operational workflows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/database-admin-free) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with SQL, JSON, and shell code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include SQL statements that should be reviewed before execution against a live database.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Description: <br>
Database Tester helps agents validate relational database operations, data integrity, SQL behavior, migrations, and performance across MySQL, PostgreSQL, SQLite, and other RDBMS. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhanghengyi1986-afk](https://clawhub.ai/user/zhanghengyi1986-afk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and QA engineers use this skill to generate and review database validation steps for CRUD behavior, constraints, transactions, migrations, slow queries, and post-API data consistency checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill includes copyable SQL examples that can delete data, mutate records, run migrations, create deadlocks, or change server-wide MySQL settings. <br>
Mitigation: Use the skill only against staging, local, or disposable databases with least-privilege test accounts; explicitly review DELETE, UPDATE, migration, deadlock, API mutation, and SET GLOBAL examples before execution. <br>


## Reference(s): <br>
- [MySQL Specific Tests](references/mysql-tests.md) <br>
- [PostgreSQL Specific Tests](references/postgresql-tests.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/zhanghengyi1986-afk/db-tester) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with SQL, Bash, and Python code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces executable examples that require review before use against any database.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

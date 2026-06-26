## Description: <br>
Helps agents work with SQLite and MySQL databases by generating or using Python utilities for SQL queries, data changes, table statistics, backups, and JSON import/export. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qiuwenxi416488212-ship-it](https://clawhub.ai/user/qiuwenxi416488212-ship-it) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and data-focused agents use this skill to inspect database structure, run SQL queries, update records, export or import JSON data, and create backups for SQLite or MySQL workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can execute SQL that reads, inserts, updates, deletes, or drops database data. <br>
Mitigation: Use least-privileged or read-only accounts where possible, review SQL before execution, and back up important databases before write operations. <br>
Risk: Database credentials or sensitive query results may be exposed if shared with the agent or written into outputs. <br>
Mitigation: Avoid production root credentials, provide only scoped credentials, and redact sensitive data before sharing outputs. <br>
Risk: Redis support includes a flush operation that can erase a selected Redis database. <br>
Mitigation: Do not invoke Redis flush operations unless erasure is intended and the selected database has been confirmed. <br>
Risk: Unpinned optional dependencies can vary across environments. <br>
Mitigation: Pin dependencies in controlled environments before deployment. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/qiuwenxi416488212-ship-it/database-toolkit) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python and SQL code snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include database connection settings, SQL statements, backup paths, and dependency installation commands.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

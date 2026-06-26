## Description: <br>
Connect to and explore databases (PostgreSQL, MySQL, SQLite, MongoDB, Redis), run queries, inspect schemas, export data, and debug database issues. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lrg913427-dot](https://clawhub.ai/user/lrg913427-dot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to connect to PostgreSQL, MySQL, SQLite, MongoDB, and Redis databases, inspect schemas, run diagnostic queries, and export results. It is useful for database exploration, troubleshooting, performance checks, backups, restores, and migration planning. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Database connection details and credentials may expose sensitive systems or data if copied into commands, logs, or shell history. <br>
Mitigation: Use limited database accounts, prefer read-only access by default, keep credentials in environment variables or secure configuration, and avoid echoing secrets. <br>
Risk: Export, backup, restore, import, migration, and write examples can expose, overwrite, or modify important data. <br>
Mitigation: Review every command before execution, require explicit confirmation for writes or restore/import/migration work, limit query results unless full export is requested, and handle generated files under applicable data retention rules. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lrg913427-dot/db-explorer-gavin) <br>
- [MongoDB Shell documentation](https://mongodb.com/docs/shell) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, code, configuration, guidance] <br>
**Output Format:** [Markdown with shell, SQL, and database CLI command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include read-only query plans, schema summaries, export commands, backup and restore commands, and safety checks for database operations.] <br>

## Skill Version(s): <br>
2.5.2 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

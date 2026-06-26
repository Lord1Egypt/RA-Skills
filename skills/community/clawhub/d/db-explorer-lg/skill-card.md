## Description: <br>
Connect to and explore databases (PostgreSQL, MySQL, SQLite, MongoDB, Redis), run queries, inspect schemas, export data, and debug database issues. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lrg913427-dot](https://clawhub.ai/user/lrg913427-dot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, database administrators, and support engineers use this skill to inspect database schemas, run diagnostic read queries, export scoped results, and troubleshoot PostgreSQL, MySQL, SQLite, MongoDB, and Redis systems from a terminal. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Restore, import, migration, and write commands can make high-impact changes to databases. <br>
Mitigation: Use read-only or least-privileged credentials by default, review every command before execution, and require separate explicit confirmation before writes, restores, imports, migrations, or full exports. <br>
Risk: Database exports and backups can expose sensitive or production data. <br>
Mitigation: Avoid production or admin access unless explicitly needed, scope exports to the minimum required data, and confirm destination paths before creating dump or export files. <br>
Risk: Connection strings and passwords may be exposed through shell history or command output. <br>
Mitigation: Prefer environment variables or protected secret handling, avoid echoing passwords, and redact credentials from any shared output. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lrg913427-dot/db-explorer-lg) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/lrg913427-dot) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and database query examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose database client commands, SQL queries, export commands, backup commands, restore commands, and safety checks.] <br>

## Skill Version(s): <br>
2.0.0 (source: release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Description: <br>
Connect to and explore databases (PostgreSQL, MySQL, SQLite, MongoDB, Redis). Run queries, inspect schemas, export data. Use when user wants to query a database, explore schema, check data, export results, or debug database issues. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lrg913427-dot](https://clawhub.ai/user/lrg913427-dot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to connect to PostgreSQL, MySQL, SQLite, MongoDB, or Redis databases from the terminal, inspect schemas and row counts, run diagnostic queries, and export selected results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use database credentials and run database commands in the user's environment. <br>
Mitigation: Use read-only or least-privilege non-production credentials when possible and review every command before execution. <br>
Risk: Restore, import, migration, or write operations could change database state. <br>
Mitigation: Require explicit approval for any restore, import, migration, or write operation, and show the exact command before running it. <br>
Risk: Exports and backups may contain sensitive data. <br>
Mitigation: Limit exports to the needed data and delete exported or backup files when they are no longer required. <br>
Risk: Broad scans or unrestricted queries can stress production systems. <br>
Mitigation: Avoid broad production scans and use limited, targeted queries by default. <br>


## Reference(s): <br>
- [Db Explorer ClawHub release](https://clawhub.ai/lrg913427-dot/db-explorer-lrg913427) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Markdown, Code, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline shell and database command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose database CLI commands, query examples, export paths, and environment variable usage.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

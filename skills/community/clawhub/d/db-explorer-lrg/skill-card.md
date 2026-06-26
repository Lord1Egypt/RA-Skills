## Description: <br>
Connect to and explore PostgreSQL, MySQL, SQLite, MongoDB, and Redis databases by running queries, inspecting schemas, exporting data, and debugging database issues. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lrg913427-dot](https://clawhub.ai/user/lrg913427-dot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and data engineers use this skill to inspect schemas, run database queries, diagnose database health and performance, and export results across common database systems. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Database export, restore, migration, and full-table read examples can expose or alter sensitive data when used against production systems. <br>
Mitigation: Use least-privilege read-only credentials by default, require explicit approval for exports, restores, migrations, and full-table reads, and verify destination paths and rollback plans before execution. <br>
Risk: Large or unrestricted queries can read more data than intended or affect database performance. <br>
Mitigation: Limit result sets by default, confirm user intent before broad reads or exports, and review generated commands before running them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lrg913427-dot/db-explorer-lrg) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, markdown] <br>
**Output Format:** [Markdown with inline shell and SQL code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands may reference database connection environment variables such as DATABASE_URL, DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD, and DB_TYPE.] <br>

## Skill Version(s): <br>
3.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

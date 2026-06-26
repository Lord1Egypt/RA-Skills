## Description: <br>
Connect to and explore databases (PostgreSQL, MySQL, SQLite, MongoDB, Redis), run queries, inspect schemas, export data, and debug database issues. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lrg913427-dot](https://clawhub.ai/user/lrg913427-dot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to inspect database schemas, run limited read queries, export result sets, and perform database health or performance checks from terminal tools. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated database commands can modify, delete, restore, or migrate production data if run with elevated privileges. <br>
Mitigation: Use read-only or least-privilege credentials by default, require explicit approval for write, restore, import, and migration commands, and verify backups before administrative actions. <br>
Risk: Database exports and query results may expose sensitive or regulated data. <br>
Mitigation: Limit query results and exports, review generated queries before execution, and store exported files only in access-controlled paths. <br>
Risk: Connection strings and credentials can leak through shell history, logs, or shared output. <br>
Mitigation: Use environment variables or secure credential handling and avoid echoing passwords or connection strings into command history. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lrg913427-dot/db-explorer-tool) <br>
- [Publisher profile](https://clawhub.ai/user/lrg913427-dot) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline SQL and shell command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include database CLI commands, read-only query examples, schema summaries, export steps, and safety guidance.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata and artifact frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

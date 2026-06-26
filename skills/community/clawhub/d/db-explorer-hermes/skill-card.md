## Description: <br>
Connect to and explore databases (PostgreSQL, MySQL, SQLite, MongoDB, Redis), run queries, inspect schemas, export data, and debug database issues. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lrg913427-dot](https://clawhub.ai/user/lrg913427-dot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to inspect database schemas, run diagnostic queries, export query results, and perform database backup, restore, and migration tasks from terminal database clients. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Restore, import, write, or full export commands can overwrite, change, or expose real database data. <br>
Mitigation: Use read-only credentials where possible, require the agent to show the exact command and target database first, and require explicit approval before restore, import, write, or full export actions. <br>
Risk: Production or shared databases may be affected if the agent connects to the wrong target. <br>
Mitigation: Confirm the database type, host, database name, and environment before execution, especially for production systems. <br>


## Reference(s): <br>
- [Db Explorer ClawHub page](https://clawhub.ai/lrg913427-dot/db-explorer-hermes) <br>
- [lrg913427-dot publisher profile](https://clawhub.ai/user/lrg913427-dot) <br>
- [MongoDB Shell documentation](https://www.mongodb.com/docs/shell/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline SQL and shell command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include database client commands, schema summaries, query examples, export instructions, and safety confirmation prompts.] <br>

## Skill Version(s): <br>
2.4.0 (source: server release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

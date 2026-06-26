## Description: <br>
Python-based database connectivity skill supporting MySQL, PostgreSQL, Oracle, SQL Server, and SQLite. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jami-lin](https://clawhub.ai/user/jami-lin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to connect agents to relational databases, run parameterized SQL queries, inspect schemas, and manage transactions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can modify connected databases through UPDATE, DELETE, INSERT, and batch SQL execution. <br>
Mitigation: Use least-privileged or read-only database accounts by default and review every modifying statement or batch SQL file before running it. <br>
Risk: The agent may be connected to real databases that contain sensitive or production data. <br>
Mitigation: Avoid production credentials for exploration and only connect to databases the user intentionally authorizes. <br>
Risk: Connection metadata can persist in a temporary saved-connections file. <br>
Mitigation: Do not put passwords in JDBC URLs and clear the saved-connections file when connection metadata should not persist. <br>


## Reference(s): <br>
- [Connection management](references/connection-pooling.md) <br>
- [Query execution](references/query-execution.md) <br>
- [Supported databases](references/supported-databases.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline Python, SQL, YAML, and shell code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance may include executable database commands and configuration examples.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Description: <br>
Connect to and explore databases (PostgreSQL, MySQL, SQLite, MongoDB, Redis). Run queries, inspect schemas, export data. Use when user wants to query a database, explore schema, check data, export results, or debug database issues. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lrg913427-dot](https://clawhub.ai/user/lrg913427-dot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to inspect database schemas, run diagnostic queries, export result sets, and troubleshoot PostgreSQL, MySQL, SQLite, MongoDB, or Redis data stores. It guides an agent toward terminal-based database exploration with read-only defaults and explicit confirmation before higher-impact operations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Database restore, import, migration, or full export guidance can affect production data or expose sensitive records if run against the wrong target. <br>
Mitigation: Use read-only or least-privilege credentials by default, avoid production credentials unless necessary, and require explicit confirmation of the target database, source file, backup state, and expected impact before running these commands. <br>
Risk: Connection strings and database credentials may be exposed through shell history, logs, command output, or shared transcripts. <br>
Mitigation: Prefer environment variables or secret managers, avoid echoing passwords, and redact credentials before sharing command output. <br>
Risk: Large exports or unrestricted queries can create performance, availability, or data-handling issues. <br>
Mitigation: Limit query results by default, confirm full-table exports explicitly, and use the skill's read-only posture for exploratory work. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lrg913427-dot/db-explorer-lens) <br>
- [Publisher profile](https://clawhub.ai/user/lrg913427-dot) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline SQL and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce database connection, query, export, backup, restore, and migration command guidance; users should apply least-privilege credentials and confirm write-impacting commands.] <br>

## Skill Version(s): <br>
2.3.0 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

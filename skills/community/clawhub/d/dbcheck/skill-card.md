## Description:

DBCheck performs health inspections for MySQL, PostgreSQL, Oracle, SQL Server, DM8, TiDB, IvorySQL, GBase 8s, YashanDB, and KingbaseES databases and generates Word inspection reports with risk findings for DBAs and operations teams.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fiyo](https://clawhub.ai/user/fiyo)

### License/Terms of Use:

MIT

## Use Case:

DBAs, operations teams, and developers use this skill to run authorized database health checks, collect configuration and performance signals, and produce inspection reports for review and remediation planning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires database credentials and may optionally use SSH credentials for host resource collection.

Mitigation: Use least-privileged read-only database accounts, avoid passing passwords on the command line, and avoid SSH password authentication with unknown hosts.

Risk: Generated reports, history, and logs can expose sensitive database configuration, performance, and infrastructure details.

Mitigation: Store generated files in private locations, restrict sharing to authorized reviewers, and delete local artifacts when they are no longer needed.

Risk: The server security verdict flags the release as suspicious because credential handling and infrastructure exposure are broader than users may expect.

Mitigation: Review the security guidance before installation and keep any online AI integration disabled unless the destination and payload have been reviewed.

## Reference(s):

- [ClawHub DBCheck Skill Page](https://clawhub.ai/fiyo/skills/dbcheck)
- [DBCheck Project Repository](https://github.com/fiyo/DBCheck)
- [Oracle Instant Client Downloads](https://www.oracle.com/database/technologies/instant-client/winx64-64-downloads.html)
- [Microsoft ODBC Driver for SQL Server](https://learn.microsoft.com/zh-cn/sql/connect/odbc/download-odbc-driver-for-sql-server)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration instructions, Guidance, Files]

**Output Format:** [Markdown guidance with shell commands; bundled scripts generate local DOCX inspection reports.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated reports and history files may contain sensitive database and infrastructure details.]

## Skill Version(s):

2.6.2 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

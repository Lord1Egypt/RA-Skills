## Description:

DBQ is a multi-database SQL assistant for querying MySQL, PostgreSQL, SQLite, and MariaDB across dev, test, and prod environments with read-only defaults, DML/DDL gating, and EXPLAIN analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yinpengfei](https://clawhub.ai/user/yinpengfei)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to let an AI coding agent run database queries, inspect schemas, test connections, and perform gated SQL changes through preconfigured database aliases across dev, test, and prod environments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Production database access can expose or change sensitive live data.

Mitigation: Review before installing for prod and use least-privileged, read-only database accounts unless write access is explicitly required.

Risk: Credential exposure may occur through password retrieval commands or accessible local logs.

Mitigation: Do not use --keychain-get, restrict access to logs, and disable full SQL logging where sensitive queries may appear.

Risk: SQL safety controls can be weakened by confirmation bypasses or unsafe network paths.

Mitigation: Avoid DB_QUERY_ASSUME_YES for writes and require verified TLS or a trusted private network for remote databases.

## Reference(s):

- [README_EN.md](README_EN.md)
- [Database driver installation guide](references/drivers.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands; CLI results can be table, JSON, or CSV.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Database operations are executed through local shell commands and may create local query logs.]

## Skill Version(s):

1.4.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

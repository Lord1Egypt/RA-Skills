## Description:

Operate the local HiDataLinker desktop app to inspect saved MySQL, PostgreSQL, SQL Server, and Oracle connections with read-only queries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[henrybit](https://clawhub.ai/user/henrybit)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and database users use the skill to inspect saved database connections, discover schemas, review table structures, and run read-only queries through HiDataLinker.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review describes the release as benign but notes partial Skillspector coverage and asks users to consider the setup and launcher script.

Mitigation: Review the launcher and setup instructions before enabling the HiDataLinker MCP service.

## Reference(s):

- [HiDataLinker agent tools](artifact/references/tools.md)
- [DB Ops Client on ClawHub](https://clawhub.ai/henrybit/skills/db-ops-hidatalinker)

## Skill Output:

**Output Type(s):** [Text, Analysis, Guidance]

**Output Format:** [Markdown summaries with database query results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports read-only results; previews are limited to 1,000 rows and queries to 5,000 rows, with truncation noted.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

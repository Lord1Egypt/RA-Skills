## Description:

Guides an agent in using the clickhouse-client CLI to connect to ClickHouse databases, inspect schemas, run SELECT queries, perform data mutations, manage databases and tables, execute batch SQL, and format results as JSON.

This skill is ready for commercial/non-commercial use.

## Publisher:

[429668385](https://clawhub.ai/user/429668385)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, data engineers, and database operators use this skill to generate ClickHouse CLI commands and guidance for querying, schema inspection, import/export, troubleshooting, and controlled database administration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill enables an agent to propose live database mutations, DDL, imports, exports, and multiquery scripts against ClickHouse.

Mitigation: Use read-only, least-privilege credentials by default and require explicit approval before INSERT, UPDATE, DELETE, DDL, import, export, or --multiquery execution.

Risk: Database passwords or connection secrets may be exposed through command arguments, process listings, shell history, or logs.

Mitigation: Avoid passing passwords in command arguments; prefer protected environment variables or config files, restrict config permissions, and rotate credentials if process arguments may have been captured.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash, SQL, and XML code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May describe ClickHouse output formats such as TSV, CSV, JSON, and JSONEachRow.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

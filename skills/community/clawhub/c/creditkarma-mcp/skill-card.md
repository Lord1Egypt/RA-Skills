## Description:

Access Credit Karma transaction data through an MCP server for syncing, querying, and analyzing personal finance data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chrischall](https://clawhub.ai/user/chrischall)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and end users connect an agent to a local Credit Karma MCP server to sync transaction data, review account summaries, and analyze spending by category, merchant, date, or SQL query.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires Credit Karma session access and synced financial data may be exposed to the MCP server or related extension.

Mitigation: Install only after reviewing the package and extension, use a pinned audited version, and remove stored cookies and the local SQLite database when no longer needed.

Risk: Cookie headers or MCP environment configuration can leak account session access if committed or backed up.

Mitigation: Keep CK_COOKIES, .env files, and MCP configuration containing cookies out of source control and backups.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/chrischall/skills/creditkarma-mcp)
- [creditkarma-mcp npm Package](https://www.npmjs.com/package/creditkarma-mcp)
- [creditkarma-mcp Source Repository](https://github.com/chrischall/creditkarma-mcp)
- [fetchproxy Extension](https://github.com/chrischall/fetchproxy)
- [Credit Karma](https://www.creditkarma.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, SQL queries, Guidance]

**Output Format:** [Markdown with JSON, bash, and SQL code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include MCP tool names, configuration snippets, and read-only SQL examples for local transaction analysis.]

## Skill Version(s):

2.2.5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

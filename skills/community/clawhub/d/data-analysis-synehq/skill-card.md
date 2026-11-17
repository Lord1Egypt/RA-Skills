## Description:

Kole lets agents query connected databases with SQL, PostgreSQL commands, and natural language through SyneHQ's Kole platform.

This skill is ready for commercial/non-commercial use.

## Publisher:

[theboringhumane](https://clawhub.ai/user/theboringhumane)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and data teams use this skill to discover database connections and schemas, run SQL or natural-language queries, and produce data analysis through the SyneHQ Kole MCP server.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The MCP service can run SQL queries and DDL against connected databases with the configured credentials.

Mitigation: Use a dedicated read-only database user where possible, test on non-production data first, and require explicit confirmation before listing connections, inspecting schemas, running queries, or executing DDL.

Risk: Installing the MCP package with @latest can run unpinned external code in an environment that has database credentials.

Mitigation: Pin the MCP package version and review the package source before deployment.

Risk: The SyneHQ API key grants access to databases connected to the SyneHQ account.

Mitigation: Use a narrowly scoped SyneHQ API key, store it as a sensitive secret, and avoid committing it to version control.

## Reference(s):

- [Query Patterns Reference](artifact/references/query-patterns.md)
- [SyneHQ Kole MCP GitHub Repository](https://github.com/synehq/kole-mcp)
- [SyneHQ Kole MCP NPM Package](https://www.npmjs.com/package/@synehq/kole-mcp)
- [SyneHQ Documentation](https://docs.synehq.com)
- [ClawHub Skill Page](https://clawhub.ai/theboringhumane/skills/data-analysis-synehq)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with SQL, JavaScript tool-call examples, shell commands, and JSON configuration snippets.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a configured SyneHQ Kole MCP server and SyneHQ API key to execute database operations.]

## Skill Version(s):

1.1.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

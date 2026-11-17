## Description:

Connects agents to the Baselight MCP server to discover datasets and run live SQL queries across 50+ structured data sources.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pjsousa79](https://clawhub.ai/user/pjsousa79)

### License/Terms of Use:


## Use Case:

Developers, analysts, and agent users use this skill to connect an AI tool or IDE to Baselight, discover relevant datasets, inspect schemas, and run live SQL queries with assumptions and SQL included in the response.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill connects agents to an external Baselight MCP data service and may require OAuth or API-key credentials.

Mitigation: Review Baselight account, OAuth, API-key, billing, privacy, and query-limit terms before use, especially for sensitive questions or data.

Risk: Query results can depend on dataset freshness, schema changes, query scope, and service limits.

Mitigation: Discover datasets first, inspect schemas, query iteratively, include the SQL used, explain assumptions, and narrow slow queries with smaller scope or LIMIT clauses.

## Reference(s):

- [Baselight MCP connection documentation](https://baselight.ai/docs/connecting-to-the-baselight-mcp-server/)
- [Baselight app](https://baselight.app)
- [ClawHub skill page](https://clawhub.ai/pjsousa79/skills/baselight-mcp)

## Skill Output:

**Output Type(s):** [text, markdown, SQL, configuration, guidance]

**Output Format:** [Markdown with SQL snippets and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses should include discovered data context, SQL used for queries, results, and stated assumptions when applicable.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

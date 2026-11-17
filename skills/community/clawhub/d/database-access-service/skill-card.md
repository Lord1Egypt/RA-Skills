## Description:

Provides database table listing, schema lookup, and SQL query access through the XiaoBenYang MCP service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cainingnk](https://clawhub.ai/user/cainingnk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and data-support agents use this skill to inspect database tables and schemas and to run SQL queries through a configured XiaoBenYang API key.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Raw SQL execution can expose sensitive data or perform unintended database operations if the remote service permissions are broad.

Mitigation: Use least-privilege API and database credentials, restrict backend permissions, and review SQL before execution.

Risk: The API key is stored in a local .env file.

Mitigation: Keep .env out of source control and shared directories, and rotate the key if exposure is suspected.

Risk: The skill depends on a third-party remote MCP service.

Mitigation: Install only when the publisher and remote service are trusted, and limit shared data to the intended database access scope.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cainingnk/skills/database-access-service)
- [XiaoBenYang service](https://xiaobenyang.com)
- [XiaoBenYang MCP API endpoint](https://mcp.xiaobenyang.com)

## Skill Output:

**Output Type(s):** [JSON, Text]

**Output Format:** [JSON results summarized for the user in Markdown or plain text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a XiaoBenYang API key; database results depend on the remote service and its configured permissions.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

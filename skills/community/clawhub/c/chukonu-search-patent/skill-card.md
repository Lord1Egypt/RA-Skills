## Description:

Searches China CNIPA and Europe EPO patent records through the Chukonu remote MCP server, with read-only OAuth access, fielded patent queries, pagination, and retrieval of bibliographic records, claims, and descriptions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stevenybw](https://clawhub.ai/user/stevenybw)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and patent-search agents use this skill to connect OpenClaw to the Chukonu MCP service, search CNIPA and EPO patent datasets, apply structured filters, and retrieve individual patent records or claims.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires OAuth authentication with the Chukonu remote MCP service and sends patent search queries to that external provider.

Mitigation: Confirm the provider is acceptable for the intended patent-search workload before installation or use.

Risk: External service quota limits or temporary availability issues can interrupt long patent-search runs.

Mitigation: Check usage before extended searches, respect quota responses, and retry later when the service reports upstream unavailability.

## Reference(s):

- [Chukonu MCP server](https://search.houdutech.cn/mcp/)
- [ClawHub skill page](https://clawhub.ai/stevenybw/skills/chukonu-search-patent)
- [Publisher profile](https://clawhub.ai/user/stevenybw)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands, tool-call examples, and patent search result summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only MCP workflow; OAuth login is required and result pagination is enforced.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

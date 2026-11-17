## Description:

Automate 2chat tasks via Rube MCP (Composio). Always search tools first for current schemas.

This skill is ready for commercial/non-commercial use.

## Publisher:

[eohmig](https://clawhub.ai/user/eohmig)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to discover current 2chat tools through Rube MCP, verify an active 2chat connection, and execute schema-compliant 2chat workflows through Composio.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide an agent toward live messaging, contact updates, or bulk 2chat workflows.

Mitigation: Use it only with the intended 2chat account and confirm write, messaging, contact-change, or bulk actions before execution.

Risk: 2chat tool schemas and slugs may change over time.

Mitigation: Call RUBE_SEARCH_TOOLS before execution and review the discovered schema to understand what data may be read or changed.

## Reference(s):

- [Composio 2chat Toolkit](https://composio.dev/toolkits/_2chat)
- [Rube MCP Server](https://rube.app/mcp)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline MCP tool calls and examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Rube MCP server and an active 2chat connection before executing workflows.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

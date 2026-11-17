## Description:

Connect AI agents to BytesAgain skill search via MCP SSE. Shows setup commands for OpenClaw, Claude Desktop, and curl. No files modified.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bytesagain-lab](https://clawhub.ai/user/bytesagain-lab)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to configure MCP-compatible clients for BytesAgain skill search and to check available BytesAgain MCP tools.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Commands that test, list tools, or search contact bytesagain.com; search sends the query text provided by the user.

Mitigation: Run network commands only when outbound access to bytesagain.com is acceptable, and avoid sending sensitive or private query text.

Risk: Adding a third-party MCP server changes the tools available to the agent.

Mitigation: Review the BytesAgain MCP tools and install the server only in agent environments where third-party tool access is approved.

## Reference(s):

- [BytesAgain MCP documentation](https://bytesagain.com/mcp)
- [ClawHub skill page](https://clawhub.ai/bytesagain-lab/skills/bytesagain-mcp)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and plain text with shell commands and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Network-check commands may call bytesagain.com and search commands send the query text provided by the user.]

## Skill Version(s):

1.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

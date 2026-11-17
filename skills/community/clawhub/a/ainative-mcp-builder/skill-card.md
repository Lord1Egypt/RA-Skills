## Description:

Build and publish custom MCP servers on AINative using Python FastMCP or the Node.js MCP SDK, including tool creation, agent configuration, and npm publishing guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[urbantech](https://clawhub.ai/user/urbantech)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to create MCP servers, add tools, configure them for agents such as Claude Code or Cursor, and publish packages for reuse.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Example MCP configurations and source snippets involve AINATIVE_API_KEY handling.

Mitigation: Use environment variables or a secret manager, avoid committing real keys in .claude/mcp.json or source files, and rotate any credential that was exposed.

Risk: The memory examples can store or recall remote agent memory.

Mitigation: Store confidential prompts, credentials, private user data, or sensitive business context only when that storage is deliberate, authorized, and covered by the deployment's data policy.

Risk: Generated MCP server examples depend on Python or Node.js packages that may change over time.

Mitigation: Pin dependency versions for production releases and review dependency security before publishing or deploying an MCP server.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/urbantech/skills/ainative-mcp-builder)
- [Model Context Protocol documentation](https://modelcontextprotocol.io)
- [AINative API base URL](https://api.ainative.studio)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with inline Python, TypeScript, JSON, and shell code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance includes example API calls and MCP configuration snippets; users should replace placeholder credentials with environment-managed secrets.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

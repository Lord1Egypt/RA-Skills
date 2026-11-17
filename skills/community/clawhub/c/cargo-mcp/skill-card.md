## Description:

Uses Cargo from Claude Desktop, ChatGPT or any MCP client through the hosted server at https://mcp.getcargo.io/mcp, with nothing to install: connects a client, prices and runs an action on one record or a batch, checks its status, and reads workspace data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cargo-ai](https://clawhub.ai/user/cargo-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers using Claude Desktop, ChatGPT, Cursor, or another MCP client use this skill to connect to Cargo's hosted server, discover and price actions, run actions on one or more records, check runs, and read workspace data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The OpenClaw setup requires local software even though the skill advertises hosted access with nothing to install.

Mitigation: For hosted-only use, connect directly to the MCP endpoint and avoid installing the CLI unless choosing CLI functionality. Use narrowly scoped credentials, confirm the workspace, and approve costs and effects, including those of an initial 10–20-record sample.

## Reference(s):

- [Cargo hosted MCP endpoint](https://mcp.getcargo.io/mcp)
- [Cargo MCP skill on ClawHub](https://clawhub.ai/cargo-ai/skills/cargo-mcp)
- [Cargo Skills homepage](https://github.com/getcargohq/cargo-skills)

## Skill Output:

**Output Type(s):** [Guidance, API calls, Configuration, Shell commands]

**Output Format:** [Markdown guidance with JSON configuration and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Single-stream responses; access to the hosted Cargo MCP server is required.]

## Skill Version(s):

1.3.1 (source: frontmatter; release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

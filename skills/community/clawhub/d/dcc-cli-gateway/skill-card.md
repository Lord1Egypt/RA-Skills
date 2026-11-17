## Description:

Operate named supported applications through DCC-MCP, discover tools and marketplace skills, and support explicit DCC-MCP or DCC-CUA requests.

This skill is ready for commercial/non-commercial use.

## Publisher:

[loonghao](https://clawhub.ai/user/loonghao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and creative professionals use the skill to discover and operate supported creative and productivity applications through DCC-MCP, then inspect the resulting scene, document, or artifact. It also guides explicit DCC-CUA application UI tasks with observation and readback requirements.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A fallback helper may repeat a project edit after a timeout, potentially applying a change twice.

Mitigation: Use a version that stops after an uncertain mutating call instead of retrying through REST. Until then, avoid the Python gateway helper for important edits and keep project backups.

## Reference(s):

- [DCC-MCP skill documentation](https://github.com/dcc-mcp/dcc-mcp-agent-plugins/blob/main/plugins/dcc-mcp/skills/dcc-mcp/SKILL.md)
- [DCC-MCP production reuse gate](https://github.com/dcc-mcp/dcc-mcp-core/blob/main/crates/dcc-mcp-gateway/src/gateway/native_resources/agent_workflows.md#production-reuse-gate)

## Skill Output:

**Output Type(s):** [Guidance, API calls, Shell commands, Files]

**Output Format:** [Structured DCC-MCP tool calls with text or Markdown guidance and application-specific files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Application-specific output depends on the selected app and task.]

## Skill Version(s):

0.19.117 (source: server-resolved release evidence; skill frontmatter metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

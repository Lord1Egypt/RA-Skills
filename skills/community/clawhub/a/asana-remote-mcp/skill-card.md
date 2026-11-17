## Description:

Use Asana through mcporter-backed remote MCP tools for tasks, projects, portfolios, goals, and team workspaces via the hosted mcp.asana.com server.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dam1k](https://clawhub.ai/user/dam1k)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, external users, and developers use this skill to let an agent search Asana workspaces, inspect projects and tasks, and create or update Asana work items through an OAuth-scoped MCP connection.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read Asana work data and perform requested updates through the connected account.

Mitigation: Install only when agent access to the connected Asana account is intended, and review confirmations before task creation, movement, completion, or other significant updates.

Risk: Incorrect task or project identifiers could target the wrong Asana object.

Mitigation: Resolve workspace, project, and task GIDs before detail or update calls, and fetch current task details before changing fields.

Risk: Large or overly broad list operations can consume Asana API quota.

Mitigation: Use opt_fields to limit returned data and avoid unnecessarily large list operations.

## Reference(s):

- [Asana MCP server](https://mcp.asana.com/v2/mcp)
- [ClawHub skill page](https://clawhub.ai/dam1k/skills/asana-remote-mcp)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, API Calls, Configuration]

**Output Format:** [Markdown with inline commands and MCP tool-call guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses OAuth-scoped Asana MCP access; significant task changes should be confirmed before execution.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

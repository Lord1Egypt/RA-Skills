## Description:

Manage projects and tasks with the Flower project management API via MCP. Use when creating, updating, or searching tasks/tickets, managing projects and columns, or integrating with Flower/Kanban boards. Requires @xferops/flower-mcp and a Flower API token.

This skill is ready for commercial/non-commercial use.

## Publisher:

[parker-xferops](https://clawhub.ai/user/parker-xferops)

### License/Terms of Use:


## Use Case:

Developers and project teams use this skill to manage Flower projects, columns, tasks, comments, users, team membership, and notification preferences from an MCP-enabled agent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The MCP server is installed through an unpinned npm package while using a Flower API token.

Mitigation: Pin and review the MCP package version before installation, and use a narrowly scoped Flower token.

Risk: The skill exposes live delete, member-management, and bulk update operations.

Mitigation: Require explicit confirmation before delete, remove-member, or bulk update operations.

Risk: Unrelated environment secrets could be exposed to the MCP process.

Mitigation: Limit the MCP environment to the Flower URL and narrowly scoped Flower token required by this integration.

## Reference(s):

- [Flower service URL](https://flower.xferops.com)
- [ClawHub skill page](https://clawhub.ai/parker-xferops/skills/flower)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include proposed Flower MCP actions that should be confirmed before destructive or membership-changing operations.]

## Skill Version(s):

1.0.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

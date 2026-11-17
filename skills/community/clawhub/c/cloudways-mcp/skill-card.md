## Description:

Operational guide for managing Cloudways servers and applications across one or more Cloudways accounts through the official Cloudways MCP server, with confirmation rules for write and destructive operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[benkalsky](https://clawhub.ai/user/benkalsky)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, site operators, and agency teams use this skill to connect to Cloudways MCP, inspect Cloudways servers and applications, run monitoring and audit workflows, and perform guarded maintenance tasks. It emphasizes account selection, least-privilege tokens, and explicit confirmation before write or destructive actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cloudways tokens can grant broad or full administrative access to production infrastructure.

Mitigation: Use the minimum token role needed, prefer READ for audits and monitoring, and treat FULL ACCESS tokens as production admin credentials.

Risk: Write or destructive Cloudways operations can interrupt services, overwrite data, remove resources, or change billing and access.

Mitigation: Review every write confirmation carefully, confirm the target account and resource, and use double confirmation for destructive actions.

Risk: Raw Cloudways API or MCP responses may expose credentials or sensitive operational data.

Mitigation: Avoid pasting raw responses into chats, logs, tickets, or automation stores; summarize only the fields needed for the task.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/benkalsky/skills/cloudways-mcp)
- [Cloudways MCP installation guide](https://support.cloudways.com/en/articles/14654372-how-to-use-cloudways-mcp-server-for-ai-based-server-management)
- [Cloudways MCP server tools](https://support.cloudways.com/en/articles/15798823-cloudways-mcp-server-tools)
- [Cloudways MCP v1.2 announcement](https://www.cloudways.com/blog/cloudways-mcp-v1-2-112-new-tools-role-based-access-tokens-and-full-cloudways-api-coverage/)
- [Cloudways API v2 announcement](https://www.cloudways.com/blog/introducing-cloudways-api-v2/)
- [Installation reference](references/installation.md)
- [Tools catalog](references/tools-catalog.md)
- [Monitoring workflows](references/workflows-monitoring.md)
- [Maintenance workflows](references/workflows-maintenance.md)
- [Onboarding workflows](references/workflows-onboarding.md)
- [Automation workflows](references/workflows-automation.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration, API calls]

**Output Format:** [Markdown guidance with inline shell commands, MCP tool names, workflow steps, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include operational recommendations and proposed Cloudways MCP calls; write and destructive actions require explicit user confirmation.]

## Skill Version(s):

1.5.3 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

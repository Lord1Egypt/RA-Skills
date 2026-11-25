## Description:

Provides operational guidance for managing Cloudways servers and applications through Cloudways' hosted MCP server.

This skill is ready for commercial/non-commercial use.

## Publisher:

[benkalsky](https://clawhub.ai/user/benkalsky)

### License/Terms of Use:

MIT

## Use Case:

Cloudways administrators and client operators use this skill to connect an agent to Cloudways and monitor, audit, and maintain servers and applications across accounts. It covers read-only checks and guided write workflows that require confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan reports an undisclosed Slack reporting destination and calls out webhook-triggered backups for review.

Mitigation: Review report destinations and webhook-triggered backup behavior before enabling automation.

Risk: ClawScan reports unsafe automation examples and advises reviewing how credentials are entered in commands.

Mitigation: Inspect credential handling in commands and automation before running them; follow the skill's token-handling guidance.

Risk: Two referenced files were only partially inspected, so the scan does not establish that the remaining content is safe.

Mitigation: Review the reporting and automation instructions, including the uninspected portions, before installation or use.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/benkalsky/skills/cloudways-mcp)
- [Cloudways MCP setup guide](https://support.cloudways.com/en/articles/14654372-how-to-use-cloudways-mcp-server-for-ai-based-server-management)
- [Cloudways MCP tools reference](https://support.cloudways.com/en/articles/15798823-cloudways-mcp-server-tools)
- [Cloudways API documentation](https://developers.cloudways.com/docs/)
- [Installation](references/installation.md)
- [Tools catalog](references/tools-catalog.md)
- [Monitoring workflows](references/workflows-monitoring.md)
- [Maintenance workflows](references/workflows-maintenance.md)
- [Onboarding workflows](references/workflows-onboarding.md)
- [Automation workflows](references/workflows-automation.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration, API calls]

**Output Format:** [Markdown guidance with tool calls, shell snippets, and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.5.4 (source: SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

Helps an agent administer DocsBot teams, bots, sources, members, integrations, Skills, and reporting through an OAuth-authenticated MCP server.

This skill is ready for commercial/non-commercial use.

## Publisher:

[uglyrobot](https://clawhub.ai/user/uglyrobot)

### License/Terms of Use:

MIT-0

## Use Case:

DocsBot account owners and administrators use this skill to inspect account and bot state, manage teams and sources, configure bots and integrations, review reporting, and diagnose response quality through approved tools.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The agent may read account, bot, and log data or change account resources.

Mitigation: Authorize a least-privileged DocsBot account where possible and review tool approvals.

Risk: Deletions, member changes, webhooks, external connectors, or public auto-replies may have significant effects.

Mitigation: Confirm the exact target and intended effect before high-impact changes.

Risk: OAuth credentials or other secrets could be disclosed in conversation.

Mitigation: Use the client's OAuth flow and do not paste tokens or long-lived secrets into chat.

## Reference(s):

- [DocsBot skill release](https://clawhub.ai/uglyrobot/skills/docsbot-administration)
- [DocsBot MCP server](https://mcp.docsbot.ai)
- [MCP server guide](artifact/references/mcp-server.md)
- [MCP client configuration](artifact/references/mcp-client-config.md)
- [Bot-building workflow](artifact/references/bot-builder/SKILL.md)
- [Response-quality workflow](artifact/references/response-quality/SKILL.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Configuration guidance, Shell commands]

**Output Format:** [Markdown with configuration examples and command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an MCP-compatible client, a DocsBot account, and browser-based OAuth authorization.]

## Skill Version(s):

0.6.3 (source: ClawHub release and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

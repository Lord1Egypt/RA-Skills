## Description:

Manage FlowyTeam projects, tasks, OKRs, KPIs, HR, CRM, finance, support tickets, attendance, and related workspace records through MCP.

This skill is ready for commercial/non-commercial use.

## Publisher:

[flowy-team](https://clawhub.ai/user/flowy-team)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and workspace operators use this skill to connect an MCP-compatible agent to FlowyTeam so the agent can read and manage projects, tasks, OKRs, KPIs, HR records, CRM records, finance records, support tickets, attendance, and other workspace data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can operate on broad FlowyTeam workspace data according to the permissions attached to the user's token.

Mitigation: Use the lowest-privilege token possible and avoid admin tokens unless an admin-only action is explicitly required.

Risk: Create, update, or delete actions can change tasks, HR data, CRM records, finance records, support tickets, and other business records.

Mitigation: Require explicit user confirmation in the current turn before any POST, PUT, or DELETE action.

Risk: A leaked API token could expose the connected FlowyTeam workspace.

Mitigation: Keep tokens out of shared chats and repositories, and prefer the API-token flow over password-based login.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/flowy-team/skills/flowyteam-mcp)
- [FlowyTeam Website](https://flowyteam.com)
- [FlowyTeam MCP Docs](https://flowyteam.com/get/mcp-server)
- [FlowyTeam API Reference](https://flowyteam.com/get/mcp-docs)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, API calls]

**Output Format:** [Markdown guidance with JSON configuration snippets, shell commands, and MCP API calls]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a FlowyTeam API token for authenticated workspace tools.]

## Skill Version(s):

1.1.8 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

Control application UIs through project-owned DCC-CUA for explicit DCC-CUA requests, including browsers, non-DCC apps, and DCC-MCP UI fallback.

This skill is ready for commercial/non-commercial use.

## Publisher:

[loonghao](https://clawhub.ai/user/loonghao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use DCC-CUA to control browser and desktop application interfaces through a project-owned route, binding the intended target and verifying resulting state changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A browser or application session may expose sensitive account content or reach consequential actions.

Mitigation: Review the separate companion runtime before installation, limit sessions to the intended window and browser tab, approve profile attachment deliberately, and handle sign-ins, purchases, and account changes yourself.

## Reference(s):

- [Skill documentation](https://github.com/dcc-mcp/dcc-mcp-agent-plugins/blob/main/plugins/dcc-mcp/skills/dcc-cua/SKILL.md)
- [DCC host commands](artifact/references/DCC_HOST.md)
- [Continuity and evidence epochs](artifact/references/CONTINUITY.md)
- [Browser and desktop binding](artifact/references/BROWSER_AND_DESKTOP.md)
- [Scoped window recovery workflow](https://github.com/dcc-mcp/dcc-mcp-agent-plugins/blob/main/plugins/dcc-mcp/skills/dcc-mcp/references/UI_WORKFLOWS.md#scoped-window-recovery)
- [Owned pixels and secondary popup workflow](https://github.com/dcc-mcp/dcc-mcp-agent-plugins/blob/main/plugins/dcc-mcp/skills/dcc-mcp/references/UI_WORKFLOWS.md#owned-pixels-and-secondary-popup-observations)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, UI control actions]

**Output Format:** [Markdown guidance with shell command examples and structured UI control actions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Target-bound, session-scoped interactions with state verification.]

## Skill Version(s):

0.19.117 (source: server-resolved release metadata; skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

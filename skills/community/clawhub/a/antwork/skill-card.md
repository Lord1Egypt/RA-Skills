## Description:

Helps agents draft, schedule, and publish social media posts through Antwork while matching account voice and platform limits.

This skill is ready for commercial/non-commercial use.

## Publisher:

[iker-gonzalez](https://clawhub.ai/user/iker-gonzalez)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can use the skill to connect an Antwork workspace, prepare platform-specific social posts or campaigns, publish or schedule them, and review engagement data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Publishing, scheduling, and media uploads can act on connected accounts and send content to Antwork.

Mitigation: Review OAuth permissions and confirm the intended workspace, accounts, and media before acting; confirm before deleting posts or media.

Risk: The supplied security review covers the skill instructions, not Antwork's remote service implementation.

Mitigation: Use the service's OAuth flow and review the permissions and destination shown during account connection.

## Reference(s):

- [Antwork MCP documentation](https://antwork.io/docs/mcp)
- [Antwork skills](https://antwork.io/skills)
- [ClawHub skill release](https://clawhub.ai/iker-gonzalez/skills/antwork)
- [Publisher profile](https://clawhub.ai/user/iker-gonzalez)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, API Calls, Shell commands, Configuration instructions]

**Output Format:** [Markdown and plain text, including social post drafts and tabular analytics summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Platform-specific copy and actions for one or more connected social accounts]

## Skill Version(s):

1.0.2 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

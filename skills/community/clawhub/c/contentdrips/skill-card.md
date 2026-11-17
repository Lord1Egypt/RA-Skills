## Description:

Connect OpenClaw to ContentDrips MCP for social media design and publishing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[usama-gh](https://clawhub.ai/user/usama-gh)

### License/Terms of Use:

MIT-0

## Use Case:

Creators, social media teams, and developers use this skill to create ContentDrips graphics and carousels, manage posts, and publish or schedule approved content to connected LinkedIn and Instagram accounts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The ContentDrips API token and connected social accounts allow agents to prepare account-level actions such as creating, scheduling, publishing, or deleting content.

Mitigation: Install only for trusted ContentDrips accounts, review proposed account actions, and require explicit user confirmation before publishing, scheduling, deleting, or selecting a workspace/profile.

Risk: Ambiguous workspace or platform requests could send content to the wrong profile or social channel.

Mitigation: Fetch available profiles and social accounts first, ask the user to choose when multiple workspaces exist, and set publishing flags only for platforms the user explicitly names.

Risk: Generated graphics, carousels, or captions may contain inaccurate or unsuitable public-facing claims.

Mitigation: Review generated designs and captions in the ContentDrips editor before exporting, scheduling, or publishing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/usama-gh/skills/contentdrips)
- [ContentDrips](https://contentdrips.com)
- [ContentDrips app](https://app.contentdrips.com)
- [ContentDrips MCP endpoint](https://mcp.contentdrips.com/mcp)
- [ContentDrips social accounts](https://app.contentdrips.com/social-accounts)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include ContentDrips editor links, post links, MCP setup commands, platform-specific publishing confirmations, and example JSON payloads.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

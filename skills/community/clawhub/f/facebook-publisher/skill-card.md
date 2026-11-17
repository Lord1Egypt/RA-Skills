## Description:

Publish posts to Facebook Pages when the user wants to create text, photo, album, or video posts, schedule Facebook posts, or manage scheduled Facebook posts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[snoopyrain](https://clawhub.ai/user/snoopyrain)

### License/Terms of Use:

MIT-0

## Use Case:

External users and social media operators use this skill to publish and schedule Facebook Page posts through Boring after connecting a Facebook Page. It also helps agents list Facebook Pages and manage scheduled Facebook posts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The embedded MCP connector token grants authority to publish, upload media, schedule posts, and cancel scheduled posts for connected Facebook Pages.

Mitigation: Treat the MCP link like a password, verify the connected Page before use, and require explicit user confirmation of the exact post, media, schedule time, or cancellation target before taking action.

Risk: The security verdict is suspicious because public publishing actions may proceed without a required final confirmation.

Mitigation: Review proposed Facebook actions before execution and ask the user to confirm irreversible or public-facing changes.

## Reference(s):

- [ClawHub Facebook Publisher Skill](https://clawhub.ai/snoopyrain/skills/facebook-publisher)
- [Boring MCP Setup Documentation](https://boring-doc.aiagent-me.com/getting-started/mcp.html)
- [Boring Documentation](https://boring-doc.aiagent-me.com)

## Skill Output:

**Output Type(s):** [Guidance, API calls, Configuration]

**Output Format:** [Markdown instructions with tool-call examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Boring MCP connector link with an embedded authentication token.]

## Skill Version(s):

1.0.1 (source: server release evidence; artifact frontmatter lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

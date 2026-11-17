## Description:

Track Facebook Page reach, engagement, video views, and post-level analytics through a Boring MCP connector.

This skill is ready for commercial/non-commercial use.

## Publisher:

[snoopyrain](https://clawhub.ai/user/snoopyrain)

### License/Terms of Use:

MIT-0

## Use Case:

External users and social media operators use this skill to inspect connected Facebook Page performance, compare posts, and summarize trends from Boring-provided analytics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The MCP Connector URL contains an embedded authentication token that can grant access to Facebook analytics if exposed.

Mitigation: Keep the URL private, add it only in trusted connector settings, and revoke or regenerate it if shared or exposed.

Risk: The skill depends on a third-party remote service whose token enforcement and data handling are outside the artifact.

Mitigation: Install only if comfortable routing Facebook Page analytics through Boring and review the service's account connection and revocation controls before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/snoopyrain/skills/facebook-analytics)
- [Boring MCP connector documentation](https://boring-doc.aiagent-me.com/getting-started/mcp.html)
- [Boring API documentation](https://boring-doc.aiagent-me.com)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, guidance]

**Output Format:** [Markdown summaries, tables, and connector tool-call guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Boring MCP Connector URL with an embedded authentication token; analytics access is documented as read-only.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata; artifact frontmatter lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

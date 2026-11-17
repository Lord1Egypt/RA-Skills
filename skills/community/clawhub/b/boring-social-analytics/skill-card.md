## Description:

Track social media performance and analytics across Facebook, Instagram, Threads, YouTube, and TikTok using Boring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[snoopyrain](https://clawhub.ai/user/snoopyrain)

### License/Terms of Use:

MIT-0

## Use Case:

External users and social media operators use this skill to query connected social accounts, compare platform performance, review post metrics, and summarize publishing history through Boring.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The Boring MCP Connector URL contains an embedded authentication token and can grant access to connected social analytics.

Mitigation: Treat the connector URL like a password, avoid sharing it publicly, and regenerate it if exposed.

Risk: Connected social accounts may contain sensitive performance and audience data.

Mitigation: Review connected platform permissions and only connect accounts whose analytics may be queried through Boring.

## Reference(s):

- [Boring MCP setup documentation](https://boring-doc.aiagent-me.com/getting-started/mcp.html)
- [Boring documentation](https://boring-doc.aiagent-me.com)
- [Boring account and connector setup](https://boring.aiagent-me.com)
- [ClawHub skill page](https://clawhub.ai/snoopyrain/skills/boring-social-analytics)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, configuration]

**Output Format:** [Markdown guidance with tool-call examples and summary tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Boring MCP Connector URL with an embedded authentication token.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

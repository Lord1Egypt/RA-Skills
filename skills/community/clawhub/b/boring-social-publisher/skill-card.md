## Description:

Publishes social media posts to Facebook, Instagram, Threads, YouTube, TikTok, and X through Boring from one agent workflow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[snoopyrain](https://clawhub.ai/user/snoopyrain)

### License/Terms of Use:

MIT-0

## Use Case:

External users and social media operators use this skill to prepare, adapt, publish, schedule, and report on posts across connected Boring social accounts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The MCP Connector URL contains an embedded authentication token.

Mitigation: Treat the MCP URL as a password, avoid sharing it publicly, and regenerate or revoke access from the Boring dashboard if it is exposed.

Risk: The skill can publish public content through connected social media accounts.

Mitigation: Review selected accounts, platforms, adapted text, media, and schedule before publishing.

Risk: Uploaded media and post content are processed by Boring and sent to connected social platform APIs.

Mitigation: Install only if you trust Boring with the content and media being published, and disconnect accounts when access is no longer needed.

## Reference(s):

- [Boring MCP Setup Documentation](https://boring-doc.aiagent-me.com/getting-started/mcp.html)
- [Boring API Documentation](https://boring-doc.aiagent-me.com)
- [ClawHub Skill Page](https://clawhub.ai/snoopyrain/skills/boring-social-publisher)

## Skill Output:

**Output Type(s):** [API Calls, Guidance, Markdown]

**Output Format:** [Markdown summaries with connector tool calls and publishing status details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include account summaries, adapted post text, media URLs, scheduled times, post IDs, and failure reasons.]

## Skill Version(s):

1.0.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

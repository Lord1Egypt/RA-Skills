## Description:

Publish social media posts to multiple platforms at once.

This skill is ready for commercial/non-commercial use.

## Publisher:

[snoopyrain](https://clawhub.ai/user/snoopyrain)

### License/Terms of Use:

MIT-0

## Use Case:

External users and teams use this skill to prepare, adapt, publish, and schedule social media posts across connected Facebook, Instagram, Threads, YouTube, TikTok, and X accounts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The MCP connector link acts as a posting credential for connected social accounts.

Mitigation: Keep the connector link private, review connected accounts before publishing, and revoke or regenerate the token if it is exposed or no longer needed.

Risk: The skill can publish or schedule content on connected accounts.

Mitigation: Confirm content, target platforms, media requirements, and schedule before making publishing calls.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/snoopyrain/skills/boring-social-media-publisher)
- [Boring MCP setup documentation](https://boring-doc.aiagent-me.com/getting-started/mcp.html)
- [Boring API documentation](https://boring-doc.aiagent-me.com)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, guidance]

**Output Format:** [Markdown summaries with structured tool-call guidance and publishing status reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include platform-specific adaptations, scheduled publish times, post IDs, and failure reasons.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

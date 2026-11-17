## Description:

Publish videos and photo carousels to TikTok using Boring, including privacy settings and draft mode.

This skill is ready for commercial/non-commercial use.

## Publisher:

[snoopyrain](https://clawhub.ai/user/snoopyrain)

### License/Terms of Use:

MIT-0

## Use Case:

External users and creators use this skill to publish user-provided videos or photo carousels to TikTok through Boring, including upload preparation, privacy selection, draft review, and publish status reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The MCP connector URL contains an embedded authentication token.

Mitigation: Treat the connector URL as a password and rotate it if exposed.

Risk: Media and TikTok account actions pass through Boring before reaching TikTok.

Mitigation: Install only if you trust Boring with the TikTok account and media being published.

Risk: Content may be published publicly or to the wrong TikTok account if settings are not reviewed.

Mitigation: Confirm the account, media, caption, and privacy before publishing; use draft mode or SELF_ONLY for sensitive content.

## Reference(s):

- [Boring MCP setup documentation](https://boring-doc.aiagent-me.com/getting-started/mcp.html)
- [Boring documentation](https://boring-doc.aiagent-me.com)
- [Boring web app](https://boring.aiagent-me.com)

## Skill Output:

**Output Type(s):** [guidance, API calls, configuration, text]

**Output Format:** [Markdown guidance with MCP tool-call examples and status summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include account identifiers, uploaded media URLs, post IDs, success status, privacy settings, and draft-mode instructions.]

## Skill Version(s):

1.0.1 (source: server release evidence; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

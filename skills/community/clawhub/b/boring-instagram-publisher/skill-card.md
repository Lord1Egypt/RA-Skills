## Description:

Publish posts to Instagram using Boring for photos, carousels, Reels, and scheduled Instagram posts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[snoopyrain](https://clawhub.ai/user/snoopyrain)

### License/Terms of Use:

MIT-0

## Use Case:

External users and creators use this skill to publish or schedule Instagram Business or Creator account content through Boring's MCP connector. It helps an agent collect account, caption, media, and schedule details before calling the publishing tools.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The MCP connector URL contains an embedded authentication token that can grant access to Boring-backed Instagram publishing actions.

Mitigation: Keep the connector URL private, treat it like a password, and regenerate it if it is exposed.

Risk: Captions and media are sent to Boring and then to Instagram for publishing or scheduling on the user's behalf.

Mitigation: Install only if the user trusts Boring with Instagram publishing access and the provided media and captions.

Risk: The skill can create public Instagram content or scheduled posts through the connected account.

Mitigation: Review account selection, media, captions, and schedule details before publishing or scheduling.

## Reference(s):

- [Boring MCP setup documentation](https://boring-doc.aiagent-me.com/getting-started/mcp.html)
- [Boring documentation](https://boring-doc.aiagent-me.com)
- [ClawHub skill page](https://clawhub.ai/snoopyrain/skills/boring-instagram-publisher)

## Skill Output:

**Output Type(s):** [guidance, API calls, text]

**Output Format:** [Markdown guidance with MCP tool calls and confirmation text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May upload or re-host media files before publishing or scheduling Instagram content.]

## Skill Version(s):

1.0.3 (source: server release metadata; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

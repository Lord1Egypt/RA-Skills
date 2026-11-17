## Description:

Publish text, photo, album, or video posts to Facebook Pages through Boring, including immediate publishing, scheduling, and scheduled-post management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[snoopyrain](https://clawhub.ai/user/snoopyrain)

### License/Terms of Use:

MIT-0

## Use Case:

External users and social media operators use this skill to publish, schedule, view, and cancel Facebook Page posts through Boring after connecting a Facebook Page and providing the MCP connector link.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The MCP connector URL contains an embedded authentication token.

Mitigation: Treat the connector URL like a password, avoid sharing it publicly, and regenerate it if exposure is suspected.

Risk: The connector can publish public Facebook Page content and cancel scheduled posts on connected Pages.

Mitigation: Review the target Page, post text, media, and scheduled time before approving publishing or cancellation actions.

Risk: Media files or URLs may be uploaded to Boring storage and sent to Facebook for publishing.

Mitigation: Confirm media ownership, sensitivity, and intended audience before uploading or publishing media.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/snoopyrain/skills/boring-facebook-publisher)
- [Boring MCP Setup Documentation](https://boring-doc.aiagent-me.com/getting-started/mcp.html)
- [Boring Documentation](https://boring-doc.aiagent-me.com)

## Skill Output:

**Output Type(s):** [Guidance, API Calls, Text]

**Output Format:** [Markdown guidance with MCP tool-call parameters and plain-text user confirmations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Facebook account IDs, media URLs, post IDs, scheduled times, and confirmation text.]

## Skill Version(s):

1.0.4 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

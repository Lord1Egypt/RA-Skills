## Description:

Publish posts and threads to Threads (by Meta) using Boring, including text posts, media posts, carousels, replies, scheduled posts, and multi-post threads.

This skill is ready for commercial/non-commercial use.

## Publisher:

[snoopyrain](https://clawhub.ai/user/snoopyrain)

### License/Terms of Use:

MIT-0

## Use Case:

External users and social media operators use this skill to publish, schedule, and reply to Threads content through Boring. It supports text posts, media posts, carousels, and multi-post threads while guiding account selection, media preparation, and error handling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The MCP Connector URL contains an embedded authentication token and can authorize publishing actions if exposed.

Mitigation: Keep the connector URL private, treat it like a password, and regenerate it if it may have been shared.

Risk: The skill can publish or schedule public Threads content and upload selected media through Boring.

Mitigation: Review the selected account, media, scheduled time, and final post text before publishing.

Risk: Local files or URLs may be uploaded to Boring-hosted storage so Threads can access the media.

Mitigation: Only provide media intended for publication and avoid sensitive or private files.

## Reference(s):

- [Boring MCP Connector documentation](https://boring-doc.aiagent-me.com/getting-started/mcp.html)
- [Boring documentation](https://boring-doc.aiagent-me.com)
- [ClawHub skill page](https://clawhub.ai/snoopyrain/skills/boring-threads-publisher)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, guidance]

**Output Format:** [Markdown guidance with connector tool calls and publishing status summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Threads post IDs, thread URLs, scheduling timestamps, media upload guidance, and error summaries.]

## Skill Version(s):

1.0.3 (source: server release metadata; artifact frontmatter lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

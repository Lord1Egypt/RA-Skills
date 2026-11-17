## Description:

Upload videos and Shorts to YouTube using Boring with support for titles, descriptions, tags, thumbnails, and captions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[snoopyrain](https://clawhub.ai/user/snoopyrain)

### License/Terms of Use:

MIT-0

## Use Case:

External users and creators use this skill to upload videos or Shorts to a connected YouTube channel through Boring, including metadata, thumbnails, and captions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The MCP connector URL contains an embedded authentication token.

Mitigation: Treat the connector URL like a password, avoid sharing it in chats or public places, and rotate or revoke it if exposed.

Risk: The skill can publish YouTube videos publicly without an explicit confirmation step in the instructions.

Mitigation: Manually confirm the target account, media, title, description, captions, and visibility before calling the publish tool.

Risk: Video files, thumbnails, captions, and post metadata are sent through Boring and YouTube services.

Mitigation: Use only media the user intends to upload, avoid sensitive unpublished content unless approved, and confirm the connected account before upload.

## Reference(s):

- [Boring MCP Setup](https://boring-doc.aiagent-me.com/getting-started/mcp.html)
- [Boring Documentation](https://boring-doc.aiagent-me.com)
- [ClawHub Skill Page](https://clawhub.ai/snoopyrain/skills/boring-youtube-publisher)

## Skill Output:

**Output Type(s):** [Guidance, API calls, Configuration]

**Output Format:** [Markdown guidance with MCP tool call examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces instructions for account selection, media preparation, upload, publishing, and reporting.]

## Skill Version(s):

1.0.3 (source: server release metadata; artifact frontmatter states 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

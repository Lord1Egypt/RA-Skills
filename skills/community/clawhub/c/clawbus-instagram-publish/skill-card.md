## Description:

Publish Instagram images, Reels, and carousels, check Instagram publishing status, fetch recent Instagram direct messages, and send Instagram direct messages through a preconfigured MyBrandMetrics API connection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[clawbus](https://clawhub.ai/user/clawbus)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to publish Instagram media, check publish status, and handle Instagram direct-message workflows through MyBrandMetrics after connecting Instagram Insights.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can publish posts and send direct messages that affect an Instagram account.

Mitigation: Confirm the Instagram account, media source, post type, caption, conversation ID, and exact message text before execution.

Risk: Carousel publishing can fetch arbitrary remote URLs from the user's machine before upload.

Mitigation: Use trusted local files or trusted media URLs only, and avoid untrusted remote carousel items until URL validation and size limits are added.

Risk: Credentials may be exposed if API keys, connection IDs, or account IDs are stored carelessly.

Mitigation: Prefer environment variables or runtime arguments in shared workspaces and do not commit real credentials.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/clawbus/skills/clawbus-instagram-publish)
- [Configuration](references/configuration.md)
- [Publishing Examples](references/publishing-examples.md)
- [Clawbus Website](https://www.clawbus.com/)
- [MyBrandMetrics](https://mybrandmetrics.com/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON API responses from the bundled scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a MyBrandMetrics API key, Instagram connection ID, and for publishing workflows an Instagram account ID.]

## Skill Version(s):

1.1.5 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

Automates Douyin Creator video publishing in a browser by uploading a prepared video, filling title and description metadata, and submitting the post.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vincentlau2046-sudo](https://clawhub.ai/user/vincentlau2046-sudo)

### License/Terms of Use:

MIT-0

## Use Case:

Creators or operators with an already logged-in Douyin Creator browser session use this skill to publish prepared video files and associated title, description, and hashtag metadata.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can control a logged-in Douyin creator session and click the final publish button without explicit user confirmation.

Mitigation: Require manual review of the video, title, description, hashtags, account state, and an explicit confirmation before the final publish click.

Risk: Generated metadata can include built-in Qiqi child-story branding and fixed hashtags that may be inappropriate for other videos.

Mitigation: Review and edit all title, description, and hashtag fields before upload or publishing.

## Reference(s):

- [ClawHub skill release page](https://clawhub.ai/vincentlau2046-sudo/skills/douyin-browser-publish)
- [Douyin Creator upload page](https://creator.douyin.com/creator-micro/content/upload)
- [Douyin Creator video post page](https://creator.douyin.com/creator-micro/content/post/video)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration, Files]

**Output Format:** [Markdown instructions with JavaScript snippets and JSON metadata files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Helper scripts may generate publish_meta.json or publish queue JSON files.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

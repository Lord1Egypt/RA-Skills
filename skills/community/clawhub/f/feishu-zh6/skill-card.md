## Description:

Enables an agent to send Feishu text, local image, and local file messages to a configured recipient.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zh6](https://clawhub.ai/user/zh6)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators can use this skill when they want an agent to send Feishu messages, images, or document attachments to a configured recipient through the local workspace.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Messages or files could be sent to the wrong Feishu recipient.

Mitigation: Confirm the recipient ID before each send.

Risk: Sensitive business content or unintended local files could be sent through Feishu.

Mitigation: Review message text and file paths before sending.

Risk: Network image URLs cannot be sent directly.

Mitigation: Download network images to the local workspace before sending the local file path.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zh6/skills/feishu-zh6)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with message_tool examples and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference local files under ~/.openclaw/workspace/ for images and documents.]

## Skill Version(s):

1.0.5 (source: server evidence release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

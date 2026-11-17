## Description:

Feishu Assistant helps an agent send selected local images to Feishu chats, users, or message threads using configured Feishu bot credentials.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gushenjie](https://clawhub.ai/user/gushenjie)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to deliver generated or selected image files into Feishu group chats, direct messages, or replies from an automated workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses Feishu bot credentials and uploads the selected local image to Feishu.

Mitigation: Confirm the exact local file and destination chat, user, or message thread before sending.

Risk: The local RIFF/WebP validation weakness could allow a non-image RIFF file to be uploaded if selected.

Mitigation: Send only trusted image files and review questionable WebP or RIFF-based files before use.

## Reference(s):

- [Feishu Open Platform](https://open.feishu.cn/)
- [Feishu Assistant on ClawHub](https://clawhub.ai/gushenjie/skills/feishu-assistant)

## Skill Output:

**Output Type(s):** [Shell commands, Guidance, Configuration instructions]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The invoked script sends API requests to Feishu and prints status messages plus the Feishu API response JSON.]

## Skill Version(s):

1.1.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

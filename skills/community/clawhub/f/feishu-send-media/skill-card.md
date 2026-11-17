## Description:

Send images, files, audio, video, and other media to Feishu users or chats via direct message or group chat.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yaqiangsun](https://clawhub.ai/user/yaqiangsun)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to send local media files to Feishu users or group chats, including path-based attachments and base64 inline images.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Media may be sent or uploaded to Feishu Drive without a clear confirmation step.

Mitigation: Require explicit user confirmation of recipient, file path, and upload method before sending or using the Drive fallback.

Risk: Suggested permission changes can broaden local file readability.

Mitigation: Avoid changing permissions unless necessary, confirm before running permission changes, and clean up workspace copies after sending.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes path-based send instructions, base64 image fallback, Feishu Drive fallback, and verification checklist.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

Uploads images or videos to Feishu and sends them as chat media messages with image preview and video playback.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yinranphoto](https://clawhub.ai/user/yinranphoto)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to send local image or video files to Feishu chats through configured Feishu app credentials.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Credential selection and file validation are loose enough that the wrong Feishu account, recipient, or local file could be used.

Mitigation: Before use, verify the selected workspace, Feishu account binding, recipient ID, and file path; avoid sensitive paths and prefer a version with stricter media validation and explicit upload confirmation.

Risk: The skill reads local OpenClaw configuration and performs network uploads to Feishu at runtime.

Mitigation: Install only in trusted workspaces, keep Feishu app credentials scoped to the intended tenant, and review the command before executing it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yinranphoto/skills/feishu-media-sender)
- [Feishu Upload Image API](https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/reference/im-v1/image/create)
- [Feishu Upload File API](https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/reference/im-v1/file/create)
- [Feishu Send Message API](https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/reference/im-v1/message/create)

## Skill Output:

**Output Type(s):** [shell commands, configuration, guidance, text]

**Output Format:** [Markdown with inline shell commands; runtime command prints a Feishu API JSON response.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Sends media to an external Feishu chat as a side effect.]

## Skill Version(s):

1.0.0 (source: server release evidence and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

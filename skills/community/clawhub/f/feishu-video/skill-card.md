## Description:

Send Feishu (Lark) voice messages from OPUS audio, with included tooling that can also send MP4 video messages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yangmiok](https://clawhub.ai/user/yangmiok)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to convert local audio to Feishu-compatible OPUS and send it as a voice message to Feishu/Lark users or chats. The artifact also includes MP4 video message sending and large-video segmentation support.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The package includes video-sending behavior in addition to the stated voice-message purpose.

Mitigation: Review whether video support is intended before installation; remove or ignore the video script and documentation if only voice messaging is needed.

Risk: Examples show Feishu app secrets passed as command-line arguments, which may expose them through shell history or process listings.

Mitigation: Use least-privilege Feishu app scopes and prefer a secret manager or tightly controlled environment variables for app credentials.

Risk: Selected local media files are uploaded to Feishu/Lark.

Mitigation: Verify the media content and recipient before sending, and only upload files that are approved for the target Feishu/Lark workspace.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yangmiok/skills/feishu-video)
- [OpenClaw repository](https://github.com/anthropics/claw)
- [Feishu tenant access token endpoint](https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal)
- [Feishu file upload endpoint](https://open.feishu.cn/open-apis/im/v1/files)
- [Feishu message send endpoint](https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id)
- [Feishu image upload endpoint](https://open.feishu.cn/open-apis/im/v1/images)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and command output summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js 18+, ffmpeg, Feishu app credentials, target user or chat identifiers, and local media file paths.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

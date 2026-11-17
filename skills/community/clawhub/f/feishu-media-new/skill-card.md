## Description:

Helps agents send files, images, URL images, video, audio, voice messages, and compressed archives through Feishu.

This skill is ready for commercial/non-commercial use.

## Publisher:

[a1024708231](https://clawhub.ai/user/a1024708231)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to guide an agent through sending selected media to Feishu chats or users, including ordinary file sends, URL images, voice-message preparation, archives, and video uploads through curl.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected local files or remote media may be sent to an unintended Feishu recipient.

Mitigation: Require confirmation of the exact recipient, file path or URL, and message before upload or send.

Risk: Feishu app secrets and tenant access tokens may be exposed when using raw curl commands.

Mitigation: Use an approved secret-handling process and avoid pasting secrets into chat, command history, or logs.

Risk: Video sending relies on authenticated Feishu upload commands with message and resource permissions.

Mitigation: Review the generated commands before execution and use a Feishu app with only the required permissions.

## Reference(s):

- [Feishu Media ClawHub skill page](https://clawhub.ai/a1024708231/skills/feishu-media-new)
- [Feishu tenant access token API endpoint](https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal)
- [Feishu file upload API endpoint](https://open.feishu.cn/open-apis/im/v1/files)
- [Feishu message send API endpoint](https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance]

**Output Format:** [Markdown guidance with inline command examples and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose Feishu message-tool calls, ffmpeg conversion commands, archive commands, and curl-based upload commands.]

## Skill Version(s):

1.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

Send TTS audio or an existing audio file as a playable Feishu audio message, with optional transcript replies.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kylinr](https://clawhub.ai/user/kylinr)

### License/Terms of Use:


## Use Case:

Developers and agent users use this skill to generate text-to-speech audio or send an existing audio file to a Feishu chat as a playable audio message. It is useful for voice announcements, voice roll calls, and Feishu messaging workflows that need audio bubbles rather than file attachments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Stored Feishu bot credentials can be used to send content externally.

Mitigation: Install only for trusted agents and users, and limit credential access to Feishu chats where this behavior is expected.

Risk: The file mode can upload a local audio file to Feishu.

Mitigation: Expose file mode only when it is explicitly needed, and constrain acceptable file paths and recipients.

Risk: Transcript mode can post message text as a Feishu thread reply.

Mitigation: Avoid transcript mode for sensitive text unless posting the transcript is explicitly intended.

## Reference(s):

- [Feishu Audio Message on ClawHub](https://clawhub.ai/kylinr/skills/feishu-audio-msg)
- [Feishu file upload API](https://open.feishu.cn/open-apis/im/v1/files)
- [Feishu message send API](https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=chat_id)
- [Feishu tenant access token API](https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with bash commands and command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May send audio files and optional transcript text to Feishu through configured bot credentials.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

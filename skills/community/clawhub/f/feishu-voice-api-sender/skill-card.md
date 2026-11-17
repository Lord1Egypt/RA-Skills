## Description:

Sends Feishu voice messages through the official API by uploading OPUS audio with duration metadata and sending audio message content that includes file_key and duration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[54meteor](https://clawhub.ai/user/54meteor)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to send existing Ogg Opus audio or generate TTS audio and deliver it as a Feishu voice message with required duration metadata.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Feishu credentials are required and may be loaded automatically from an OpenClaw profile fallback.

Mitigation: Use a minimally privileged Feishu app, prefer explicit environment credentials, and avoid hardcoding app secrets in scripts.

Risk: Voice text and audio content may be processed by TTS tooling and sent through Feishu.

Mitigation: Do not send sensitive or regulated content unless the use is authorized for the relevant systems and data handling requirements.

Risk: The TTS workflow can execute an unpinned third-party edge-tts package through uvx at runtime.

Mitigation: Pin or preinstall reviewed TTS dependencies before using the TTS script.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/54meteor/skills/feishu-voice-api-sender)
- [Publisher profile](https://clawhub.ai/user/54meteor)
- [Feishu Open Platform app console](https://open.feishu.cn/app)
- [Feishu tenant access token API](https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal)
- [Feishu IM file upload API](https://open.feishu.cn/open-apis/im/v1/files)
- [Feishu IM message send API](https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown with bash command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance covers Feishu credential setup and script usage for existing audio files or TTS-generated voice messages.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

实现飞书语音消息的上传下载、语音转文字及文字转语音，支持与 ElevenLabs 语音服务集成。

This skill is ready for commercial/non-commercial use.

## Publisher:

[godzff](https://clawhub.ai/user/godzff)

### License/Terms of Use:


## Use Case:

Developers and automation builders use this skill to connect Feishu voice-message workflows with ElevenLabs speech recognition and text-to-speech. It provides setup, API usage, and format-conversion guidance for receiving, transcribing, generating, uploading, and sending voice messages.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Voice content and generated reply text may be sent to ElevenLabs during speech recognition or text-to-speech workflows.

Mitigation: Confirm organizational approval for Feishu voice content and generated text to be processed by ElevenLabs, and review ElevenLabs logging and retention settings before use.

Risk: Temporary audio files can remain in the workspace during download, conversion, and upload steps.

Mitigation: Add an operational cleanup process for temporary audio files after each workflow completes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/godzff/skills/feishu-voice-lobster)
- [Publisher profile](https://clawhub.ai/user/godzff)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, Configuration]

**Output Format:** [Markdown with bash and JavaScript examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Feishu app credentials, an ElevenLabs API key, and FFmpeg for Ogg/Opus conversion.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

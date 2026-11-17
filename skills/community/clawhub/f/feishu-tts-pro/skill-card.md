## Description:

将文字转换为语音并以飞书语音气泡消息发送，使用 Edge-TTS 生成中文语音、FFmpeg 转码为 ogg/opus，并上传到飞书作为 audio 类型消息。

This skill is ready for commercial/non-commercial use.

## Publisher:

[minybear](https://clawhub.ai/user/minybear)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill when an agent should reply by converting Chinese text into a Feishu voice bubble message for a configured recipient.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Input text is sent through Edge-TTS/Microsoft and Feishu as part of voice message delivery.

Mitigation: Avoid secrets or regulated personal data in messages unless the deployment has approved those services and data flows.

Risk: Feishu app credentials and recipient identifiers control who can send and receive generated audio.

Mitigation: Use a least-privilege Feishu app, protect FEISHU_APP_ID and FEISHU_APP_SECRET, and prefer an explicit recipient for sensitive sends.

Risk: Temporary audio files are created on the local machine during conversion.

Mitigation: Avoid shared machines unless temporary-file handling is reviewed and hardened for the deployment environment.

Risk: The runtime depends on the locally installed edge-tts package.

Mitigation: Pin edge-tts in the execution environment and review dependency updates before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/minybear/skills/feishu-tts-pro)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, audio messages, guidance]

**Output Format:** [Markdown guidance with shell commands and environment configuration; runtime output is a Feishu audio message.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js 18+, Python 3.8+ with edge-tts, FFmpeg, and Feishu app credentials.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

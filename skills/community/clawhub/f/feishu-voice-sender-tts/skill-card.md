## Description:

Feishu Voice Sender generates Feishu/Lark voice messages with TTS and can optionally transcribe explicitly provided OGG/Opus audio with ASR.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sunxq1017-hash](https://clawhub.ai/user/sunxq1017-hash)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to send explicit user-requested voice messages through Feishu/Lark, using Volcengine TTS and optional ASR for user-provided OGG/Opus audio.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send message text, original prompt context, generated audio, and explicitly provided .ogg audio files to Feishu/Lark and Volcengine services.

Mitigation: Install only when those third-party transfers are acceptable, avoid sensitive prompt context in user_input, and disclose the external service flow to operators.

Risk: Voice messages may be sent to an unintended Feishu/Lark recipient if the configured or supplied receive_id is wrong.

Mitigation: Confirm the recipient before sending and keep DEFAULT_RECEIVE_ID scoped to the intended destination.

Risk: ASR reads the explicitly provided local .ogg path and uploads the file contents for recognition.

Mitigation: Restrict ASR file paths and file sizes operationally, and use ASR only for user-approved audio files.

Risk: The dependency requirement allows a broad requests version range.

Mitigation: Prefer a pinned requests version during deployment and keep network request timeouts enabled.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sunxq1017-hash/skills/feishu-voice-sender-tts)
- [Volcengine console](https://console.volcengine.com/)
- [Feishu Open Platform](https://open.feishu.cn/)
- [Volcengine ASR flash recognize API](https://openspeech.bytedance.com/api/v3/auc/bigmodel/recognize/flash)

## Skill Output:

**Output Type(s):** [text, API calls, audio messages, configuration]

**Output Format:** [Function return values plus Feishu/Lark audio message delivery through external APIs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [TTS text is limited to 300 characters; ASR accepts explicitly provided .ogg files.]

## Skill Version(s):

2.0.2 (source: server release metadata and artifact changelog, released 2026-03-24)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

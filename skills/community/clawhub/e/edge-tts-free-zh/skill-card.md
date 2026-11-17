## Description:

Edge Tts configures OpenClaw to use Microsoft Edge TTS for text-to-speech with Chinese and English neural voices and no API key.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zx0018](https://clawhub.ai/user/zx0018)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to enable text-to-speech for assistant replies, including personal assistant, accessibility, multilingual, and cost-sensitive workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic text-to-speech can send generated reply text to Microsoft TTS services.

Mitigation: Avoid automatic TTS in sensitive chats unless sharing the text with Microsoft for speech synthesis is allowed.

Risk: The default Chinese voice or automatic playback behavior may be inappropriate for some channels or audiences.

Mitigation: Select an appropriate voice and use a less automatic trigger mode when the deployment context requires user control.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/zx0018/skills/edge-tts-free-zh)
- [OpenClaw TTS Documentation](https://docs.openclaw.ai/tts)
- [Microsoft Edge TTS Voice Gallery](https://speech.microsoft.com/portal/voicegallery)
- [Edge TTS Python Library](https://github.com/rany2/edge-tts)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown instructions with shell command blocks and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

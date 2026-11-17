## Description:

使用微软 Edge TTS 生成高质量中文语音，默认使用 XiaoxiaoNeural 语音。当用户需要语音回复时自动触发。

This skill is ready for commercial/non-commercial use.

## Publisher:

[nufeng1999](https://clawhub.ai/user/nufeng1999)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent operators use this skill to turn Chinese text responses into Microsoft Edge TTS voice output for QQ media delivery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Text provided for voice generation may be sent to Microsoft TTS services.

Mitigation: Use the skill only for content that may be processed by the external TTS service.

Risk: The documented edge-tts installation command uses an unpinned user-level install from a third-party package mirror.

Mitigation: Install edge-tts in an isolated environment from a trusted, pinned package source before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nufeng1999/skills/chinese-voice-skill)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Audio file references]

**Output Format:** [Markdown with qqmedia audio-file tags and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces WAV voice media using Chinese Microsoft Edge TTS voices when edge-tts is available.]

## Skill Version(s):

1.0.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

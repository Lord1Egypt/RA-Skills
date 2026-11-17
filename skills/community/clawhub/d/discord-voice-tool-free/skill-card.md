## Description:

基础 Discord 语音频道 AI 对话工具,支持加入/离开与本地语音识别合成。

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to operate a Discord voice-channel AI assistant that can join and leave voice channels, transcribe speech with local Whisper, and speak responses with local Kokoro TTS.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests command execution for live Discord voice-channel listening.

Mitigation: Review before installing, use it only for explicitly requested Discord voice-channel interactions, and verify the repository source before running npm or system install steps.

Risk: The trigger guidance is broad and could lead to use outside the intended Discord voice workflow.

Mitigation: Restrict use to Discord voice-channel join, leave, status, transcription, and TTS response tasks.

Risk: Privacy controls for voice transcription are under-disclosed.

Mitigation: Confirm participants know the bot listens and transcribes speech, and configure allowedUsers for any shared server.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/discord-voice-tool-free)
- [Publisher profile](https://clawhub.ai/user/thcjp)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces operational guidance for Discord voice-channel connection, local speech recognition, local speech synthesis, permissions, and troubleshooting.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

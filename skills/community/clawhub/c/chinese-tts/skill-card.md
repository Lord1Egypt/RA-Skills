## Description:

Generates Chinese text-to-speech audio and sends it as a Feishu voice message when users request voice, audio, narration, reading, or Chinese-language speech output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[waao666](https://clawhub.ai/user/waao666)

### License/Terms of Use:


## Use Case:

Developers and external users use this skill to convert Chinese text into Opus voice audio and send it as a Feishu voice message.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User-provided text may be sent to external TTS services and Feishu.

Mitigation: Use the skill only for explicit Chinese TTS or Feishu voice-message requests, avoid secrets or confidential content, and show a privacy notice before sending.

Risk: Broad voice or audio triggers can cause external TTS generation or Feishu sending without enough user confirmation.

Mitigation: Add an explicit confirmation step before any external TTS call or Feishu send.

## Reference(s):

- [Chinese TTS on ClawHub](https://clawhub.ai/waao666/skills/chinese-tts)

## Skill Output:

**Output Type(s):** [Shell commands, Files, Guidance]

**Output Format:** [Markdown guidance with bash commands; generated output is an Opus audio file path for Feishu.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires UTF-8 locale settings, Edge TTS, ffmpeg, and a Feishu-accessible workspace path.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

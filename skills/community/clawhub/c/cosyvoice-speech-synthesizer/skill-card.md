## Description:

Converts user-provided text into natural-sounding speech using Alibaba Cloud DashScope CosyVoice, with options for dialect, emotion, role, voice, speed, pitch, volume, and audio format.

This skill is ready for commercial/non-commercial use.

## Publisher:

[songguocola](https://clawhub.ai/user/songguocola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content creators use this skill to synthesize speech for narration, video voiceovers, podcasts, announcements, audiobooks, and dialect or character-style audio experiments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Text submitted for synthesis is sent to Alibaba Cloud DashScope under the user's API key.

Mitigation: Avoid secrets, regulated data, and confidential business text unless third-party processing is approved.

Risk: The synthesis script writes downloaded audio to a user-provided output path.

Mitigation: Choose output paths deliberately and review them before running the command.

## Reference(s):

- [Alibaba Cloud Model Studio CosyVoice Voice List](https://help.aliyun.com/zh/model-studio/cosyvoice-voice-list)
- [CosyVoice Speech Synthesizer on ClawHub](https://clawhub.ai/songguocola/skills/cosyvoice-speech-synthesizer)

## Skill Output:

**Output Type(s):** [Shell commands, Files, Guidance]

**Output Format:** [Markdown guidance with bash commands; generated audio files or audio URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires DASHSCOPE_API_KEY; downloaded audio is written to the user-selected output path unless URL-only mode is used.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

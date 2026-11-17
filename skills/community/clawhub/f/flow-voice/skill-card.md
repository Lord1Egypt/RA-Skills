## Description:

Clone any voice from a short audio sample and generate speech with it.

This skill is ready for commercial/non-commercial use.

## Publisher:

[windseeker1111](https://clawhub.ai/user/windseeker1111)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and creators use this skill to clone a permitted voice sample, generate spoken audio from text, and optionally add that voiceover to video.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can clone voices and generate speech that may be misused without consent.

Mitigation: Use only voice samples where rights and consent are clear, and review generated speech before distribution.

Risk: Saved voice profiles use .pkl serialization and may present local code-execution risk if loaded from untrusted sources.

Mitigation: Do not load untrusted profile files or profile names; run the skill in a sandbox until profile serialization and path validation are addressed.

Risk: Reference clips downloaded from third-party sources may have unclear rights or consent.

Mitigation: Avoid third-party audio clips unless licensing and speaker permission are verified.

## Reference(s):

- [FlowVoice ClawHub skill page](https://clawhub.ai/windseeker1111/skills/flow-voice)
- [LuxTTS repository](https://github.com/ysharma3501/LuxTTS)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and generated audio or video files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can create WAV audio, MP4 video with voiceover, and saved local voice profile files.]

## Skill Version(s):

1.1.0 (source: server release metadata, released 2026-03-23; artifact metadata lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

OpenClaw voice system that uses faster-whisper for inbound transcription and Edge TTS for outbound replies with cached reply audio and voice message handling after OpenClaw updates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stephenredmond-straiteis](https://clawhub.ai/user/stephenredmond-straiteis)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw operators use this skill to add speech transcription, spoken reply generation, and voice-message handling to OpenClaw workflows. It is also used to refresh the local voice stack after OpenClaw updates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Privacy or offline expectations may be wrong because hosted Edge TTS is used for outbound audio.

Mitigation: Require corrected privacy documentation and explicit opt-in for hosted Edge TTS before use.

Risk: Crafted audio filenames may expose users to code execution through unsafe filename handling.

Mitigation: Validate audio paths and use safe argument passing before processing user-supplied filenames.

Risk: Installation may make privileged host changes or install unpinned dependencies.

Mitigation: Review installer actions, pin dependencies, and require explicit approval before privileged package changes.

## Reference(s):

- [Voice Models Reference](references/voice_models.md)
- [ClawHub Skill Page](https://clawhub.ai/stephenredmond-straiteis/skills/edge-tts-voice-system)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, files, guidance]

**Output Format:** [Markdown guidance with Python and bash examples; runtime outputs include transcribed text, generated audio file paths, configuration files, and shell command output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Installs Python and shell wrappers, creates an OpenClaw TTS configuration, and caches generated outbound audio.]

## Skill Version(s):

2.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

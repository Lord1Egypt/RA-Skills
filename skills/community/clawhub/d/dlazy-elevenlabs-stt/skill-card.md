## Description:

Transcribes audio with ElevenLabs scribe_v1, with automatic language detection and optional speaker diarization.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dlazyai](https://clawhub.ai/user/dlazyai)

### License/Terms of Use:

MIT-0

## Use Case:

People who need searchable transcripts, subtitles, or meeting notes can submit audio for speech-to-text transcription, optionally with speaker labels.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review has medium confidence; CLI behavior and some authentication and invocation details were not verified.

Mitigation: Review the linked CLI project and confirm the documented command and authentication flow before installing or using it.

Risk: Audio supplied through a local file path is uploaded to dLazy media storage for hosted transcription.

Mitigation: Submit only recordings appropriate to send to the service, especially when they contain sensitive or personal information.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/dlazyai/skills/dlazy-elevenlabs-stt)
- [dLazy service website](https://dlazy.com)
- [CLI repository linked by the skill](https://github.com/dlazy-ai/cli)
- [@dlazy/cli on npm](https://www.npmjs.com/package/@dlazy/cli)

## Skill Output:

**Output Type(s):** [Text, JSON]

**Output Format:** [JSON containing the transcription text and optional speaker diarization]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include detected language and asynchronous task status.]

## Skill Version(s):

1.3.42 (source: server-resolved ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

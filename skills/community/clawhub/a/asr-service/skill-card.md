## Description:

SenseVoice-Small ASR transcribes audio, supports speaker diarization, and returns JSON, SRT, or VTT outputs through an InferFabric-managed service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vincentlau2046-sudo](https://clawhub.ai/user/vincentlau2046-sudo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to transcribe multilingual audio, generate subtitles, inspect service health, and optionally label speakers in meeting or media recordings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive audio is sent to the configured ASR HTTP endpoint.

Mitigation: Keep service.base_url pointed at a trusted loopback service unless a remote endpoint is explicitly approved, and confirm logging and retention behavior before processing sensitive recordings.

Risk: The skill can switch or start the ASR service through IFF.

Mitigation: Review the IFF service definition before use and run the skill in an isolated environment with only approved services configured.

Risk: Runtime dependencies and speech models may be installed or downloaded during setup or first use.

Mitigation: Pin dependencies where practical and pre-stage approved model artifacts in controlled environments.

## Reference(s):

- [ClawHub asr-service skill page](https://clawhub.ai/vincentlau2046-sudo/skills/asr-service)
- [FunASR SenseVoice-Small](https://github.com/modelscope/FunASR)
- [InferFabric](https://github.com/vincentlau2046-sudo/inferfabric)

## Skill Output:

**Output Type(s):** [Text, JSON, Subtitle text, Service status]

**Output Format:** [Plain text, JSON transcription data, SRT, VTT, or service status JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Verbose output can include language, duration, timestamped segments, and speaker labels.]

## Skill Version(s):

1.1.0 (source: frontmatter, release metadata, README version history)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

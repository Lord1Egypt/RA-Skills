## Description:

ClawVox is an ElevenLabs voice studio for OpenClaw that can generate speech, transcribe audio, clone voices, create sound effects, isolate voice tracks, dub audio, and manage voice libraries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[abhishek-official1](https://clawhub.ai/user/abhishek-official1)

### License/Terms of Use:

MIT

## Use Case:

Developers and OpenClaw users use this skill to add ElevenLabs-powered voice workflows to an assistant, including text-to-speech, speech-to-text, voice cloning, sound effects, voice isolation, dubbing, and voice library management.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Debug output can expose ElevenLabs API credentials or request details in logs.

Mitigation: Keep DEBUG unset when using real credentials and redact logs before sharing them.

Risk: Voice and audio files may contain private, regulated, or customer data and are sent to ElevenLabs for processing.

Mitigation: Use only approved data, review applicable privacy requirements, and avoid regulated recordings unless the environment is cleared for that use.

Risk: Voice cloning can reproduce a person's voice from uploaded samples.

Mitigation: Clone voices only from samples where consent and usage rights are documented.

Risk: Running shell scripts or tests from shared writable directories can expose credentials or files to local tampering.

Mitigation: Install and run the skill from a trusted directory with appropriate permissions after reviewing the scripts.

## Reference(s):

- [ElevenLabs Developers](https://elevenlabs.io/developers)
- [ElevenLabs API Documentation](https://elevenlabs.io/docs)
- [ElevenLabs Voice Library](https://elevenlabs.io/voice-library)
- [ElevenLabs Pricing](https://elevenlabs.io/pricing)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, audio files, API calls, guidance]

**Output Format:** [Markdown guidance with shell commands, JSON configuration examples, text transcripts, and generated audio files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl, jq, and ELEVENLABS_API_KEY; generated media is created through ElevenLabs API calls.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

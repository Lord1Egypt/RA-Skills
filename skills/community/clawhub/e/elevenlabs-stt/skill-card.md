## Description:

Transcribe audio files using ElevenLabs Speech-to-Text (Scribe v2).

This skill is ready for commercial/non-commercial use.

## Publisher:

[clawdbotborges](https://clawhub.ai/user/clawdbotborges)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent users use this skill to send local audio or video files to ElevenLabs Speech-to-Text and receive transcripts, with optional diarization, language selection, event tagging, and JSON timestamps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected audio files are uploaded to ElevenLabs for processing.

Mitigation: Use only recordings approved for third-party processing, and avoid confidential, regulated, or third-party audio unless approval is documented.

Risk: The ElevenLabs API key may be exposed locally through command-line argument handling.

Mitigation: Harden secret handling before broad deployment, restrict local process visibility, and rotate the API key if exposure is suspected.

Risk: The security verdict is suspicious.

Mitigation: Review and scan the skill before installation or deployment, using the ClawHub security summary as the authoritative risk source.

## Reference(s):

- [ElevenLabs Speech-to-Text](https://elevenlabs.io/speech-to-text)
- [ElevenLabs Speech-to-Text API Documentation](https://elevenlabs.io/docs/api-reference/speech-to-text)
- [ClawHub Skill Page](https://clawhub.ai/clawdbotborges/skills/elevenlabs-stt)
- [ClawHub Publisher Profile](https://clawhub.ai/user/clawdbotborges)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration]

**Output Format:** [Plain text transcript by default, or JSON with transcript details when requested.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can include speaker diarization, language code selection, audio event tagging, and word-level timestamps through script options.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

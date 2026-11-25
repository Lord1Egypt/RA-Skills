## Description:

Converts audio to text with ElevenLabs scribe_v1, with optional speaker diarization, for subtitles, transcripts, and meeting notes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dlazyai](https://clawhub.ai/user/dlazyai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other users can transcribe audio for subtitles, written transcripts, and meeting notes, with optional speaker labels.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security assessment reports a benign verdict with medium confidence and incomplete evidence, including mismatches between the stated transcription purpose and reported dLazy login and language options.

Mitigation: Review the complete instructions and confirm the CLI authentication and language options match the intended transcription service before use.

Risk: The skill documentation says local audio files are uploaded to dLazy media storage for processing.

Mitigation: Send only recordings approved for cloud processing, especially when they contain sensitive speech.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/dlazyai/skills/dlazy-elevenlabs-stt)
- [dLazy CLI homepage (metadata link)](https://github.com/dlazy-ai/cli)
- [@dlazy/cli on npm](https://www.npmjs.com/package/@dlazy/cli)
- [dLazy service](https://dlazy.com)

## Skill Output:

**Output Type(s):** [Text, JSON]

**Output Format:** [Structured JSON containing transcription results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Optional speaker diarization; asynchronous task status when requested.]

## Skill Version(s):

1.3.45 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

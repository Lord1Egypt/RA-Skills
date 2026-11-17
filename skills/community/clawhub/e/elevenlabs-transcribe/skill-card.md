## Description:

Transcribe audio to text using ElevenLabs Scribe, with support for batch transcription, realtime streaming from URLs, microphone input, and local files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[paulasjes](https://clawhub.ai/user/paulasjes)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to convert local audio files, live streams, or microphone input into transcripts. It is useful for meeting notes, voice input capture, media transcription, and workflows that need text or JSON output from audio.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected audio, live stream content, or microphone input is sent to ElevenLabs for transcription.

Mitigation: Use only audio appropriate for ElevenLabs terms and the user's compliance needs; avoid sensitive recordings unless approved.

Risk: The wrapper creates a local Python virtual environment and installs dependencies on first use.

Mitigation: Run the skill in an isolated environment and review dependency installation behavior before deployment.

Risk: The skill requires an ElevenLabs API key.

Mitigation: Use a scoped API key and avoid exposing it in logs, prompts, or shared shell history.

## Reference(s):

- [ElevenLabs Speech to Text](https://elevenlabs.io/speech-to-text)
- [ClawHub skill page](https://clawhub.ai/paulasjes/skills/elevenlabs-transcribe)

## Skill Output:

**Output Type(s):** [text, JSON]

**Output Format:** [Plain text transcripts by default, or JSON with transcript metadata when requested.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Realtime mode may emit partial and final transcript events; batch JSON output can include language metadata, word timestamps, and speaker identifiers.]

## Skill Version(s):

1.0.1 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

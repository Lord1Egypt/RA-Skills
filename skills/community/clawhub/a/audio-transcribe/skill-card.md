## Description:

Auto-transcribe voice messages locally using faster-whisper with selectable Whisper models and no API key required.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aktheknight](https://clawhub.ai/user/aktheknight)

### License/Terms of Use:


## Use Case:

Developers and bot operators use this skill to transcribe incoming voice messages and audio files locally, with model size adjustable for speed, memory use, and accuracy.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic transcription can expose voice-message content to people or systems that receive, store, or review transcripts.

Mitigation: Enable the skill only where transcription is acceptable to users, and document who can trigger transcription plus how transcripts are stored and deleted.

Risk: The skill depends on faster-whisper and model downloads, which introduce dependency and model supply-chain considerations.

Mitigation: Use a virtual environment, pin faster-whisper and its dependencies, and avoid running package installation as root.

## Reference(s):

- [ClawHub Audio Transcribe release](https://clawhub.ai/aktheknight/skills/audio-transcribe)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Plain text transcript with language metadata, plus Markdown usage guidance and shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Defaults to the small faster-whisper model on CPU with int8 compute; supported inputs include wav, mp3, ogg, m4a, flac, and opus audio files.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

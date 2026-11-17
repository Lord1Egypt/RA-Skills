## Description:

Local speech-to-text using faster-whisper with GPU acceleration support, word-level timestamps, and distilled model options.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jeminay](https://clawhub.ai/user/jeminay)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to transcribe local audio files into plain text or JSON, with optional model selection, language selection, word timestamps, and voice activity detection.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup downloads current Python packages and Whisper model assets into a local virtual environment.

Mitigation: Install in a controlled environment and pin and hash dependencies before setup when higher assurance is required.

Risk: Local audio transcription may process sensitive audio content.

Mitigation: Review local data handling requirements before processing audio files and keep generated transcripts within the approved environment.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration]

**Output Format:** [Plain text transcript or JSON transcript metadata, with shell commands and configuration guidance for setup and execution.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can write transcript output to a local file when requested.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

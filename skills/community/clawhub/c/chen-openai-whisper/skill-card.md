## Description:

Local speech-to-text with the Whisper CLI (no API key).

This skill is ready for commercial/non-commercial use.

## Publisher:

[cs995279497-byte](https://clawhub.ai/user/cs995279497-byte)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, engineers, and other agent users use this skill to produce local Whisper CLI transcription or translation commands for audio files without using an API key.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing the Homebrew openai-whisper package adds a local command-line dependency.

Mitigation: Confirm the package source and installation method before installing or running the generated commands.

Risk: Whisper may download models to the local cache and process local audio content.

Mitigation: Use the skill only with audio files intended for local transcription and confirm local storage is acceptable.

## Reference(s):

- [OpenAI Whisper](https://openai.com/research/whisper)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands assume the local whisper binary is installed; first use may download models to the user's local cache.]

## Skill Version(s):

1.0.0 (source: server release evidence and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

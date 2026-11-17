## Description:

On-device speech-to-text with Whisper and text-to-speech with Qwen3-TTS for macOS agents using the WhisperKit CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zachnagengast](https://clawhub.ai/user/zachnagengast)

### License/Terms of Use:


## Use Case:

Developers and agent builders use this skill to transcribe user-provided audio into text, generate spoken replies as audio files, and optionally expose local speech endpoints on macOS.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unsafe shell examples could expose users to command injection when passing model or user text to the CLI.

Mitigation: Agents should pass text through an argument-array process API or a securely created text file instead of interpolating untrusted text into shell templates.

Risk: Fixed temporary paths can allow temporary-file tampering during transcription or audio generation workflows.

Mitigation: Use securely created files in private temporary directories for audio inputs, text files, and generated reply audio.

Risk: The CLI can optionally start a localhost API server.

Mitigation: Enable the local server only when needed and keep access constrained to trusted local workflows.

## Reference(s):

- [WhisperKit documentation and model list](https://github.com/argmaxinc/WhisperKit)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and CLI usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local transcription text and guidance for generating .wav or .m4a audio reply files.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

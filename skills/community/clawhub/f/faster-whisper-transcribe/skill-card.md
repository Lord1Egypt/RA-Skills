## Description:

Transcribes local voice messages to text using Faster Whisper models for fast, privacy-focused speech recognition on audio files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kalmuraee](https://clawhub.ai/user/kalmuraee)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to transcribe local audio or voice message files into text while keeping processing on the local machine.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The install instructions use an unpinned package install with --break-system-packages.

Mitigation: Install in an isolated virtual environment or pipx-style environment, pin reviewed dependency versions, and avoid sudo or root privileges.

Risk: The voice-transcribe implementation is not included in the artifact, so the exact audio-processing behavior is uncertain.

Mitigation: Review the installed command and process only audio files from trusted or approved sources before using it in production workflows.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Markdown with inline bash code blocks and plain text transcription output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports tiny, base, small, and medium Faster Whisper model choices; larger models require more RAM.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

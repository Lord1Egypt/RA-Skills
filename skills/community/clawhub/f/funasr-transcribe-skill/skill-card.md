## Description:

Use when the user needs local speech-to-text transcription for audio files, especially Chinese or mixed Chinese-English audio, without relying on cloud transcription APIs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[limboinf](https://clawhub.ai/user/limboinf)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and external users use this skill to transcribe local audio files, especially Chinese or mixed Chinese-English recordings, into text without relying on a cloud ASR API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup and first use may download third-party packages, dependencies, and model files.

Mitigation: Install only when the configured PyPI mirror, FunASR dependencies, and model providers are trusted.

Risk: The skill creates a persistent local environment and may consume several GB of disk space.

Mitigation: Confirm local storage capacity and environment location before installation.

Risk: Transcription writes or overwrites a .txt file next to the selected audio file.

Mitigation: Run it on intended input files and review the output path before relying on the generated transcript.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/limboinf/skills/funasr-transcribe-skill)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance]

**Output Format:** [Plain text transcript plus Markdown guidance with shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Prints the transcript to stdout and writes a sibling .txt transcript file next to the selected audio file.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

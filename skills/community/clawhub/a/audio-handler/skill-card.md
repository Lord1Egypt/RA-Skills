## Description:

Read, analyze, convert, and process audio files (MP3, WAV, FLAC, AAC, M4A, OGG, OPUS, WMA).

This skill is ready for commercial/non-commercial use.

## Publisher:

[neckr0ik](https://clawhub.ai/user/neckr0ik)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to inspect audio metadata and prepare ffmpeg-based commands or bundled scripts for converting, trimming, normalizing, merging, and extracting audio.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The server security summary reports an artifact-backed command-injection risk through the conversion script's quality argument.

Mitigation: Only invoke convert_audio.sh with trusted, simple numeric quality values until the script validates numeric inputs and uses shell arrays for ffmpeg options.

Risk: Audio-processing commands can overwrite or create files as side effects.

Mitigation: Inspect proposed ffmpeg or shell commands before execution, especially when processing untrusted audio requests or file paths.

## Reference(s):

- [ClawHub Audio Handler Skill](https://clawhub.ai/neckr0ik/skills/audio-handler)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown with inline bash code blocks and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference local audio files and create converted, trimmed, normalized, merged, or extracted audio outputs when commands are executed.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

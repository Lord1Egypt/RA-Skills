## Description:

Process, enhance, and convert audio files with noise removal, normalization, format conversion, transcription, and podcast workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

Developers, creators, and agents use this skill to inspect, convert, clean up, normalize, transcribe, and package user-provided audio files with FFmpeg, ffprobe, and optional audio tooling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cloud transcription can send potentially sensitive recordings to a third-party service.

Mitigation: Use cloud transcription only with user awareness and approval, and prefer local transcription for sensitive audio.

Risk: API tokens used for optional transcription services can leak through shell history or source control.

Mitigation: Keep tokens in environment or secret-management tooling and avoid placing credentials directly in commands or files.

Risk: Optional Python and Conda installs may introduce unreviewed dependencies.

Mitigation: Install optional tools in a dedicated virtual environment or container with reviewed package versions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ivangdavila/skills/audio)
- [FFmpeg audio commands](artifact/commands.md)
- [Loudness standards by platform](artifact/loudness.md)
- [Podcast production workflow](artifact/podcast.md)
- [Transcription workflow](artifact/transcription.md)
- [AssemblyAI transcript API endpoint](https://api.assemblyai.com/v2/transcript)

## Skill Output:

**Output Type(s):** [guidance, shell commands, code, configuration, markdown]

**Output Format:** [Markdown guidance with shell command examples and optional code snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local audio-processing guidance for user-provided files; optional transcription paths may produce TXT, SRT, VTT, JSON, or TSV files.]

## Skill Version(s):

1.0.1 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

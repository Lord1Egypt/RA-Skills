## Description:

Generate or align SRT subtitles from audio, with transcript-to-audio alignment, timing cleanup, SRT quality checks, and subtitle preview video rendering.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sariel2018](https://clawhub.ai/user/sariel2018)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and media workflow users use this skill to generate SRT subtitles from audio, align a transcript to audio, inspect timing quality, and optionally create a burned-subtitle preview video.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Dependency installation and model runtime setup can change the local environment or download model assets.

Mitigation: Use a project-specific virtual environment, review requirements.txt before installation, and plan for faster-whisper model asset downloads on first use.

Risk: Subtitle and preview generation writes output files and may overwrite existing paths.

Mitigation: Choose output paths deliberately, keep generated files in a dedicated output directory, and preserve copies of important existing SRT or MP4 files.

Risk: Preview rendering depends on ffmpeg and processes local media files.

Mitigation: Verify ffmpeg is installed from a trusted source and run the workflow only on media files the user selected and is authorized to process.

## Reference(s):

- [Command Templates](references/command-templates.md)
- [Audio SRT Workflow ClawHub page](https://clawhub.ai/sariel2018/skills/audio-srt-workflow)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, Files]

**Output Format:** [Markdown guidance with inline bash commands and generated subtitle or preview file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces SRT subtitle files, timing diagnostics, and optional MP4 preview files from local audio, transcript, and subtitle inputs.]

## Skill Version(s):

0.1.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

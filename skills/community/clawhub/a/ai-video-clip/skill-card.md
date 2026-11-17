## Description:

AI Video Clip Assistant helps agents transcribe video, generate edit decision lists, render clips with FFmpeg, create subtitles, export social formats, and run post-render quality checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dwan25744](https://clawhub.ai/user/dwan25744)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, creators, and video operations teams use this skill to automate local video clipping workflows from transcription through EDL review, rendering, subtitles, social export, and quality checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: AI-influenced EDL files can cause FFmpeg to process unexpected source or subtitle paths.

Mitigation: Review every generated EDL before rendering and reject unexpected paths or edits.

Risk: Untrusted transcripts or media inputs can influence edit decisions and rendered outputs.

Mitigation: Use trusted media and transcripts for rendering workflows, and avoid rendering EDLs from untrusted transcript sources.

Risk: Local FFmpeg and ML transcription dependencies process media files on the host system.

Mitigation: Use an isolated virtual environment with pinned dependencies and run the skill only on chosen media files.

## Reference(s):

- [FFmpeg Cheatsheet](references/ffmpeg_cheatsheet.md)
- [Edit Decision List Schema](templates/edl_schema.json)
- [Clip Strategies](templates/clip_strategies.yaml)
- [Subtitle Styles](templates/subtitle_styles.json)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, JSON, Files]

**Output Format:** [Markdown guidance with command examples plus generated EDL JSON, subtitle files, video files, and quality reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs depend on local FFmpeg and ASR tools; EDL JSON should be reviewed before rendering.]

## Skill Version(s):

2.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

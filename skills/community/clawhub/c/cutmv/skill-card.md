## Description:

cutmv helps agents process local video and audio files with FFmpeg, including cutting, conversion, compression, frame or audio extraction, watermarking, and subtitle addition.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qiaotucodes](https://clawhub.ai/user/qiaotucodes)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent builders use cutmv to automate common local media-processing tasks such as trimming clips, reducing video size for messaging platforms, converting formats, extracting frames or audio, and adding watermarks or subtitles.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The info command uses an unsafe Python eval path when parsing media frame-rate data.

Mitigation: Avoid using the info command on untrusted media or with an untrusted FFmpeg/FFprobe in PATH until the parser is replaced with safe fraction parsing.

Risk: FFmpeg commands can overwrite existing output files without prompting.

Mitigation: Use new output filenames or keep backups before running processing commands.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/qiaotucodes/skills/cutmv)
- [Publisher profile](https://clawhub.ai/user/qiaotucodes)
- [FFmpeg downloads](https://ffmpeg.org/download.html)

## Skill Output:

**Output Type(s):** [Files, JSON, Shell commands, Guidance]

**Output Format:** [Processed media files with JSON status objects and Markdown or shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires FFmpeg and FFprobe on PATH; no external Python dependencies are declared.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

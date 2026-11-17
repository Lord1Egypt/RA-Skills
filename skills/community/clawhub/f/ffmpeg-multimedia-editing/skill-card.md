## Description:

Uses FFmpeg to edit local video and audio files, including trimming, concatenation, conversion, compression, subtitles, watermarks, screenshots, GIF conversion, speed changes, and audio processing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[showtimewalker](https://clawhub.ai/user/showtimewalker)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to direct an agent through local FFmpeg-based media editing tasks such as clipping, joining, transcoding, compressing, adding subtitles or watermarks, extracting audio, generating screenshots, and adjusting playback or audio properties.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs local FFmpeg commands and can overwrite user-selected output files without confirmation.

Mitigation: Use a dedicated output directory, avoid important filenames, and review every agent-proposed --output or --output-dir path before execution.

Risk: Media processing writes generated files to the local machine and may create large outputs.

Mitigation: Set OUTPUT_ROOT to a workspace or scratch location with sufficient disk space and review generated paths before running long operations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/showtimewalker/skills/ffmpeg-multimedia-editing)

## Skill Output:

**Output Type(s):** [Shell commands, Code, Configuration, JSON, Guidance]

**Output Format:** [Markdown guidance with shell commands; local scripts emit JSON result objects with media type, operation, local path, input path, and elapsed time.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires uv, ffmpeg, ffprobe, and Python; outputs are written under OUTPUT_ROOT outputs/ffmpeg by default.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

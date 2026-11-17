## Description:

Perform video and audio cutting, format conversion, compression, frame and audio extraction, audio replacement, text watermarking, and subtitle embedding using FFmpeg.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qiaotucodes](https://clawhub.ai/user/qiaotucodes)

### License/Terms of Use:

MIT License

## Use Case:

Developers and media workflow users can use this skill to prepare, inspect, and transform local video or audio files for messaging, platform compatibility, screenshots, watermarks, subtitles, or smaller file sizes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review reports that one metadata path can evaluate ffprobe frame-rate output as Python code.

Mitigation: Avoid running the info command on untrusted media until frame-rate parsing is replaced with safe numeric parsing.

Risk: The security review reports that output files can be overwritten by default.

Mitigation: Choose output paths carefully and avoid pointing commands at files that must be preserved.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/qiaotucodes/skills/cutmv-video-tool)
- [Publisher profile](https://clawhub.ai/user/qiaotucodes)
- [FFmpeg](https://ffmpeg.org/)
- [OpenClaw](https://github.com/openclaw/openclaw)
- [README.md](artifact/README.md)
- [SKILL.md](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Files, JSON, Shell commands, Code]

**Output Format:** [Generated media files, JSON status objects, Python API return values, and CLI output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires FFmpeg in PATH and reads from and writes to user-selected local media paths.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

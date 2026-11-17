## Description:

Expert audio/video processing with ffmpeg and ffprobe for converting, compressing, editing, analyzing, streaming, and processing audio or video files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kunalshah](https://clawhub.ai/user/kunalshah)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, media engineers, and content teams use this skill to generate ffmpeg and ffprobe guidance for media conversion, quality analysis, encoding presets, streaming setup, capture, repair, metadata handling, and validation workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated media commands may capture screen, microphone, webcam, or stream to remote destinations if run without confirming inputs and outputs.

Mitigation: Review device names, duration, output paths, and streaming destinations before execution.

Risk: Installation guidance may involve elevated package installs, static binaries, or mutable container images.

Mitigation: Prefer trusted package-manager installs and avoid unverified static binaries or unpinned images.

Risk: Batch processing and overwrite behavior can damage or replace media outputs.

Mitigation: Test on a small sample first, use separate output files or directories, and keep non-overwrite behavior unless replacement is intentional.

## Reference(s):

- [Codec & Container Compatibility Matrix](references/codecs-containers.md)
- [FFmpeg Flag Reference](references/ffmpeg-flags.md)
- [ffprobe Analysis Reference](references/ffprobe-analysis.md)
- [Platform-Specific Encoding Presets](assets/platform-presets.md)
- [Audio/Video Output Quality Checklist](assets/quality-checklist.md)
- [Feature Overview](assets/features.md)
- [Google Spatial Media Tool](https://github.com/google/spatial-media)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands, command explanations, and validation checks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands should be reviewed before execution and validated with ffprobe or ffmpeg checks.]

## Skill Version(s):

0.1.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

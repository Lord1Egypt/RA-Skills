## Description:

Extract frames or short clips from videos using ffmpeg.

This skill is ready for commercial/non-commercial use.

## Publisher:

[1yihui](https://clawhub.ai/user/1yihui)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content workflows can use this skill to extract a single frame from a local video file at the first frame, a timestamp, or a frame index for inspection, sharing, or thumbnail creation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on local ffmpeg execution and optional Homebrew installation.

Mitigation: Install only in environments where local ffmpeg use and package installation are acceptable.

Risk: The documentation says the skill can extract short clips, but the included script only writes a single frame image.

Mitigation: Use the provided script for frame extraction only, and add separate reviewed tooling before relying on clip extraction.

Risk: The script reads the video path and writes to the output path supplied by the user.

Mitigation: Run it only on intended local video files and choose output paths that are safe to create or overwrite.

## Reference(s):

- [ffmpeg](https://ffmpeg.org)
- [Dalong Video Frames on ClawHub](https://clawhub.ai/1yihui/skills/dalong-video-frames)
- [Publisher profile](https://clawhub.ai/user/1yihui)

## Skill Output:

**Output Type(s):** [Shell commands, Files, Guidance]

**Output Format:** [Markdown with inline bash commands and local image file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires ffmpeg and writes one frame image to the requested output path.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

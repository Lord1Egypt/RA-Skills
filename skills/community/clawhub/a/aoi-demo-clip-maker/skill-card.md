## Description:

Create and edit macOS hackathon demo clips via terminal commands to record, crop, trim, and apply presets using ffmpeg and ffprobe locally.

This skill is ready for commercial/non-commercial use.

## Publisher:

[edmonddantesj](https://clawhub.ai/user/edmonddantesj)

### License/Terms of Use:

MIT

## Use Case:

Developers and hackathon teams use this skill on macOS to create local demo clips by listing capture devices, recording the screen, cropping UI chrome, trimming footage, and applying a terminal preset.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Screen recording can capture sensitive windows, notifications, or other on-screen content.

Mitigation: Use only in a sanitized demo workspace, and close sensitive windows and notifications before recording.

Risk: FFmpeg crop and trim output paths can overwrite existing user-writable files.

Mitigation: Use simple local filenames, avoid agent-generated file paths, and verify output targets before running crop or trim commands.

## Reference(s):

- [AOI Demo Clip Maker on ClawHub](https://clawhub.ai/edmonddantesj/skills/aoi-demo-clip-maker)
- [AOI skills issue tracker](https://github.com/edmonddantesj/aoi-skills/issues)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and local CLI guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local macOS ffmpeg and ffprobe command guidance for recording, cropping, trimming, device listing, and terminal presets; it does not upload or post clips.]

## Skill Version(s):

0.1.4 (source: server release metadata and package.json; _meta.json reports 0.1.3)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
